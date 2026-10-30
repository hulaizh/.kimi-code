# Seaborn Core Reference

## Table of Contents
- [Function Interface](#function-interface)
  - [Relational Plots](#relational-plots)
  - [Distribution Plots](#distribution-plots)
  - [Categorical Plots](#categorical-plots)
  - [Regression Plots](#regression-plots)
  - [Matrix Plots](#matrix-plots)
- [Figure-Level vs Axes-Level](#figure-level-vs-axes-level)
- [Multi-Plot Grids](#multi-plot-grids)
- [Objects Interface (Modern API)](#objects-interface-modern-api)
  - [Plot Class](#plot-class)
  - [Mark Objects](#mark-objects)
  - [Stat Objects](#stat-objects)
  - [Move Objects](#move-objects)
  - [Scale Objects](#scale-objects)
- [Data Structure](#data-structure)
- [Color Palettes](#color-palettes)
- [Theming](#theming)
- [Common Patterns](#common-patterns)

## Function Interface

### Relational Plots

**scatterplot()** - Points for individual observations
```python
sns.scatterplot(data=df, x='x', y='y',
    hue='group',      # Color by group
    size='weight',     # Size by variable
    style='type',      # Marker by type
    palette='Set2',    sizes=(20, 200),
    alpha=0.6,         ax=ax)
```

**lineplot()** - Trends with automatic CI
```python
sns.lineplot(data=df, x='time', y='signal',
    hue='condition',   style='subject',
    estimator='mean',  errorbar=('ci', 95),  # or 'sd', 'se', 'pi'
    err_style='band',  markers=True,
    sort=True,         ax=ax)
```

**relplot()** - Figure-level with faceting
```python
sns.relplot(data=df, x='x', y='y',
    hue='group',       col='condition',    row='time',
    kind='scatter',    # or 'line'
    height=3,          aspect=1.5,         col_wrap=3)
```

### Distribution Plots

**histplot()** - Frequency distributions
```python
sns.histplot(data=df, x='value',
    hue='group',       stat='density',     # 'count', 'frequency', 'probability', 'percent'
    bins=30,           kde=True,
    multiple='layer',  # 'dodge', 'stack', 'fill'
    element='bars',    # 'step', 'poly'
    cumulative=False,  ax=ax)
```

**kdeplot()** - Smooth density estimates
```python
# Univariate
sns.kdeplot(data=df, x='value', hue='group',
    fill=True,         bw_adjust=1.5,
    common_norm=False, cut=3,              ax=ax)
# Bivariate
sns.kdeplot(data=df, x='x', y='y',
    fill=True,         levels=10,          thresh=0.05)
```

**ecdfplot()** - Empirical CDF
```python
sns.ecdfplot(data=df, x='value', hue='group', stat='proportion')
```

**displot()** - Figure-level distributions
```python
sns.displot(data=df, x='value', hue='group',
    col='condition',   kind='kde',         # 'hist', 'kde', 'ecdf'
    fill=True,         rug=True,
    height=3,          aspect=1.5,         col_wrap=3)
```

**jointplot()** - Bivariate with marginals
```python
g = sns.jointplot(data=df, x='x', y='y',
    hue='group',       kind='scatter',     # 'kde', 'hist', 'hex', 'reg', 'resid'
    height=8,          ratio=4,            space=0.1,
    joint_kws={'alpha': 0.5},
    marginal_kws={'kde': True, 'bins': 30})
```

**pairplot()** - Matrix of pairwise relationships
```python
sns.pairplot(df,
    hue='species',     vars=['a', 'b', 'c'],
    kind='scatter',    diag_kind='kde',    # 'hist', 'kde', None
    corner=True,       height=2.5,
    palette='Set2',    plot_kws={'alpha': 0.5})
```

### Categorical Plots

**Scatterplots:** `stripplot()`, `swarmplot()`
```python
sns.stripplot(data=df, x='group', y='value', hue='sex', dodge=True, jitter=0.2, alpha=0.5)
sns.swarmplot(data=df, x='group', y='value', hue='sex', dodge=True, size=4)
# swarmplot: avoid for >1000 points (use stripplot instead)
```

**Distributions:** `boxplot()`, `violinplot()`, `boxenplot()`
```python
sns.boxplot(data=df, x='group', y='value',
    hue='condition',   showmeans=True,     notch=True,
    palette='Set3',    whis=1.5,           width=0.6)

sns.violinplot(data=df, x='group', y='value',
    hue='condition',   split=True,         inner='quartile',  # 'box', 'point', 'stick'
    bw_adjust=0.8,     palette='muted')

sns.boxenplot(data=df, x='group', y='value', k_depth='tukey')
```

**Estimates:** `barplot()`, `pointplot()`, `countplot()`
```python
sns.barplot(data=df, x='group', y='value',
    hue='condition',   estimator='mean',
    errorbar=('ci', 95),  capsize=0.1,     dodge=True)

sns.pointplot(data=df, x='time', y='score',
    hue='treatment',   markers=['o', 's'],
    linestyles=['-', '--'],  dodge=0.3,    capsize=0.1)

sns.countplot(data=df, x='category', hue='type', stat='percent')
```

**catplot()** - Figure-level categorical
```python
sns.catplot(data=df, x='group', y='value',
    hue='condition',   col='time',
    kind='violin',     # 'strip', 'swarm', 'box', 'violin', 'boxen', 'bar', 'point', 'count'
    split=True,        height=4,           aspect=0.8)
```

### Regression Plots

```python
sns.regplot(data=df, x='x', y='y',
    order=2,           ci=95,
    robust=True,       lowess=False,
    scatter_kws={'alpha': 0.5},
    line_kws={'color': 'red'},
    ax=ax)

sns.lmplot(data=df, x='x', y='y',
    hue='group',       col='condition',
    height=4,          aspect=1.2)

sns.residplot(data=df, x='x', y='y', lowess=True,
    scatter_kws={'alpha': 0.5},
    line_kws={'color': 'red', 'lw': 2})
```

### Matrix Plots

```python
# Heatmap
sns.heatmap(corr_matrix,
    annot=True,        fmt='.2f',
    cmap='coolwarm',   center=0,
    square=True,       linewidths=1,
    mask=np.triu(np.ones_like(corr_matrix, dtype=bool)),
    cbar_kws={'shrink': 0.8, 'label': 'Correlation'},
    ax=ax)

# Clustermap
g = sns.clustermap(data_matrix,
    method='ward',     metric='euclidean',
    z_score=0,         cmap='RdBu_r',     center=0,
    row_colors=row_colors,
    col_colors=col_colors,
    figsize=(12, 10),  dendrogram_ratio=(0.1, 0.1),
    linewidths=0.5)
```

## Figure-Level vs Axes-Level

| Feature | Axes-Level | Figure-Level |
|---------|-----------|-------------|
| Accept `ax=` | Yes | No |
| Return type | `Axes` | `FacetGrid` / `JointGrid` / `PairGrid` |
| Faceting | Manual | Built-in `col`, `row` |
| Size control | `figsize` on `plt.subplots()` | `height`, `aspect` |
| Examples | `scatterplot`, `histplot`, `boxplot`, `heatmap` | `relplot`, `displot`, `catplot`, `lmplot` |

**Axes-level** for custom multi-plot layouts:
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(data=df, x='x', y='y', ax=axes[0, 0])
sns.histplot(data=df, x='x', ax=axes[0, 1])
sns.boxplot(data=df, x='group', y='y', ax=axes[1, 0])
sns.heatmap(df.corr(), ax=axes[1, 1])
```

**Figure-level** for faceted plots:
```python
g = sns.relplot(data=df, x='x', y='y', col='condition', row='group', height=3, aspect=1.2)
g.set_axis_labels('X Variable', 'Y Variable')
g.set_titles('{col_name} | {row_name}')
```

## Multi-Plot Grids

### FacetGrid
```python
g = sns.FacetGrid(df, col='time', row='sex', hue='smoker',
                  height=3, aspect=1.5, margin_titles=True)
g.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.7)
g.add_legend()
g.set_axis_labels('Total Bill ($)', 'Tip ($)')
g.set_titles('{col_name} | {row_name}')
```

### PairGrid
```python
g = sns.PairGrid(df, hue='species', vars=['a', 'b', 'c'], corner=True)
g.map_upper(sns.scatterplot, alpha=0.5)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot, kde=True)
g.add_legend()
```

### JointGrid
```python
g = sns.JointGrid(data=df, x='x', y='y', hue='group', height=6, ratio=5)
g.plot_joint(sns.scatterplot, alpha=0.5)
g.plot_marginals(sns.histplot, kde=True)
g.set_axis_labels('Variable X', 'Variable Y')
```

## Objects Interface (Modern API)

The `seaborn.objects` interface (v0.12+) is a declarative, composable API.

### Plot Class

```python
from seaborn import objects as so

# Basic usage
p = (
    so.Plot(data=df, x='x', y='y', color='group')
    .add(so.Dot(alpha=0.5))
    .add(so.Line(), so.PolyFit(order=2))
    .facet(col='condition', wrap=3)
    .scale(
        x=so.Continuous().tick(every=5),
        color=so.Nominal(['#1f77b4', '#ff7f0e', '#2ca02c']),
    )
    .label(x='X Variable', y='Y Variable', title='Analysis')
    .limit(x=(0, 100), y=(0, 50))
    .layout(size=(10, 6), engine='constrained')
    .share(x=True, y=False)
    .theme({**sns.axes_style('whitegrid')})
)
p.show()
p.save('plot.pdf', dpi=300)
```

**Key methods:**
- `.add(mark, *transforms, orient=None, legend=True, data=None, **variables)` - Add layer
- `.facet(col, row, order, wrap)` - Faceted subplots
- `.pair(x, y, wrap, cross)` - Pairwise subplots
- `.scale(**scales)` - Customize mappings
- `.limit(x, y)` - Set axis limits
- `.label(x, y, color, title)` - Set labels
- `.theme(config)` - Apply style
- `.layout(size, extent, engine)` - Configure layout
- `.share(x, y)` - Control axis sharing
- `.on(target)` - Plot on existing matplotlib axes/figure

### Mark Objects

| Mark | Description | Key Properties |
|------|-------------|---------------|
| `so.Dot()` | Points/markers | `color`, `alpha`, `marker`, `pointsize`, `edgecolor` |
| `so.Line()` | Connected line | `color`, `alpha`, `linewidth`, `linestyle` |
| `so.Path()` | Line in data order | Same as Line |
| `so.Bar()` | Single bars | `color`, `alpha`, `edgecolor`, `width` |
| `so.Bars()` | Multiple bars | Same as Bar (use with Agg/Est) |
| `so.Area()` | Filled area | `color`, `alpha`, `edgecolor` |
| `so.Band()` | Range band | Same as Area (needs ymin/ymax or Est) |
| `so.Range()` | Line + endpoints | `color`, `linewidth`, `marker` |
| `so.Dash()` | Short lines | `color`, `linewidth`, `width` |
| `so.Text()` | Text labels | `color`, `fontsize`, `halign`, `valign` |

### Stat Objects

| Stat | Description | Key Parameters |
|------|-------------|---------------|
| `so.Agg(func)` | Aggregate | `func`: 'mean', 'median', 'sum', callable |
| `so.Est(func, errorbar)` | Estimate + CI | `func`, `errorbar`: ('ci', 95), 'sd', 'se' |
| `so.Hist(stat, bins)` | Histogram | `stat`: 'count', 'density', 'probability' |
| `so.KDE(bw_adjust)` | Kernel density | `bw_method`, `bw_adjust`, `gridsize` |
| `so.Count()` | Count obs | (no params) |
| `so.PolyFit(order)` | Polynomial fit | `order`: 1=linear, 2=quadratic |
| `so.Perc(k)` | Percentiles | `k`: number of intervals |

### Move Objects

| Move | Description | Key Parameters |
|------|-------------|---------------|
| `so.Dodge(gap)` | Side-by-side | `empty`: 'keep'/'drop', `gap` |
| `so.Stack()` | Stack vertically | (no params) |
| `so.Jitter(width)` | Random noise | `width`, `height`, `seed` |
| `so.Shift(x, y)` | Constant shift | `x`, `y` (data units) |
| `so.Norm(func)` | Normalize | `func`: 'max', 'sum', 'area' |

### Scale Objects

```python
# Continuous (numeric)
so.Continuous(values=(0, 1), trans='log')  # trans: 'log', 'sqrt', 'symlog'
    .tick(every=5, at=[1, 10, 100])
    .label(like='{x:.1f}')

# Nominal (categorical)
so.Nominal(values=['#1f77b4', '#ff7f0e'], order=['A', 'B', 'C'])

# Temporal (datetime)
so.Temporal().tick(every=('month', 1)).label(concise=True)
```

## Data Structure

**Long-form (preferred):** Each variable is a column, each observation is a row.
```
   subject  condition  measurement
0        1    control         10.5
1        1  treatment         12.3
```

**Wide-form:** Variables spread across columns. Convert with:
```python
df_long = df.melt(var_name='condition', value_name='measurement')
```

## Color Palettes

**Qualitative:** `"deep"`, `"muted"`, `"pastel"`, `"bright"`, `"dark"`, `"colorblind"`
**Sequential:** `"rocket"`, `"mako"`, `"flare"`, `"crest"`, `"viridis"`, `"magma"`
**Diverging:** `"vlag"`, `"icefire"`, `"coolwarm"`, `"Spectral"`

```python
sns.set_palette("colorblind")
sns.color_palette("husl", 8)              # 8 evenly-spaced hues
custom = ['#E64B35', '#4DBBD5', '#00A087']
sns.set_palette(custom)
```

## Theming

```python
# Set global theme
sns.set_theme(style='whitegrid', palette='colorblind', font='Arial', font_scale=1.1)

# Styles: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
sns.set_style("ticks")
sns.despine(left=False, bottom=False, offset=10, trim=True)

# Contexts: 'paper', 'notebook', 'talk', 'poster'
sns.set_context("talk", font_scale=1.2)

# Publication-ready
sns.set_theme(context='paper', style='ticks', palette='colorblind', font='Arial',
    font_scale=1.1,
    rc={'pdf.fonttype': 42, 'axes.linewidth': 1.0, 'legend.frameon': False})
```

## Common Patterns

### EDA
```python
sns.pairplot(df, hue='target', corner=True)
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
```

### Publication Multi-Panel
```python
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.scatterplot(data=df, x='x1', y='y', hue='group', ax=axes[0, 0])
sns.histplot(data=df, x='x1', hue='group', ax=axes[0, 1])
sns.violinplot(data=df, x='group', y='y', ax=axes[1, 0])
sns.heatmap(df.pivot_table(values='y', index='x1', columns='x2'), ax=axes[1, 1])
sns.despine()
plt.tight_layout()
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

### Significance Annotations
```python
def add_significance_bar(ax, x1, x2, y, h, text):
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], 'k-', lw=1.5)
    ax.text((x1+x2)/2, y+h, text, ha='center', va='bottom')

sns.boxplot(data=df, x='group', y='value', ax=ax)
add_significance_bar(ax, 0, 2, y_max + 1, 0.5, '***')
```

### Before/After Comparison
```python
fig, ax = plt.subplots(figsize=(8, 6))
for subj in df['subject'].unique():
    d = df[df['subject'] == subj]
    ax.plot(d['timepoint'], d['value'], 'o-', alpha=0.3, color='gray')
sns.pointplot(data=df, x='timepoint', y='value', color='red',
              markers='D', errorbar=('ci', 95), capsize=0.2, ax=ax)
```
