# Lagrangian torus fibrations on general-type surfaces
2026-11-21 / v3.3 — [研究方針](00_research_plan.md) · [研究ノート](research/notes.md) · [Cloud Codexの再開手順](research/cloud-codex.md) · [research-hub](https://github.com/uedakazushi/research-hub)

**各固定次数 \(d\ge5\) の一般位置全平面退化について、actual負Kähler–Einstein形式の大域Lagrangian torus fibrationが、径の尺度のGH極限を実現する定理の証明を主稿に置いている。** 同じ写像 \(f_t=p_T\pi_t\) の全曲面ambient距離に関する一様distortionと、特異fiberを含む全fiber合併の収縮を扱う。今回の新証明と接続を複数担当で内部点検した。形式証明、全主稿・全外部入力の包括的再監査、外部査読、新規性の網羅的確認は未実施である。**このリポジトリは複素次元2専用**。三次元の研究は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) を正本とする。

## 全域実現定理の内容

\(\operatorname{Ric}(\omega_t)=-\omega_t\)、\(R_t=\log(-\log|t|^2)\) とし、actual \(\omega_t\)-Lagrangianな大域fibration \(\pi_t:X_t\to B_d(T)\) を、標識付き基底収縮 \(p_T:B_d(T)\to\mathcal C_d\) と合成して
\[
\sup_{x,y\in X_t}\left|R_t^{-1}d_{g_t}(x,y)-d_\square(p_T\pi_t(x),p_T\pi_t(y))\right|\longrightarrow0
\]
を証明した。対象族は平面が一般位置、\(F_d\) が全三重点で非零かつ各二重線で相異なる単純零点を持ち、小さい非零parameterで滑らかという既存の一般性条件を満たす。全曲面のambient距離を用い、source・branch・coreの全特異fibersを含む。\(d\ge6\) では \(p_T\) が潰す内部木上の複数のfibersの合併全体も収縮する。主張は `ke:global-realization`、統合証明は [ke_global_metric_realization.tex](papers/sections/paper/ke_global_metric_realization.tex) の `ke:global-metric-realization`、定数と選択の範囲は [研究方針](00_research_plan.md) を参照。

証明は十分遅い対角選択と一つの許容された標識付き木系を用いる。最適収束速度、任意に先指定した木系への適合、次数一様性、全次数のmatroidal atlas、special Lagrangian性は結論に含めない。関連KE研究のCP/PBE/TCを証明したとはせず、本稿ではscalar Schwarz障壁による下界とportal接続による上界で代替する。必要な外部入力の所在と仮定は [依存関係表](research/ke-dependencies.md) にまとめる。従来の大域構成・作用適合atlas・整数接着の有効な成果も保持する。

## Cloud Codexから再開する

最新mainで [研究方針](00_research_plan.md) → [AGENTS.md](AGENTS.md) → [依存関係](research/ke-dependencies.md) → [研究ノート](research/notes.md) を読む。次に `ke:global-metric-realization` から依存する接着・source・scalar・portalの証明をたどる。現在の優先課題は、公表に向けた一次文献と依存結果の包括的再点検、新規性の確認、主稿構成の整頓である。改訂23ではsourceの特異reductionと全段階に共通な標識付き木の補題を明示し、K2の全交わりの証明を補強した。追加証明は独立点検中で、改訂23は未組版。改訂22ではcomponentの対数接続費用と全fiber予算を強め、coreの弱い層別構造を明示した。組版・表示確認の現在の状態は末尾を参照。

```sh
python3 scripts/research_check.py setup --require-tex
python3 scripts/research_check.py static
python3 scripts/research_check.py tex
```

環境要件・そのまま渡せる開始指示・必要な範囲の検証方法は [Cloud Codexの再開手順](research/cloud-codex.md)。通常の研究継続・コミット・mainへの保存は承諾を求めず行い、**切りのよいところで、長くても前回成功pushから約15分を目安に有効な現行成果を保存**しながら、方針の達成条件に沿って研究を進める。保存が必要でも未完成の証明を完成と記さず、他者変更を保持する。これらのファイルは再開・実行のための指示であり、Cloudサービス側の環境設定や新規タスク起動を自動的に行うものではない。

## 論文と役割

| 原稿 | 役割 | 組版の確認範囲 |
| --- | --- | ---: |
| [主原稿](papers/surface-lagrangian-torus-fibration.tex) | 相対SNC構成・次数分割・分岐底・作用適合atlas、actual KE全域fibrationによるGH実現定理（改訂22） | 改訂22：246頁、変更箇所を含む23頁を表示確認 |
| [五次整数接着](papers/quintic-integer-gluing.tex) | 指定K5データの整数条件・高分母支持・未解決の大域接着 | 201頁 |
| [Meridian surgery](papers/meridian-surgery.tex) | 閉corner circuitsの局所置換の障害 | 18頁 |
| [TeX研究ノート](papers/research-notes.tex) | 証明素材・残る条件の整理 | 現行65頁、第1・4頁を表示確認 |

## 主な到達点と残る課題
指定hyperplane Kähler classでの正則Lagrangian \(T^2\) と、分岐辺上の \(S^1\times(S^1\vee S^1)\)、面内のpinched torus、core上のlogarithmic Weinstein skeletonを扱う。五次は(cores, branch edges, nodes)=(5,10,50)、六次は(6,30,90)で、分岐辺数は無限個のfiberの個数ではない。通常のalmost toric fibrationを超える特異模型を用いるため、Leung–Symingtonの分類と矛盾しない。全大域接着の公表前監査はなお必要。

五次整数アフィン接着では、四rayの完全matching条件等を証明し、高分母の必要支持候補を \(G_{5,14},G_{5,16},G_{5,17}\) の3型・26標識まで絞った。ただし26は実現数ではなく、一般分母の剛性・三高係数の同時非負性や全支持型の大域接着は未解決。

KE退化との関連では、全閉triple cornerのactual局所GH収束、定量的二段階平均、固定残余基底のactual neckとsourceのpinched torusを得ている。現行主稿の主要結果は次の通り。

- **同じnormal moment上の接続：** 固定source-free基底の残余点全体をactual長さ $O(1)$ で結ぶ。Moser像と、同じlevel上の複数fiberの合併も、正規化ambient径 $O(R_t^{-1})$ を持つ（`ke:fixed-base-moment-connectors`）。
- **三つの端の座標と作用：** 固定深度比で分離したarmで、射影neck座標との比の対数を全固定階で指数的に評価。積を保つsmooth補間で三端のnormal circlesを同時に合わせ、canonical normal periodの厳密な一致を示す。非正則な補間帯ではtame symplectic性を使う（`ke_neck_corner_transition.tex`）。
- **一つのcorner bundleへの統合：** 平均順序を比較するHamiltonianを $O(m^{-2})$ で評価してcutoffし、各端のnormal-first構成を相対統合する。単一moving armでは共通moment intervalを両端の漸近から構成し、actual reduced葉が小さいgraphとなることを示す。Collar外を固定して延長できる（`ke_relative_corner_patch.tex`）。第二periodの一致は自動でない。
- **遅いcutでも局所GH近似：** $m_t\to\infty,\ \log m_t=o(R_t)$ なら、内在・protected距離のdistortionは $C[m_t^{-1}+(\log(m_t+1)+\log R_t)/R_t]$。固定領域の列に合わせたstepwiseな対角選択にも使える（`ke:slow-cut-closed-corner-gh`）。

- **全交わりで葉が一致する部分fibration：** 残余compact、normal cutoff、moment区間、parameter閾値の順に選び、全flowの共通開領域を構成する。Corner cut $m_t=6b_j$ とneckの葉でのtrim $B=7b_j$ を離して選び、first-exitと逆normal flowの自然性により、全intersectionが双方の全fibersで飽和することを証明した。Source・saddleの局所型を保って貼り合わせられる（`ke:neck-corner-saturated-union`）。
- **Central sourceのactual経路評価：** 固定rescalingでdensityは $L_t^{-2}$、canonical potentialは有界、normal momentは $O(L_t^{-1})$。Traceと平均二乗距離は $O(1)$、全中央点からgateへの退出は $O(L_t^{-1/2})$、oriented arm断面へは $O(1)$ で接続できる（`ke_source_connectors.tex`）。Source-freeな $|\mu|\le A/M_t$ のcentral band全体もactual径 $O(1)$。Source側では正のpotentialの対数勾配でactual球を深部に閉じ込め、complex SobolevのGaussian積分とBishop–Gromov比較から、固定点を含む中央coreの全点径 $O(1)$ を証明した。固定基底のsource-inclusive中央帯と閉pinched torus全体も正規化ambient径で収縮する。Potentialの一様square-root-Dini modulusを仮定する十分条件も示し、そのmodulus自体は未検証と区別する。
- **全momentのsource退出：** `ke:source-arm-uniform-tensor` は、三種類の境界でnormal covectorを制御し、source軸を含むoriented armの二側tensor比較を与える。固定normal座標での水平経路と動径補正により、`ke:source-all-moment-exit` の費用は全共通intervalで $O(1)$。中央固定点も短いgate退出と同じarm比較で扱えるため、この接続定理はGaussian可積分性に依存しない。同一momentの全fiber合併は固定基底で非正規化径が有界となる。

固定source chartのEuler場による明示的なresidual接続も保持する。成分coreではcanonical primitiveの差から固定領域のactual移送を構成し、境界を固定する相対flux条件とexactな平均化germを明示した（`ke_component_core_transfer.tex`）。`ke_component_core_geometry.tex` は任意固定compactと全collar上でKE形式・primitiveを保つsmooth正則化、正residueの有限型KE core、その小さい飽和近傍のmarked Lagrangian fillingを与える。全域への相対接着は下記四節で証明した。

**Actual KE形式上の全域接着：** `ke_component_link_cover.tex` で正residue periodを既存momentsと厳密に合わせ、閉linkと全特異層近傍の固定段階被覆を構成する。`ke_core_invariant_primitive.tex` はgeneratorのC1評価、exact scalar平均と全cutoff支持の被覆から、core外にtrappingを作らないadapted primitiveを得る。`ke_relative_reduced_foliations.tex` はsaddleを動かしてfull critical leavesを保つ。`ke_actual_core_gluing.tex` の `ke:actual-global-fibration` はLiouville cone fillingと全fiber単位のtrimにより、全 $X_t$ を覆うactual fibrationへ接着する。追加証明は別担当と内部点検済み。内側のprimitiveをcompact-relative Morse–Smaleに選び、index順の閉isotropic filtrationを得た。Skeletonの連結性は負時間像のnested intersectionから直接示す。各componentのcoreと変更collarは $C(1+\log(N_j+1))$ のactual ambient接続費用を持ち、十分遅い対角選択で正規化径が消える。

**Core cutのtarget像：** 固定成分のstrictly plurisubharmonic potentialへ最大原理を使い、切り取った各coreの二つの独立深度を $CN_j$ 以下に抑えた。各capの旧softmax像は成分頂点の $\sqrt2\log(CN_j)/R_t$ 近傍に入る（`ke:removed-corner-target-cap`）。保持cornerには旧protected距離の評価が残り、旧corner内の経路は全曲面距離の上界に使える。旧softmax値と $p_T\pi_t$ の整合は次の構成で与える。

**全域基底の整合：** `ke:global-base-parameterization` により、全保持cornerで旧softmax値との誤差は $O((1+\log N_j)/R_t)$。正則torusを持つ旧辺をtriangleの少し内側へ送り、core panelsとneck stripsを明示的に貼り合わせる。潰される内部木には全枝共通のcanonical momentを使う。

**全曲面の距離下界：** `ke:sharp-global-one-active` はsourceを含む正則normal frameに対する係数 $1+o(1)$ のscalar評価を与える。二active方向は既存full-triple比較で扱い、`ke:global-depth-lipschitz` で全曲線の長さを先に評価する。`ke:global-depth-base-comparison` により同じ $f_t$ と一様に比較し、`ke:global-ambient-lower` を得る。経路の領域間往復回数を仮定しない。

**全曲面の距離上界とfiber合併：** `ke:global-ambient-upper` は、旧cornerの経路、全moment source退出、同じmomentのneck全体、各componentの対数費用と有限portal galleryを組み合わせる。Anchor interval外のneck尾部にも深度 $CN_j$ を証明し、残余基底の接続定数を先に選んで $1+\log(N_j+1)$ に吸収する。全接続予算は $H_{j,t}=C(1+\log(N_j+1))$、上界誤差は $C_d\{b_j^{-1}+(1+\log R_t+\log(N_j+1))/R_t\}$。このcut選択から最適収束速度は結論しない。`ke:collapsed-tree-full-fiber-collapse` は六次以上の内部木上の全fiber合併も評価する。各componentのcore径評価を、異なるcore全部の合併径やfiber内在径と取り違えない。これらを `ke:global-metric-realization` で同じ全射 $f_t=p_T\pi_t$ のdistortion消失へ統合した。

公表前には、依存する既存証明と一次文献の包括的再点検、新規性確認、主稿の全体点検が必要である。確認済みの範囲は [検証状態](research/validation.json) に分けて記録する。

## 極限候補の有限距離幾何

座標部分複体への明示的な非伸長retractionにより、全targetの最短路を六つ以下のlabelへ還元できる。Closed-cornerの三枚のsquareは全targetに等長に埋め込まれ、portal比較のgallery数は五次30、六次以上60で足りる。

六次以上では **$\operatorname{diam}(\mathcal C_d,d_\square)=2\sqrt5$**。最大対は互いに素な三元supportのall-ones頂点対に限る。四つのsquare galleryによる上界と120三角形のPL calibrationによる下界を証明し、有限部分を有理数演算で独立検算した。この直径定理は既存の五次の値 $\sqrt{13}$ に依存しない。全域実現定理と合わせ、六次以上ではactual KE曲面の $R_t^{-1}\operatorname{diam}(X_t,g_t)\to2\sqrt5$ を得る。

## ビルドと再現

repo直下で `latexmk papers/surface-lagrangian-torus-fibration.tex`、`latexmk papers/quintic-integer-gluing.tex`、`latexmk papers/meridian-surgery.tex`。LuaLaTeX、LuaTeX-ja、日本語フォント、TikZを使用し、PDF/SyncTeXは `build/`。計算の入口は `python3 verification/run_current_checks.py`。ソースと証明書は `papers/sections/` と `verification/`。PDFはGitで追跡しない。

2026-11-21 / v3.2：主稿改訂22に対数接続費用・全fiber予算・coreの弱い層別構造を統合し、追加証明と主要接着依存を複数担当で内部点検した。静的構成検査は通過。改訂22はLuaLaTeXで246頁に組版済み。第1・2・17・18・132–134・155–160・179–184・241–243・246頁の計23頁を表示確認した。未解決参照・引用、重複ラベル、欠字、overfull警告はない。TeX研究ノートは既存65頁の組版記録を維持する。今回、整数検算suite・他論文の組版は再実行していない。形式証明・全主稿と全外部入力の包括的再監査・外部査読・網羅的新規性確認は未実施。
