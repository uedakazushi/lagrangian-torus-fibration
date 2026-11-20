# 現行研究ノート：一般型曲面のLagrangian torus fibration
更新：2026-11-21 / v2.5

主稿 `papers/surface-lagrangian-torus-fibration.tex` と整数接着 `papers/quintic-integer-gluing.tex` を正本とする。以下は曲面・KE局所幾何・作用・アフィン接着に関する現在有効なノート。三次元の原稿と相対円板群・補集合の計算は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) を正本とし、こちらに重複保持しない。

## 最優先目標への接続と最初の未解決補題

現在の目標は、主稿 `ke:global-realization` のactual KE–Lagrangian fibrationによる全曲面GH極限の実現である。対象・達成条件・K0–K5の着手順は [研究方針](../00_research_plan.md)、外部定理の正確なpath・label・確認commit・残る仮定は [KE依存表](ke-dependencies.md) を参照する。ここには証明を進めるための知識を残し、課題一覧を重複させない。

固定 source-free compact 基底上の moving normal strip では、actual 計量で一定の buffer と $O(m_t^{-1})$ の短円を証明した（主稿 `ke:fixed-base-neck-moser`）。$\varphi_t=\log(\omega_t^2/\Omega_{t,d}^{\rm low})$ とし、大域の $\varphi_t\ge-C$ と $dd^c\log\Omega_{t,d}^{\rm low}\ge c\omega_{\rm FS}$ を、正則包含の Chern–Lu 不等式に組み合わせる。最大値原理から $\operatorname{tr}_{\omega_t}\omega_{\rm FS}\le C e^{A\varphi_t}$。固定 pair chart では体積包絡が $\varphi_t\le C$ を与える。入れ子座標間の固定射影幅から actual 球を確保し、局所 Chern–Lu を complete annulus–disc に適用して actual 二側比較を得る。法線深度を $m_t$ から $m_t/2$ に広げ、残余基底にも固定した余裕を取ることで、Moser map の source と像の両方が同じ内側 strip を覆う。

Residual collarを三重点へ動かす共通flow領域と葉の一致は、以下の遅いexhaustionで確保した。Source gate の $|x|\asymp |t|^{1/2}$ では固定射影座標の距離下界は法線の rescaling 幅を検出しない。 一方、source 模型 $xy=tz$ の法線円は gate まで残余方向の rank-one 下界と annulus–disc の体積上界で短くなる。正則ベクトル場 $x\partial_x-y\partial_y$ の Bochner 不等式で gate の $O(L_t^{-1})$ 評価を central bidisc に伝播できる（主稿 `ke:source-short-circle`）。固定 shell 上の成分KE収束と cusp 下界を使い、対角選択で十分遅く縮む source 領域に限り、共通 Moser source・像と actual focus–focus germ を構成した（`ke:source-diagonal-moser`）。所定の速さで動く法線境界の下界は別問題である。固定残余領域内の閉じた pinched torus は次の共通neckで構成する。

Source と通常 pair の共通化を主稿 `ke:projected-source-normal-form`, `ke:projected-source-neck` で証明した。固定残余基底で射影を保つ正則 Morse 座標 $x'y'=t h_t(p)$ を用いる。capped density と短円評価は $O(t)$ 座標変更で保たれ、固定 shell の対角選択で source を含む一つの actual Moser map を得る。共通 primitive の moment と基底射影の組で商は $I_t\times P$。指定した残余葉の持ち上げから、閉じた一重 pinched torus と saddle fiber が得られる。三重点側との共通開領域と全intersectionのfiber一致は、以下の部分fibrationで実現する。

三重点と射影neckの座標接続の正本は `papers/sections/paper/ke_neck_corner_transition.tex`。全三重点を避ける共通の無限遠超平面内に各二重線の射影補空間を選び、三平面の式 $q_0q_1q_2=tU$ のunitを三乗根で対称に除く。射影Morse変換の後にbase-only gaugeを施すことで、三つの端を同じexact triple chartと比較できる。固定 $\sigma>0$ のarm $\ell_i,\ell_j\ge(1+\sigma)\ell_k$ では、座標比の主枝対数 $e_{ka}$ が全phase・全固定階で $\|e_{ka}\|_{C^q(h)}\le C_{q,\sigma}e^{-c_\sigma m}$ を満たす。深度の相対幅が一定の正規化正則chartでCauchy評価を使い、$L_t$ に依存する微分損失を避ける。

三つの分離したarmで積を保つsmooth補間を行うと、一つのtorus作用が各端の射影neckのnormal circleに厳密に一致する（`ke:three-arm-coordinate-interpolation`）。補間帯では非正則なのでKähler性を主張せず、共通toric模型との小摂動から平均と凸pathのtame symplectic性を証明する。Canonical primitiveの差はbase-only closed formと一価関数のexact differentialに分かれ、normal periodは一致する（`ke:transition-normal-primitive`）。残余cycleのperiodは同じとは限らない。

`papers/sections/paper/ke_relative_corner_patch.tex` はcentered averagingの順序比較を定量化する。模型に近いprimitiveを選ぶと、比較Hamiltonianそのものが $O(e\delta)$ であり、領域の直径を掛けずにcutoffできる。Actual tripleでは $e,\delta=O(m^{-1})$ なので $O(m^{-2})$。三つの端にそれぞれ指定したnormal-first構成を、一つのactual corner bundleへ組み込める。小さいreduced circle graphを固定collarの外で恒等なdiffeomorphismへ延長する明示式も `ke:reduced-collar-graph` に置く。単一armでは、共通moment stripと外側marginを指定すればactual reduced葉のgraph評価も証明した（`ke:single-arm-reduced-graph`）。Normal生成場の長さを $a$ とするとmoment差が $O(a b^{-2})$、normal微分が $\ge ca$ なので、normal深度が極端に大きくても逆係数 $a^{-1}$ の損失は相殺される。Graphの $C^1$ はmomentを固定した残余座標に関するものとし、無重みのmoment微分には同じ一様性を主張しない。Source-inclusive neckとの共通moment stripとflow領域は、`ke:neck-corner-diagonal-matching` で別途確保する。

単一armで必要なmoment区間の存在も `ke:arm-common-moment-strip` で実証した。残余深度 $b\asymp b_0\to\infty$、$b_0/L\to0$ とし、normal端を $\ell_i=Kb$ または $\ell_j=Kb$（固定 $K>1+2\sigma$）に取ると、canonical momentは
\[
 \mu,\nu=\pm\frac{4\pi}{Kb}
 +O\!\left(b_0^{-2}+\frac{(b_0/L)^2}{b_0}\right).
\]
従って $I_t=[-c_*/b_0,c_*/b_0]$ の各levelが全残余annulusで一意に存在し、固定比のarm marginを持つ。Source-inclusive neckとの共通区間・共通flow domainには、下記の固定段階の選択を追加して使う。

微分評価の障害：単に $\ell_i-\ell_k\to\infty$ では足りない。例えば $f=\zeta_i/\zeta_k$、深度 $(N+\log N,N+\log N,N)$ では $|f|=N^{-1/2}$ だが、cusp単位ベクトルでの微分は $N^{1/2}$ と増大する（`ke:coordinate-czero-obstruction`）。座標比の値が1に近いことを、Moserの正値性に必要な微分小摂動へ読み替えない。

固定残余compactの各座標では、`neck:prop:volume-envelope` から法線方向の積分評価を得た（主稿 `ke:neck-integrated-normal-energy`）。$s=-\log(|u|^2/r^2)$、$d(s)=\min(s,M_t-s)$ とし、周期1生成場の軌道平均エネルギーを $E_t$ とする。$\Omega=du/u\wedge dz$ に対する対数体積の角度平均 $\bar F_t$ は $-2\log d(s)+O(1)$、かつ $E_t=8\pi^2\partial_s^2\bar F_t$。よって $\int_m^{M_t-m}E_t(s,z)\,ds=O(m^{-1})$ が残余点 $z$ に一様に成立する。例外深度の測度は $E_t>A/m^2$ に対し $O(m/A)$ であり、例外集合の位置は $z$ に依存する。

同じ $z$ に沿う動径経路には一つの角度を選んで長さ $\int_a^b ds/d(s)+O(1)$ を得る（`ke:neck-axial-upper`）。両端円が短ければ任意の端点を結べる。固定 source-free 基底で同じ normal moment を持つ点については、残余点を変える接続も原稿 `ke:fixed-base-moment-connectors` で解決した。深度は、$|\mu|=O(M_t^{-1})$ なら両側とも $M_t$ と比較可能、それ以外は符号に応じた片側深度が $|\mu|^{-1}$ と比較可能である。一定深度の水平持ち上げ・動径弧・短い円弧を合わせると、level全体の actual ambient 直径は $O(1)$、Moser像でも同じ、正規化後は $O(R_t^{-1})$ となる。葉内経路やMoserの $C^1$ 評価は使わない。Sourceを含むlevel、moving residual collar、異なるmomentをまたぐ木全体と全曲面の下界は残る。

Moser 流では軌道全体の最大速度を軌道平均エネルギーの平方根で置き換えられる（`ke:neck-averaged-speed`）。外側の深部領域の実計量での境界距離 $\delta_t$（上限1）が $m_t\delta_t^2\to\infty$ を満たせば、局所 Chern–Lu と体積上界から共通の source・像を得る（`ke:neck-shrinking-buffer`）。この縮小条件は残余 collar を動かす場合にも候補となる。

固定残余基底上で両側の moving cut $m_t$ における canonical moment は符号が逆で絶対値が $m_t^{-1}$ と一様比較可能である（`ke:neck-deep-moment-strip`）。よって同じ actual Moser map の下で、深部に共通の縮小 moment interval を置ける。K1の局所的な成功後も、第二periodとreduced葉の同時整合、source・branch・coreの被覆、全曲面のshortcutとportalを別々に検証する。任意のMoser移送による定性的存在と、\(p_T\pi_t\) の距離歪み消失も区別する。

大域距離を得る経路は二つある。KE側の未解決解析入力を実証して既存近似写像 \(\Phi_t\) と \(p_T\pi_t\) を一様に比較するか、同じ \(p_T\pi_t\) に対して全域の距離下界・liftによる上界を直接証明する。前者の条件付き定理を無条件の入力にせず、後者では基底上の人工計量をactual全空間の距離で置き換える根拠が必要である。

## 共通の end collar での actual fiber の一致

主稿のラベル `ke:normal-flow-naturality` が自然性の正本。全円軌道を含む共通plateauで同じcentered kernelを選ぶと、$G^*K_N\omega_N=K_\alpha G^*\omega_N$ であり、全trajectoryがそこに留まる限り $\phi_NG=G\phi_\alpha$ が厳密に成立する。Primitive $\lambda$ の一致を仮定せず、flowを決める $K\omega$ を比較する。Canonical normal momentの一致と合わせれば、corner torusはneckの同じmoment reduction上の円の全逆像として一致する。

主稿 `ke:neck-corner-diagonal-matching` は、残余cut $b_j$ と固定compact $P_j\Subset P_j^+$、それらの定数を支配するnormal cutoff $n_j\gg b_j$、共通moment区間 $I_j$、最後に $t_j$ の順で選ぶ。三重点側の $a=4n_j$ と $c=4n_j$ におけるmomentはそれぞれ $\pm\pi/n_j$ と比較でき、$I_j$ を狭くして全levelをdeep normal stripへ収める。全circle orbit・第二段の像・第一段の全trajectoryを共通plateauとneckの内側tubeに含められる。この共通collarの一致を、次の全intersectionの制御へ用いる。

Reduced graphに合わせて残余foliationをmomentに滑らかに依存させることは `ke:moment-dependent-neck-foliation` で許される。変更をsource・saddleの近傍とcollar外で恒等にすれば、閉pinched torusとsaddle fiberの型を保つ。固定 $t$ ごとの滑らかさでよく、無重みのmoment微分の一様な小ささは不要。残余基底は元の射影点 $p$ であり、$h_t(p)$ はsource近傍以外でglobal座標としない。Endのradial座標は $Z_{k,t}=C_D^2/h_{k,t}$ を使う。

`ke:neck-corner-saturated-union` はcorner cut $m_t=6b_j$ とneckの境界葉 $B=7b_j$ を分離する。先に $5b_j\le b\le9b_j$、normal深度 $\ge n_j/2$ の広い領域でnormal-first構成へ補正する。Neckの全normal trajectoriesはouter tube内にあり、frame差を引いてもlocal normal深度 $\ge3n_j/4$。そこで $|d\log b(Y_N)|\le C/(n_jb_j)$ を使うfirst-exitにより、neck imageは $b<8b_j$ に留まる。Cornerの最小深度と元の射影の線形性から交点で $b\ge6b_j-C$ を得る。逆normal flowの自然性でmomentを同定した後にnormal深度 $\ge4n_j$ を結論する順序で、循環を避ける。Reduced graphと葉でのtrimから全intersectionが全torusで飽和し、source・saddleを含むactual部分fibrationとなる。End markingは共通torus同定に合わせて選び、任意に独立な第二periodの一致を含めない。全曲面被覆とcore接着は残る。

## Source中央部の体積・momentとactual接続

正本は `papers/sections/paper/ke_source_connectors.tex`。$xy=tz$、$t=\tau^2$、$(x,y,z)=(\tau X,\tau Y,XY)$ として固定bidiscを使う。`ke:source-central-density` はdensityを $L^{-2}|dX\wedge dY|^2$ と両側比較する。下界はcapped canonical density、上界は正しいoriented gateのannulus–disc volume上界と中央の最大値原理による。Canonical potential $u_t=\log(\omega_t^2/|dX\wedge dY|^2)+2\log L$ は有界で $dd^cu_t=\omega_t$。射影を保つMorse座標にも適用できる。

`ke:source-central-moment` は同じcanonical primitiveで $|\mu_t|\le C/L$、固定点で $\mu_t=0$ を与える。Normal平均potentialの凸性と中央からoriented arm断面までの割線を用いる。Base-only変更はnormal momentを変えず、独立な加法定数の調整を行わない。`ke:source-central-mean-distance` は固定Euclidean体積に関するtrace積分と平均二乗ambient距離を $O(1)$ に抑える。部分積分と線分の二点積分による。ほとんどの点からなる部分集合の径は得られるが、全点・固定点・特定moment levelの径にはならない。

`ke:source-central-short-escape` はactual inradiusを $O(L^{-1/2})$ に抑える。Density上界から $\operatorname{tr}_{g_t}g_{\rm E}\ge cL$ を得て、大きさ $O(1/L)$ の非負Laplacian barrierを作る。Ricci下界による距離二乗のLaplacian comparisonと最大値原理で、全中央点からあるgateへの短い退出を得る。`ke:source-central-arm-connectors` はgateから正しいarm内を $s_x=\kappa L$ 又は $s_y=\kappa L$ まで進め、全費用を $O(1)$ とする。終点の残余座標・momentは指定しない。

固定連結source-free compact基底では `ke:fixed-base-central-band` により、固定 $A>0$、$m_t\to\infty$、$m_t=o(M_t)$ の下、$|\mu|\le A/M_t$ のcentral band全体がactual径 $O_{P,A}(1)$ を持つ。異なるmomentも含み、Moser像には $O(m_t^{-1})$ の端点費用だけを加える。両normal深度 $\ge\kappa_A M_t$ をmomentの片側下界から導き、水平・動径・円弧を組み合わせる。

Source側の `ke:source-central-band-reduction` は、固定residual disc、人工境界からの余裕、normal最小深度の下で、$|\mu|\le A/L$ の全点を固定rescaled coreへ $O(1)$ で接続する。従って中央帯の残る径問題はcore全点の径、またはcoreからsource-free shellの $|\mu|\le A'/L$ への $o(R)$ 接続に帰着する。一般の同一moment集合については、指定した残余境界への退出条件 `ke:eq:source-moment-exit-input` が十分であるが、これは未証明。Central inradius、平均距離、全source fiberの径、長いnormal armsを含むneck全体の径を区別する。

`ke:source-potential-modulus` はGuedj–Guenancia–Zeriahi（参考文献キー `GGZDiameter`、Proposition 1.4）の局所距離評価を用いる十分条件を記す。Potential $u_t$ に一様な連続度 $m$ があり $\int_0^{r_0}\sqrt{m(r)}\,dr/r<\infty$ なら、固定coreのambient径は $O(1)$。このsquare-root-Dini modulusや一様Hölder評価自体はまだ証明していない。有界potentialから自動的に導いたり、同論文の大域Kähler class仮定を局所族へ無条件に適用したりしない。

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

遅いexhaustionでflow生存・共通bufferとtriple endsの葉の一致は実証した。残るactual入力は、部分fibrationの外を含む全域被覆・core接着と全点の距離評価である。KE側 `neck:lem:rank-one-circle` はresidual rank-one下界とvolume上界だけでnormal circle長を抑えるが、その下界とactual bufferを証明する必要がある。固定residual境界の影響が消えないexact negative KE productの例があるため、normal深度だけからproduct asymptoticsを推論しない。


## 全深部三重点の actual semi-flat 比較
任意の固定次数 d≥5 の一般位置全平面退化で、三重点の全深度比・全角度に一様な actual KE 比較を証明した。正確な座標 ζ0ζ1ζ2=t、ell_i=−log|ζ_i|²、L=−log|t|²、R=log L とし、k_Lをlogarithmic simplex上のcomplete toric KE form、その実計量をg_L^sfとする。十分大きい固定m1と各qのCqについて、m≥m1、min ell_i≥mで
\[
\left|\log\frac{\omega_t^2}{k_L^2}\right|\le C/m,\qquad
\|g_t-g_L^{sf}\|_{C^q}\le C_q/m.
\]
定数は固定dと族に依存してよい。次数一様性は主張しない。証明の正本はKE主稿 `coarse:thm:full-triple-tensor`。

固定toric模型の存在・完備性にはZhang (2015), §2.1, Theorem 2.1 / Proposition 2.2を用いる（退化族のTheorem 2.4とQ-factorial仮定は使わない）。ψ_L=log L−Σlog ell_iに対してψ_L−(log3)/2≤φ_L≤ψ_L、V_L/3≤k_L²≤V_Lを内外にずらした障壁で証明する。Complete模型から三つの半平面へのYau Schwarz lemma、determinant比較、内部正則性により一様cusp geometryを得る。凸性からfacet shiftのlog-density差をO(1/min ell)とし、actual計量を内外のsimplex KE metricsでvolume比較する。Savinの小摂動定理でtensor・全高階誤差へ移る。Actual metric bufferや(TC)/(PBE)を前提としない。

Actual側の大域入力は `coarse:cor:degree-d-volume-lower`。Adjunction residueでcanonical densityを固定し、backgroundによるHermitian frame errorの吸収と各正のcap方向のminorから六型のdeterminant下界を証明する。Sourceでは元のplane coordinatesを保つexact xy=tzとrescalingにより二つのcap係数≥c_d/Lを使う。Compact minimum原理からactual volume下界を得る。この依存部分の証明と適用条件はKE側の原稿に明示されている。現行整備ではその所在と仮定を確認し、全証明の独立再監査は行っていない。


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

全fiberのintrinsic/ambient diameterはO(1/R)、正規化後はO(1/R²)、raw-map誤差はO(log R/R)。Squareの共通辺と共通頂点でも同じregular T² fiberである。これらを既存大域fibrationのsource・branch・coreのsingular fibersとは同定しない。V_t外を通る全曲面のshortcut、部分fibrationの外を含む被覆とcore接着は未解決。新規性の網羅的確認と外部査読・形式証明は未実施。

一般のcut $m_t\to\infty,\ \log m_t=o(R_t)$ についても、同じsoftmaxとMoser mapの射影が局所GH近似になることを `ke:slow-cut-closed-corner-gh` で証明した。内在・protected距離のdistortionは $C[m_t^{-1}+(\log(m_t+1)+\log R_t)/R_t]$、fiberの元の尺度の内在径は $C/m_t$。内部squareを幅 $\delta=(\log(m+1)+4\log R)/R$ だけ縮め、pruningでは $S=R-\log m-\log R$ を使う。$m_t$のparameter微分を使わず、stepwiseな遅いexhaustionにも適用できる。この遅いcutを `ke:neck-corner-saturated-union` の対角選択へ用いて部分fibrationを構成した。全曲面への延長は別課題である。


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

主稿 `base_topology.tex` の `topo:ke-map-compatibility` に、$\operatorname{dis}(\Phi_t)\le a_t$ と $\sup_xd_\square(\Phi_t(x),p_T\pi_t(x))\le b_t$ から $\operatorname{dis}(p_T\pi_t)\le a_t+2b_t$ を得る比較命題と証明を置いた。Ambient fiber diametersは同じ量以下、GH距離はその半分以下である。一般的新規性は主張しない。この初等比較の証明の点検と、actual $a_t,b_t\to0$ が未証明であることを区別する。

**具体的な次の課題：** 全phaseのmoving triple比較と閉cornerの内在・保護領域内のGH同定を入力として、actual neck collarのorbit partition、action periods、定量的bufferを一致させる。`ke:relative-fiber-preserving` を適用できる開overlapを構成し、sourceのpinched torus、branchのS¹×figure-eight、coreへ相対的に接着する。必要なのは全特異領域を含む一様評価と大域no-shortcutであり、regular fibersの点ごとの収縮では不足する。Action-affine structureだけからcanonicalなRiemannian基底計量は決まらない。


## 局所fibrationの証明と解析入力
曲面側の着手対象は複素次元2でのKE極限とLagrangian fibrationの適合性である。主稿の `papers/sections/paper/ke_fiber_compatibility.tex` に次の証明を置いた。

- `ke:short-torus-averaging`：自由な正則 $T^2$ 作用、torus不変Hermitian計量 $h$、$c h\le g_\omega\le C h$、torus上のperiod零を仮定する。作用の周期1生成場の長さの和を $e$ とすると、平均化のchain homotopyから長さ $O(e)$ のprimitiveを作り、一つのMoser flowで領域全体にLagrangian fibrationを構成する。変位は $Ce/(2c)$ 以下、ambient fiber diameterは $\sqrt C e(C/c+1/2)$ 以下。高階微分比較は使わない。
- `ke:triple-hexagon`：$\zeta_i\zeta_j\zeta_k=t$ の三つのsquareを一つのhexagonとして全phase torusで実現し、raw-depth mapとの誤差を $O((1+\log m_t)/R_t)$ に抑える。
- `ke:triple-moving-fibration`：全phaseを含む moving domain $\min\ell_a>m_t/2$ 上の一様tensor比較を追加仮定すれば、actual負KE形式に対する局所fibrationが得られ、そのambient fiber diameterは元の尺度でも $O(m_t^{-1})$。$m_t=R_t\to\infty$ とできる。負KE equationにより局所canonical trivialization上で形式がexactとなるのでperiod条件は満たされる。

これらは原稿に条件と証明を保持する局所結果である。Averaging–Moserの基本方法はRuan, arXiv:math/0309177v2, §3に先行し、一般的新規性は未確認。H-minimal/special Lagrangian性、大域接着、singular fibersの計量評価は結論しない。

**解析入力の区別：** 関連KE主稿の `coarse:prop:density-counterexample` により、負KE計量であってもbounded volume densityから一様tensor比較は導けない。五次coarse metric packageには独立な $(\mathrm{TC})_5$ が必要であり、その無条件な検証は未完成である。これは対象compact familyの反例ではない。全深部三重点のfull-orbit moving tensor比較は全固定d≥5で検証した。Source等を含むexterior全体への拡張は未解決である。

### Averaging–Moserの先行研究
W.-D. Ruan, *H-minimal Lagrangian fibrations in Kähler manifolds and minimal Lagrangian vanishing tori in Kähler–Einstein manifolds*, arXiv:math/0309177v2, https://arxiv.org/abs/math/0309177v2 。§3 Proposition 3.1はpotentialのtorus平均、Lemma 3.3はHamiltonian-gradient flowを扱い、Theorem 3.1はhomothetic toric potentialと一様 $C^\infty$ quasi-isometryの下でH-minimal fibrationを構成する。Theorem 4.2はsimple toroidal canonical degenerationの最大退化点へ消えるminimal torusの存在を示す。

本研究の補題はperiod-zero、$C^0$ tensor比較、短い生成場だけを用いてprimitiveとambient diameterを直接評価する。Ruanの高階幾何とH-minimal性の結論は求めない。既存方法の定量化として位置付け、新規性は未確認。ZhangのTheorem 2.6の個別generalized special Lagrangian torusの存在とも、全域のsingular fibrationとも区別する。

### 固定領域と移動領域の区別・相対接着への入口
主稿 `ke:fixed-simplex-scale` の計算により、固定simplex compactaは径の尺度のtriple vertexしか見ない。関連KE研究ノートの「固定領域の収束から径の尺度へ移る際の障害」に、固定compacta上ではcusp metricと完全一致し、全体で一様に粗比較できるにもかかわらず、正規化した区間長が $1$ から $3/2$ に変わる一次元例を証明付きで収録した。KE反例ではなく、sharp moving estimatesの必要性を示す例である。

主稿 `ke:relative-fiber-preserving` は、torus-saturatedな**開**collar N上で元のorbitsが既にactual ω-Lagrangianであれば、β=Hω、H=K_1+A_1K_2というchain primitiveがvertical vectorsを消すことを用いる。ω_sも同じvertical distributionをLagrangianに保つため、Moser場はverticalであり、各fiberと基底値が保存される。ωの作用不変性は不要。Centered chain primitiveでも同じ証明が成立するが、同じdβを持つ任意のprimitiveへの置換では消滅条件が保存されるとは限らない。

`ke:relative-neck-matching` は、別のactual Lagrangian fibrationがこの開overlap上で同じorbit partitionを持つなら、基底collarを同定して写像を接着できるという局所系である。各点の固定や単一境界上の一致だけを用いた接着は主張しない。点ごとの固定が必要なら、既存の `ke:relative-averaging` のcentered kernel 1/2−sと作用不変collarを使える。許容射影と遅い対角選択では共通葉・normal moment・bufferを `ke:neck-corner-saturated-union` で実証した。独立な第二periodの一致は含まない。

定数係数monomial変更ζ'=c(t)ζ^A、A∈GL(2,Z)はphase orbit partitionを保つ。一方、非定数holomorphic unitを含む変更ζ'=ζ^A u(ζ,t)は一般に保存しない。二つのtorus actionsが同じoverlapに存在するだけでは相対補題の仮定にならない。Sourceのcritical valuesについても `ke:source-marking` のcore交差仮定の下でp_T(b_t)→e_i+e_jが必要であり、固定された任意の内部markingは使えない。


## 相対接着の補助計算：primitiveの選択と障害

以下はregular torus領域での補助計算であり、仮定と証明をこのノートに保持する。主稿の `ke:relative-fiber-preserving` の証明を重複させず、primitiveの変更、整数基底の変更、collarの点固定に関する情報を整理する。選んだneckとcornerの共通葉・normal moment・bufferは上記部分fibrationで実証した。独立な第二periodとcore接着には追加確認が必要であり、補助計算の新規性も未確認である。

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

**着手方法。** `ke:neck-corner-saturated-union` を出発点とし、残るnormal領域とcoreを含む全域への相対延長を調べる。距離側ではsource中央coreの全点径・shellへの接続、または `ke:eq:source-moment-exit-input` の同一momentでの退出を扱う。Potential連続度の十分条件は未検証入力として保持する。全source fiberの径を既証明と扱わず、全曲面のno-shortcutと木上のfiber合併の費用を別に構成する。


## 複素次元2：先行研究・singular fibersの確定事項（2026-11-20）
本研究の曲面X_d⊂P³, d≥5の一般SNC gluingと、全平面模型の明示的なsingular fiber型を区別する。主要な定理は papers/sections/paper/geometry_main_statements_v17.tex の main:global、nodeの線型monodromyは invariants_examples.tex、より詳しい先行比較は geometry_introduction_v25.tex。

**一次資料の比較：**
- I. Smith, *Torus fibrations on symplectic four-manifolds*, Turkish J. Math. **25** (2001), 69–96, https://journals.tubitak.gov.tr/math/vol25/iss1/4/ 。Homologically essential Lagrangian toriとtame singularitiesという追加条件下での閉四次元多様体の制限定理。本研究の分岐・core特異ファイバーへの直接適用は、tamenessとregular torusのhomology classの検証なしにしない。
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
**Singular fiberは一般にsmooth embedded Lagrangianではなく、各smooth stratumがisotropicなstratified fiber**として定義している。Core skeletonも一般のdで一つの固定したpants型ではない。この基本的なlocal topology、個数、Euler数の証明と先行研究との範囲比較は原稿に保持する。幾何学的gluing証明全体の独立監査はなお必要である。


## 五次整数接着：保持する独立課題
全pair productsが狭義正の四ray整数データの正weightsはmatchingと同値。G5_14両単位枝の{5,0,0}を排除し、{4,1,0}に限定したと原稿は記録する。必要支持はG5_14、G5_16、G5_17の3型26標識。存在・幾何的非同型類の個数とは異なる。三高Dの一般同時非負性と一般分母剛性は残る。
これらはP0の全域GH実現に必要な場合以外は後順位とする。証明・計算資産は維持し、独立した分類の未完了をKE研究の停止理由にしない。


## KE退化との分岐基底の位相的比較
曲面基底 \(B_d(T)\) の三価木 \(T_{ij}\) を収縮する既存の \(q:B_d(T)\to\operatorname{Sk}_2\Delta^{d-1}\) と、KE候補 \(\mathcal C_d\) の正規化同相の逆を合成すると、**labelを保ち点逆像が可縮な** \(p_T:B_d(T)\to\mathcal C_d\) を得る。一般次数の厳密な証明は `papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`。\(d=5\) では同相、\(d\ge6\) では両者は同相ではない（辺の局所分岐次数が異なる）。KEのGH極限や作用アフィン計量との一致は主張しない。

整数鎖複体の主張を検査するため、\(d=5,\dots,8\) の \(B_d(T)\) と \(\operatorname{Sk}_2\Delta^{d-1}\) の \(\partial_1,\partial_2\) の階数を独立に計算して、\(b_1=0\)、\(b_2=\binom{d-1}{3}\) と一致した。再現コードは `verification/verify_ke_base_topology.py`。これは有限体 \(\mathbb F_{1000003}\) 上の有限検算であり、整数係数の一般定理の証明は本文のexplicit chain contractionが担当する。


## 人工的基底計量の鋭い収束速度と幾何学的比較の核心
$p_T:B_d(T)\to\mathcal C_d$ に補助piecewise Euclidean metric $h$ を固定し、$|v|_\varepsilon^2=|dp_T(v)|_\square^2+\varepsilon^2|v|_h^2$ の内在距離を考える。graph correspondenceのdistortion $\mathcal D_\varepsilon$ は、$d=5$ で $\Theta(\varepsilon^2)$、$d\ge6$ で $\Theta(\varepsilon)$ と鋭く決まる（主原稿に読み込む base_topology.tex の topo:metric-collapse-sharp）。$d\ge6$ の下界は同一fiber内の正の $h$-距離に由来するが、**GH距離の下界ではない**。

実際の基底長さ計量 $d_t$ に対する十分条件（topo:finite-portal-criterion）は、(N) global no-shortcut誤差 $\alpha_t$、(S) square segment liftの乗法誤差 $\sigma_t$・加法誤差 $\lambda_t$、(F) 同じfiberの接続費用 $\kappa_t$。最大square数 $N_d=d\binom{d-1}{2}$、直径 $D_d$ について
\[
\operatorname{dis}(p_T)\le\max\{\alpha_t,\ \sigma_tD_d+N_d\lambda_t+(N_d+1)\kappa_t\}.
\]
二枚のunit squareを一頂点で貼り、二枚を一枚に折る反例では(N),(S)が誤差零でも(F)が成立せず、$d_{\rm GH}\ge\sqrt2/2$（topo:portal-counterexample）。したがって局所模型だけでは大域収束は言えない。実際のLagrangian action metricの長さ完備化、枝・coreへの延長、および(N),(S),(F)の確認は未解決。新規性は未確認。


## 六次Petersen分岐基底の対称性
$d=6$ で全ての頂点リンクをPetersenグラフとするラベル付き木系はちょうど六つであり、$S_6$ はこの集合に推移的に作用する。固定した一系の安定化群は位数 $6!/6=120$、指数6。従ってその一系の選択は座標置換の全 $S_6$ 対称性を保たない。KE候補 $\mathcal C_6$ は自然に $S_6$ 対称なので、Petersen分岐基底とのラベル付き比較を対称に行うには六つの木系全体を管理する必要がある。証明は base_topology.tex の topo:petersen-symmetry、全15 perfect matchingsと六one-factorizationsの有限列挙・安定化群位数は別に確認した。これは任意の別構成やラベル忘却後のシンプレクティックな対称性の不存在ではない。

## 検証状態
2026-11-21 / v2.1では、目標P0の量化・規格化・actual/ambient距離・外部仮定の整合を別担当が点検し、依存定理の所在を確認した。全解析証明と大域接着証明の独立再監査を完了したものではない。主稿改訂9をLuaLaTeXで132頁に組版し、引用・参照、PDF/SyncTeX、変更箇所の表示を確認した。重複ラベル・欠落字形・overfull警告はない。構成検査と実行環境検査も通過した。

既存整数計算の証明書は保持するが、この整備では整数検算suiteを再実行していない。整数接着201頁・meridian18頁・TeXノート65頁は従来の組版記録であり、現行での再組版とは区別する。局所KE原稿の証明、全曲面actual GH適合性の未解決、有限計算、形式証明、組版、GitHubへの保存はそれぞれ別の状態として扱う。実行の入口は `scripts/research_check.py`。
