---
name: cfo-cash-scenarios
description: 売上未達・入金遅延・追加支出などの条件で資金推移を比較するときに使う。
metadata:
  aachat.headline.ja: "売上が届かないときや入金が遅れたときの資金を比べる"
  aachat.headline.en: "Compare cash when sales fall short or payments come late"
  aachat.description.ja: "基本の見通しはそのままに、条件を変えて計算し直す。ケースごとの最低残高と足りなくなる日、結論が変わる境目を示す。"
  aachat.description.en: "Recalculates from a fixed baseline under changed conditions, and shows each case's lowest balance, shortfall date and the point where the conclusion changes."
  aachat.discovery.listed: "true"
---

# 資金シナリオ比較

同じ基準日・開始残高・通貨・期間の基本予測を固定し、判断に効く変数を選ぶ。変更する取引と日付・金額・確度を明示する。
売上未達を入金減少へ置き換える際は請求・回収時期を反映する。入金遅延は元の入金を移動し、元日に残したまま追加しない。予測期間の外へ移った入金をその期間内の資金に含めない。
単一要因の影響と複合した場合を分ける。シナリオに確率を付けるのは根拠がある場合だけ。楽観・悲観の割合を勝手に標準値にしない。

各ケースの最低残高、最初の不足日、下限との差、判断期限を同じ方法で再計算する。資金予測Skillの計算手段が利用可能なら再利用し、なければ式を明記して表計算やコードで計算する。
成果は条件別比較と、結論が変わる境界、先に確かめたい仮定。基本予測をシナリオで上書きしない。最終判断は本人へ返す。
