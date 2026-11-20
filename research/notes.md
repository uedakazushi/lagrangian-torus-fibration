# 研究ノートの入口

詳細な現行ノートは `papers/research-notes.tex`（曲面第25版、65頁）に移行した。証明を短い要約で置き換えない。

## 曲面：現在の核心
全pair productsが狭義正の四ray整数データの正weightsはmatchingと同値。G5_14両単位枝の{5,0,0}を排除し、{4,1,0}に限定したと原稿は記録する。必要支持はG5_14、G5_16、G5_17の3型26標識。存在・幾何的非同型類の個数とは異なる。三高Dの一般同時非負性と一般分母剛性は残る。

## KE退化との分岐基底の位相的比較（新たに証明）
曲面基底 \(B_d(T)\) の三価木 \(T_{ij}\) を収縮する既存の \(q:B_d(T)\to\operatorname{Sk}_2\Delta^{d-1}\) と、KE候補 \(\mathcal C_d\) の正規化同相の逆を合成すると、**labelを保ち点逆像が可縮な** \(p_T:B_d(T)\to\mathcal C_d\) を得る。一般次数の厳密な証明は `papers/sections/paper/base_topology.tex` の `topo:KE-cubical-comparison`。\(d=5\) では同相、\(d\ge6\) では両者は同相ではない（辺の局所分岐次数が異なる）。KEのGH極限や作用アフィン計量との一致は主張しない。

整数鎖複体の主張を検査するため、\(d=5,\dots,8\) の \(B_d(T)\) と \(\operatorname{Sk}_2\Delta^{d-1}\) の \(\partial_1,\partial_2\) の階数を独立に計算して、\(b_1=0\)、\(b_2=\binom{d-1}{3}\) と一致した。再現コードは `verification/verify_ke_base_topology.py`。これは有限体 \(\mathbb F_{1000003}\) 上の有限検算であり、整数係数の一般定理の証明は本文のexplicit chain contractionが担当する。

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

## 三次元：管状補集合とfocus境界の整数位相
**曲線の構成：** d≥6、e=d−2。平面曲線C_eを含むsmooth hypersurfaceはF=q_eR_2+z_3G_{d−1}+z_4H_{d−1}のfirst-jet生成から取れる。Normal完全列より det N_{C_e/Y_d}=O_{C_e}(e+2−d)=O_{C_e}。Ehresmann–Moser移送したC'⊂X_dのsymplectic normalは自明、genusはg=(d−3)(d−4)/2。一般のnormal-trivial symplectic curve（degree e, genus g）には2g−2=(d−5)eが必要で、d偶数ならe偶数（主稿の tnc:degree-genus-parity）。Holomorphic normal rank-two bundleそのものの自明性は主張しない。

**管状補集合の整数homology：** 小さいnormal disk bundle N(C')の補集合V_0=X_d＼int N(C')では、Lefschetz・Thom長完全列により
\[
H_3(V_0;\mathbb Z)\simeq \mathbb Z^{b_d}\oplus\mathbb Z/(d-2),\qquad
H_4(V_0;\mathbb Z)\simeq\mathbb Z^{2g},\qquad
b_d=d^4-5d^3+10d^2-10d+4.
\]
Torsionはnormal meridian S³のclassから生じる（tnc:tubular-homology）。六次ではH_3(V_0)=Z^{520}⊕Z/4、H_4(V_0)=Z^6。X_dの整数cohomologyの一次資料はO. Randal-Williams, Math. Ann. 391 (2025), 1965–2003, §2.1, DOI 10.1007/s00208-024-02951-4。

**Actual focus blockは別の位相：** 構成済みU=C'×K_cのnormal factorは、Q=|XY−c|²が正の区間に入るfocus block。Arg(XY−c)へ巻数1のloopが存在するのでH_1(K_c)はZを直和因子に持ち、K_cはD⁴とhomotopy equivalentでない（tnc:focus-nondisk）。境界∂K_cは一つのfocus–focus点の周りのT²-bundleで、monodromyはprimitive unipotent、基本群は整数Heisenberg群、H_1=H_2=Z²（tnc:focus-boundary-homology）。Closed-curve face ∂U=C'×∂K_cのBetti数は
\[
(1,\,2g+2,\,4g+3,\,4g+3,\,2g+2,\,1),
\]
六次では(1,8,15,15,8,1)（tnc:focus-boundary-betti）。**V_0と実際のUの補集合VのEuler数は一致するが、H_3(V)にZ/(d−2)が残るとはまだいえない。** Ambientのπ_3(X_d)に現れる既知のZ/dとも別の不変量。

**Euler予算：** χ(U)=−(d−2)(d−5)、χ(V)=−(d⁴−5d³+9d²−3d−10)。六次ではχ(V)=−512。Euler数非零fiberが有限個の孤立基底点にだけ存在してすべて−1なら512個必要（tnc:complement-singularity-budget）。正次元特異strataではcompact-support Euler数で重み付けし、一般のglobal Lagrangian fibrationの実現数には外挿しない。

**核心と次の一手：** 相対対(K_c,∂K_c)、境界包含∂U→Uおよび∂U→Vの整数homology・基本群写像、meridional classの像、monodromy/Maslov/action periodsを計算してから、補集合のsingular strataとnormal facesの接着へ進む。これらの境界写像とglobal fillingは未構成。

## 検証
移行時にWorkがv25の五主検算と五独立監査を再実行した。今回の新規トポロジー命題は原稿で論証し、次数ごとのEuler数とWang行列を独立検算したが、保存済み検算スクリプトの最新版全体は今回再実行していない。保存済みの旧verification/証明書全体を今回の実行結果とは扱わない。詳細はmigration.md。計算は解析的symplectic gluingや新規性の証明を代替しない。
