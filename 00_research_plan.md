# 現行研究方針：一般型曲面のLagrangian torus fibration
更新：2026-11-21 / v2.4（複素次元2専用、曲面主稿改訂15・五次整数接着第25稿）

## 現在の目標と優先順位
**最優先目標P0：本研究の大域Lagrangian torus fibrationによって、負Kähler–Einstein計量の径の尺度でのGromov–Hausdorff極限を幾何学的に実現する。現時点では未解決である。** 以下の達成条件を満たすまで、Cloud Codexはこの目標に必要な証明・計算・文献確認・原稿整備を自律的に進める。具体的な実行手順は [AGENTS.md](AGENTS.md) と [Cloud Codexの再開手順](research/cloud-codex.md) に置く。

局所KE–Lagrangian bundleと閉cornerのGH比較が得られたため、次の中心問題をそれらの全域的な接着と距離制御に定める。従来の大域fibration構成・特異fiber・作用適合atlasの成果は保持し、そのうちP0に使う接着証明を監査する。五次整数接着の全分類は未完の独立課題として保持するが、P0の補題に必要な部分以外は後順位とする。三次元の存在問題は別repoを正本とする。

### P0の数学的な達成条件

任意の**固定した**次数 \(d\ge5\) に対し、主稿 `deg:family` の明示族、および同じ一般性条件を満たす全平面退化
\[
 X_t=\{\prod_{i=1}^{d}L_i+tF_d=0\}\subset\mathbb P^3
\]
を対象とする。平面は一般位置、\(F_d\) は全三重点で非零、各二重線で相異なる単純零点を持ち、十分小さい非零parameterで \(X_t\) は滑らかとする。\(\operatorname{Ric}(\omega_t)=-\omega_t\)、\([\omega_t]=2\pi(d-4)H\)、\(R_t=\log(-\log|t|^2)\) と固定する。次数・族一様の定数やspecial Lagrangian性を追加要求しない。

許容される一つの標識付き木系 \(T\) を選び、実際の \(\omega_t\) に関して全regular fibersがLagrangian \(T^2\) である連結fiberの大域全射 \(\pi_t:X_t\to B_d(T)\) を構成する。Sourceのpinched torus、branchの \(S^1\times(S^1\vee S^1)\)、core skeletonを含む本研究の相対構成に接続する。特異fiberは各smooth stratumがisotropicという意味で扱う。Markingの位相的な型を保ちながらnodeの位置や必要な構成パラメータは \(t\) とともに選び直せる。あらゆる既存の任意選択に対する収束は要求しない。

`topo:KE-cubical-comparison` の \(p_T:B_d(T)\to\mathcal C_d\) に対し、\(f_t=p_T\circ\pi_t\) が
\[
 \varepsilon_t:=\sup_{x,y\in X_t}
 \left|R_t^{-1}d_{g_t}(x,y)-d_\square(f_t(x),f_t(y))\right|
 \longrightarrow0
\]
を満たすことを証明する。ここで \(d_{g_t}\) は**曲面全体の全経路を許すambient距離**、\(d_\square\) は \(\mathcal C_d\) 全体のunit-square長さ距離である。全射性からGH距離は \(\varepsilon_t/2\) 以下となる。さらに全ての \(f_t\)-fiber、従って正則・特異を含む全 \(\pi_t\)-fiberの正規化ambient直径が一様にゼロとなる。\(d\ge6\) では \(p_T\) が潰す木上の複数の \(\pi_t\)-fibersの合併全体を評価する必要がある。

主稿 `ke:global-realization` が数学的な問題設定の正本。五次 \(d=5\) は \(p_T\) が同相となる最初の完結した節目とし、五次だけの解決を全固定次数 \(d\ge5\) の解決と報告しない。証明を妨げる真の反例が出た場合は、失敗する仮定・範囲と最も近い正しい定式化を証明付きで整理する。

### 完了の判定と、完了に読み替えない結果

P0の完了には、上記のactual fibration・特異領域を含む一様評価・全域距離比較の証明、使用した外部結果の仮定の確認、依存する大域接着証明の監査、主稿への統合が必要。組版・有限計算・GitHub保存はそれぞれ別の確認である。

KE側の \((\mathrm{G})_d+(\mathrm{CP})_d+(\mathrm{PBE})_d\) を満たすことと、既存GH近似 \(\Phi_t\) への \(\sup_xd_\square(\Phi_t(x),f_t(x))\to0\) を証明すれば `topo:ke-map-compatibility` が使える。**未証明の解析仮定を追加したままP0を完了としない。** 必要な入力を証明するか、それらを迂回する十分な直接の全域距離評価を証明する。五次coarse packageで使う \((\mathrm{TC})_5\) も独立な未解決入力である。

全閉cornerだけの内在・protected-ambient GH収束、regular fiberの点ごとの収縮、無制御なMoser移送、人工PL計量の崩壊、抽象的な条件付き比較命題、有限計算の成功はP0の解決ではない。最適な収束速度や独立した整数接着分類の完了はP0の必要条件に加えない。

### 現在の証明課題と着手順

現在はK1を第一着手とし、独立なK3・K4の部分課題とK0の必要箇所を並行できる。依存先が未解決なら具体的な補題へ分け、解ける最高優先の課題を進める。詳細な解析入力・参照commit・定理ラベルは [KE依存関係](research/ke-dependencies.md)、障害と着想は [研究ノート](research/notes.md) が正本。

| 課題 | 最初に行うこと | この課題の達成条件・現在の状態 |
| --- | --- | --- |
| K0：入力の監査 | `main:global`、`ke:global-realization` とKE依存表を読み、採用する族・木系・form・marked collarsを固定する。 | P0に実際に使う大域接着・外部定理の仮定と証明を照合。資料と入力の所在は整備済み、全証明の独立監査は未了。 |
| K1：actual neckの短円とbuffer | `ke:short-circle-image-buffer` とKE側 `neck:lem:rank-one-circle` を接続する。Movingな作用不変領域 \(U_t\supset K_t\) を指定し、period-1生成場の上界 \(\varepsilon_t^{\rm circ}\) とactual境界距離 \(\delta_t\) を別々に評価する。 | \(\delta_t>(2c_w+1/2)\varepsilon_t^{\rm circ}\) と必要な誤差消失を全neckで証明し、sourceとMoser像の双方が同じ \(K_t\) を覆う。固定 source-free compact 基底の moving normal strip で、actual 二側比較・正の境界距離・短円 $O(m_t^{-1})$・共通 source/像を証明。Source 模型では中心を含む短円と、十分遅く縮む領域での共通 Moser 被覆・actual focus–focus germ を証明。固定残余基底では source と通常 pair を一つの actual neck に統合した（`ke:projected-source-neck`）。Source・三重点へ動く残余 collar 全体の buffer および作用整合は未達。 |
| K2：複数endの同時整合 | `ke:staged-neck-averaging`、`ke:staged-reduced-extension`、`ke:relative-neck-matching` を使い、単一primitive・全marked action periods・reduced leaves・critical actions・overlapを合わせる。 | 実際の開collarsで同一fiber partitionを得るか、制御された相対同定を構成。Normal actionの一致だけでは未達。K1の局所結果に続けて進める。 |
| K3：source・branch・coreの相対接着 | `global_gluing.tex` / `neck_models.tex` / `relative_compactification.tex` をactual KE形式と計量の下で監査する。特に \(xy=tz\) のsourceとcoreを覆う領域・接続路を指定する。 | 全域を覆う連結fiberの \(\pi_t\) と、特異fiberおよび木fiber全体の正規化ambient接続費用の消失。既存の定性的構成だけでは未達。K1と独立な局所解析も行う。 |
| K4：全曲面の距離比較 | K1–K3と閉corner評価を用い、全曲面を通る経路の下界とsquare lift・portal connectorによる上界を別々に作る。 | 固定 source-free 基底上では、同じ normal moment のlevel全体を actual長さ $O(1)$ で結び、そのMoser像の正規化ambient径 $O(R_t^{-1})$ を証明した（`ke:fixed-base-moment-connectors`）。Source・moving collar・異なるmomentをまたぐ木への拡張と、\(f_t\) の全点対distortionは未証明。(N),(S),(F)のactual全空間での検証と局所保護領域外のshortcutを含める。 |
| K5：主定理と独立点検 | 五次の完結した証明を節目に、全固定 \(d\ge5\) へ一般化し、全ての入力と定数依存を追う。 | 主稿の問題を仮定未残の定理と十分な証明へ置換し、別の読み手による論理点検、一次文献比較、再現・組版を完了。現在未着手。 |

K1では固定残余基底の moving normal strip を解決した（`ke:fixed-base-neck-moser`）。次に必要なのは、三重点へ動く残余 collar で pair の束表示を保ちながら actual 短円・buffer を確保し、同じ normal action を K2 の開 overlap に持ち込むこと。Source 付近では固定射影座標の距離下界だけでは、$|x|\asymp|t|^{1/2}$ の rescaling gate の法線幅を評価できない。固定残余領域内では canonical moment の moving interval も確保した（`ke:neck-deep-moment-strip`）。

## 原稿・ノートの正本と公表単位
- `papers/surface-lagrangian-torus-fibration.tex`：このrepoの主たる公表用本文。相対SNC構成、次数分割、分岐底、作用適合atlasとKE–fibrationの大域実現問題（現行改訂15。直前の組版確認は改訂14・139頁、2026-11-21）。
- `papers/quintic-integer-gluing.tex`：五次整数アフィン接着、高分母支持グラフの独立論文（第25稿、201頁の記録）。指定SNC cores・K5 graph・標準cones・marked puncturesを保つ候補が対象。必要支持3型26標識は**実現数ではない**。G5_14の中央matching、一般分母剛性、三高Dの同時非負性が未解決。
- `papers/meridian-surgery.tex`：四pantsのmeridian局所置換と閉corner circuitsの障害（18頁の記録）。
- `papers/research-notes.tex`：各種補題・証明素材のTeXノート（65頁の記録）。
- `research/notes.md`：現在有効な数学上の着想、条件、文献比較、障害と再開手順。検証コードは `verification/`。
- 複素次元3のnormal-trivial curves、focus block、相対円板群と大域存在目標は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) の `main` が正本。詳細をこのrepoへ二重掲載しない。関連するKE研究はresearch-hubから参照する。

## 複素次元2：先行研究とsingular fibers
曲面の主定理 main:global は、Mikhalkin (Topology 43, 2004, Theorem 1) の全次元stratified topological torus fibration（Lagrangian性は各maximal cellで選ばれたfiberだけ）、Zhang (J. Math. Study 58, 2025, Theorem 1.1) の一般型と微分同相な四次元多様体のpants分解、Evans–Mauri (Ann. Henri Lebesgue 4, 2021, §3.1) の四次元pantsの局所Lagrangian fibrationとは区別する。Smith (Turkish J. Math. 25, 2001) の制限はhomologically essential toriとtame singularitiesを追加仮定する。Leung–Symington (JSG 8, 2010, **Theorem 2.1**) により、閉almost toric fibrationを持つ四次元多様体の分類に一般型X_dは含まれない。Fernández de Bobadilla–Pełka (CPAM, 2026) の一般SNC退化の部分領域構成から全域のfibrationは自動的には従わない。一次資料と仮定はresearch/notes.mdの「複素次元2」節と主稿Introductionに整理。

全平面構成のsingular fiberは、(1) 分岐辺上の S¹×(S¹∨S¹)（Euler数0）、(2) 面内孤立nodeでの一重pinched T²（Euler数1、focus monodromy）、(3) d個のcore頂点の一般位置d−1直線補空間に対応するlogarithmic Weinstein skeleton（Euler数C(d−3,2)）。正則fiberはLagrangian T²。全平面分割の開分岐辺はC(d,2)(d−4)本（**fiberの個数ではない**）、孤立nodeはd C(d,2)個。五次では(cores, branch edges, nodes)=(5,10,50)、六次では(6,30,90)。通常のalmost toricにない分岐辺とcoreを許すことが本研究の特徴。一般次数の全体構成と、五次・六次に限る大域作用適合atlasは別の主張。先行研究との比較は現行原稿とノートに保持する。全証明の独立検証と包括的新規性の確定は未了である。

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

Actual側の大域入力は `coarse:cor:degree-d-volume-lower`。Adjunction residueでcanonical densityを固定し、backgroundによるHermitian frame errorの吸収と各正のcap方向のminorから六型のdeterminant下界を証明する。Sourceでは元のplane coordinatesを保つexact xy=tzとrescalingにより二つのcap係数≥c_d/Lを使う。Compact minimum原理からactual volume下界を得る。この依存部分の証明と適用条件はKE側の原稿に明示されている。現行整備ではその所在と仮定を確認し、全証明の独立再監査は行っていない。

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

これらは原稿に条件と証明を保持する局所結果である。Averaging–Moserの基本方法はRuan, arXiv:math/0309177v2, §3に先行し、一般的新規性は未確認。H-minimal/special Lagrangian性、大域接着、singular fibersの計量評価は結論しない。

**解析入力の区別：** 関連KE主稿の `coarse:prop:density-counterexample` により、負KE計量であってもbounded volume densityから一様tensor比較は導けない。五次coarse metric packageには独立な $(\mathrm{TC})_5$ が必要であり、その無条件な検証は未完成である。これは対象compact familyの反例ではない。全深部三重点のfull-orbit moving tensor比較は全固定d≥5で検証済みであり、閉cornerへの局所適用に追加仮定は不要である。Source等を含むexterior全体の比較は別の未解決問題である。

## 中心結果と証明の状態
- 曲面側の分岐基底 \(B_d(T)\) とKE候補 \(\mathcal C_d\) は、labelled cell-like homotopy equivalence \(p_T\) で結ばれる。\(d=5\) では同相、\(d\ge6\) では非同相（`papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`）。
- 人工的PL長さ距離\(d_\varepsilon\)によるgraph correspondenceの誤差は、\(d=5\) で \(\Theta(\varepsilon^2)\)、\(d\ge6\) で \(\Theta(\varepsilon)\)。GH収束は上から同じ次数で評価できるが、\(d\ge6\) にGH距離の同次数の下界を主張しない（`topo:metric-collapse-sharp`）。
- 幾何学的な基底計量で同じ収束を得るための十分条件は、(N) global no-shortcut、(S) square geodesic lifts、(F) small-fiber/portal connectors（`topo:finite-portal-criterion`）。二つのsquareを一頂点で貼った反例（`topo:portal-counterexample`）により、(F) は(N)+(S)からは従わない。これらは抽象的距離論であり、actual action metricの構成と検証は未完成。
- 六次同時Petersen分岐木系は6通り・\(S_6\)の一軌道で、各安定化群の位数は120。固定木系はfull \(S_6\)-equivariantではない。新規性は未確認。

## 優先する次の一手
最初に上のK1へ着手し、K0–K5をP0の依存関係に沿って進める。部分的に公表価値のある成果は主稿へ統合し、全問題の解決まで公表準備を一律に遅らせない。五次整数接着の \(G_{5,14}\) 中央matching・\(\{4,1,0\}\) 配分・分母三条件、\(G_{5,16}\)、\(G_{5,17}\)、三高係数の同時非負性と一般分母剛性は、P0に必要な場合以外は保留する。必要な26標識は実現数と読み替えない。有効な証明・証明書・未解決の障害は保持する。

## 保存・再現と現在の検証状態
現行のTeX分割節と検証スクリプトは `papers/sections/` を直接参照し、旧ルートsymlinkに依存しない。静的な構成検査は `python3 verification/verify_repository_layout.py`、現行の五主検算・五独立監査は `python3 verification/run_current_checks.py`。旧JSONやmanifestの相対パス・記録時点のSHA-256は出典情報として保持し、パス正規化後の現行実行パスと区別する。
組版はrepo直下の `latexmk papers/surface-lagrangian-torus-fibration.tex`、整数接着は `latexmk papers/quintic-integer-gluing.tex`。LuaLaTeXとLuaTeX-ja／TikZ／日本語フォントが必要、PDFとSyncTeXはbuild/へ出力しGitで追跡しない。段階別の実行は `scripts/research_check.py` と [Cloud Codexの再開手順](research/cloud-codex.md) を参照する。元の計算コード、入力、証明書は保持する。

2026-11-21 / v2.1の確認：setup/preflight、4主原稿・119検証Python source等の静的構成検査、現行Markdown参照検査、主稿改訂9のLuaLaTeX組版（132頁）と変更箇所の表示確認を実施。引用・参照・PDF/SyncTeX出力を確認し、重複ラベル・欠落字形・overfull警告はない。P0の定式化とKE依存仮定の整合を別担当が点検した。整数検算suite、他三稿の組版、既存の解析・接着全証明の独立再監査は未実施。P0は未解決であり、新しい解析的解決を得たとは主張しない。形式証明・外部査読・包括的新規性確認も未実施。Cloud環境設定・新規タスク起動は今回のrepo整備と別であり、実施していない。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りでは承諾なしで通常コミットを `main` へpushし、Cloud Codexの長時間作業は切りのよいところ、遅くとも前回成功pushから約15分を目安に現行の有効な成果と未解決箇所を保存する（詳細はAGENTS.md）。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。

2026-11-21 / v2.2の確認：主稿改訂10（134頁）を組版し、静的構成検査と追加の命題・系の参照解決を確認。法線方向の積分エネルギー、動径接続上界とMoser速度の規格化を独立に点検した。全neckの実計量buffer、特異領域接着と全域比較は未解決。
