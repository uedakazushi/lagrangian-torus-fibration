# Lagrangian torus fibrations on general-type surfaces
2026-11-21 / v2.2 — [研究方針](00_research_plan.md) · [研究ノート](research/notes.md) · [Cloud Codexの再開手順](research/cloud-codex.md) · [research-hub](https://github.com/uedakazushi/research-hub)

**最優先目標は、本研究の大域Lagrangian torus fibrationが、負Kähler–Einstein計量のGromov–Hausdorff極限を幾何学的に実現すること。現時点では未解決である。** 対象は各固定次数 \(d\ge5\) の一般位置全平面退化 \(X_t\subset\mathbb P^3\)。**このリポジトリは複素次元2専用**。三次元の研究は [threefold-lagrangian-torus-fibration](https://github.com/uedakazushi/threefold-lagrangian-torus-fibration) を正本とする。

## 何をもって解決とするか

\(\operatorname{Ric}(\omega_t)=-\omega_t\)、\(R_t=\log(-\log|t|^2)\) とし、actual \(\omega_t\)-Lagrangianな大域fibration \(\pi_t:X_t\to B_d(T)\) を、標識付き基底収縮 \(p_T:B_d(T)\to\mathcal C_d\) と合成して
\[
\sup_{x,y\in X_t}\left|R_t^{-1}d_{g_t}(x,y)-d_\square(p_T\pi_t(x),p_T\pi_t(y))\right|\longrightarrow0
\]
を証明する。全曲面のambient距離を用い、source・branch・coreの全特異fibersを含む。\(d\ge6\) では木上の複数のfibersの合併全体も収縮させる。五次は最初の到達点であり、最終的な次数範囲を五次に限らない。詳細は主稿の未解決問題 `ke:global-realization` と [研究方針のP0](00_research_plan.md)。

既存の局所GH収束や、未証明の解析仮定を残した条件付き大域定理は、この目標の解決とは区別する。必要なKE入力の所在と仮定は [依存関係表](research/ke-dependencies.md) にまとめる。従来の大域構成・作用適合atlas・整数接着の証明は保持し、独立した整数接着分類はこの目標に必要な場合以外は後順位とする。

## Cloud Codexから再開する

最新mainで [研究方針](00_research_plan.md) → [AGENTS.md](AGENTS.md) → [依存関係](research/ke-dependencies.md) → [研究ノート](research/notes.md) を読む。次の最初の課題は、moving neck領域でのactual normal circleの短さと、Moserのsource・像の双方を覆う一様buffer（K1）。その後、複数endの作用・reduced葉、全特異領域への相対接着、全曲面の距離比較を進める。

```sh
python3 scripts/research_check.py setup --require-tex
python3 scripts/research_check.py static
python3 scripts/research_check.py tex
```

環境要件・そのまま渡せる開始指示・必要な範囲の検証方法は [Cloud Codexの再開手順](research/cloud-codex.md)。通常の研究継続・コミット・mainへの保存は承諾を求めず行い、**切りのよいところで、長くても前回成功pushから約15分を目安に有効な現行成果を保存**しながら、方針の達成条件に沿って研究を進める。保存が必要でも未完成の証明を完成と記さず、他者変更を保持する。これらのファイルは再開・実行のための指示であり、Cloudサービス側の環境設定や新規タスク起動を自動的に行うものではない。

## 論文と役割
| 原稿 | 役割 | 組版の確認範囲 |
| --- | --- | ---: |
| [主原稿](papers/surface-lagrangian-torus-fibration.tex) | 相対SNC構成・次数分割・分岐底・作用適合atlas、局所KE収束と大域実現問題（改訂10） | 現行134頁・2026-11-21組版確認 |
| [五次整数接着](papers/quintic-integer-gluing.tex) | 指定K5データの整数条件・高分母支持・未解決の大域接着 | 201頁 |
| [Meridian surgery](papers/meridian-surgery.tex) | 閉corner circuitsの局所置換の障害 | 18頁 |
| [TeX研究ノート](papers/research-notes.tex) | 証明素材・残る条件の整理 | 65頁 |

## 主な到達点と残る課題
指定hyperplane Kähler classでの正則Lagrangian \(T^2\) と、分岐辺上の \(S^1\times(S^1\vee S^1)\)、面内のpinched torus、core上のlogarithmic Weinstein skeletonを扱う。五次は(cores, branch edges, nodes)=(5,10,50)、六次は(6,30,90)で、分岐辺数は無限個のfiberの個数ではない。通常のalmost toric fibrationを超える特異模型を用いるため、Leung–Symingtonの分類と矛盾しない。全大域接着の公表前監査はなお必要。

五次整数アフィン接着では、四rayの完全matching条件等を証明し、高分母の必要支持候補を \(G_{5,14},G_{5,16},G_{5,17}\) の3型・26標識まで絞った。ただし26は実現数ではなく、一般分母の剛性・三高係数の同時非負性や全支持型の大域接着は未解決。

KE退化との関連では、全閉triple cornerのactual局所GH収縮、短normal circleを用いる定量的二段階平均・共通作用周期の管理が主な到達点。固定残余compactでは法線円の深度積分評価と、同じ残余点に沿う係数1・加法誤差 $O(1)$ の動径接続上界を得た。軌道平均エネルギーを使うMoser速度評価と、縮小する実計量の境界距離 $\delta_t$ に対する十分条件 $m_t\delta_t^2\to\infty$ も主稿に追加した。**全neckの一様buffer、source・branch・core相対接着、全曲面のGH no-shortcutおよび既存fibrationとの大域的な一様適合性は未証明**。局所KE定理と大域GH収束を混同しない。先行研究の仮定と新規性の未確認点は主原稿序論と[研究ノート](research/notes.md)を参照。

## ビルドと再現
repo直下で `latexmk papers/surface-lagrangian-torus-fibration.tex`、`latexmk papers/quintic-integer-gluing.tex`、`latexmk papers/meridian-surgery.tex`。LuaLaTeX、LuaTeX-ja、日本語フォント、TikZを使用し、PDF/SyncTeXは `build/`。計算の入口は `python3 verification/run_current_checks.py`。ソースと証明書は `papers/sections/` と `verification/`。PDFはGitで追跡しない。

2026-11-21の改訂10で、環境に用意されたLuaTeX-jaを有効にして `setup --require-tex` / `static` / `tex` を実行し、主稿134頁、PDF・SyncTeXの同一出力先、追加した命題・系の参照解決を確認した。新しい積分エネルギー評価と動径上界を独立に数学点検した。他三稿の頁数は従来記録。今回の整数検算suite、他三稿の組版、既存の全証明の再監査、形式証明、包括的新規性調査は未実施。

**再現用パス：** 現行の分割TeXと検算入力は `papers/sections/` 以下を直接参照する。ルートの旧互換性symlink（`paper`, `paper_arithmetic`, `paper_surgery`, `notes`）は不要になり撤去した。構成の静的検査は `python3 verification/verify_repository_layout.py`、数学的な既定検算は `python3 verification/run_current_checks.py`。既存監査JSONの旧相対パスは出典記録として保持する。
