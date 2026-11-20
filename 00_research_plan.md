# 現行研究方針：一般型超曲面のLagrangian torus fibration
2026-11-20 / v1.0

## 研究固有の目標
一般型射影超曲面の指定Kähler classで、分岐を許し自由な外部境界のないLagrangian torus fibrationを構成する。五次曲面等の2次元超曲面での相対接着と、(X_d\subset\mathbf P^4, d\ge6\) の3次元局所blocksを区別し、**局所blocksから大域global fibrationへのギャップ**を最優先にする。

## 現在の二本の原資料
- 曲面：`general_type_surface_fibration_paper_ja_v5.pdf`（2026-10-27、第5稿、30頁）。(X_d\subset\mathbf P^3,d\ge5\)、三価分岐2-complexを基底とする(T^2)-fibration、relative Liouville collar / Moser / equivariant transport、底空間の整数ホモロジー等を原稿中で主張。解析的相対接着の全仮定と証明の独立精査は未了。
- 3次元：`focus_curve_blocks_and_obstructions_ja.pdf`（2026-10-28、第9版、166頁）。(X_d\subset\mathbf P^4,d\ge6\) でnormal-trivialなclosed symplectic curveの近傍のactual (T^3)-blockと ((d-2)(d-5)) 個のfocus–hyperbolic fibersを原稿中で構成。**normal facesとcomplementのfibration、全体を覆う境界のないfibrationは未完成**。
- 原稿の利用と今回の論理監査、生成された抽出テキストと正規のTeXソースを分ける。旧Libraryには `quintic_fibration_source.zip` があるが、今回は生のZIP内容の移行が接続制約で完了していない。

## 到達基準と優先順位
1. 3次元のnormal faces/caps/complementを接続し、固定symplectic form上で全fiberのLagrangian性、境界の整合、Maslov/monodromyを証明する。既存のnormal degree (2d) 障害を避けるclosed curveの選択を維持する。
2. 曲面論文のrelative compactificationと指定Kähler classの許容領域を証明単位ごとに点検し、必要な定量評価を明確にする。
3. 一般次元を模索しつつ、tropical/integral affine atlas、KE degenerationとの比較、special Lagrangian性は証明と予想を区別して追究する。

## 文書と依存
- 主原稿 `papers/lagrangian-torus-fibration.tex`：曲面の場合の現在の到達範囲と証明問題。
- 独立の3次元原稿 `papers/threefold-blocks.tex`。
- 現行研究ノート `research/notes.md`。PDF原本・ZIPは従来のLibraryに残るが、GitHubの正本への完全なTeXソース移行は別途回収が必要。
- [kaehler-einstein-degeneration](https://github.com/uedakazushi/kaehler-einstein-degeneration) との比較は将来の課題であり、Lagrangian/global GH双方の完成を前提にしない。

## 共通研究原則・保存許可（研究固有の方針ではない）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し研究方針を柔軟に更新する。証明済み、追加仮定付き、未完成、予想、計算観察を分ける。先行研究の重要な入力は一次資料で確認し、正確な仮定と独自の貢献をIntroductionに記す。日本語LuaLaTeXで公表原稿と十分な証明を整理し、有効なアイデア・反例・障害・計算は重複なく現行ノートに保持する。再現に不可欠なソース・入力を保全し、旧版/作業ログで代用しない。区切りごとに追加承認なしで通常コミットを `main` にpushし、長時間作業では15〜30分で保存する。force pushとGitHub Actionsの追加/起動はしない。他者の変更と公開範囲を保持する。Libraryの既存ファイルを削除せず、GitHub移行後のLibrary定常二重保存は不要。各repoを保存してからresearch-hubを現状へ反映し、対象repoとhubの更新成功を別々に検証する。論理監査・計算・組版・反映を別々に報告する。
