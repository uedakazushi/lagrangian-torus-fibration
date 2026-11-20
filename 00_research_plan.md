# 現行研究方針：一般型超曲面のLagrangian torus fibration
更新：2026-11-20 / v1.1

## 研究固有の目標
一般型射影超曲面の指定symplectic/Kähler classで自由な外部境界のないbranched Lagrangian torus fibrationを構成する。曲面の相対接着と、3次元のclosed-curve local blockを分ける。最優先は3次元のnormal faces/complementと接着した**global fibration完成**である。

## 原資料と到達点
- 曲面：2026-10-27第5稿30頁のLibrary `general_type_surface_fibration_paper_ja_v5.pdf`。次数 \(d\ge5\) の \(X_d\subset\mathbf P^3\)、branched base、正則 \(T^2\)-fibers、relative Moser/transport、baseの整数ホモロジーを主張する。証明の独立監査は未了。
- 三次元：2026-10-28第9稿166頁のLibrary `focus_curve_blocks_and_obstructions_ja.pdf`。\(X_d\subset\mathbf P^4\), \(d\ge6\) にnormal-trivialなclosed symplectic curveと局所 \(T^3\)-blockを構成したとする。Whole focus–hyperbolic fibersは \((d-2)(d-5)\) 個。**Normal faces、complement、全体を覆う境界なしのfibrationは未構成。**
- 旧Library `quintic_fibration_source.zip` の生データ転送は接続制約で未完了。GitHubのLuaLaTeX二論文は有効な内容の一部を再構成したものであり、原PDFの全証明の移植とは区別する。

## 次の一手
1. 曲面v5のLiouville collar、divisor-preserving Moser、equivariant transport、integral homologyを各補題ごとに検証・ソース化する。
2. 三次元v9でnormal degreeの障害を避ける閉曲線の構成とwhole-fiber接着を監査する。
3. Normal faces、positive normal shell、relative caps、complementのLagrangian fibersを同じsymplectic formに整合させる。
4. Tropical atlas、special Lagrangian、KE collapseとの比較は推測と実証を分け、一般次元の構造に優先して取り組む。

## 正本と依存
主原稿：`papers/lagrangian-torus-fibration.tex`（曲面）。独立論文：`papers/threefold-blocks.tex`（3次元）。ノート：`research/notes.md`。KE degenerationとの将来の比較対象は [kaehler-einstein-degeneration](https://github.com/uedakazushi/kaehler-einstein-degeneration)。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りには承諾なしで通常コミットを `main` へpushし、15–30分ごとに区切って保存する。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。
