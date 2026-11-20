# 移行範囲と検証

2026-11-20。Libraryから曲面第25版のhandoff ZIP、三次元第9版166頁PDF、旧曲面第4版ZIPを取得した。元Libraryは変更・削除しない。

## 原資料と配置

第25版の4本の現行TeX（幾何、整数接着、meridian置換、研究ノート）をpapers/直下の全文主原稿にし、input先と探索パスだけを変更した。必要な分割ソースと過去の検証器・証明書が参照する証明をpapers/sections/へ保持した。ソース対応とhashはsource-manifest.json。原稿・証明のバイト一致と、主原稿のinputパス変換を区別する。

証明書の相対パスを保つため、ルートpaper/、paper_arithmetic/、paper_surgery/、notes/は分割原稿ディレクトリへのsymlinkである。実体の重複はない。移行前の旧TeXのうち、現行原稿と保存した検証器・証明書から参照されない6断片は持ち込まなかった。元資料は手元にも残している。

三次元PDFは元TeX未取得のため、全証明を失わない目的でsources/に例外的に追跡する。通常の生成PDFはbuild/に出力し追跡しない。対応するpapers/threefold-blocks.texは要約のみ。166頁のソース移行・再組版完了とは報告しない。

## 照合と未了事項

旧曲面v4はneck・relative compactification・actual component filling・transport・base homologyを含み、v25のrelative_compactification.tex、neck_models.tex、global_gluing.tex、base_topology.texが現在の詳細な対応先である。旧稿の全補題を逐一比較した網羅的保存監査は未了。

三次元TeXと必要な再現資産は未取得。Libraryのfocus検索でPDFを取得できたが、検索は一部結果の読み込み失敗を報告したため、ソースが存在しないとは断定しない。完全移行の残件として保持する。

## 今回の検証

LuaLaTeXで幾何96頁、整数接着201頁、局所置換18頁、ノート65頁を生成し、短い三次元要約も組版した。PDF/SyncTeXはbuild/。最終logに未解決参照・引用やoverfull/underfull boxがないことを確認した。フォント置換警告は残る。各原稿の冒頭・中間・末尾頁を画像化して目視確認した。VS Code UIは未検証。

`python3 verification/run_current_checks.py`で第25版の五主検算と五独立監査を実行し全てexit 0。比例軸端点の有限再構成は既定s≤400、退化面の固定b検査は既定b=2,…,20。無上界の恒等式検査・係数証明と有限走査を区別する。詳細出力はbuild/migration-checks/。全113 scriptsの再実行や、外部査読・形式証明は行っていない。

今回の全主原稿の最終logに未解決参照・引用とoverfull/underfull boxはなし。各原稿の冒頭・中間・末尾を描画して確認した。全頁の目視監査は未実施。フォント置換・scale・PDF bookmarkの数式警告は残る。VS Codeは主原稿だけをroot候補とする設定を検査したがUI操作は未検証。
