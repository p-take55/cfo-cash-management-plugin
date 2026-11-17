---
name: cfo-cash-monitor
description: 前回からの資金見通しの変化、入金遅れ、想定外支出、残高下限への接近を調べるときに使う。
metadata:
  aachat.headline.ja: "前回から資金の見通しがどう変わったかを調べる"
  aachat.headline.en: "See how the cash outlook changed since last time"
  aachat.description.ja: "入金の遅れ、想定外の支出、残高の下限への接近を見つけ、新しく出たもの・悪くなったもの・良くなったもの・解消したものを分けて伝える。"
  aachat.description.en: "Spots late payments, unexpected spending and balances nearing your floor, and reports new, worse, better and resolved items separately."
  aachat.discovery.listed: "true"
---

# 資金変化の検知

今回と前回の資金予測、元資料の更新記録、入金予定と実績を読む。同じ事業・通貨・期間に揃え、定義変更と事業変化を分ける。
入金期限を過ぎた未回収、支出の増加・前倒し、最低残高と不足日の変化を確認する。データ未取得と未入金を混同しない。古い資料では現在問題なしと断定しない。
監視条件は本人が合意した金額・残高・期日・重要度を使う。未設定なら候補を提示し、継続通知を始めない。

同じ問題は原因の取引・対象期間で追跡し、新規・悪化・改善・解消を区別する。未解消を毎回新件として通知しない。資料遅延だけで解消扱いにしない。
成果は変化、根拠、資金への影響、対応期限、推奨する次の確認。本人に判断が必要なものを先に示す。
このSkillは呼び出された時点の確認。常駐や次回実行を自動で約束しない。通知・定期実行の設定済み状態は実際の登録結果で確認する。
