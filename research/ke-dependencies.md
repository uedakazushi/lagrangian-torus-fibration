# KE–fibration 大域実現の依存関係

2026-11-21 / v1.2。目標・優先順位は [研究方針](../00_research_plan.md)、数学的な目標の定式化は主原稿の `ke:global-realization-section` 節を正本とする。本書は外部入力の所在・適用範囲と、次に証明すべき接続条件を保持する。

## 確認した正本と規格化

関連する [kaehler-einstein-degeneration](https://github.com/uedakazushi/kaehler-einstein-degeneration) の確認コミットは `74ba687f67e1f87a4d308bf868fcdef98db441df`。以下の **IV** は同repoの [papers/kaehler-einstein-degeneration.tex](https://github.com/uedakazushi/kaehler-einstein-degeneration/blob/74ba687f67e1f87a4d308bf868fcdef98db441df/papers/kaehler-einstein-degeneration.tex)、**V** は [papers/cubical-gh-limit.tex](https://github.com/uedakazushi/kaehler-einstein-degeneration/blob/74ba687f67e1f87a4d308bf868fcdef98db441df/papers/cubical-gh-limit.tex) を表す。外部の分割原稿は同repoの `papers/sections/` にある。この確認版を固定した参照として保持し、再開時に最新 `main` と比較して、訂正・追加仮定を優先する。外部原稿本文をこのrepoへ複製しない。

今回確認したのは、該当する定理文・証明の所在・依存仮定・規格化である。下表の「証明あり」は原稿の状態を表し、全証明の独立再監査・形式証明・一次文献の再精読・組版の再実行を意味しない。本repoの参照元は分割後の `0cfab9239636739899859c9657c01a7dcff54b8c` と照合した。

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

## 外部解析入力の状態

| 入力 | 正本・ラベル | 適用範囲と残る条件 |
| --- | --- | --- |
| 全次数のcapped volume下界 | IV `coarse:cor:degree-d-volume-lower` | 固定 $d\ge5$、`ass:Gd` の下で証明あり。体積比からtensor二側比較を推論しない。 |
| 全深部tripleのactual/model比較 | `full_triple_comparison.tex`, `coarse:thm:full-triple-tensor` | $m_1\le m<L_t/3$、$\min\ell_i\ge m$ で全phase・全深度比に $C^q$ 誤差 $O_d(m^{-1})$。追加のTC/PBE仮定を用いない。Source・pair全域の結論ではない。 |
| 係数1・境界の積漸近 | `simplex_boundary_geometry.tex`, `simplex:lem:rank-one-schwarz`, `simplex:prop:dominant-product`, `simplex:cor:active-cogram` | Complete simplex模型とそのactual tripleへの適用。三重点の外の全raw-active領域へ拡張した結果ではない。 |
| 閉cornerの距離評価 | `closed_triple_metric.tex`, `simplex:thm:closed-corner-model`, `simplex:cor:actual-closed-corner-metric` | 同一tripleの三枚のsquare自身の距離。内在距離と保護領域内の経路について $O(\log R_t/R_t)$。全 $X_t$ のambient距離は未処理。 |
| Source-free束座標と一つのprimitive | `source_free_neck_coordinates.tex`, `pair:prop:bundle-conic`, `pair:cor:global-primitive` | Source・tripleを除いた二重線 $D^\circ$ の**固定**compact base上のexact $uv=t$ とnormal action。$\Omega=d\log v\wedge\tau$、$\lambda_t=d^c\log(\omega_t^2/\lvert\Omega\rvert^2)$ を固定。Moving baseへの一様性は未証明。 |
| 共通moment interval | 同上 `pair:thm:fixed-end-moment`, `pair:cor:actual-common-moment` | Period 1のnormal generator、$\iota_V\eta_t=-d\mu_t$。固定endで $\mu_t=\pm4\pi/s_r+O(s_r^{-1-\delta})+o_t(1)$、$s_r=-\log r^2$。**先に $r$ を固定し、その後 $t\to0$**。Average $\eta_t$ の結果で、actual formへのMoser flow生存を含まない。 |
| Normal circle上界の十分条件 | `source_free_neck_comparison.tex`, `neck:lem:rank-one-circle`, `neck:cor:buffer-circle` | $p^*h_D\le A\omega_t$、$\omega_t^2\le B(h_A+h_D)^2$ からvertical方向 $g_t\le ABg_A$。Actual ball bufferを別に仮定して円の長さ $O(1/\min(s,M_t-s))$。Mixed termsを許す。Buffer自体は未解決。 |
| Exterior比較 | IV `coarse:hyp:TC5`, `coarse:cor:exterior-comparison` | **TC5は未検証仮定**。各点で正しいorientationのmodelに対し $h_t^{\rm mod}\le C\omega_t$。これに依存するsource直径・connector・粗い比較を無条件化しない。 |
| 全域のGH極限 | V `hyp:CPd`, `hyp:PBEd`, `thm:degree-d-limit`; IV `ass:PBEd`, `thm:degree-d-cogram` | **CP/PBE付き**。CPはraw density、source局在、粗い二側距離とfinite connectors。PBEはterminal product座標、protected rectangular inclusion、全radiusでの一様比較、actual/model両距離のescapeとcompatible exhaustion。局所chart存在だけでは不足。 |

`multiscale-kaehler-einstein` の固定配置補空間に関する結果はIVが引用する外部入力であり、固定空間の漸近から退化族上の一様性を自動的に導かない。本更新ではそのrepoと引用一次論文の全証明を再監査していない。具体的な結果を新たに使用するときは、IVの引用箇所から一次資料の定理・仮定を確認する。

## 本repoで接続する結果

| 入力・障害 | 原稿の所在 | 使用上の区別 |
| --- | --- | --- |
| 実際のLagrangian closed corner | [ke_closed_corner_gh.tex](../papers/sections/paper/ke_closed_corner_gh.tex), `ke:closed-corner-gh`, `ke:closed-corner-protected-gh` | 同じMoser像・同じfibrationに対する局所結果。Protected distanceを全曲面距離と同一視しない。 |
| 固定残余compactの法線エネルギーと接続 | [ke_staged_neck_averaging.tex](../papers/sections/paper/ke_staged_neck_averaging.tex), `ke:neck-integrated-normal-energy`, `ke:neck-axial-upper`, `ke:neck-averaged-speed`, `ke:neck-shrinking-buffer` | KE側 `neck:prop:volume-envelope` から積分短円と同一残余点の係数1の接続上界。実計量の境界距離（上限1） $\delta_t$ が $m_t\delta_t^2\to\infty$ なら共通source・像。所要のcollarでの境界距離下界とmoving residual baseへの拡張が残る。 |
| Normal平均の双方向buffer | [ke_staged_neck_averaging.tex](../papers/sections/paper/ke_staged_neck_averaging.tex), `ke:short-circle-actual-buffer`, `ke:short-circle-image-buffer` | Actual短円とactual bufferを入力とする。像のambient直径を与えるが、$C^1$ 制御・intrinsic fiber径・base projection保存は与えない。 |
| Endsとneckの接着 | 同上 `ke:staged-neck-averaging`, `ke:staged-reduced-extension`, `ke:staged-neck-scope`; `ke_closed_corner_gh.tex`, `ke:relative-neck-matching` | 共通primitive・marked periodsを追跡できる。Reduced foliation germsの同時延長、開overlapの同じfiber partition、actual flowの生存は別に確認する。 |
| 距離の全域化 | [base_topology.tex](../papers/sections/paper/base_topology.tex), `topo:finite-portal-criterion`, `topo:portal-counterexample`, `topo:ke-map-compatibility` | (N) no-shortcut、(S) square lifts、(F) fiber/portal connectorsは別入力。(F)は(N)+(S)から従わない。Base上の原理を $X_t$ へ用いる際は、選んだ距離と持ち上げ・接続条件を別途証明する。 |

## 最初に閉じる三つの証明課題

### 1. Actual normal circleとflowの共通領域

固定 compact の source-free 基底で normal 深度だけを動かす場合は、主稿 `ke:fixed-base-neck-moser` で解決した。$\Omega_{t,d}^{\rm low}$ の大域下界、capped background の射影下界、固定 pair chart の体積上界を使い、射影包含の大域 Chern–Lu と actual ball 上の局所 Chern–Lu を順に適用する。共通の縮小 moment interval は `ke:neck-deep-moment-strip`。次は residual base を動かす場合の束座標の有効範囲と計量評価である。Source gate 近くでは射影距離による buffer を rescaled normal 距離へ読み替えない。 Source 模型では `coarse:lem:pair-arm-density` と `coarse:lem:complete-volume-upper` を oriented 側に使い、正則ベクトル場の Bochner 不等式で central source まで法線生成場の $O(L_t^{-1})$ 評価を得た（`ke:source-short-circle`）。

### 2. 同じglobal fibrationへの相対接着

第一課題で得た一つのnormal actionとprimitiveを用い、各triple collarの二段階平均、reduced circle foliation、critical actionsとmarkingを同時に合わせる。非定数holomorphic unitはfull $T^2$-orbit partitionを変え得るため、整数基底変更だけで処理しない。Sourceの $xy=tz$、branch、coreを含む全域へactual $\omega_t$-Lagrangian fibrationを延長し、使用した相対isotopyのraw map誤差または $g_t$-変位 $o(R_t)$ を明記する。単なる同じcohomology classやMoser同相はGH適合の証明にならない。

### 3. 全曲面の距離歪みとportal費用

選んだ $f_t=p_T\pi_t$ に対し、全 $X_t$ の経路を許した距離について

\[
\sup_{x,y\in X_t}
\bigl|R_t^{-1}d_{g_t}(x,y)-d_\square(f_t(x),f_t(y))\bigr|\longrightarrow0
\]

を証明する。二つの経路がある。(a) CP/PBEの未解決入力を対象族で証明し、Vの近似写像 $\Psi_{t,A(t)}$ に対する $\sup_xd_\square(\Psi_{t,A(t)}(x),f_t(x))\to0$ を示す。(b) $f_t$ へ直接、scalar no-shortcut下界とsquare lifts・portal connectorsによる上界を示す。後者が十分ならCP/PBEという強いpackage全体の証明を必須にしない。いずれも全source・singular fibersを含む。$d\ge6$ では $p_T^{-1}(c)$ に属する複数の $\pi_t$-fibersの**合併全体**の収縮が必要である。固定triple内の $O(\log R_t/R_t)$ をそのまま大域の率としない。

## 再開時の確認

外部repoの最新 `main`、AGENTSと方針を確認し、上表のラベルの存在と追加仮定を照合する。未取得・アクセス不能なら、確認済みコミットと未確認範囲を残し、利用可能な独立課題を進める。解析的結果を外部repoへ追加した場合は、そちらを先に保存してから、この表の参照版と本repoの依存箇所を更新する。外部入力の更新・本repoでの適用証明・組版・計算検証は別々に記録する。
