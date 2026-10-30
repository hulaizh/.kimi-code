# Matplotlib Core Reference

## Table of Contents
- [Core Classes](#core-classes)
  - [Figure](#figure)
  - [Axes](#axes)
  - [pyplot Module](#pyplot-module)
- [Line and Marker Styles](#line-and-marker-styles)
- [Color Specifications](#color-specifications)
- [Common Parameters](#common-parameters)
- [rcParams Configuration](#rcparams-configuration)
- [GridSpec for Complex Layouts](#gridspec-for-complex-layouts)
- [Subplot Mosaic](#subplot-mosaic)
- [Twin Axes and Shared Axes](#twin-axes-and-shared-axes)
- [3D Plotting](#3d-plotting)
- [Animation](#animation)
- [Image Operations](#image-operations)
- [Date Formatting](#date-formatting)
- [Event Handling](#event-handling)
- [Useful Utilities](#useful-utilities)

## Core Classes

### Figure

The top-level container for all plot elements.

**Creation:**
```python
fig = plt.figure(figsize=(10, 6), dpi=100, facecolor='white')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
fig, axes = plt.subplots(2, 2, figsize=(12, 10), constrained_layout=True)
```

**Key Methods:**
- `fig.add_subplot(nrows, ncols, index)` - Add a subplot
- `fig.add_axes([left, bottom, width, height])` - Add axes at specific position
- `fig.savefig(filename, dpi=300, bbox_inches='tight')` - Save figure
- `fig.tight_layout()` - Adjust spacing to prevent overlaps
- `fig.suptitle(title)` - Set figure title
- `fig.legend()` - Create figure-level legend
- `fig.colorbar(mappable)` - Add colorbar to figure
- `plt.close(fig)` - Close figure to free memory

**Key Attributes:**
- `fig.axes` - List of all axes in the figure
- `fig.dpi` - Resolution in dots per inch

### Axes

The actual plotting area where data is visualized.

**Plotting Methods:**

| Category | Method | Use |
|----------|--------|-----|
| Lines | `ax.plot(x, y)` | Line plot |
| Lines | `ax.step(x, y, where='mid')` | Step plot |
| Lines | `ax.errorbar(x, y, yerr, xerr)` | Error bars |
| Scatter | `ax.scatter(x, y, s, c)` | Scatter plot |
| Bars | `ax.bar(x, height)` | Vertical bars |
| Bars | `ax.barh(y, width)` | Horizontal bars |
| Stats | `ax.hist(data, bins=30)` | Histogram |
| Stats | `ax.boxplot(data)` | Box plot |
| Stats | `ax.violinplot(data)` | Violin plot |
| 2D | `ax.imshow(array, cmap)` | Image/matrix |
| 2D | `ax.contour(X, Y, Z)` | Contour lines |
| 2D | `ax.contourf(X, Y, Z)` | Filled contours |
| 2D | `ax.pcolormesh(X, Y, Z)` | Pseudocolor mesh |
| Fill | `ax.fill_between(x, y1, y2)` | Fill between curves |
| Fill | `ax.fill_betweenx(y, x1, x2)` | Fill between vertical |
| Text | `ax.text(x, y, text)` | Add text |
| Text | `ax.annotate(text, xy, xytext)` | Annotate with arrow |

**Customization Methods:**

```python
# Labels and titles
ax.set_xlabel(label, fontsize=12)
ax.set_ylabel(label, fontsize=12)
ax.set_title(title, fontsize=14)

# Limits and scales
ax.set_xlim(left, right)
ax.set_ylim(bottom, top)
ax.set_xscale('log')       # 'linear', 'log', 'symlog'
ax.set_yscale('log')

# Ticks
ax.set_xticks(positions)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.tick_params(axis='both', labelsize=10, direction='in')

# Grid and spines
ax.grid(True, alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend
ax.legend(loc='best', fontsize=10, frameon=True)

# Aspect
ax.set_aspect('equal')
```

### pyplot Module

High-level interface for quick plotting (state-machine style).

```python
plt.figure()              # Create new figure
plt.subplots()            # Create figure + axes
plt.show()                # Display figure
plt.savefig()             # Save figure
plt.close()               # Close figure
plt.style.use(name)       # Apply style sheet
plt.gca()                 # Get current axes
plt.gcf()                 # Get current figure
plt.clf()                 # Clear current figure
plt.cla()                 # Clear current axes
```

**Recommendation:** Use the OO interface (`fig, ax = plt.subplots()`) for all production code. Reserve pyplot for quick interactive exploration.

## Line and Marker Styles

**Line styles:** `'-'` solid, `'--'` dashed, `'-.'` dash-dot, `':'` dotted, `''` none

**Markers:** `'.'` point, `'o'` circle, `'v'^<>'` triangles, `'s'` square, `'p'` pentagon, `'*'` star, `'+'` plus, `'x'` cross, `'D'` diamond

**Format strings:** Combine color + marker + line: `'ro-'` = red circles with solid line, `'b--'` = blue dashed.

## Color Specifications

- **Single char:** `'b'` blue, `'r'` red, `'g'` green, `'k'` black, `'w'` white
- **Named:** `'steelblue'`, `'coral'`, `'teal'`, `'goldenrod'`
- **Hex:** `'#FF5733'`
- **RGB tuple:** `(0.1, 0.2, 0.3)`
- **RGBA tuple:** `(0.1, 0.2, 0.3, 0.5)`

## Common Parameters

### ax.plot()
```python
ax.plot(x, y,
    color='blue',           linewidth=2,
    linestyle='--',         marker='o',
    markersize=8,           markerfacecolor='red',
    markeredgecolor='black', markeredgewidth=1,
    alpha=0.7,              label='data',
    zorder=2,               rasterized=True,
)
```

### ax.scatter()
```python
ax.scatter(x, y,
    s=50,                   c='blue',
    marker='o',             cmap='viridis',
    alpha=0.5,              edgecolors='black',
    linewidths=1,           vmin=0, vmax=1,
    label='data',
)
```

### ax.text()
```python
ax.text(x, y, text,
    fontsize=12,            fontweight='bold',
    fontstyle='italic',     color='black',
    ha='center',            va='center',
    rotation=0,
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'),
)
```

### ax.annotate()
```python
ax.annotate('label', xy=(x, y), xytext=(x+1, y+1),
    fontsize=10,
    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
    bbox=dict(facecolor='yellow', alpha=0.8),
)
```

## rcParams Configuration

```python
plt.rcParams.update({
    # Figure
    'figure.figsize': (10, 6),
    'figure.dpi': 100,
    'figure.facecolor': 'white',
    'figure.constrained_layout.use': True,

    # Font
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 12,

    # Axes
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'axes.linewidth': 1.5,
    'axes.grid': True,
    'axes.grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,

    # Lines
    'lines.linewidth': 2,
    'lines.markersize': 8,

    # Ticks
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,

    # Legend
    'legend.fontsize': 12,
    'legend.frameon': True,
    'legend.framealpha': 0.8,

    # Grid
    'grid.alpha': 0.3,
    'grid.linestyle': '--',

    # Save
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})
```

**Temporary overrides:**
```python
with plt.rc_context({'font.size': 14, 'lines.linewidth': 2.5}):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```

## GridSpec for Complex Layouts

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])      # Top row, all columns
ax2 = fig.add_subplot(gs[1:, 0])     # Bottom two rows, first column
ax3 = fig.add_subplot(gs[1, 1:])     # Middle row, last two columns
ax4 = fig.add_subplot(gs[2, 1])      # Bottom row, middle column
ax5 = fig.add_subplot(gs[2, 2])      # Bottom row, right column
```

## Subplot Mosaic

```python
fig, axes = plt.subplot_mosaic(
    [['left', 'right_top'],
     ['left', 'right_bottom']],
    figsize=(10, 8),
    constrained_layout=True
)
axes['left'].plot(x, y)
axes['right_top'].scatter(x, y)
axes['right_bottom'].hist(data)
```

## Twin Axes and Shared Axes

```python
# Twin axes (two y-axes)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(x, y1, 'b-', label='left')
ax2.plot(x, y2, 'r-', label='right')
ax1.set_ylabel('Left Y', color='b')
ax2.set_ylabel('Right Y', color='r')

# Shared axes
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
```

## 3D Plotting

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot types
ax.plot(x, y, z)                    # 3D line
ax.scatter(x, y, z, c=z, cmap='viridis')  # 3D scatter
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')  # Surface
ax.plot_wireframe(X, Y, Z, color='black', linewidth=0.5)    # Wireframe
ax.contour(X, Y, Z, levels=15)     # 3D contour
ax.bar3d(x, y, z, dx, dy, dz)      # 3D bars

# Customization
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.view_init(elev=30, azim=45)
```

## Animation

```python
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1, 1)

def update(frame):
    x = np.linspace(0, 2*np.pi, 100)
    line.set_data(x, np.sin(x + frame/10))
    return line,

anim = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
anim.save('animation.gif', writer='pillow', fps=20)
```

## Image Operations

```python
# Read and display
img = plt.imread('image.png')
ax.imshow(img)

# Matrix as image
im = ax.imshow(matrix, cmap='viridis', aspect='auto',
               interpolation='nearest', origin='lower',
               extent=[x_min, x_max, y_min, y_max])

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Values')

# Colorbar with separate axes (for consistent subplot sizes)
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
```

## Date Formatting

```python
import matplotlib.dates as mdates

ax.plot(dates, values)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
plt.xticks(rotation=45, ha='right')

# Scientific notation
ax.ticklabel_format(style='scientific', axis='y', scilimits=(0, 0))
```

## Event Handling

```python
def on_click(event):
    if event.inaxes:
        print(f'Clicked at x={event.xdata:.2f}, y={event.ydata:.2f}')

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', lambda e: print(f'Key: {e.key}'))
```

## Useful Utilities

```python
# Axis limits
xlims = ax.get_xlim()
ylims = ax.get_ylim()

# Remove tick labels
ax.set_xticklabels([])

# Horizontal/vertical lines
ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)

# Shaded regions
ax.axvspan(x_start, x_end, alpha=0.2, color='gray')
ax.axhspan(y_start, y_end, alpha=0.2, color='gray')

# Legend outside plot
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Custom legend entries
from matplotlib.lines import Line2D
handles = [Line2D([0], [0], color='r', lw=2),
           Line2D([0], [0], color='b', lw=2, ls='--')]
ax.legend(handles, ['Label 1', 'Label 2'])

# Inset axes
axins = ax.inset_axes([0.6, 0.6, 0.35, 0.35])  # [x, y, width, height]
axins.plot(x, y)
```
