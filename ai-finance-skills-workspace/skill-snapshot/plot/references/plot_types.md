# Plot Types Catalog

## Table of Contents
- [Line Plots](#line-plots)
- [Scatter Plots](#scatter-plots)
- [Bar Charts](#bar-charts)
- [Histograms](#histograms)
- [Box and Violin Plots](#box-and-violin-plots)
- [Heatmaps](#heatmaps)
- [Contour Plots](#contour-plots)
- [Fill Between](#fill-between)
- [Pie and Donut Charts](#pie-and-donut-charts)
- [Polar and Radar Charts](#polar-and-radar-charts)
- [Quiver and Stream Plots](#quiver-and-stream-plots)
- [3D Plots](#3d-plots)
- [Specialized Plots](#specialized-plots)
- [Seaborn-Specific Plots](#seaborn-specific-plots)
- [Plot Selection Guide](#plot-selection-guide)

## Line Plots

**Use:** Time series, continuous data, trends, function visualization

### Basic + Multiple Lines
```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, linewidth=2, label='Series A')
ax.plot(x, y2, linewidth=2, linestyle='--', label='Series B')
ax.plot(x, y3, linewidth=2, linestyle=':', label='Series C')
ax.legend()
```

### Line with Markers
```python
ax.plot(x, y, marker='o', markersize=6, linewidth=1.5,
        markerfacecolor='white', markeredgecolor='blue', markevery=5)
```

### Step Plot
```python
ax.step(x, y, where='mid', linewidth=2)  # where: 'pre', 'post', 'mid'
```

### Error Bars
```python
ax.errorbar(x, y, yerr=err, fmt='o-', linewidth=1.5,
            capsize=4, capthick=1.5, elinewidth=1, label='Data')
```

### Seaborn lineplot (auto CI)
```python
sns.lineplot(data=df, x='time', y='value', hue='group',
             errorbar=('ci', 95), err_style='band')
```

## Scatter Plots

**Use:** Correlations, relationships, clusters, outlier detection

### Basic Scatter
```python
ax.scatter(x, y, s=50, alpha=0.6, edgecolors='k', linewidths=0.5)
```

### Multi-dimensional Scatter
```python
sc = ax.scatter(x, y, s=sizes*100, c=colors, cmap='viridis',
                alpha=0.6, edgecolors='k', linewidths=0.5)
plt.colorbar(sc, ax=ax, label='Color variable')
```

### Seaborn scatterplot (semantic encoding)
```python
sns.scatterplot(data=df, x='x', y='y', hue='group', size='weight',
                style='type', palette='Set2', sizes=(20, 200))
```

### Hexbin (large datasets)
```python
hb = ax.hexbin(x, y, gridsize=30, cmap='Blues', mincnt=1)
plt.colorbar(hb, ax=ax, label='Count')
```

## Bar Charts

**Use:** Categorical comparisons, discrete data, counts

### Vertical + Horizontal
```python
ax.bar(categories, values, color='steelblue', edgecolor='k', linewidth=1)
ax.barh(categories, values, color='coral', edgecolor='k')
```

### Grouped Bars
```python
x_pos = np.arange(len(categories))
width = 0.35
ax.bar(x_pos - width/2, vals1, width, label='Group 1')
ax.bar(x_pos + width/2, vals2, width, label='Group 2')
ax.set_xticks(x_pos)
ax.set_xticklabels(categories)
ax.legend()
```

### Stacked Bars
```python
ax.bar(categories, vals1, label='Part 1')
ax.bar(categories, vals2, bottom=vals1, label='Part 2')
ax.bar(categories, vals3, bottom=vals1 + vals2, label='Part 3')
ax.legend()
```

### Bars with Error Bars + Hatching
```python
ax.bar(x_pos, values, yerr=errors, capsize=5,
       color='white', edgecolor='black', hatch='//', linewidth=1.5)
```

### Seaborn barplot (auto stats)
```python
sns.barplot(data=df, x='group', y='value', hue='condition',
            estimator='mean', errorbar=('ci', 95), capsize=0.1)
```

## Histograms

**Use:** Distributions, frequency analysis

### Basic + Density Overlay
```python
ax.hist(data, bins=30, density=True, alpha=0.7, edgecolor='k', color='steelblue')
from scipy.stats import norm
mu, std = norm.fit(data)
x_fit = np.linspace(data.min(), data.max(), 100)
ax.plot(x_fit, norm.pdf(x_fit, mu, std), 'r-', lw=2, label=f'Normal (μ={mu:.2f})')
```

### Multiple Overlapping
```python
ax.hist(data1, bins=30, alpha=0.5, label='A')
ax.hist(data2, bins=30, alpha=0.5, label='B')
ax.legend()
```

### 2D Histogram
```python
h = ax.hist2d(x, y, bins=30, cmap='Blues')
plt.colorbar(h[3], ax=ax, label='Count')
```

### Seaborn histplot (rich options)
```python
sns.histplot(data=df, x='value', hue='group', stat='density',
             bins=30, kde=True, multiple='layer', alpha=0.5)
```

## Box and Violin Plots

**Use:** Statistical distributions, outlier detection, comparing groups

### Box Plot
```python
# Matplotlib
bp = ax.boxplot([d1, d2, d3], labels=['A', 'B', 'C'],
    patch_artist=True, showmeans=True,
    boxprops=dict(facecolor='lightblue', edgecolor='k'),
    medianprops=dict(color='red', linewidth=2),
    meanprops=dict(marker='D', markerfacecolor='green', markersize=8))

# Seaborn
sns.boxplot(data=df, x='group', y='value', hue='condition',
            showmeans=True, notch=True, palette='Set3')
```

### Violin Plot
```python
# Seaborn (better defaults)
sns.violinplot(data=df, x='group', y='value', hue='sex',
               split=True, inner='quartile', palette='muted')
```

### Box + Strip (combined)
```python
sns.boxplot(data=df, x='group', y='value', palette='Set2', ax=ax)
sns.stripplot(data=df, x='group', y='value', color='k', alpha=0.3, size=3, ax=ax)
```

## Heatmaps

**Use:** Correlation matrices, pivot tables, gene expression

### Matplotlib imshow
```python
im = ax.imshow(matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
plt.colorbar(im, ax=ax, label='Value')
# Annotations
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        ax.text(j, i, f'{matrix[i, j]:.2f}', ha='center', va='center')
```

### Seaborn heatmap
```python
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1,
            mask=np.triu(np.ones_like(corr, dtype=bool)),
            cbar_kws={'shrink': 0.8, 'label': 'Correlation'})
```

### Clustermap
```python
g = sns.clustermap(data, method='ward', z_score=0, cmap='RdBu_r', center=0,
                   row_colors=colors, figsize=(12, 10),
                   dendrogram_ratio=(0.1, 0.1), linewidths=0.5)
```

## Contour Plots

**Use:** 3D data on 2D plane, topography, function surfaces

### Contour Lines + Filled
```python
contourf = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
contour = ax.contour(X, Y, Z, levels=10, colors='k', linewidths=0.5, alpha=0.4)
ax.clabel(contour, inline=True, fontsize=8)
plt.colorbar(contourf, ax=ax, label='Z value')
```

## Fill Between

**Use:** Uncertainty bands, confidence intervals, areas

### Between Two Curves
```python
ax.plot(x, y_mean, 'k-', linewidth=2, label='Mean')
ax.fill_between(x, y_mean - std, y_mean + std, alpha=0.3, label='±1σ')
ax.fill_between(x, y_mean - 2*std, y_mean + 2*std, alpha=0.15, label='±2σ')
```

### Conditional Fill
```python
ax.fill_between(x, y1, y2, where=(y2 >= y1), alpha=0.3,
                color='green', interpolate=True, label='y2 > y1')
ax.fill_between(x, y1, y2, where=(y2 < y1), alpha=0.3,
                color='red', interpolate=True, label='y2 < y1')
```

## Pie and Donut Charts

**Use:** Proportions (use sparingly; bars often better)

```python
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
       colors=colors, explode=(0.1, 0, 0, 0))
ax.axis('equal')

# Donut
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       wedgeprops=dict(width=0.5), startangle=90)
```

## Polar and Radar Charts

**Use:** Cyclic data, directional data, multivariate comparisons

```python
# Radar chart
categories = ['A', 'B', 'C', 'D', 'E']
values = [4, 3, 5, 2, 4]
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
values_c = np.concatenate([values, [values[0]]])
angles_c = np.concatenate([angles, [angles[0]]])

ax = plt.subplot(111, projection='polar')
ax.plot(angles_c, values_c, 'o-', linewidth=2)
ax.fill(angles_c, values_c, alpha=0.25)
ax.set_xticks(angles)
ax.set_xticklabels(categories)
```

## Quiver and Stream Plots

**Use:** Vector fields, flow visualization

```python
ax.quiver(X, Y, U, V, alpha=0.8)
ax.streamplot(X, Y, U, V, density=1.5, color='k', linewidth=1)
```

## 3D Plots

**Use:** Three-dimensional data visualization

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
fig.colorbar(surf, ax=ax, shrink=0.5)

# Scatter
ax.scatter(x, y, z, c=z, cmap='viridis', s=50)

# Wireframe
ax.plot_wireframe(X, Y, Z, color='k', linewidth=0.5)

ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.view_init(elev=30, azim=45)
```

## Specialized Plots

### Stem Plot
```python
ax.stem(x, y, linefmt='C0-', markerfmt='C0o', basefmt='k-')
```

### Stairs Plot
```python
ax.stairs(values, edges, fill=True, alpha=0.5)
```

### Broken Barh (Gantt-style)
```python
ax.broken_barh([(10, 50), (100, 20)], (10, 9), facecolors='tab:blue')
ax.broken_barh([(10, 20), (50, 50)], (20, 9), facecolors='tab:orange')
ax.set_yticks([15, 25])
ax.set_yticklabels(['Task 1', 'Task 2'])
```

### Time Series with Shaded Regions
```python
ax.plot(dates, values, linewidth=2)
ax.axvspan(start_date, end_date, alpha=0.2, color='gray', label='Recession')
```

## Seaborn-Specific Plots

### KDE (univariate + bivariate)
```python
# Univariate
sns.kdeplot(data=df, x='value', hue='group', fill=True, common_norm=False)
# Bivariate
sns.kdeplot(data=df, x='x', y='y', fill=True, levels=10, thresh=0.05)
```

### ECDF
```python
sns.ecdfplot(data=df, x='value', hue='group')
```

### Pairplot
```python
sns.pairplot(df, hue='species', corner=True, diag_kind='kde')
```

### Jointplot
```python
g = sns.jointplot(data=df, x='x', y='y', kind='hex', height=8)
```

### Stripplot / Swarmplot
```python
sns.stripplot(data=df, x='group', y='value', jitter=0.2, alpha=0.5)
sns.swarmplot(data=df, x='group', y='value', size=4)  # Non-overlapping
```

### Pointplot (connected estimates)
```python
sns.pointplot(data=df, x='time', y='score', hue='treatment',
              markers=['o', 's'], linestyles=['-', '--'], dodge=0.3)
```

### Regression
```python
sns.regplot(data=df, x='x', y='y', order=2, ci=95)
sns.lmplot(data=df, x='x', y='y', hue='group', col='condition')
```

### Countplot
```python
sns.countplot(data=df, x='category', hue='type', stat='percent')
```

### Boxenplot (letter-value)
```python
sns.boxenplot(data=df, x='group', y='value', k_depth='tukey')
```

## Plot Selection Guide

| Data Type | Best Plot | Alternatives |
|-----------|-----------|-------------|
| 1 continuous | Histogram, KDE | Box, violin, ECDF |
| 2 continuous | Scatter | Hexbin, 2D hist, jointplot |
| Time series | Line | Area, step |
| Categorical vs continuous | Bar, box | Violin, strip, swarm, point |
| 2 categorical | Heatmap | Grouped bar |
| 3 continuous | 3D scatter, contour | Color-coded scatter |
| Proportions | Bar | Pie (sparingly) |
| Distribution comparison | Box, violin | Overlaid hist/KDE |
| Correlation matrix | Heatmap | Clustermap |
| Pairwise relationships | Pairplot | Scatter matrix |
| Vector field | Quiver, streamplot | - |
| Many groups time series | Faceted line | Small multiples |
