---
name: plot
description: "Use for data visualization with matplotlib/seaborn — any chart, graph, figure or plot, and publication-ready economics/finance figures (coefficient plots, event-study, binscatter, RDD, parallel-trends, IRF, fan charts, portfolio-sort bars, Kaplan-Meier); StatsPAI result.plot() first, custom matplotlib fallback, Two-Level Figure rule (clean PDF to output/figures/, no titles/captions). Triggers: 'plot this', 'make a figure/chart', 'coefficient/event-study/binscatter/RDD plot', 'publication-ready figure'. NOT for interactive web dashboards/UI (use frontend-design); NOT for embedding or captioning a figure in LaTeX (use latex)."
---

# Plot: Unified Visualization Skill

## Routing: StatsPAI plots vs custom matplotlib

For figures derived from a StatsPAI result object (event-study, RD, synth gap, coefplot, density, balance), prefer `result.plot()` first — it carries CIs, bandwidths, and reference lines correctly, and outputs a matplotlib `Figure` you can post-customize.

```python
import statspai as sp
import matplotlib.pyplot as plt

cs = sp.callaway_santanna(data=df, y='lemp', t='year', i='countyreal', g='first_treat')

fig, ax = plt.subplots(figsize=(6.5, 4.5))
cs.plot(ax=ax)                 # if the StatsPAI plotter accepts an `ax` kwarg
ax.set_xlabel('Event time')    # post-customize
ax.set_ylabel('ATT')
ax.spines[['top', 'right']].set_visible(False)
fig.savefig('output/figures/event_study.pdf', dpi=300, bbox_inches='tight')
```

Not all StatsPAI plot methods accept an `ax` kwarg — check `sp.describe_function('<name>')` before assuming. If `result.plot()` returns a fully composed Figure that you cannot inject into, fall back to building from `result.tidy()` with custom matplotlib here.

**Use this skill (matplotlib + seaborn) for:**
- Custom multi-panel figures (GridSpec, mosaic, shared axes)
- Conceptual diagrams (DAGs, illustrations, schematic figures)
- Exploratory data analysis (EDA), distribution plots, pair plots
- Figures combining results from multiple estimators
- Anything matplotlib/seaborn-native that StatsPAI doesn't emit
- 3D plots and animations (only matplotlib has these)

## Two-Level Figure Rule (CRITICAL)

Figures saved to `output/figures/*.pdf` carry NO titles, NO paper-context annotations, NO captions. Captions and descriptions live in `sections/figures.tex`. This applies whether the figure comes from `result.plot()` or from custom matplotlib. Strip titles before saving:

```python
ax.set_title('')   # remove any title StatsPAI added
fig.savefig('output/figures/x.pdf', dpi=300, bbox_inches='tight')
```

## Quick Start

### Simple Matplotlib Plot

For exploratory work in a notebook, set a title freely. For publication output to `output/figures/`, OMIT `ax.set_title(...)` (caption goes in `sections/figures.tex`).

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)', linewidth=2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
fig.savefig('output/figures/plot.pdf', dpi=300, bbox_inches='tight')
```

### Simple Seaborn Plot
```python
import seaborn as sns
import pandas as pd

df = sns.load_dataset('tips')
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.tight_layout()
plt.savefig('scatter.pdf', dpi=300, bbox_inches='tight')
```

### Publication-Ready Defaults
```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'figure.figsize': (6.5, 4.5),
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.size': 4,
    'ytick.major.size': 4,
    'legend.fontsize': 9,
    'legend.frameon': False,
    'pdf.fonttype': 42,       # TrueType fonts in PDF
    'ps.fonttype': 42,
})
```

## When to Use Matplotlib vs Seaborn

| Task | Library | Rationale |
|------|---------|-----------|
| Custom multi-panel figures | matplotlib | Full layout control (GridSpec, mosaic) |
| Quick EDA / distributions | seaborn | One-liner with `pairplot`, `displot` |
| Faceted plots (row/col splits) | seaborn | Built-in `col`/`row` in figure-level functions |
| Heatmaps with annotations | seaborn | `sns.heatmap(annot=True)` is simpler |
| Economics/finance plots | matplotlib | Custom coefficient, event study, RDD plots |
| 3D plots | matplotlib | Only option (`mpl_toolkits.mplot3d`) |
| Animations | matplotlib | `FuncAnimation` |
| Fine-grained axis control | matplotlib | OO API for precise customization |
| Statistical overlays (CI, KDE) | seaborn | Automatic CI bands, KDE estimation |
| Combining both | both | Seaborn plots on matplotlib axes via `ax=` |

**Rule of thumb:** Start with seaborn for statistical plots and EDA. Switch to matplotlib when you need custom layouts, non-standard plot types, or pixel-level control.

## Plot Type Catalog

### Line Plots
Time series, trends, continuous functions.
```python
ax.plot(x, y, linewidth=2, marker='o', markevery=10, label='data')
ax.errorbar(x, y, yerr=err, fmt='o-', capsize=4)
```

### Scatter Plots
Relationships, correlations, clusters.
```python
ax.scatter(x, y, s=sizes, c=colors, cmap='viridis', alpha=0.6, edgecolors='k')
sns.scatterplot(data=df, x='x', y='y', hue='group', size='weight', style='type')
```

### Bar Charts
Categorical comparisons, counts.
```python
ax.bar(categories, values, color='steelblue', edgecolor='k')
sns.barplot(data=df, x='group', y='value', hue='condition', errorbar='ci')
```

### Histograms & Distributions
```python
ax.hist(data, bins=30, density=True, edgecolor='k', alpha=0.7)
sns.histplot(data=df, x='value', hue='group', stat='density', kde=True)
sns.kdeplot(data=df, x='value', fill=True, bw_adjust=1.5)
```

### Box & Violin Plots
Statistical distributions across categories.
```python
sns.boxplot(data=df, x='group', y='value', showmeans=True)
sns.violinplot(data=df, x='group', y='value', hue='condition', split=True, inner='quartile')
```

### Heatmaps
Correlation matrices, pivot tables.
```python
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True)
sns.clustermap(data, method='ward', z_score=0, cmap='viridis', figsize=(10, 10))
```

### Contour Plots
3D data on 2D plane.
```python
contourf = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
contour = ax.contour(X, Y, Z, levels=10, colors='k', linewidths=0.5)
ax.clabel(contour, inline=True, fontsize=8)
```

### Fill Between (Confidence Bands)
```python
ax.plot(x, y_mean, 'k-', linewidth=2)
ax.fill_between(x, y_mean - y_std, y_mean + y_std, alpha=0.3)
```

### Multi-Panel Figures
```python
# Matplotlib GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(2, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, :])

# Matplotlib mosaic
fig, axes = plt.subplot_mosaic([['left', 'right_top'],
                                 ['left', 'right_bottom']], figsize=(10, 8))

# Seaborn FacetGrid
sns.relplot(data=df, x='x', y='y', col='condition', row='group', kind='scatter', height=3)
```

### Pairwise & Joint Plots (Seaborn)
```python
sns.pairplot(df, hue='species', corner=True, diag_kind='kde')
sns.jointplot(data=df, x='x', y='y', kind='scatter', hue='group')
```

### Regression Plots (Seaborn)
```python
sns.regplot(data=df, x='x', y='y', order=2, ci=95)
sns.lmplot(data=df, x='x', y='y', hue='group', col='condition', height=4)
sns.residplot(data=df, x='x', y='y', lowess=True)
```

### 3D Plots (Matplotlib)
```python
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
```

For complete examples, see `references/plot_types.md`.

## Figure Output Format (CRITICAL)

Scripts save figures as **PDF only** to `output/figures/`. Figures must contain ONLY the plot — no `fig.suptitle()` with paper-specific titles, no embedded captions, no annotation blocks describing the paper context. All titles, captions, and descriptions go in the wrapper file (`sections/figures.tex`), not in the figure itself.

Axis labels, legends, and data annotations (e.g., coefficient values on a plot) are fine — these are part of the figure content. What is NOT allowed: paper-level metadata like "Table III reports..." or "Source: CRSP/Compustat" as figure text.

```python
# CORRECT: clean figure, PDF output
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(x, y)
ax.set_xlabel('Year')
ax.set_ylabel('Emissions (tCO2e)')
ax.legend()
plt.savefig('output/figures/trend.pdf', dpi=300, bbox_inches='tight')
plt.close()
```

## Publication-Ready Configuration

### Journal Presets

**Economics journals (AER, QJE, JPE, Econometrica):**
- Single-column width: 3.4 in; double-column: 6.75 in
- Font: Times New Roman or Computer Modern, 8-10pt
- PDF with embedded TrueType fonts (`pdf.fonttype: 42`)

**Finance journals (JF, JFE, RFS):**
- Similar to economics; figures typically 6-7 in wide
- Sans-serif (Arial/Helvetica) also accepted

See `references/styling_guide.md` for full journal presets.

### Key Settings for Journals
```python
plt.rcParams.update({
    'pdf.fonttype': 42,           # CRITICAL: embeds TrueType fonts
    'ps.fonttype': 42,
    'font.family': 'serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'savefig.dpi': 300,
})
```

## Economics & Finance Plots

This skill includes production-quality templates for common academic economics plots:

1. **Coefficient plots** with confidence intervals (from statsmodels/linearmodels)
2. **Event study plots** (dynamic treatment effects with pre/post periods)
3. **Binscatter plots** (conditional means with optional controls)
4. **RDD plots** (regression discontinuity with polynomial fits)
5. **Parallel trends plots** (DID pre-trends verification)
6. **Fan charts** (forecast uncertainty bands)
7. **IRF plots** (impulse response functions from VAR/local projections)
8. **Portfolio sort bar charts** (quintile/decile returns)
9. **Fama-MacBeth coefficient time series**
10. **Kaplan-Meier survival curves**

See `references/economics_plots.md` for full working code examples.

Helper functions are available in `scripts/econ_plots.py`:
```python
from econ_plots import coefficient_plot, event_study_plot, binscatter, rdd_plot
fig, ax = coefficient_plot(results, var_names=['x1', 'x2', 'x3'])
```

## Seaborn Objects Interface (Modern API)

Declarative, composable API (seaborn 0.12+):
```python
from seaborn import objects as so
(
    so.Plot(df, x='total_bill', y='tip', color='day')
    .add(so.Dot(alpha=0.5))
    .add(so.Line(), so.PolyFit(order=2))
    .facet(col='time')
    .label(x='Total Bill ($)', y='Tip ($)')
    .layout(size=(10, 6))
)
```

See `references/seaborn_core.md` for full objects interface guide.

## Common Issues Quick Reference

| Problem | Solution |
|---------|----------|
| Overlapping labels | `constrained_layout=True` or `bbox_inches='tight'` |
| Memory leak (many figs) | `plt.close(fig)` after saving |
| Font not found | `plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']` |
| Colorbar shrinks plot | Use `constrained_layout=True` or `make_axes_locatable` |
| Log scale with zeros | Use `symlog` or filter `data > 0` |
| PDF fonts not embedded | Set `pdf.fonttype: 42` |
| Dates show as numbers | Use `mdates.DateFormatter('%Y-%m-%d')` |
| `AxesSubplot not subscriptable` | `fig, ax = plt.subplots()` returns single ax, not array |
| Seaborn legend outside plot | `g._legend.set_bbox_to_anchor((0.9, 0.5))` |
| KDE too smooth/jagged | Adjust `bw_adjust` (lower = less smooth) |

See `references/common_issues.md` for detailed solutions.

## Color Palette Quick Reference

**Sequential (ordered data):** `viridis`, `plasma`, `inferno`, `magma`, `cividis`
**Diverging (centered):** `coolwarm`, `RdBu`, `vlag`, `icefire`
**Qualitative (categories):** `tab10`, `Set2`, `colorblind`
**Colorblind-friendly:** `viridis`, `cividis`, `colorblind` (seaborn)

**Avoid:** `jet` (not perceptually uniform)

## Reference Files

- **`references/matplotlib_core.md`** - Figure/Axes API, core classes, parameters, GridSpec, 3D, animation
- **`references/seaborn_core.md`** - Function interface, objects interface, grids, multi-plot patterns
- **`references/styling_guide.md`** - Colormaps, rcParams, journal presets, typography, color palettes
- **`references/plot_types.md`** - Comprehensive plot type catalog with code examples
- **`references/economics_plots.md`** - 10 economics/finance plot types with full working code
- **`references/common_issues.md`** - Troubleshooting guide for common problems

## Scripts

- **`scripts/plot_template.py`** - Template demonstrating various plot types with best practices
- **`scripts/style_configurator.py`** - Configure styles and generate .mplstyle files
- **`scripts/econ_plots.py`** - Helper functions for economics/finance plot types

