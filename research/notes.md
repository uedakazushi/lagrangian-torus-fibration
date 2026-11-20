# 研究ノートの入口

詳細な現行ノートは `papers/research-notes.tex`（曲面第25版、65頁）に移行した。証明を短い要約で置き換えない。

## 負KE計量のGH極限とfiber収縮（2026-11-20）

### 二つの尺度と先行定理
全平面退化は $X_t=\{\prod_iL_i+tF_d=0\}\subset\mathbf P^3$、$d\ge5$ とし、$F_d$ は三重点で非零、二重線上では単純零点を持つとする。$\operatorname{Ric}(\omega_t)=-\omega_t$ の規約では $[\omega_t]=2\pi(d-4)H$、$\operatorname{Vol}(X_t,g_t)=2\pi^2d(d-4)^2$ である。複素構造を固定したままの負KE計量はこの規約で一意であり、ここで動かすのは複素構造である。

Song, arXiv:1706.01518v1, Theorem 1.2（https://arxiv.org/abs/1706.01518 ）の適用：中央fiberはSNCでslc、相対canonicalは $\mathcal O(d-4)$ でample、全空間は $xy=tz$ 型ordinary double pointsを持つnormal canonical varietyなのでstable degenerationの仮定を満たす。成分内部に基点を置く非崩壊極限は $d$ 個の $\mathbf P^2\setminus\{d-1\text{本の直線}\}$ の完備有限体積KE曲面である。これはcore skeletonではなく四実次元の開曲面である。Song–Sturm–Wang, arXiv:2003.04709v1, Theorem 6.1（https://arxiv.org/abs/2003.04709 ）もstable familyの多点付き極限を扱う。すべての基点列が非崩壊だという意味ではない。

Zhang, *Collapsing of negative Kähler–Einstein metrics*, MRL 22 (2015), 1843–1869, DOI 10.4310/MRL.2015.v22.n6.a16, arXiv:1505.04728v2, Theorems 1.1/2.4は、Q-factorialなsimple toroidal total spaceと相対canonicalのamplenessの下で、stratumへ動かす基点における局所torus collapseを示す。曲面では二重曲線でS¹、三重点でT²が縮む。主稿 `intro:ke-collapse` に比較を収録した。我々のsourceの局所環 $\mathbf C[x,y,z,t]/(xy-tz)$ はQ-factorialでない。Small resolutionはcrepantなのでexceptional $\mathbf P^1$ 上の相対canonicalの次数は0となる。従って「小解消すればZhangをそのまま適用できる」とは言えない。

Mandel, *Degenerations of negative Kähler–Einstein surfaces*, JLMS 109 (2024), e12818, DOI 10.1112/jlms.12818, arXiv:2206.09792, Theorems 1.1–1.2は負KE neckとその尺度別模型を構成するが、我々のcompact family全体へのgluingを完了した定理として引用しない。K3での対照例はGross–Tosatti–Zhang, CAG 24 (2016), 93–113, DOI 10.4310/CAG.2016.v24.n1.a4, arXiv:1304.1820, Theorem 1.1。楕円K3の適切なRicci-flat metric族が底へ崩壊し、hyperkähler rotationでspecial Lagrangianの解釈を得る。負KEに同じ結論を移す証拠にはしない。

### 我々のdiameter-scale候補と残る適合性
KE研究の `papers/cubical-gh-limit.tex` では $R_t=\log(-\log|t|^2)$、$\mathcal C_d=\{w\in[0,1]^d:\max w_i=1,\ |\operatorname{supp}w|\le3\}$ とし、$(X_t,R_t^{-2}g_t)\to(\mathcal C_d,d_\square)$ を **(G)$_d$+(CP)$_d$+(PBE)$_d$の下**で述べる。関連repoの現行方針・Part IV–Vが解析入力の正本であり、無条件のactual GH収束は未証明。

局所plumbingのモデル $z_0z_1z_2=t$ で $u_i=-\log|z_i|$、$L=-\log|t|$ とすると $\sum u_i=L$。Cuspのradial model $\sum (du_i/u_i)^2$ を $(\log L)^2$ で割り、$r_i=\log u_i/\log L$ と置くと、制約は極限で $\max r_i=1$ となる。三重点では三枚のsquareが現れる。これは候補を説明する模型計算であり、actual KE metricの一様漸近を証明しない。

望ましい写像は $f_t=p_T\circ\pi_t:X_t\to B_d(T)\to\mathcal C_d$。五次では $p_T$ は同相、六次以上では基底内の木も収縮する。**空間としてのGH収束**と**指定したLagrangian fibrationによる実現**を区別する。

主稿 `base_topology.tex` の `topo:ke-map-compatibility` に、$\operatorname{dis}(\Phi_t)\le a_t$ と $\sup_xd_\square(\Phi_t(x),p_T\pi_t(x))\le b_t$ から $\operatorname{dis}(p_T\pi_t)\le a_t+2b_t$ を得る比較命題と証明を置いた。Ambient fiber diametersは同じ量以下、GH距離はその半分以下である。一般的新規性は主張しない。証明を今回三角不等式で点検したことと、actual $a_t,b_t\to0$ が未証明であることを区別する。

**具体的な次の課題：** ラベルを保ち適切にパラメータ化した $\pi_t$ の構成で、KE側のpruned logarithmic-depth mapとの一様誤差 $b_t\to0$ を調べる。まずtriple chartsの角トーラス、その次にsourceのpinched torus、branchのS¹×figure-eightとcoreに進む。必要なのは全特異領域を含む一様評価であり、regular fibersの点ごとの収縮では不足する。Moserのsymplectic同定だけでは距離制御は得られない。Action-affine structureだけからcanonicalなRiemannian基底計量も決まらない。

## 複素次元2：先行研究・singular fibersの確定事項（2026-11-20）
本研究の曲面X_d⊂P³, d≥5の一般SNC gluingと、全平面模型の明示的なsingular fiber型を区別する。主要な定理は papers/sections/paper/geometry_main_statements_v17.tex の main:global、nodeの線型monodromyは invariants_examples.tex、より詳しい先行比較は geometry_introduction_v25.tex。

**一次資料の比較：**
- I. Smith, *Torus fibrations on symplectic four-manifolds*, Turkish J. Math. **25** (2001), 69–96, https://journals.tubitak.gov.tr/math/vol25/iss1/4/ 。Homologically essential Lagrangian toriとtame singularitiesという追加条件下での閉四次元多様体の制限定理。今回の分岐・core特異ファイバーへの直接適用は、tamenessとregular torusのhomology classの検証なしにしない。
- G. Mikhalkin, *Decomposition into pairs-of-pants for complex algebraic hypersurfaces*, Topology **43** (2004), 1035–1065, DOI 10.1016/j.top.2003.11.006、Theorem 1。任意次数・次元のstratified topological torus fibrationは既知。各maximal cellで少なくとも一つのLagrangian torusを与えるが全regular torusがLagrangianとはいわない。
- N. C. Leung and M. Symington, *Almost toric symplectic four-manifolds*, J. Symplectic Geom. **8** (2010), 143–187, DOI 10.4310/JSG.2010.v8.n2.a2、**Theorem 2.1**, Table 1。閉almost toric 4-foldの全空間を分類し、一般型曲面X_dは含まれない。通常のalmost toricはsmooth surface base、ellipticと孤立focus singularitiesが許される。本研究はbranched baseとlog-Weinstein coreを許し、仮定が異なる。
- J. D. Evans and M. Mauri, *Constructing local models for Lagrangian torus fibrations*, Ann. Henri Lebesgue **4** (2021), 537–570, DOI 10.5802/ahl.80、§3.1。P²から一般位置4直線を除く4-dimensional pair of pantsのLagrangian fibrationを構成し、cone over K₄のbranch/coreモデルを与える。曲面の「core singular fiberの局所模型」の直接的先行結果。
- M. Golla and B. Martelli, *Pair of pants decomposition of 4-manifolds*, Algebr. Geom. Topol. **17** (2017), 1407–1444, DOI 10.2140/agt.2017.17.1407。四次元pants decompositionの微分位相。
- Y. Zhang, *Pair-of-Pants Decompositions of 4-Manifolds Diffeomorphic to General Type Hypersurfaces*, J. Math. Study **58** (2025), 211–252, DOI 10.4208/jms.v58n2.25.06、Theorem 1.1。X_dと微分同相な四次元多様体にd(d−4)²個のpantsとK3由来の部分領域を用いる分解。境界にS¹×(S¹∨S¹)などの位相的な分岐模型を含む。所定のωの下で**全regular torus fibersをLagrangianにする大域構成**とは区別する。
- J. Fernández de Bobadilla and T. Pełka, *Fibrations by Lagrangian Tori for Maximal Calabi–Yau Degenerations and Beyond*, CPAM (2026), DOI 10.1002/cpa.70060、Theorem 6.14。一般Kähler SNC退化のmaximal/submaximal strataに対応する部分領域のLagrangian fibrationを構成する。本研究は未充填のcomponent-core領域のfinite compactificationと実際のoverlap gluingを必要とする。
Leung–Wan (JDG **83** (2009))の一般型での漸近special性はMikhalkinが選んだLagrangian fibersに関するもので、全regular fibersではない。これらの結果を踏まえ、「一般型で初めてtorus fibrationを構成する」といわず、所定のKähler formで**全regular fibersがLagrangianな閉曲面上のglobal construction**を本稿独自の主張として、証明監査と先行研究の網羅性を引き続き検証する。

**全平面分割における主定理のfiber一覧：**
- 2D top stratum: 正則Lagrangian T²、Euler数0。
- 1D branch-edge interior: S¹×(S¹∨S¹)、Euler数0。三枚のsheetが接し、各辺全体に連続的に出現するため、辺の本数は「個々のsingular fibersの個数」ではない。
- Face interiorのisolated nodal value: 一重pinched T²、Euler数1、local focus monodromy [[1,1],[0,1]]。全部でd C(d,2)個。
- 0D core vertex: P²からd−1本の一般位置直線を除いた補空間のlogarithmic Weinstein skeletonのsymplectic image。Homotopy typeは(T^{d−2})の2-skeleton、b₁=d−2、b₂=C(d−2,2)、Euler数C(d−3,2)。全部でd個。

基底の開branch辺はC(d,2)(d−4)本、三角形C(d,3)枚、bigon C(d,2)(d−5)枚。d=5なら(core, branch-edge, node)=(5,10,50)、coreのχ=1、全Euler数55。d=6なら(6,30,90)、coreのχ=3、全Euler数108。内訳：五次は十triangleに各5 node、六次は二十triangleに各3 nodeと十五bigonに各2 node。一般dのEulerチェックは
\[
d\binom{d-3}{2}+d\binom d2=d(d^2-4d+6)=c_2(X_d).
\]
**Singular fiberは一般にsmooth embedded Lagrangianではなく、各smooth stratumがisotropicなstratified fiber**として定義している。Core skeletonも一般のdで一つの固定したpants型ではない。この基本的なlocal topology、個数、Euler数の証明は原稿に既存、今回の作業は出典・適用範囲との照合であり、幾何学的gluing証明全体の独立監査ではない。

## 曲面：現在の核心
全pair productsが狭義正の四ray整数データの正weightsはmatchingと同値。G5_14両単位枝の{5,0,0}を排除し、{4,1,0}に限定したと原稿は記録する。必要支持はG5_14、G5_16、G5_17の3型26標識。存在・幾何的非同型類の個数とは異なる。三高Dの一般同時非負性と一般分母剛性は残る。

## KE退化との分岐基底の位相的比較（新たに証明）
曲面基底 \(B_d(T)\) の三価木 \(T_{ij}\) を収縮する既存の \(q:B_d(T)\to\operatorname{Sk}_2\Delta^{d-1}\) と、KE候補 \(\mathcal C_d\) の正規化同相の逆を合成すると、**labelを保ち点逆像が可縮な** \(p_T:B_d(T)\to\mathcal C_d\) を得る。一般次数の厳密な証明は `papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`。\(d=5\) では同相、\(d\ge6\) では両者は同相ではない（辺の局所分岐次数が異なる）。KEのGH極限や作用アフィン計量との一致は主張しない。

整数鎖複体の主張を検査するため、\(d=5,\dots,8\) の \(B_d(T)\) と \(\operatorname{Sk}_2\Delta^{d-1}\) の \(\partial_1,\partial_2\) の階数を独立に計算して、\(b_1=0\)、\(b_2=\binom{d-1}{3}\) と一致した。再現コードは `verification/verify_ke_base_topology.py`。これは有限体 \(\mathbb F_{1000003}\) 上の有限検算であり、整数係数の一般定理の証明は本文のexplicit chain contractionが担当する。

## 三次元一般型のLagrangian torus fibration：一次文献比較（2026-11-20）
最重要の先行結果は以下。**位相的stratified torus fibration**、**選んだLagrangian fiber**、**全regular fibersがLagrangianな大域fibration**、**SNC degenerationの部分領域のLagrangian fibration**を混同しない。

- G. Mikhalkin, *Decomposition into pairs-of-pants for complex algebraic hypersurfaces*, Topology 43 (2004), 1035–1065, DOI 10.1016/j.top.2003.11.006, arXiv:math/0205011。**Theorem 1**は全次数・全次元のsmooth hypersurface X_dにstratified topological T^n-fibrationを作り、底はwedge of p_g(X_d) spheres S^nのhomotopy型を持つ。**Lagrangian性は各maximal n-cell内の少なくとも一点のfiberに限る**。特に一般型threefold d≥6のtopological torus decompositionは既知。全regular fibersが所定ωでLagrangianという結論はない。
- N. C. Leung and T. Y. H. Wan, *Calabi-Yau components in general type hypersurfaces*, J. Differential Geom. 83 (2009), 43–74, DOI 10.4310/jdg/1253804351, arXiv:0807.1784。**Theorem 2.4**がMikhalkinの定理を再掲し、**Theorem 3.3**は選ばれたLagrangian fibersが正則n形式に関してasymptotically specialになることを示す。全正則fiberのLagrangian性は証明しない。
- J. D. Evans and M. Mauri, *Constructing local models for Lagrangian torus fibrations*, Ann. Henri Lebesgue 4 (2021), 537–570, DOI 10.5802/ahl.80。Affine SNC complementのlocal model、3-fold negative vertex、one-dimensional stratum近傍。Projective general type X_dのglobal fibrationではない。
- M. Abouzaid, D. Auroux and L. Katzarkov, *Lagrangian fibrations on blowups of toric varieties and mirror symmetry for hypersurfaces*, Publ. Math. IHÉS 123 (2016), 199–282, DOI 10.1007/s10240-016-0081-9。Affine hypersurfaces of general typeへ応用するが、blowup of V×C along H×0のfibrationを、compact H⊂P^4そのものへのglobal fibrationと同一視できない。
- J. Fernández de Bobadilla and T. Pełka, *Fibrations by Lagrangian Tori for Maximal Calabi–Yau Degenerations and Beyond*, Commun. Pure Appl. Math., first published 8 July 2026, article e70060, DOI 10.1002/cpa.70060, arXiv:2312.13248v4。A'Campo boundaryから近傍fiberへsymplectic transportをする一般Kähler degeneration方法。Maximal CYではgeneric regionのLagrangian torus fibrationであり、一般型compact threefoldのglobal coverageには直接至らない。本研究のthreefold-fibration.texにTheorem 6.14の部分適用が既にある。
- C. Y. Mak, D. Matessi, H. Ruddat and I. ZharkovのCalabi–Yau hypersurfaceへのglobal Lagrangian fibrationは2026年1月/6月/11月の公的**講演要旨**で発表。2026年11月12日のMak講演要旨（IMJ-PRG）はiron coefficientsとconvex non-strict potential、Liouville flowを明示している。確認した範囲でcomplete published proof/preprintは未取得。対象はCY/anticanonicalであり一般型には自動適用できない。公式要旨 https://www.imj-prg.fr/gestion/evenement/affEvenement/45 と https://www.mittag-leffler.se/seminar/helge-ruddat-tba/ 。

**目標の新規性の正確な位置**：smooth general type X_d⊂P^4, d≥6, 指定ω=aHについて、全regular T^3 fibersがLagrangianで、明示されたsingular local modelsをもち、全X_dを覆い、境界なし、連結fiber、Hausdorff baseとなるglobal mapを構成する。Mikhalkinのtopological fibrationとLeung–Wanの部分的special性より強い。しかし「初めての一般型torus fibration」「一般型のLagrangian torusが未知られ」などの主張は誤り。新規性の網羅的な保証は未完了。より弱いgeneral singular setを許しても大域存在を優先する。現在未完成の相対filling、curvature-flat normal lifts、reduced surfaceの両端葉層一致、actual coverageの証明を必要とする。

## 三次元：局所稿の参照先
`papers/threefold-blocks.tex`第25・33節：positive normal shell、membrane/focus collars。第26節：smooth focus Cartanとnormal degreeの障害。第34–35節：compact focus blockとnormal-trivial closed curve。第36節：weighted collars。旧48 ports、normal faces、complement、大域boundary-free fibrationは未完成。全体稿は `papers/threefold-fibration.tex`。

## 人工的基底計量の鋭い収束速度と幾何学的比較の核心
$p_T:B_d(T)\to\mathcal C_d$ に補助piecewise Euclidean metric $h$ を固定し、$|v|_\varepsilon^2=|dp_T(v)|_\square^2+\varepsilon^2|v|_h^2$ の内在距離を考える。graph correspondenceのdistortion $\mathcal D_\varepsilon$ は、$d=5$ で $\Theta(\varepsilon^2)$、$d\ge6$ で $\Theta(\varepsilon)$ と鋭く決まる（主原稿に読み込む base_topology.tex の topo:metric-collapse-sharp）。$d\ge6$ の下界は同一fiber内の正の $h$-距離に由来するが、**GH距離の下界ではない**。

実際の基底長さ計量 $d_t$ に対する十分条件（topo:finite-portal-criterion）は、(N) global no-shortcut誤差 $\alpha_t$、(S) square segment liftの乗法誤差 $\sigma_t$・加法誤差 $\lambda_t$、(F) 同じfiberの接続費用 $\kappa_t$。最大square数 $N_d=d\binom{d-1}{2}$、直径 $D_d$ について
\[
\operatorname{dis}(p_T)\le\max\{\alpha_t,\ \sigma_tD_d+N_d\lambda_t+(N_d+1)\kappa_t\}.
\]
二枚のunit squareを一頂点で貼り、二枚を一枚に折る反例では(N),(S)が誤差零でも(F)が成立せず、$d_{\rm GH}\ge\sqrt2/2$（topo:portal-counterexample）。したがって局所模型だけでは大域収束は言えない。実際のLagrangian action metricの長さ完備化、枝・coreへの延長、および(N),(S),(F)の確認は未解決。新規性は未確認。

## 六次Petersen分岐基底の対称性
$d=6$ で全ての頂点リンクをPetersenグラフとするラベル付き木系はちょうど六つであり、$S_6$ はこの集合に推移的に作用する。固定した一系の安定化群は位数 $6!/6=120$、指数6。従ってその一系の選択は座標置換の全 $S_6$ 対称性を保たない。KE候補 $\mathcal C_6$ は自然に $S_6$ 対称なので、Petersen分岐基底とのラベル付き比較を対称に行うには六つの木系全体を管理する必要がある。証明は base_topology.tex の topo:petersen-symmetry、全15 perfect matchingsと六one-factorizationsの有限列挙・安定化群位数は別に確認した。これは任意の別構成やラベル忘却後のシンプレクティックな対称性の不存在ではない。

## 三次元：管状補集合とfocus境界の整数位相
**曲線の構成：** d≥6、e=d−2。平面曲線C_eを含むsmooth hypersurfaceはF=q_eR_2+z_3G_{d−1}+z_4H_{d−1}のfirst-jet生成から取れる。Normal完全列より det N_{C_e/Y_d}=O_{C_e}(e+2−d)=O_{C_e}。Ehresmann–Moser移送したC'⊂X_dのsymplectic normalは自明、genusはg=(d−3)(d−4)/2。一般のnormal-trivial symplectic curve（degree e, genus g）には2g−2=(d−5)eが必要で、d偶数ならe偶数（主稿の tnc:degree-genus-parity）。Holomorphic normal rank-two bundleそのものの自明性は主張しない。

**管状補集合の整数homology：** 小さいnormal disk bundle N(C')の補集合V_0=X_d＼int N(C')では、Lefschetz・Thom長完全列により
\[
H_3(V_0;\mathbb Z)\simeq \mathbb Z^{b_d}\oplus\mathbb Z/(d-2),\qquad
H_4(V_0;\mathbb Z)\simeq\mathbb Z^{2g},\qquad
b_d=d^4-5d^3+10d^2-10d+4.
\]
Torsionはnormal meridian S³のclassから生じる（tnc:tubular-homology）。六次ではH_3(V_0)=Z^{520}⊕Z/4、H_4(V_0)=Z^6。X_dの整数cohomologyの一次資料はO. Randal-Williams, Math. Ann. 391 (2025), 1965–2003, §2.1, DOI 10.1007/s00208-024-02951-4。

**Actual focus blockの整数homology（証明済み）：** $K_c$の座標を$w=XY$、$A=P_X-P_Y$とすると、$w$を保持して$A\to0$へ変形収縮できる。$A=0$は$w$-annulusと円周の積で、$w=0$の一円周を潰したものだから
\[
K_c\simeq S^1\vee S^2
\]
（tnc:focus-homotopy）。従って実際のblockの補集合$\mathcal V=\overline{X_d\setminus\operatorname{int}(C'\times K_c)}$に相対Poincaré–Lefschetz双対性を適用すると
\[
H_1(\mathcal V)=\mathbb Z,\quad H_2(\mathcal V)=\mathbb Z^{2g+2},\quad
H_3(\mathcal V)=\mathbb Z^{b_d+2g+1}\oplus\mathbb Z/(d-2),\quad
H_4(\mathcal V)=\mathbb Z^{2g+1}.
\]
六次では$(b_1,b_2,b_3^{\rm free},b_4)=(1,8,527,7)$、$H_3$のtorsionは$\mathbb Z/4$（tnc:actual-complement-homology）。Torsionを表す3-cycleは固定した曲線上の一点での$\partial K_c$。管状補集合$V_0$と$\mathcal V$は同じEuler数だが自由rankが異なる（tnc:complement-distinction）。Ambientの$\pi_3(X_d)$に現れる既知の$\mathbb Z/d$は別の不変量。

**Actual normal face：** $\partial K_c$はfocus点一つのmonodromy $\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)$を持つtorus bundleで、$\pi_1$は整数Heisenberg群、$H_1=H_2=\mathbb Z^2$（tnc:focus-boundary-homology）。$\partial\mathcal U=C'\times\partial K_c$のBetti数は$(1,2g+2,4g+3,4g+3,2g+2,1)$、六次では$(1,8,15,15,8,1)$（tnc:focus-boundary-betti）。

**Euler予算：** χ(U)=−(d−2)(d−5)、χ(V)=−(d⁴−5d³+9d²−3d−10)。六次ではχ(V)=−512。Euler数非零fiberが有限個の孤立基底点にだけ存在してすべて−1なら512個必要（tnc:complement-singularity-budget）。正次元特異strataではcompact-support Euler数で重み付けし、一般のglobal Lagrangian fibrationの実現数には外挿しない。

**境界包含H₁の新たな必要条件：** Focus基底長方形の境界を一周するloopをnormal coordinatesのsectionで持ち上げると、H₁(∂U)→H₁(U)のkernelの原始生成元を得る。Mayer–Vietoris列によってこのclassはH₁(V)=Zの原始生成元へ写る（tnc:focus-boundary-primitive）。従って補集合でこのloopを零homologousにする境界同定はできない。**次は** 境界包含のH₂・H₃・基本群の写像、vanishing-cycleとmeridional torsion、monodromy/Maslov/action periodsを照合してrelative fillingを構成する。大域fibrationは未完成。

## 検証
移行時にWorkがv25の五主検算と五独立監査を再実行した。今回の新規トポロジー命題は原稿で論証し、次数ごとのEuler数とWang行列を独立検算したが、保存済み検算スクリプトの最新版全体は今回再実行していない。保存済みの旧verification/証明書全体を今回の実行結果とは扱わない。詳細はmigration.md。計算は解析的symplectic gluingや新規性の証明を代替しない。
