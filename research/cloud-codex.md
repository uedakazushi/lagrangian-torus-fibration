# Cloud Codexでの実行と再開

2026-11-21 / v1.0

研究目標・達成判定・優先順位は [研究方針](../00_research_plan.md)、継続と保存の規則は [AGENTS.md](../AGENTS.md) が正本である。本書は実行環境と開始方法だけを補う。解析上の外部依存は [KE依存表](ke-dependencies.md) にまとめる。

## 開始時に渡す指示

次の指示で、新しいタスクも現行mainだけから開始できる。

> surface-lagrangian-torus-fibrationのmainを読み、research-hubの該当項目、00_research_plan.md、AGENTS.mdに従って研究を続けて下さい。最優先目標は、actualな負Kähler–Einstein形式に対する大域Lagrangian torus fibrationが、正規化した曲面全体のGromov–Hausdorff極限を幾何学的に実現することです。方針に定めた達成条件を満たすまで、最初の未解決の証明課題を選び、証明・反例・文献調査・必要な計算を進め、検証して次の課題へ移って下さい。局所結果や追加仮定付き結果を全体の解決とせず、必要な解析入力も研究対象として下さい。判断できる方針選択・検証・通常コミットとmainへのpushには再承諾を求めず、研究の区切りで現行資料とresearch-hubを更新して下さい。時間・アクセス等の実行制約が来た場合は、具体的な未解決箇所と次の着手方法を現行資料へ保存して下さい。

## 必要な環境

| 用途 | 必要なもの |
| --- | --- |
| 文書編集、構成検査、既存の整数検算 | Git、Python 3.10以降。既存の現行検算はPython標準ライブラリで実行する。 |
| 日本語原稿の組版 | LuaLaTeX、latexmk、LuaTeX-ja/fontspec、日本語OpenTypeフォント、LaTeXの標準・追加パッケージ、TikZ。`papers/sections/common.tex`と`.latexmkrc`を使用する。 |
| 依存する解析結果の確認 | `kaehler-einstein-degeneration`の現行資料への読取アクセス。必要な箇所に限り`multiscale-kaehler-einstein`も参照する。 |
| 保存と研究全体への反映 | 本repoと`research-hub`のmainへの認証済み書込アクセス。追加の解析結果を外部repoで編集する場合は、その作業指示と権限も確認する。 |
| 一次文献 | 引用先の論文・著者ページ等へのアクセス。ローカルに資料があることと最新の内容を確認したことを区別する。 |

環境の準備では必要な依存だけを入れ、既存のTeX設定を尊重する。TeX Live等の一式がある場合は再インストールせず、下記の検査と実際の組版で確認する。機械固有のフォントパス、認証情報、キャッシュをGitに含めない。

現在のCloud環境では、対象repoを含む環境を準備して公開し、そこからタスクを開始する。環境のInstall script / Start skillに使う実行コマンドは次の通り。公式の[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)に従い、依存の導入・ネットワーク・GitHub接続は環境側で設定する。これは旧Cloudのsetup/maintenance scriptの動作を前提としない。

```bash
python3 scripts/research_check.py setup --require-tex
python3 scripts/research_check.py static
```

`setup`は何度実行しても同じ状態になるよう、無視対象の`build/`を作り、利用可能な依存を調べるだけである。パッケージのインストール、環境設定の書換え、ネットワークアクセス、Git書込、Cloudタスク起動は行わない。TeXが不足する場合は必要な依存を環境の導入手順で補い、同じコマンドを再実行する。フォント・formatを含む組版の成否は次の`tex`段階で確認する。

## 検証を選ぶ

repo直下で実行する。外部KEのcheckoutが兄弟ディレクトリにない場合は、`preflight`と`tex`に`--ke-repo /path/to/kaehler-einstein-degeneration`を付けられる。

| 段階 | コマンド | 確認する範囲 |
| --- | --- | --- |
| 再開時 | `python3 scripts/research_check.py preflight` | 必須ファイル、Python、Git HEAD、変更の有無、TeX依存、外部KE checkoutの所在。読取だけ。 |
| 保存前の軽量検査 | `python3 scripts/research_check.py static` | 既存の構成検査と`git diff --check`。証明の正しさは検査しない。 |
| 主稿のTeX変更時 | `python3 scripts/research_check.py tex` | `.latexmkrc`を明示してLuaLaTeXで組版し、PDF/SyncTeX/logの出力、未解決の引用・参照、重複ラベル、欠落字形を確認する。変更したページは別に表示確認する。 |
| 別原稿の変更時 | `python3 scripts/research_check.py tex --paper quintic-integer-gluing` | 指定した原稿の組版。他の選択肢は`meridian-surgery`、`research-notes`。 |
| 整数接着の証明・コード・入力を変更したとき | `python3 scripts/research_check.py arithmetic` | 既存の五主検算・五独立監査。KE解析や大域GH収束の検証とは別。 |

整数接着に関係しない変更のたびに長い整数検算を再実行する必要はない。新しい解析補題は、仮定・量化・定数の一様性・領域・依存する結果・論理の循環を数学的に点検する。数値実験や上記スクリプトの成功を、その代用にしない。

外部結果を使う前に、KE依存表の参照先と実際のcheckoutの差を読む。`preflight`はcommitを表示するだけで、依存する定理の最新版の正しさや適用条件を保証しない。ネットワーク確認や認証済みpushは実際の接続で別途確認する。読取が可能でも書込権限があるとは判断しない。


## 環境の公開前に確認すること

Cloudの再利用環境を作るときは、まず `surface-lagrangian-torus-fibration`、`kaehler-einstein-degeneration`、`research-hub` を利用可能なリポジトリとして選び、必要なら `multiscale-kaehler-einstein` も追加する。前二者の研究資料は別正本であり、hubの更新も独立のpush権限が必要である。ChatGPTのGitHub connectorの書込権限はCloud実行環境の認証を保証しない。

環境の初期設定ではTeX Liveの不足したLuaLaTeX/日本語パッケージと日本語フォントを実際に導入・確認する。`setup --require-tex` は依存を**インストールせず、存在を検査するだけ**である。環境をPublishする前に少なくとも以下を実行して成功を確かめる。

```bash
python3 scripts/research_check.py setup --require-tex
python3 scripts/research_check.py static
python3 scripts/research_check.py tex
```

次いで外部KE repoのcheckoutと参照コミット／最新mainを点検し、一次論文への必要なネットワークアクセスを設定する。認証済みGitHub pushが可能かは公開範囲を変えず別に確認する。**Environment published** と表示されたあと、その環境から新しいタスクを開始し、上記の開始指示を渡す。Cloud環境のPublish、実際のタスク起動、継続している状態はこのGitHubファイル自体には記録されないため、リポジトリの整備済みをCloud起動済みと読み替えない。

Codexのタスクには実行・サービス上の区切りがある。AGENTSの「解決まで自走」は、実行できるあいだ優先課題を連続して進め、区切りではmainへ保存して次のタスクが自立再開できるという意味であり、**無期限の自動再起動を保証しない**。手動で再開する際も新しい指示を一から書く必要はない。

## 継続と実行状態

実行中のタスクはAGENTS.mdの研究サイクルを繰り返す。未解決の補題で一つの方法が失敗した場合は本質的な障害をノートに残し、代替経路や依存する解析入力の証明へ進む。タスクを再開するときはmainの方針とノートから最初の未解決項目を選ぶ。過去のチャットや機械固有の作業ディレクトリを必須にしない。

リポジトリにこれらの指示を保存したこと、Cloud環境を設定・公開したこと、Cloudタスクを実際に起動したこと、数学的目標を解決したことは別の状態である。文書の整備だけをタスク起動や無期限の自動再起動と報告しない。タスクの制限で中断するときも、得た証明と残る具体的な課題を保存すれば、次の実行が同じ地点から継続できる。
