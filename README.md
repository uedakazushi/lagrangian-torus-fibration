# Lagrangian torus fibrations

曲面側の第25版ソースを回収し、全文原稿と必要な検証資産を移行した。

| 原稿 | 頁数 | 役割 |
| --- | ---: | --- |
| [主稿](papers/lagrangian-torus-fibration.tex) | 96 | 相対SNC構成・次数分割・作用atlas |
| [整数接着](papers/quintic-integer-gluing.tex) | 201 | 指定K5データの整数条件と障害 |
| [局所置換](papers/meridian-surgery.tex) | 18 | meridian・四pants置換の障害 |
| [研究ノート](papers/research-notes.tex) | 65 | 証明素材・現在の残余 |
| [三次元局所稿](papers/threefold-blocks.tex) | 166（原版） | 第9版の全文TeX |
| [三次元全体稿](papers/threefold-fibration.tex) | 187（原版） | 第11稿の全文TeX |

三次元の大域接着は研究上の未解決課題。三次元の検算は `python3 verification/run_threefold_checks.py`。

**現行の数学的到達点：** [基底の位相・計量](papers/sections/paper/base_topology.tex)では、KE候補へのcell-like写像を用いる人工的長さ計量のdistortionが次数5で $\Theta(\varepsilon^2)$、次数6以上で $\Theta(\varepsilon)$ となることを証明（GH距離については上界）。実際の作用計量への十分条件は no-shortcut、各squareのlift、fiber/portal connectorの消失であり、局所比較だけでは不十分な明示反例も掲載。[三次元局所稿](papers/threefold-blocks.tex)にはnormal-trivial曲線の次数・種数制約と、未構成の補集合のEuler予算を整理。六次で補集合のEuler数は $-512$。孤立した非零Euler fiberがすべて $-1$ なら512個必要だが、一般の特異strataの構成は未解決。

最初に[研究方針](00_research_plan.md)、[移行範囲](research/migration.md)、[ソース対応](research/source-manifest.json)を確認する。

組版はルートで `latexmk`。現行10検査は `python3 verification/run_current_checks.py`。PDF/SyncTeX・再実行結果はbuild/。

正本はmain。[research-hub](https://github.com/uedakazushi/research-hub)。元Libraryは削除しない。
