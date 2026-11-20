# 移行範囲と検証

2026-11-20。Libraryから曲面第25版のhandoff ZIP、三次元第9版166頁PDF、旧曲面第4版ZIPを取得した。元Libraryは変更・削除しない。

## 原資料と配置

第25版の4本の現行TeX（幾何、整数接着、meridian置換、研究ノート）をpapers/直下の全文主原稿にし、移行時にはinput先と探索パスを変更した。その後の基底の位相比較と研究再開先の修正があるため、`source-manifest.json` では `source_sha256`（元資料）と `sha256`（現行）を分ける。必要な分割ソースと過去の検証器・証明書が参照する証明をpapers/sections/へ保持した。ソース対応とhashはsource-manifest.json。原稿・証明のバイト一致と、主原稿のinputパス変換を区別する。

証明書の相対パスを保つため、ルートpaper/、paper_arithmetic/、paper_surgery/、notes/は分割原稿ディレクトリへのsymlinkである。実体の重複はない。移行前の旧TeXのうち、現行原稿と保存した検証器・証明書から参照されない6断片は持ち込まなかった。元資料は手元にも残している。


## 照合と未了事項

旧曲面v4はneck・relative compactification・actual component filling・transport・base homologyを含み、v25のrelative_compactification.tex、neck_models.tex、global_gluing.tex、base_topology.texが現在の詳細な対応先である。旧稿の全補題を逐一比較した網羅的保存監査は未了。


## 今回の検証

LuaLaTeXで幾何96頁、整数接着201頁、局所置換18頁、ノート65頁を生成し、当時の三次元要約も組版した。PDF/SyncTeXはbuild/。最終logに未解決参照・引用やoverfull/underfull boxがないことを確認した。フォント置換警告は残る。各原稿の冒頭・中間・末尾頁を画像化して目視確認した。VS Code UIは未検証。

`python3 verification/run_current_checks.py`で第25版の五主検算と五独立監査を実行し全てexit 0。比例軸端点の有限再構成は既定s≤400、退化面の固定b検査は既定b=2,…,20。無上界の恒等式検査・係数証明と有限走査を区別する。詳細出力はbuild/migration-checks/。全113 scriptsの再実行や、外部査読・形式証明は行っていない。

今回の全主原稿の最終logに未解決参照・引用とoverfull/underfull boxはなし。各原稿の冒頭・中間・末尾を描画して確認した。全頁の目視監査は未実施。フォント置換・scale・PDF bookmarkの数式警告は残る。VS Codeは主原稿だけをroot候補とする設定を検査したがUI操作は未検証。

## 三次元継続用bundle第10版

[2026-10-28版の原資料](https://chatgpt.com/space/file/libfile_47c5d4044694819192c28e687c95557f)から局所稿第9版と全体稿第11稿を全文移行した。共通の証明・図・コードは `papers/sections/threefold/` に置いた。組版の参照パスを調整し、図はPNGで収録した。旧原稿PDFをGitの現行ツリーから削除した。

元bundleの検算15本はすべて成功した。うち三次元13本は `python3 verification/run_threefold_checks.py` で再実行できる。

LuaLaTeXで局所稿166頁・全体稿187頁を生成し、最終ログで未解決の参照・引用がないことを確認した。

## 曲面v4の検算の回収

三次元研究継続用bundle第10版の `surface_v4/` を照合した。相対Moserと輸送の現行の参照先は `papers/sections/paper/global_gluing.tex`、整数鎖収縮と六次のPetersenリンクは `base_topology.tex`。旧稿の具体例を再現する二つの検算コードは `verification/surface_v4/` に収録した。五次の50節点・交点回避・面積・境界の検算と、次数5–12の構成データの検算が正常終了した。

再実行するには、リポジトリ直下から以下を実行する。

```sh
mkdir -p build/surface-v4-checks
cp verification/surface_v4/*.py build/surface-v4-checks/
python3 build/surface-v4-checks/verify_data.py
python3 build/surface-v4-checks/verify_general_degree.py
```

旧曲面稿の全証明の逐条照合は継続課題。
