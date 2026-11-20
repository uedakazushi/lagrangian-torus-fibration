# 研究ノートの入口

詳細な現行ノートは `papers/research-notes.tex`（曲面第25版、65頁）に移行した。証明を短い要約で置き換えない。

## 曲面：現在の核心
全pair productsが狭義正の四ray整数データの正weightsはmatchingと同値。G5_14両単位枝の{5,0,0}を排除し、{4,1,0}に限定したと原稿は記録する。必要支持はG5_14、G5_16、G5_17の3型26標識。存在・幾何的非同型類の個数とは異なる。三高Dの一般同時非負性と一般分母剛性は残る。

## KE退化との分岐基底の位相的比較（新たに証明）
曲面基底 \(B_d(T)\) の三価木 \(T_{ij}\) を収縮する既存の \(q:B_d(T)\to\operatorname{Sk}_2\Delta^{d-1}\) と、KE候補 \(\mathcal C_d\) の正規化同相の逆を合成すると、**labelを保ち点逆像が可縮な** \(p_T:B_d(T)\to\mathcal C_d\) を得る。一般次数の厳密な証明は `papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`。\(d=5\) では同相、\(d\ge6\) では両者は同相ではない（辺の局所分岐次数が異なる）。KEのGH極限や作用アフィン計量との一致は主張しない。

整数鎖複体の主張を検査するため、\(d=5,\dots,8\) の \(B_d(T)\) と \(\operatorname{Sk}_2\Delta^{d-1}\) の \(\partial_1,\partial_2\) の階数を独立に計算して、\(b_1=0\)、\(b_2=\binom{d-1}{3}\) と一致した。再現コードは `verification/verify_ke_base_topology.py`。これは有限体 \(\mathbb F_{1000003}\) 上の有限検算であり、整数係数の一般定理の証明は本文のexplicit chain contractionが担当する。

## 三次元normal-trivial closed curveの代数的点検
原稿の `papers/sections/threefold/local_blocks/trivial_normal_curve.tex` にある代数的構成を直接点検した。\(e=d-2\) のsmooth plane curve \(C_e\subset\mathbf P^2\subset\mathbf P^4\) を含む次数 \(d\) 超曲面を
\[
F=q_eR_2+z_3G_{d-1}+z_4H_{d-1}
\]
の一般元として選ぶ。曲線外では一次jet生成、曲線上では三つのnormal一次jetの独立性により一般元はsmoothになる。normal exact sequenceは
\[
0\to N_{C_e/Y_d}\to
\mathcal O_{C_e}(e)\oplus\mathcal O_{C_e}(1)^{\oplus2}
\to\mathcal O_{C_e}(d)\to0,
\]
よって \(\det N_{C_e/Y_d}\simeq\mathcal O_{C_e}(e+2-d)\simeq\mathcal O_{C_e}\)。これはholomorphic determinantの自明性であり、holomorphic rank-two bundle自体の自明性を意味しない。しかし閉曲面上のcomplex rank-two bundleは \(c_1\) でsmooth分類されるので、symplectic normal bundleは自明。\(g=(d-3)(d-4)/2\) かつ \(n=(d-2)(d-5)=2g-2\) は偶数で、三価graphの \(V=n,E=3n/2,b_1=g\) と一致する（六次では \(g=3,V=4,E=6\)）。指定した一般の \(X_d\) とKähler formへのEhresmann+Moser移送は原稿の別の補題である。Actual Lagrangian whole fibersの解析とglobal gluingはこのChern計算だけでは従わない。

## 三次元：局所稿の参照先
`papers/threefold-blocks.tex`第25・33節：positive normal shell、membrane/focus collars。第26節：smooth focus Cartanとnormal degreeの障害。第34–35節：compact focus blockとnormal-trivial closed curve。第36節：weighted collars。旧48 ports、normal faces、complement、大域boundary-free fibrationは未完成。全体稿は `papers/threefold-fibration.tex`。

## 人工的基底計量の鋭い収束速度と幾何学的比較の核心
$p_T:B_d(T)\to\mathcal C_d$ に補助piecewise Euclidean metric $h$ を固定し、$|v|_\varepsilon^2=|dp_T(v)|_\square^2+\varepsilon^2|v|_h^2$ の内在距離を考える。graph correspondenceのdistortion $\mathcal D_\varepsilon$ は、$d=5$ で $\Theta(\varepsilon^2)$、$d\ge6$ で $\Theta(\varepsilon)$ と鋭く決まる（主原稿に読み込む base_topology.tex の topo:metric-collapse-sharp）。$d\ge6$ の下界は同一fiber内の正の $h$-距離に由来するが、**GH距離の下界ではない**。

実際の基底長さ計量 $d_t$ に対する十分条件（topo:finite-portal-criterion）は、(N) global no-shortcut誤差 $\alpha_t$、(S) square segment liftの乗法誤差 $\sigma_t$・加法誤差 $\lambda_t$、(F) 同じfiberの接続費用 $\kappa_t$。最大square数 $N_d=d\binom{d-1}{2}$、直径 $D_d$ について
\[
\operatorname{dis}(p_T)\le\max\{\alpha_t,\ \sigma_tD_d+N_d\lambda_t+(N_d+1)\kappa_t\}.
\]
二枚のunit squareを一頂点で貼り、二枚を一枚に折る反例では(N),(S)が誤差零でも(F)が成立せず、$d_{\rm GH}\ge\sqrt2/2$（topo:portal-counterexample）。したがって局所模型だけでは大域収束は言えない。実際のLagrangian action metricの長さ完備化、枝・coreへの延長、および(N),(S),(F)の確認は未解決。新規性は未確認。

## 六次Petersen分岐基底の対称性
$d=6$ で全ての頂点リンクをPetersenグラフとするラベル付き木系はちょうど六つであり、$S_6$ はこの集合に推移的に作用する。固定した一系の安定化群は位数 $6!/6=120$、指数6。従ってその一系の選択は座標置換の全 $S_6$ 対称性を保たない。KE候補 $\mathcal C_6$ は自然に $S_6$ 対称なので、Petersen分岐基底とのラベル付き比較を対称に行うには六つの木系全体を管理する必要がある。証明は base_topology.tex の topo:petersen-symmetry、全15 perfect matchingsと六one-factorizationsの有限列挙・安定化群位数は別に確認した。これは任意の別構成やラベル忘却後のシンプレクティックな対称性の不存在ではない。

## Symplectic normalが自明な閉曲線と補集合のEuler予算
三次元の原稿 trivial_normal_curve.tex の tnc:degree-genus-parity は、任意のsmooth $X_d\subset\mathbf P^4$（$d\ge6$）のnormal-trivialなclosed symplectic curve $S$ について、hyperplane degreeを $e>0$ とすれば
\[
2g(S)-2=(d-5)e
\]
と示す。従って$d$偶数なら$e$偶数。曲線方向の三価Reeb graphの頂点数も（局所Morse構成の仮定下で）$(d-5)e$ に固定される。これだけでは埋込みやglobal fibrationは得られない。

構成済みblock $\mathcal U$ とcompact complement $\mathcal V$ には
\[
\chi(\mathcal U)=-(d-2)(d-5),\quad
\chi(\mathcal V)=-\mathcal N_d,\quad
\mathcal N_d=d^4-5d^3+9d^2-3d-10.
\]
特に六次では$\chi(X_6)=-516$、$\chi(\mathcal U)=-4$、$\chi(\mathcal V)=-512$。$\mathcal V\to B_{\mathcal V}$ が有限層別局所自明で、Euler数非零のfiberが有限個の孤立基底点$S$にだけ存在すると仮定すれば、
\[
\sum_{b\in S}\chi(f^{-1}(b))=-\mathcal N_d.
\]
非零fiber全てがEuler数$-1$型なら、六次で**512個**必要（tnc:complement-singularity-budget）。特異ファイバーが正次元base stratum上に広がる場合はstratumのcompact支えEuler数 $\chi_c$ で重み付けしなければならず、この個数を一般の全体fibrationへ外挿できない。今後のnormal faces/complement設計では、fiber Euler、area/Maslov、monodromyを併せて検証する。

## 検証
v25の五主検算と五独立監査を今回再実行。保存済みの旧verification/証明書全体を今回の実行結果とは扱わない。詳細はmigration.md。計算は解析的symplectic gluingや新規性の証明を代替しない。
