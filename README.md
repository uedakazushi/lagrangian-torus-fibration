# Lagrangian torus fibrations on general-type surfaces
2026-11-21 / v2.0 — [研究方針](00_research_plan.md) · [研究ノート](research/notes.md) · [research-hub](https://github.com/uedakazushi/research-hub)

滑らかな一般型曲面 \(X_d\subset\mathbb P^3\)（\(d\ge5\)）の大域Lagrangian \(T^2\)-fibrationと、特異fiber・作用適合整数アフィン接着・KE退化との関係を研究する。**このリポジトリは複素次元2専用**。三次元の研究は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) へ分離した。

## 論文と役割
| 原稿 | 役割 | 組版の従来記録 |
| --- | --- | ---: |
| [主原稿](papers/surface-lagrangian-torus-fibration.tex) | 相対SNC構成・次数分割・分岐底・作用適合atlas | 130頁 |
| [五次整数接着](papers/quintic-integer-gluing.tex) | 指定K5データの整数条件・高分母支持・未解決の大域接着 | 201頁 |
| [Meridian surgery](papers/meridian-surgery.tex) | 閉corner circuitsの局所置換の障害 | 18頁 |
| [TeX研究ノート](papers/research-notes.tex) | 証明素材・残る条件の整理 | 65頁 |

## 主な到達点と残る課題
指定hyperplane Kähler classでの正則Lagrangian \(T^2\) と、分岐辺上の \(S^1\times(S^1\vee S^1)\)、面内のpinched torus、core上のlogarithmic Weinstein skeletonを扱う。五次は(cores, branch edges, nodes)=(5,10,50)、六次は(6,30,90)で、分岐辺数は無限個のfiberの個数ではない。通常のalmost toric fibrationを超える特異模型を用いるため、Leung–Symingtonの分類と矛盾しない。全大域接着の公表前監査はなお必要。

五次整数アフィン接着では、四rayの完全matching条件等を証明し、高分母の必要支持候補を \(G_{5,14},G_{5,16},G_{5,17}\) の3型・26標識まで絞った。ただし26は実現数ではなく、一般分母の剛性・三高係数の同時非負性や全支持型の大域接着は未解決。

KE退化との関連では、全閉triple cornerのactual局所GH収縮、短normal circleを用いる定量的二段階平均・共通作用周期の管理が主な到達点。**全neckの一様buffer、source・branch・core相対接着、全曲面のGH no-shortcutおよび既存fibrationとの大域的な一様適合性は未証明**。局所KE定理と大域GH収束を混同しない。先行研究の仮定と新規性の未確認点は主原稿序論と[研究ノート](research/notes.md)を参照。

## ビルドと再現
repo直下で `latexmk papers/surface-lagrangian-torus-fibration.tex`、`latexmk papers/quintic-integer-gluing.tex`、`latexmk papers/meridian-surgery.tex`。LuaLaTeX、LuaTeX-ja、日本語フォント、TikZを使用し、PDF/SyncTeXは `build/`。計算の入口は `python3 verification/run_current_checks.py`。ソースと証明書は `papers/sections/` と `verification/`。頁数・既存検算記録は分離前の記録であり、今日再組版・再検算した証拠ではない。PDFはGitで追跡しない。
