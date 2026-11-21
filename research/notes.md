# 現行研究ノート：一般型曲面のLagrangian torus fibration
更新：2026-11-21 / v3.4

主稿 `papers/surface-lagrangian-torus-fibration.tex` と整数接着 `papers/quintic-integer-gluing.tex` を正本とする。以下は曲面・KE局所幾何・作用・アフィン接着に関する現在有効なノート。三次元の原稿と相対円板群・補集合の計算は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) を正本とし、こちらに重複保持しない。

## 全域実現定理と現在の点検範囲

主稿 `ke:global-realization` と統合証明 `ke:global-metric-realization` は、任意の固定 $d\ge5$ と既存一般性条件の全平面退化について、actual負KE形式の全域fibrationと、同じ $f_t=p_T\pi_t$ の全曲面ambient距離に関するdistortion消失を与える。潰される内部木上の全fiber合併も一様に収縮する。**原稿に証明があり、今回の新証明と接続を複数担当で内部点検した。** 形式証明、全主稿・全外部入力の包括的再監査、外部査読、網羅的な新規性確認は未実施である。現在は公表に向けた一次文献・依存結果・主稿構成の点検を優先する。

対象・結論の範囲と優先順位は [研究方針](../00_research_plan.md)、外部定理のpath・label・確認commitは [KE依存表](ke-dependencies.md) を参照する。ここには証明全文を複製せず、核心、入力の区別、有効な障害を残す。十分遅い対角選択と一つの許容された木系を使う結論であり、最適rate、任意の先指定木系への適合、全次数のmatroidal atlasは含まない。

## 主要解析入力の確認範囲

Capped volume下界の六型determinant、full-triple比較の固定境界面でのdensity下界、模型側SchwarzとSavinの小摂動定理、Songのfixed-gauge収束、Rochon–ZhangのSNC remainderを重点点検した。一般のcomplete volume上比較では、対数体積比の上有界性を明示し、Ricci下界から得るLaplacian型最大値原理とAM–GMで証明する。有限窓・angular coverでの実適用は、固定parameterのcompact closureとmodelの境界発散からこの上有界性を確認する。外部正本にも同じ仮定を明記した。定理ラベル・一次資料・監査の限界は [KE依存表](ke-dependencies.md#主要な外部解析入力の重点監査) にまとめる。Cheng–Yau (1982)原論文の証明の再精読、全旧証明・全先行研究の包括的確認は未了である。

## Sourceを含むsharp scalar評価から全曲面の下界へ

正本は `papers/sections/paper/ke_sharp_normal.tex` と `ke_global_ambient_lower.tex`。正則global normal frameで $s=-\log|x'_g|^2$、$U=|d\log s|_{g_t}^2$ とすると、$\Delta s=0$ とrank-one Bochner計算から $\Delta\log U\ge U-1$ を得る。Source-inclusive方程式 $x'_gy'_g=th_t(p)$ に対し、$\mathfrak n_j\le s\le\kappa L$ の比較領域は $h_t(p)=0$ でもannulusと固定残余compactの積であり、sourceを除く人工境界を必要としない。

補助cut $\mathfrak n_j$ は、neck/corner構成の $n_j$ とは独立の記号とする。三種類の境界を分ける。残余境界は既存full-tripleの係数1評価、外側固定shellは射影下界と固定座標微分からの有限上界 $A_j$、内側 $s=\kappa L$ は既証のsource-arm tensor比較による有限上界 $C_j$ を使う。Arm比較はpositive-Poisson bufferとlocalized Schwarzから独立に得られ、このscalar障壁を入力にしない。明示的な障壁
\[
 B(s)=1+\varepsilon_j+A_j\mathfrak n_j/s+C_js/(\kappa L)
\]
が `ke:sharp-scalar-normal-barrier` の中心である。外側でsharp cusp漸近を仮定せず、下側clipを後から十分深くして $A_j\mathfrak n_j/s$ を吸収する。残余frameのbase-only差とMorse変換の $O(t)$ 誤差は、active上側cut $s\le L/K_j$ と $K_j>4$ の下でphysical depthへ転送する（`ke:sharp-global-one-active`）。

旧corner cut $6b_j$ と独立に $\mathfrak m_j\gg A_j\mathfrak n_j/\varepsilon_j,N_j$、$K_j\gg C_j/(\kappa\varepsilon_j)$ を選び、最後に $\log\mathfrak m_j+\log K_j=o(R_t)$ とする。Global clipped map
\[
 \Theta_{i,t}=\left[\frac{\log(\ell_i/\mathfrak m_j)}{\log((L/K_j)/\mathfrak m_j)}\right]_0^1
\]
には少なくとも一つのplateauがあり、active方向は高々二つ。二方向はfull-tripleのdominant-product比較、一方向は上のscalar評価で扱う。`ke:global-depth-lipschitz` は全曲線に対する長さ評価を先に与え、領域間の往復回数に依存しない。

`ke:global-depth-base-comparison` は、cornerの旧softmaxとcoreの頂点値を比較し、neckでは `ke:same-moment-corner-reference` の参照torusへ値比較を移す。固定残余基底を全marked tree・source discs・旧corner辺の残余像を含むよう先に選ぶ。旧辺は $B=6b_j+r_c$, $0\le r_c<1$ なので、この選択はcomponent cut $N_j$ に依存しない。各保持neck点 $x$ には同じcanonical momentを持つ旧corner辺の任意の点 $y$ があり、既証のsource-inclusive同一moment接続から $d_{g_t}(x,y)\le C_j^{\rm neck}$。従って、$\Lambda_{j,t}=\sqrt{1+\epsilon_{j,t}}/S$ として
\[
 d_\square(\Theta_t(x),f_{j,t}(x))
 \le \Lambda_{j,t}C_j^{\rm neck}
   +d_\square(\Theta_t(y),f_{j,t}(y))
   +C\eta_{j,t}.
\]
最後の項は両点で同じmoment profileを使うことによる。これは点の選択であり、torus bundleの大域sectionを仮定しない。経路はfiber又はmoment levelの内部に留まらなくてよい。Source固定点・軸・pinched fiber・saddle fiberも同じ集合に含まれる。

依存順序は、局所的なsource退出と同一moment接続、全曲線での $\Theta_t$ のLipschitz評価、cornerでの値比較、全neckへの移送、同じ $f_t$ の距離下界である。全域上界やGH収束を参照点の存在・費用に使わない。`ke:fixed-base-neck-moser` と `ke:fixed-base-moment-connectors` は、固定残余近傍に依存する有限下限 $m_P$ 以上の全cutに一様であることを定理文に明示する。正の固定bufferと $C_P/m$ の短円評価を用いるので、固定stageを先に選んでから $t\to0$ とする用途に適用できる。

`ke:common-profile-log-depth` の $\sigma_t(\mu)=\log(1/|\mu|)/R$（向きにより $2-$ を付ける）という解釈も保持する。直接の座標比較を要する用途では、`ke:source-arm-moment-depth` の $s\asymp_j|\mu|^{-1}$、中央帯の $s_x,s_y\ge\kappa_jL$、projected coordinatesの $O(t)$ 差を使える。全域値比較自体は上の参照torusによる移送で証明する。CP/PBE/TC全体を証明したのではなく、本稿の下界に必要な入力を直接与える。

## Portal上界と潰される木の全fiber合併

正本は `papers/sections/paper/ke_global_ambient_upper.tex`。`ke:global-ambient-upper` は、保持corner内の旧経路を全曲面の経路として用い、同一momentのneck接続、source退出、各componentの固定stage費用を有限のtarget galleryでつなぐ。保持corner自体の新しい内在距離評価は要求しない。対象ごとに固定した有限定数は最後の遅い対角選択で $o(R_t)$ とする。

`ke:collapsed-tree-common-moment` により、辺内点での $p_T$-fiberは同じcanonical moment上の内部木全体である。`ke:collapsed-tree-full-fiber-collapse` は一つのtorusだけでなく、その木上の全 $\pi_t$-fibersの合併を評価する。Sourceの中央帯・非中央armとcore側endpointを含めてこの評価を行い、全域上下界を `ke:global-metric-realization` へ統合する。経路がfiber又はmoment level内に留まるという主張ではない。

## 有限の飽和全被覆でも局所加法誤差だけでは足りない

有効な障害として `ke:full-cover-oscillating-bypass` を `ke_global_ambient_lower.tex` に保持する。Rectangle上の計量を $g_N=dy^2+a_N(x,y)^2dx^2$ とし、上下の薄い列で $a_\pm(x)=1\pm c\sin(2\pi Nx)$、中央帯の幅を $h_N=N^{-3}$、係数を $1+c$ とする。上下各半分ではprimitive $A_\pm(x)=\int_0^xa_\pm$ により局所intrinsic/protected distortionは $O(N^{-1})$、恒等写像のfibersは一点である。しかし安い側を周期ごとに選ぶ経路の長さは $1-2c/\pi+o(1)$ となり、全域下界の誤差は消えない。

これはactual KE族の反例ではなく、有限の飽和全被覆・連結overlap・zero fiber diameterから局所加法誤差を有限回だけ足してよいとする推論への反例である。正しいbuffer原理には局所誤差とfirst-exit幅の比 $\epsilon/b\to0$ が必要（`ke:buffered-local-lower-globalization`）。本稿のP0では全曲線のscalar微分評価を使い、この往復回数の問題を回避した。

## 固定残余基底のnormal比較と相対接着の入力

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

同じ $z$ に沿う動径経路には一つの角度を選んで長さ $\int_a^b ds/d(s)+O(1)$ を得る（`ke:neck-axial-upper`）。両端円が短ければ任意の端点を結べる。固定 source-free 基底で同じ normal moment を持つ点については、残余点を変える接続も原稿 `ke:fixed-base-moment-connectors` で解決した。深度は、$|\mu|=O(M_t^{-1})$ なら両側とも $M_t$ と比較可能、それ以外は符号に応じた片側深度が $|\mu|^{-1}$ と比較可能である。一定深度の水平持ち上げ・動径弧・短い円弧を合わせると、level全体の actual ambient 直径は $O(1)$、Moser像でも同じ、正規化後は $O(R_t^{-1})$ となる。葉内経路やMoserの $C^1$ 評価は使わない。Sourceを含む中央levelは以下の全点径で扱える。Sourceを含む全intervalへの拡張は以下のscaleごとの退出評価で得た。Moving residual collarと全域基底値の対応、および全曲面の下界は別に扱う。

Moser 流では軌道全体の最大速度を軌道平均エネルギーの平方根で置き換えられる（`ke:neck-averaged-speed`）。外側の深部領域の実計量での境界距離 $\delta_t$（上限1）が $m_t\delta_t^2\to\infty$ を満たせば、局所 Chern–Lu と体積上界から共通の source・像を得る（`ke:neck-shrinking-buffer`）。この縮小条件は残余 collar を動かす場合にも候補となる。

固定残余基底上で両側の moving cut $m_t$ における canonical moment は符号が逆で絶対値が $m_t^{-1}$ と一様比較可能である（`ke:neck-deep-moment-strip`）。よって同じ actual Moser map の下で、深部に共通の縮小 moment interval を置ける。K1の局所的な成功後も、第二periodとreduced葉の同時整合、source・branch・coreの被覆、全曲面のshortcutとportalを別々に検証する。任意のMoser移送による定性的存在と、\(p_T\pi_t\) の距離歪み消失も区別する。

大域距離の証明には、関連KE側の条件付き近似写像を入力にする経路と、同じ $p_T\pi_t$ に対して全域上下界を直接示す経路を区別する。本稿では後者を実行した。CP/PBE/TCの対象族での検証自体は結論せず、人工的な基底計量をactual全空間の距離と同一視することもない。

## 共通の end collar での actual fiber の一致

主稿のラベル `ke:normal-flow-naturality` が自然性の正本。全円軌道を含む共通plateauで同じcentered kernelを選ぶと、$G^*K_N\omega_N=K_\alpha G^*\omega_N$ であり、全trajectoryがそこに留まる限り $\phi_NG=G\phi_\alpha$ が厳密に成立する。Primitive $\lambda$ の一致を仮定せず、flowを決める $K\omega$ を比較する。Canonical normal momentの一致と合わせれば、corner torusはneckの同じmoment reduction上の円の全逆像として一致する。

主稿 `ke:neck-corner-diagonal-matching` は、残余cut $b_j$ と固定compact $P_j\Subset P_j^+$、それらの定数を支配するnormal cutoff $n_j\gg b_j$、共通moment区間 $I_j$、最後に $t_j$ の順で選ぶ。三重点側の $a=4n_j$ と $c=4n_j$ におけるmomentはそれぞれ $\pm\pi/n_j$ と比較でき、$I_j$ を狭くして全levelをdeep normal stripへ収める。全circle orbit・第二段の像・第一段の全trajectoryを共通plateauとneckの内側tubeに含められる。この共通collarの一致を、次の全intersectionの制御へ用いる。

Reduced graphに合わせて残余foliationをmomentに滑らかに依存させることは `ke:moment-dependent-neck-foliation` で許される。変更をsource・saddleの近傍とcollar外で恒等にすれば、閉pinched torusとsaddle fiberの型を保つ。固定 $t$ ごとの滑らかさでよく、無重みのmoment微分の一様な小ささは不要。残余基底は元の射影点 $p$ であり、$h_t(p)$ はsource近傍以外でglobal座標としない。Endのradial座標は $Z_{k,t}=C_D^2/h_{k,t}$ を使う。

`ke:neck-corner-saturated-union` はcorner cut $m_t=6b_j$ とneckの境界葉 $B=7b_j$ を分離する。先に $5b_j\le b\le9b_j$、normal深度 $\ge n_j/2$ の広い領域でnormal-first構成へ補正する。Neckの全normal trajectoriesはouter tube内にあり、frame差を引いてもlocal normal深度 $\ge3n_j/4$。Projected normal深度から旧plateauへの移行にはscaled Morse逆写像の粗評価と、固定annulus上で最後に選ぶ $t_j$ の条件を用いる。非incidentなtriple chartと二重線のouter tubesは最初に分離する。そこで $|d\log b(Y_N)|\le C/(n_jb_j)$ を使うfirst-exitにより、neck imageは $b<8b_j$ に留まる。Cornerの最小深度と元の射影の線形性から交点で $b\ge6b_j-C$ を得る。逆normal flowの自然性でmomentを同定した後にnormal深度 $\ge4n_j$ を結論する順序で、循環を避ける。Reduced graphと葉でのtrimから全intersectionが全torusで飽和し、source・saddleを含むactual部分fibrationとなる。End markingは共通torus同定に合わせて選び、任意に独立な第二periodの一致を含めない。この部分構成を `ke:actual-global-fibration` でcoreへ接着し、全曲面を覆った。

## Source reductionと全段階に共通なmarked tree

Sourceの幾何学的入力を `ke:source-reduction-pinched-fiber` にまとめる。固定 $t\ne0$ の $x'y'=th_t(p)$ では、canonical volume frameはsourceでも非零に延びる。Centered homotopyのchain primitiveは固定点で零なので、Moser場とflowもその点を固定する。正規化したnormal momentはそこで厳密に零であり、actual座標での商は $(\mu,p)\circ\phi_N^{-1}$ を用いる。Moser map自体が元の射影 $p$ を保存するとは仮定しない。

零momentの商は位相的には残余曲面であっても、source点で通常の滑らかなsymplectic曲面とは扱えない。標準product模型では $m=(|u|^2-|v|^2)/2$, $w=uv$ として reduced form は $\sqrt{m^2+|w|^2}^{-1}$ に比例し、$m=0$ で特異になる。この模型のDarboux座標がactual残余射影を保つとは主張しない。葉のliftのLagrangian性はambient接空間で直接示す。相異なるregular leavesにsourceを置く条件が、閉じたcritical fiberを一重pinched torusとし、branch fiberとの混在を除く。Normal orbitはprimitiveな消滅cycleである。Focusの局所型とmonodromy自体は既知であり、Zung, *A note on focus-focus singularities*, Differential Geom. Appl. 7 (1997), 123–130, §§2–4, Corollary 1（[一次原稿](https://arxiv.org/abs/math/0110147)）と照合する。異なる $t$ やstageのsemi-global symplectic不変量の一致は結論しない。Vũ Ngọc, Topology 42 (2003), Theorem 2.1（[一次原稿](https://arxiv.org/pdf/math/0208245)）の分類は、同じ単純focus型でもformal power seriesの追加不変量があることを示す。

`ke:fixed-marked-tree-exhaustion` は $D\setminus Q$ 上の一つのembedded marked pants foliationを最初に固定する。単純sourceは $t=0$ を含むparameter disc上で一価に追跡し、その小円板に支持を持つisotopyで運ぶ。全source葉とcritical pantsを含む固定compactの外にend graph補正を置くため、全stageと全ての十分小さい複素 $t$ で同じ標識付き木を使える。K3の相対葉族補間と全fiber単位のtrimもこの木を変えない。これは抽象木・source・成分labelsの固定であり、全torusの二つのcycleの族全体での自明化や、$t$ に滑らかな全域fibration族を与える主張ではない。

一般のMorse関数のpath componentが同じことだけから固定Reeb treeは従わない。Maksymenko, Comment. Math. Helv. 80 (2005), Main Theorem p.658 はpath components、Lemma 4.1 p.665 はgeneric KR-mapの同値を扱う。Regular annulusの葉を保つDehn twistは§6.1, Lemma 6.4 p.668（[掲載版](https://ems.press/content/serial-article-files/43060)）。本稿の固定木には、既に構成した実際の葉層のdiffeomorphismによる移送を使う。

## Source中央部の体積・momentとactual接続

正本は `papers/sections/paper/ke_source_connectors.tex`。$xy=tz$、$t=\tau^2$、$(x,y,z)=(\tau X,\tau Y,XY)$ として固定bidiscを使う。`ke:source-central-density` はdensityを $L^{-2}|dX\wedge dY|^2$ と両側比較する。下界はcapped canonical density、上界は正しいoriented gateのannulus–disc volume上界と中央の最大値原理による。Canonical potential $u_t=\log(\omega_t^2/|dX\wedge dY|^2)+2\log L$ は有界で $dd^cu_t=\omega_t$。射影を保つMorse座標にも適用できる。

`ke:source-central-moment` は同じcanonical primitiveで $|\mu_t|\le C/L$、固定点で $\mu_t=0$ を与える。Normal平均potentialの凸性と中央からoriented arm断面までの割線を用いる。Base-only変更はnormal momentを変えず、独立な加法定数の調整を行わない。`ke:source-central-mean-distance` は固定Euclidean体積に関するtrace積分と平均二乗ambient距離を $O(1)$ に抑える。部分積分と線分の二点積分による。ほとんどの点からなる部分集合の径は得られるが、全点・固定点・特定moment levelの径にはならない。

`ke:source-central-short-escape` はactual inradiusを $O(L^{-1/2})$ に抑える。Density上界から $\operatorname{tr}_{g_t}g_{\rm E}\ge cL$ を得て、大きさ $O(1/L)$ の非負Laplacian barrierを作る。Ricci下界による距離二乗のLaplacian comparisonと最大値原理で、全中央点からあるgateへの短い退出を得る。`ke:source-central-arm-connectors` はgateから正しいarm内を $s_x=\kappa L$ 又は $s_y=\kappa L$ まで進め、全費用を $O(1)$ とする。終点の残余座標・momentは指定しない。

固定連結source-free compact基底では `ke:fixed-base-central-band` により、固定 $A>0$、$m_t\to\infty$、$m_t=o(M_t)$ の下、$|\mu|\le A/M_t$ のcentral band全体がactual径 $O_{P,A}(1)$ を持つ。異なるmomentも含み、Moser像には $O(m_t^{-1})$ の端点費用だけを加える。両normal深度 $\ge\kappa_A M_t$ をmomentの片側下界から導き、水平・動径・円弧を組み合わせる。

Source側の `ke:source-central-band-reduction` は、固定residual disc、人工境界からの余裕、normal最小深度の下で、$|\mu|\le A/L$ の全点を固定rescaled coreへ $O(1)$ で接続する。この帰着と下記のGaussian体積比較により、中央帯の全点径は $O(1)$ となる。一般の同一moment集合についても、`ke:source-all-moment-exit` が指定した残余境界への退出条件 `ke:eq:source-moment-exit-input` を証明する。Central inradius、平均距離、全source fiberの径、長いnormal armsを含むneck全体の径を区別する。

`ke:source-potential-modulus` はGuedj–Guenancia–Zeriahi（参考文献キー `GGZDiameter`、Proposition 1.4）の局所距離評価を用いる十分条件を記す。Potential $u_t$ に一様な連続度 $m$ があり $\int_0^{r_0}\sqrt{m(r)}\,dr/r<\infty$ なら、固定coreのambient径は $O(1)$。このsquare-root-Dini modulusや一様Hölder評価自体はまだ証明していない。現行の $O(1)$ 径定理は下記のslab/Gaussian比較により無条件で得ており、このmodulusを必要としない。有界potentialから自動的に導いたり、同論文の大域Kähler class仮定を局所族へ無条件に適用したりしない。

## Source中央全点径：potential bufferとGaussian体積比較

正本は主稿の `ke:source-central-diameter` と `ke:fixed-base-source-central-band`。固定した $d$・族・residual基底について、固定点と座標軸を含む中央source全体のambient径は $O(1)$、正規化後は $O(R_t^{-1})$。Source-inclusiveな $|\mu_t|\le A/L_t$ の全中央帯と閉pinched torus全体にも拡張できる。追加のTCや一様Hölder仮定は使わない。

証明の依存順は次の通り。

1. `ke:source-tube-potential`：固定physical tubeをcentral coreと正しい二half-armsで覆い、actual densityとcapped densityを二側比較する。射影Chern–Luから $g_t\ge c g_{FS}$、nested physical tubesから固定actual bufferを得る。
2. `ke:positive-poisson-log-gradient`, `ke:source-potential-buffer`：非零正則frame $dx\wedge dy/t$ を固定した $u=\log(\omega_t^2/|\Omega|^2)+2R+C\ge1$ は $\Delta u=c_4$。Bochnerと距離cutoffで $|\nabla\log u|\le C$。中央点の固定小球では $u$ が有界となり、capsの積下界から両normal深度が $\kappa L$ 以上となる。縮小するrescaled bidisc内に球を閉じ込める必要はない。
3. `ke:source-shell-gaussian-tail`, `ke:source-wide-gaussian-tail`：固定source-free shellへのambient距離の $W_*^{1,2}$ normを有界potentialから抑える。Dinh–Marinescu–Vu, Theorem 1.2（参考文献 `DMVMT`）は固定補助Euclidean potentialに適用するので、actual potentialのHölder性は不要。$x=e^{Lw}$ の固定サイズcoverでは約 $L$ 個の周期を除して、広い中央帯のactual体積tailを $CL^{-1}e^{-aA^2}$ とする。
4. `ke:source-central-volume-anchor`：固定source-free residual annulusと $L/4\le s_x\le L/3$ のslabを取る。Density $L^{-2}$、logarithmic normal幅 $\asymp L$、一周期の角度から体積は $cL^{-1}$。Source-free中央帯の既存接続によりshellへの距離は $O(1)$ であり、sourceの全点径を入力にしない。
5. `ke:source-central-diameter`：距離 $D$ の中央点の小球は広い中央帯に入り、体積上界は $CL^{-1}e^{-a(D-\delta)_+^2}$。前項のslabと全曲面のRicci下界によるBishop–Gromov比較から、同じ球の体積下界 $cL^{-1}e^{-C(D+1)}$。係数 $L^{-1}$ が相殺し、$D^2\le C(D+1)$、全点で $D=O(1)$。

固定基底の残りはsource-free中央帯の $O(1)$ 接続でつなぐ。Canonical primitiveのbase-only変更はnormal momentを変えず、actual Moser像には両端の短いtrajectoryだけを加える。経路はfiber又はmoment level内に留まらなくてよく、intrinsic fiber径の主張ではない。全intervalの同一moment接続は次の結果で与える。木上のfiberとのtarget対応と全曲面のno-shortcutは別に扱う。Gaussian tailだけ、短円の長さだけ、又はMoser像のorbit直径だけで全点評価を結論しない。

## 全moment intervalのsource退出

正本は `ke_source_all_moment_connectors.tex` の `ke:source-arm-uniform-tensor`、`ke:source-direct-central-exit`、`ke:source-all-moment-exit`。中央帯・source軸・固定点を含めて、同じcanonical momentを持つ指定残余境界への退出費用は **$O(1)$**。経路自体はlevelに留まらなくてよい。固定stageの同一moment集合全体の径も $C+C_P$ 以下となる。定数は固定source chart・族・次数に依存するが、source退出の定数を残余exhaustion stageに依存させる必要はない。

核心は $xy=tz$、$s=-\log|x|^2$ の領域 $n_*\le s\le\kappa L$、$|z|\le\beta$ における $U=|d\log s|_g^2$ の制御である。Rank-one Bochner計算から $\Delta U\ge U(U-1)$。固定normal境界では射影下界から $U\le Ce^{n_*}/n_*^2$、残余境界ではsource-free tensor比較から有界、moving境界 $s=\kappa L$ では正のpotentialが有界なのでorientationを保つ固定半径のactual球を取り、localized Schwarzから有界となる。三境界の最大値原理で全armの $U$ が有界となる。

このnormal covectorの下支配と、射影下界による残余covectorの下支配を合わせ、cusp–disc積 $h$ に対して $h\le C\omega_t$ を得る。既存のvolume上界 $\omega_t^2\le Ch^2$ と複素次元2の固有値比較から $\omega_t\le C'h$。固定 $x$ で $z$ をshellへ動かす水平経路は有界長であり、momentとnormal深度の二側比較から最後の動径補正も有界長となる。

中央点は `ke:source-central-short-escape` の $CL^{-1/2}$ 退出でgateへ運び、短円の上界を積分して $s=\kappa L$ へ接続し、上の水平経路へつなぐ。従って全moment退出にも中央全点径にも、Gaussian可積分性を入力にしない証明がある。これは中央のtensor二側比較を主張するものではない。

**依存の順序。** Capped density・complete volume上界 → 射影下界・正のPoisson potential → orientationを保つactual球 → 境界Schwarz → arm tensor → 直接退出。固定normal境界の粗い上界にSong/Rochon–Zhangの成分収束は不要であり、full-triple比較・global sharp scalar評価・中央全点径をこの鎖の入力にしない。Source-free側面のtensor比較は、その独立なactual first-exit証明を使う。

深度 $S$ ごとのGaussian tailとgood slabの体積 $S^{-1}$ の評価は独立の補助結果として保持する。Positive potentialだけによる一般のscale bufferは半径 $c/(1+u)\gtrsim R^{-1}$ であり、moving境界 $s=\kappa L$ では $u=2\log(1/\kappa)+O(1)$ によって固定半径となる。この区別が三境界証明を非循環にする。Actual Moser像には両端の既存の短いtrajectoryを加え、同じcanonical momentを移送する。

## 旧corner値と全域基底のparameter化

正本は `ke_global_base_compatibility.tex`。`ke:common-edge-moment-profile` は全triple endsのcanonical momentを共通simplex profileと比較する。Moment誤差はnormal生成場の長さ $\mathfrak a$ を含む $O(\mathfrak a/m)$、normal longitude微分は $\asymp\mathfrak a$ なので、逆写像で重みが相殺し辺座標誤差 $O(1/(mR))$ となる。Momentの加法定数は既存primitive periodの厳密同定で固定する。

`ke:corner-cap-disk` は小さいtarget像だけからdisk構造を推論しない。閉linkのnormal facesとroundingを列挙し、joint momentの単調性で各cap境界が一本のproper arcであることを示す。この三capを取り除いたdiskを、各vertexの $O(\eta)$ 近傍内の境界延長でuncapする。さらにsimplex座標で一様にinsetし、残るannulusを3vertex panelsと3edge stripsへ分ける。Stripでは全枝共通profileと各end profileの単調補間を用い、core sectorでは境界homeomorphismをdiskへ延長する。

結果は `ke:global-base-parameterization` の全保持cornerにおける旧softmaxとの誤差 $C\eta$、各component core/変更collar像の頂点への $C\eta$ 近接である。$\eta=A(1+\log(N_j+1))/R_t$。`ke:collapsed-tree-common-moment` はcore近傍以外の $p_T$-fiberが厳密に同一moment上の内部木全体となることを別に保証する。`ke:neck-base-value-control` は全保持neckで辺値との $C\eta$ 近接、source critical valuesでは $e_i+e_j$ への近接を与える。

旧softmaxの閉辺にはregular torus fibersがある一方、全域基底のcellular辺はbranch locusである。従って全保持cornerでの厳密な値の一致は一般に不可能であり、insetによる一様に小さい誤差が適切である。位相同定だけからこの値の制御を結論しない。

## Component coreの固定段階移送と相対条件

正本は `ke_component_core_transfer.tex`。成分極限 $\omega_i^\infty$ へのfixed-gauge smooth収束から、$\beta_t=d^c\log((E_t^*\omega_t)^2/(\omega_i^\infty)^2)\to0$、$d\beta_t=E_t^*\omega_t-\omega_i^\infty$ を得る。固定compact上のMoserはactual変位・$C^1$誤差を $o_t(1)$ とする。$\beta_t$そのものがd-exactという主張ではない。

境界germを点ごとに保存するには、primitive差のcollar $H^1$ classがcoreの $H^1$ から延びることが必要となる。Fiber periodsが全て零でもbase-circle fluxが残る例を `ke:core-relative-flux-example` に保持する。これはfiber partitionの不存在例ではない。平均形式にもparameter方向の同変Moserを入れる $A_t b_t A_0^{-1}$ はexact symplectic germとなり、normal momentの加法定数も保つ。

`ke_component_core_geometry.tex` により、任意の固定compactと全collarでKE形式・primitiveに厳密一致するsmooth compactification、正residueの有限型KE core、その小さい飽和近傍のLagrangian fillingを得た。この局所core fillingの存在と、既存full collarの葉を保つことは別条件である。後述のactual link構成はその相対問題を解く。`comp:finite` の出力葉が指定葉に一致することは、二形式の一致だけからは従わない。条件付き系 `ke:conditional-component-core-filling` は、その入力があればactual移送・接着・十分遅い対角選択でcore全体の正規化径を消せることを示す。

## Saddle を動かす相対葉族補間

`ke_relative_reduced_foliations.tex` の `ke:simple-saddle-family-trivialization` と `ke:saddle-moving-relative-interpolation` を証明した。Compact reduced surface上のsmooth first-integral族を対象とし、各connected critical leafが一つのsimple saddleを含み、boundary collarの葉partitionとcontinuation markingが固定されると仮定する。全critical valuesの相異性は不要。各critical pants上でcritical-value速度に一致するglobal basic関数ζを作り、∂μf+df(Y)=ζ、dζ=a dfを解く。これにより全critical leavesと全regular annuliを同時に同定し、anchorで一致する二族をmoment cutoffで補間できる。異なる値のfirst integral表示を一致させる必要はない。

`ke:actual-saddle-moving-neck-interpolation` は自由Hamiltonian normal bandへ持ち上げ、actual Lagrangian性とS¹×figure-eight、全corner葉、normal markingを保つ。補間はsourceのcritical momentから離して行うためcentral pinched torusを変えない。Liouville moment M=μ−ρの場合、時間は s(μ)=log((μ−ρ)/(μ*−ρ)) で再parameterizeする。この葉族補題は別担当と内部点検済み。全link被覆・primitive補正・coreの全域接着は次節の別の証明で確認した。この葉族補題単独の帰結ではない。

## Actual core の全域相対接着

**主稿 `ke:actual-global-fibration` に証明を統合し、追加証明を別担当と内部点検した。** 任意の固定 $d\ge5$ と既存一般性条件の族について、K2の部分fibrationから全 $X_t$ 上のactual KE–Lagrangian fibrationを構成する。Markingの組合せ型を保ち、第二作用やcritical valuesの数値は先指定しない。全曲面の距離歪みはこの構成定理の結論ではなく、`ke:global-ambient-lower` と `ke:global-ambient-upper` の別の証明で扱う。

### 正確な period と閉 link

正本は `ke_component_link_cover.tex`。Positive-residue primitiveの周期1 meridian積分を $M_a$ とすると、$q_a=M_a+2\pi w_a$ は既存canonical normal momentの向き付き値と**厳密に**一致する。有限直線ではlog volume frameとの比の単純極、無限遠ではaffine volumeの3重極とlog volumeの単純極の差を使う。Holomorphic unitのwindingは固定collar上のhomotopyで零。非正則な座標補間では $G^*\lambda$ を使い、$G^*d^c=d^cG^*$ としない。

残余尺度 $b_j$、normal cutoff $n_j$、共通幅 $\iota_j$ の後で $N_j\iota_j\gg1$ と $N_j\gg n_j$ を選ぶ。$\delta_j=4\pi/N_j$ のnormal moment facesを取り、cornerでは $(q_a-\delta_j,q_c-\delta_j)$ のsmooth monotone minimumで丸める。Corner momentは全深度比に一様に $4\pi/s_a$ と比較できる。重複帯ではresidual momentが $1/b_j\gg\delta_j$ なので丸めは作動せず、normal faceと厳密に一致する。深さを近似的に合わせた切断ではない。正のresiduesにより $M_a=q_a-2\pi w_a<0$、不変primitiveのLiouville場はこのlinkを外向きに横断する。

### 固定段階でも全特異層を覆う理由

`ke:fixed-stage-stratum-coverage` は、同じcentered normal Moser flowをさらに深い**固定**tubeへ制限する。FlowはODE一意性で元のものと同一である。Fixed-shell momentの下界だけでは足りず、$|\mu|\le C_P/M<\iota_j$ の上界と逆像bufferを用いる。Source基底点もcomponent側cusp shellでは通常の滑らかな点なので含む。残余は $6.5b_j$ まで、cornerのactual imageはphysical最小深度 $6.3b_j$ から覆い、端のgapをなくす。粗い $\min\ell>2m=12b_j$ の包含だけではneck cut $7b_j$ との間が残る。

中央の全特異locusの固定ambient近傍を覆うので、部分fibrationの外部は各 $W_i$ の互いに素な固定compactのgraph imagesに入る。閉linkをその外側へ置けば全域被覆を得る。境界が全fiberで飽和し旧fiberが連結なら、そのfiberは内外を横切れない。これが `ke:whole-fiber-core-trim` の全fiber単位の切詰めである。

### Invariant primitive と nontrapping

正本は `ke_core_invariant_primitive.tex`。短円の0次評価からgeneratorの一階評価は出ない。Normal logarithmic chartでbare generatorを深度逆数の定数場として書き、RZの全cusp微分からMoser mapをC2まで制御する。Cornerも比較Hamiltonianを一階高めてC2flowを得る。必要なactual actionsで $|V|+|\nabla V|\le\varepsilon_j$、$\varepsilon_j=C_*/b_j+C_j/N_0$ となる。

Actual symplectic circleのcentered kernelについて
\[
 F=\int_0^1(1/2-s)\lambda(V)\circ R_s\,ds,
 \qquad\mathcal A\lambda-\lambda=dF,
 \qquad |F|+|dF|\le C\varepsilon_j H
\]
が成り立つ。$K\omega=0$ がexactnessの理由である。Common normal action上では $F_C-F_N$ が不変なので、source torus label $B/b_j\in[5.2,5.4]$ の帯でnormal-invariantに貼る。Retained cornerに達する前にfull torus gaugeへ切り替える。$\eta(\Psi/N)$ の零延長支持全体は広いnormal/corner construction domainsで覆える。保持されたsoftmax領域だけを作用の定義域と誤認しない。

正residue potentialは $|d\Psi|\asymp H$、$Z_0\Psi\ge cH^2$ を満たすため、補正後も $Z^{\rm ad}\Psi\ge(c-C\varepsilon_j)H^2>0$。Core外に新しいtrappingを作らない。Actual形式では先に固定compactのexact Moserを行い、$\lambda_{\rm int,t}=(\varphi_t^{-1})^*\lambda_0$ をactual actionsで平均する。Canonical positive-residue gaugeとの差はexactなのでperiodsを保つ。二形式を合わせる前のprimitive差をexactとみなしてcutoffしない。

### Cone filling、相対補間、費用

正本は `ke_actual_core_gluing.tex`。各linkのquotientは、normal facesの木 $T_{ij}$ の標識endをcorner annuliでつないだgraph $\Gamma_i$。Contact formを変更せず、compact Liouville domainの $K\setminus\Sigma\simeq(-\infty,0]\times S$ に対し $\Pi(\varphi_s(y))=[e^s,\pi_S(y)]$ とする。有限退出時間とcompactnessがcone pointでの連続性を与える。これはEvans–Mauri Lemma 2.16のcompact版であり、既存のcone原理自体を新成果とはしない。

外向きcollarのLiouville葉族は一般には旧neck葉族と異なるため、前節の相対補間を $q_a=\delta_j\ne0$ の小帯へ適用する。全corner葉とsource近傍を保ち、saddleは動かせる。全fiber trim後のclosed piecesでlocal fiber relationsの有限和は既に推移的なので、閉同値関係となりHausdorff基底を得る。基底は同じ $B_d(T)$。

`ke:component-logarithmic-connectors` により、各componentのcore・変更collarの接続費用とambient径は $C(1+\log(N_j+1))$ で抑えられる。$C$ は固定した族・charts・weightsのみに依存する。全深度が $CN_j$ 以下であることと固定componentのcusp上比較を使い、normal動径の積分 $\int ds/s$ で固定compactへ結ぶ。全経路は $\{\Psi_i\le AN_j\}$ に入り、この拡大compactを先に固定してからactual metricを比較する。これは**各componentごとのambient評価**であり、異なるcores全部の合併径や任意Liouville軌道の全長、fiber内在径は結論しない。

Skeletonの連結性は $\Sigma=\bigcap_{T\ge0}\varphi_{-T}(K)$ というnested compact connected setsの表示から直接従う。保持cornerのquotientがdiskであることとproper cap arcsは `ke:corner-cap-disk` を用い、$B_d(T)$ の同定との循環を避ける。対数接続補題は別担当も独立に導出・点検済み。`ke:compact-relative-morse-smale` は境界とcritical germsを保つ小さいcontact holonomy変更とexact Moserにより、同じKE二形式上のprimitiveをMorse–Smaleにする。Stable manifoldsのclosureは低いindexにのみ落ちるため、次元順の閉isotropic filtrationが得られる。Whitney条件は主張しない。Cone fillingでは開辺上のsmooth submersionも明記した。

### 全接続予算の選択順序

旧softmax辺の全体で $B=m_j+r_c$、$0\le r_c<1$ なので、全marked tree・source discs・portal端を含む $P_{ab,j}\Subset P^+_{ab,j}$ は $N_j$ より先に固定できる。同一moment接続定数を $C_j^{\rm neck}$ とする。`ke:component-neck-tail-depth` は $q\ge4\pi/N_j$ の成分側尾部に $s\le2N_j$ を与え、同じcentered flowの浅い固定compactと深いtubeへの制限を分けて、actual像も深度 $CN_j$ に入れる。深い側のfirst-exitには固定componentの $|d\log s_a|\le K$ と全normal/residual buffersを用いる。

従って、まず $H_j\le C(1+\log(N_j+1))+C_j^{\rm neck}$ が得られる。許容cutの下限に $C_j^{\rm neck}\le1+\log(N_j+1)$ を加えれば
\[
H_j=C(1+\log(N_j+1)),\qquad
U_{j,t}\le C_d\left\{b_j^{-1}+\frac{1+\log R_t+\log(N_j+1)}{R_t}\right\}
\]
とできる。これは残余定数のexhaustion増大率の解析評価ではなく、選択順序による吸収である。下界の段階定数とfixed-compact収束の閾値も残るため、最適な全域rateは結論しない。経路はambientであり、同一momentやfiberの内部を通る必要はない。

### 主要接着依存の点検範囲

Centered averageの $K\omega=0$、二作用の $F=K_1\lambda+A_1K_2\lambda$、common normal上の $V(F_C-F_N)=0$ を直接確認した。GeneratorのC1評価にはmapのC2が必要であり、既存C5入力からの微分階数を確認した。切替え帯 $5.2b_j$–$5.4b_j$ は広い構成域 $\min\ell>3b_j$ とnormal-first plateau $5b_j$–$9b_j$ に入り、実交点 $5.5b_j$–$8b_j$ までにfull torus gaugeへ移る。支持全体の被覆、先行するexact Moserとperiod保存、$Zq=q-\rho<0$ の向き、全fiber trim、相対葉族の境界germとcritical-leaf marking、閉quotientを読み合わせた。これは全旧局所証明の包括的再監査ではない。

### 切り取った cap と旧 softmax 値

`ke:core-depth-upper` は、固定componentのstrictly plurisubharmonic potential $\Psi_i=\sum_aw_as_a-2\sum_a\log s_a+O(1)$ を使う。Link上の深度が $CN_j$ 以下なら、$E_{i,t}^{-1}(K_{i,j,t})$ における最大原理と $\Psi_i\ge c\sum_as_a-C$ からcore全体でも同じ上界が得られる。ここではLiouville補正後のpotentialを要求しない。Graph gaugeはこの固定compact上で最後に $t$ を小さく選び、corner逆写像のlog-depth変位から乗法的に比較する。

`ke:removed-corner-target-cap` は、$x\in K_{i,j,t}\cap W_{t,J}$ に対して
\[
 d_\square(P^{\rm old}_{t,J}(x),e_i)
 \le\eta_{j,t}:=\frac{\sqrt2\log(CN_j)}{R_t}
\]
を与える。各capの径は $2\eta_{j,t}$ 以下で一様に消えるが、異なる成分cap全体の合併径は消えない。実際に構成したcompact coreだけを扱い、full corner全体のmoment不等式の解集合を同じcoreと同一視しない。

保持corner $A_{t,J}$ の旧projection像は $2\eta_{j,t}$-netであり、旧protected距離の制限を用いたGH誤差は $E_{j,t}/2+2\eta_{j,t}$ 以下。全曲面距離の上界にも旧cornerの経路を使える。一方、保持部分自身の新しい内在距離の上界にはcapを避けるdetourが必要で、全曲面距離の下界にはno-shortcut評価が必要である。

全域基底が $B_d(T)$ と同相で、保持cornerのtorus partitionが一致しても、特定の基底parameterizationで $p_T\pi_t=P^{\rm old}$ とは限らない。`ke:global-base-parameterization` はcore側のcone sectorsを上のvertex capsへ送り、全保持cornerで旧softmax値との一様に小さい誤差を実現する。小さいactual径だけから、任意のtarget parameterizationで像も小さいとはいえない。

## Source の residual cutoff と Euler 場

`ke:source-euler-bound` は固定source tube上のEuler場 $W_+=x\partial_x+y\partial_y$ をactual norm $O(1)$ に抑える。固定normal境界はcomponent KE収束、固定residual境界はsource-free tensor比較で評価し、内部へBochner最大値原理で延ばす。中央点で $|z|\ge e^{-a_t}$、$a_t=o(R_t)$ なら正の同時scalingを $O(a_t+1)$ 時間で固定residual shellまで進められ、終点はcanonical central moment帯にある（`ke:source-sublog-residual-connectors`）。この経路だけでは $z=0$ と $|z|<e^{-a_t}$ を制御しない。以下の別の体積比較で全点評価へ進む。無限のscaling時間を有界な経路長に読み替えない。

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

遅いexhaustionでflow生存・共通bufferとtriple endsの葉の一致は実証した。全域被覆・core接着は `ke:actual-global-fibration` で証明した。特異領域を含む全点の距離評価は、sourceの全moment退出とscalar/portalの各節で別に証明した。KE側 `neck:lem:rank-one-circle` はresidual rank-one下界とvolume上界だけでnormal circle長を抑えるが、その下界とactual bufferを証明する必要がある。固定residual境界の影響が消えないexact negative KE productの例があるため、normal深度だけからproduct asymptoticsを推論しない。


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
を証明する。一つはW_{t,J}内の経路による内在距離、もう一つはV_t={min ell_a>R/2}内の全経路を許した距離をW_{t,J}へ制限したもの。標的d_Jは三枚のunit squares自身の内在距離として定義され、`topo:coordinate-retraction` により全C_dの距離の制限と等しい。Source側で全曲面の経路を許す下界は `ke:global-ambient-lower` で別に証明した。

模型の証明はKE主稿 `simplex:thm:closed-corner-model`。S=R−2 log Rとし、Ψ_a=[log(ell_a/R)/S]_0^1とclipする。最大深度≥L/3からΨの像はC_Jに入り、微分がactiveなのは高々二方向である。一方向では係数1のSchwarz評価、二方向ではell_j+ell_k≤2L/Rからsharp product比較を使い、complete simplex全体の全経路の長さ下界を得る。上界ではC_Jのgeodesicを高々三枚の異なるsquares内の直線分で実現し、各線分を幅4 log R/Rだけ内部へ移す。Sharpな内部比較とcoarseな短いconnectorsを合わせて同じ率を得る。Seam collarが薄いことだけを下界の根拠にはしない。

Actual/model比較O(1/R)に加え、Moser場のC1評価からmodel計量のLie derivativeを直接抑え、φ_t^*g_t=(1+O(1/R))g_L^sfを得る。保護領域内の全経路を扱うときは、Moser trajectoryのmodel長さO(1/R)とΨのLipschitz定数O(1/R)から、端点誤差d_J(Ψφ_t(z),Ψ(z))=O(R^−2)を用いる。これにより、閉cornerのfibrationの射影そのものがGH approximationになる。

全fiberのintrinsic/ambient diameterはO(1/R)、正規化後はO(1/R²)、raw-map誤差はO(log R/R)。Squareの共通辺と共通頂点でも同じregular T² fiberである。これらを既存大域fibrationのsource・branch・coreのsingular fibersとは同定しない。全曲面の被覆・core接着と、$V_t$ 外を通るshortcutの下界は、それぞれ別の証明で確保した。新規性の網羅的確認と外部査読・形式証明は未実施。

一般のcut $m_t\to\infty,\ \log m_t=o(R_t)$ についても、同じsoftmaxとMoser mapの射影が局所GH近似になることを `ke:slow-cut-closed-corner-gh` で証明した。内在・protected距離のdistortionは $C[m_t^{-1}+(\log(m_t+1)+\log R_t)/R_t]$、fiberの元の尺度の内在径は $C/m_t$。内部squareを幅 $\delta=(\log(m+1)+4\log R)/R$ だけ縮め、pruningでは $S=R-\log m-\log R$ を使う。$m_t$のparameter微分を使わず、stepwiseな遅いexhaustionにも適用できる。この遅いcutを `ke:neck-corner-saturated-union` の対角選択へ用い、actual core接着と全域距離評価へ組み込んだ。


## 開正方形上のactual KE–Lagrangian collapse
主稿 `papers/sections/paper/ke_open_cell_collapse.tex` は、任意の固定次数d≥5、固定0<η<1/2についてKη=[η,1−η]²上の局所結果を与える。関連KE主稿 `simplex:cor:actual-dominant-product` により、独立深度a,b∈[L^η/2,2L^(1−η)]ではproduct-cuspとの誤差は全固定階でO(L^−η)である。模型側O(((a+b)/L)²)とactual側O(1/min ell)を合わせた率であり、global capped volume下界、complete模型の上下比較、Savin正則性に依存する。(TC)_dや(PBE)_dは追加仮定しない。

`ke:open-cell-moser-c1` はchain primitiveとMoser場のC1 normをO(L^−η)とし、flowのpullback metricを制御する。`ke:open-cell-collapse` はactual Lagrangian T² fibration、fiberのintrinsic/ambient diameter O(L^−η)、raw-map誤差O(1/R)を与える。Moser像領域に内在長さ距離を入れると、R^−2 g_tは平坦KηへGH収束し、projection distortionはO(L^−η+L^−η/R)=O(L^−η)。定数は固定ηに依存する。

開正方形と全閉cornerの局所結果、source・saddleを含む部分fibration、coreへの全域接着、全曲面ambient距離の比較を区別する。現在は各段階の証明を `ke:global-metric-realization` に統合している。局所GH評価だけを全域distortionの根拠にはしない。


## 負KE計量のGH極限とfiber収縮

### 二つの尺度と先行定理
全平面退化は $X_t=\{\prod_iL_i+tF_d=0\}\subset\mathbf P^3$、$d\ge5$ とし、$F_d$ は三重点で非零、二重線上では単純零点を持つとする。$\operatorname{Ric}(\omega_t)=-\omega_t$ の規約では $[\omega_t]=2\pi(d-4)H$、$\operatorname{Vol}(X_t,g_t)=2\pi^2d(d-4)^2$ である。複素構造を固定したままの負KE計量はこの規約で一意であり、ここで動かすのは複素構造である。

Song, arXiv:1706.01518v1, Theorem 1.2（https://arxiv.org/abs/1706.01518 ）の適用：中央fiberはSNCでslc、相対canonicalは $\mathcal O(d-4)$ でample、全空間は $xy=tz$ 型ordinary double pointsを持つnormal canonical varietyなのでstable degenerationの仮定を満たす。成分内部に基点を置く非崩壊極限は $d$ 個の $\mathbf P^2\setminus\{d-1\text{本の直線}\}$ の完備有限体積KE曲面である。これはcore skeletonではなく四実次元の開曲面である。Song–Sturm–Wang, arXiv:2003.04709v1, Theorem 6.1（https://arxiv.org/abs/2003.04709 ）もstable familyの多点付き極限を扱う。すべての基点列が非崩壊だという意味ではない。

Zhang, *Collapsing of negative Kähler–Einstein metrics*, MRL 22 (2015), 1843–1869, DOI 10.4310/MRL.2015.v22.n6.a16, arXiv:1505.04728v2, Theorems 1.1/2.4は、Q-factorialなsimple toroidal total spaceと相対canonicalのamplenessの下で、stratumへ動かす基点における局所torus collapseを示す。曲面では二重曲線でS¹、三重点でT²が縮む。主稿 `intro:ke-collapse` に比較を収録した。我々のsourceの局所環 $\mathbf C[x,y,z,t]/(xy-tz)$ はQ-factorialでない。Small resolutionはcrepantなのでexceptional $\mathbf P^1$ 上の相対canonicalの次数は0となる。従って「小解消すればZhangをそのまま適用できる」とは言えない。

Mandel, *Degenerations of negative Kähler–Einstein surfaces*, JLMS 109 (2024), e12818, DOI 10.1112/jlms.12818, arXiv:2206.09792, Theorems 1.1–1.2は負KE neckとその尺度別模型を構成するが、我々のcompact family全体へのgluingを完了した定理として引用しない。K3での対照例はGross–Tosatti–Zhang, CAG 24 (2016), 93–113, DOI 10.4310/CAG.2016.v24.n1.a4, arXiv:1304.1820, Theorem 1.1。楕円K3の適切なRicci-flat metric族が底へ崩壊し、hyperkähler rotationでspecial Lagrangianの解釈を得る。負KEに同じ結論を移す証拠にはしない。

### Diameter-scale極限とactual fibrationによる実現
KE研究の `papers/cubical-gh-limit.tex` では $R_t=\log(-\log|t|^2)$、$\mathcal C_d=\{w\in[0,1]^d:\max w_i=1,\ |\operatorname{supp}w|\le3\}$ とし、$(X_t,R_t^{-2}g_t)\to(\mathcal C_d,d_\square)$ を **(G)$_d$+(CP)$_d$+(PBE)$_d$の下**で述べる。これらの条件付き定理の正本は関連repoの現行方針・Part IV–Vである。本稿の `ke:global-metric-realization` はscalar下界とportal上界による別の直接証明を与え、CP/PBE/TCを検証したとはしない。

局所plumbingのモデル $z_0z_1z_2=t$ で $u_i=-\log|z_i|$、$L=-\log|t|$ とすると $\sum u_i=L$。Cuspのradial model $\sum (du_i/u_i)^2$ を $(\log L)^2$ で割り、$r_i=\log u_i/\log L$ と置くと、制約は極限で $\max r_i=1$ となる。三重点では三枚のsquareが現れる。このradial計算は候補の説明である。Actual KE metricの一様漸近と全閉cornerの局所GH極限には、上記のcomplete模型比較と距離定理を別に用いる。

本稿で構成した写像は $f_t=p_T\circ\pi_t:X_t\to B_d(T)\to\mathcal C_d$。五次では $p_T$ は同相、六次以上では基底内の木も収縮する。**空間としてのGH収束**と**指定したLagrangian fibrationによる実現**を区別する。

主稿 `base_topology.tex` の `topo:ke-map-compatibility` に、$\operatorname{dis}(\Phi_t)\le a_t$ と $\sup_xd_\square(\Phi_t(x),p_T\pi_t(x))\le b_t$ から $\operatorname{dis}(p_T\pi_t)\le a_t+2b_t$ を得る比較命題と証明を置いた。Ambient fiber diametersは同じ量以下、GH距離はその半分以下である。一般的新規性は主張しない。この一般的な比較命題と、同じ $f_t$ に対して直接証明した全域distortionの消失は別の結果である。本稿の主定理は外部の条件付き近似写像 $\Phi_t$ を入力にしない。

**公表前の点検：** `ke:global-metric-realization` から依存する局所・全域証明を逆にたどり、文献の適用条件、固定stageの定数と最後のparameter閾値、同じ写像への上下界の適用を包括的に確認する。新証明と接続は内部点検済みだが、全主稿の再監査とは区別する。Action-affine structureだけからcanonicalなRiemannian基底計量は決まらない。


## 局所fibrationの証明と解析入力
曲面側の着手対象は複素次元2でのKE極限とLagrangian fibrationの適合性である。主稿の `papers/sections/paper/ke_fiber_compatibility.tex` に次の証明を置いた。

- `ke:short-torus-averaging`：自由な正則 $T^2$ 作用、torus不変Hermitian計量 $h$、$c h\le g_\omega\le C h$、torus上のperiod零を仮定する。作用の周期1生成場の長さの和を $e$ とすると、平均化のchain homotopyから長さ $O(e)$ のprimitiveを作り、一つのMoser flowで領域全体にLagrangian fibrationを構成する。変位は $Ce/(2c)$ 以下、ambient fiber diameterは $\sqrt C e(C/c+1/2)$ 以下。高階微分比較は使わない。
- `ke:triple-hexagon`：$\zeta_i\zeta_j\zeta_k=t$ の三つのsquareを一つのhexagonとして全phase torusで実現し、raw-depth mapとの誤差を $O((1+\log m_t)/R_t)$ に抑える。
- `ke:triple-moving-fibration`：全phaseを含む moving domain $\min\ell_a>m_t/2$ 上の一様tensor比較を追加仮定すれば、actual負KE形式に対する局所fibrationが得られ、そのambient fiber diameterは元の尺度でも $O(m_t^{-1})$。$m_t=R_t\to\infty$ とできる。負KE equationにより局所canonical trivialization上で形式がexactとなるのでperiod条件は満たされる。

これらは原稿に条件と証明を保持する局所結果である。Averaging–Moserの基本方法はRuan, arXiv:math/0309177v2, §3に先行し、一般的新規性は未確認。H-minimal/special Lagrangian性、大域接着、singular fibersの計量評価は結論しない。

**解析入力の区別：** 関連KE主稿の `coarse:prop:density-counterexample` により、負KE計量であってもbounded volume densityから一様tensor比較は導けない。五次coarse metric packageには独立な $(\mathrm{TC})_5$ が必要であり、その無条件な検証は未完成である。これは対象compact familyの反例ではない。全深部三重点のfull-orbit moving tensor比較は全固定d≥5で検証した。Source等を含むexterior全体への一様tensor二側比較の拡張は未解決である。本稿の全域距離比較は別のscalar/portal評価により得た。

### Averaging–Moserの先行研究
W.-D. Ruan, *H-minimal Lagrangian fibrations in Kähler manifolds and minimal Lagrangian vanishing tori in Kähler–Einstein manifolds*, arXiv:math/0309177v2, https://arxiv.org/abs/math/0309177v2 。§3 Proposition 3.1はpotentialのtorus平均、Lemma 3.3はHamiltonian-gradient flowを扱い、Theorem 3.1はhomothetic toric potentialと一様 $C^\infty$ quasi-isometryの下でH-minimal fibrationを構成する。Theorem 4.2はsimple toroidal canonical degenerationの最大退化点へ消えるminimal torusの存在を示す。

本研究の補題はperiod-zero、$C^0$ tensor比較、短い生成場だけを用いてprimitiveとambient diameterを直接評価する。Ruanの高階幾何とH-minimal性の結論は求めない。既存方法の定量化として位置付け、新規性は未確認。ZhangのTheorem 2.6の個別generalized special Lagrangian torusの存在とも、全域のsingular fibrationとも区別する。

### 固定領域と移動領域の区別・相対接着への入口
主稿 `ke:fixed-simplex-scale` の計算により、固定simplex compactaは径の尺度のtriple vertexしか見ない。関連KE研究ノートの「固定領域の収束から径の尺度へ移る際の障害」に、固定compacta上ではcusp metricと完全一致し、全体で一様に粗比較できるにもかかわらず、正規化した区間長が $1$ から $3/2$ に変わる一次元例を証明付きで収録した。KE反例ではなく、sharp moving estimatesの必要性を示す例である。

主稿 `ke:relative-fiber-preserving` は、torus-saturatedな**開**collar N上で元のorbitsが既にactual ω-Lagrangianであれば、β=Hω、H=K_1+A_1K_2というchain primitiveがvertical vectorsを消すことを用いる。ω_sも同じvertical distributionをLagrangianに保つため、Moser場はverticalであり、各fiberと基底値が保存される。ωの作用不変性は不要。Centered chain primitiveでも同じ証明が成立するが、同じdβを持つ任意のprimitiveへの置換では消滅条件が保存されるとは限らない。

`ke:relative-neck-matching` は、別のactual Lagrangian fibrationがこの開overlap上で同じorbit partitionを持つなら、基底collarを同定して写像を接着できるという局所系である。各点の固定や単一境界上の一致だけを用いた接着は主張しない。点ごとの固定が必要なら、既存の `ke:relative-averaging` のcentered kernel 1/2−sと作用不変collarを使える。許容射影と遅い対角選択では共通葉・normal moment・bufferを `ke:neck-corner-saturated-union` で実証した。独立な第二periodの一致は含まない。

定数係数monomial変更ζ'=c(t)ζ^A、A∈GL(2,Z)はphase orbit partitionを保つ。一方、非定数holomorphic unitを含む変更ζ'=ζ^A u(ζ,t)は一般に保存しない。二つのtorus actionsが同じoverlapに存在するだけでは相対補題の仮定にならない。Sourceのcritical valuesについても `ke:source-marking` のcore交差仮定の下でp_T(b_t)→e_i+e_jが必要であり、固定された任意の内部markingは使えない。


## 相対接着の補助計算：primitiveの選択と障害

以下はregular torus領域での補助計算であり、仮定と証明をこのノートに保持する。主稿の `ke:relative-fiber-preserving` の証明を重複させず、primitiveの変更、整数基底の変更、collarの点固定に関する情報を整理する。選んだneckとcornerの共通葉・normal moment・bufferは上記部分fibrationで実証した。任意に独立先指定した第二periodの一致には追加確認が必要であり、補助計算の新規性も未確認である。

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

**適用先。** 全域構成・基底値整合・全moment接続・全fiber合併・no-shortcut/portalの各証明は主稿に保持する。上の相対classの条件は点固定germを指定する別問題に有効であり、actual linkからの構成と混同しない。Potential連続度の十分条件も未検証入力として保持するが、P0の径評価には不要である。


## 複素次元2：先行研究・singular fibersの確定事項
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
曲面基底 \(B_d(T)\) の三価木 \(T_{ij}\) を収縮する既存の \(q:B_d(T)\to\operatorname{Sk}_2\Delta^{d-1}\) と、KE候補 \(\mathcal C_d\) の正規化同相の逆を合成すると、**labelを保ち点逆像が可縮な** \(p_T:B_d(T)\to\mathcal C_d\) を得る。一般次数の厳密な証明は `papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`。\(d=5\) では同相、\(d\ge6\) では両者は同相ではない（辺の局所分岐次数が異なる）。この位相的比較単独ではKEのGH極限や作用アフィン計量との一致を結論しない。Actual ambient距離でのGH実現には `ke:global-metric-realization` の解析と接着を用いる。

整数鎖複体の主張を検査するため、\(d=5,\dots,8\) の \(B_d(T)\) と \(\operatorname{Sk}_2\Delta^{d-1}\) の \(\partial_1,\partial_2\) の階数を独立に計算して、\(b_1=0\)、\(b_2=\binom{d-1}{3}\) と一致した。再現コードは `verification/verify_ke_base_topology.py`。これは有限体 \(\mathbb F_{1000003}\) 上の有限検算であり、整数係数の一般定理の証明は本文のexplicit chain contractionが担当する。


## Cubical targetの非伸長retraction・六次以上の厳密直径

**既知の組合せ的構成との関係。** $\mathcal C_d$ のcellは $\varnothing\ne A\subseteq B$、$|B|\le3$ の区間に対応するので、単体二骨格のcubical barycentric subdivisionである。この同定はfaceの式から直接確認できる。E. K. Babson, L. J. Billera, C. S. Chan, *Neighborly cubical spheres and a cubical lower bound conjecture*, Israel J. Math. 102 (1997), 297–315, DOI [10.1007/BF02773804](https://doi.org/10.1007/BF02773804) の1996年preprint §2.3、Proposition 2.2、Corollary 2.4に対応する。[確認した一次scan](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Billera/BilleraEhrenborgcdindex.pdf) は論文が連結・逆順になっており、PDF第24頁が本文p.6、第30頁が対象の表題・著者・日付。書誌は[著者の刊行論文一覧](https://pi.math.cornell.edu/~billera/research.html)とも照合した。既知の細分の構成と、今回のunit-square長さ距離の非伸長retraction・厳密直径とは区別する。後者に一致する既存定理は短い一次文献探索では確認できなかったが、新規性を確定したものではない。

正本は `base_topology.tex` の `topo:coordinate-retraction`、`topo:six-label-gallery`、`topo:diameter-six-labels`。非空Iとanchor a∈Iを選び、外側座標を $r_a=\min(1,\sqrt{w_a^2+\sum_{\ell\notin I}w_\ell^2})$ へまとめる。Euclidean非伸長性に加え、各source squareが一つのtarget cellへ写ることから、内在距離に対する非伸長retractionを得る。したがって $d_I=d_\square|_{\mathcal C_I}$。両端のsupportの和へ縮約できるので、最短路には六label以下で十分。Gallery上限は $3\binom{\min(d,6)}3$ である。

六次以上の直径 $2\sqrt5$ の上界は、共通labelを持つ場合の二square展開と、disjointな三元supportの場合の3L+1Dの四shuffleで証明する。後者の下界は、二組の三labelの個数に応じた9頂点型の値を120個の三角形へaffineに延長するcalibration。四galleryの共有辺・全展開座標、全120三角形の勾配二乗を有理数演算で再実行した。`verification/verify_cubical_six_label_geometry.py` がその再現コードであり、retractionの解析的証明やKE推定の検証ではない。新規性の網羅的確認は未了。

`ke:closed-corner-global-target` は既存closed-cornerのtarget距離を全 $\mathcal C_d$ のものへ置換する。Source側の全曲面ambient下界は `ke:global-ambient-lower` の別の証明で与える。`topo:protected-thin-bypass` は、一般の二square長さ空間で局所の飽和したprotected距離と全域(S),(F)が誤差零でも、細い外側帯によるshortcutが起こる例である。Actual KE族の反例ではない。有限の全被覆でも加法誤差だけでは不足することは、本ノート冒頭の `ke:full-cover-oscillating-bypass` が別に示す。

## 人工的基底計量の鋭い収束速度と幾何学的比較の核心
$p_T:B_d(T)\to\mathcal C_d$ に補助piecewise Euclidean metric $h$ を固定し、$|v|_\varepsilon^2=|dp_T(v)|_\square^2+\varepsilon^2|v|_h^2$ の内在距離を考える。graph correspondenceのdistortion $\mathcal D_\varepsilon$ は、$d=5$ で $\Theta(\varepsilon^2)$、$d\ge6$ で $\Theta(\varepsilon)$ と鋭く決まる（主原稿に読み込む base_topology.tex の topo:metric-collapse-sharp）。$d\ge6$ の下界は同一fiber内の正の $h$-距離に由来するが、**GH距離の下界ではない**。

実際の基底長さ計量 $d_t$ に対する十分条件（topo:finite-portal-criterion）は、(N) global no-shortcut誤差 $\alpha_t$、(S) square segment liftの乗法誤差 $\sigma_t$・加法誤差 $\lambda_t$、(F) 同じfiberの接続費用 $\kappa_t$。十分なsquare数 $N_d=3\binom{\min(d,6)}3$、直径 $D_d$ について
\[
\operatorname{dis}(p_T)\le\max\{\alpha_t,\ \sigma_tD_d+N_d\lambda_t+(N_d+1)\kappa_t\}.
\]
二枚のunit squareを一頂点で貼り、二枚を一枚に折る反例では(N),(S)が誤差零でも(F)が成立せず、$d_{\rm GH}\ge\sqrt2/2$（topo:portal-counterexample）。したがって局所模型だけでは大域収束は言えない。独立のLagrangian action metricの長さ完備化と枝・coreへの延長は本稿の全域実現定理の結論外である。P0では全空間のactual ambient距離に直接no-shortcut・portal評価を証明した。新規性は未確認。


## 六次Petersen分岐基底の対称性
$d=6$ で全ての頂点リンクをPetersenグラフとするラベル付き木系はちょうど六つであり、$S_6$ はこの集合に推移的に作用する。固定した一系の安定化群は位数 $6!/6=120$、指数6。従ってその一系の選択は座標置換の全 $S_6$ 対称性を保たない。KE候補 $\mathcal C_6$ は自然に $S_6$ 対称なので、Petersen分岐基底とのラベル付き比較を対称に行うには六つの木系全体を管理する必要がある。証明は base_topology.tex の topo:petersen-symmetry、全15 perfect matchingsと六one-factorizationsの有限列挙・安定化群位数は別に確認した。これは任意の別構成やラベル忘却後のシンプレクティックな対称性の不存在ではない。

## 検証状態


2026-11-21 / v3.4：主稿改訂24では、共通anchorによる保持neckの正確なmoment範囲と、同一momentの旧corner辺参照torusによる全域基底値比較を明示した。固定残余基底のMoser被覆・同一moment接続・中央帯評価を、十分大きい有限cutにも一様に適用できる定理文へ整理した。追加証明と接続を内部点検中。現行改訂24の組版・表示確認は未実行で、直近に確認したPDFは改訂23の251頁・指定23頁である。整数検算suite・他論文・TeX研究ノートの組版は今回は未実行。形式証明・全主稿と全外部入力の包括的再監査・外部査読・網羅的新規性確認は未実施。
