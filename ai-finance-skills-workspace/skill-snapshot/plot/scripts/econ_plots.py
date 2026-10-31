#!/usr/bin/env python3
"""
Economics and Finance Plot Helper Functions

Production-quality plotting functions for common academic economics visualizations.
Each function takes data + config, returns (fig, ax).

Usage:
    from econ_plots import coefficient_plot, event_study_plot, binscatter
    fig, ax = coefficient_plot(results, var_names=['x1', 'x2', 'x3'])
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Default style for economics figures
# ---------------------------------------------------------------------------





def _get_ax(ax, figsize=None):
    """Return existing ax or create new figure+ax. Track if we created it."""
    created = ax is None
    if created:
        fig, ax = plt.subplots(
            figsize=figsize or (6.5, 4.5), constrained_layout=True
        )
    else:
        fig = ax.get_figure()
    return fig, ax, created


# ---------------------------------------------------------------------------
# 1. Coefficient Plot
# ---------------------------------------------------------------------------

def coefficient_plot(coefs, se=None, ci_low=None, ci_high=None,
                     var_names=None, alpha=0.05, horizontal=True,
                     title='Coefficient Estimates', xlabel='Coefficient',
                     color='#2c3e50', ax=None):
    """Plot regression coefficients with confidence intervals.

    Parameters
    ----------
    coefs : array-like or statsmodels result object
        Coefficient estimates. If a statsmodels result, extracts params/CI.
    se : array-like, optional
        Standard errors (used if ci_low/ci_high not provided).
    ci_low, ci_high : array-like, optional
        Pre-computed confidence interval bounds.
    var_names : list of str, optional
        Variable names for labels.
    alpha : float
        Significance level for CI (default 0.05 = 95% CI).
    horizontal : bool
        If True, horizontal plot (variables on y-axis).
    title, xlabel : str
        Plot labels.
    color : str
        Color for points and lines.
    ax : matplotlib Axes, optional

    Returns
    -------
    fig, ax
    """
    # Handle statsmodels result objects
    if hasattr(coefs, 'params') and hasattr(coefs, 'conf_int'):
        result = coefs
        ci_df = result.conf_int(alpha=alpha)
        coefs_arr = result.params.values
        ci_low = ci_df.iloc[:, 0].values
        ci_high = ci_df.iloc[:, 1].values
        if var_names is None:
            var_names = result.params.index.tolist()
        # Skip constant if present
        if var_names[0] in ('const', 'Intercept'):
            coefs_arr = coefs_arr[1:]
            ci_low = ci_low[1:]
            ci_high = ci_high[1:]
            var_names = var_names[1:]
        coefs = coefs_arr

    coefs = np.asarray(coefs, dtype=float)
    n = len(coefs)

    if ci_low is None or ci_high is None:
        if se is not None:
            from scipy.stats import norm as sp_norm
            z = sp_norm.ppf(1 - alpha / 2)
            se = np.asarray(se, dtype=float)
            ci_low = coefs - z * se
            ci_high = coefs + z * se
        else:
            raise ValueError("Provide se or (ci_low, ci_high) or a statsmodels result.")

    if var_names is None:
        var_names = [f'x{i+1}' for i in range(n)]

    fig, ax, _ = _get_ax(ax)
    positions = np.arange(n)

    if horizontal:
        ax.hlines(positions, ci_low, ci_high, color=color, linewidth=1.5)
        ax.scatter(coefs, positions, color=color, s=50, zorder=5)
        ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
        ax.set_yticks(positions)
        ax.set_yticklabels(var_names)
        ax.set_xlabel(xlabel)
    else:
        ax.vlines(positions, ci_low, ci_high, color=color, linewidth=1.5)
        ax.scatter(positions, coefs, color=color, s=50, zorder=5)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
        ax.set_xticks(positions)
        ax.set_xticklabels(var_names, rotation=45, ha='right')
        ax.set_ylabel(xlabel)

    ax.set_title(title)
    return fig, ax


# ---------------------------------------------------------------------------
# 2. Event Study Plot
# ---------------------------------------------------------------------------

def event_study_plot(event_time, coefs, se, ref_period=-1,
                     title='Event Study', xlabel='Event Time',
                     ylabel='Coefficient', color='#1f77b4', ax=None):
    """Plot dynamic treatment effects (event study).

    Parameters
    ----------
    event_time : array-like
        Relative time periods (e.g., -5, -4, ..., 0, 1, ..., 7).
    coefs : array-like
        Point estimates for each period.
    se : array-like
        Standard errors for each period.
    ref_period : int
        Reference period (set to 0 in plot). Default -1.
    title, xlabel, ylabel : str
    color : str
    ax : matplotlib Axes, optional

    Returns
    -------
    fig, ax
    """
    event_time = np.asarray(event_time)
    coefs = np.asarray(coefs, dtype=float)
    se = np.asarray(se, dtype=float)

    fig, ax, _ = _get_ax(ax, figsize=(7, 4.5))

    ci_upper = coefs + 1.96 * se
    ci_lower = coefs - 1.96 * se

    ax.fill_between(event_time, ci_lower, ci_upper, alpha=0.2, color=color)
    ax.plot(event_time, coefs, 'o-', color=color, linewidth=1.5,
            markersize=5, markerfacecolor='white', markeredgewidth=1.5)

    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax.axvline(x=ref_period + 0.5, color='red', linestyle=':', linewidth=0.8,
               alpha=0.7)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return fig, ax


# ---------------------------------------------------------------------------
# 3. Binscatter
# ---------------------------------------------------------------------------

def binscatter(x, y, nbins=20, controls=None, fit_line=True,
               title='Binscatter', xlabel='X', ylabel='Y',
               color='#2c3e50', ax=None):
    """Create a binscatter plot, optionally residualizing on controls.

    Parameters
    ----------
    x, y : array-like
        Variables to plot.
    nbins : int
        Number of equal-frequency bins.
    controls : array-like or DataFrame, optional
        Control variables to partial out.
    fit_line : bool
        Add OLS fit line through bin means.
    title, xlabel, ylabel : str
    color : str
    ax : matplotlib Axes, optional

    Returns
    -------
    fig, ax
    """
    import statsmodels.api as sm

    x_vals = np.asarray(x, dtype=float)
    y_vals = np.asarray(y, dtype=float)

    # Residualize if controls provided
    if controls is not None:
        X_ctrl = sm.add_constant(np.asarray(controls, dtype=float))
        x_vals = sm.OLS(x_vals, X_ctrl, missing='drop').fit().resid
        y_vals = sm.OLS(y_vals, X_ctrl, missing='drop').fit().resid

    # Remove NaN/inf
    mask = np.isfinite(x_vals) & np.isfinite(y_vals)
    x_vals, y_vals = x_vals[mask], y_vals[mask]

    # Compute bin means
    bin_edges = np.percentile(x_vals, np.linspace(0, 100, nbins + 1))
    bin_idx = np.digitize(x_vals, bin_edges[1:-1])

    x_means, y_means = [], []
    for i in range(nbins):
        m = bin_idx == i
        if m.sum() > 0:
            x_means.append(x_vals[m].mean())
            y_means.append(y_vals[m].mean())
    x_means = np.array(x_means)
    y_means = np.array(y_means)

    fig, ax, _ = _get_ax(ax)

    ax.scatter(x_means, y_means, color=color, s=50, zorder=5, edgecolors='white')

    if fit_line and len(x_means) > 1:
        slope, intercept = np.polyfit(x_means, y_means, 1)
        x_line = np.linspace(x_means.min(), x_means.max(), 100)
        ax.plot(x_line, slope * x_line + intercept, color='#e74c3c',
                linewidth=1.5, linestyle='--')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return fig, ax


# ---------------------------------------------------------------------------
# 4. RDD Plot
# ---------------------------------------------------------------------------

def rdd_plot(running_var, outcome, cutoff=0, bandwidth=None, poly_order=1,
             nbins=20, title='Regression Discontinuity', xlabel='Running Variable',
             ylabel='Outcome', ax=None):
    """RDD plot with polynomial fits on each side of the cutoff.

    Parameters
    ----------
    running_var, outcome : array-like
    cutoff : float
        Discontinuity threshold.
    bandwidth : float, optional
        If given, restrict to |running_var - cutoff| <= bandwidth.
    poly_order : int
        Degree of polynomial fit on each side.
    nbins : int
        Number of bins per side for scatter.
    title, xlabel, ylabel : str
    ax : matplotlib Axes, optional

    Returns
    -------
    fig, ax
    """
    x = np.asarray(running_var, dtype=float)
    y = np.asarray(outcome, dtype=float)

    if bandwidth is not None:
        mask = np.abs(x - cutoff) <= bandwidth
        x, y = x[mask], y[mask]

    fig, ax, _ = _get_ax(ax, figsize=(7, 5))

    for side_mask, color in [(x < cutoff, '#1f77b4'), (x >= cutoff, '#ff7f0e')]:
        xs, ys = x[side_mask], y[side_mask]
        if len(xs) == 0:
            continue

        # Bin scatter
        if len(xs) >= nbins:
            edges = np.percentile(xs, np.linspace(0, 100, nbins + 1))
            bidx = np.digitize(xs, edges[1:-1])
            xm = [xs[bidx == i].mean() for i in range(nbins) if (bidx == i).sum() > 0]
            ym = [ys[bidx == i].mean() for i in range(nbins) if (bidx == i).sum() > 0]
            ax.scatter(xm, ym, color=color, s=50, zorder=5, edgecolors='white')
        else:
            ax.scatter(xs, ys, color=color, s=20, alpha=0.4)

        # Polynomial fit
        if len(xs) > poly_order:
            coeffs = np.polyfit(xs, ys, poly_order)
            xf = np.linspace(xs.min(), xs.max(), 200)
            ax.plot(xf, np.polyval(coeffs, xf), color=color, linewidth=2)

    ax.axvline(x=cutoff, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return fig, ax


# ---------------------------------------------------------------------------
# 5. Parallel Trends Plot
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# 6. Fan Chart
# ---------------------------------------------------------------------------

def fan_chart(horizons, forecast, sigmas, historical_dates=None,
              historical_values=None, bands=(90, 50),
              title='Forecast Fan Chart', xlabel='Horizon', ylabel='Value',
              ax=None):
    """Fan chart for forecast uncertainty.

    Parameters
    ----------
    horizons : array-like
        Forecast horizons.
    forecast : array-like
        Point forecasts.
    sigmas : array-like
        Forecast standard errors.
    historical_dates, historical_values : array-like, optional
        Historical actuals to show before the forecast.
    bands : tuple of int
        CI widths in percent (e.g., (90, 50) draws 90% and 50% bands).
    title, xlabel, ylabel : str
    ax : matplotlib Axes, optional

    Returns
    -------
    fig, ax
    """
    from scipy.stats import norm as sp_norm

    horizons = np.asarray(horizons)
    forecast = np.asarray(forecast, dtype=float)
    sigmas = np.asarray(sigmas, dtype=float)

    fig, ax, _ = _get_ax(ax, figsize=(8, 5))

    alphas = np.linspace(0.1, 0.25, len(bands))
    for band_pct, alpha_val in zip(sorted(bands, reverse=True), alphas):
        lo_q = (100 - band_pct) / 200
        hi_q = 1 - lo_q
        lo = forecast + sp_norm.ppf(lo_q) * sigmas
        hi = forecast + sp_norm.ppf(hi_q) * sigmas
        ax.fill_between(horizons, lo, hi, color='#1f77b4', alpha=alpha_val,
                        label=f'{band_pct}% CI')

    ax.plot(horizons, forecast, 'o-', color='#1f77b4', linewidth=2,
            markersize=4, label='Forecast', zorder=5)

    if historical_dates is not None and historical_values is not None:
        ax.plot(historical_dates, historical_values, 'k-', linewidth=1.5,
                label='Actual')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(frameon=False, fontsize=8)
    return fig, ax


# ---------------------------------------------------------------------------
# 7. IRF Plot
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# 8. Portfolio Sort Bar Chart
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# 9. Fama-MacBeth Coefficient Time Series
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# 10. Kaplan-Meier Survival Curve
# ---------------------------------------------------------------------------


