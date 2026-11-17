---
name: cfo-cash-forecast
description: 現預金と入出金予定から、将来の資金推移・不足時期・最低残高を計算するときに使う。
metadata:
  aachat.headline.ja: "いつ資金が足りなくなるかを計算する"
  aachat.headline.en: "Find out when cash runs short"
  aachat.description.ja: "残高と入出金の予定から日ごとの資金を出し、最初に足りなくなる日・最低残高・守りたい残高との差を返す。計算用の Python スクリプト付き。"
  aachat.description.en: "Projects daily cash from balances and scheduled payments, and returns the first shortfall date, the lowest balance and the gap to the floor you want to keep. Includes a Python script for the math."
  aachat.discovery.listed: "true"
---

# 資金見通しの更新

対象事業・口座範囲・通貨、基準日、開始残高、入出金予定、予測期間を揃える。利用制限のある残高は使える資金と分ける。開始残高は基準日直前の残高か基準日時点かを明記する。
短期なら週次・13週を候補にするが、支払判断に必要な期間へ変える。本人が守りたい残高は未設定をゼロと区別し、勝手に決めない。
期末残高＝期首残高＋期間内入金－期間内出金。売上の計上日ではなく入金日を使う。税・年払い・返済・返金等は資料にある支払予定を反映し、未契約商談・融資を確定入金へ混ぜない。

日付がある場合は日次まで計算し、週末には回復する途中の不足も示す。同日内の順序が不明なら日末残高だけで支払可能と言わない。日付・金額不明の予定は欠落一覧と影響を残す。
日付の確定した単一通貨の予測は [scripts/forecast.py](scripts/forecast.py) を使える。入力と実行例は [references/input.md](references/input.md)。不明値をスクリプトに合わせて補完しない。
成果は基準日、対象範囲、資金推移、最初の不足日、最低残高、下限との差、原因の入出金、判断期限。不確かな入金は別シナリオで示す。
前回との差を入出金の追加・取消・日付変更・金額変更に分ける。予測を将来の確定値と表現しない。
考え方の出典は [references/evidence.md](references/evidence.md)。
