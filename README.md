# Lagrangian torus fibrations

**2026-11-21 / v1.8：三次元focus補集合の全境界写像・第二ホモトピー・巡回被覆を決定。**

[補集合の位相](papers/sections/threefold/local_blocks/focus_exterior_topology.tex)では、構成済みのactual product block U=C'×K_cに対してnormal exterior E≃S¹∨S²∨S³、π₁(V)=Zと両側の全整数境界写像を証明した。境界のnormal loops a,bと曲線loopsはVで消え、focus基底のboundary lift tが生成元となる。H₂(∂U)→H₂(V)の像の指数はe=d−2である。

さらにΛ=Z[τ,τ⁻¹]、g=(d−3)(d−4)/2としてπ₂(V)≅Λ^(2g+1)⊕Λ/(e(τ−1))を求めた。m重巡回被覆のH₂はZ^{m(2g+1)+1}⊕(Z/e)^{m−1}。六次ではπ₂(V)=Λ⁷⊕Λ/(4(τ−1))、二重被覆のH₂=Z¹⁵⊕Z/4となる。これらは具体的な積埋込に対する結果で、relative symplectic fillingと三次元大域Lagrangian fibrationは未完成である。証明を相互点検し、`python3 verification/verify_focus_exterior_topology.py --json` の整数検算を実行した。包括的新規性と形式証明は未確認・未実施。

**曲面のnormal averagingにも前進。** [二段階構成](papers/sections/paper/ke_staged_neck_averaging.tex)に、actual circleの長さεだけからMoser trajectory長をc_w εに抑える補題と、同じcompact集合Kをsource/imageの両方に含める条件δ>(2c_w+1/2)εを加えた。通常kernelでc_w=π/(2√3)。この評価に不変背景やtensor二側比較は不要である。既存の共通normal circle・全marked periodsの保持、共通buffer上のHamiltonian比較も維持する。

関連KE稿ではsource-free固定compact base上のexact bundle coordinates、canonical primitive、円平均後の共通moment intervalを証明した。**全neckのflow buffer、各triple endの同一作用とreduced leavesの同時整合は未解決**である。Fixed-endの収束はmoving endsのtensor比較ではない。

**全閉triple cornerの局所GH収縮。** [閉cornerの距離定理](papers/sections/paper/ke_closed_corner_gh.tex)の `ke:closed-corner-gh` と `ke:closed-corner-protected-gh` は、固定した任意のd≥5について、三枚の閉unit squaresからなるC_Jへのprojection distortionをO(log R/R)と評価する。対象はMoser像領域自身の内在距離と、外側保護領域{min ell_i>R/2}内の全経路を許す距離。標的はC_J自身の内在距離であり、full C_dの距離の制限ではない。m=Rでfiberのintrinsic/ambient diameterはO(1/R)、R^−2 g_tに正規化後はO(1/R²)、raw-map誤差はO(log R/R)。Squareの継目にも同一のregular T² fiberがある。

[開正方形の局所collapse](papers/sections/paper/ke_open_cell_collapse.tex)では、固定compact rectangle上のactual product比較とGH distortionの率をO(L^−η)とした。全曲面のshortcut、actual neckとのorbit matching、source・branch・coreのsingular fibersへの相対接着、既存大域fibrationとの同定は未解決。局所定理には証明と点検記録があるが、包括的新規性は未確認。今回の独立点検の範囲は新しい補集合の位相とshort-circle averagingであり、既存の大域接着全体を再監査したものではない。


曲面側の第25版ソースを回収し、全文原稿と必要な検証資産を移行した。

| 原稿 | 頁数 | 役割 |
| --- | ---: | --- |
| [主稿](papers/lagrangian-torus-fibration.tex) | 130 | 相対SNC構成・次数分割・作用atlas |
| [整数接着](papers/quintic-integer-gluing.tex) | 201（記録） | 指定K5データの整数条件と障害 |
| [局所置換](papers/meridian-surgery.tex) | 18（記録） | meridian・四pants置換の障害 |
| [研究ノート](papers/research-notes.tex) | 65（記録） | 証明素材・現在の残余 |
| [三次元局所稿](papers/threefold-blocks.tex) | 179 | 第10版の現行TeX |
| [三次元全体稿](papers/threefold-fibration.tex) | 201 | 第12稿の現行TeX |

主稿・三次元局所稿・三次元全体稿は2026-11-21にLuaLaTeXとlatexmkで組版し、未解決の参照・引用がないことを確認し、追加部分のPDF表示も点検した。他の三稿の頁数は既存の組版記録で、今回再組版していない。PDFとSyncTeXはbuild/へ出力し、Gitでは追跡しない。

**先行研究との境界：** [三次元全体稿の文献比較](papers/threefold-fibration.tex)で、Mikhalkin (2004) の任意次数・次元のstratified **topological** torus fibration（Lagrangian性は各maximal cellの選ばれたfiber）、Leung–Wan (2009)の一般型における漸近special性、Evans–Mauri・AAKの局所／affine模型、Fernández de Bobadilla–Pełka (2026)の部分領域構成、Mak–Matessi–Ruddat–Zharkovの2026年Calabi–Yau講演発表を区別した。今回の大域目標は**一般型三次元の全regular fibersがLagrangianな全域構成**であって、一般型の位相的torus fibrationの初存在ではない。

三次元の大域接着は研究上の未解決課題。三次元の検算は `python3 verification/run_threefold_checks.py`。

**現行の数学的到達点：** [基底の位相・人工計量](papers/sections/paper/base_topology.tex)ではKE候補へのcell-like写像、次数5と6以上で異なる収縮速度、portal/no-shortcut条件と反例を証明。[三次元局所稿](papers/threefold-blocks.tex)ではnormal-trivial曲線とfocus–hyperbolic blockの構成に加え、**小さい管状補集合**の整数ホモロジーをLefschetz–Thom列から計算した（六次ではH₃にZ/4 torsion）。**実際のfocus blockの補集合**も整数homologyを計算し、六次では H₁=Z、H₂=Z⁸、H₃=Z⁵²⁷⊕Z/4、H₄=Z⁷ と得た。管状補集合とのfree rankの違いも説明した。Focus normal faceはunipotent torus bundleで基本群は整数Heisenberg群、六次closed-curve faceのBetti数は(1,8,15,15,8,1)。Focus基底の境界を回るloopはH₁(U)では消えるがH₁(V)=Zの原始生成元へ写ると証明した。境界包含のhigher homology・基本群写像は上記の新節で決定済み。**relative fillingとglobal Lagrangian接着は未解決**。補集合のEuler数は六次で−512だが、孤立非零Euler fiberが全て−1という仮定なしに「512個必要」とは主張しない。

**局所構成と相対接着：** 二段階構成の条件付きneck延長は、reduced surfaceのmarked simple-saddle foliationとend germsの適合を明示的に仮定する。Regular fiberはT²、simple-saddle fiberはS¹×figure-eightであり、source nodes・coresまでの接着は含まない。 [定量的averaging–Moser](papers/sections/paper/ke_fiber_compatibility.tex)は短いtorus作用とC0 tensor比較から局所Lagrangian fibersを作る。三枚の閉squareはhexagonで一度に実現し、actual適用はcomplete simplex比較で検証した。[Fiberを保つ相対補題](papers/sections/paper/ke_closed_corner_gh.tex) `ke:relative-fiber-preserving` は、開torus-saturated collarの元のorbitsが既にactual Lagrangianなら、chain primitive Hωによるflowが各fiberと基底値を保つことを示す。作用不変性は不要。各点を固定する結論や任意のprimitiveへの拡張ではない。同じorbit partitionを持つactual neck collarの存在は別に検証する必要がある。基本方法の先行研究はRuan (arXiv:math/0309177v2, §3)であり、一般的な新規性は主張しない。

**KE極限との関係：** 径の尺度 $R_t=\log(-\log|t|^2)$ での大域候補は $X_t\to B_d(T)\to\mathcal C_d$。KE側の解析仮定に加え、GH近似写像と既存大域Lagrangian fibrationの一様な適合性が必要。[基底比較の命題](papers/sections/paper/base_topology.tex)はその条件から全fiberのambient直径収縮を導く。この大域適合性は未証明であり、上記の単一closed cornerにおけるactual局所GH定理と区別する。Zhangの局所負KE collapseと我々の非Q-factorial sourceの違いは[研究ノート](research/notes.md)・主稿序論に記す。

**複素次元2の先行研究とfiber型：** [主原稿](papers/lagrangian-torus-fibration.tex)の全平面構成では、正則T²のほか、三価分岐辺上のS¹×(S¹∨S¹)、面内の一重pinched torus、core頂点上のlogarithmic Weinstein skeletonが現れる。五次は(cores, branch edges, isolated nodes)=(5,10,50)、六次は(6,30,90)。分岐辺の本数は無限個ある辺上ファイバーの個数とは違う。Mikhalkin (2004)のstratified topological fibration、Smith (2001)の追加仮定付き制限定理、Leung–Symington (2010)のalmost toric分類、Evans–Mauri (2021)のpants局所構成、Zhang (2025)の一般型のpants分解と区別し、[現行研究ノート](research/notes.md)に引用と適用範囲を記載。

最初に[研究方針](00_research_plan.md)、[移行範囲](research/migration.md)、[ソース対応](research/source-manifest.json)を確認する。

組版はルートで `latexmk`。現行10検査は `python3 verification/run_current_checks.py`。PDF/SyncTeX・再実行結果はbuild/。

正本はmain。[research-hub](https://github.com/uedakazushi/research-hub)。元Libraryは削除しない。
