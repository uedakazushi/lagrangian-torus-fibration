# surface-lagrangian-torus-fibration — 研究・保存指示
2026-11-21 / v1.1

## 入口と正本
- 研究全体の入口は https://github.com/uedakazushi/research-hub 。再開時はhubの該当項目を確認し、最初にこのrepoの `00_research_plan.md`、次に本書、`research/notes.md` と必要な原稿を読む。
- 本研究の現行資料の正本はGitHub `main`。主たる公表用原稿は `papers/surface-lagrangian-torus-fibration.tex`（本文のある主原稿）であり、節分割可。独立論文は記述的な別名を付け、READMEと研究方針に役割を明記する。
- 一般原則と研究固有の目標を区別する。研究で使う文献、証明、再現入力の正本は当該repoに置く。

## この研究の最優先目標と自走指示

最優先は `00_research_plan.md` のP0、すなわち**本研究のactual Lagrangian fibrationが負KE計量のGH極限を幾何学的に実現すること**である。精密な問題は主稿の `ke:global-realization`。任意の固定次数d≥5について、実際のKE形式に関する大域fibrationと、合成写像p_Tπ_tの全曲面ambient距離に対する一様distortionの消失を証明する。五次は最初の節目であり、最終目標の縮小ではない。

- 本目標の解決へ向けた証明、反例の探索、必要な計算、一次文献確認、現行文書と再現手順の更新は継続して実行する。通常の研究上の選択ごとに「続けてよいか」と確認せず、計画だけを作って終了しない。独立した五次整数接着分類・三次元研究へ、P0との依存理由なく優先対象を移さない。
- 再開時は最新mainと作業ツリー・並行変更を確認し、研究方針 → 本書 → `research/ke-dependencies.md` → `research/notes.md` → 必要な原稿の順に読む。環境の具体的な入口は `research/cloud-codex.md`。会話履歴、旧bundle、前回の一時ディレクトリを前提にしない。
- 方針のK1から、または既に解決していれば最優先の未解決課題から着手する。各作業単位で仮定・領域・定数の依存・証明する補題を特定し、証明または明確な障害を得るまで検討する。独立な解析、接着、証明点検は可能なら分担する。
- 一つの方法が詰まったら、その失敗が計算上の問題か、未証明入力か、反例によるものかを区別し、ノートに本質的障害だけを残す。より弱い十分条件、直接の距離比較、別の局所構成、独立な次の課題へ進む。同じ未検証仮定を言い換えて証明済みにしない。
- K1–K4の成果は適切な主稿の節と現行ノートへ統合し、証明済み・条件付き・未完成の状態と次の具体的補題を研究方針で更新する。文書整備・検算成功・部分結果をP0の完了と報告しない。
- P0を完了とする前に、全特異領域を含む全射性・連結fiber、actual Lagrangian性、全域distortion、全固定dの範囲、依存証明・一次資料を点検する。重要な新証明は可能なら別agentが独立に点検する。数学的点検と形式証明を混同しない。
- 反例が得られたら元の主張と依存主張を訂正し、どの条件を変えれば正しいかを証明とともに整理する。反例を隠すための無言の目標縮小や、仮定の追加だけによる完了宣言はしない。
- 実行時間やサービスの制約で作業が区切られる場合も、その時点の有効な結果・未解決の補題・再開先をmainへ保存する。アクセス不足なら利用可能な課題を続け、未保存分は下記の緊急保存方針に従う。リポジトリへの指示の保存と、Cloud環境の設定・タスク開始・継続実行は別の状態として報告する。

## P0で維持する数学的な区別

- Ric(ω_t)=−ω_t、R_t=log(−log|t|²)、計量R_t^−2g_t、距離R_t^−1d_gを使う。正規化前の成分内部の四次元極限と混同しない。
- Mainの定性的存在結果から無制御にMoser移送しただけでは計量適合性を得ない。局所closed-cornerの内在/protected距離を全曲面のambient距離に読み替えない。
- KE側の(G)_d・(CP)_d・(PBE)_d、五次coarse packageの(TC)_5は実際の仮定を確認する。未解決入力は証明するか、同等に十分な別の全域評価で置き換える。Bounded volume densityはtensor二側比較を含意しない。
- d≥6ではp_Tが潰す木の上の全fiberの合併を制御する。Normal circleの一致とreduced葉・第二periodの一致、位相的同型と計量的一様性も区別する。P0に大域matroidal atlasや最適収束速度を追加要求しない。
- 解析入力の正本は `uedakazushi/kaehler-einstein-degeneration`、多重スケールの背景は `uedakazushi/multiscale-kaehler-einstein`。必要な定理のpath・label・確認commit・仮定を依存表で確認し、sourceを読んで使う。外部repoで作業するときはそちらの最新方針・AGENTSを先に読み、証明を二重管理しない。

## 研究の方針と確実性
1. 数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し、目的と方針を柔軟に修正する。履歴を積み増す代わりに現行資料を整理する。
2. 証明済み・追加仮定付き・証明未完成・予想・計算観察を区別し、仮定・証明の所在・依存関係・未解決箇所を記録する。原稿に証明が存在することは、その証明を今回独立に監査したことと異なる。
3. 先行研究の一次資料を確認し、適用範囲と本研究の貢献をIntroductionに明示する。文献と新規性の未確認事項は憶測で埋めない。他repoの結果を使うときは具体的な定理と仮定を記す。
4. 論文は原則日本語のLuaLaTeX。https://github.com/uedakazushi/research-hub の `papers/paper-template.tex`, `papers/README.md`, `.latexmkrc`, `.vscode/` を参考にする。主原稿を改名するときはinput、分割原稿のTeX root、文献、README、設定も更新する。
5. 研究ノートは現行の着想・例・補題・計算・障害・文献比較を保持する。論文中の十分な証明は複製せず参照する。過去の会話や更新日誌・旧版ZIPを蓄積しない。
6. 誤りの判明時は依存する主張を含めて修正し、ノート・方針・公表原稿・hubの記述を一致させる。

## 保存と検証
- 現行資料だけで再開できるよう、ソース、必要な文献情報、再現コード、入力、証明書を保持する。軽量化を理由に価値ある証明を削らない。古い資料の有効部分を統合するまでは消去しない。
- 研究の区切りでは追加の承諾なしに通常コミットで `main` へpush。長時間作業時は15〜30分で区切り保存する。他の作業者の変更を保護し、force push・GitHub Actionsの追加/起動は行わない。
- `latexmk` と VS Code LaTeX Workshopで組版し、SyncTeXとPDFを `build/` に整合させる。PDF・中間生成物は通常Git追跡しない。実行した数学的点検、計算、組版、pushは別々に報告する。
- `python3 scripts/research_check.py preflight` で依存環境、`python3 scripts/research_check.py static` で構成を確認する。TeXを変更したら `python3 scripts/research_check.py tex` で主稿を組版する。既存整数接着の有限検算は関連箇所を変更・使用した場合に `python3 scripts/research_check.py arithmetic` で行う。静的検査は数学の証明ではなく、整数検算はKEの解析的主張を検証しない。必要な検証ができなかったときは対象と理由を明記する。
- GitHub管理後はLibraryへの定常的二重保存/ZIP作成をしない。push不能時は緊急保存する。既存Libraryファイルは明示指示なしに削除しない。

## research-hub 更新義務
1. まず本repoの方針・原稿・ノート・READMEを最新の内容へ整理し、`main`へ保存する。
2. hubの最新READMEとAGENTS.mdを読んで、主要到達点・主張の状態・未解決の核心・次の一手・依存関係・正本・再開先・資料を実際に確認した日を更新する。
3. 詳細todo/証明/履歴はhubに転載しない。実質変更がないときは無用に更新しない。他項目と並行変更を保つ。
4. hubも通常コミットで`main`へ反映し、研究repo保存とhub更新の成否を独立に確認する。失敗した場合は対象と理由を報告する。公開範囲を勝手に変更しない。

## 回収した原資料の扱い
`research/source-manifest.json`と`research/migration.md`で全文・要約・未回収を区別する。移行完了の判定に短い要約を使わない。取得した最新版の訂正・追加仮定を旧稿の強い記述より優先する。保存済みの証明書と今回の再実行を混同しない。

## 複素次元3の正本との区別
三次元のfocus block・補集合の位相・全域存在問題は `https://github.com/uedakazushi/threefold-lagrangian-torus-fibration` を正本とする。曲面の主原稿、五次整数接着、KE適合は本repoで管理する。相互の結果は定理番号・適用仮定を明示して引用し、正本を二重化しない。

## 参照パスの現行運用
TeXの分割節と検証用proofは `papers/sections/{paper,paper_arithmetic,paper_surgery,notes}/` に置き、ルートsymlinkに依存しない。検算コードの参照を変えるときは `verification/run_current_checks.py` と `verification/verify_repository_layout.py` を照合する。旧検証JSON中の相対パス・SHA-256は歴史的な出典記録であり書換えない。ハッシュ確認は元コードとのパスだけの差を検証して数学的変更を許さない。現行のGitHub正本・hub更新義務は従前どおり。
