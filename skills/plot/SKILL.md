---
name: plot
description: "Create, revise, and verify static charts from data using matplotlib or seaborn, with reproducible code and PNG/PDF output. Use for trends, comparisons, distributions, performance, risk, cash flow, variance, or model-result figures. Not for interactive interfaces (use frontend-design), report layout (use latex), or estimation without a chart."
---

# Static data visualization

Build figures that answer a specific question and can be reproduced from a script. A polished chart must also have the right data, transformation, units, and comparison period.

## Workflow

1. **Inspect the data.** Confirm field names, dates, frequency, units, currency, missing values, and whether the series is a price, return, percentage, or ratio.
2. **Choose the chart from the question.** Use a line for ordered time series, bars for discrete comparisons, scatter for relationships, histograms for distributions, and multi-panel layouts when comparisons need separate scales.
3. **Define the finance transformation.** Common examples include simple versus log returns, adjusted prices, indexation to 100, rolling windows, drawdown, and annualization. State the convention in the script or figure note.
4. **Render with matplotlib or seaborn.** Use the project's existing dependencies and coding style. Do not install a library merely for aesthetics.
5. **Validate the content.** Reconcile a few plotted values with the input, check the date range and axis direction, and inspect the saved image.
6. **Save both the script and figure in their proper project locations.** Reusable code belongs in `src/`; generated figures belong in `output/figures/`.

Read [references/finance_plots.md](references/finance_plots.md) before creating investment, portfolio, risk, earnings, or peer-comparison charts.

## Output modes

### Standalone finance figure

This is the default. Save a PNG at 300 dpi to `output/figures/` unless the user requests another format. Include:

- A short descriptive title.
- Axis labels with units or percentage conventions.
- A readable legend or direct labels.
- Source and data-as-of note using actual supplied information.
- A note for adjusted prices, illustrative data, or a nonstandard calculation when relevant.

### Figure embedded in a LaTeX report

Save PDF when vector output is useful, or PNG when requested. Keep the axis labels and data annotations. The title may be omitted when the LaTeX caption supplies it; do not duplicate a long caption inside the image. Coordinate with the `latex` skill for wrappers and notes.

Use a title and source note when the figure must stand alone. For an embedded figure, keep those details in its report wrapper.

## Finance checks

Explain one plotted calculation when the user is learning a method. For analytical work, expose transformation choices and sensitivity. For decision summaries, emphasize the comparison and exception that matter, while retaining units and source context.

Apply the checks relevant to the chart:

- Use adjusted prices for total-return-like historical comparisons when the data definition requires them; do not label adjusted prices as raw prices.
- Show whether returns are daily, cumulative, annualized, or excess returns.
- For performance comparisons, use a common start date and state the base when indexing to 100.
- For drawdowns, compute from the chosen wealth or price series and show negative values consistently.
- For volatility, state the return frequency, rolling window, and annualization factor.
- For portfolio weights, check whether they sum to 100% and show negative or leveraged positions honestly.
- For peer comparisons, align units, fiscal periods, currencies, and metric definitions.
- For factors and attribution, distinguish percentage points from percent and exposures from returns.
- Do not fabricate a benchmark, confidence interval, forecast, or source note.

## Defaults

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'figure.figsize': (8, 4.5),
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'lines.linewidth': 1.8,
    'legend.frameon': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})
```

Use a colorblind-aware palette, adequate contrast, and direct labeling where it reduces legend work. Avoid `jet`, decorative 3D effects, unnecessary dual axes, and truncated bar-chart baselines.

## Standalone example

```python
fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
ax.plot(wealth.index, wealth, label='Portfolio')
ax.set_title('Portfolio growth since 31 December 2025')
ax.set_xlabel('Date')
ax.set_ylabel('Wealth index (start = 100)')
ax.legend()
fig.text(0.01, -0.02, 'Source: supplied adjusted prices; data through 30 September 2026.', fontsize=8)
fig.savefig('output/figures/portfolio_growth.png', dpi=300, bbox_inches='tight')
plt.close(fig)
```

Use the actual dates and source from the data rather than copying this example's text.

## Specialized figures

- To export a reusable style, use [scripts/style_configurator.py](scripts/style_configurator.py):
  `--list` shows the finance, presentation, web, dark, and minimal presets;
  `--preset finance --output chart.mplstyle` saves one. `--preview` displays an
  illustrative chart and also saves `chart_preview.png` when an output path is supplied.
- For core matplotlib APIs and multi-panel layouts, read [references/matplotlib_core.md](references/matplotlib_core.md).
- For seaborn statistical plots, read [references/seaborn_core.md](references/seaborn_core.md).
- For typography, palettes, and sizing, read [references/styling_guide.md](references/styling_guide.md).
- For rendering problems, read [references/common_issues.md](references/common_issues.md).

When a StatsPAI result object is already available in the project, `result.plot()` can preserve estimator-specific intervals and reference lines. Check the installed API before assuming an `ax` argument, and post-process the figure to meet the output mode above.

## Final inspection

Open the saved image and check it at the size the reader will see. Look for clipped labels, unreadable ticks, overlapping series, misleading scales, stale dates, and inconsistent number formatting. Then verify that rerunning the script reproduces the same figure from the same inputs.
