# Two-sided spine. `spine` with no hubx -> hub-x is COMPUTED from the left half's
# width, so wider left-side labels (e.g. Chinese) push the whole centre right,
# per language, automatically. side=left/right is inherited by the subtree.

spine

[softskills] side=left grade=junior
  [communication]  grade=junior
  [thinking]       grade=junior
  [responsibility] grade=junior
  [selforg]        grade=junior

[langsyntax] side=right grade=junior
  [stl] grade=junior
    [iostream]       grade=junior
    [datetime]       grade=junior
    [containers]     grade=junior
    [iterators]      grade=junior
    [algorithms]     grade=junior
    [multithreading] grade=middle
  [templates] grade=junior
  [standards] grade=junior

[langtools] side=right grade=junior
  [debugger]     grade=junior
  [buildsystems] grade=junior
