#!/usr/bin/env python3
"""Local setup and explicit verification stages; no install, network or Git writes.

These checks verify executability and document integrity, not KE estimates,
global gluing, novelty, or mathematical completeness.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = (
    "surface-lagrangian-torus-fibration",
    "quintic-integer-gluing",
    "meridian-surgery",
    "research-notes",
)
TEX_INPUTS = (
    "luatexja-fontspec.sty", "geometry.sty", "amsmath.sty", "amssymb.sty",
    "amsthm.sty", "mathtools.sty", "booktabs.sty", "tabularx.sty",
    "array.sty", "longtable.sty", "enumitem.sty", "xcolor.sty", "tikz.sty",
    "microtype.sty", "hyperref.sty", "fancyhdr.sty",
)


def capture(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False, timeout=30)


def run(args: list[str]) -> int:
    print("RUN: " + " ".join(args), flush=True)
    return subprocess.run(args, cwd=ROOT, check=False).returncode


def preflight(require_tex: bool, ke_repo: Path | None) -> bool:
    ok = sys.version_info >= (3, 10)
    print(f"{'PASS' if ok else 'FAIL'}: Python {sys.version.split()[0]} (requires >= 3.10)")
    for relative in ("AGENTS.md", "00_research_plan.md", "research/notes.md",
                     "research/ke-dependencies.md", ".latexmkrc",
                     "papers/surface-lagrangian-torus-fibration.tex",
                     "verification/verify_repository_layout.py",
                     "verification/run_current_checks.py"):
        exists = (ROOT / relative).is_file()
        print(f"{'PASS' if exists else 'FAIL'}: {relative}")
        ok = exists and ok
    if shutil.which("git"):
        head = capture(["git", "rev-parse", "HEAD"])
        if head.returncode:
            print("FAIL: checkout has no readable Git HEAD")
            ok = False
        else:
            branch = capture(["git", "branch", "--show-current"]).stdout.strip()
            changes = capture(["git", "status", "--porcelain"]).stdout.splitlines()
            print(f"INFO: HEAD {head.stdout.strip()}, branch {branch or '(detached)'}; "
                  f"{len(changes)} changed/untracked paths; changes preserved")
    else:
        print("FAIL: git is unavailable")
        ok = False

    tex_ok = True
    for name in ("latexmk", "lualatex", "kpsewhich"):
        executable = shutil.which(name)
        tex_ok = bool(executable) and tex_ok
        print(f"{'PASS' if executable else 'MISSING'}: {name}")
    if shutil.which("kpsewhich"):
        for name in TEX_INPUTS:
            result = capture(["kpsewhich", name])
            found = result.returncode == 0 and bool(result.stdout.strip())
            tex_ok = found and tex_ok
            if not found:
                print(f"MISSING: TeX input {name}")
        print("INFO: font and format availability is conclusively checked by the tex stage")
    if not tex_ok:
        print("ACTION: prepare LuaLaTeX, latexmk, LuaTeX-ja, Japanese fonts, "
              "LaTeX extras and TikZ in the environment; see research/cloud-codex.md")
    if require_tex:
        ok = tex_ok and ok

    candidate = ke_repo or ROOT.parent / "kaehler-einstein-degeneration"
    if candidate.is_dir() and shutil.which("git"):
        dep_head = capture(["git", "rev-parse", "HEAD"], candidate)
        if dep_head.returncode == 0:
            print(f"INFO: KE dependency checkout {candidate}, HEAD {dep_head.stdout.strip()}")
            print("INFO: compare its statements and assumptions with research/ke-dependencies.md")
        else:
            print("WARN: KE dependency directory is not a readable Git checkout")
    else:
        print("WARN: no local KE dependency checkout; read/obtain it before using its results")
    print("INFO: repository access, push rights, mathematical proofs and Cloud task launch "
          "are not checked by preflight")
    return ok


def build(paper: str, ke_repo: Path | None) -> int:
    if not preflight(True, ke_repo):
        return 1
    code = run(["latexmk", "-norc", "-r", ".latexmkrc", f"papers/{paper}.tex"])
    if code:
        return code
    missing = [suffix for suffix in (".pdf", ".synctex.gz", ".log")
               if not (ROOT / "build" / f"{paper}{suffix}").is_file()]
    if missing:
        print(f"FAIL: expected build outputs are missing: {', '.join(missing)}")
        return 1
    log = (ROOT / "build" / f"{paper}.log").read_text(encoding="utf-8", errors="replace")
    bad = re.findall(r"^.*(?:undefined references|undefined citations|multiply defined|"
                     r"Citation .+ undefined|Reference .+ undefined|Missing character:).*$",
                     log, flags=re.MULTILINE | re.IGNORECASE)
    if bad:
        print("FAIL: unresolved references/citations, duplicate labels, or missing glyphs:")
        print("\n".join(bad))
        return 1
    overfull = len(re.findall(r"Overfull \\[hv]box", log))
    print(f"PASS: PDF, SyncTeX and log in build/; {overfull} overfull box warnings "
          "(inspect changed pages separately)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("setup", "preflight", "static", "tex", "arithmetic"))
    parser.add_argument("--require-tex", action="store_true",
                        help="make missing TeX dependencies fail setup/preflight")
    parser.add_argument("--paper", choices=PAPERS, default=PAPERS[0],
                        help="main document to build in the tex stage")
    parser.add_argument("--ke-repo", type=Path,
                        help="existing KE checkout (default: sibling repository)")
    args = parser.parse_args()
    try:
        if args.stage == "setup":
            (ROOT / "build").mkdir(exist_ok=True)
            print("INFO: ignored build/ directory is ready; no packages or settings modified")
            return 0 if preflight(args.require_tex, args.ke_repo) else 1
        if args.stage == "preflight":
            return 0 if preflight(args.require_tex, args.ke_repo) else 1
        if args.stage == "static":
            code = run([sys.executable, "verification/verify_repository_layout.py"])
            return code or run(["git", "diff", "--check"])
        if args.stage == "tex":
            return build(args.paper, args.ke_repo)
        print("INFO: this stage checks the existing quintic arithmetic package, "
              "not KE/GH analysis", flush=True)
        return run([sys.executable, "verification/run_current_checks.py"])
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
