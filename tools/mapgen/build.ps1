<#
.SYNOPSIS
  Generate a draw.io map fragment from a language-neutral DSL + per-language
  translation files. One rigid text source -> one .drawio.svg per language.

.DESCRIPTION
  Reads <Dir>/structure.dsl (topology, grades, hints, frames, spine) and
  <Dir>/<lang>.tsv (id <TAB> text), computes physical layout per language
  (widths from text metrics, column packing, bus routing), emits mxGraph XML,
  renders it through the draw.io CLI, and restores the light-dark background.

  The DSL fixes the *logical* layout (rows, columns, order, grade, anchors);
  the generator computes the *physical* layout (x, width, waypoints, frame
  size) so the same structure reflows correctly for each language's text.

.EXAMPLE
  pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/examples/stl
  pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/examples/spine -Langs en,zh

.NOTES
  Windows only: uses System.Drawing for text metrics and the draw.io desktop
  CLI for rendering. See README.md for the DSL grammar and known gaps.
#>
param(
  [Parameter(Mandatory=$true)][string]$Dir,      # folder with structure.dsl + <lang>.tsv
  [string[]]$Langs = @('en','ru','zh'),
  [string]$OutDir = $null,                        # defaults to $Dir
  [string]$DrawioCli = "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe",
  [string]$Font = "Microsoft YaHei"               # covers Latin + Cyrillic + CJK
)
Add-Type -AssemblyName System.Drawing
if(-not $OutDir){ $OutDir = $Dir }
if(-not (Test-Path $OutDir)){ New-Item -ItemType Directory -Force $OutDir | Out-Null }
if(-not (Test-Path $DrawioCli)){ throw "draw.io CLI not found: $DrawioCli (override with -DrawioCli)" }
$structPath = Join-Path $Dir "structure.dsl"
if(-not (Test-Path $structPath)){ throw "structure.dsl not found in $Dir" }

# ---- layout constants (match the map's conventions; see README) ----
$H=30; $PITCH=60; $GAP=40; $MARGIN=40; $FONTSIZE=20; $PADX=12
$HINT_W=320; $HINT_GAP=90; $LINEH=24; $PADV=9; $SPINE_STUB=90
$grades = @{ junior="#96BB7C"; middle="#FAD586"; senior="#BBCCEE"; optional="#CCEEFF" }
$HINT_FILL = "#FFD5E4"; $FRAME_FILL = "#F5F5F5"

# ---- text measurement ----
$bmp=New-Object System.Drawing.Bitmap(2,2); $gfx=[System.Drawing.Graphics]::FromImage($bmp)
$fontObj=New-Object System.Drawing.Font($Font,$FONTSIZE,[System.Drawing.GraphicsUnit]::Pixel)
$sf=[System.Drawing.StringFormat]::GenericTypographic
function Measure-Width([string]$t){ [double]($gfx.MeasureString($t,$fontObj,[int]::MaxValue,$sf)).Width }
function Wrap([string]$text,[double]$maxw){
  # Tokenize so wrapping works for CJK too: Latin words stay whole, spaces are
  # explicit tokens, each CJK char is its own token (CJK has no spaces).
  $tokens=@(); $buf=""
  foreach($ch in $text.ToCharArray()){
    $code=[int]$ch
    $isCJK = ($code -ge 0x3000 -and $code -le 0x9FFF) -or ($code -ge 0xF900 -and $code -le 0xFAFF) -or ($code -ge 0xFF00 -and $code -le 0xFFEF)
    if($ch -eq ' '){ if($buf -ne ''){$tokens+=$buf;$buf=''}; $tokens+=' ' }
    elseif($isCJK){ if($buf -ne ''){$tokens+=$buf;$buf=''}; $tokens+=[string]$ch }
    else { $buf+=$ch }
  }
  if($buf -ne ''){$tokens+=$buf}
  $lines=@(); $cur=""
  foreach($tk in $tokens){
    $try = if($tk -eq ' '){"$cur "}else{"$cur$tk"}
    if((Measure-Width $try) -le $maxw -or $cur -eq ""){ $cur=$try }
    else { $lines+=$cur.TrimEnd(); $cur = if($tk -eq ' '){""}else{$tk} }
  }
  if($cur.Trim() -ne ""){ $lines+=$cur.TrimEnd() }
  if($lines.Count -eq 0){ $lines=@($text) }
  return ,$lines
}

# ---- parse DSL: nodes (by indent) + hint / frame / spine directives ----
$lines=[IO.File]::ReadAllLines($structPath,[Text.Encoding]::UTF8)
$nodes=@{}; $order=@(); $stack=@{}; $hints=@(); $frames=@(); $SPINE=$null
foreach($ln in $lines){
  $t=$ln.Trim()
  if($t -eq "" -or $t.StartsWith("#")){ continue }
  if($t -match '^spine\b'){
    $SPINE=@{ hubx=$null; gate=$null; header=$null; center=$null }   # null hubx -> computed
    if($t -match 'hubx=(\d+)'){ $SPINE.hubx=[double]$Matches[1] }
    if($t -match 'gate=(\d+)'){ $SPINE.gate=[double]$Matches[1] }
    if($t -match 'header=(\S+)'){ $SPINE.header=$Matches[1] }
    if($t -match 'center=(\S+)'){ $SPINE.center=$Matches[1] }   # node on the trunk; halves centre on it
    continue
  }
  if($t -match '^frame\s+\[([^\]]+)\]'){
    $fid=$Matches[1]; $ftitle=$null; $fcont=$null
    if($t -match 'title=(\S+)'){ $ftitle=$Matches[1] }
    if($t -match 'contains=(\S+)'){ $fcont=($Matches[1] -split ',') | ForEach-Object { $_.Trim() } }
    $frames += [ordered]@{ id=$fid; titleKey=$ftitle; contains=$fcont }
    continue
  }
  if($t -match '^hint\s+\[([^\]]+)\]\s*->\s*(.+)$'){
    $hid=$Matches[1]; $tg=($Matches[2] -split ',') | ForEach-Object { $_.Trim() }
    $hints += [ordered]@{ id=$hid; targets=$tg }
    continue
  }
  $indent=($ln.Length-$ln.TrimStart().Length); $depth=[int]($indent/2)
  if($ln -notmatch '\[([^\]]+)\]'){ continue }
  $id=$Matches[1]
  $grade="junior"; if($ln -match 'grade=(\w+)'){ $grade=$Matches[1] }
  $parent=$null; if($depth -gt 0){ $parent=$stack[$depth-1] }
  $side="right"; if($ln -match 'side=(left|right)'){ $side=$Matches[1] } elseif($parent){ $side=$nodes[$parent].side }
  $nodes[$id]=[ordered]@{ id=$id; grade=$grade; depth=$depth; parent=$parent; side=$side; children=@() }
  if($parent){ $nodes[$parent].children+=$id }
  $stack[$depth]=$id; $order+=$id
}

function XmlEsc([string]$s){ $s.Replace('&','&amp;').Replace('<','&lt;').Replace('>','&gt;').Replace('"','&quot;') }
function Descendants($rootId){ $acc=@($rootId); foreach($c in $nodes[$rootId].children){ $acc += (Descendants $c) }; return $acc }

function Build-Lang([string]$lang){
  $trPath = Join-Path $Dir "$lang.tsv"
  if(-not (Test-Path $trPath)){ "  $lang SKIPPED (no $lang.tsv)"; return }
  $tr=@{}
  foreach($l in [IO.File]::ReadAllLines($trPath,[Text.Encoding]::UTF8)){
    if($l.Trim() -eq ""){continue}; $p=$l -split "`t",2; $tr[$p[0]]=$p[1]
  }
  # node text + width (physical width derived from this language's text)
  foreach($id in $order){
    $x=$tr[$id]; if(-not $x){$x=$id}
    $nodes[$id].text=$x
    $nodes[$id].width=[math]::Ceiling((Measure-Width $x)+2*$PADX)
  }
  # vertical layout: leaves sequential (row pitch), parent = avg(children)
  $script:row=0
  function Assign-Y($id){
    $n=$nodes[$id]
    if($n.children.Count -eq 0){ $n.cy=$MARGIN+$script:row*$PITCH+$H/2; $script:row++ }
    else{ foreach($c in $n.children){ Assign-Y $c }; $n.cy=($nodes[$n.children[0]].cy+$nodes[$n.children[-1]].cy)/2 }
  }
  # left and right sections each stack from the top, so the two halves run in
  # parallel down the trunk instead of one long sequential column.
  $script:row=0
  foreach($id in $order){ if($nodes[$id].depth -eq 0 -and $nodes[$id].side -ne 'left'){ Assign-Y $id } }
  $script:row=0
  foreach($id in $order){ if($nodes[$id].depth -eq 0 -and $nodes[$id].side -eq 'left'){ Assign-Y $id } }
  # a centre node (spine center=<id>) sits on the trunk at the vertical middle;
  # both halves are shifted so their midpoints line up on it.
  $centerW=0; $centerY=$null
  if($SPINE -and $SPINE.center){
    $ctext = if($tr[$SPINE.center]){ $tr[$SPINE.center] } else { $SPINE.center }
    $centerW=[math]::Ceiling((Measure-Width $ctext)+2*$PADX)
    $rt=1e18;$rb=-1e18;$lt=1e18;$lb=-1e18
    foreach($id in $order){ $n=$nodes[$id]
      if($n.side -eq 'left'){ if($n.cy-$H/2 -lt $lt){$lt=$n.cy-$H/2}; if($n.cy+$H/2 -gt $lb){$lb=$n.cy+$H/2} }
      else                 { if($n.cy-$H/2 -lt $rt){$rt=$n.cy-$H/2}; if($n.cy+$H/2 -gt $rb){$rb=$n.cy+$H/2} } }
    $rH=[math]::Max(0,$rb-$rt); $lH=[math]::Max(0,$lb-$lt)
    $centerY=$MARGIN+[math]::Max($rH,$lH)/2
    if($rb -gt $rt){ $dy=$centerY-($rt+$rb)/2; foreach($id in $order){ if($nodes[$id].side -ne 'left'){$nodes[$id].cy+=$dy} } }
    if($lb -gt $lt){ $dy=$centerY-($lt+$lb)/2; foreach($id in $order){ if($nodes[$id].side -eq 'left'){$nodes[$id].cy+=$dy} } }
  }
  # horizontal layout: LOCAL packing — each child sits just right of its own
  # parent (bus in the gap), so the tree stays compact instead of aligning every
  # depth to one global column (which sprawls on a deep map). With a spine the
  # right half grows right from hub-x and the left half grows left; hub-x is
  # computed from the left half's ACTUAL extent, so it shifts per language.
  function Layout-X($id,$x,$dir){
    $nodes[$id].x=$x; $n=$nodes[$id]
    foreach($c in $n.children){
      $cx = if($dir -eq 1){ $n.x+$n.width+2*$GAP } else { $n.x-2*$GAP-$nodes[$c].width }
      Layout-X $c $cx $dir
    }
  }
  $effStub = if($centerW -gt 0){ $centerW/2 + 2*$GAP } else { $SPINE_STUB }
  $leftRoots=@(); $rightRoots=@()
  foreach($id in $order){ if($nodes[$id].depth -eq 0){ if($nodes[$id].side -eq 'left'){$leftRoots+=$id}else{$rightRoots+=$id} } }
  if($SPINE){
    $hubx = if($SPINE.hubx){ [double]$SPINE.hubx } else { 460.0 }
    if($leftRoots.Count -gt 0){
      foreach($id in $leftRoots){ Layout-X $id (-$effStub-$nodes[$id].width) -1 }   # relative to hub=0
      $leftmost=1e18; foreach($id in $order){ if($nodes[$id].side -eq 'left' -and $nodes[$id].x -lt $leftmost){$leftmost=$nodes[$id].x} }
      if(-not $SPINE.hubx){ $hubx=$MARGIN-$leftmost }
      foreach($id in $order){ if($nodes[$id].side -eq 'left'){ $nodes[$id].x += $hubx } }
    }
    foreach($id in $rightRoots){ Layout-X $id ($hubx+$effStub) 1 }
  } else {
    foreach($id in $rightRoots){ Layout-X $id $MARGIN 1 }
  }
  # hints: wrap text + size box, centre on target span (phase 1) ...
  foreach($hn in $hints){
    $txt=$tr[$hn.id]; if(-not $txt){$txt=$hn.id}
    $wl=Wrap $txt ($HINT_W-2*$PADX)
    $hn.lines=$wl; $hn.width=$HINT_W
    $hn.height=[math]::Max($H, $wl.Count*$LINEH+2*$PADV)
    $cys=@(); $hn.side='right'
    foreach($tid in $hn.targets){ if($nodes[$tid]){ $cys+=$nodes[$tid].cy; $hn.side=$nodes[$tid].side } }
    $hn.cy=(($cys|Measure-Object -Minimum).Minimum + ($cys|Measure-Object -Maximum).Maximum)/2
  }
  # ... then x = clear EVERY node whose vertical span overlaps the box (2D clearance).
  # A hint for the left branch goes to the LEFT of its targets (mirror).
  foreach($hn in $hints){
    $hy0=$hn.cy-$hn.height/2; $hy1=$hn.cy+$hn.height/2
    if($hn.side -eq 'left'){
      $lt=1e18
      foreach($id in $order){ $n=$nodes[$id]
        if(($n.cy+$H/2) -ge $hy0 -and ($n.cy-$H/2) -le $hy1 -and $n.x -lt $lt){ $lt=$n.x } }
      $hn.x=$lt-$HINT_GAP-$hn.width
    } else {
      $rt=0
      foreach($id in $order){ $n=$nodes[$id]
        if(($n.cy+$H/2) -ge $hy0 -and ($n.cy-$H/2) -le $hy1 -and ($n.x+$n.width) -gt $rt){ $rt=$n.x+$n.width } }
      $hn.x=$rt+$HINT_GAP
    }
  }

  # ---- emit mxGraph XML ----
  $sb=New-Object Text.StringBuilder
  [void]$sb.AppendLine('<mxfile host="mapgen"><diagram name="frag" id="frag"><mxGraphModel dx="0" dy="0" grid="0" pageWidth="850" pageHeight="1100" background="#ffffff" math="0" shadow="0"><root>')
  [void]$sb.AppendLine('<mxCell id="0"/><mxCell id="1" parent="0"/>')
  # frames first (behind everything): grow-to-fit bbox over member nodes
  $FPAD=24; $FTITLE=50
  foreach($fr in $frames){
    if($fr.contains){ $members=@(); foreach($r in $fr.contains){ $members += (Descendants $r) } } else { $members=$order }
    $minX=1e9;$minY=1e9;$maxX=-1e9;$maxY=-1e9
    foreach($id in $members){ $n=$nodes[$id]
      if($n.x -lt $minX){$minX=$n.x}; if(($n.x+$n.width) -gt $maxX){$maxX=$n.x+$n.width}
      if(($n.cy-$H/2) -lt $minY){$minY=$n.cy-$H/2}; if(($n.cy+$H/2) -gt $maxY){$maxY=$n.cy+$H/2} }
    $fx=$minX-$FPAD; $fy=$minY-$FTITLE; $fw=($maxX-$minX)+2*$FPAD; $fh=($maxY-$minY)+$FTITLE+$FPAD
    $title=""; if($fr.titleKey -and $tr[$fr.titleKey]){ $title=$tr[$fr.titleKey] }
    $st="rounded=0;html=0;fillColor=$FRAME_FILL;strokeColor=#000000;strokeWidth=1;fontSize=28;fontColor=#000000;fontFamily=$Font;verticalAlign=top;align=center;fontStyle=1;container=0;"
    [void]$sb.AppendLine("<mxCell id=""$($fr.id)"" parent=""1"" vertex=""1"" style=""$st"" value=""$(XmlEsc $title)""><mxGeometry x=""$fx"" y=""$fy"" width=""$fw"" height=""$fh"" as=""geometry""/></mxCell>")
  }
  # spine: fixed trunk at hub-x + left-of-gate header (drawn before nodes)
  if($SPINE){
    $gate=$SPINE.gate    # $hubx is the per-language value computed during layout
    $rootIds=@(); foreach($id in $order){ if($nodes[$id].depth -eq 0){ $rootIds+=$id } }
    $rc=@(); foreach($id in $rootIds){ $rc+=$nodes[$id].cy }
    $minR=($rc|Measure-Object -Minimum).Minimum; $maxR=($rc|Measure-Object -Maximum).Maximum
    $hcy=($minR+$maxR)/2
    $top=1e9;$bot=-1e9
    foreach($id in $order){ if(($nodes[$id].cy-$H/2) -lt $top){$top=$nodes[$id].cy-$H/2}; if(($nodes[$id].cy+$H/2) -gt $bot){$bot=$nodes[$id].cy+$H/2} }
    $y0=[math]::Min($minR,$hcy); $y1=[math]::Max($maxR,$hcy)
    if($gate -and $gate -gt 0){
      [void]$sb.AppendLine("<mxCell id=""_gate"" parent=""1"" edge=""1"" style=""endArrow=none;html=0;strokeColor=#999999;dashed=1;""><mxGeometry relative=""1"" as=""geometry""><mxPoint x=""$gate"" y=""$($top-20)"" as=""sourcePoint""/><mxPoint x=""$gate"" y=""$($bot+20)"" as=""targetPoint""/></mxGeometry></mxCell>")
      [void]$sb.AppendLine("<mxCell id=""_gatelbl"" parent=""1"" vertex=""1"" style=""text;html=0;fontSize=14;fontColor=#999999;align=center;"" value=""gate""><mxGeometry x=""$($gate-20)"" y=""$($top-44)"" width=""40"" height=""18"" as=""geometry""/></mxCell>")
    }
    [void]$sb.AppendLine("<mxCell id=""_trunk"" parent=""1"" edge=""1"" style=""endArrow=none;html=0;strokeColor=#000000;strokeWidth=1;""><mxGeometry relative=""1"" as=""geometry""><mxPoint x=""$hubx"" y=""$y0"" as=""sourcePoint""/><mxPoint x=""$hubx"" y=""$y1"" as=""targetPoint""/></mxGeometry></mxCell>")
    if($SPINE.header){
      $htext=$tr[$SPINE.header]; if(-not $htext){$htext=$SPINE.header}
      $hw=[math]::Ceiling((Measure-Width $htext)+2*$PADX); $hx=$gate-$hw-24; $hy=$hcy-$H/2
      $st="rounded=0;html=0;fillColor=#96BB7C;strokeColor=#000000;strokeWidth=1;fontSize=$FONTSIZE;fontColor=#000000;fontFamily=$Font;verticalAlign=middle;align=center;"
      [void]$sb.AppendLine("<mxCell id=""_hdr"" parent=""1"" vertex=""1"" style=""$st"" value=""$(XmlEsc $htext)""><mxGeometry x=""$hx"" y=""$hy"" width=""$hw"" height=""$H"" as=""geometry""/></mxCell>")
      [void]$sb.AppendLine("<mxCell id=""_hdrstub"" parent=""1"" edge=""1"" source=""_hdr"" style=""edgeStyle=none;html=0;endArrow=none;strokeColor=#000000;exitX=1;exitY=0.5;exitDx=0;exitDy=0;""><mxGeometry relative=""1"" as=""geometry""><mxPoint x=""$hubx"" y=""$hcy"" as=""targetPoint""/></mxGeometry></mxCell>")
    }
    foreach($id in $rootIds){
      $r=$nodes[$id]; $entry = if($r.side -eq 'left'){1}else{0}   # left roots attach on their right side
      [void]$sb.AppendLine("<mxCell id=""_s_$id"" parent=""1"" edge=""1"" target=""$id"" style=""edgeStyle=none;html=0;endArrow=none;strokeColor=#000000;entryX=$entry;entryY=0.5;entryDx=0;entryDy=0;""><mxGeometry relative=""1"" as=""geometry""><mxPoint x=""$hubx"" y=""$($r.cy)"" as=""sourcePoint""/></mxGeometry></mxCell>")
    }
    if($SPINE.center){   # central node on the trunk, at the vertical middle
      $ct = if($tr[$SPINE.center]){ $tr[$SPINE.center] } else { $SPINE.center }
      $st="rounded=1;html=0;fillColor=#FFE5B9;strokeColor=#000000;strokeWidth=1;fontSize=$FONTSIZE;fontColor=#000000;fontFamily=$Font;verticalAlign=middle;align=center;fontStyle=1;"
      [void]$sb.AppendLine("<mxCell id=""_center"" parent=""1"" vertex=""1"" style=""$st"" value=""$(XmlEsc $ct)""><mxGeometry x=""$($hubx-$centerW/2)"" y=""$($centerY-$H/2)"" width=""$centerW"" height=""$H"" as=""geometry""/></mxCell>")
    }
  }
  # nodes
  foreach($id in $order){
    $n=$nodes[$id]; $fill=$grades[$n.grade]; $y=$n.cy-$H/2
    $st="rounded=0;html=0;fillColor=$fill;strokeColor=#000000;strokeWidth=1;fontSize=$FONTSIZE;fontColor=#000000;fontFamily=$Font;verticalAlign=middle;align=center;"
    [void]$sb.AppendLine("<mxCell id=""$id"" parent=""1"" vertex=""1"" style=""$st"" value=""$(XmlEsc $n.text)""><mxGeometry x=""$($n.x)"" y=""$y"" width=""$($n.width)"" height=""$H"" as=""geometry""/></mxCell>")
  }
  # hint boxes (breaks already inserted by Wrap; no whiteSpace=wrap so draw.io
  # doesn't re-wrap and mis-break CJK)
  foreach($hn in $hints){
    $y=$hn.cy-$hn.height/2
    $val=(@($hn.lines) | ForEach-Object { XmlEsc $_ }) -join '&#xa;'
    $st="rounded=0;html=0;fillColor=$HINT_FILL;strokeColor=#000000;strokeWidth=1;fontSize=$FONTSIZE;fontColor=#000000;fontFamily=$Font;verticalAlign=middle;align=center;"
    [void]$sb.AppendLine("<mxCell id=""$($hn.id)"" parent=""1"" vertex=""1"" style=""$st"" value=""$val""><mxGeometry x=""$($hn.x)"" y=""$y"" width=""$($hn.width)"" height=""$($hn.height)"" as=""geometry""/></mxCell>")
  }
  # parent -> child edges (orthogonal via the column bus). Left-side parents exit
  # on their left and the bus sits to their left (mirror of the right side).
  foreach($id in $order){
    $n=$nodes[$id]; if($n.children.Count -eq 0){continue}
    if($n.side -eq 'left'){ $busx=$n.x-$GAP; $ex=0; $en=1 } else { $busx=$n.x+$n.width+$GAP; $ex=1; $en=0 }
    foreach($cid in $n.children){
      $c=$nodes[$cid]
      $st="edgeStyle=none;html=0;strokeColor=#000000;strokeWidth=1;startArrow=none;endArrow=none;rounded=0;exitX=$ex;exitY=0.5;exitDx=0;exitDy=0;entryX=$en;entryY=0.5;entryDx=0;entryDy=0;"
      [void]$sb.AppendLine("<mxCell id=""e_$cid"" parent=""1"" edge=""1"" source=""$id"" target=""$cid"" style=""$st""><mxGeometry relative=""1"" as=""geometry""><Array as=""points""><mxPoint x=""$busx"" y=""$($n.cy)""/><mxPoint x=""$busx"" y=""$($c.cy)""/></Array></mxGeometry></mxCell>")
    }
  }
  # hint arrows: curved, from the hint's inner edge to each target's facing edge
  # (right branch: hint-left -> target-right; left branch: hint-right -> target-left)
  foreach($hn in $hints){
    if($hn.side -eq 'left'){ $ex=1; $en=0 } else { $ex=0; $en=1 }
    foreach($tid in $hn.targets){
      if(-not $nodes[$tid]){continue}
      $st="edgeStyle=none;html=0;strokeColor=#000000;strokeWidth=1;startArrow=none;endArrow=block;endFill=1;curved=1;exitX=$ex;exitY=0.5;exitDx=0;exitDy=0;entryX=$en;entryY=0.5;entryDx=0;entryDy=0;"
      [void]$sb.AppendLine("<mxCell id=""a_$($hn.id)_$tid"" parent=""1"" edge=""1"" source=""$($hn.id)"" target=""$tid"" style=""$st""><mxGeometry relative=""1"" as=""geometry""/></mxCell>")
    }
  }
  [void]$sb.AppendLine('</root></mxGraphModel></diagram></mxfile>')

  $drawio = Join-Path $OutDir "$lang.drawio"
  [IO.File]::WriteAllText($drawio,$sb.ToString(),(New-Object Text.UTF8Encoding($false)))
  $svg = Join-Path $OutDir "$lang.drawio.svg"
  if(Test-Path $svg){ Remove-Item $svg }
  & $DrawioCli -x -f svg -e -u --svg-theme auto -o $svg $drawio 2>&1 | Out-Null
  Start-Sleep -Milliseconds 500
  if(Test-Path $svg){
    # the CLI exports a transparent bg; restore the map's light-dark background
    $tt=[IO.File]::ReadAllText($svg,[Text.Encoding]::UTF8)
    $tt=$tt.Replace('background: transparent; background-color: transparent;','background: #ffffff; background-color: light-dark(#ffffff, #121212);')
    [IO.File]::WriteAllText($svg,$tt,(New-Object Text.UTF8Encoding($false)))
    "  $lang -> $lang.drawio.svg ($((Get-Item $svg).Length) bytes)"
  } else { "  $lang EXPORT FAILED" }
}

"mapgen: $Dir"
foreach($lang in $Langs){ Build-Lang $lang }
"done"
