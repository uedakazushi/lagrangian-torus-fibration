# KE–fibration 大域実現の依存関係

2026-11-21 / v2.1。目標・優先順位は [研究方針](../00_research_plan.md)、大域実現の定式化と結論は主原稿の `ke:global-realization-section` 節・定理 `ke:global-metric-realization` を正本とする。本書は外部入力の所在・適用範囲、本稿の直接評価による依存の接続、および確認範囲を保持する。

## 確認した正本と規格化

関連する [kaehler-einstein-degeneration](https://github.com/uedakazushi/kaehler-einstein-degeneration) の確認コミットは `1abc96cea3d9c369410e0e9d2a57414276e7c776`。以下の **IV** は同repoの [papers/kaehler-einstein-degeneration.tex](https://github.com/uedakazushi/kaehler-einstein-degeneration/blob/1abc96cea3d9c369410e0e9d2a57414276e7c776/papers/kaehler-einstein-degeneration.tex)、**V** は [papers/cubical-gh-limit.tex](https://github.com/uedakazushi/kaehler-einstein-degeneration/blob/1abc96cea3d9c369410e0e9d2a57414276e7c776/papers/cubical-gh-limit.tex) を表す。外部の分割原稿は同repoの `papers/sections/` にある。この確認版を固定した参照として保持し、再開時に最新 `main` と比較して、訂正・追加仮定を優先する。外部原稿本文をこのrepoへ複製しない。

外部入力について確認したのは、該当する定理文・証明の所在・依存仮定・規格化と、本稿の接続に必要な証明箇所である。下表の「証明あり」は原稿の状態を表し、全旧証明の独立再監査・形式証明・全一次文献の再精読・組版の再実行を意味しない。現行証明では上記mainを再取得し、full-triple比較、`simplex:lem:rank-one-schwarz`、`simplex:prop:dominant-product`、`simplex:cor:active-cogram`、`pair:thm:fixed-end-moment` と関連するvolume入力の定理文・必要な証明・規格化を照合した。今回の新証明と大域接続の内部点検範囲は末尾に記す。

IV の `ass:Gd` は、一般位置の $d$ 平面、非零小parameterでの滑らかさ、各二重線上の $F_d$ の相異なる $d$ 個の単純零点、全三重点での $F_d\ne0$ を仮定する。各固定 $d\ge5$ と固定族を扱い、次数や族全体に一様な定数を要求しない。

\[
X_t=\{\textstyle\prod_{i=1}^{d}L_i+tF_d=0\},\quad
\operatorname{Ric}(\omega_t)=-\omega_t,\quad
[\omega_t]=2\pi(d-4)H,\quad
L_t=-\log|t|^2,\quad R_t=\log L_t.
\]

距離は $\bar d_t=R_t^{-1}d_{g_t}$、Riemannian metric は $R_t^{-2}g_t$。標的は

\[
\mathcal C_d=\{w\in[0,1]^d:\max_iw_i=1,\ |\operatorname{supp}w|\le3\}
\]

の各unit squareをEuclidean距離で貼った**複体全体の内在長さ距離** $d_\square$ である（IV `eq:degree-d-normalization`, `eq:Cd-definition`）。Primitive class $2\pi H$ に再規格化すると距離が $1/\sqrt{d-4}$ 倍になる。一般のhyperplane classでのfibrationをactual KE formへMoser移送する際、その移送の計量的制御は別の入力である。

## 現行の結論と外部仮定の扱い

定理 `ke:global-metric-realization` は、上の一般性条件を満たす任意の固定 $d\ge5$ について、actual $\omega_t$ に関する連結fiberの連続全射 $\pi_t:X_t\to B_d(T)$ と、同じ $f_t=p_T\pi_t$ に対する

\[
\sup_{x,y\in X_t}
\left|R_t^{-1}d_{g_t}(x,y)-d_\square(f_t(x),f_t(y))\right|\longrightarrow0
\]

を与える。正則fiberはLagrangian $T^2$、source・branch・coreの特異fiberは本稿の相対構成による。左辺は全曲面の任意の経路を許すambient距離である。$d\ge6$ で $p_T$ が潰す内部木上の全fiber合併も一様に収縮する。木系の組合せ型は固定するが、critical values・collar・基底parameter化と遅い段階選択は $t$ に依存してよい。

この結論は `ke:actual-global-fibration`、`ke:global-base-parameterization`、`ke:global-ambient-lower`、`ke:global-ambient-upper` を同じ写像で組み合わせたものである。**外部のCP/PBE/TCは未検証のままであり、本稿がそれらの全packageを証明したとは主張しない。** 本稿では、sourceを含むsharp scalar normal評価と全域clipped logarithmic mapによる下界、共通momentの接続と有限galleryによる上界で、P0に十分な距離評価を直接証明する。最適収束速度、次数一様性、任意に先指定されたcritical valuesの実現は含まない。

## 外部解析入力の状態

| 入力 | 正本・ラベル | 適用範囲と残る条件 |
| --- | --- | --- |
| 全次数のcapped volume下界 | IV `coarse:cor:degree-d-volume-lower` | 固定 $d\ge5$、`ass:Gd` の下で証明あり。体積比からtensor二側比較を推論しない。 |
| Sourceのoriented volume比較 | IV `coarse:lem:pair-arm-density`, `coarse:lem:complete-volume-upper` | $xy=tz$ の正しいorientationのannulus–disc上で用いる。一般のcomplete域では対数体積比の上有界性を明示的に仮定する。本稿の有限annulus–discでは固定 $t$ のcompact closureへの延長とmodel densityの境界発散で確認できる。中央gateからvolume上界だけを中央へ延長し、中央のtensor比較は入力にしない。 |
| 全深部tripleのactual/model比較 | `full_triple_comparison.tex`, `coarse:thm:full-triple-tensor` | $m_1\le m<L_t/3$、$\min\ell_i\ge m$ で全phase・全深度比に $C^q$ 誤差 $O_d(m^{-1})$。追加のTC/PBE仮定を用いない。Source・pair全域の結論ではない。 |
| 係数1・境界の積漸近 | `simplex_boundary_geometry.tex`, `simplex:lem:rank-one-schwarz`, `simplex:prop:dominant-product`, `simplex:cor:active-cogram` | Complete simplex模型とそのactual tripleへの適用。三重点の外の全raw-active領域へ拡張した結果ではない。 |
| 閉cornerの距離評価 | `closed_triple_metric.tex`, `simplex:thm:closed-corner-model`, `simplex:cor:actual-closed-corner-metric` | 同一tripleの三枚のsquare自身の距離（本repo `topo:coordinate-retraction` により全target距離の制限と等しい）。Sourceの内在距離と保護領域内の経路について $O(\log R_t/R_t)$。この局所結果だけでは全 $X_t$ のambient下界を結論しない。 |
| Source-free束座標と一つのprimitive | `source_free_neck_coordinates.tex`, `pair:prop:bundle-conic`, `pair:cor:global-primitive` | Source・tripleを除いた二重線 $D^\circ$ の**固定**compact base上のexact $uv=t$ とnormal action。$\Omega=d\log v\wedge\tau$、$\lambda_t=d^c\log(\omega_t^2/\lvert\Omega\rvert^2)$ を固定。本稿のmoving exhaustionは固定段階の定数を先に取り、遅い対角選択で処理する。任意の指定速度に一様な外部定理とは読まない。 |
| 共通moment interval | 同上 `pair:thm:fixed-end-moment`, `pair:cor:actual-common-moment` | Period 1のnormal generator、$\iota_V\eta_t=-d\mu_t$。固定endで $\mu_t=\pm4\pi/s_r+O(s_r^{-1-\delta})+o_t(1)$、$s_r=-\log r^2$。**先に $r$ を固定し、その後 $t\to0$**。Average $\eta_t$ の結果で、actual formへのMoser flow生存を含まない。 |
| Normal circle上界の十分条件 | `source_free_neck_comparison.tex`, `neck:lem:rank-one-circle`, `neck:cor:buffer-circle` | $p^*h_D\le A\omega_t$、$\omega_t^2\le B(h_A+h_D)^2$ からvertical方向 $g_t\le ABg_A$。Actual ball bufferを別に仮定して円の長さ $O(1/\min(s,M_t-s))$。Mixed termsを許す。この外部補題自体はbufferを与えず、必要な固定段階のbufferは本稿のK1–K2で証明する。 |
| Exterior比較 | IV `coarse:hyp:TC5`, `coarse:cor:exterior-comparison` | **TC5は未検証仮定**。各点で正しいorientationのmodelに対し $h_t^{\rm mod}\le C\omega_t$。これに依存するsource直径・connector・粗い比較を無条件化しない。 |
| 全域のGH極限 | V `hyp:CPd`, `hyp:PBEd`, `thm:degree-d-limit`; IV `ass:PBEd`, `thm:degree-d-cogram` | **CP/PBE付き**。CPはraw density、source局在、粗い二側距離とfinite connectors。PBEはterminal product座標、protected rectangular inclusion、全radiusでの一様比較、actual/model両距離のescapeとcompatible exhaustion。局所chart存在だけでは不足。 |
| Rank-one Schwarz計算と局所最大値原理 | S.-T. Yau, *A general Schwarz lemma for Kähler manifolds*, Amer. J. Math. 100 (1978), 197–203, Theorem 2・式(16)とその証明、[doi:10.2307/2373880](https://doi.org/10.2307/2373880)、[掲載版PDF](https://archive.ymsc.tsinghua.edu.cn/pacm_download/59/11034-Shing-Tung_Yau_30.pdf) | 一次PDFのTheorem 2と証明を確認。主稿の参考文献は `YauSchwarz`。本稿 `ke_sharp_normal.tex` では $\Delta\log U\ge U-1$ の係数をBochner計算から直接導き、actual球上のcutoffと全境界を明示する。局所領域にcomplete-source版の結論を無条件で適用しない。 |
| Complex Sobolev関数のGaussian可積分性 | Dinh–Marinescu–Vu, *Ann. Sc. Norm. Super. Pisa* (5) 24 (2023), 927–954, Theorem 1.2・pp.928–929、[掲載版PDF](https://www.mi.uni-koeln.de/~gmarines/PREPRINTS/Dinh_Marinescu_Vu_ASNP_2023.pdf) | 一次資料で仮定を確認。固定Euclidean領域の距離函数に適用し、固定補助potentialの測度を使う。Actual potentialの一様Hölder性は仮定しない。正規化coverの周期数を除してactual体積のGaussian tailへ移す部分は本稿で証明する。 |
| 局所potentialの連続度による距離評価 | Guedj–Guenancia–Zeriahi, [arXiv:2310.20482v1](https://arxiv.org/abs/2310.20482v1), Proposition 1.4, p.5 | 一次PDFで仮定と証明を確認。固定Euclidean領域のpotentialに一様square-root-Dini modulusがあればcoreの径は $O(1)$。本source族でのそのmodulusは**未証明**。別の条件付き十分入力として保持し、P0の証明には使用しない。 |

`multiscale-kaehler-einstein` の固定配置補空間に関する結果はIVが引用する外部入力であり、固定空間の漸近から退化族上の一様性を自動的に導かない。本更新ではそのrepoと引用一次論文の全証明を再監査していない。具体的な結果を新たに使用するときは、IVの引用箇所から一次資料の定理・仮定を確認する。

## 本repoで接続する結果

| 入力・障害 | 原稿の所在 | 使用上の区別 |
| --- | --- | --- |
| 実際のLagrangian closed corner | [ke_closed_corner_gh.tex](../papers/sections/paper/ke_closed_corner_gh.tex), `ke:closed-corner-gh`, `ke:closed-corner-protected-gh` | 同じMoser像・同じfibrationに対する局所結果。Protected distanceを全曲面距離と同一視しない。 |
| 遅いcutのclosed corner | 同上 `ke:slow-cut-closed-corner-gh` | $m\to\infty,\ \log m=o(R)$ ならdistortionは $C[m^{-1}+(\log(m+1)+\log R)/R]$。Stepwiseな対角選択可。外部のfull-triple比較、rank-one Schwarz、dominant-product比較と有限galleryを使用し、$m=R$ の定理を単に代入し直した結果ではない。 |
| 固定baseの同一moment上の接続 | [ke_staged_neck_averaging.tex](../papers/sections/paper/ke_staged_neck_averaging.tex), `ke:fixed-base-moment-connectors` | Source-freeな固定連結基底に限り、level全体とMoser像のactual ambient径 $O(1)$、正規化後 $O(R^{-1})$。異なる残余点を結ぶ。`ke:fixed-base-central-band` は固定 $A>0$ に対する $\lvert\mu\rvert\le A/M_t$ のband全体を、異なるmomentも含めactual径 $O(1)$ とする。Source・moving collar・全曲面の下界は含まない。 |
| 三armの座標・normal period | [ke_neck_corner_transition.tex](../papers/sections/paper/ke_neck_corner_transition.tex), `ke:arm-log-derivatives`, `ke:three-arm-coordinate-interpolation`, `ke:transition-normal-primitive` | 共通の許容射影を選び、固定深度比で分離したarmに限る。全固定階で指数的小摂動、積保存smooth補間、canonical normal periodの厳密一致。非正則補間帯はtame symplecticでありKähler性を仮定しない。第二periodの一致は含まない。 |
| 三端の平均順序の相対統合 | [ke_relative_corner_patch.tex](../papers/sections/paper/ke_relative_corner_patch.tex), `ke:quantitative-order-hamiltonian`, `ke:relative-corner-patch`, `ke:single-arm-reduced-graph`, `ke:arm-common-moment-strip` | 小さいprimitiveを固定し、centered平均の比較Hamiltonianを $O(m^{-2})$ で評価。Common source/imageとcutoff buffersの下で端ごとのstaged bundleを一つのactual corner bundleへ統合。単一moving armでは共通moment stripとactual reduced graphを証明。Source-inclusive neckとの共通flow領域と全交わりは、下のexhaustionの結果で別途確保する。 |
| Source-inclusive neckとcornerの全交わり | [ke_neck_corner_exhaustion.tex](../papers/sections/paper/ke_neck_corner_exhaustion.tex), `ke:fixed-stage-source-neck`, `ke:neck-corner-diagonal-matching`, `ke:neck-corner-saturated-union` | 残余compact→normal cutoff→moment区間→parameter閾値の順に選ぶ。Corner cut $6b_j$ とneckの葉でのtrim $7b_j$、first-exitと逆flow自然性により全交わりを同じ全fibersで飽和させる。Source・saddleを含む部分fibration。全曲面被覆・core・global GHは含まない。 |
| Central sourceの体積・moment・経路 | [ke_source_connectors.tex](../papers/sections/paper/ke_source_connectors.tex), `ke:source-central-density`, `ke:source-central-moment`, `ke:source-central-mean-distance`, `ke:source-central-short-escape`, `ke:source-central-arm-connectors` | 固定rescalingでdensity $L^{-2}$、有界potential、moment $O(L^{-1})$、平均二乗距離 $O(1)$、inradius $O(L^{-1/2})$、arm断面への接続 $O(1)$。Capped volume下界・oriented pair-arm density・complete volume上界を使用。全点径は結論しない。 |
| Source中央帯の全点径 | 同上 `ke:source-central-band-reduction`, `ke:source-potential-modulus` | $\lvert\mu\rvert\le A/L$ のsource中央帯を固定rescaled coreへ $O(1)$ で結ぶ。`ke:source-central-diameter` と `ke:fixed-base-source-central-band` により、固定点を含むcoreと固定基底中央帯・閉pinched torus全体のactual ambient径は $O(1)$。一様square-root-Dini modulusは**未証明**だが、Gaussian体積評価とBishop比較による証明に加え、`ke:source-direct-central-exit` のgate・arm・水平経路による直接証明がある。いずれもそのmodulusを用いない。全intervalには `ke:source-all-moment-exit` を用いる。 |
| Source-inclusive全moment退出とlevel合併 | `ke_source_all_moment_connectors.tex`, `ke:source-arm-uniform-tensor`, `ke:source-direct-central-exit`, `ke:source-all-moment-exit` | Source軸・固定点を含む全intervalで同じmomentの残余境界へ $O(1)$。三境界のrank-one Schwarz、射影下界、volume上界からarm tensor比較を導き、水平・動径経路で接続。中央点は短いgate退出を併用し、Gaussian可積分性を入力にしない。Target parameter化・全域下界は含まない。 |
| 固定残余compactの法線エネルギーと接続 | [ke_staged_neck_averaging.tex](../papers/sections/paper/ke_staged_neck_averaging.tex), `ke:neck-integrated-normal-energy`, `ke:neck-axial-upper`, `ke:neck-averaged-speed`, `ke:neck-shrinking-buffer` | KE側 `neck:prop:volume-envelope` から積分短円と同一残余点の係数1の接続上界。実計量の境界距離（上限1） $\delta_t$ が $m_t\delta_t^2\to\infty$ なら共通source・像。この十分条件と、K1–K2の固定段階で実証したbuffer・遅いexhaustionを区別する。 |
| Normal平均の双方向buffer | [ke_staged_neck_averaging.tex](../papers/sections/paper/ke_staged_neck_averaging.tex), `ke:short-circle-actual-buffer`, `ke:short-circle-image-buffer` | Actual短円とactual bufferを入力とする。像のambient直径を与えるが、$C^1$ 制御・intrinsic fiber径・base projection保存は与えない。 |
| Endsとneckの接着 | 同上 `ke:staged-neck-averaging`, `ke:staged-reduced-extension`, `ke:staged-neck-scope`; `ke_closed_corner_gh.tex`, `ke:relative-neck-matching` | 共通primitive・marked periodsを追跡できる。Reduced foliation germsの同時延長、開overlapの同じfiber partition、actual flowの生存は別に確認する。 |
| 距離の全域化 | [base_topology.tex](../papers/sections/paper/base_topology.tex), `topo:finite-portal-criterion`, `topo:portal-counterexample`, `topo:ke-map-compatibility` | (N) no-shortcut、(S) square lifts、(F) fiber/portal connectorsは別入力。(F)は(N)+(S)から従わない。現行の上界は、再parameter化後のexact square liftを仮定せず、旧cornerのendpoint距離と共通momentの接続を有限galleryに直接適用する。下界は全域scalar mapで別途証明する。 |

## 中央sourceの全点径とcomponent移送の追加入力

主稿 `ke_source_potential_buffer.tex` はcapped/actual density比較を固定source tube全体へ統合し、射影下界と正のcanonical potentialのPoisson方程式からactual球の深部局在を証明する。`ke_source_global_distance.tex` はDinh–Marinescu–Vu, Ann. Sc. Norm. Super. Pisa (5) 24 (2023), Theorem 1.2（[掲載版PDF](https://www.mi.uni-koeln.de/~gmarines/PREPRINTS/Dinh_Marinescu_Vu_ASNP_2023.pdf)、pp.928–929で仮定確認）を距離函数に適用し、logarithmic coverの周期数を除してactual Gaussian tailを得る。`ke_source_diameter.tex` は同じactual球へのBishop–Gromov比較から全点径を導く。Actual potentialのHölder性、TC、局所tensor二側比較は追加仮定しない。このGaussian経路は独立な補助結果として保持し、現行の全moment退出と中央径には `ke:source-direct-central-exit` の直接経路を使える。

`ke_component_core_transfer.tex` はfixed-gauge smooth KE収束のcanonical primitive差から固定compactのactual移送を構成する。相対flux条件とexact collar germは証明した。`ke_component_core_geometry.tex` は任意固定compactで厳密一致するsmooth正則化、正residueの有限型KE coreとその小さい飽和近傍のfillingを与えるが、その存在だけから全collar葉の一致は従わない。現行の全域接着は下記四節によりactual linkから直接構成する。Smooth compactifying formの `comp:finite` をこの極限形式の定理と読み替えない。


Actual全域構成の追加証明は次を用いる。

| 入力・結論 | 主稿の節・ラベル | 検証範囲 |
| --- | --- | --- |
| 正residue period、閉link、固定段階の被覆とtrim | `ke_component_link_cover.tex`、`ke:component-meridian-normalization`、`ke:closed-component-link`、`ke:fixed-stage-stratum-coverage`、`ke:whole-fiber-core-trim` | Cornerのdominant-productは全深度比に一様。Source基底点を含むfixed-shell上界はRZの通常component cusp上で証明。整数windingとexact transportでmoment定数も同定。 |
| Actual invariant primitive | `ke_core_invariant_primitive.tex`、`ke:component-normal-generator-c1`、`ke:relative-corner-patch-c2`、`ke:component-shell-primitive-support` | RZの全cusp derivatives、triple全固定階比較、広いK2 construction domainsを使用。追加の全域tensor仮定なし。 |
| Saddle-moving relative family | `ke_relative_reduced_foliations.tex`、`ke:saddle-moving-relative-interpolation` | 各connected critical leafに一つのsimple saddle、boundaryのleaf partition固定。Global vector fieldの直接証明。非零moment bandのactual Lagrangian lift。 |
| 全域core接着 | `ke_actual_core_gluing.tex`、`ke:actual-global-fibration` | Evans–Mauri Lemma 2.16のcompact-domain版と上記入力。全曲面の連結fiberの全射とactual Lagrangian性、各componentごとの固定compact費用を与える。Uniform distortionは下の上下界と組み合わせて得る。 |
| Core cutのtarget cap | `ke_actual_core_gluing.tex`、`ke:core-depth-upper`、`ke:removed-corner-target-cap` | 固定成分のstrict psh potential・graph convergence・旧softmax逆式。各capは成分頂点へ一様収縮。保持cornerの旧protected距離と全曲面距離の上界を維持。全域parameterizationとambient下界は含まない。 |
| 全域基底parameter化と内部木の共通moment | `ke_global_base_compatibility.tex`, `ke:common-edge-moment-profile`, `ke:corner-cap-disk`, `ke:global-base-parameterization`, `ke:collapsed-tree-common-moment` | Weighted moment inverse、moment-cut capのproper arc、明示insetとstrip補間で全保持cornerの旧値へ $O((1+\log N_j)/R_t)$ 近接。内部木の中央部分では全枝共通momentを厳密に保つ。全曲面距離下界を含まない。 |
| Sourceを含む係数一の法線評価 | [ke_sharp_normal.tex](../papers/sections/paper/ke_sharp_normal.tex), `ke:normal-harmonic-depth-barrier`, `ke:sharp-scalar-normal-barrier`, `ke:sharp-global-one-active` | 正則global normal frameで $\Delta s=0$、$U=\lvert d\log s\rvert^2$ に $\Delta U\ge U(U-1)$。固定shell・moving shell・残余境界の全てを評価し、$1+\varepsilon_j+A_j\mathfrak n_j/s+C_js/(\kappa L)$ の障壁を使う。Source軸、physical-depth補正、triple外のactive全被覆を含む。SharpなRZ漸近や全neck tensor比較を追加仮定しない。 |
| 全域scalar mapとambient下界 | [ke_global_ambient_lower.tex](../papers/sections/paper/ke_global_ambient_lower.tex), `ke:global-depth-lipschitz`, `ke:global-depth-base-comparison`, `ke:global-ambient-lower` | 下側cut $\mathfrak m_j$ とplateau $L/K_j$ を用いる全域 $\Theta_t$。一方向はsharp normal、二方向はfull-tripleのco-Gramで評価し、任意の全曲面経路に沿って長さを抑える。同じ $f_t$ との全域値比較を証明。経路の領域往復回数を有限と仮定しない。 |
| 内部木の全fiber合併とambient上界 | [ke_global_ambient_upper.tex](../papers/sections/paper/ke_global_ambient_upper.tex), `ke:collapsed-tree-full-fiber-collapse`, `ke:coherent-corner-portals`, `ke:global-ambient-upper` | 全 $f_t$-fiberのambient径を $C_j$ で評価。全endsで同じmomentのportalsを選び、旧full-cornerのendpoint上界を高々60本のsquare galleryで接続する。除去capを通る曲線もambient上界には使用できる。 |
| 同じactual写像による大域実現 | [ke_global_metric_realization.tex](../papers/sections/paper/ke_global_metric_realization.tex), `ke:global-metric-realization` | 上記の同じ $\pi_t$ と $f_t=p_T\pi_t$ に、全固定段階の条件を満たす一つの遅い対角選択を適用。全射性、uniform ambient distortion消失、GH収束、全fiber合併の一様収縮を得る。外部CP/PBE/TCの結論を入力にしない。 |

## 固定成分coreのcusp入力と有限target幾何

Rochon–Zhang, *Adv. Math.* 231 (2012), 2892–2952, [arXiv:1106.0873v2](https://arxiv.org/abs/1106.0873v2), §5 (5.3)–(5.6), Theorem 5.1を一次資料で確認した。SNC全体におけるbounded $C^\infty_{fc}$ potentialを用い、smooth divisor専用のfull expansionは使わない。$K_{\mathbf P^2}+D=\mathcal O(d-4)$ のamplenessと本稿の $dd^c=i\partial\bar\partial$ を照合し、$u=-2\sum\log s_a+v$ を使用する。正則化・有限型性・compact exact Moserと局所core fillingの証明は本repoの `ke_component_core_geometry.tex` が正本。

`topo:coordinate-retraction` によりclosed-cornerのtargetの内在距離は全複体距離の制限と等しい。六labelのgallery還元と `topo:diameter-six-labels` の $D_d=2\sqrt5$（d≥6）は解析仮定から独立。直径対の線形安定性 `topo:diameter-six-stability` だけはVの `thm:intro-diameter-C5`・`sec:finite-diameter`（確認commitは上記と同じ）の $D_5=\sqrt{13}$ を使用する。四galleryと120三角形は本repoの保存された有理数検算により確認されている。現行のuniform distortionと全射性からactual曲面の正規化直径も $D_d$ へ収束する。具体的な数値 $D_5=\sqrt{13}$ の適用には上記五次の有限target距離結果を用いる。

## 大域実現を支える接続とパラメータの選択

### 1. Actual normal circleとflowの共通領域

固定 compact の source-free 基底で normal 深度だけを動かす場合は、主稿 `ke:fixed-base-neck-moser` で解決した。$\Omega_{t,d}^{\rm low}$ の大域下界、capped background の射影下界、固定 pair chart の体積上界を使い、射影包含の大域 Chern–Lu と actual ball 上の局所 Chern–Lu を順に適用する。共通の縮小 moment interval は `ke:neck-deep-moment-strip`。遅いresidual exhaustionの束座標・共通flow領域は `ke:neck-corner-diagonal-matching` で確保した。任意に指定した縮小速度への一様性は主張しない。Source gate 近くでは射影距離による buffer を rescaled normal 距離へ読み替えない。 Source 模型では `coarse:lem:pair-arm-density` と `coarse:lem:complete-volume-upper` を oriented 側に使い、正則ベクトル場の Bochner 不等式で central source まで法線生成場の $O(L_t^{-1})$ 評価を得た（`ke:source-short-circle`）。

### 2. 同じglobal fibrationへの相対接着

`ke:actual-global-fibration` により固定stageの全域接着を証明した。K2の全intersection saturationを入力とし、閉moment link・actual invariant primitive・非零moment帯のsaddle-moving補間・whole-fiber trimを実証する。全曲面被覆はfixed-shellの上界と同じnormal flowの逆像bufferを使い、部分fibrationの外を各componentの固定compactへ閉じ込める。各componentのcoreと変更collarのactual ambient径・選択した接続費用は $C_j<\infty$ であり、遅い対角選択で $C_j/R_t\to0$ とできる。独立に先指定した全periodやcritical valuesを合わせる定理ではない。Actual Lagrangian性と連結fiberの全射を、次の距離評価の前に確保している。

### 3. 全曲面のscalar下界

Sharp normal比較領域は、sourceを除かない固定残余compact上の正則annulus bundleである。固定した $\kappa>0$ に対する $s=\kappa L$ の粗い上界は、独立に証明したsource-arm tensor比較で供給する。その前段はpositive-Poisson bufferとlocalized rank-one Schwarzであり、global scalar障壁へ依存しない。残余境界はfull-triple、固定外側shellは射影下界と座標微分の上界を用いる。全境界を明示した最大値原理により

\[
|d\log s|_{g_t}^2
\le1+\varepsilon_j+A_j\mathfrak n_j/s+C_js/(\kappa L)
\]

を得る。比較領域の境界 $\kappa L$ と、clipped mapのplateau $L/K_j$ は異なる。新しい下側cut $\mathfrak m_j$ は旧corner cut $m_{\mathrm{old}}=6b_j$ と独立であり、全固定段階の定数と非成分深度の上界を決めてから選ぶ。

Global Hermitian depthsを $\ell_i=-\log\|L_i\|^2$ とし、

\[
\Theta_{i,t}
=\left[\frac{\log(\ell_i/\mathfrak m_j)}
 {R_t-\log\mathfrak m_j-\log K_j}\right]_0^1
\]

とする。少なくとも一座標が1、非零座標は高々三つなので、active covectorsは高々二本である。一active方向はsharp normal、二active方向はfull-tripleのdominant-product co-Gramで制御する。この全域微分評価を任意のrectifiable curveに積分するため、neck・corner・coreの往復回数に比例する誤差は生じない。先に $\Theta_t$ の全域Lipschitz評価を証明し、それをMoser前後の比較に使う。共通moment profileとcore cap制御により $\sup_xd_\square(\Theta_t(x),f_t(x))\to0$ を得て、同じ $f_t$ のambient下界へ移す。

### 4. 共通momentの全fiber合併と上界

保持cornerの旧softmaxと全域の $p_T\pi_t$ の値の整合は `ke:global-base-parameterization` による。Core capの位置だけでなく、moment profileとcap境界のproper arcを用いる。潰される内部木では全枝に同じlongitude $\sigma_t(\mu)$ を使うので、辺の中央値の逆像は厳密に同一moment上の全fiber合併である。

Source側では中央全点径と共通interval全体の同一moment退出がともに $O(1)$。`ke:source-arm-uniform-tensor` は三境界のnormal covector評価とvolume上界からsource軸を含むarmの二側比較を与え、`ke:source-all-moment-exit` は水平・動径の直接経路で証明する。中央固定点には短いgate退出を先に用いるため、この接続はDMV/Gaussianに依存しない。固定source-free基底の接続と各componentのcore・変更collarの費用を合わせ、全 $f_t$-fiberのambient径は $H_{j,t}=C_j$ で抑えられる。Gaussian体積定理は有効な独立補助結果として保持する。

Target最短路は `topo:six-label-gallery` により高々60本のsquare線分で選べる。各junctionに同じnormal momentのcorner portalsを取り、旧full-cornerのambient endpoint上界と $H_{j,t}$ を有限回足す。これはtarget最短路に対する有限galleryの使用であり、sourceの任意の経路の出入り回数を制限する議論ではない。再parameter化後の $f_t$ に厳密に写るsquare liftsは要求しない。

### 5. 一つの遅い対角選択

固定 $j$ ごとに $b_j$、残余compacts、K2のnormal cutoff $n_j$、共通moment区間、$N_j$、core・collarを決める。その後、sharp barrier専用の補助cut $\mathfrak n_j$ と境界定数 $A_j,C_j$、有限費用を全て確定する。$\mathfrak n_j$ は $n_j$ と独立であり、既存のcoreや $N_j$ を選び直さない。最後に $\mathfrak m_j$、$K_j$ を大きく選び、$t_j$ を小さくする。$\varepsilon_j\to0$、$b_j,\mathfrak m_j,K_j\to\infty$ とし、全固定段階の定数を含む

\[
\frac{C_j(1+\log\mathfrak m_j+\log K_j+\log(N_j+1))}{R_t}\longrightarrow0
\]

を課してよい。これにより上下界、各componentの費用、全fiber合併径を同じ $j(t)$ と同じ $f_t$ で制御する。固定triple内の $O(\log R_t/R_t)$ をそのまま大域の収束速度とする主張ではない。

## 主要な外部解析入力の重点監査

以下は本稿の接続に必要な証明を読み合わせた範囲であり、外部主稿全体の独立再検証を意味しない。

1. **Capped volume下界。** IV `coarse:cor:degree-d-volume-lower` のadjunction規格化、smooth Hermitian frameの誤差吸収、六種類の局所determinant下界を点検した。Sourceでは射影Morse座標だけに置き換えず、元のplane coordinatesのcap項を保持して、rescaling後の二方向の係数が $c/L$ 以上になることを使う。正のminorの和なので相殺は起こらない。これをcompact minimum原理へ入れる順序であり、先にactual tensor比較を要求しない。
2. **Full-triple比較の最小入力。** `full_triple_comparison.tex` の `coarse:rem:full-triple-face-input` に、固定深度 $m_0$ の境界面全phaseでの $\omega_t^2\ge c_*V_L$ がvolume障壁の下側に十分なことを明記した。固定 $t$ のradial closureと角度torusはexact triple chart内でcompactである。拡大simplexが下側、縮小simplexが上側の障壁となり、後者は人工境界で発散する。深部内部全体のdensity floor、actual距離buffer、actual metricの完備性をこの段階で入力にしない。$v=\log(\omega_t^2/k_L^2)$ と $dd^cv=\omega_t-k_L$ の同じRicci規格化も照合した。
3. **Small perturbationからtensor比較へ。** O. Savin, *Comm. Partial Differential Equations* 32 (2007), 557–578, Theorem 1.3・§4 Proposition 4.1、[掲載版PDF](https://www.math.columbia.edu/~savin/Small_pert.pdf)、[doi:10.1080/03605300500394405](https://doi.org/10.1080/03605300500394405) を一次資料で確認した。Complete模型のcoarse tensor下界は半平面へのSchwarz、上界はdeterminant比較から先に得る。全深度比のnormalized windowsで模型係数の高階評価を確保した上で、determinant作用素の単調な拡張、零近傍の一様楕円性と $C^2$ bound、$\|v\|_{C^0}=O(m^{-1})$ を照合した。Small $C^{2,\alpha}$ の後にbootstrapと線形化を使って $C^q$ 誤差 $O(m^{-1})$ に進む。模型側のdominant-product squeezeとfacet幅 $\beta=(b^2d_*)^{1/3}$ も点検し、active co-Gramの係数1がこの順序で得られることを確認した。
4. **Complete volume上比較。** IV `coarse:lem:complete-volume-upper` の一般形は $u=\log((\pi_D^*\omega_t)^2/h^2)$ の $\sup_Du<\infty$ を仮定する。Ricci下界から使えるLaplacian型最大値原理とAM–GMにより $\Delta_hu\le\epsilon$ の点で $e^u\le(1+\epsilon/2)^2$、従って $\omega_t^2\le h^2$ となる。Hessian型原理や、完備性だけによる $u$ の上有界性は用いない。実際のfinite ball・annulus–disc・product windowsとangular coversでは、固定 $t$ のclosureへの延長、model densityの境界発散、deck周期性を各適用で確認した。この点は外部正本の一般形にも反映してある。
5. **Component極限とSNC cusp。** Song [arXiv:1706.01518](https://arxiv.org/abs/1706.01518) のDefinition 2.3・Lemmas 4.4–4.5と、Rochon–Zhang [arXiv:1106.0873v2](https://arxiv.org/abs/1106.0873v2) §5 (5.3)–(5.6)・Theorem 5.1を一次資料で照合した。Total-space source $xy+tz=0$ のcanonical特異点、stable family、$K_{\mathbf P^2}+D=\mathcal O(d-4)$ のampleness、fixed-gauge収束を区別する。SNC上の $x^\nu C^\infty_{fc}$ remainderとradial cusp微分から固定endのmoment漸近を得ており、smooth divisor専用のfull polyhomogeneous expansionは使わない。本稿の新しいsource-arm tensor比較とscalar外側境界はこのcomponent収束を使わないが、core移送等の既存入力から除いたわけではない。

Complete simplex模型の存在はZhang [arXiv:1505.04728v2](https://arxiv.org/abs/1505.04728v2) Theorem 2.1・Proposition 2.2を一次資料で確認した。同Theorem 2.1が引用するCheng–Yau (1982), Theorem 4.4の原論文の証明そのものは今回再精読していない。Zhangの退化族に関するTheorem 2.4のQ-factorial仮定をsourceを持つ本族に適用してはいない。DMVのTheorem 1.2についても、固定Euclidean補助測度、正閉current、$L^2$ 規格化、周期coverの個数とBishop比較の実次元4を照合した。ただし現行の有界source退出はこのGaussian経路から独立である。

## 今回の内部点検と残る確認範囲

- K2–K3の接続に必要な全intersection saturation、fixed-stage stratum coverage、whole-fiber trim、actual Lagrangian性、compact Hausdorff quotientへの全射とconnected fibers、固定 $d\ge5$ の範囲、core・変更collarの固定compact費用を点検した。
- 新しい中央 $O(1)$ 径、全moment source退出、sharp scalar barrier、global physical-depth補正とactive cover、全域co-Gramと $\Theta_t$–$f_t$ 比較、共通moment portals、全fiber合併、有限gallery上下界を、作成担当以外の読み手が内部点検した。特に全境界、source軸、同じcanonical moment、依存の非循環性、固定段階から遅い対角選択への順序を照合した。
- YauのTheorems 1–2、Savinのsmall perturbation、Songのfixed-gauge収束、DMVの掲載版Theorem 1.2、Rochon–ZhangのSNCに関する指定箇所は一次資料で確認した。外部KE原稿の全証明や旧主稿全体の独立再監査、公表前の網羅的な先行研究・新規性調査、形式証明を完了したという意味ではない。
- 解析証明の数学的点検、保存された有限有理数検算、その再実行、組版、GitHubへの反映は別の確認である。各実行状態は現行の検証資料を参照し、本書の「証明あり」を計算・組版による証明の検証と読み替えない。

## 再開時の確認

外部repoの最新 `main`、AGENTSと方針を確認し、上表のラベルの存在と追加仮定を照合する。未取得・アクセス不能なら、確認済みコミットと未確認範囲を残し、利用可能な独立課題を進める。解析的結果を外部repoへ追加した場合は、そちらを先に保存してから、この表の参照版と本repoの依存箇所を更新する。外部入力の更新・本repoでの適用証明・組版・計算検証は別々に記録する。
