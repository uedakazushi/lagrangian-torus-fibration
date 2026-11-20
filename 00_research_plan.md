# 現行研究方針：一般型超曲面のLagrangian torus fibration
更新：2026-11-20 / 原資料の回収・全文移行

## 目標と現行資料
曲面の大域的fibration・作用適合atlasと、三次元のclosed-curve local blocksを区別する。曲面側は2026-10-28第25版のソース一式を回収し、旧30頁稿と短いGitHub草稿から現行の三論文へ移行した。三次元側は継続用bundle第10版から局所稿第9版・全体稿第11稿を全文TeXで移行した。

## 原稿と主張の状態
- `papers/lagrangian-torus-fibration.tex`：幾何・相対SNC構成・次数分割・大域作用atlas、96頁。Smooth X_d⊂P³、d≥5、hyperplane Kähler class aH。分岐底、正則T²、分岐S¹×figure-eight。任意のKähler class、special Lagrangian、KE collapseは主張しない。
- `papers/quintic-integer-gluing.tex`：五次整数接着、201頁。指定SNC cores・K5 graph・標準cones・marked puncturesを保つデータが対象。四ray正符号matchingとG5_14両単位枝{4,1,0}等。必要支持3型26標識は実現数ではない。全G5_14の排除、一般分母剛性、三高D同時非負性は未解決。
- `papers/meridian-surgery.tex`：meridian局所置換、18頁。閉corner circuitsへのregular torus bundles追加による四pants置換の障害。Open corridors等へ拡張しない。
- `papers/research-notes.tex`：研究ノート65頁。再利用補題・量化・現行の残余。詳細todoの正本はこちら。
- `papers/threefold-blocks.tex`：原版166頁の局所稿第9版。所定X_d⊂P⁴にdegree d−2、genus (d−3)(d−4)/2のnormal-trivial closed symplectic curveとactual local T³ blockを構成したとする。Normal faces、complement、大域boundary-free fibrationは未構成。
- `papers/threefold-fibration.tex`：原版187頁の全体稿第11稿。

## 独立に確認した幾何・位相
主原稿が読み込むbase_topology.texでB_d(T)からKE候補C_dへのcell-like homotopy equivalenceとd≥6での非同相性を証明し、さらに任意の固定Tについて人工的な区分的長さ距離d_epsilonのGH収束を誤差O(epsilon)で証明した（topo:metric-collapse）。これは実際の作用計量やKE計量の収束ではない。d=5,6,7,8の鎖階数は独立に有理数体上で検算し、有限体の回帰コードもverification/verify_ke_base_topology.pyに保管した。三次元のtrivial_normal_curve.texでは、normal-trivialな閉symplectic曲線のdegree eとgenus gに2g-2=(d-5)eが必要で、d偶数ならe偶数という制約と、三価Reeb graphのsaddle数が(d-5)eとなることを証明した（tnc:degree-genus-parity）。これらはnormal faces/complementの大域Lagrangian接着を完成させるものではない。メトリック収縮の一般的な先行研究に対する新規性は未確認。

## 次の一手
1. G5_14の中央matchingと二{4,1,0}・分母三の位置を同時に課す。G5_16のnode5、G5_17全matchingも別に扱う。
2. 三高Dの比例零軸・退化面の固定入力有限復元を、一般入力の上界や不存在へ外挿しない。
3. 三次元ではnormal facesとcomplementの大域接着を進める。
4. 曲面の旧v4ソースと現行v25の主要構成を照合し、旧版独自内容の網羅的照合は未了と記録する。

## 保存と検証
`research/source-manifest.json`に元ZIP・ソース対応・SHA-256を記載。各証明の断片はpapers/sections/に保持し、証明書が参照する旧版名の証明は必要依存として残す。古いビルドログ・PDF・不要TeXは持ち込まない。旧verification/内の証明書は保存時点の記録であり、今回全てを再実行した記録ではない。

曲面移行時に4本の全文原稿をLuaLaTeXで組版し、v25の五主検算と五独立監査を再実行した。実行入口は `python3 verification/run_current_checks.py`。生成物はbuild/。外部査読・形式証明・全113 scripts再実行とは異なる。

## 共通研究原則と保存許可（研究固有方針から独立）
数学的重要性・新規性・理解の深化・応用可能性・正確性・実現可能性を総合し方針を見直す。証明済み・仮定付き・未完成・予想・計算観察、既知成果と新規性、草稿の証明と今回の独立監査を区別する。重要な先行研究は一次資料の仮定と参照箇所を確認する。日本語LuaLaTeXで十分な証明を保ち、有効な着想・反例・障害は現行ノートへ整理する。再現資産を保持し、旧版ZIP/ログの集積を避ける。研究の区切りには承諾なしで通常コミットを `main` へpushし、15–30分ごとに区切って保存する。force push・GitHub Actions追加/起動をしない。Library旧資料を削除せず、GitHub管理後の定常二重保存は行わない。対象repo保存後にresearch-hubの到達点・核心・次の一手・依存と再開先を更新し、数学検証・組版・push・hub反映を区別する。
