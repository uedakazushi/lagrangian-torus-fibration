# Lagrangian torus fibrations on general-type surfaces
2026-11-21 / v2.8 — [研究方針](00_research_plan.md) · [研究ノート](research/notes.md) · [Cloud Codexの再開手順](research/cloud-codex.md) · [research-hub](https://github.com/uedakazushi/research-hub)

**最優先目標は、本研究の大域Lagrangian torus fibrationが、負Kähler–Einstein計量のGromov–Hausdorff極限を幾何学的に実現すること。現時点では未解決である。** 対象は各固定次数 \(d\ge5\) の一般位置全平面退化 \(X_t\subset\mathbb P^3\)。**このリポジトリは複素次元2専用**。三次元の研究は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) を正本とする。

## 何をもって解決とするか

\(\operatorname{Ric}(\omega_t)=-\omega_t\)、\(R_t=\log(-\log|t|^2)\) とし、actual \(\omega_t\)-Lagrangianな大域fibration \(\pi_t:X_t\to B_d(T)\) を、標識付き基底収縮 \(p_T:B_d(T)\to\mathcal C_d\) と合成して
\[
\sup_{x,y\in X_t}\left|R_t^{-1}d_{g_t}(x,y)-d_\square(p_T\pi_t(x),p_T\pi_t(y))\right|\longrightarrow0
\]
を証明する。全曲面のambient距離を用い、source・branch・coreの全特異fibersを含む。\(d\ge6\) では木上の複数のfibersの合併全体も収縮させる。五次は最初の到達点であり、最終的な次数範囲を五次に限らない。詳細は主稿の未解決問題 `ke:global-realization` と [研究方針のP0](00_research_plan.md)。

既存の局所GH収束や、未証明の解析仮定を残した条件付き大域定理は、この目標の解決とは区別する。必要なKE入力の所在と仮定は [依存関係表](research/ke-dependencies.md) にまとめる。従来の大域構成・作用適合atlas・整数接着の証明は保持し、独立した整数接着分類はこの目標に必要な場合以外は後順位とする。

## Cloud Codexから再開する

最新mainで [研究方針](00_research_plan.md) → [AGENTS.md](AGENTS.md) → [依存関係](research/ke-dependencies.md) → [研究ノート](research/notes.md) を読む。遅い残余exhaustionにより、closed cornerとsource-inclusive neckの全交わりで葉が一致するactual部分fibrationを得た。中央sourceの全点径と固定基底中央帯・閉pinched torusの収縮まで得た。極限KE coreの小さい飽和近傍のfillingと、六次以上のtarget直径 $2\sqrt5$ も得た。次はcore fillingを既存の全collar葉へ相対延長し、中央帯外のsource接続と全曲面の距離比較を進める。

```sh
python3 scripts/research_check.py setup --require-tex
python3 scripts/research_check.py static
python3 scripts/research_check.py tex
```

環境要件・そのまま渡せる開始指示・必要な範囲の検証方法は [Cloud Codexの再開手順](research/cloud-codex.md)。通常の研究継続・コミット・mainへの保存は承諾を求めず行い、**切りのよいところで、長くても前回成功pushから約15分を目安に有効な現行成果を保存**しながら、方針の達成条件に沿って研究を進める。保存が必要でも未完成の証明を完成と記さず、他者変更を保持する。これらのファイルは再開・実行のための指示であり、Cloudサービス側の環境設定や新規タスク起動を自動的に行うものではない。

## 論文と役割
| 原稿 | 役割 | 組版の確認範囲 |
| --- | --- | ---: |
| [主原稿](papers/surface-lagrangian-torus-fibration.tex) | 相対SNC構成・次数分割・分岐底・作用適合atlas、局所KE収束と大域実現問題（改訂18） | 改訂18・188頁、変更箇所を中心に18頁を表示確認 |
| [五次整数接着](papers/quintic-integer-gluing.tex) | 指定K5データの整数条件・高分母支持・未解決の大域接着 | 201頁 |
| [Meridian surgery](papers/meridian-surgery.tex) | 閉corner circuitsの局所置換の障害 | 18頁 |
| [TeX研究ノート](papers/research-notes.tex) | 証明素材・残る条件の整理 | 65頁 |

## 主な到達点と残る課題
指定hyperplane Kähler classでの正則Lagrangian \(T^2\) と、分岐辺上の \(S^1\times(S^1\vee S^1)\)、面内のpinched torus、core上のlogarithmic Weinstein skeletonを扱う。五次は(cores, branch edges, nodes)=(5,10,50)、六次は(6,30,90)で、分岐辺数は無限個のfiberの個数ではない。通常のalmost toric fibrationを超える特異模型を用いるため、Leung–Symingtonの分類と矛盾しない。全大域接着の公表前監査はなお必要。

五次整数アフィン接着では、四rayの完全matching条件等を証明し、高分母の必要支持候補を \(G_{5,14},G_{5,16},G_{5,17}\) の3型・26標識まで絞った。ただし26は実現数ではなく、一般分母の剛性・三高係数の同時非負性や全支持型の大域接着は未解決。

KE退化との関連では、全閉triple cornerのactual局所GH収束、定量的二段階平均、固定残余基底のactual neckとsourceのpinched torusを得ている。現行改訂18の主要結果は次の通り。

- **同じnormal moment上の接続：** 固定source-free基底の残余点全体をactual長さ $O(1)$ で結ぶ。Moser像と、同じlevel上の複数fiberの合併も、正規化ambient径 $O(R_t^{-1})$ を持つ（`ke:fixed-base-moment-connectors`）。
- **三つの端の座標と作用：** 固定深度比で分離したarmで、射影neck座標との比の対数を全固定階で指数的に評価。積を保つsmooth補間で三端のnormal circlesを同時に合わせ、canonical normal periodの厳密な一致を示す。非正則な補間帯ではtame symplectic性を使う（`ke_neck_corner_transition.tex`）。
- **一つのcorner bundleへの統合：** 平均順序を比較するHamiltonianを $O(m^{-2})$ で評価してcutoffし、各端のnormal-first構成を相対統合する。単一moving armでは共通moment intervalを両端の漸近から構成し、actual reduced葉が小さいgraphとなることを示す。Collar外を固定して延長できる（`ke_relative_corner_patch.tex`）。第二periodの一致は自動でない。
- **遅いcutでも局所GH近似：** $m_t\to\infty,\ \log m_t=o(R_t)$ なら、内在・protected距離のdistortionは $C[m_t^{-1}+(\log(m_t+1)+\log R_t)/R_t]$。固定領域の列に合わせたstepwiseな対角選択にも使える（`ke:slow-cut-closed-corner-gh`）。

- **全交わりで葉が一致する部分fibration：** 残余compact、normal cutoff、moment区間、parameter閾値の順に選び、全flowの共通開領域を構成する。Corner cut $m_t=6b_j$ とneckの葉でのtrim $B=7b_j$ を離して選び、first-exitと逆normal flowの自然性により、全intersectionが双方の全fibersで飽和することを証明した。Source・saddleの局所型を保って貼り合わせられる（`ke:neck-corner-saturated-union`）。
- **Central sourceのactual経路評価：** 固定rescalingでdensityは $L_t^{-2}$、canonical potentialは有界、normal momentは $O(L_t^{-1})$。Traceと平均二乗距離は $O(1)$、全中央点からgateへの退出は $O(L_t^{-1/2})$、oriented arm断面へは $O(1)$ で接続できる（`ke_source_connectors.tex`）。Source-freeな $|\mu|\le A/M_t$ のcentral band全体もactual径 $O(1)$。Source側では正のpotentialの対数勾配でactual球を深部に閉じ込め、complex SobolevのGaussian積分とBishop–Gromov比較から、固定点を含む中央coreの全点径 $O(\sqrt{R_t})$ を証明した。固定基底のsource-inclusive中央帯と閉pinched torus全体も正規化ambient径で収縮する。Potentialの一様square-root-Dini modulusを仮定する十分条件も示し、そのmodulus自体は未検証と区別する。

固定source chartのEuler場による明示的なresidual接続も保持する。成分coreではcanonical primitiveの差から固定領域のactual移送を構成し、境界を固定する相対flux条件とexactな平均化germを明示した（`ke_component_core_transfer.tex`）。`ke_component_core_geometry.tex` は任意固定compactと全collar上でKE形式・primitiveを保つsmooth正則化、正residueの有限型KE core、その小さい飽和近傍のmarked Lagrangian fillingを与える。既存neck/cornerの全collar葉を指定した相対fillingは追加条件である。

**P0は未解決。** 部分fibrationの外を含む全曲面の被覆、coreへの相対接着、中央帯外のsource接続と木上のfiber合併の径、全曲面のshortcutとportal費用が残る。局所GH近似のtargetの距離は非伸長retractionにより全cubical複体の距離の制限に等しい。Source側のprotected距離を全曲面ambient距離に置換した下界は未証明。先行研究の仮定と新規性の未確認点は主原稿序論と[研究ノート](research/notes.md)を参照。

## 極限候補の有限距離幾何

座標部分複体への明示的な非伸長retractionにより、全targetの最短路を六つ以下のlabelへ還元できる。Closed-cornerの三枚のsquareは全targetに等長に埋め込まれ、portal比較のgallery数は五次30、六次以上60で足りる。

六次以上では **$\operatorname{diam}(\mathcal C_d,d_\square)=2\sqrt5$**。最大対は互いに素な三元supportのall-ones頂点対に限る。四つのsquare galleryによる上界と120三角形のPL calibrationによる下界を証明し、有限部分を有理数演算で独立検算した。主定理は既存の五次の直径 $\sqrt{13}$ に依存しない。これは候補targetの結果であり、actual KE曲面の直径漸近は未解決の全域距離比較を要する。

## ビルドと再現

repo直下で `latexmk papers/surface-lagrangian-torus-fibration.tex`、`latexmk papers/quintic-integer-gluing.tex`、`latexmk papers/meridian-surgery.tex`。LuaLaTeX、LuaTeX-ja、日本語フォント、TikZを使用し、PDF/SyncTeXは `build/`。計算の入口は `python3 verification/run_current_checks.py`。ソースと証明書は `papers/sections/` と `verification/`。PDFはGitで追跡しない。

2026-11-21 / v2.8：固定compactのKE正則化、正residue coreと局所飽和filling、targetの非伸長retraction・六label最短路・六次以上の厳密直径を主稿改訂18へ統合し、追加証明を別担当と内部点検した。Rochon–ZhangのSNC cusp表示、Evans–Mauriのcone extension、Babson–Billera–Chanの既知cubical細分との関係を一次資料で確認した。主稿はLuaLaTeX/latexmkで188頁、PDF/SyncTeXを生成し、未解決の参照・引用、重複ラベル、欠落字形、overfull boxはない。序論・target距離・closed corner・core・文献の変更箇所を中心に18頁を表示確認した。四galleryと120三角形の有理数検算、静的構成検査も通過。形式証明・外部査読、包括的新規性確認、旧整数検算suiteや他三稿の再組版は今回未実施。P0と研究ノートの相対接着四課題は未解決。

**再現用パス：** 現行の分割TeXと検算入力は `papers/sections/` 以下を直接参照する。ルートの旧互換性symlink（`paper`, `paper_arithmetic`, `paper_surgery`, `notes`）は不要になり撤去した。構成の静的検査は `python3 verification/verify_repository_layout.py`、数学的な既定検算は `python3 verification/run_current_checks.py`。既存監査JSONの旧相対パスは出典記録として保持する。
