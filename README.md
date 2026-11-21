# Lagrangian torus fibrations on general-type surfaces
2026-11-21 / v3.0 — [研究方針](00_research_plan.md) · [研究ノート](research/notes.md) · [Cloud Codexの再開手順](research/cloud-codex.md) · [research-hub](https://github.com/uedakazushi/research-hub)

**最優先目標は、本研究の大域Lagrangian torus fibrationが、負Kähler–Einstein計量のGromov–Hausdorff極限を幾何学的に実現すること。現時点では未解決である。** 対象は各固定次数 \(d\ge5\) の一般位置全平面退化 \(X_t\subset\mathbb P^3\)。**このリポジトリは複素次元2専用**。三次元の研究は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) を正本とする。

## 何をもって解決とするか

\(\operatorname{Ric}(\omega_t)=-\omega_t\)、\(R_t=\log(-\log|t|^2)\) とし、actual \(\omega_t\)-Lagrangianな大域fibration \(\pi_t:X_t\to B_d(T)\) を、標識付き基底収縮 \(p_T:B_d(T)\to\mathcal C_d\) と合成して
\[
\sup_{x,y\in X_t}\left|R_t^{-1}d_{g_t}(x,y)-d_\square(p_T\pi_t(x),p_T\pi_t(y))\right|\longrightarrow0
\]
を証明する。全曲面のambient距離を用い、source・branch・coreの全特異fibersを含む。\(d\ge6\) では木上の複数のfibersの合併全体も収縮させる。五次は最初の到達点であり、最終的な次数範囲を五次に限らない。詳細は主稿の未解決問題 `ke:global-realization` と [研究方針のP0](00_research_plan.md)。

既存の局所GH収束や、未証明の解析仮定を残した条件付き大域定理は、この目標の解決とは区別する。必要なKE入力の所在と仮定は [依存関係表](research/ke-dependencies.md) にまとめる。従来の大域構成・作用適合atlas・整数接着の証明は保持し、独立した整数接着分類はこの目標に必要な場合以外は後順位とする。

## Cloud Codexから再開する

最新mainで [研究方針](00_research_plan.md) → [AGENTS.md](AGENTS.md) → [依存関係](research/ke-dependencies.md) → [研究ノート](research/notes.md) を読む。`ke:actual-global-fibration` により、既存neck/cornerの保持葉とsource近傍を保ってcoreへ相対接着し、全曲面上のactual KE–Lagrangian fibrationを構成した。各componentの変更領域の正規化ambient径も消せる。全interval source接続と旧corner値に近い基底parameter化を得た。次は全曲面の距離上下界と木上のfiber合併の評価を統合する。

```sh
python3 scripts/research_check.py setup --require-tex
python3 scripts/research_check.py static
python3 scripts/research_check.py tex
```

環境要件・そのまま渡せる開始指示・必要な範囲の検証方法は [Cloud Codexの再開手順](research/cloud-codex.md)。通常の研究継続・コミット・mainへの保存は承諾を求めず行い、**切りのよいところで、長くても前回成功pushから約15分を目安に有効な現行成果を保存**しながら、方針の達成条件に沿って研究を進める。保存が必要でも未完成の証明を完成と記さず、他者変更を保持する。これらのファイルは再開・実行のための指示であり、Cloudサービス側の環境設定や新規タスク起動を自動的に行うものではない。

## 論文と役割
| 原稿 | 役割 | 組版の確認範囲 |
| --- | --- | ---: |
| [主原稿](papers/surface-lagrangian-torus-fibration.tex) | 相対SNC構成・次数分割・分岐底・作用適合atlas、局所KE収束・actual KE全域構成と大域実現問題（改訂20） | 現行改訂20の組版は未実施。改訂19は211頁で確認済み |
| [五次整数接着](papers/quintic-integer-gluing.tex) | 指定K5データの整数条件・高分母支持・未解決の大域接着 | 201頁 |
| [Meridian surgery](papers/meridian-surgery.tex) | 閉corner circuitsの局所置換の障害 | 18頁 |
| [TeX研究ノート](papers/research-notes.tex) | 証明素材・残る条件の整理 | 65頁 |

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
- **全momentのsource退出：** `ke:source-all-moment-exit` により、共通intervalの全点を同じcanonical momentの残余境界へ $O(\sqrt{\log(R_t+2)})=o(R_t)$ で結ぶ。Normal深度ごとのcover、Gaussian tailとslabの体積尺度の相殺、actual球の局在、出口のmoment補正を証明した。同一momentの全fiber合併も固定基底で収縮する。

固定source chartのEuler場による明示的なresidual接続も保持する。成分coreではcanonical primitiveの差から固定領域のactual移送を構成し、境界を固定する相対flux条件とexactな平均化germを明示した（`ke_component_core_transfer.tex`）。`ke_component_core_geometry.tex` は任意固定compactと全collar上でKE形式・primitiveを保つsmooth正則化、正residueの有限型KE core、その小さい飽和近傍のmarked Lagrangian fillingを与える。全域への相対接着は下記四節で証明した。

**Actual KE形式上の全域接着：** `ke_component_link_cover.tex` で正residue periodを既存momentsと厳密に合わせ、閉linkと全特異層近傍の固定段階被覆を構成する。`ke_core_invariant_primitive.tex` はgeneratorのC1評価、exact scalar平均と全cutoff支持の被覆から、core外にtrappingを作らないadapted primitiveを得る。`ke_relative_reduced_foliations.tex` はsaddleを動かしてfull critical leavesを保つ。`ke_actual_core_gluing.tex` の `ke:actual-global-fibration` はLiouville cone fillingと全fiber単位のtrimにより、全 $X_t$ を覆うactual fibrationへ接着する。追加証明は別担当と内部点検済み。各componentのcoreと変更collarは固定stageでactual径が有界、十分遅い対角選択で正規化径が消える。

**Core cutのtarget像：** 固定成分のstrictly plurisubharmonic potentialへ最大原理を使い、切り取った各coreの二つの独立深度を $CN_j$ 以下に抑えた。各capの旧softmax像は成分頂点の $\sqrt2\log(CN_j)/R_t$ 近傍に入る（`ke:removed-corner-target-cap`）。保持cornerには旧protected距離の評価と全曲面距離の上界が残る。旧softmax値と $p_T\pi_t$ の相対parameterizationは次の課題である。

**全域基底の整合：** `ke:global-base-parameterization` により、全保持cornerで旧softmax値との誤差は $O((1+\log N_j)/R_t)$。正則torusを持つ旧辺をtriangleの少し内側へ送り、core panelsとneck stripsを明示的に貼り合わせる。潰される内部木には全枝共通のcanonical momentを使う。

**P0の距離条件は未解決。** 全interval source接続と基底parameter化を統合し、六次以上で潰される木上の全fiber合併の径、全曲面のshortcutとportal費用を検証する。各componentのcore径評価は、異なるcore全部の合併径やfiberの内在径の評価ではない。局所GH近似のtarget距離は非伸長retractionにより全cubical複体の距離の制限と等しいが、source側のprotected距離を全曲面ambient距離へ置換した下界は未証明。先行研究の仮定と新規性の未確認点は主原稿序論と[研究ノート](research/notes.md)を参照。

## 極限候補の有限距離幾何

座標部分複体への明示的な非伸長retractionにより、全targetの最短路を六つ以下のlabelへ還元できる。Closed-cornerの三枚のsquareは全targetに等長に埋め込まれ、portal比較のgallery数は五次30、六次以上60で足りる。

六次以上では **$\operatorname{diam}(\mathcal C_d,d_\square)=2\sqrt5$**。最大対は互いに素な三元supportのall-ones頂点対に限る。四つのsquare galleryによる上界と120三角形のPL calibrationによる下界を証明し、有限部分を有理数演算で独立検算した。主定理は既存の五次の直径 $\sqrt{13}$ に依存しない。これは候補targetの結果であり、actual KE曲面の直径漸近は未解決の全域距離比較を要する。

## ビルドと再現

repo直下で `latexmk papers/surface-lagrangian-torus-fibration.tex`、`latexmk papers/quintic-integer-gluing.tex`、`latexmk papers/meridian-surgery.tex`。LuaLaTeX、LuaTeX-ja、日本語フォント、TikZを使用し、PDF/SyncTeXは `build/`。計算の入口は `python3 verification/run_current_checks.py`。ソースと証明書は `papers/sections/` と `verification/`。PDFはGitで追跡しない。

2026-11-21 / v3.0：中央全点径 $O(1)$、全moment source退出 $O(\sqrt{\log(R_t+2)})$、旧corner値に近い全域基底parameter化と内部木の共通momentを主稿改訂20へ統合し、追加証明を別担当と点検した。現行改訂20の組版は未実施（直前の改訂19は211頁で組版・28頁の表示確認済み）。形式証明・外部査読・包括的新規性確認・旧整数検算suiteと他三稿の再組版は未実施。P0の全曲面距離の統合は未完了。
