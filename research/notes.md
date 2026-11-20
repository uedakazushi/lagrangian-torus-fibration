# 研究ノートの入口
更新：2026-11-21 / v1.9 / 曲面改訂8・三次元局所稿11・全体稿13

詳細な現行ノートは `papers/research-notes.tex`（曲面第25版、65頁）に移行した。証明を短い要約で置き換えない。

## 二段階平均によるnormal actionとperiodsの接続

正本は主稿 `papers/sections/paper/ke_staged_neck_averaging.tex`。証明全文はここへ重複させない。`ke:circle-exact-transport` / `ke:staged-neck-averaging` は、ω=dλに対してnormal circleを先に平均し、残る円の平均をnormal-equivariantに行う。η=A1ω、κ=A2η、φ*ω=η、ψ*η=κなら、Θ=φψは
\[
 \Theta^*\lambda=A_2A_1\lambda+dq,\qquad
 \mu\circ\psi=A_2\mu,\qquad
 \widehat\rho_1=\phi\rho_1\phi^{-1}
\]
を満たし、全整数cycleのperiodsを同じprimitiveで規格化する。Periodは1、ι_Vω=−dμの規約。Normal actionが一致しても、別に指定したneck fibrationの第二periodやreduced leavesは自動的に一致しない。

`ke:staged-hamiltonian-comparison` はpositive triangle (1−u)κ+(u−v)η+vω、0≤v≤u≤1内のpath homotopyを用いる。各endpointがprimitiveを同じ平均primitiveからexact差まで保つため、そのsmooth familyがHamiltonianとなる。共通domain bufferに加え、F_r(D_small)⊂F_0(D_large)というimage bufferが必要。Exact endpointだけを根拠にしない。`ke:staged-closed-corner-gh` は任意の固定primitive subgroupを第一段に選んでもO(log R/R)の局所GH率を保つ。旧bundleとの関係は、同じsoftmax labelsのfibersを対応させるHamiltonian mapである。

関連KE主稿 `pair:prop:bundle-conic` は、射影的normal bundleでh=−F_d/G、x_i'=x_i h0/h、x_j'=x_jとしてexact uv=tを得る。局所overlapをcomplete C* automorphismとする不十分な議論を使わない。(u,v)↦(ue^u,ve^(−u))はuvとaxesを保つlocal mapだがbase-only乗数ではない、という例を覚えておく。新構成もfixed compact baseに限り、tripleへ動くbaseのtransition boundsを含まない。

同稿 `pair:cor:global-primitive` / `pair:cor:actual-common-moment` は、source-free固定base B上で非消滅正則1-form τを選び、Ω=dlogv∧τからglobal λ_tを得る。Canonical normal momentはτの変更で変わらないが、residual periodsには同じprimitiveを使う。Song (arXiv:1706.01518, Lemmas 4.4–4.5)とRochon–Zhang (arXiv:1106.0873, Theorem 5.1)の固定end入力から、μ_tの端値は±4π/s_r+O(s_r^(−1−δ))+o_t(1)。rを固定後t→0とし、η_t=A1ω_tのreductionsの共通intervalを確保する。

`ke:short-circle-actual-buffer` は不変背景を不要にする。g_a=ρ_a*g_ω、η=Aω、b=ε||w||₂とすると|β(X)|≤b|X|_{g_η}。Moser場は(1−s)|Y|²_η+s|Y|²_ω≤b|Y|_ηを満たし、平方完成で|Y|_ω≤b/(2√(s(1−s)))となる。両向きtrajectory長はc_w ε、通常kernelでc_w=π/(2√3)、centeredでπ/(4√3)。Exactnessは長さ評価に不要。`ke:short-circle-image-buffer` はδ>(2c_w+1/2)εから、同じcompact飽和集合Kを含むsource Oとimage φ(O)を得る。Backward c_w ε＋半orbit ε/2＋forward c_w εの予算であり、conjugated actionを元のK上で使うための像の条件を明示した。C¹制御やintrinsic径、全neckでの仮定検証とは別。

残るactual入力は、neck全体のnormal Moser flowの生存・一様buffer、triple endsでの同一正則作用とreduced foliationの同時一致、source/coreとの接着である。KE側 `neck:lem:rank-one-circle` はresidual rank-one下界とvolume上界だけでnormal circle長を抑えるが、その下界とactual bufferを証明する必要がある。固定residual境界の影響が消えないexact negative KE productの例があるため、normal深度だけからproduct asymptoticsを推論しない。

## 全深部三重点の actual semi-flat 比較
任意の固定次数 d≥5 の一般位置全平面退化で、三重点の全深度比・全角度に一様な actual KE 比較を証明した。正確な座標 ζ0ζ1ζ2=t、ell_i=−log|ζ_i|²、L=−log|t|²、R=log L とし、k_Lをlogarithmic simplex上のcomplete toric KE form、その実計量をg_L^sfとする。十分大きい固定m1と各qのCqについて、m≥m1、min ell_i≥mで
\[
\left|\log\frac{\omega_t^2}{k_L^2}\right|\le C/m,\qquad
\|g_t-g_L^{sf}\|_{C^q}\le C_q/m.
\]
定数は固定dと族に依存してよい。次数一様性は主張しない。証明の正本はKE主稿 `coarse:thm:full-triple-tensor`。

固定toric模型の存在・完備性にはZhang (2015), §2.1, Theorem 2.1 / Proposition 2.2を用いる（退化族のTheorem 2.4とQ-factorial仮定は使わない）。ψ_L=log L−Σlog ell_iに対してψ_L−(log3)/2≤φ_L≤ψ_L、V_L/3≤k_L²≤V_Lを内外にずらした障壁で証明する。Complete模型から三つの半平面へのYau Schwarz lemma、determinant比較、内部正則性により一様cusp geometryを得る。凸性からfacet shiftのlog-density差をO(1/min ell)とし、actual計量を内外のsimplex KE metricsでvolume比較する。Savinの小摂動定理でtensor・全高階誤差へ移る。Actual metric bufferや(TC)/(PBE)を前提としない。

Actual側の大域入力は `coarse:cor:degree-d-volume-lower`。Adjunction residueでcanonical densityを固定し、backgroundによるHermitian frame errorの吸収と各正のcap方向のminorから六型のdeterminant下界を証明する。Sourceでは元のplane coordinatesを保つexact xy=tzとrescalingにより二つのcap係数≥c_d/Lを使う。Compact minimum原理からactual volume下界を得る。今回この依存部分も再点検して明示化した。

## Complete simplex模型の境界での鋭い比較
KE主稿 `papers/sections/simplex_boundary_geometry.tex` が正本。`simplex:lem:rank-one-schwarz` は、complete模型から各半平面への正則写像にYau Schwarz lemmaを適用して
\[
|d\log\ell_i|_{(g_L^{\mathrm{sf}})^{-1}}\le1
\]
という係数1の評価を与える。粗いtensor比較によるtraceの有界性とcomplete最大値原理を使うので、深度比・全角度・正の深度に絶対的下限を設けず有効である。

`simplex:prop:dominant-product` ではa=ell_j、b=ell_k、δ=(a+b)/Lとして
\[
1\le\frac{k_L^2}{\omega_{\mathrm{prod}}^2}
 \le\left(\frac{\pi\delta}{\sin(\pi\delta)}\right)^4,
\qquad
g_L^{\mathrm{sf}}-g_{\mathrm{prod}}=O_{C^q}(\delta^2)
\]
を示す。下比較はexpanded quadrant、上比較は辺長La/(a+b)、Lb/(a+b)のrectangleによる。境界がsimplexと接するrectangleは内部へ縮めて比較してから極限を取る。固定product balls上では深度が中心と固定比の間にあり、potentialの小ささO(δ²)が保たれる。Angular coverを双曲平面二つの積の固定正則座標へ正規化し、Savinと線形化後のSchauder評価で同率の全固定階比較を得る。

`simplex:prop:facet-product` は、一深度bがd_*=min(a,L−a)に比べ小さい場合に、cuspと幅Lのcomplete annulusの積p_Lを比較相手とする。内側rectangleの幅βを(b²d_*)^(1/3)とし、volume-potential誤差
\[
C\bigl((b/\beta)^2+\beta/d_*\bigr)
 =O((b/d_*)^{2/3})
\]
を固定p_L-ball全体で評価する。Actual側にはO(1/b)を加える。`simplex:cor:active-cogram` はell_i≤L e^−Aのactive covectorsについて、二方向ならco-Gram誤差O(e^−2A)、一方向を含む一様評価ならO(e^−A/2)を与える。Actual側はO(1/min ell)を加える。閉cornerの距離下界には、一方向のexact Schwarz評価と二方向のdominant比較だけで足り、facet比較を追加依存としない。

## 同じactual Lagrangian bundleによる全閉cornerのGH極限
正本は `papers/sections/paper/ke_closed_corner_gh.tex`。Lagrangian主稿 `ke:actual-closed-corner` で構成した同じMoser flow φ_tと同じbundleを用いる。m=Rとし、
\[
\ell_a(w)=R+(L-3R)\frac{L^{w_a}}{\sum_bL^{w_b}},
\qquad
\mathcal C_J=\{w\in[0,1]^3:\max w_a=1\}
\]
のhexagon全phase preimageをH_t、そのMoser像をW_{t,J}、射影をπ_{t,J}とする。`ke:closed-corner-gh` と `ke:closed-corner-protected-gh` は、R^−2 g_tの二つの距離に対して
\[
\operatorname{dis}(\pi_{t,J})\le C\frac{\log R}{R}
\]
を証明する。一つはW_{t,J}内の経路による内在距離、もう一つはV_t={min ell_a>R/2}内の全経路を許した距離をW_{t,J}へ制限したもの。標的d_Jは三枚のunit squares自身の内在距離であり、full C_dの他のcellsを通る経路の距離ではない。

模型の証明はKE主稿 `simplex:thm:closed-corner-model`。S=R−2 log Rとし、Ψ_a=[log(ell_a/R)/S]_0^1とclipする。最大深度≥L/3からΨの像はC_Jに入り、微分がactiveなのは高々二方向である。一方向では係数1のSchwarz評価、二方向ではell_j+ell_k≤2L/Rからsharp product比較を使い、complete simplex全体の全経路の長さ下界を得る。上界ではC_Jのgeodesicを高々三枚の異なるsquares内の直線分で実現し、各線分を幅4 log R/Rだけ内部へ移す。Sharpな内部比較とcoarseな短いconnectorsを合わせて同じ率を得る。Seam collarが薄いことだけを下界の根拠にはしない。

Actual/model比較O(1/R)に加え、Moser場のC1評価からmodel計量のLie derivativeを直接抑え、φ_t^*g_t=(1+O(1/R))g_L^sfを得る。保護領域内の全経路を扱うときは、Moser trajectoryのmodel長さO(1/R)とΨのLipschitz定数O(1/R)から、端点誤差d_J(Ψφ_t(z),Ψ(z))=O(R^−2)を用いる。これにより、閉cornerのfibrationの射影そのものがGH approximationになる。

全fiberのintrinsic/ambient diameterはO(1/R)、正規化後はO(1/R²)、raw-map誤差はO(log R/R)。Squareの共通辺と共通頂点でも同じregular T² fiberである。これらを既存大域fibrationのsource・branch・coreのsingular fibersとは同定しない。V_t外を通る全曲面のshortcut、異なるtriple chartの接合、大域相対接着は未解決。新規性の網羅的確認と外部査読・形式証明は未実施。

## 開正方形上のactual KE–Lagrangian collapse
主稿 `papers/sections/paper/ke_open_cell_collapse.tex` は、任意の固定次数d≥5、固定0<η<1/2についてKη=[η,1−η]²上の局所結果を与える。関連KE主稿 `simplex:cor:actual-dominant-product` により、独立深度a,b∈[L^η/2,2L^(1−η)]ではproduct-cuspとの誤差は全固定階でO(L^−η)である。模型側O(((a+b)/L)²)とactual側O(1/min ell)を合わせた率であり、global capped volume下界、complete模型の上下比較、Savin正則性に依存する。(TC)_dや(PBE)_dは追加仮定しない。

`ke:open-cell-moser-c1` はchain primitiveとMoser場のC1 normをO(L^−η)とし、flowのpullback metricを制御する。`ke:open-cell-collapse` はactual Lagrangian T² fibration、fiberのintrinsic/ambient diameter O(L^−η)、raw-map誤差O(1/R)を与える。Moser像領域に内在長さ距離を入れると、R^−2 g_tは平坦KηへGH収束し、projection distortionはO(L^−η+L^−η/R)=O(L^−η)。定数は固定ηに依存する。

開正方形の局所結果と、前節の全閉cornerの局所結果を区別する。閉cornerまでの距離同定は証明したが、全曲面のambient shortcut、source・branch・coreへの相対接着、既存大域fibrationとの同定は残る。

## 負KE計量のGH極限とfiber収縮（2026-11-20）

### 二つの尺度と先行定理
全平面退化は $X_t=\{\prod_iL_i+tF_d=0\}\subset\mathbf P^3$、$d\ge5$ とし、$F_d$ は三重点で非零、二重線上では単純零点を持つとする。$\operatorname{Ric}(\omega_t)=-\omega_t$ の規約では $[\omega_t]=2\pi(d-4)H$、$\operatorname{Vol}(X_t,g_t)=2\pi^2d(d-4)^2$ である。複素構造を固定したままの負KE計量はこの規約で一意であり、ここで動かすのは複素構造である。

Song, arXiv:1706.01518v1, Theorem 1.2（https://arxiv.org/abs/1706.01518 ）の適用：中央fiberはSNCでslc、相対canonicalは $\mathcal O(d-4)$ でample、全空間は $xy=tz$ 型ordinary double pointsを持つnormal canonical varietyなのでstable degenerationの仮定を満たす。成分内部に基点を置く非崩壊極限は $d$ 個の $\mathbf P^2\setminus\{d-1\text{本の直線}\}$ の完備有限体積KE曲面である。これはcore skeletonではなく四実次元の開曲面である。Song–Sturm–Wang, arXiv:2003.04709v1, Theorem 6.1（https://arxiv.org/abs/2003.04709 ）もstable familyの多点付き極限を扱う。すべての基点列が非崩壊だという意味ではない。

Zhang, *Collapsing of negative Kähler–Einstein metrics*, MRL 22 (2015), 1843–1869, DOI 10.4310/MRL.2015.v22.n6.a16, arXiv:1505.04728v2, Theorems 1.1/2.4は、Q-factorialなsimple toroidal total spaceと相対canonicalのamplenessの下で、stratumへ動かす基点における局所torus collapseを示す。曲面では二重曲線でS¹、三重点でT²が縮む。主稿 `intro:ke-collapse` に比較を収録した。我々のsourceの局所環 $\mathbf C[x,y,z,t]/(xy-tz)$ はQ-factorialでない。Small resolutionはcrepantなのでexceptional $\mathbf P^1$ 上の相対canonicalの次数は0となる。従って「小解消すればZhangをそのまま適用できる」とは言えない。

Mandel, *Degenerations of negative Kähler–Einstein surfaces*, JLMS 109 (2024), e12818, DOI 10.1112/jlms.12818, arXiv:2206.09792, Theorems 1.1–1.2は負KE neckとその尺度別模型を構成するが、我々のcompact family全体へのgluingを完了した定理として引用しない。K3での対照例はGross–Tosatti–Zhang, CAG 24 (2016), 93–113, DOI 10.4310/CAG.2016.v24.n1.a4, arXiv:1304.1820, Theorem 1.1。楕円K3の適切なRicci-flat metric族が底へ崩壊し、hyperkähler rotationでspecial Lagrangianの解釈を得る。負KEに同じ結論を移す証拠にはしない。

### 我々のdiameter-scale候補と残る適合性
KE研究の `papers/cubical-gh-limit.tex` では $R_t=\log(-\log|t|^2)$、$\mathcal C_d=\{w\in[0,1]^d:\max w_i=1,\ |\operatorname{supp}w|\le3\}$ とし、$(X_t,R_t^{-2}g_t)\to(\mathcal C_d,d_\square)$ を **(G)$_d$+(CP)$_d$+(PBE)$_d$の下**で述べる。関連repoの現行方針・Part IV–Vが解析入力の正本であり、無条件のactual GH収束は未証明。

局所plumbingのモデル $z_0z_1z_2=t$ で $u_i=-\log|z_i|$、$L=-\log|t|$ とすると $\sum u_i=L$。Cuspのradial model $\sum (du_i/u_i)^2$ を $(\log L)^2$ で割り、$r_i=\log u_i/\log L$ と置くと、制約は極限で $\max r_i=1$ となる。三重点では三枚のsquareが現れる。このradial計算は候補の説明である。Actual KE metricの一様漸近と全閉cornerの局所GH極限には、上記のcomplete模型比較と距離定理を別に用いる。

望ましい写像は $f_t=p_T\circ\pi_t:X_t\to B_d(T)\to\mathcal C_d$。五次では $p_T$ は同相、六次以上では基底内の木も収縮する。**空間としてのGH収束**と**指定したLagrangian fibrationによる実現**を区別する。

主稿 `base_topology.tex` の `topo:ke-map-compatibility` に、$\operatorname{dis}(\Phi_t)\le a_t$ と $\sup_xd_\square(\Phi_t(x),p_T\pi_t(x))\le b_t$ から $\operatorname{dis}(p_T\pi_t)\le a_t+2b_t$ を得る比較命題と証明を置いた。Ambient fiber diametersは同じ量以下、GH距離はその半分以下である。一般的新規性は主張しない。証明を今回三角不等式で点検したことと、actual $a_t,b_t\to0$ が未証明であることを区別する。

**具体的な次の課題：** 全phaseのmoving triple比較と閉cornerの内在・保護領域内のGH同定を入力として、actual neck collarのorbit partition、action periods、定量的bufferを一致させる。`ke:relative-fiber-preserving` を適用できる開overlapを構成し、sourceのpinched torus、branchのS¹×figure-eight、coreへ相対的に接着する。必要なのは全特異領域を含む一様評価と大域no-shortcutであり、regular fibersの点ごとの収縮では不足する。Action-affine structureだけからcanonicalなRiemannian基底計量は決まらない。

## 局所fibrationの証明と解析入力
曲面側の着手対象は複素次元2でのKE極限とLagrangian fibrationの適合性である。主稿の `papers/sections/paper/ke_fiber_compatibility.tex` に次の証明を置いた。

- `ke:short-torus-averaging`：自由な正則 $T^2$ 作用、torus不変Hermitian計量 $h$、$c h\le g_\omega\le C h$、torus上のperiod零を仮定する。作用の周期1生成場の長さの和を $e$ とすると、平均化のchain homotopyから長さ $O(e)$ のprimitiveを作り、一つのMoser flowで領域全体にLagrangian fibrationを構成する。変位は $Ce/(2c)$ 以下、ambient fiber diameterは $\sqrt C e(C/c+1/2)$ 以下。高階微分比較は使わない。
- `ke:triple-hexagon`：$\zeta_i\zeta_j\zeta_k=t$ の三つのsquareを一つのhexagonとして全phase torusで実現し、raw-depth mapとの誤差を $O((1+\log m_t)/R_t)$ に抑える。
- `ke:triple-moving-fibration`：全phaseを含む moving domain $\min\ell_a>m_t/2$ 上の一様tensor比較を追加仮定すれば、actual負KE形式に対する局所fibrationが得られ、そのambient fiber diameterは元の尺度でも $O(m_t^{-1})$。$m_t=R_t\to\infty$ とできる。負KE equationにより局所canonical trivialization上で形式がexactとなるのでperiod条件は満たされる。

これらは条件と証明を今回点検した局所結果である。Averaging–Moserの基本方法はRuan, arXiv:math/0309177v2, §3に先行し、一般的新規性は未確認。H-minimal/special Lagrangian性、大域接着、singular fibersの計量評価は結論しない。

**解析入力の区別：** 関連KE主稿の `coarse:prop:density-counterexample` により、負KE計量であってもbounded volume densityから一様tensor比較は導けない。五次coarse metric packageには独立な $(\mathrm{TC})_5$ が必要であり、その無条件な検証は未完成である。これは対象compact familyの反例ではない。全深部三重点のfull-orbit moving tensor比較は全固定d≥5で検証した。Source等を含むexterior全体への拡張は未解決である。

### Averaging–Moserの先行研究
W.-D. Ruan, *H-minimal Lagrangian fibrations in Kähler manifolds and minimal Lagrangian vanishing tori in Kähler–Einstein manifolds*, arXiv:math/0309177v2, https://arxiv.org/abs/math/0309177v2 。§3 Proposition 3.1はpotentialのtorus平均、Lemma 3.3はHamiltonian-gradient flowを扱い、Theorem 3.1はhomothetic toric potentialと一様 $C^\infty$ quasi-isometryの下でH-minimal fibrationを構成する。Theorem 4.2はsimple toroidal canonical degenerationの最大退化点へ消えるminimal torusの存在を示す。

今回の補題はperiod-zero、$C^0$ tensor比較、短い生成場だけを用いてprimitiveとambient diameterを直接評価する。Ruanの高階幾何とH-minimal性の結論は求めない。既存方法の定量化として位置付け、新規性は未確認。ZhangのTheorem 2.6の個別generalized special Lagrangian torusの存在とも、全域のsingular fibrationとも区別する。

### 固定領域と移動領域の区別・相対接着への入口
主稿 `ke:fixed-simplex-scale` の計算により、固定simplex compactaは径の尺度のtriple vertexしか見ない。関連KE研究ノートの「固定領域の収束から径の尺度へ移る際の障害」に、固定compacta上ではcusp metricと完全一致し、全体で一様に粗比較できるにもかかわらず、正規化した区間長が $1$ から $3/2$ に変わる一次元例を証明付きで収録した。KE反例ではなく、sharp moving estimatesの必要性を示す例である。

主稿 `ke:relative-fiber-preserving` は、torus-saturatedな**開**collar N上で元のorbitsが既にactual ω-Lagrangianであれば、β=Hω、H=K_1+A_1K_2というchain primitiveがvertical vectorsを消すことを用いる。ω_sも同じvertical distributionをLagrangianに保つため、Moser場はverticalであり、各fiberと基底値が保存される。ωの作用不変性は不要。Centered chain primitiveでも同じ証明が成立するが、同じdβを持つ任意のprimitiveへの置換では消滅条件が保存されるとは限らない。

`ke:relative-neck-matching` は、別のactual Lagrangian fibrationがこの開overlap上で同じorbit partitionを持つなら、基底collarを同定して写像を接着できるという局所系である。各点の固定や単一境界上の一致だけを用いた接着は主張しない。点ごとの固定が必要なら、既存の `ke:relative-averaging` のcentered kernel 1/2−sと作用不変collarを使える。Actual neckで必要なorbit一致・action periods・bufferを同時に実現することは未解決。

定数係数monomial変更ζ'=c(t)ζ^A、A∈GL(2,Z)はphase orbit partitionを保つ。一方、非定数holomorphic unitを含む変更ζ'=ζ^A u(ζ,t)は一般に保存しない。二つのtorus actionsが同じoverlapに存在するだけでは相対補題の仮定にならない。Sourceのcritical valuesについても `ke:source-marking` のcore交差仮定の下でp_T(b_t)→e_i+e_jが必要であり、固定された任意の内部markingは使えない。

## 相対接着の補助計算：primitiveの選択と障害

以下はregular torus領域での補助計算であり、仮定と証明をこのノートに保持する。主稿の `ke:relative-fiber-preserving` の証明を重複させず、primitiveの変更、整数基底の変更、collarの点固定に関する情報を整理する。Actual neck全体でのorbit partition・action periods・bufferの整合は未証明であり、これらの補助計算の新規性も未確認である。

### Centered primitiveの整数基底変更

自由な同じT²作用に対し、全Haar平均をA、周期1の円作用をρ_{j,s}とする。Centered homotopy
\[
\widetilde K_j\xi=\int_0^1(1/2-s)\rho_{j,s}^*(\iota_{V_j}\xi)\,ds,
\qquad \widetilde H=\widetilde K_1+A_1\widetilde K_2
\]
はdH̃+H̃d=A−IとAH̃=0を満たす。後者は全平均がpullback・contractionと可換で、weightの積分が零であることから従う。整数基底や順序を変えた二つのβ_r=H̃_rωはdβ_r=Aω−ω、Aβ_r=0を満たす。従ってγ=β_1−β_0はclosed、Aγ=0であり、いずれかのtorus homotopy Hを用いると
\[
\gamma=-d(H\gamma)=df,\qquad f=-H\gamma.
\]
これはbaseの単連結性やH¹(U)=0を要しない。

ω_s=(1−s)Aω+sω、ι_{Y_s^r}ω_s=β_rとし、共通のbuffer内で両flow φ_s^rとその相対写像が定義される内側領域を取る。χ_s=(φ_s^0)^{-1}φ_s^1はAω-symplecticであり、Eulerian生成場Z_sは
\[
\iota_{Z_s}(A\omega)=(\phi_s^0)^*\gamma=d(f\circ\phi_s^0)
\]
を満たす。従ってHamiltonian isotopyで比較できる。ただし二つのflowそのものが一致するという主張ではない。両β_rが飽和collar N上で零なら、Hはorbit内で作用するためf|N=0、両flowとχ_sはNを点ごとに固定する。不変背景hに対して|Hγ|≤Ce|γ|なので、β_r=O(eδ)ならHamiltonianの大きさはO(e²δ)となる。定数は用いる有限個の整数基底に依存してよい。

### 負KE potentialからのprimitiveと定数係数monomial変更

Toric chart上の不変logarithmic volume formをΩ=dlogζ_1∧dlogζ_2とし、Ric(ω)=−ωとする。正のvolume規約で
\[
F=\log\frac{\omega^2}{\Omega\wedge\overline\Omega},\qquad
dd^cF=\omega,\qquad
\beta_{\rm can}=d^c(AF-F)
\]
と置く。ここでd^c=(i/2)(\bar∂−∂)。作用が正則なのでAとd^cは可換し、dβ_can=Aω−ω、Aβ_can=0である。同じphysical overlap上でζ′=c(t)ζ^B、B∈GL(2,Z)と変えると、orbitとHaar平均は同じで、Ω′=det(B)Ω、|det B|=1である。従ってF、β_can、ω_sが一致し、共通buffer上のMoser flowもODEの一意性により厳密に一致する。Centered chain primitiveとの比較は上のHamiltonian計算で与えられる。

定量的には、torus不変Kähler背景h、torus不変模型k、v=log(ω²/k²)に対して、固定階のC^{q+2}(h) normがO(δ)、生成場の|V|+|∇V|がO(e)とする。模型のpotential部分は不変なのでAF−F=Av−vである。Isometric pullbackは∇_hと可換し、tensor∇^jvのLie derivativeにはVと∇Vだけが現れるから
\[
\|Av-v\|_{C^{q+1}(h)}\le C_q e\delta,
\qquad \|\beta_{\rm can}\|_{C^q(h)}\le C_qe\delta.
\]
必要な逆形式の一様C^q boundsとflow bufferの下でMoser場も同率となる。全深部tripleではe=O(m^{-1})、δ=O(m^{-1})であり、固定階ごとにO(m^{-2})を得る。Centered chain primitiveについてもH̃k=0からβ=H̃(ω−k)となり、同じ短い生成場と微分評価の下でO(m^{-2})である。主稿のclosed-corner GHは既存のchain flowのO(m^{-1})評価だけで証明している。

**Fiber保存との区別。** β_canのvertical成分の消滅は、元のorbitが既にLagrangianであることから自動的には導かれない。一般のpotential averagingの例として、compact product annulusの近傍で
\[
F=|z_1|^2+|z_2|^2+\epsilon\operatorname{Re}(z_1)|z_1|^2
\]
とする。十分小さいεではdd^cFは二つの複素一次元因子のKähler formの和なので、元のphase toriはLagrangianである。しかしz_1=re^{iθ_1}として
\[
d^c(AF-F)(\partial_{\theta_1})
=-\frac32\epsilon r^3\cos\theta_1
\]
は一般に零でない。この例がKEであるとは主張しない。`ke:relative-fiber-preserving` を使う際はchain primitiveを選ぶ必要がある。ωがcollar上で作用不変なら、Fも不変なのでβ_canも零になる。

### Volume frameのgaugeとorbit partitionの変更

同じ作用を固定してΩ′=uΩ（holomorphic unit）とだけ変えれば
\[
\beta'_{\rm can}-\beta_{\rm can}
=d^c(\log|u|^2-A\log|u|^2)
\]
はclosedである。Logarithmic base Dが可縮なReinhardt domainならu=ζ^n e^fと書ける。n∈Z²はwinding vector、fは一価正則関数であり、Afは正則かつtorus不変なので定数である。従って上の差はd Im fでexactとなり、Hamiltonian比較へ入る。

一方、座標そのものを
\[
\zeta'_1=\zeta_1e^{\epsilon\zeta_2},\quad
\zeta'_2=\zeta_2,\quad
\zeta'_0=\zeta_0e^{-\epsilon\zeta_2}
\]
と変えると、積方程式ζ_0ζ_1ζ_2=tとΩ′=Ωは保たれるが、|ζ′_1|は元のphase torus上で一定でない。従ってorbit partitionとHaar averaging operator自体が異なる。小さいunit変化を小さいisotopyとして比較できても、指定neck collarに相対的なsymplectic/Hamiltonian matchingや作用周期の一致は別に必要である。

### 点固定のrelative classと両端のperiod matching

同じsymplectic pathに対する任意のprimitiveの差γ_sはclosedだが、一般にはexactでない。相対Moser isotopyの生成場のdualは(φ_s^0)^*γ_sであり、isotopyが各時刻でHamiltonianになる条件はこの1-formのexactnessである。時間積分したfluxやendpointのHamiltonian同値とは区別する。上のcentered choicesではγ_s=−d(Hγ_s)がこの障害を消す。

ω_sが滑らかなcollar N上でsに依らず、σ_s=−∂_sω_sがNで零とする。Nを点ごとに固定するprimitive、すなわちdβ_s=σ_s、β_s|N=0の存在条件はrelative class [σ_s]∈H²(U,N;R)が零となることである。通常のrelative de Rham complexとextension/cutoffを使えるcollarを取り、必要なら少し縮める。時間についての滑らかな選択とflowの存在bufferは別に課す。

絶対primitive β_sが既にあるとき、同条件は[β_s|N]がrestriction H¹(U;R)→H¹(N;R)の像に入ることと同値である。十分性は、同じrestriction classを持つglobal closed 1-formを引き、残るexact restrictionをcutoff extensionで消すことで示せる。必要性は二つのprimitiveの差がglobal closedであることから従う。

特にU=B×T²、Bは可縮なcorridor、N=N_-⊔N_+は両端のfull torus collarsとする。RestrictionはR²→R²⊕R²の対角写像なので、両端の二つのtorus period vectorsの一致が条件になる。その差は対応するS¹を運んだcylinder上のσ_sの積分である。これは指定したmarkingとaction originを保つ相対同定の条件であり、自由なbase relabellingを許すfibrationの存在障害と同一視しない。

**着手方法。** 二段階平均とexact primitive transportは主稿 `ke:staged-neck-averaging` に証明した。Source-free固定base上のprimitiveと共通moment intervalも関連KE稿で確保した。次はactual familyでの全neck flow bufferと、複数endsの同一正則作用・reduced-circle foliationsを具体的に合わせる。Critical actionの直線性とsourceを含む接着は残り、既存の固定symplectic neck模型のtaming/cutoff評価をactual KE familyへ一様に移す証明はまだない。

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
`papers/threefold-blocks.tex`第25・33節：positive normal shell、membrane/focus collars。第26節：smooth focus Cartanとnormal degreeの障害。第34–35節：compact focus blockとnormal-trivial closed curve。第36節：actual補集合の境界写像・equivariant π₂・巡回被覆。第37節：normal ballへの相対補完・relative handlesとdisk group・接着の障害。第38節：weighted collars。Normal exterior Eのfibrationは構成済み。旧48 ports、V₀への延長、elliptic faceを消すboundary-free接着は未完成。全体稿は `papers/threefold-fibration.tex`。

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

**境界包含・被覆空間の現在の到達点：** 証明の正本は `papers/sections/threefold/local_blocks/focus_exterior_topology.tex`。Hopf商によってnormal exterior E≃S¹∨S²∨S³を同定し、V=V₀∪_{C'×S³}(C'×E)を用いてπ₁(V)=Zを証明した。境界のcurve loopsとa,bはVで消え、focus基底boundary lift tは生成元。両側への同時π₁写像のkernelはHeisenberg中心〈a〉である。全整数境界表も決定した（`tnc:all-boundary-homology-maps`）。F=regular torusはU側、T=aをt沿いにtransportしたtorusはV側に残る。H₂ boundary→VのcokernelはZ/e、[∂K_c]はH₃(V)の位数eのtorsion、H₃(V)/im boundary=H₃(X_d)、H₄ boundary→Vは全射。Framing・orientationを固定するが、H₃(X_d)のliftは非標準的なのでcanonicalなsplittingと混同しない。

Λ=Z[τ,τ⁻¹]に対し `tnc:equivariant-pi2` はπ₂(V)=Λ^(2g+1)⊕Λ/(e(τ−1))を与える。Universal coverのMVで[C']=e hとなり、deck不変性からe(τ−1)h=0が生じる。残りのaugmentation ideal (τ−1)Λはfreeなのでextensionがsplitする。整数torsion部分はΛ/eΛだが、coinvariants H₂(V)=Z^(2g+2)はfreeである。`tnc:cyclic-cover-h2` は全m≥1についてH₂(V_m)=Z^{m(2g+1)+1}⊕(Z/e)^{m−1}を証明する。有限coverではH₁(C')⊗H₁(E_m)=Z^(2g)の項を落としてはいけない。六次二重被覆はZ¹⁵⊕Z/4。

**再現と先行研究：** `python3 verification/verify_focus_exterior_topology.py --json` は17個のSmith algorithm自己照合、d6–20の60境界行列、m1–12の180被覆関係行列と180群環coinvariant行列を整数演算で確認する。一般の式は原稿の証明による。Auroux arXiv:0706.3207 §5.1のnodal model、Akbulut arXiv:1103.3137v2 Introduction/Figure 1のS⁴のfishtail分解、Hatcher Theorems 4.32/4.41・Example 4.45を一次資料で確認した。既知の模型・道具と今回の具体計算を区別し、包括的新規性は未確認。

## 三次元：normal補完と相対円板の現在の知識

証明は `papers/sections/threefold/local_blocks/focus_relative_filling.tex` に集約する。

**Positive construction。** `ncc:normal-ball-completion` は、K_c⊂int D⁴の余裕 a_*²+4π²(c+√q₊)²<L²を使い、商平面上のcompactly supported flowでψ_Aを作る。Inner blockを含むfilled diskではw−c、outer collarではidentityであり、H=|ψ_A(XY)|²はAとPoisson可換になる。ψ_A自体にsymplectic性を要求しない点が重要。全fiberの連結性とĜ⁻¹(R)=K_cは各reduced sliceのdiffeomorphism性から従う。C′との積は既存focus–hyperbolic fibersを保存する。商座標の図はintegral-affine図ではない。

**大域化の障害。** H=0は真のelliptic faceであり、そのwhole T² fiberと近傍のpartitionをcompact X_d上で保つと半空間germが残る（`ncc:elliptic-face-limitation`）。外側S³への接着だけでこのgermを消すことはできない。これはnormal exteriorのfibrationが存在するという成果と、境界のないglobal baseの未完成を分ける点である。

**相対handles。** Eはouter S³からHopf linkに沿う一つのround 1-handleで得られ、ordinary 1+2 handlesへ分けられる。逆向きは2+3で、唯一の2-handleのbased attaching wordはwhiskerと向きでbにできる。Knot isotopyやframingの自由な選択は主張しない。V≃V₀∪_i(C′×(S¹∨S²))はV₀からの写像を保ち、i=f_e∘q、q:C′→S²、[f_e]=e hである。CofiberはwedgeだがV自体はV₀とのwedgeではない。Curve 2-cell×normal 1-cellがe(τ−1)hの関係を担う。

C′×Eのouter側のminimal relative handle数は(1,2g+1,2g+1,1)、index1–4。H₄=Z、reverseではH₅=Zのため、どちら向きにも全二境界を保つWeinstein cobordismにならない（`tnc:no-weinstein-normal-transition`）。C°のboundary componentsがr≥1ならouter relative Betti数はindex1–3で(1,2g+r,2g+r−1)となる。これは側面∂C°×Eをrelative subspaceに含めない計算であり、puncture後のWeinstein構造の存在は未証明。

**Normal disk module。** `tnc:normal-relative-disk-module` はπ₂(E,Y)=ΛB、∂(fB)=f(1)b+f′(1)a、sphere subgroup=(τ−1)²ΛBを与える。Bは適切に選んだ唯一のreverse 2-handleのcore。任意のb-capではなく、B+(τ−1)²gBは係数がunitでなければΛ-basisにならない。Yの誘導被覆T²×RでFが実際のsolid torusで埋まるためcentral extension classは零。AbeliannessとPeiffer identityが境界kernelの作用を消し、一般relative Hurewiczで必要な作用quotientを正当化する。ν_relは旧sphere generatorとunit ±τⁿだけ異なり、marked orientationとの同一視は別途指定する。

**Curve disksの非可換関係。** `tnc:relative-disk-central-extension` でπ₂(V,∂U)はM=π₂(V)によるπ₁(C′)×Z²のcentral extensionとなり、∏[A_i,B_i]=e h。Curve diskを変更してもcommutator積は変わらず、t作用との整合性がe(τ−1)h=0を再現する。Hyperplane degree ℓでMをZへ押し出すとEuler数eのcircle bundle P_eのπ₁とZ²の積になる。全三次元pairの各curve diskへのt作用、embedded disksとsmooth framingはまだ決定していない。∂UはLagrangianでないので相対群全体へsymplectic areaを定義しない。Sphere subgroupではarea=aℓ、c₁=(5−d)ℓ。

**Clean diskの制約。** Ω=dX∧dYについてμ(a)=0, μ(b)=2（`ncc:normal-maslov-marking`）。Normal C²内のLagrangian diskがregular torusと境界でcleanに交わるなら、境界ma+nbはn=0かつmA=0。逆向き2-handleのword b+kaをこの種のcoreで実現する案は使えない。Elliptic collapseのtransverse diskはsymplecticなので矛盾しない。Curve方向へ動くdiskやnonclean/singular diskの非存在には拡張しない。

**一次資料と位置づけ。** M. Symington, *Four dimensions from two in symplectic topology*, Proc. Sympos. Pure Math. 71 (2003), 153–208, arXiv:math/0210033, §6.1 Lemma 6.3 / Theorem 6.5は標準nodal trade。D. Asimov, *Round handles and non-singular Morse–Smale flows*, Ann. of Math. 102 (1975), 41–54, DOI 10.2307/1970972はround handleの出典（公式書誌を確認、本稿のhandle分解は直接証明）。K. Cieliebak–Y. Eliashberg, *Flexible Weinstein manifolds*, arXiv:1305.1635, §1.1 pp.2–3はisotropic stable manifoldsとindex制限。R. Brown, JLMS (2) 22 (1980), 146–152, DOI 10.1112/jlms/s2-22.1.146, [author PDF](https://www.groupoids.org.uk/pdffiles/whiteheadthm.pdf) §2はrelative crossed module。B. Conrad, [Group cohomology and group extensions](https://math.stanford.edu/~conrad/210BPage/handouts/gpext.pdf), §2はH²によるcentral extension分類。Hatcher *Algebraic Topology*, Props.0.18–0.19、Thms.4.37,4.57はhomotopy pushout、relative Hurewicz、cohomology表現。これらの道具自体と本研究の具体計算を区別し、包括的新規性は未確認。

**次の着手。** Toric outer collarとV₀側を接続し、内部elliptic faceの近傍を変える。C′を有境界曲面へ切る案では、上のH₄障害を除いた後に側面のwhole fibers・action periods・coorientationを定める。Normal diskの二階差分とcurve relationを保ち、global circle actionの障害を避けるgenerator変更領域が必要である。

## 検証
今回の相互点検対象はnormal ballへの明示的補完、elliptic base germ、round handlesとrelative pushout、normal relative crossed module、全補集合のcentral extension、Weinsteinおよびclean normal diskの障害である。原稿の証明と独立点検を行った。既存の補集合位相・short-circle averaging・KE局所解析の証明と点検記録は保持するが、大域接着全体を再監査したものではない。

`python3 verification/verify_focus_relative_models.py --json` を実行し、243 Laurent多項式の境界・整数除法、1,701 deck作用、15 closed-curveと60 punctured-curveのKünneth計算を正確な整数演算で確認した。有限代数検算は相対Hurewiczの仮定・handle geometry・symplectic補完の証明を代替しない。外部査読と形式証明は未実施。

2026-11-21に三次元局所稿190頁・全体稿211頁をLuaLaTeXとlatexmkで組版し、未解決の参照・引用がないことを確認した。新節の代表頁と図はPDFを画像化して表示を点検した。曲面主稿改訂8の130頁は保持した組版記録で、今回再組版していない。既存節の2.27ptのOverfull警告一件は残るが、新節にはない。GitHub反映は組版と別に確認する。
