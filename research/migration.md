# 現行ソースの由来と再現範囲

2026-11-21 / v2.2。複素次元2の正本は本repoの `main`。研究再開は `00_research_plan.md` → `AGENTS.md` → `research/ke-dependencies.md` → `research/notes.md` → 主原稿から行い、過去のLibrary bundle、旧リポジトリ名、旧会話の取得を前提にしない。

現行主原稿 `papers/surface-lagrangian-torus-fibration.tex` は日本語LuaLaTeXの本文を持ち、分割節は `papers/sections/paper/`、五次整数接着は `papers/sections/paper_arithmetic/`、meridianは `papers/sections/paper_surgery/`、TeXノートは `papers/sections/notes/` を利用する。ルートの旧互換性symlinkは存在しない。必要な検証コードと結果の正本は `verification/`。源流である2026-10-28のLibrary資料の識別子は `research/source-manifest.json` に残すが、現在のファイルや状態はその旧記録のハッシュではなくGitのmainと `research/validation.json` で確認する。

複素次元3の局所稿・大域稿・全分割節・図・専用検証資産は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) が正本。本repoに旧三次元作業のログや組版報告を現行成果として重複させない。

組版・検査：
```sh
python3 scripts/research_check.py preflight
python3 scripts/research_check.py static
python3 scripts/research_check.py tex
```
整数接着の変更を確認するときは `python3 scripts/research_check.py arithmetic`。LuaLaTeX、latexmk、LuaTeX-ja、日本語フォント、TikZ等に依存し、PDF/SyncTeXは追跡しない `build/` へ出力。現在の達成状況、未解決・確認済み範囲は `research/validation.json` と研究方針を参照する。Libraryの元資料は削除しない。
