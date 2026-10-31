# Economics & Finance Plot Types

## Table of Contents
- [Coefficient Plots](#1-coefficient-plots)
- [Event Study Plots](#2-event-study-plots)
- [Binscatter Plots](#3-binscatter-plots)
- [RDD Plots](#4-rdd-plots)
- [Parallel Trends Plots](#5-parallel-trends-plots)
- [Fan Charts](#6-fan-charts)
- [IRF Plots](#7-impulse-response-function-plots)
- [Portfolio Sort Bar Charts](#8-portfolio-sort-bar-charts)
- [Fama-MacBeth Coefficient Time Series](#9-fama-macbeth-coefficient-time-series)
- [Kaplan-Meier Survival Curves](#10-kaplan-meier-survival-curves)

All examples produce publication-ready output with `pdf.fonttype: 42` for journal submission.

---

## 1. Coefficient Plots

Display regression coefficients with confidence intervals. Standard in applied micro.

### From statsmodels OLS
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Fit model
X = sm.add_constant(df[['x1', 'x2', 'x3', 'x4', 'x5']])
model = sm.OLS(df['y'], X).fit(cov_type='HC1')

# Extract coefficients (skip constant)
var_names = ['x1', 'x2', 'x3', 'x4', 'x5']
coefs = model.params[1:]
ci = model.conf_int(alpha=0.05).iloc[1:]
ci_low = ci[0].values
ci_high = ci[1].values

# Plot
fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
y_pos = np.arange(len(var_names))

ax.hlines(y_pos, ci_low, ci_high, color='#2c3e50', linewidth=1.5)
ax.scatter(coefs, y_pos, color='#2c3e50', s=60, zorder=5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)

ax.set_yticks(y_pos)
ax.set_yticklabels(var_names)
ax.set_xlabel('Coefficient Estimate')
ax.set_title('Regression Coefficients with 95% CI')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('coef_plot.pdf', dpi=300, bbox_inches='tight')
```

### From linearmodels (panel FE)
```python
from linearmodels.panel import PanelOLS

mod = PanelOLS(df['y'], df[['x1', 'x2', 'x3']], entity_effects=True)
res = mod.fit(cov_type='clustered', cluster_entity=True)

var_names = res.params.index.tolist()
coefs = res.params.values
se = res.std_errors.values

fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
y_pos = np.arange(len(var_names))

ax.errorbar(coefs, y_pos, xerr=1.96 * se, fmt='o', color='#2c3e50',
            capsize=4, capthick=1.5, markersize=6, linewidth=1.5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(var_names)
ax.set_xlabel('Coefficient')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Multi-specification Comparison
```python
fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
specs = {'Baseline': (coefs1, se1), 'Controls': (coefs2, se2), 'FE': (coefs3, se3)}
offsets = np.linspace(-0.2, 0.2, len(specs))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for i, (label, (c, s)) in enumerate(specs.items()):
    y_pos = np.arange(len(var_names)) + offsets[i]
    ax.errorbar(c, y_pos, xerr=1.96 * s, fmt='o', label=label,
                color=colors[i], capsize=3, markersize=5, linewidth=1.2)

ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
ax.set_yticks(np.arange(len(var_names)))
ax.set_yticklabels(var_names)
ax.legend(loc='lower right', frameon=False, fontsize=8)
```

---

## 2. Event Study Plots

Dynamic treatment effects with pre/post periods. Essential for DID designs.

```python
# event_time: relative period (-K, ..., -1, 0, 1, ..., L)
# coefs, se: arrays from event study regression (period -1 normalized to 0)

event_time = np.arange(-5, 8)  # -5 to +7
# Example: from regression with relative time dummies
# coefs[i], se[i] correspond to event_time[i]
# Period -1 is the reference (coef=0, se=0)

fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)

# Confidence bands
ci_upper = coefs + 1.96 * se
ci_lower = coefs - 1.96 * se
ax.fill_between(event_time, ci_lower, ci_upper, alpha=0.2, color='#1f77b4')

# Point estimates
ax.plot(event_time, coefs, 'o-', color='#1f77b4', linewidth=1.5,
        markersize=5, markerfacecolor='white', markeredgewidth=1.5)

# Reference lines
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.axvline(x=-0.5, color='red', linestyle=':', linewidth=0.8, alpha=0.7,
           label='Treatment onset')

# Labels
ax.set_xlabel('Event Time (Periods Relative to Treatment)')
ax.set_ylabel('Coefficient Estimate')
ax.set_title('Event Study: Dynamic Treatment Effects')
ax.legend(frameon=False, fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Pre-trends annotation
ax.annotate('Pre-trends', xy=(-3, coefs[2]), fontsize=8, color='gray',
            ha='center', va='bottom')

plt.savefig('event_study.pdf', dpi=300, bbox_inches='tight')
```

### With Multiple Treatment Groups
```python
fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)

for label, (c, s), color in zip(
    ['Group A', 'Group B'],
    [(coefs_a, se_a), (coefs_b, se_b)],
    ['#1f77b4', '#ff7f0e']
):
    ci_up = c + 1.96 * s
    ci_lo = c - 1.96 * s
    ax.fill_between(event_time, ci_lo, ci_up, alpha=0.15, color=color)
    ax.plot(event_time, c, 'o-', color=color, linewidth=1.5,
            markersize=4, label=label)

ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.axvline(x=-0.5, color='red', linestyle=':', linewidth=0.8)
ax.legend(frameon=False)
```

---

## 3. Binscatter Plots

Conditional means: bin x-variable, plot mean y within each bin. Optionally residualize.

### Basic Binscatter
```python
def binscatter(x, y, nbins=20, controls=None, ax=None):
    """Create a binscatter plot, optionally residualizing on controls."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)

    x_vals = np.array(x, dtype=float)
    y_vals = np.array(y, dtype=float)

    # Optionally residualize
    if controls is not None:
        X_ctrl = sm.add_constant(np.array(controls, dtype=float))
        x_vals = sm.OLS(x_vals, X_ctrl).fit().resid
        y_vals = sm.OLS(y_vals, X_ctrl).fit().resid

    # Bin x and compute means
    mask = np.isfinite(x_vals) & np.isfinite(y_vals)
    x_vals, y_vals = x_vals[mask], y_vals[mask]

    bin_edges = np.percentile(x_vals, np.linspace(0, 100, nbins + 1))
    bin_idx = np.digitize(x_vals, bin_edges[1:-1])

    x_means = np.array([x_vals[bin_idx == i].mean() for i in range(nbins)])
    y_means = np.array([y_vals[bin_idx == i].mean() for i in range(nbins)])

    # Plot
    ax.scatter(x_means, y_means, color='#2c3e50', s=50, zorder=5, edgecolors='white')

    # Fit line through bin means
    slope, intercept = np.polyfit(x_means, y_means, 1)
    x_line = np.linspace(x_means.min(), x_means.max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color='#e74c3c',
            linewidth=1.5, linestyle='--')

    ax.set_xlabel('X (binned)')
    ax.set_ylabel('Y (mean within bin)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return ax

# Usage
fig, ax = plt.subplots(figsize=(6, 4.5), constrained_layout=True)
binscatter(df['income'], df['consumption'], nbins=20, ax=ax)
ax.set_xlabel('Log Income')
ax.set_ylabel('Log Consumption')
ax.set_title('Binscatter: Income vs. Consumption')
plt.savefig('binscatter.pdf', dpi=300, bbox_inches='tight')
```

### With binsreg Package
```python
# pip install binsreg
from binsreg import binsreg

est = binsreg(df['y'], df['x'], nbins=20)
fig = est.bins_plot
fig.savefig('binsreg.pdf', dpi=300, bbox_inches='tight')
```

---

## 4. RDD Plots

Regression discontinuity design: show jump at cutoff with polynomial fits.

```python
def rdd_plot(running_var, outcome, cutoff=0, bandwidth=None, poly_order=1,
             nbins=20, ax=None):
    """RDD plot with polynomial fits on each side of the cutoff."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)

    x = np.array(running_var, dtype=float)
    y = np.array(outcome, dtype=float)

    if bandwidth is not None:
        mask = np.abs(x - cutoff) <= bandwidth
        x, y = x[mask], y[mask]

    left = x < cutoff
    right = x >= cutoff

    # Bin scatter
    for side, mask_s, color in [('left', left, '#1f77b4'), ('right', right, '#ff7f0e')]:
        x_s, y_s = x[mask_s], y[mask_s]
        if len(x_s) < nbins:
            ax.scatter(x_s, y_s, color=color, s=20, alpha=0.4)
            continue
        bin_edges = np.percentile(x_s, np.linspace(0, 100, nbins + 1))
        bin_idx = np.digitize(x_s, bin_edges[1:-1])
        x_means = [x_s[bin_idx == i].mean() for i in range(nbins) if (bin_idx == i).sum() > 0]
        y_means = [y_s[bin_idx == i].mean() for i in range(nbins) if (bin_idx == i).sum() > 0]
        ax.scatter(x_means, y_means, color=color, s=50, zorder=5, edgecolors='white')

    # Polynomial fits
    for mask_s, color in [(left, '#1f77b4'), (right, '#ff7f0e')]:
        x_s, y_s = x[mask_s], y[mask_s]
        if len(x_s) < poly_order + 1:
            continue
        coeffs = np.polyfit(x_s, y_s, poly_order)
        x_fit = np.linspace(x_s.min(), x_s.max(), 200)
        y_fit = np.polyval(coeffs, x_fit)
        ax.plot(x_fit, y_fit, color=color, linewidth=2)

    # Cutoff line
    ax.axvline(x=cutoff, color='red', linestyle='--', linewidth=1, alpha=0.7)

    ax.set_xlabel('Running Variable')
    ax.set_ylabel('Outcome')
    ax.set_title('Regression Discontinuity Design')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return ax

# Usage
fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
rdd_plot(df['score'], df['outcome'], cutoff=50, bandwidth=20, poly_order=2, ax=ax)
ax.set_xlabel('Test Score')
ax.set_ylabel('Enrollment Rate')
plt.savefig('rdd.pdf', dpi=300, bbox_inches='tight')
```

---

## 5. Parallel Trends Plots

DID pre-trends verification: treatment vs. control group trajectories before treatment.

```python
# df has columns: period, group ('Treatment'/'Control'), outcome
# Treatment starts at period 0

fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)

for label, color, marker in [('Treatment', '#e74c3c', 'o'), ('Control', '#2c3e50', 's')]:
    grp = df[df['group'] == label].groupby('period')['outcome']
    means = grp.mean()
    se = grp.sem()
    periods = means.index

    ax.plot(periods, means, marker=marker, color=color, linewidth=1.5,
            markersize=5, label=label)
    ax.fill_between(periods, means - 1.96 * se, means + 1.96 * se,
                    alpha=0.15, color=color)

# Treatment onset
ax.axvline(x=-0.5, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax.text(-0.3, ax.get_ylim()[1] * 0.95, 'Treatment', fontsize=8,
        color='gray', ha='left', va='top')

ax.set_xlabel('Period')
ax.set_ylabel('Outcome')
ax.set_title('Parallel Trends Check')
ax.legend(frameon=False, fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('parallel_trends.pdf', dpi=300, bbox_inches='tight')
```

### Normalized (Difference from Baseline)
```python
# Normalize both groups to period -1 = 0
baseline = df[df['period'] == -1].groupby('group')['outcome'].mean()
df['outcome_norm'] = df.apply(
    lambda r: r['outcome'] - baseline[r['group']], axis=1)
# Then plot as above using 'outcome_norm'
```

---

## 6. Fan Charts

Forecast uncertainty bands expanding over the horizon.

```python
# forecast: array of point forecasts at horizons 1..H
# sigmas: array of forecast standard errors at each horizon

horizons = np.arange(1, len(forecast) + 1)
percentiles = [10, 25, 75, 90]  # Symmetric fan

fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)

# Fan bands
alphas = [0.1, 0.2]
for i, (lo_p, hi_p) in enumerate([(10, 90), (25, 75)]):
    from scipy.stats import norm
    lo = forecast + norm.ppf(lo_p / 100) * sigmas
    hi = forecast + norm.ppf(hi_p / 100) * sigmas
    ax.fill_between(horizons, lo, hi, color='#1f77b4', alpha=alphas[i],
                    label=f'{hi_p - lo_p}% CI' if i == 0 else f'{hi_p - lo_p}% CI')

# Point forecast
ax.plot(horizons, forecast, 'o-', color='#1f77b4', linewidth=2,
        markersize=5, label='Point forecast', zorder=5)

# Historical data
ax.plot(np.arange(-4, 1), historical[-5:], 'k-', linewidth=1.5, label='Actual')
ax.axvline(x=0.5, color='gray', linestyle=':', linewidth=0.8)

ax.set_xlabel('Forecast Horizon (quarters)')
ax.set_ylabel('GDP Growth (%)')
ax.set_title('GDP Growth Fan Chart')
ax.legend(frameon=False, fontsize=8, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('fan_chart.pdf', dpi=300, bbox_inches='tight')
```

---

## 7. Impulse Response Function Plots

From VAR models or local projections.

### From statsmodels VAR
```python
from statsmodels.tsa.api import VAR

model = VAR(df[['gdp', 'inflation', 'rate']]).fit(maxlags=4)
irf = model.irf(periods=20)

# Built-in plot
irf.plot(orth=True)
plt.tight_layout()
plt.savefig('irf_auto.pdf', dpi=300, bbox_inches='tight')
```

### Custom IRF Plot
```python
def plot_irf(irf_point, irf_lower, irf_upper, shock_name, response_name,
             horizons=None, ax=None):
    """Plot a single impulse response function with confidence bands."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    if horizons is None:
        horizons = np.arange(len(irf_point))

    ax.fill_between(horizons, irf_lower, irf_upper, alpha=0.2, color='#1f77b4')
    ax.plot(horizons, irf_point, '-', color='#1f77b4', linewidth=2)
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)

    ax.set_xlabel('Horizon')
    ax.set_ylabel('Response')
    ax.set_title(f'Response of {response_name} to {shock_name} Shock')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return ax

# Multi-panel IRF (e.g., 3 variables responding to 1 shock)
fig, axes = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)
variables = ['GDP', 'Inflation', 'Interest Rate']
for i, (var, ax) in enumerate(zip(variables, axes)):
    irfs = irf.irfs[:, 0, i]      # shock=0, response=i
    lower = irf.ci[:, 0, i, 0]    # lower bound
    upper = irf.ci[:, 0, i, 1]    # upper bound
    plot_irf(irfs, lower, upper, 'Monetary Policy', var, ax=ax)

plt.savefig('irf_panel.pdf', dpi=300, bbox_inches='tight')
```

### Local Projections IRF
```python
# horizons: 0..H
# For each h, regress y_{t+h} on shock_t + controls
# Store coefficients and SEs

fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
H = len(lp_coefs)
horizons = np.arange(H)
ci_up = lp_coefs + 1.96 * lp_se
ci_lo = lp_coefs - 1.96 * lp_se

ax.fill_between(horizons, ci_lo, ci_up, alpha=0.2, color='#1f77b4')
ax.plot(horizons, lp_coefs, 'o-', color='#1f77b4', linewidth=1.5, markersize=4)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.set_xlabel('Horizon (months)')
ax.set_ylabel('Response')
ax.set_title('Local Projection: Response to Shock')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

---

## 8. Portfolio Sort Bar Charts

Quintile or decile returns from cross-sectional asset pricing tests.

```python
# portfolios: sorted quintile/decile labels
# returns: mean excess returns for each portfolio
# se: standard errors

portfolios = [f'Q{i}' for i in range(1, 6)] + ['Q5-Q1']
returns = np.array([0.3, 0.5, 0.7, 0.9, 1.4, 1.1])
se = np.array([0.15, 0.12, 0.13, 0.14, 0.16, 0.22])
t_stats = returns / se

fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)

colors = ['#1f77b4'] * 5 + ['#e74c3c']  # Highlight long-short
bars = ax.bar(portfolios, returns, yerr=1.96 * se, capsize=4,
              color=colors, edgecolor='black', linewidth=0.8, alpha=0.85)

# Add t-stat annotations
for bar, t in zip(bars, t_stats):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
            f't={t:.2f}', ha='center', va='bottom', fontsize=7, color='gray')

ax.axhline(y=0, color='gray', linewidth=0.8)
ax.set_xlabel('Portfolio (sorted by characteristic)')
ax.set_ylabel('Mean Monthly Excess Return (%)')
ax.set_title('Portfolio Sort: Quintile Returns')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('portfolio_sort.pdf', dpi=300, bbox_inches='tight')
```

### Decile Version with Monotonicity Line
```python
deciles = [f'D{i}' for i in range(1, 11)]
ret = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 0.95, 1.1, 1.4])

fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
ax.bar(deciles, ret, color='#2c3e50', edgecolor='black', linewidth=0.5)
ax.plot(deciles, ret, 'o-', color='#e74c3c', linewidth=1.5, markersize=4, zorder=5)
ax.set_ylabel('Mean Excess Return (%)')
ax.set_xlabel('Decile')
```

---

## 9. Fama-MacBeth Coefficient Time Series

Show how cross-sectional regression coefficients evolve over time.

```python
# dates: array of dates
# gamma_t: time series of cross-sectional slope coefficients
# se_t: time series of standard errors

fig, axes = plt.subplots(2, 1, figsize=(8, 6), constrained_layout=True,
                          gridspec_kw={'height_ratios': [3, 1]})

# Top: coefficient time series with rolling mean
ax = axes[0]
ax.plot(dates, gamma_t, color='#1f77b4', linewidth=0.5, alpha=0.6, label='Monthly γ')

# Rolling mean (12-month)
rolling_mean = pd.Series(gamma_t, index=dates).rolling(12, min_periods=6).mean()
ax.plot(dates, rolling_mean, color='#e74c3c', linewidth=2, label='12-month MA')

ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.axhline(y=np.mean(gamma_t), color='green', linestyle=':', linewidth=1,
           label=f'Mean = {np.mean(gamma_t):.3f}')

ax.set_ylabel('Risk Premium (γ)')
ax.set_title('Fama-MacBeth: Cross-Sectional Price of Risk')
ax.legend(frameon=False, fontsize=8, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Bottom: t-statistics over time
ax2 = axes[1]
t_rolling = rolling_mean / pd.Series(se_t, index=dates).rolling(12, min_periods=6).mean()
ax2.fill_between(dates, t_rolling, 0, where=(t_rolling > 0), color='#2ca02c', alpha=0.3)
ax2.fill_between(dates, t_rolling, 0, where=(t_rolling <= 0), color='#d62728', alpha=0.3)
ax2.axhline(y=1.96, color='gray', linestyle=':', linewidth=0.5)
ax2.axhline(y=-1.96, color='gray', linestyle=':', linewidth=0.5)
ax2.set_ylabel('t-stat')
ax2.set_xlabel('Date')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.savefig('fama_macbeth.pdf', dpi=300, bbox_inches='tight')
```

---

## 10. Kaplan-Meier Survival Curves

Survival analysis for duration models (e.g., firm survival, loan default).

### Using lifelines
```python
from lifelines import KaplanMeierFitter

fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)

groups = df['group'].unique()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for group, color in zip(groups, colors):
    mask = df['group'] == group
    kmf = KaplanMeierFitter()
    kmf.fit(df.loc[mask, 'duration'], event_observed=df.loc[mask, 'event'],
            label=group)
    kmf.plot_survival_function(ax=ax, ci_show=True, color=color)

ax.set_xlabel('Time (months)')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Survival Curves')
ax.legend(frameon=False, fontsize=9)
ax.set_ylim(0, 1.05)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('kaplan_meier.pdf', dpi=300, bbox_inches='tight')
```

### Manual Kaplan-Meier (no lifelines dependency)
```python
def kaplan_meier(durations, events):
    """Compute KM survival curve from durations and event indicators."""
    df_km = pd.DataFrame({'t': durations, 'e': events}).sort_values('t')
    times = df_km['t'].unique()
    n_at_risk = len(df_km)
    surv = 1.0
    km_times, km_surv = [0], [1.0]

    for t in times:
        at_t = df_km[df_km['t'] == t]
        d = at_t['e'].sum()
        surv *= (1 - d / n_at_risk)
        km_times.append(t)
        km_surv.append(surv)
        n_at_risk -= len(at_t)

    return np.array(km_times), np.array(km_surv)

fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
for group, color in zip(['A', 'B'], ['#1f77b4', '#ff7f0e']):
    mask = df['group'] == group
    t, s = kaplan_meier(df.loc[mask, 'duration'], df.loc[mask, 'event'])
    ax.step(t, s, where='post', color=color, linewidth=2, label=group)

ax.set_xlabel('Time')
ax.set_ylabel('Survival Probability')
ax.set_ylim(0, 1.05)
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

---

## Common Configuration for All Economics Plots

Apply these settings before any economics figure:

```python
plt.rcParams.update({
    'figure.figsize': (6.5, 4.5),
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.6,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'legend.fontsize': 8,
    'legend.frameon': False,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})
```
