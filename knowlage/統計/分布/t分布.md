---
status: 完了
tags:
  - problem
level: 0
last: 2026-09-29
retired: false
category: 基礎
---
```meta-bind-button
id: srs-o
class: srs-btn-o
hidden: true
label: "○ 正解＋説明できた"
style: primary
action:
  type: js
  file: exam/スクリプト/review.js
  args:
    grade: "○"
```

```meta-bind-button
id: srs-tri
class: srs-btn-tri
hidden: true
label: "△ 正解したが説明できない"
style: default
action:
  type: js
  file: exam/スクリプト/review.js
  args:
    grade: "△"
```

```meta-bind-button
id: srs-x
class: srs-btn-x
hidden: true
label: "× 不正解"
style: destructive
action:
  type: js
  file: exam/スクリプト/review.js
  args:
    grade: "×"
```

`BUTTON[srs-o]` `BUTTON[srs-tri]` `BUTTON[srs-x]`


**母分散 $\sigma^2$ が未知のとき、標本平均を「$\sigma$ の代わりに標本の $s$」で標準化した統計量が従う連続分布。** 形は[[自由度]] $\nu$ だけで決まり、$t(\nu)$ と書く。

## 統計量（$X_1, \ldots, X_n$ が $N(\mu, \sigma^2)$ からの無作為標本）

$$
T = \frac{\bar{X} - \mu}{s / \sqrt{n}} \sim t(n-1), \qquad s = \sqrt{\frac{1}{n-1}\sum (X_i - \bar{X})^2}
$$

$\sigma$ が既知なら $Z = \dfrac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim N(0,1)$ だった（→ [[標本分布]]）。分母の $\sigma$ を不偏分散の平方根 $s$（→ [[分散・不偏分散]]）に置き換えただけ。自由度が $n-1$ なのは $s$ を計算するのに $\bar{X}$ を1つ使っているから。

## 形と性質

- 平均0、左右対称。見た目は標準正規分布とほぼ同じ釣鐘型
- **裾が正規分布より厚い**。分母の $s$ も標本ごとにブレるので、極端な $T$ が出やすくなる
- 自由度が大きいほど $N(0,1)$ に近づく（$s$ が $\sigma$ に近づくため）。目安 $n \ge 30$ で実用上は同じ
- 分散は $\dfrac{\nu}{\nu - 2}$（$\nu > 2$）。1より大きく、$\nu \to \infty$ で1に収束

一般形：$Z \sim N(0,1)$ と $W \sim \chi^2(\nu)$ が独立なら $T = \dfrac{Z}{\sqrt{W/\nu}} \sim t(\nu)$（→ [[χ2乗分布]]）。上の統計量はこの形に整理できる。

## よく使う形

- 母平均の信頼区間（$\sigma$ 未知）：$\bar{x} \pm t_{\alpha/2}(n-1)\, \dfrac{s}{\sqrt{n}}$
- 1標本 t検定：帰無仮説 $\mu = \mu_0$ のもとで $T = \dfrac{\bar{x} - \mu_0}{s/\sqrt{n}}$ を $t(n-1)$ と比べる
- 対応のある2群：差 $d_i$ を取って1標本と同じ扱い（自由度 $n-1$）
- 対応のない2群（等分散仮定）：自由度 $n_1 + n_2 - 2$、分母はプールした分散
- 回帰係数の検定：$t = \dfrac{\text{推定値}}{\text{標準誤差}}$、自由度は $n - (\text{係数の個数})$
- t表の読み方：表の値は上側確率 $\alpha$ の点 $t_\alpha(\nu)$。対称なので下側は $-t_\alpha(\nu)$、両側5%なら上側2.5%の列を見る

## 例

$n = 10$、$\bar{x} = 52$、$s = 5$ のとき母平均の95%信頼区間：$t_{0.025}(9) = 2.262$ なので $52 \pm 2.262 \times \dfrac{5}{\sqrt{10}} = 52 \pm 3.58$、つまり $[48.4,\ 55.6]$。
もし $\sigma = 5$ が既知なら $1.96$ を使って $\pm 3.10$。$\sigma$ を推定している分、t分布の区間のほうが広くなる。

## 関連
[[標本分布]]（$T$ が出てくる元） / [[χ2乗分布]]（分母の正体） / [[自由度]] / [[分散・不偏分散]] / [[標準誤差]] / [[標準化]]
