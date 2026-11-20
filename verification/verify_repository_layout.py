#!/usr/bin/env python3
"""Static integrity checks for the symlink-free surface research layout.

This checks source and path consistency, not the mathematical verification
scripts, LuaLaTeX compilation, or the correctness of the theorems.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAMES = ("paper", "paper_arithmetic", "paper_surgery", "notes")
CURRENT_DIRS = tuple(ROOT / "papers" / "sections" / x for x in LEGACY_NAMES)
ROOT_TEX = (
    "surface-lagrangian-torus-fibration.tex",
    "quintic-integer-gluing.tex",
    "meridian-surgery.tex",
    "research-notes.tex",
)
CURRENT_PROOFS = (
    "four_ray_matching_v25.tex",
    "g514_five_node_exclusion_v25.tex",
    "g514_central_matching_v25.tex",
    "high_d_axis_endpoints_v25.tex",
    "degenerate_divisor_reduction_v25.tex",
)
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
LEGACY_PY_RE = re.compile(
    r"""(['"])(paper|paper_arithmetic|paper_surgery|notes)(?:/|\1)"""
)


def main() -> None:
    for name in LEGACY_NAMES:
        legacy = ROOT / name
        assert not legacy.exists() and not legacy.is_symlink(), (
            f"Unexpected old root directory or symlink: {legacy}"
        )
    for path in CURRENT_DIRS:
        assert path.is_dir() and not path.is_symlink(), path

    root_tex_count = 0
    for name in ROOT_TEX:
        tex = ROOT / "papers" / name
        assert tex.is_file(), tex
        text = tex.read_text(encoding="utf-8")
        assert "\\begin{document}" in text, f"Empty main TeX: {tex}"
        for ref in INPUT_RE.findall(text):
            if ref == "local-fonts.tex":  # optional machine-local override
                continue
            candidate = ROOT / "papers" / ref
            assert candidate.is_file() or candidate.with_suffix(".tex").is_file(), (
                f"Missing TeX input: {tex}: {ref}"
            )
        root_tex_count += 1

    scripts = list((ROOT / "verification").rglob("*.py"))
    for path in scripts:
        content = path.read_text(encoding="utf-8")
        ast.parse(content, filename=str(path))
        hit = None if path.name == "verify_repository_layout.py" else LEGACY_PY_RE.search(content)
        assert hit is None, f"Legacy active path in {path}: {hit.group() if hit else ''}"

    for proof in CURRENT_PROOFS:
        candidate = ROOT / "papers/sections/paper" / proof
        assert candidate.is_file(), candidate

    assert (ROOT / "verification/run_current_checks.py").is_file()
    print(f"PASS: {root_tex_count} main TeX files, {len(scripts)} Python sources, "
          "five current proofs; no root symlinks")


if __name__ == "__main__":
    main()
