# Lagrangian torus fibrations

**2026-11-20 / v1.4：五次の開正方形上でactual KE–Lagrangian collapseを証明。** [主稿](papers/lagrangian-torus-fibration.tex)の `ke:open-cell-collapse` は、関連KE稿の明示barrier＋Savinによるtensor漸近を用い、固定Kη=[η,1−η]²上でfiber intrinsic diameter O(L^−η)、raw-map誤差O(1/R)、内在距離で平坦KηへのGH収束を与える。全曲面のshortcut、全閉corner、singular fibersと既存大域fibrationの接着は未解決。証明・適用条件を点検し、新規性は未確認。現行改訂はLuaLaTeX基本資産不足により未組版。


曲面側の第25版ソースを回収し、全文原稿と必要な検証資産を移行した。

| 原稿 | 頁数 | 役割 |
| --- | ---: | --- |
| [主稿](papers/lagrangian-torus-fibration.tex) | 96 | 相対SNC構成・次数分割・作用atlas |
| [整数接着](papers/quintic-integer-gluing.tex) | 201 | 指定K5データの整数条件と障害 |
| [局所置換](papers/meridian-surgery.tex) | 18 | meridian・四pants置換の障害 |
| [研究ノート](papers/research-notes.tex) | 65 | 証明素材・現在の残余 |
| [三次元局所稿](papers/threefold-blocks.tex) | 166（原版） | 第9版の全文TeX |
| [三次元全体稿](papers/threefold-fibration.tex) | 187（原版） | 第11稿の全文TeX |

頁数は回収稿の記録。現行KE比較の改訂は、環境のLuaLaTeX基本資産不足により未組版。

**先行研究との境界：** [三次元全体稿の文献比較](papers/threefold-fibration.tex)で、Mikhalkin (2004) の任意次数・次元のstratified **topological** torus fibration（Lagrangian性は各maximal cellの選ばれたfiber）、Leung–Wan (2009)の一般型における漸近special性、Evans–Mauri・AAKの局所／affine模型、Fernández de Bobadilla–Pełka (2026)の部分領域構成、Mak–Matessi–Ruddat–Zharkovの2026年Calabi–Yau講演発表を区別した。今回の大域目標は**一般型三次元の全regular fibersがLagrangianな全域構成**であって、一般型の位相的torus fibrationの初存在ではない。

三次元の大域接着は研究上の未解決課題。三次元の検算は `python3 verification/run_threefold_checks.py`。

**現行の数学的到達点：** [基底の位相・人工計量](papers/sections/paper/base_topology.tex)ではKE候補へのcell-like写像、次数5と6以上で異なる収縮速度、portal/no-shortcut条件と反例を証明。[三次元局所稿](papers/threefold-blocks.tex)ではnormal-trivial曲線とfocus–hyperbolic blockの構成に加え、**小さい管状補集合**の整数ホモロジーをLefschetz–Thom列から計算した（六次ではH₃にZ/4 torsion）。**実際のfocus blockの補集合**も整数homologyを計算し、六次では H₁=Z、H₂=Z⁸、H₃=Z⁵²⁷⊕Z/4、H₄=Z⁷ と得た。管状補集合とのfree rankの違いも説明した。Focus normal faceはunipotent torus bundleで基本群は整数Heisenberg群、六次closed-curve faceのBetti数は(1,8,15,15,8,1)。Focus基底の境界を回るloopはH₁(U)では消えるがH₁(V)=Zの原始生成元へ写ると証明した。**higher homology・基本群の境界包含写像、relative fillingとglobal Lagrangian接着は未解決**。補集合のEuler数は六次で−512だが、孤立非零Euler fiberが全て−1という仮定なしに「512個必要」とは主張しない。

**局所Lagrangian collapseへの前進（2026-11-20 / v1.3）：** [主稿の新節](papers/sections/paper/ke_fiber_compatibility.tex)で、短いtorus作用の平均化とMoser法から、$C^0$ tensor比較だけで局所Lagrangian fibrationのambient fiber diameterを制御した。三重点の全閉cubical cornerをhexagonで実現し、raw-depth mapとの誤差も評価した。Actual KEへの応用は全phaseを含むmoving領域でのtensor比較付きであり、大域collapseの証明は未完成。関連KE研究ではbounded densityからtensor比較への推論を反例により訂正したため、その比較を別途証明することが現在の解析課題である。方法の先行研究はRuan (arXiv:math/0309177v2, §3)。

**KE極限との関係：** 径の尺度 $R_t=\log(-\log|t|^2)$ での候補は $X_t\to B_d(T)\to\mathcal C_d$。KE側の解析仮定に加え、GH近似写像とLagrangian fibrationの一様な適合性が必要。[基底比較の命題](papers/sections/paper/base_topology.tex)はその条件から全fiberのambient直径収縮を導く。Actual適合性は未証明。Zhangの局所負KE collapseと我々の非Q-factorial sourceの違いを[研究ノート](research/notes.md)・主稿序論に明記。

**複素次元2の先行研究とfiber型：** [主原稿](papers/lagrangian-torus-fibration.tex)の全平面構成では、正則T²のほか、三価分岐辺上のS¹×(S¹∨S¹)、面内の一重pinched torus、core頂点上のlogarithmic Weinstein skeletonが現れる。五次は(cores, branch edges, isolated nodes)=(5,10,50)、六次は(6,30,90)。分岐辺の本数は無限個ある辺上ファイバーの個数とは違う。Mikhalkin (2004)のstratified topological fibration、Smith (2001)の追加仮定付き制限定理、Leung–Symington (2010)のalmost toric分類、Evans–Mauri (2021)のpants局所構成、Zhang (2025)の一般型のpants分解と区別し、[現行研究ノート](research/notes.md)に引用と適用範囲を記載。

最初に[研究方針](00_research_plan.md)、[移行範囲](research/migration.md)、[ソース対応](research/source-manifest.json)を確認する。

組版はルートで `latexmk`。現行10検査は `python3 verification/run_current_checks.py`。PDF/SyncTeX・再実行結果はbuild/。

正本はmain。[research-hub](https://github.com/uedakazushi/research-hub)。元Libraryは削除しない。
