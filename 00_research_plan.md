# 現行研究方針：一般型曲面のLagrangian torus fibration
更新：2026-11-21 / v3.4（複素次元2専用、曲面主稿改訂24・五次整数接着第25稿）

## 現在の成果と優先順位

**P0の全域GH実現には、現在の原稿に証明がある。** 任意の固定次数 \(d\ge5\) と下記の一般性条件を満たす全平面退化について、actual負KE形式の大域Lagrangian torus fibrationと、同じ写像 \(f_t=p_T\pi_t\) の全曲面ambient距離に関する一様distortionの消失を構成した。主定理は `ke:global-realization`、統合証明は `ke:global-metric-realization`。今回の新証明と局所・全域の接続を複数担当で内部点検したが、形式証明、全主稿・全外部入力の包括的再監査、外部査読、新規性の網羅的確認は行っていない。

現在の優先課題は、公表に向けた一次文献と依存結果の包括的再点検、新規性の確認、主稿の構成整理である。Sourceの全moment退出は三境界Schwarzと直接経路により $O(1)$ に改善した。Componentの接続費用は $C(1+\log(N_j+1))$。残余基底の定数を先に固定し、それを吸収するcut $N_j$ を選ぶことで、全fiber合併とportalの予算も $H_{j,t}=C(1+\log(N_j+1))$ とできる。これは残余定数の増大率や最適収束速度を評価した結果ではない。SourceのGaussian評価は独立な補助結果として保持する。従来の大域fibration構成・特異fiber・作用適合atlasの有効な成果は保持する。五次整数接着の全分類は未完の独立課題であり、公表準備と必要な検証を優先しながら維持する。三次元の存在問題は別repoを正本とする。自律的な研究・保存の手順は [AGENTS.md](AGENTS.md) と [Cloud Codexの再開手順](research/cloud-codex.md) に置く。

### P0で得た定理の範囲

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
を満たすことを証明した。ここで \(d_{g_t}\) は**曲面全体の全経路を許すambient距離**、\(d_\square\) は \(\mathcal C_d\) 全体のunit-square長さ距離である。全射性からGH距離は \(\varepsilon_t/2\) 以下となる。全ての \(f_t\)-fiber、従って正則・特異を含む全 \(\pi_t\)-fiberの正規化ambient直径が一様にゼロとなる。\(d\ge6\) で \(p_T\) が潰す内部木についても、一つの木上の複数の \(\pi_t\)-fibersの**合併全体**を評価した（`ke:collapsed-tree-full-fiber-collapse`）。

証明は十分遅い固定段階の対角選択を用い、各固定次数・固定族について一つの許容された標識付き木系を選ぶ。最適収束速度、任意に先指定した木系・作用・critical valuesへの一様な適合、次数一様の評価、全次数のmatroidal atlas、special Lagrangian性は結論に含めない。五次だけの結果ではない。新たな誤りが見つかった場合は、依存する主張・方針・hubを含めて訂正する。

### 証明の状態と外部KE仮定との区別

現行改訂24では、`ke:anchor-trimmed-neck-domain` により共通anchorで保持されたneckのmoment範囲を正確に $[-\delta_j,\delta_j]$ と同定する。`ke:same-moment-corner-reference` はsource・branchを含む全点を、同じcanonical momentの旧corner辺torusへ有界なambient費用で接続する。この参照点と既証のclipped-depth Lipschitz評価により、同じ $f_t=p_T\pi_t$ の全域値比較を導く。固定残余基底のMoser被覆と接続は有限cut版を明示した。Sourceの特異reduction、全段階共通のmarked tree、K2全intersectionの補強も保持する。今回の追加証明の内部点検・組版・表示確認は末尾に区別する。

Actual全域構成、sourceの全点評価、同じ基底値に対する全域上下界を主稿に保持する。Componentの対数接続費用、anchor interval外のneck尾部の深度、残余基底→cut→parameterの非循環な選択も保持する。Coreのcompact-relative Morse–Smale化と閉isotropic filtrationも明示し、primitive・nontrapping・collar補間・全fiber trim・閉quotientを重点監査した。追加証明は別担当と独立に内部点検済み。数学的点検、形式証明、組版、有限計算、GitHub保存は区別する。

本研究は、正則normal frameのscalar Schwarz障壁とglobal clipped-depth mapでno-shortcut下界を、同一moment接続と有限portal galleryで上界を直接証明する。**関連KE研究の \((\mathrm{CP})_d\)、\((\mathrm{PBE})_d\)、\((\mathrm{TC})_5\) を証明したという主張ではない。** これらを対象族で検証する課題は関連研究側に残り、本稿の全域実現定理では仮定として使わない。`topo:ke-map-compatibility` による既存GH近似との条件付き比較は、有効な補助結果として保持する。

### 証明の構成と公表前に点検する箇所

K1–K3はactual全域fibrationを、K4は同じ写像の全曲面distortionと全fiber合併の収縮を与える。K5の統合定理は `ke:global-metric-realization` に置く。現在はK0とK5の公表前点検を優先する。詳細な入力・参照commit・定理ラベルは [KE依存関係](research/ke-dependencies.md)、有効な障害と着想は [研究ノート](research/notes.md) が正本。

| 課題 | 最初に行うこと | この課題の達成条件・現在の状態 |
| --- | --- | --- |
| K0：入力の監査 | 次は `ke:global-base-parameterization` と `ke:global-depth-base-comparison` を逆にたどり、保持corner・branch・source・coreで同じ $f_t$ の基底値を使っていることを点検する。並行して一次文献との比較を詰める。 | Capped・full-triple/Savin・complete volume比較・Song/RZに加え、actual primitiveのC1生成場、全support被覆、nontrapping、relative collar、whole-fiber trim、compact cone fillingを重点監査済み。Source中心のsingular reduction・primitive消滅cycle・閉pinched torus、K2の全intersection、全stageの固定marked treeを追加点検した。Coreの弱い層別構造はcompact-relative Morse–Smale化で閉じた。全既存証明・全入力の包括的再監査と外部査読は未了。 |
| K1：actual neckの短円とbuffer | `ke:fixed-stage-source-neck`、`ke:neck-corner-diagonal-matching` の残余compact→normal cutoff→moment区間→parameter閾値の選択を用いる。 | 固定source-free基底の二側比較、source中心を含む短円、共通source/像、source-inclusive neckを証明。十分遅い残余exhaustionでは全flow・全円orbitを含むtripleとの共通開領域も確保した。任意に指定した縮小速度や曲面全体の被覆への一様性は主張しない。 |
| K2：複数endの同時整合 | `ke:neck-corner-saturated-union` の部分fibrationを全域構成への入力として使う。 | 三armの座標接続、normal period一致、相対Hamiltonian補正、共通moment区間とreduced graphにより、closed cornerと切詰めたneckの**全交わり**でfiber partition・向き付きnormal cycle・内部source/saddle markingを一致させた。Endの第二cycleは共通torus同定で移送して選ぶ。Source・saddleを含むactual部分fibrationを得た。独立に選んだ第二periodの一致は自動ではない。Core接着と全曲面被覆はK3で別途証明した。 |
| K3：component coreの相対接着 | `ke:actual-global-fibration` と四つの追加節を距離評価の入力とする。 | **固定段階の全域構成を証明。** 正residue periodの厳密同定、閉moment link、固定stageでの全特異層近傍の被覆とcompact complement、actual generator C1・adapted primitive/nontrapping、saddleを動かす相対葉族、全fiber単位のtrimを経て、全 $X_t$ をactual Lagrangian fibrationで覆った。各componentのcore・変更collar・neck尾部のambient接続費用は $C(1+\log(N_j+1))$、遅い対角選択で正規化径が消える。全曲面distortionは含まない。 |
| K4：全曲面の距離比較 | `ke:sharp-global-one-active` → `ke:global-depth-lipschitz` → `ke:global-depth-base-comparison` → `ke:global-ambient-lower` と、`ke:global-ambient-upper` の接続を点検する。 | 原稿に全域上下界の証明あり。中央sourceの全点径 $O(1)$、全moment退出 $O(1)$、保持cornerの基底値整合、全内部木の共通momentを用いる。`ke:collapsed-tree-full-fiber-collapse` は潰される全fiber合併を評価する。新証明と接続を複数担当で内部点検済み。 |
| K5：統合主定理と公表準備 | `ke:global-metric-realization` の全固定 $d\ge5$ の主張から、一次文献比較・新規性確認・本文の説明順を整える。 | 同じ $f_t=p_T\pi_t$ のdistortion消失を統合。全域上界は $C_d\{b_j^{-1}+(1+\log R_t+\log(N_j+1))/R_t\}$ に整理した。下界の段階定数と定性的な閾値は残り、最適rateは未解決。組版・表示確認の状態は末尾を参照。全主稿再監査・外部査読・形式証明は未実施。 |

K1–K2の正本は `ke_neck_corner_exhaustion.tex`。残余compactの定数を先に固定し、それを支配するnormal cutoffと共通moment区間を選び、最後にparameter閾値を取る。`ke:normal-flow-naturality` とmoment依存のreduced葉により共通開collarを構成する。さらにcorner cut $m_t=6b_j$、neckの葉でのtrim $B=7b_j$、広いnormal-first patchを用い、first-exit評価で全intersectionを共通plateauへ閉じ込める。逆normal flowの自然性からmomentを同定した後に深いnormal下界を使う（`ke:neck-corner-saturated-union`）。

この部分fibrationはsourceのpinched torusとsaddle fiberを含み、各closed cornerの内在・protected GH評価を持つ。`ke:actual-global-fibration` は保持されたcorner葉とsource近傍を保って全域へ接着する。中央全点径にはGaussian tail・Bishop–Gromov比較による証明と、短いgate退出・source-arm tensor比較による直接証明がある。全intervalのsource接続と基底値の整合を用い、全曲面のshortcut下界と木上のfiber合併・portal上界を別々に証明した。局所protected距離をそのまま全曲面距離に読み替えてはいない。

Source全体のEuler場 $W_+=x\partial_x+y\partial_y$ のactual normを固定chart上で一様に抑えた（`ke:source-euler-bound`）。中央sourceの $|z|\ge e^{-a_t}$、$a_t=o(R_t)$ の部分は、固定residual shellへ $O(a_t+1)$ で接続でき、正規化ambient径が消える（`ke:source-sublog-residual-connectors`）。Euler経路だけでは軸に届かないが、`ke:source-central-diameter` は別のGaussian体積比較で $z=0$ と極小residual点も含む全点径を $O(1)$ に抑える。`ke:fixed-base-source-central-band` により、固定基底の全中央帯と閉pinched torus全体も収縮する。

## 原稿・ノートの正本と公表単位
- `papers/surface-lagrangian-torus-fibration.tex`：このrepoの主たる公表用本文。相対SNC構成、次数分割、分岐底、作用適合atlasとactual KE–fibrationの全域GH実現定理（現行改訂24）。統合証明は `papers/sections/paper/ke_global_metric_realization.tex`。組版・表示確認の実施状態は末尾と `research/validation.json` に記す。
- `papers/quintic-integer-gluing.tex`：五次整数アフィン接着、高分母支持グラフの独立論文（第25稿、201頁の記録）。指定SNC cores・K5 graph・標準cones・marked puncturesを保つ候補が対象。必要支持3型26標識は**実現数ではない**。G5_14の中央matching、一般分母剛性、三高Dの同時非負性が未解決。
- `papers/meridian-surgery.tex`：四pantsのmeridian局所置換と閉corner circuitsの障害（18頁の記録）。
- `papers/research-notes.tex`：各種補題・証明素材のTeXノート（現行65頁、変更した第1・4頁を表示確認）。
- `research/notes.md`：現在有効な数学上の着想、条件、文献比較、障害と再開手順。検証コードは `verification/`。
- 複素次元3のnormal-trivial curves、focus block、相対円板群と大域存在目標は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) の `main` が正本。詳細をこのrepoへ二重掲載しない。関連するKE研究はresearch-hubから参照する。

## 複素次元2：先行研究とsingular fibers
曲面の主定理 main:global は、Mikhalkin (Topology 43, 2004, Theorem 1) の全次元stratified topological torus fibration（Lagrangian性は各maximal cellで選ばれたfiberだけ）、Zhang (J. Math. Study 58, 2025, Theorem 1.1) の一般型と微分同相な四次元多様体のpants分解、Evans–Mauri (Ann. Henri Lebesgue 4, 2021, §3.1) の四次元pantsの局所Lagrangian fibrationとは区別する。Smith (Turkish J. Math. 25, 2001) の制限はhomologically essential toriとtame singularitiesを追加仮定する。Leung–Symington (JSG 8, 2010, **Theorem 2.1**) により、閉almost toric fibrationを持つ四次元多様体の分類に一般型X_dは含まれない。Fernández de Bobadilla–Pełka (CPAM, 2026) の一般SNC退化の部分領域構成から全域のfibrationは自動的には従わない。一次資料と仮定はresearch/notes.mdの「複素次元2」節と主稿Introductionに整理。

全平面構成のsingular fiberは、(1) 分岐辺上の S¹×(S¹∨S¹)（Euler数0）、(2) 面内孤立nodeでの一重pinched T²（Euler数1、focus monodromy）、(3) d個のcore頂点の一般位置d−1直線補空間に対応するlogarithmic Weinstein skeleton（Euler数C(d−3,2)）。正則fiberはLagrangian T²。全平面分割の開分岐辺はC(d,2)(d−4)本（**fiberの個数ではない**）、孤立nodeはd C(d,2)個。五次では(cores, branch edges, nodes)=(5,10,50)、六次では(6,30,90)。通常のalmost toricにない分岐辺とcoreを許すことが本研究の特徴。一般次数の全体構成と、五次・六次に限る大域作用適合atlasは別の主張。先行研究との比較は現行原稿とノートに保持する。全証明の独立検証と包括的新規性の確定は未了である。

## KEのGH極限との関係
標準負KE尺度では成分内部の四次元完備KE幾何が残る。径の尺度 $R_t=\log(-\log|t|^2)$ では、本稿の `ke:global-metric-realization` が同じ $f_t=p_T\pi_t$ を用いるactual GH収束を直接証明する。五次は $p_T$ が同相、六次以上は基底内の木全体も収縮する。関連KE研究にある $(\mathrm{CP})_d+(\mathrm{PBE})_d$ を使う経路とは証明を区別し、これらの仮定自体を検証したとはしない。既存近似 $\Phi_t$ と $p_T\pi_t$ の一様比較から収束を移す `topo:ke-map-compatibility` も補助命題として保持する。Zhang (MRL, 2015)の局所collapse定理のQ-factorial・相対ample仮定は、source germ $xy=tz$ を持つ我々の族へそのまま適用できない。文献と適用計算は `research/notes.md`、公表用の比較は主稿 `intro:ke-collapse` を参照。

## 成分coreの存在とtarget距離の確定部分

`ke_component_core_geometry.tex` はRochon–ZhangのSNC cusp potentialを用いて、固定compactで厳密一致する正則化と、極限KE形式自体の正residue・有限型Weinstein coreを与える。全域への接着は、既存のactual linkの葉をLiouville flowで内向きに延ばす構成で実現した。これにより、compactification出力の葉を先指定したcollarへ点固定で移す相対germを追加入力とせずに済む。既存の局所core fillingの結果は保持する。

`ke_component_link_cover.tex` は $q_a=M_a+2\pi w_a=\pm\widehat\mu_N$ を整数windingとexact transportから同定し、$N_j\iota_j\gg1$ のmoment cutsを丸めて閉linkを作る。固定shellのmoment上界と同じMoser flowの逆像bufferにより、K2の部分fibrationが中央の全特異層の固定近傍を覆い、その補集合がcomponent compactsに入ることも証明する。`ke_core_invariant_primitive.tex` は生成場のC1 smallness、centered scalar平均によるexact補正、全overlapとcutoff shellの被覆、nontrappingを証明する。`ke_relative_reduced_foliations.tex` はfull critical leavesを保つ相対葉族を構成する。

`ke_actual_core_gluing.tex` の `ke:actual-global-fibration` がこれらを統合し、全 $X_t$ 上のactual KE–Lagrangian fibrationを与える。全fiber単位のtrimと閉同値関係により連結fiber・Hausdorff基底を保ち、基底は同じ標識付き $B_d(T)$ となる。第二actionやcritical valuesの数値は先指定しない。各componentの変更領域とneck尾部の接続費用を $C(1+\log(N_j+1))$ と評価し、$R_t\ge jC(1+\log(N_j+1))$ によって正規化ambient径・選んだ接続費用を消す。異なるcomponent cores全部の合併径、任意のLiouville軌道長、core/fiberの内在径の評価とは区別する。

`ke:core-depth-upper` と `ke:removed-corner-target-cap` は、実際に切り取った各component capの旧softmax像を $d_\square(P^{\rm old}(x),e_i)\le\sqrt2\log(CN_j)/R_t$ と評価する。閉link上の深度上界を固定strictly plurisubharmonic potentialの最大原理でcore全体へ延ばす。`ke:global-base-parameterization` は旧softmax値との $O((1+\log N_j)/R_t)$ 整合を全保持cornerで与える。保持領域自身の新しい内在距離の上界を要求せず、旧corner内の経路を全曲面の経路として用いて `ke:global-ambient-upper` へ接続する。全曲面の下界はscalar評価による別の証明である。

`base_topology.tex` の非伸長座標retractionにより、任意の座標部分複体 $\mathcal C_I$ の内在距離は全 $\mathcal C_d$ の距離の制限に一致する。特にclosed-cornerのGH評価は同じ誤差で全target距離を使えるが、source側の全曲面shortcutを制御したとはしない。最短路には六label以下で十分で、portal比較のgallery数は五次30、六次以上60にできる。

六次以上では $\operatorname{diam}\mathcal C_d=2\sqrt5$。最大対は互いに素な三元supportのall-ones頂点対に限る。四つの明示的galleryによる上界と、120三角形上のPL calibrationによる下界を本文で証明した。五次の既存値 $\sqrt{13}$ を使わず自己完結した証明である。直径近似対の明示的な線形安定性だけに五次の厳密値を使う。有限部分は `python3 verification/verify_cubical_six_label_geometry.py` で再検算できる。Actual KE曲面の $R_t^{-1}\operatorname{diam}(X_t,g_t)\to2\sqrt5$ は、六次以上では全域実現定理とこの有限幾何を合わせた帰結となる。

## 全深部三重点の actual 比較と閉cornerのGH極限
任意の固定次数 d≥5 の一般位置全平面退化で、三重点の全深度比・全角度に一様な actual KE 比較を証明した。正確な座標 ζ0ζ1ζ2=t、ell_i=−log|ζ_i|²、L=−log|t|²、R=log L とし、k_Lをlogarithmic simplex上のcomplete toric KE form、その実計量をg_L^sfとする。十分大きい固定m1と各qのCqについて、m≥m1、min ell_i≥mで
\[
\left|\log\frac{\omega_t^2}{k_L^2}\right|\le C/m,\qquad
\|g_t-g_L^{sf}\|_{C^q}\le C_q/m.
\]
定数は固定dと族に依存してよい。次数一様性は主張しない。証明の正本はKE主稿 `coarse:thm:full-triple-tensor`。

固定toric模型の存在・完備性にはZhang (2015), §2.1, Theorem 2.1 / Proposition 2.2を用いる（退化族のTheorem 2.4とQ-factorial仮定は使わない）。ψ_L=log L−Σlog ell_iに対してψ_L−(log3)/2≤φ_L≤ψ_L、V_L/3≤k_L²≤V_Lを内外にずらした障壁で証明する。Complete模型から三つの半平面へのYau Schwarz lemma、determinant比較、内部正則性により一様cusp geometryを得る。凸性からfacet shiftのlog-density差をO(1/min ell)とし、actual計量を内外のsimplex KE metricsでvolume比較する。Savinの小摂動定理でtensor・全高階誤差へ移る。Actual metric bufferや(TC)/(PBE)を前提としない。

Actual側の大域入力は `coarse:cor:degree-d-volume-lower`。Adjunction residueでcanonical densityを固定し、backgroundによるHermitian frame errorの吸収と各正のcap方向のminorから六型のdeterminant下界を証明する。Sourceでは元のplane coordinatesを保つexact xy=tzとrescalingにより二つのcap係数≥c_d/Lを使う。Compact minimum原理からactual volume下界を得る。この依存部分の証明と適用条件はKE側の原稿に明示されている。このcapped下界とfull-triple比較の必要な証明を重点点検し、固定境界面の下界だけで足りる箇所も明示した。監査範囲は依存表に記し、外部主稿全体の独立再監査は行っていない。

Lagrangian主稿 `ke:actual-closed-corner` の同じ averaging–Moser flow と同じactual Lagrangian torus bundleに対し、`ke:closed-corner-gh` と `ke:closed-corner-protected-gh` が全閉cornerのGH極限を与える。m=Rでsoftmax hexagonのMoser像をW_{t,J}、その射影をπ_{t,J}とすると、R^−2 g_tによる距離について
\[
\sup_{x,y\in W_{t,J}}
\left|d_t(x,y)-d_J(\pi_{t,J}(x),\pi_{t,J}(y))\right|
\le C\frac{\log R}{R}.
\]
これはW_{t,J}自身の内在距離と、外側保護領域V_t={min ell_i>R/2}内の全経路を許す距離の双方で成立する。標的のd_Jは三枚のunit squaresからなるC_J自身の内在距離として定義する。`topo:coordinate-retraction` により、これはfull C_dの距離の制限と等しい。この局所評価からの形式的な置換は行わず、全曲面ambient下界は `ke:global-ambient-lower` で別に証明した。全fiberのintrinsic/ambient diameterはO(1/R)、正規化後はO(1/R²)、raw cubical mapとの誤差はO(log R/R)。Squareの継目も同一のregular T²であり、既存大域fibrationのsource・branch・coreのsingular fibersとは同定しない。

距離の解析入力はKE主稿 `simplex:lem:rank-one-schwarz` の係数1評価と `simplex:prop:dominant-product` のsharp product比較。Clipped logarithmic projectionで模型simplex全体の経路の下界を示し、三枚以内のsquare galleryを内部へ移して上界を得る（`simplex:thm:closed-corner-model`）。ActualとのO(1/R)比較と同じMoser flowのC1評価で上記の結論へ移す。正本は `papers/sections/paper/ke_closed_corner_gh.tex`。Source・saddleを含むneckからcoreへの全域接着は `ke:actual-global-fibration` で証明した。全曲面を通るshortcutは `ke:global-depth-lipschitz` の全曲線評価と同じ基底値との比較で制御した。新規性の網羅的確認と外部査読・形式証明は未実施。

## 開正方形上のactual KE–Lagrangian collapse
主稿の `papers/sections/paper/ke_open_cell_collapse.tex` に、任意の固定次数d≥5のactual KE計量に対する局所結果を置く。関連KE主稿 `simplex:cor:actual-dominant-product` は、三重点独立深度 a,b∈[L^η/2,2L^(1−η)]、0<η<1/2 上のproduct-cusp比較を全固定階でO(L^−η)と与える。Complete simplex模型の誤差O(((a+b)/L)²)とactual/model誤差O(1/min ell)を合わせた率であり、global capped volume下界、明示的な上下KE barriers、Savin (2007), Theorem 1.3に依存する。(TC)_dや(PBE)_dを追加仮定しない。

`ke:open-cell-moser-c1` は平均化のprimitiveとMoser場のC1 normをO(L^−η)とし、flowのpullback metricを制御する。`ke:open-cell-collapse` はKη=[η,1−η]²上のactual KE–Lagrangian T² fibrationを構成し、fiberのintrinsic/ambient diameter O(L^−η)、raw mapとの誤差O(1/R)を与える。Moser像領域に内在長さ距離を入れると、R^−2 g_tは平坦KηへGH収束し、projection distortionはO(L^−η+L^−η/R)=O(L^−η)。定数は固定ηに依存する。これらの証明と一次資料の適用条件を点検した。一般的新規性は未確認。

固定ηの開正方形と全閉cornerは、それぞれ上記の局所定理で扱う。Source・branch・coreを含む全域fibrationと同じ写像のambient距離比較は `ke:global-metric-realization` へ統合した。局所定理単独から全域distortionを推論してはいない。

## 共通normal circleに適合する二段階平均

主稿 `papers/sections/paper/ke_staged_neck_averaging.tex` が正本。自由な正則normal S¹を先に平均してη=A1ωとし、triple endで残る円を平均してκ=A2ηとする。単一primitive ω=dλとflow/domain bufferの下で、φ*ω=η、ψ*η=κ、Θ=φψについてΘ*λ=A2A1λ+dqとなる。第二flowはnormal circleと可換であるから、各actual torusはneckと同じactual action φρ1φ^−1を含む。μ∘ψ=A2μが厳密に成り立ち、全marked整数cycleのaction periodsを同じλから規格化できる（`ke:staged-neck-averaging`）。

`ke:short-circle-actual-buffer` は、作用不変領域全体でperiod-1 normal generatorがactual計量に関して|V|≤εを満たせば、Moser trajectoryのactual長をc_w ε以下に抑える。c_w=(π/2)||w||₂で、通常kernelならπ/(2√3)、centered kernelならπ/(4√3)。作用不変背景・tensor二側比較・exactnessはこの評価に不要で、forward/backward両flowに成立する。さらにcompact飽和集合Kのactual bufferが(2c_w+1/2)εを超えれば、飽和source OとそのMoser像の両方がKを含む（`ke:short-circle-image-buffer`）。単一primitiveがあれば同じKの近傍にactual Hamiltonian normal actionを得る。全neckの一様な短さ・buffer、C¹とintrinsic fiber径は引き続き別の入力である。

一段階構成、二段階構成、固定整数基底の変更は、共通domain/image bufferの下でHamiltonian isotopyにより比較できる（`ke:staged-hamiltonian-comparison`）。形式のpositive triangle上のpath homotopyとexact primitive transportを明示している。Exact endpoint mapであることだけからHamiltonian性を結論しない。旧bundleと同じfiber partitionとは主張しない。

`ke:staged-closed-corner-gh` は、三重点の標準T²の任意の固定primitive subgroupを第一段に選び、actual closed-corner bundleと同じO(log R/R)の内在・protected-ambient GH評価を与える。Fiberの元の尺度のintrinsic径はO(1/R)。三重点内の定量的bufferは既存のfull-triple比較で検証済みである。

関連KE主稿 `pair:prop:bundle-conic` / `pair:cor:global-primitive` / `pair:cor:actual-common-moment` により、source-freeな固定compact base上では一つの正則normal action、canonical primitive、円平均η_tの共通moment intervalが得られた。Fixed-end momentはperiod1の規約で±4π/(−log r²)を主項とし、r固定後t→0とする。これらからneck全体のnormal Moser flowの生存・bufferや各triple endとの同時一致は従わない。

`ke:staged-reduced-extension` は、marked simple-saddle foliationと適合するreduced end germsの延長を仮定して、regular T²とsaddle S¹×figure-eightを持つneckを接着する。共通normal actionだけでは、別に固定したneckの第二periodやfiberそのものの一致を意味しない。Reduced leaves、内部marking、critical actionの条件を具体的な構成で確認し、全域接着とGH実現へ用いた。任意の独立先指定periodへの適合は結論しない。

## 相対接着で必要なcollar条件
`ke:relative-fiber-preserving` は、torus飽和した開collar N上の元のphase toriが既にactual ω-Lagrangianなら、chain primitive β=Hω、H=K_1+A_1K_2によるMoser flowが各fiberを集合として保ち、p∘φ^−1=p on Nを満たすことを証明する。作用不変性は不要であり、centered chain primitiveでも同じ結論となる。各点を固定することとは異なる。点ごとの固定には、作用不変なcollarとcentered primitiveを用いる既存の `ke:relative-averaging` が使える。

`ke:relative-neck-matching` は、同じorbit partitionを持つactual Lagrangian neck fibrationが開overlap上に与えられれば、基底collarを同定して局所接着できるという条件付きの系である。共通葉と全intersectionの飽和は、許容射影と遅い対角選択を用いた `ke:neck-corner-saturated-union` で別途実証した。定数係数のmonomial座標変更はorbit partitionを保つが、非定数holomorphic unitを含む変更は一般に保たない。任意の別のprimitiveへの置換でもfiber保存が続くとは仮定しない。

## 小さいLagrangian fibersへの局所的な前進
曲面側の着手対象は複素次元2でのKE極限とLagrangian fibrationの適合性である。主稿の `papers/sections/paper/ke_fiber_compatibility.tex` に次の証明を置いた。

- `ke:short-torus-averaging`：自由な正則 $T^2$ 作用、torus不変Hermitian計量 $h$、$c h\le g_\omega\le C h$、torus上のperiod零を仮定する。作用の周期1生成場の長さの和を $e$ とすると、平均化のchain homotopyから長さ $O(e)$ のprimitiveを作り、一つのMoser flowで領域全体にLagrangian fibrationを構成する。変位は $Ce/(2c)$ 以下、ambient fiber diameterは $\sqrt C e(C/c+1/2)$ 以下。高階微分比較は使わない。
- `ke:triple-hexagon`：$\zeta_i\zeta_j\zeta_k=t$ の三つのsquareを一つのhexagonとして全phase torusで実現し、raw-depth mapとの誤差を $O((1+\log m_t)/R_t)$ に抑える。
- `ke:triple-moving-fibration`：全phaseを含む moving domain $\min\ell_a>m_t/2$ 上の一様tensor比較を追加仮定すれば、actual負KE形式に対する局所fibrationが得られ、そのambient fiber diameterは元の尺度でも $O(m_t^{-1})$。$m_t=R_t\to\infty$ とできる。負KE equationにより局所canonical trivialization上で形式がexactとなるのでperiod条件は満たされる。

これらは原稿に条件と証明を保持する局所結果である。Averaging–Moserの基本方法はRuan, arXiv:math/0309177v2, §3に先行し、一般的新規性は未確認。H-minimal/special Lagrangian性、大域接着、singular fibersの計量評価は結論しない。

**解析入力の区別：** 関連KE主稿の `coarse:prop:density-counterexample` により、負KE計量であってもbounded volume densityから一様tensor比較は導けない。五次coarse metric packageには独立な $(\mathrm{TC})_5$ が必要であり、その無条件な検証は未完成である。これは対象compact familyの反例ではない。全深部三重点のfull-orbit moving tensor比較は全固定d≥5で検証済みであり、閉cornerへの局所適用に追加仮定は不要である。Source等を含むexterior全体の一様tensor二側比較は別の未解決問題である。本稿の全域ambient距離比較は、それを仮定しないscalar/portal評価で証明した。

## 中心結果と証明の状態
- 曲面側の分岐基底 \(B_d(T)\) とKE候補 \(\mathcal C_d\) は、labelled cell-like homotopy equivalence \(p_T\) で結ばれる。\(d=5\) では同相、\(d\ge6\) では非同相（`papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`）。
- 人工的PL長さ距離\(d_\varepsilon\)によるgraph correspondenceの誤差は、\(d=5\) で \(\Theta(\varepsilon^2)\)、\(d\ge6\) で \(\Theta(\varepsilon)\)。GH収束は上から同じ次数で評価できるが、\(d\ge6\) にGH距離の同次数の下界を主張しない（`topo:metric-collapse-sharp`）。
- 幾何学的な基底計量で同じ収束を得るための十分条件は、(N) global no-shortcut、(S) square geodesic lifts、(F) small-fiber/portal connectors（`topo:finite-portal-criterion`）。二つのsquareを一頂点で貼った反例（`topo:portal-counterexample`）により、(F) は(N)+(S)からは従わない。これらは抽象的距離論である。本稿のP0では全空間のactual ambient距離を直接扱い、独立のactual action metricの構成・その長さ完備化までは結論していない。
- 六次同時Petersen分岐木系は6通り・\(S_6\)の一軌道で、各安定化群の位数は120。固定木系はfull \(S_6\)-equivariantではない。新規性は未確認。

## 優先する次の一手

1. **依存証明と一次資料の包括的再点検。** 直近は共通anchorの全域分割・同一moment参照点・有限cut版の独立点検を終え、`ke:global-base-parameterization` → `ke:global-depth-base-comparison` の依存を確定する。さらに `ke:global-metric-realization` から逆にたどり、外部KE主稿の大域capped volume下界・full-triple比較・fixed-component収束、Rochon–Zhang、Dinh–Marinescu–Vu、Evans–Mauri、Yau等の仮定・規格化・領域を一覧と本文で照合する。今回の内部点検を全依存証明の再監査と読み替えない。
2. **新規性と公表範囲の確認。** 一般型曲面の既存torus分解、所定Kähler形式での全regular fiberのLagrangian性、負KEの径の尺度でのGH収束、source・branch・coreを含む全域実現を分けて比較する。関連repo側のCP/PBE/TCの条件付き結果との関係を明示する。
3. **主稿の構成と再現。** 統合定理を軸に本文の説明順・参照・要約を整え、有効な既存証明と独立成果を保持する。必要な組版・表示確認を行い、通常commitで研究repo、続いてhubを更新する。旧版の追記や重複した証明を増やさない。

五次整数接着の \(G_{5,14}\) 中央matching・\(\{4,1,0\}\) 配分・分母三条件、\(G_{5,16}\)、\(G_{5,17}\)、三高係数の同時非負性と一般分母剛性は独立した未解決課題として保持する。必要な26標識は実現数と読み替えない。

## 保存・再現と現在の検証状態

重点点検済みの範囲は、sourceのsingular reductionと固定marked tree、K2全intersection、中央sourceの全点径、全moment退出、基底の接着、sharp scalar障壁、同じ写像の全域上下界、統合主定理と必要なK2/K3の接続を対象とした。DMVの掲載版Theorem 1.2とYauのSchwarz lemmaを一次資料で確認し、Rochon–ZhangのSNC cusp入力、Evans–Mauri Lemma 2.16、および外部KE主稿のdominant-product・fixed-end momentの適用も照合した。全主稿の独立再監査とは区別する。

現行のTeX分割節と検証スクリプトは `papers/sections/` を直接参照し、旧ルートsymlinkに依存しない。静的な構成検査は `python3 verification/verify_repository_layout.py`、現行の五主検算・五独立監査は `python3 verification/run_current_checks.py`。旧JSONやmanifestの相対パス・記録時点のSHA-256は出典情報として保持し、パス正規化後の現行実行パスと区別する。
組版はrepo直下の `latexmk papers/surface-lagrangian-torus-fibration.tex`、整数接着は `latexmk papers/quintic-integer-gluing.tex`。LuaLaTeXとLuaTeX-ja／TikZ／日本語フォントが必要、PDFとSyncTeXはbuild/へ出力しGitで追跡しない。段階別の実行は `scripts/research_check.py` と [Cloud Codexの再開手順](research/cloud-codex.md) を参照する。元の計算コード、入力、証明書は保持する。

2026-11-21 / v3.4：主稿改訂24では、共通anchorによる保持neckの正確なmoment範囲と、同一momentの旧corner辺参照torusによる全域基底値比較を明示した。固定残余基底のMoser被覆・同一moment接続・中央帯評価を、十分大きい有限cutにも一様に適用できる定理文へ整理した。追加証明と接続を内部点検中。現行改訂24の組版・表示確認は未実行で、直近に確認したPDFは改訂23の251頁・指定23頁である。整数検算suite・他論文・TeX研究ノートの組版は今回は未実行。形式証明・全主稿と全外部入力の包括的再監査・外部査読・網羅的新規性確認は未実施。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りでは承諾なしで通常コミットを `main` へpushし、Cloud Codexの長時間作業は切りのよいところ、遅くとも前回成功pushから約15分を目安に現行の有効な成果と未解決箇所を保存する（詳細はAGENTS.md）。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。

GitHub管理前の研究では、区切りごとに現行方針・ノート・論文・必要な再現資産と組版済みPDFをbundleとして承諾なくLibraryへ保存する。移行後は対象repoのmainを正本とし、Libraryはpush不能時の緊急保存または別途指定に用いる。現在有効な内容から再開できる構成を保ち、旧版の復元用アーカイブ、組版中間物、重複実装を現行一式へ蓄積しない。元資料独自の有用内容は移行・検証前に失わず、削除を指示されていない既存Library資料は保持する。
