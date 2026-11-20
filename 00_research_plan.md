# 現行研究方針：一般型曲面のLagrangian torus fibration
更新：2026-11-21 / v2.0（複素次元2専用、曲面主稿改訂8・五次整数接着第25稿）

## 現在の目標と優先順位
滑らかな一般型曲面 \(X_d\subset\mathbb P^3,\ d\ge5\) の指定hyperplane Kähler classでの大域Lagrangian \(T^2\)-fibration、特異fiber、作用適合整数アフィンatlasを研究する。曲面に固有の大域構成とKE退化の局所結果を区別する。最優先は、全neckのactual Moser flowの生存・共通buffer、三重点間の作用・reduced leavesの同時整合、source・branch・coreでの相対接着、全曲面でのGH shortcut障害の処理。次に五次曲面の整数アフィン接着の残る支持型を分類し、公表用の全大域接着の証明と先行研究上の新規性を監査する。

## 原稿・ノートの正本と公表単位
- `papers/surface-lagrangian-torus-fibration.tex`：このrepoの主たる公表用本文。相対SNC構成、次数分割、分岐底、作用適合atlas（分離前の現行改訂8、組版記録130頁）。
- `papers/quintic-integer-gluing.tex`：五次整数アフィン接着、高分母支持グラフの独立論文（第25稿、201頁の記録）。指定SNC cores・K5 graph・標準cones・marked puncturesを保つ候補が対象。必要支持3型26標識は**実現数ではない**。G5_14の中央matching、一般分母剛性、三高Dの同時非負性が未解決。
- `papers/meridian-surgery.tex`：四pantsのmeridian局所置換と閉corner circuitsの障害（18頁の記録）。
- `papers/research-notes.tex`：各種補題・証明素材のTeXノート（65頁の記録）。
- `research/notes.md`：現在有効な数学上の着想、条件、文献比較、障害と再開手順。検証コードは `verification/`。
- 複素次元3のnormal-trivial curves、focus block、相対円板群と大域存在目標は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) の `main` が正本。詳細をこのrepoへ二重掲載しない。関連するKE研究はresearch-hubから参照する。

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

## 優先する次の一手
1. Source-free neck全体のnormal Moser flowの生存と一様bufferを調べ、KE側のresidual rank-one下界、実際のsource/end幾何、共通action periodsの両立を証明する。複数endsのreduced foliationとmonomial/unit変更のorbit partitionへの効果を明示する。
2. 五次整数接着の\(G_{5,14}\)中央matchingと二つの\(\{4,1,0\}\)配分、分母三条件、\(G_{5,16}\)、\(G_{5,17}\)、三高係数の同時非負性・一般分母剛性を調べる。必要な26標識は実現数と読み替えない。
3. 曲面主稿の大域接着全体と先行研究を改めて監査し、曲面の大域fibration・局所KE collapse・条件付きglobal GH比較を区別したまま公表準備を行う。
4. 有効な旧補題・証明書の依存関係は保持し、元資料の未検証部分を無理に削除しない。

## 保存・再現と前回までの検証の範囲
現行のTeX分割節と検証スクリプトは `papers/sections/` を直接参照し、旧ルートsymlinkに依存しない。静的な構成検査は `python3 verification/verify_repository_layout.py`、現行の五主検算・五独立監査は `python3 verification/run_current_checks.py`。旧JSONやmanifestの相対パス・記録時点のSHA-256は出典情報として保持し、パス正規化後の現行実行パスと区別する。
組版はrepo直下の `latexmk papers/surface-lagrangian-torus-fibration.tex`、整数接着は `latexmk papers/quintic-integer-gluing.tex`。LuaLaTeXとLuaTeX-ja／TikZ／日本語フォントが必要、PDFとSyncTeXはbuild/へ出力しGitで追跡しない。現行検証の入口は `python3 verification/run_current_checks.py`。過去の曲面主稿の組版・整数監査記録を、本日の分割時に再実行した証拠と混同しない。元の計算コード、入力、証明書は保存し、必要な範囲で再実行する。形式証明・外部査読・包括的新規性の確認は未実施。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りには承諾なしで通常コミットを `main` へpushし、15–30分ごとに区切って保存する。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。
