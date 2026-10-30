# Finance plotting guide

Use these patterns for student investment, portfolio, risk, earnings, and peer-analysis figures. Adapt the calculations to the supplied data definitions rather than assuming a field name implies a convention.

## Indexed performance

Use indexed performance to compare series with different price levels. Align dates, choose a common start, and state the base.

```python
prices = prices.sort_index().dropna(how='all')
common = prices.dropna()
wealth = common.div(common.iloc[0]).mul(100)

fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
wealth.plot(ax=ax)
ax.set_title('Indexed performance')
ax.set_xlabel('Date')
ax.set_ylabel('Index (common start = 100)')
ax.legend(frameon=False)
```

`dropna()` across all series gives a common complete sample, but it can discard meaningful history. Inspect missingness before choosing that rule and disclose a shortened comparison period.

Use adjusted prices when the analysis intends to reflect corporate-action-adjusted performance. An adjusted-price wealth index is not automatically a full total-return index; dividends must be treated according to the data definition.

## Drawdown

```python
running_peak = wealth.cummax()
drawdown = wealth.div(running_peak).sub(1)

ax.fill_between(drawdown.index, drawdown * 100, 0, alpha=0.3)
ax.plot(drawdown.index, drawdown * 100)
ax.set_ylabel('Drawdown (%)')
```

Check that the running peak begins at the intended analysis date. A drawdown chart does not show losses before the first observation.

## Rolling volatility

```python
returns = prices.pct_change(fill_method=None)
rolling_vol = returns.rolling(63).std() * (252 ** 0.5) * 100

ax.plot(rolling_vol.index, rolling_vol)
ax.set_ylabel('Annualized volatility (%)')
```

State the return type, 63-observation window, and 252-day annualization convention. Do not show the initial unavailable window as zero. For weekly or monthly data, use an appropriate annualization factor and explain it.

## Portfolio allocation

Use horizontal bars for a small number of holdings or grouped exposure categories.

```python
weights = weights.sort_values()
colors = ['#c44e52' if x < 0 else '#4c72b0' for x in weights]
ax.barh(weights.index, weights * 100, color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Portfolio weight (%)')
```

Check the weight convention and whether weights sum to 100%. Negative and leveraged positions should remain visible. A pie chart is usually harder to compare and handles short positions poorly.

## Performance contribution or attribution

Use bars for contributions by holding, sector, factor, or period. Label whether values are percentage points of contribution, percent returns, or another unit. Reconcile their sum with the total when the method says they should add up.

Sort categories by contribution only when rank is more important than a natural sector or factor order. Keep positive and negative colors consistent with the report.

## Factor exposures

A coefficient plot can show exposures with confidence intervals when supplied by the estimation result. Do not treat factor loadings as return contributions. Label the estimation sample, factor definitions, and interval level in the accompanying note.

For a simple exposure dashboard without intervals, horizontal bars with a zero reference line are clearer than a radar chart.

## Peer valuation and operating comparisons

Use aligned bars, dot plots, or small multiples. Before plotting, align:

- Fiscal period and whether values are historical or estimated.
- Currency and units.
- Enterprise-value versus equity-value multiples.
- Margin and growth definitions.
- Missing or not-meaningful values.

Do not convert a missing multiple to zero. Exclude it visibly or mark it `n/a` in an accompanying table.

## Earnings figures

Common exhibits include revenue and profit by period, margin trends, actual versus consensus, segment contributions, and guidance changes. Keep reported and estimated periods visually distinct. For actual-versus-estimate comparisons, state the estimate source and date.

## Returns distributions

Histograms can show the distribution of periodic returns, but add the return frequency and sample period. A normal curve or value-at-risk line is an additional model assumption, not a default decoration. Include it only when the user requests it or the analysis defines it.

## Risk-return scatter

Use return and risk measures with matching periods and annualization. Label each point directly when the number of portfolios or assets is small. A benchmark or efficient-frontier line requires an actual calculation; do not add an illustrative curve to a real-results chart without labeling it.

## Source and context notes

For standalone figures, use a concise note such as:

```python
fig.text(
    0.01,
    -0.02,
    'Source: supplied adjusted close data; daily observations through 30 September 2026.',
    fontsize=8,
)
```

Replace every detail with the actual source and period. If no source was supplied, identify the file or user-provided dataset rather than inventing a provider.

## Recurring-report figures

Use stable axis conventions and color assignments across runs so changes are visible. Let limits adapt only when doing so will not hide an important change. A failed refresh should not silently overwrite the previous good figure. Write to a temporary file, validate the result, and then replace the final output according to the project's workflow.
