# 現行研究方針：一般型超曲面のLagrangian torus fibration
更新：2026-11-21 / v1.9・現行研究方針 / 曲面主稿改訂8・三次元局所稿11・全体稿13

## 目標と現行資料
曲面の大域的fibration・作用適合atlasと、三次元のclosed-curve local blocksを区別する。最優先の三次元大域存在問題に向け、actual focus blockを固定するnormal ballへの補完と相対円板群を得た。次には新たなelliptic faceの近傍変更と管状補集合V₀への接続を構成する。曲面側ではKE計量に適合する局所fibrationとneck接着を並行して進める。証明全文は以下の現行TeX原稿に置き、移行元との対応はresearch/migration.mdとsource-manifest.jsonを参照する。

## 三次元大域存在定理の先行研究上の位置
最優先の目標は、滑らかな一般型三次元超曲面 \(X_d\subset\mathbf P^4\), \(d\ge6\), 指定Kähler形式に対して、全正則 \(T^3\) fiberがLagrangianであり、連結な特異fiberとHausdorffな境界のない基底を持ち、全体を覆う大域fibrationを構成すること。最初の定理ではspecial Lagrangian、細いdiscriminant、全特異点の非退化性を必須とせず、適切なrelative local modelsを柔軟に選ぶ。

Mikhalkin（Topology 43 (2004), Theorem 1）は**任意のdegree、dimensionのsmooth hypersurfaceにstratified topological torus fibration**を既に構成した。ただしLagrangianとするのは各maximal cellの選ばれた少なくとも一点のfiberであり、全regular fibersではない。Leung–Wan（JDG 83 (2009), Theorem 3.3）はその選ばれたLagrangian fibersの漸近的special性を一般型hypersurfaceで確立。既知のtopological torus fibrationや一般型のLagrangian toriの存在を本研究の新規性として主張しない。

Evans–Mauri（2021）はSNC/negative vertexの局所模型、Abouzaid–Auroux–Katzarkov（2016）はaffine general type hypersurfacesへのmirror/fibration構成、Fernández de Bobadilla–Pełka（2026, CPAM, DOI 10.1002/cpa.70060）は一般Kähler degenerationのA'Campo/部分領域Lagrangian fibrationを与えるが、いずれも所定のcompact general type X_dの全域大域構成を今回確認した範囲で結論しない。Mak–Matessi–Ruddat–Zharkovによるcompact toric CY hypersurfaceの大域構成は2026年11月の公的講演要旨でも発表されているが、対象はCYである。具体的な定理・書誌・適用範囲は `research/notes.md` と三次元全体稿のIntroduction／`sec:literature` に記す。新規性の網羅的確認とCY構成の全証明との比較は引き続き必要。

## 原稿と主張の状態
- `papers/lagrangian-torus-fibration.tex`：幾何・相対SNC構成・次数分割・大域作用atlas、130頁（現行組版）。Smooth X_d⊂P³、d≥5、hyperplane Kähler class aH。分岐底、正則T²、分岐S¹×figure-eight。任意のKähler class、special Lagrangian性、曲面全体のactual KE collapseは主張しない。三重点での局所actual KE collapseは以下の新しい局所定理で扱う。
- `papers/quintic-integer-gluing.tex`：五次整数接着、201頁。指定SNC cores・K5 graph・標準cones・marked puncturesを保つデータが対象。四ray正符号matchingとG5_14両単位枝{4,1,0}等。必要支持3型26標識は実現数ではない。全G5_14の排除、一般分母剛性、三高D同時非負性は未解決。
- `papers/meridian-surgery.tex`：meridian局所置換、18頁。閉corner circuitsへのregular torus bundles追加による四pants置換の障害。Open corridors等へ拡張しない。
- `papers/research-notes.tex`：研究ノート65頁。再利用補題・量化・現行の残余。詳細todoの正本はこちら。
- `papers/threefold-blocks.tex`：現行局所稿第11版。所定X_d⊂P⁴にdegree d−2、genus (d−3)(d−4)/2のnormal-trivial closed symplectic curveとactual local T³ blockを構成する。Normal exterior Eのfibrationは、inner blockを固定しouter collarをtoricにする形で構成済み。新たなelliptic base boundary、V₀への延長と大域接着は未解決。相対smooth handlesと円板群も決定した。
- `papers/threefold-fibration.tex`：現行全体稿第13稿。

## 三次元actual focus補集合の境界・第二ホモトピー・巡回被覆

正本は `papers/sections/threefold/local_blocks/focus_exterior_topology.tex`。構成済みの具体的な積埋込 U=C'×K_c⊂N=C'×D⁴⊂X_d を使う。K_cと同じ抽象的homotopy型を持つ任意の埋込へは拡張しない。e=d−2、g=(d−3)(d−4)/2、V=cl(X_d∖U)、V₀=cl(X_d∖N) とする。

- `tnc:focus-exterior-hopf` / `tnc:focus-exterior-homotopy`：反対位相S¹の商 h=(π(|X|²−|Y|²),XY) で、normal exterior E=D⁴∖int K_c を、原点を含むunknotted solid torusの三次元補集合上のHopf circle bundleとして記述する。E≃S¹∨S²∨S³で、outer S³の包含も同定する。
- `tnc:actual-complement-pi1`：V₀の単連結性とvan Kampenからπ₁(V)=Z。境界π₁(C')×Heisenberg群から、曲線loopsとnormal fiberの二つのloops a,bはVで消え、focus基底境界のsection lift tが生成元となる。UとVへの同時写像のkernelはcentral vanishing-cycle subgroup〈a〉。
- `tnc:all-boundary-homology-maps`：両側への全整数homology写像をmarked basisで決定。Regular torus FはU側に残りVで消える。aをt沿いにtransportしたtorus TはUで消えV側に残る。H₂(∂U)→H₂(V)のcokernelはZ/e、normal face [∂K_c]はH₃(V)の位数eのtorsionを生成し、H₃(V)/im boundary≅H₃(X_d)、H₄ boundary→Vは全射。
- `tnc:equivariant-pi2`：Λ=Z[τ,τ⁻¹]をπ₁(V)の群環とすると、π₂(V)≅Λ^(2g+1)⊕Λ/(e(τ−1))。分解は一般に非標準的だがmoduleの同型型を決定した。整数torsion部分はΛ/eΛ。Universal coverのMayer–Vietoris列で、曲線のdegreeから関係e(τ−1)h=0が生じる。
- `tnc:cyclic-cover-h2`：任意のm≥1の連結巡回被覆V_mはH₂(V_m;Z)≅Z^{m(2g+1)+1}⊕(Z/e)^{m−1}。六次ではπ₂(V)=Λ⁷⊕Λ/(4(τ−1))、二重被覆のH₂=Z¹⁵⊕Z/4。

証明を独立に相互点検し、一般の被覆公式は明示的な整数基底変換でも証明した。`python3 verification/verify_focus_exterior_topology.py --json` はd=6,…,20、m=1,…,12の境界行列・巡回被覆関係・群環coinvariantsを整数演算で照合する。有限検算と一般証明は別であり、形式証明ではない。Auroux §5.1、Akbulut arXiv:1103.3137v2のIntroduction/Figure 1、Hatcher Theorems 4.32/4.41・Example 4.45を一次資料で照合した。標準nodal/fishtail模型やHopf理論自体の新規性は主張せず、今回の具体的な組合せの包括的新規性は未確認。

## 三次元：normal ballへの相対補完と円板の接着条件

正本は `papers/sections/threefold/local_blocks/focus_relative_filling.tex`（局所稿第37節、全体稿の同名節）。標準symplectic normal ballで次を証明した。

- `ncc:normal-ball-completion` / `ncc:product-completion`：逆位相circleの商座標A=π(|X|²−|Y|²), w=XYに対し、平面diffeomorphism ψ_Aを内側でw−c、outer sphere近傍でidentityとする。H=|ψ_A(w)|²によりĜ=(A,H)を構成し、K_cの開近傍で元のG_cと一致、Ĝ⁻¹(R)=K_c、outer collarで標準toric、全fiber連結を証明する。Curve quotientとの積はregular Lagrangian T³を持ち、既存のfocus–hyperbolic fibersを保持する。
- `ncc:elliptic-face-limitation`：新しいH=0のfiberはregular curve level上でT²、base germは半空間になる。Compact X_dからHausdorff baseへの大域quotientがこのwhole fiberと近傍の葉層を保つなら、そのgermは外側からの接着だけでは消えない。**Boundary-free目標にはelliptic近傍自体の変更が必要。**
- `tnc:normal-round-handle` / `tnc:relative-pushout`：Eはouter S³から一つのround 1-handleで得られる。逆向きの唯一の2-handleはa^k b^±1を殺し、whiskerでbに正規化できる。V≃V₀∪_i(C'×(S¹∨S²))をV₀の下で同定し、iは[C']=e hを表す。CofiberはS¹∨(∨^{2g+1}S²)∨(∨^{2g+1}S³)∨S⁴。V自体がV₀とのwedgeだという意味ではない。
- `tnc:product-relative-handles` / `tnc:no-weinstein-normal-transition`：C'×Eのouter側からのminimal smooth handle数はindex1,2,3,4で(1,2g+1,2g+1,1)。相対H₄=Z、逆向きでは相対H₅=Zなので、二つの全境界成分を保つWeinstein cobordismはどちら向きにも存在しない。Nonexactな構成や切り分けた境界を否定しない。曲線をpunctureするとこのH₄は消えるが側面∂C°×Eの接着が生じる（`tnc:punctured-relative-handles`）。
- `tnc:normal-relative-disk-module`：適切なreverse 2-handle core class Bについてπ₂(E,Y)=ΛB、∂(fB)=f(1)b+f′(1)a。π₂(E)の像は(τ−1)²ΛBであり、一階差分はa-disk、二階差分はsphere class。任意のb-capをΛ-basisとする主張ではない。
- `tnc:relative-disk-central-extension`：M=π₂(V)に対してπ₂(V,∂U)はMによるπ₁(C')×Z²のcentral extensionで、curve disk liftsは∏[A_i,B_i]=e hを満たす。e h≠0なので非分裂。Degree quotientはEuler数eのcircle bundle P_eのπ₁とZ²の積。Normal pairの全作用は決定したが、全三次元pairでの各curve diskへのt作用とsmooth framingは未決定。
- `ncc:normal-maslov-marking`：normal regular torusのμ(a)=0, μ(b)=2。境界でcleanに交わるnormal C²内のLagrangian diskがma+nbを埋めるならn=0, mA=0。従ってb+kaはこの方法では埋まらない。Elliptic collapseのtransverse symplectic diskやcurve方向にも動くdiskは対象外。

Symingtonのnodal trade、Brownのrelative crossed moduleとHatcherのrelative Hurewicz、Cieliebak–EliashbergのWeinstein index制限を一次資料と照合した。Asimovのround handleの出典は公式書誌を確認し、用いる分解は直接証明した。既知の方法そのものの新規性は主張せず、本研究の具体的相対データの包括的新規性は未確認。全三次元の大域fibrationは未完成である。

## 複素次元2：先行研究とsingular fibers
曲面の主定理 main:global は、Mikhalkin (Topology 43, 2004, Theorem 1) の全次元stratified topological torus fibration（Lagrangian性は各maximal cellで選ばれたfiberだけ）、Zhang (J. Math. Study 58, 2025, Theorem 1.1) の一般型と微分同相な四次元多様体のpants分解、Evans–Mauri (Ann. Henri Lebesgue 4, 2021, §3.1) の四次元pantsの局所Lagrangian fibrationとは区別する。Smith (Turkish J. Math. 25, 2001) の制限はhomologically essential toriとtame singularitiesを追加仮定する。Leung–Symington (JSG 8, 2010, **Theorem 2.1**) により、閉almost toric fibrationを持つ四次元多様体の分類に一般型X_dは含まれない。Fernández de Bobadilla–Pełka (CPAM, 2026) の一般SNC退化の部分領域構成から全域のfibrationは自動的には従わない。一次資料と仮定はresearch/notes.mdの「複素次元2」節と主稿Introductionに整理。

全平面構成のsingular fiberは、(1) 分岐辺上の S¹×(S¹∨S¹)（Euler数0）、(2) 面内孤立nodeでの一重pinched T²（Euler数1、focus monodromy）、(3) d個のcore頂点の一般位置d−1直線補空間に対応するlogarithmic Weinstein skeleton（Euler数C(d−3,2)）。正則fiberはLagrangian T²。全平面分割の開分岐辺はC(d,2)(d−4)本（**fiberの個数ではない**）、孤立nodeはd C(d,2)個。五次では(cores, branch edges, nodes)=(5,10,50)、六次では(6,30,90)。通常のalmost toricにない分岐辺とcoreを許すことが本研究の特徴。一般次数の全体構成と、五次・六次に限る大域作用適合atlasは別の主張。今回の作業は現行原稿の主張の一次文献・範囲との照合であり、全証明の独立検証完了でも包括的新規性確定でもない。

## KEのGH極限との関係
標準負KE尺度では成分内部の四次元完備KE幾何が残る。径の尺度 $R_t=\log(-\log|t|^2)$ では、関連KE研究の $(\mathrm{CP})_d+(\mathrm{PBE})_d$ の下で候補 $\mathcal C_d$ へのGH収束を扱う。我々のfibrationによる実現には、さらに選んだ $\pi_t:X_t\to B_d(T)$ とKE近似写像 $\Phi_t$ が $\sup_x d_\square(\Phi_t(x),p_T\pi_t(x))\to0$ を満たす必要がある。主稿 `topo:ke-map-compatibility` はこの適合性から全fiberのambient直径収縮を導く初等的な比較命題であり、actual KEの収束を証明したものではない。五次は $p_T$ が同相、六次以上は基底内の木も収縮する。Zhang (MRL, 2015)の局所collapse定理のQ-factorial・相対ample仮定は、source germ $xy=tz$ を持つ我々の族へそのまま適用できない。文献と適用計算は `research/notes.md`、公表用の比較は主稿 `intro:ke-collapse` を参照。

## 全深部三重点の actual 比較と閉cornerのGH極限
任意の固定次数 d≥5 の一般位置全平面退化で、三重点の全深度比・全角度に一様な actual KE 比較を証明した。正確な座標 ζ0ζ1ζ2=t、ell_i=−log|ζ_i|²、L=−log|t|²、R=log L とし、k_Lをlogarithmic simplex上のcomplete toric KE form、その実計量をg_L^sfとする。十分大きい固定m1と各qのCqについて、m≥m1、min ell_i≥mで
\[
\left|\log\frac{\omega_t^2}{k_L^2}\right|\le C/m,\qquad
\|g_t-g_L^{sf}\|_{C^q}\le C_q/m.
\]
定数は固定dと族に依存してよい。次数一様性は主張しない。証明の正本はKE主稿 `coarse:thm:full-triple-tensor`。

固定toric模型の存在・完備性にはZhang (2015), §2.1, Theorem 2.1 / Proposition 2.2を用いる（退化族のTheorem 2.4とQ-factorial仮定は使わない）。ψ_L=log L−Σlog ell_iに対してψ_L−(log3)/2≤φ_L≤ψ_L、V_L/3≤k_L²≤V_Lを内外にずらした障壁で証明する。Complete模型から三つの半平面へのYau Schwarz lemma、determinant比較、内部正則性により一様cusp geometryを得る。凸性からfacet shiftのlog-density差をO(1/min ell)とし、actual計量を内外のsimplex KE metricsでvolume比較する。Savinの小摂動定理でtensor・全高階誤差へ移る。Actual metric bufferや(TC)/(PBE)を前提としない。

Actual側の大域入力は `coarse:cor:degree-d-volume-lower`。Adjunction residueでcanonical densityを固定し、backgroundによるHermitian frame errorの吸収と各正のcap方向のminorから六型のdeterminant下界を証明する。Sourceでは元のplane coordinatesを保つexact xy=tzとrescalingにより二つのcap係数≥c_d/Lを使う。Compact minimum原理からactual volume下界を得る。今回この依存部分も再点検して明示化した。

Lagrangian主稿 `ke:actual-closed-corner` の同じ averaging–Moser flow と同じactual Lagrangian torus bundleに対し、`ke:closed-corner-gh` と `ke:closed-corner-protected-gh` が全閉cornerのGH極限を与える。m=Rでsoftmax hexagonのMoser像をW_{t,J}、その射影をπ_{t,J}とすると、R^−2 g_tによる距離について
\[
\sup_{x,y\in W_{t,J}}
\left|d_t(x,y)-d_J(\pi_{t,J}(x),\pi_{t,J}(y))\right|
\le C\frac{\log R}{R}.
\]
これはW_{t,J}自身の内在距離と、外側保護領域V_t={min ell_i>R/2}内の全経路を許す距離の双方で成立する。標的のd_Jは三枚のunit squaresからなるC_J自身の内在距離であり、full C_dの距離を制限したものではない。全fiberのintrinsic/ambient diameterはO(1/R)、正規化後はO(1/R²)、raw cubical mapとの誤差はO(log R/R)。Squareの継目も同一のregular T²であり、既存大域fibrationのsource・branch・coreのsingular fibersとは同定しない。

距離の解析入力はKE主稿 `simplex:lem:rank-one-schwarz` の係数1評価と `simplex:prop:dominant-product` のsharp product比較。Clipped logarithmic projectionで模型simplex全体の経路の下界を示し、三枚以内のsquare galleryを内部へ移して上界を得る（`simplex:thm:closed-corner-model`）。ActualとのO(1/R)比較と同じMoser flowのC1評価で上記の結論へ移す。正本は `papers/sections/paper/ke_closed_corner_gh.tex`。全曲面でのshortcut、異なるtriple chartの接合、actual neckおよびsingular fibersとの相対接着は未解決。新規性の網羅的確認と外部査読・形式証明は未実施。

## 開正方形上のactual KE–Lagrangian collapse
主稿の `papers/sections/paper/ke_open_cell_collapse.tex` に、任意の固定次数d≥5のactual KE計量に対する局所結果を置く。関連KE主稿 `simplex:cor:actual-dominant-product` は、三重点独立深度 a,b∈[L^η/2,2L^(1−η)]、0<η<1/2 上のproduct-cusp比較を全固定階でO(L^−η)と与える。Complete simplex模型の誤差O(((a+b)/L)²)とactual/model誤差O(1/min ell)を合わせた率であり、global capped volume下界、明示的な上下KE barriers、Savin (2007), Theorem 1.3に依存する。(TC)_dや(PBE)_dを追加仮定しない。

`ke:open-cell-moser-c1` は平均化のprimitiveとMoser場のC1 normをO(L^−η)とし、flowのpullback metricを制御する。`ke:open-cell-collapse` はKη=[η,1−η]²上のactual KE–Lagrangian T² fibrationを構成し、fiberのintrinsic/ambient diameter O(L^−η)、raw mapとの誤差O(1/R)を与える。Moser像領域に内在長さ距離を入れると、R^−2 g_tは平坦KηへGH収束し、projection distortionはO(L^−η+L^−η/R)=O(L^−η)。定数は固定ηに依存する。これらの証明と一次資料の適用条件を点検した。一般的新規性は未確認。

固定ηの開正方形と全閉cornerは、それぞれ上記の局所定理で扱う。全曲面のambient shortcut、source・branch・coreのsingular fibersとの接着、既存の大域fibrationとの同定は残る。

## 共通normal circleに適合する二段階平均

主稿 `papers/sections/paper/ke_staged_neck_averaging.tex` が正本。自由な正則normal S¹を先に平均してη=A1ωとし、triple endで残る円を平均してκ=A2ηとする。単一primitive ω=dλとflow/domain bufferの下で、φ*ω=η、ψ*η=κ、Θ=φψについてΘ*λ=A2A1λ+dqとなる。第二flowはnormal circleと可換であるから、各actual torusはneckと同じactual action φρ1φ^−1を含む。μ∘ψ=A2μが厳密に成り立ち、全marked整数cycleのaction periodsを同じλから規格化できる（`ke:staged-neck-averaging`）。

`ke:short-circle-actual-buffer` は、作用不変領域全体でperiod-1 normal generatorがactual計量に関して|V|≤εを満たせば、Moser trajectoryのactual長をc_w ε以下に抑える。c_w=(π/2)||w||₂で、通常kernelならπ/(2√3)、centered kernelならπ/(4√3)。作用不変背景・tensor二側比較・exactnessはこの評価に不要で、forward/backward両flowに成立する。さらにcompact飽和集合Kのactual bufferが(2c_w+1/2)εを超えれば、飽和source OとそのMoser像の両方がKを含む（`ke:short-circle-image-buffer`）。単一primitiveがあれば同じKの近傍にactual Hamiltonian normal actionを得る。全neckの一様な短さ・buffer、C¹とintrinsic fiber径は引き続き別の入力である。

一段階構成、二段階構成、固定整数基底の変更は、共通domain/image bufferの下でHamiltonian isotopyにより比較できる（`ke:staged-hamiltonian-comparison`）。形式のpositive triangle上のpath homotopyとexact primitive transportを明示している。Exact endpoint mapであることだけからHamiltonian性を結論しない。旧bundleと同じfiber partitionとは主張しない。

`ke:staged-closed-corner-gh` は、三重点の標準T²の任意の固定primitive subgroupを第一段に選び、actual closed-corner bundleと同じO(log R/R)の内在・protected-ambient GH評価を与える。Fiberの元の尺度のintrinsic径はO(1/R)。三重点内の定量的bufferは既存のfull-triple比較で検証済みである。

関連KE主稿 `pair:prop:bundle-conic` / `pair:cor:global-primitive` / `pair:cor:actual-common-moment` により、source-freeな固定compact base上では一つの正則normal action、canonical primitive、円平均η_tの共通moment intervalが得られた。Fixed-end momentはperiod1の規約で±4π/(−log r²)を主項とし、r固定後t→0とする。これらからneck全体のnormal Moser flowの生存・bufferや各triple endとの同時一致は従わない。

`ke:staged-reduced-extension` は、marked simple-saddle foliationと適合するreduced end germsの延長を仮定して、regular T²とsaddle S¹×figure-eightを持つneckを接着する。共通normal actionだけでは、別に固定したneckの第二periodやfiberそのものの一致を意味しない。Reduced leaves、内部marking、critical actionの条件も確認する。Sourceと既存の大域fibrationへの接着、全曲面のGH収束は未解決である。

## 相対接着で必要なcollar条件
`ke:relative-fiber-preserving` は、torus飽和した開collar N上の元のphase toriが既にactual ω-Lagrangianなら、chain primitive β=Hω、H=K_1+A_1K_2によるMoser flowが各fiberを集合として保ち、p∘φ^−1=p on Nを満たすことを証明する。作用不変性は不要であり、centered chain primitiveでも同じ結論となる。各点を固定することとは異なる。点ごとの固定には、作用不変なcollarとcentered primitiveを用いる既存の `ke:relative-averaging` が使える。

`ke:relative-neck-matching` は、同じorbit partitionを持つactual Lagrangian neck fibrationが開overlap上に与えられれば、基底collarを同定して局所接着できるという条件付きの系である。Actual neckでこの仮定を実現することは未解決。定数係数のmonomial座標変更はorbit partitionを保つが、非定数holomorphic unitを含む変更は一般に保たない。任意の別のprimitiveへの置換でもfiber保存が続くとは仮定しない。

## 小さいLagrangian fibersへの局所的な前進
曲面側の着手対象は複素次元2でのKE極限とLagrangian fibrationの適合性である。主稿の `papers/sections/paper/ke_fiber_compatibility.tex` に次の証明を置いた。

- `ke:short-torus-averaging`：自由な正則 $T^2$ 作用、torus不変Hermitian計量 $h$、$c h\le g_\omega\le C h$、torus上のperiod零を仮定する。作用の周期1生成場の長さの和を $e$ とすると、平均化のchain homotopyから長さ $O(e)$ のprimitiveを作り、一つのMoser flowで領域全体にLagrangian fibrationを構成する。変位は $Ce/(2c)$ 以下、ambient fiber diameterは $\sqrt C e(C/c+1/2)$ 以下。高階微分比較は使わない。
- `ke:triple-hexagon`：$\zeta_i\zeta_j\zeta_k=t$ の三つのsquareを一つのhexagonとして全phase torusで実現し、raw-depth mapとの誤差を $O((1+\log m_t)/R_t)$ に抑える。
- `ke:triple-moving-fibration`：全phaseを含む moving domain $\min\ell_a>m_t/2$ 上の一様tensor比較を追加仮定すれば、actual負KE形式に対する局所fibrationが得られ、そのambient fiber diameterは元の尺度でも $O(m_t^{-1})$。$m_t=R_t\to\infty$ とできる。負KE equationにより局所canonical trivialization上で形式がexactとなるのでperiod条件は満たされる。

これらは条件と証明を今回点検した局所結果である。Averaging–Moserの基本方法はRuan, arXiv:math/0309177v2, §3に先行し、一般的新規性は未確認。H-minimal/special Lagrangian性、大域接着、singular fibersの計量評価は結論しない。

**解析入力の区別：** 関連KE主稿の `coarse:prop:density-counterexample` により、負KE計量であってもbounded volume densityから一様tensor比較は導けない。五次coarse metric packageには独立な $(\mathrm{TC})_5$ が必要であり、その無条件な検証は未完成である。これは対象compact familyの反例ではない。全深部三重点のfull-orbit moving tensor比較は全固定d≥5で検証済みであり、閉cornerへの局所適用に追加仮定は不要である。Source等を含むexterior全体の比較は別の未解決問題である。

## 中心結果と証明の状態
- 曲面側の分岐基底 \(B_d(T)\) とKE候補 \(\mathcal C_d\) は、labelled cell-like homotopy equivalence \(p_T\) で結ばれる。\(d=5\) では同相、\(d\ge6\) では非同相（`papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`）。
- 人工的PL長さ距離\(d_\varepsilon\)によるgraph correspondenceの誤差は、\(d=5\) で \(\Theta(\varepsilon^2)\)、\(d\ge6\) で \(\Theta(\varepsilon)\)。GH収束は上から同じ次数で評価できるが、\(d\ge6\) にGH距離の同次数の下界を主張しない（`topo:metric-collapse-sharp`）。
- 幾何学的な基底計量で同じ収束を得るための十分条件は、(N) global no-shortcut、(S) square geodesic lifts、(F) small-fiber/portal connectors（`topo:finite-portal-criterion`）。二つのsquareを一頂点で貼った反例（`topo:portal-counterexample`）により、(F) は(N)+(S)からは従わない。これらは抽象的距離論であり、actual action metricの構成と検証は未完成。
- 六次同時Petersen分岐木系は6通り・\(S_6\)の一軌道で、各安定化群の位数は120。固定木系はfull \(S_6\)-equivariantではない。新規性は未確認。
- 三次元のnormal-trivial closed symplectic curveは\(2g-2=(d-5)e\)を満たす。**小さい管状補集合**\(V_0=X_d\setminus\operatorname{int}N(C')\)について、Lefschetz–Thom長完全列から\(H_3(V_0;\mathbb Z)=\mathbb Z^{b_d}\oplus\mathbb Z/(d-2)\)、\(H_4(V_0;\mathbb Z)=\mathbb Z^{2g}\)を証明した（tnc:tubular-homology）。六次では\(\mathbb Z^{520}\oplus\mathbb Z/4\)。これは実際のfocus blockの補集合の群と同一視しない。
- Actual normal factorは \(K_c\simeq S^1\vee S^2\) と計算できた（tnc:focus-homotopy）。実際のfocus block \(\mathcal U=C'\times K_c\) の補集合 \(\mathcal V\) についても相対Poincaré–Lefschetz列から整数homologyを完全に計算した：\(H_1(\mathcal V)=\mathbb Z\)、\(H_2(\mathcal V)=\mathbb Z^{2g+2}\)、\(H_3(\mathcal V)=\mathbb Z^{b_d+2g+1}\oplus\mathbb Z/(d-2)\)、\(H_4(\mathcal V)=\mathbb Z^{2g+1}\)。六次では \(H_3(\mathcal V)=\mathbb Z^{527}\oplus\mathbb Z/4\)（tnc:actual-complement-homology）。管状補集合との自由rankの差を区別する。
- Focus境界\(\partial K_c\)はunipotent torus mapping torusで、\(\pi_1\)は整数Heisenberg群。\(\partial\mathcal U=C'\times\partial K_c\)のBetti数は \((1,2g+2,4g+3,4g+3,2g+2,1)\)、六次では \((1,8,15,15,8,1)\)。さらに \(\chi(\mathcal V)=-(d^4-5d^3+9d^2-3d-10)\)、六次で \(-512\)。孤立した非零Euler fiberが全て \(-1\)なら512個必要という条件付き結果は保持する。Focus基底のboundary circuitはH₁(∂U)→H₁(U)のkernelの原始生成元であり、H₁(V)=Zへ原始的に写ることをMayer–Vietoris列で証明した（tnc:focus-boundary-primitive）。境界包含の全整数homology・基本群写像は上記の新節で決定した。**Normal ball内のrelative補完は上記で構成済み。残るのはelliptic faceの変更、V₀への延長とglobal Lagrangian接着**。

## 次の一手
1. 三次元では、構成したtoric outer collarに適合するV₀側のfibrationと、内部elliptic faceを変更する領域を作る。最初にC′を境界付き曲面へ切ったC°×Eを調べ、側面∂C°×Eのwhole fibers・primitive periods・coorientationを明示する。閉曲線全体のWeinstein移行とb+kaをclean normal Lagrangian diskで埋める方式は上記の障害により使えない。相対円板の(τ−1)²関係とcurve relation e hを接着の必要条件として保持し、V₀側でcircle generatorが変わる領域を探す。Puncture後のhomology消滅を存在定理とは扱わない。
2. 曲面側の継続では、source-free neck全体のnormal Moser flowの生存と一様bufferを最優先にする。固定base上のprimitiveと共通moment intervalは得たため、KE側 `neck:lem:rank-one-circle` のresidual rank-one下界とactual bufferを調べる。三重点の指定subgroupと射影的neck actionのoverlapを比較し、複数endsのnormal action・reduced foliation・primitive markingsを同時に合わせる。`ke:staged-neck-averaging` と `ke:staged-reduced-extension` はその条件下で接着を与える。非定数unitによるfull orbit partitionの変化は整数基底変更と別に扱う。Source・branch・coreの接着、全X_tでの(N),(S),(F)とglobal no-shortcutは未解決。
3. 五次整数接着の\(G_{5,14}\)中央matchingと二\(\{4,1,0\}\)・分母三の位置条件、\(G_{5,16}\)、\(G_{5,17}\)、三高Dの未解決を継続する。
4. 旧曲面v4と現行v25の補題単位の照合を進める。版番号付き分割原稿は、参照する証明書と依存関係を確認するまで削除しない。

## 保存と検証
`research/source-manifest.json`に元ZIP・ソース対応・SHA-256を記載。各証明の断片はpapers/sections/に保持し、証明書が参照する旧版名の証明は必要依存として残す。古いビルドログ・PDF・不要TeXは持ち込まない。旧verification/内の証明書は保存時点の記録であり、今回全てを再実行した記録ではない。

曲面移行時に4本の全文原稿をLuaLaTeXで組版し、v25の五主検算と五独立監査を再実行した。実行入口は `python3 verification/run_current_checks.py`。生成物はbuild/。外部査読・形式証明・全113 scripts再実行とは異なる。

今回の独立点検対象は、normal ballへの相対補完とelliptic base germ、smooth round handleとrelative pushout、relative disk crossed moduleとcentral extension、Weinsteinおよびclean normal diskの障害である。主張の証明は新節にあり、相互点検済み。既存の境界写像・equivariant π₂・有限被覆・short-circle averagingの証明と点検記録は保持するが、大域構成全体を今回再監査したわけではない。外部査読・形式証明・包括的新規性の確認は未実施。

`python3 verification/verify_focus_relative_models.py --json` は243 Laurent多項式の境界と整数除法、1,701 deck作用、d=6,…,20の15 closed-curveおよび60 punctured-curveの相対Künneth計算を整数演算で検算した。一般の位相・幾何の結論は原稿の証明による。既存 `verify_focus_exterior_topology.py` の境界・巡回被覆検算記録は維持し、既存suite全体は今回再実行していない。

2026-11-21に三次元局所稿190頁・全体稿211頁をLuaLaTeXとlatexmkで組版し、未解決の参照・引用がないことを確認した。新節の代表頁と図はPDFを画像化して表示を点検した。曲面主稿改訂8の130頁という組版記録は保持するが今回は未変更・未再組版である。実行にはLuaLaTeX format・LuaTeX-ja・日本語font・TikZを含むTeX環境が必要であり、latexmkによりPDFとSyncTeXをbuild/へ出力する。既存節の2.27ptのOverfull警告一件は残るが、新節にはない。数学検証・組版・GitHub反映は別々の状態として扱う。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りには承諾なしで通常コミットを `main` へpushし、15–30分ごとに区切って保存する。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。
