# 現行研究方針：一般型超曲面のLagrangian torus fibration
更新：2026-11-20 / v1.6・現行研究方針 / 主稿改訂6

## 目標と現行資料
曲面の大域的fibration・作用適合atlasと、三次元のclosed-curve local blocksを区別する。曲面側は2026-10-28第25版のソース一式を回収し、旧30頁稿と短いGitHub草稿から現行の三論文へ移行した。三次元側は継続用bundle第10版から局所稿第9版・全体稿第11稿を全文TeXで移行した。

## 三次元大域存在定理の先行研究上の位置
最優先の目標は、滑らかな一般型三次元超曲面 \(X_d\subset\mathbf P^4\), \(d\ge6\), 指定Kähler形式に対して、全正則 \(T^3\) fiberがLagrangianであり、連結な特異fiberとHausdorffな境界のない基底を持ち、全体を覆う大域fibrationを構成すること。最初の定理ではspecial Lagrangian、細いdiscriminant、全特異点の非退化性を必須とせず、適切なrelative local modelsを柔軟に選ぶ。

Mikhalkin（Topology 43 (2004), Theorem 1）は**任意のdegree、dimensionのsmooth hypersurfaceにstratified topological torus fibration**を既に構成した。ただしLagrangianとするのは各maximal cellの選ばれた少なくとも一点のfiberであり、全regular fibersではない。Leung–Wan（JDG 83 (2009), Theorem 3.3）はその選ばれたLagrangian fibersの漸近的special性を一般型hypersurfaceで確立。既知のtopological torus fibrationや一般型のLagrangian toriの存在を本研究の新規性として主張しない。

Evans–Mauri（2021）はSNC/negative vertexの局所模型、Abouzaid–Auroux–Katzarkov（2016）はaffine general type hypersurfacesへのmirror/fibration構成、Fernández de Bobadilla–Pełka（2026, CPAM, DOI 10.1002/cpa.70060）は一般Kähler degenerationのA'Campo/部分領域Lagrangian fibrationを与えるが、いずれも所定のcompact general type X_dの全域大域構成を今回確認した範囲で結論しない。Mak–Matessi–Ruddat–Zharkovによるcompact toric CY hypersurfaceの大域構成は2026年11月の公的講演要旨でも発表されているが、対象はCYである。具体的な定理・書誌・適用範囲は `research/notes.md` と三次元全体稿のIntroduction／`sec:literature` に記す。新規性の網羅的確認とCY構成の全証明との比較は引き続き必要。

## 原稿と主張の状態
- `papers/lagrangian-torus-fibration.tex`：幾何・相対SNC構成・次数分割・大域作用atlas、96頁（回収時）。Smooth X_d⊂P³、d≥5、hyperplane Kähler class aH。分岐底、正則T²、分岐S¹×figure-eight。任意のKähler class、special Lagrangian性、曲面全体のactual KE collapseは主張しない。三重点での局所actual KE collapseは以下の新しい局所定理で扱う。
- `papers/quintic-integer-gluing.tex`：五次整数接着、201頁。指定SNC cores・K5 graph・標準cones・marked puncturesを保つデータが対象。四ray正符号matchingとG5_14両単位枝{4,1,0}等。必要支持3型26標識は実現数ではない。全G5_14の排除、一般分母剛性、三高D同時非負性は未解決。
- `papers/meridian-surgery.tex`：meridian局所置換、18頁。閉corner circuitsへのregular torus bundles追加による四pants置換の障害。Open corridors等へ拡張しない。
- `papers/research-notes.tex`：研究ノート65頁。再利用補題・量化・現行の残余。詳細todoの正本はこちら。
- `papers/threefold-blocks.tex`：原版166頁の局所稿第9版。所定X_d⊂P⁴にdegree d−2、genus (d−3)(d−4)/2のnormal-trivial closed symplectic curveとactual local T³ blockを構成したとする。Normal faces、complement、大域boundary-free fibrationは未構成。
- `papers/threefold-fibration.tex`：原版187頁の全体稿第11稿。

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

## 相対接着で必要なcollar条件
`ke:relative-fiber-preserving` は、torus飽和した開collar N上の元のphase toriが既にactual ω-Lagrangianなら、chain primitive β=Hω、H=K_1+A_1K_2によるMoser flowが各fiberを集合として保ち、p∘φ^−1=p on Nを満たすことを証明する。作用不変性は不要であり、centered chain primitiveでも同じ結論となる。各点を固定することとは異なる。点ごとの固定には、作用不変なcollarとcentered primitiveを用いる既存の `ke:relative-averaging` が使える。

`ke:relative-neck-matching` は、同じorbit partitionを持つactual Lagrangian neck fibrationが開overlap上に与えられれば、基底collarを同定して局所接着できるという条件付きの系である。Actual neckでこの仮定を実現することは未解決。定数係数のmonomial座標変更はorbit partitionを保つが、非定数holomorphic unitを含む変更は一般に保たない。任意の別のprimitiveへの置換でもfiber保存が続くとは仮定しない。

## 小さいLagrangian fibersへの局所的な前進
現在の着手対象は複素次元2でのKE極限とLagrangian fibrationの適合性である。主稿の `papers/sections/paper/ke_fiber_compatibility.tex` に次の証明を置いた。

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
- Focus境界\(\partial K_c\)はunipotent torus mapping torusで、\(\pi_1\)は整数Heisenberg群。\(\partial\mathcal U=C'\times\partial K_c\)のBetti数は \((1,2g+2,4g+3,4g+3,2g+2,1)\)、六次では \((1,8,15,15,8,1)\)。さらに \(\chi(\mathcal V)=-(d^4-5d^3+9d^2-3d-10)\)、六次で \(-512\)。孤立した非零Euler fiberが全て \(-1\)なら512個必要という条件付き結果は保持する。Focus基底のboundary circuitはH₁(∂U)→H₁(U)のkernelの原始生成元であり、H₁(V)=Zへ原始的に写ることをMayer–Vietoris列で証明した（tnc:focus-boundary-primitive）。**未解決なのはhigher homology・基本群の境界包含写像、relative symplectic fillingとglobal Lagrangian接着**。

## 次の一手
1. 三次元では管状disk bundleとactual focus blockの境界を区別し、normal facesとcomplementの接着を優先する。計算済みの\(H_*(K_c)\)と\(H_*(\mathcal V)\)を使って境界包含\(\partial\mathcal U\to\mathcal U,\mathcal V\)の具体的な整数homology・\(\pi_1\)写像、meridional torsionの像を求め、Maslov・作用周期・unipotent monodromy・Euler予算を同時に照合する。
2. 曲面側では `ke:relative-fiber-preserving` を使えるactual neck collarを構成する。まず開overlap上でphase orbit partitionと既存のLagrangian fibersを一致させ、action periodsと定量的bufferを確認する。非定数unitを吸収する座標変更ではorbit partitionを再確認する。全閉cornerの内在・保護領域内のGH比較は証明済みであるが、source・branch・coreへの相対接着、異なるtriple chartsの接合、V_t外を通る大域no-shortcutは未解決。実際の基底長さ距離に対する(N)、(S)、(F)の大域検証はそれぞれ独立に行う。Source nodeのcritical valueには対応pair vertexへ近づく基底パラメータ化が必要であり得る（`ke:source-marking`）。
3. 五次整数接着の\(G_{5,14}\)中央matchingと二\(\{4,1,0\}\)・分母三の位置条件、\(G_{5,16}\)、\(G_{5,17}\)、三高Dの未解決を継続する。
4. 旧曲面v4と現行v25の補題単位の照合を進める。版番号付き分割原稿は、参照する証明書と依存関係を確認するまで削除しない。

## 保存と検証
`research/source-manifest.json`に元ZIP・ソース対応・SHA-256を記載。各証明の断片はpapers/sections/に保持し、証明書が参照する旧版名の証明は必要依存として残す。古いビルドログ・PDF・不要TeXは持ち込まない。旧verification/内の証明書は保存時点の記録であり、今回全てを再実行した記録ではない。

曲面移行時に4本の全文原稿をLuaLaTeXで組版し、v25の五主検算と五独立監査を再実行した。実行入口は `python3 verification/run_current_checks.py`。生成物はbuild/。外部査読・形式証明・全113 scripts再実行とは異なる。

現行のKE比較部分では、全固定次数のglobal density下界、complete simplexのvolume squeeze、固定product balls上のSavin適用、dominant/facet漸近、exact rank-one Schwarz、clipped projectionによる全経路下界を点検した。Lagrangian側では同じMoser flowのC1評価、全閉cornerの内在・protected-ambient GH distortion、端点移動O(R^−2)、chain primitiveによるfiber保存を独立に読み直した。Averagingの符号、hexagonの逆写像、raw-depth誤差・微分評価、および固定simplexとmoving領域の尺度差も確認している。全曲面でのactual GH収束と既存大域fibrationとの一様適合性は未完成。現環境では `lualatex.fmt`・LuaTeX-ja等の基本資産がなく、LuaLaTeX組版の試行は本文処理前に停止した。回収時の組版成功と現行主稿改訂6の未組版を区別する。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りには承諾なしで通常コミットを `main` へpushし、15–30分ごとに区切って保存する。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。
