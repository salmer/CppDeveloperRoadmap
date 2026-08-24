#!/usr/bin/env python3
"""
setup -- get this machine ready to build the roadmap maps.

Installs what the generator needs and reports what it cannot install for you, so a
contributor can go from a fresh clone to a working build with one command:

    python tools/mapgen/setup.py            # install into the current interpreter
    python tools/mapgen/setup.py --venv     # create tools/mapgen/.venv and install there

It handles Pillow (the text-metrics library) and checks the two things that must be
installed by hand: a metrics font and the draw.io desktop CLI. Nothing here is required to
*edit* the map source -- only to render it. `build.py` re-verifies everything anyway;
this script is the one that fixes what it can.
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS = os.path.join(HERE, "requirements.txt")
VENV_DIR = os.path.join(HERE, ".venv")

sys.path.insert(0, HERE)
import build            # reuse the same font/CLI detection the build uses

# how to install the draw.io desktop app, per platform (it renders the .drawio.svg)
DRAWIO_HINTS = {
    "win32":  "winget install --id JGraph.Draw -e",
    "darwin": "brew install --cask drawio",
    "linux":  "sudo snap install drawio     # or the .deb/.AppImage from the site",
}
DRAWIO_URL = "https://www.drawio.com/blog/diagrams-offline"

FONT_HINTS = {
    "win32":  "Microsoft YaHei ships with Windows; if it is missing, install any CJK font "
              "and pass --font",
    "darwin": "PingFang ships with macOS; otherwise `brew install --cask font-noto-sans-cjk`",
    "linux":  "sudo apt-get install fonts-noto-cjk",
}


def platform_hint(table):
    return table.get(sys.platform, table["linux"])


def run(cmd):
    print("    $ " + " ".join(cmd))
    sys.stdout.flush()          # so the child's output lands after ours, not interleaved
    return subprocess.run(cmd).returncode == 0


def in_venv():
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def venv_python(root):
    p = os.path.join(root, "Scripts", "python.exe")
    return p if os.path.exists(p) else os.path.join(root, "bin", "python")


def activate_hint(root):
    rel = os.path.relpath(root, os.getcwd()).replace(os.sep, "/")
    if sys.platform == "win32":
        win = rel.replace("/", "\\")
        return rf"{win}\Scripts\Activate.ps1"
    return f"source {rel}/bin/activate"


def make_venv():
    """Create tools/mapgen/.venv if absent; return its interpreter."""
    py = venv_python(VENV_DIR)
    if os.path.exists(py):
        print(f"  ok   virtualenv already exists: {os.path.relpath(VENV_DIR, os.getcwd())}")
        return py
    print(f"  ..   creating virtualenv in {os.path.relpath(VENV_DIR, os.getcwd())}")
    if not run([sys.executable, "-m", "venv", VENV_DIR]):
        return None
    return venv_python(VENV_DIR)


def install_pillow(python):
    """Install Pillow into `python`. Returns True if importable afterwards."""
    probe = [python, "-c", "import PIL, sys; sys.stdout.write(PIL.__version__)"]
    got = subprocess.run(probe, capture_output=True, text=True)
    if got.returncode == 0:
        print(f"  ok   Pillow {got.stdout.strip()} already installed")
        return True
    print("  ..   installing Pillow")
    if not run([python, "-m", "pip", "install", "--quiet", "-r", REQUIREMENTS]):
        return False
    return subprocess.run(probe, capture_output=True, text=True).returncode == 0


def main():
    ap = argparse.ArgumentParser(description="Prepare this machine to build the roadmap maps.")
    ap.add_argument("--venv", action="store_true",
                    help=f"create {os.path.relpath(VENV_DIR, os.getcwd())} and install into it")
    args = ap.parse_args()

    print("mapgen setup\n")
    manual = []          # things this script cannot install for you

    if sys.version_info < (3, 8):
        sys.exit(f"  Python 3.8+ required (running {sys.version.split()[0]})")
    print(f"  ok   Python {sys.version.split()[0]}")

    # --- 1. the Python dependency -------------------------------------------------
    if args.venv:
        python = make_venv()
        if not python:
            sys.exit("  could not create the virtualenv")
    else:
        python = sys.executable
        if not in_venv():
            print("  note installing into the interpreter you ran this with, which is NOT a\n"
                  "       virtualenv. Re-run with --venv for an isolated one.")
    if not install_pillow(python):
        sys.exit("  Pillow could not be installed -- install it by hand:\n"
                 f"      {python} -m pip install -r {REQUIREMENTS}")

    # --- 2. things that must be installed by hand ---------------------------------
    font = next((p for p in build.FONT_CANDIDATES if os.path.exists(p)), None)
    if font:
        print(f"  ok   metrics font {os.path.basename(font)}")
    else:
        manual.append("A CJK-capable metrics font (measures label widths).\n"
                      f"      {platform_hint(FONT_HINTS)}")

    cli = build.find_drawio_cli()
    if cli:
        print(f"  ok   draw.io CLI {cli}")
    else:
        manual.append("The draw.io desktop app (renders the .drawio.svg).\n"
                      f"      {platform_hint(DRAWIO_HINTS)}\n"
                      f"      or download it from {DRAWIO_URL}\n"
                      "      Already installed somewhere unusual? Pass --drawio-cli <path>.")

    # --- 3. what to do next -------------------------------------------------------
    build_cmd = "python tools/mapgen/build.py --dir tools/mapgen/roadmap --deploy --check"
    if args.venv:
        build_cmd = f"{activate_hint(VENV_DIR)}\n      {build_cmd}"

    if manual:
        print("\n  Still needed (install these yourself):\n")
        for m in manual:
            print("    - " + m)
        print("\n  Everything else is ready. You can already edit the map source; you just\n"
              "  cannot render it until the above is installed. If you would rather not\n"
              "  install it, edit tools/mapgen/roadmap/ and say so in your PR -- a\n"
              "  maintainer will regenerate the maps.")
        return 1

    print("\n  All set. Build the maps with:\n\n      " + build_cmd + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
