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

**先行研究との境界：** [三次元全体稿の文献比較](papers/threefold-fibration.tex)で、Mikhalkin (2004) の任意次数・次元のstratified **topological** torus fibration（Lagrangian性は各maximal cellの選ばれたfiber）、Leung–Wan (2009)の一般型における漸近special性、Evans–Mauri・AAKの局所／affine模型、Fernández de Bobadilla–Pełka (2026)の部分領域構成、Mak–Matessi–Ruddat–Zharkovの2026年Calabi–Yau講演発表を区別した。今回の大域目標は**一般型三次元の全regular fibersがLagrangianな全域構成**であって、一般型の位相的torus fibrationの初存在ではない。

三次元の大域接着は研究上の未解決課題。三次元の検算は `python3 verification/run_threefold_checks.py`。

**現行の数学的到達点：** [基底の位相・人工計量](papers/sections/paper/base_topology.tex)ではKE候補へのcell-like写像、次数5と6以上で異なる収縮速度、portal/no-shortcut条件と反例を証明。[三次元局所稿](papers/threefold-blocks.tex)ではnormal-trivial曲線とfocus–hyperbolic blockの構成に加え、**小さい管状補集合**の整数ホモロジーをLefschetz–Thom列から計算した（六次ではH₃にZ/4 torsion）。**実際のfocus blockの補集合**も整数homologyを計算し、六次では H₁=Z、H₂=Z⁸、H₃=Z⁵²⁷⊕Z/4、H₄=Z⁷ と得た。管状補集合とのfree rankの違いも説明した。Focus normal faceはunipotent torus bundleで基本群は整数Heisenberg群、六次closed-curve faceのBetti数は(1,8,15,15,8,1)。Focus基底の境界を回るloopはH₁(U)では消えるがH₁(V)=Zの原始生成元へ写ると証明した。**higher homology・基本群の境界包含写像、relative fillingとglobal Lagrangian接着は未解決**。補集合のEuler数は六次で−512だが、孤立非零Euler fiberが全て−1という仮定なしに「512個必要」とは主張しない。

最初に[研究方針](00_research_plan.md)、[移行範囲](research/migration.md)、[ソース対応](research/source-manifest.json)を確認する。

組版はルートで `latexmk`。現行10検査は `python3 verification/run_current_checks.py`。PDF/SyncTeX・再実行結果はbuild/。

正本はmain。[research-hub](https://github.com/uedakazushi/research-hub)。元Libraryは削除しない。
