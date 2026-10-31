# Common Issues and Solutions

## Table of Contents
- [Display and Backend Issues](#display-and-backend-issues)
- [Layout and Spacing Issues](#layout-and-spacing-issues)
- [Memory and Performance Issues](#memory-and-performance-issues)
- [Font and Text Issues](#font-and-text-issues)
- [Color and Colormap Issues](#color-and-colormap-issues)
- [Axis and Scale Issues](#axis-and-scale-issues)
- [Legend Issues](#legend-issues)
- [Saving and Export Issues](#saving-and-export-issues)
- [3D Plot Issues](#3d-plot-issues)
- [Seaborn-Specific Issues](#seaborn-specific-issues)
- [Common Errors](#common-errors)
- [Best Practices Checklist](#best-practices-checklist)

## Display and Backend Issues

### Plots Not Showing
```python
# Check backend
import matplotlib
print(matplotlib.get_backend())

# Try different backend
matplotlib.use('TkAgg')  # or 'Qt5Agg', 'MacOSX'

# Jupyter
%matplotlib inline     # Static
%matplotlib widget     # Interactive

# Ensure plt.show() is called
plt.show()
```

### "RuntimeError: main thread is not in main loop"
```python
matplotlib.use('Agg')  # Non-interactive backend
plt.ioff()              # Turn off interactive mode
```

### Figures Not Updating Interactively
```python
plt.ion()
plt.draw()
plt.pause(0.001)
```

## Layout and Spacing Issues

### Overlapping Labels and Titles
```python
# Best: constrained_layout
fig, ax = plt.subplots(constrained_layout=True)

# Alternative: tight_layout
plt.tight_layout()

# Manual margins
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# Save with tight bbox
plt.savefig('fig.png', bbox_inches='tight')

# Rotate long tick labels
ax.set_xticklabels(labels, rotation=45, ha='right')
```

### Colorbar Affects Subplot Size
```python
# Best: constrained_layout
fig, ax = plt.subplots(constrained_layout=True)
im = ax.imshow(data)
plt.colorbar(im, ax=ax)

# Manual: separate axes for colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

# Shared colorbar across subplots
fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.95)
```

### Subplots Too Close Together
```python
fig, axes = plt.subplots(2, 2, constrained_layout=True)
# or
plt.subplots_adjust(hspace=0.4, wspace=0.4)
# or
plt.tight_layout(h_pad=2.0, w_pad=2.0)
```

## Memory and Performance Issues

### Memory Leak with Many Figures
```python
# Always close after saving
fig, ax = plt.subplots()
ax.plot(x, y)
plt.savefig('plot.png')
plt.close(fig)         # Close specific figure
# or
plt.close('all')       # Close all figures
```

### Large File Sizes
```python
# Reduce DPI
plt.savefig('fig.png', dpi=150)

# Rasterize complex elements
ax.plot(x, y, rasterized=True)

# Vector format for simple plots
plt.savefig('fig.pdf')
```

### Slow Plotting with Large Datasets
```python
# Downsample
from scipy.signal import decimate
y_down = decimate(y, 10)

# Rasterize
ax.scatter(x, y, rasterized=True)

# Use hexbin instead of scatter
ax.hexbin(x, y, gridsize=50, cmap='viridis')
```

## Font and Text Issues

### Font Not Found Warning
```python
# List available fonts
from matplotlib.font_manager import findfont, FontProperties
print(findfont(FontProperties(family='sans-serif')))

# Rebuild font cache
import matplotlib.font_manager
matplotlib.font_manager._rebuild()

# Specify fallbacks
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'sans-serif']
```

### LaTeX Rendering Errors
```python
# Use raw strings
ax.set_xlabel(r'$\alpha$')  # Correct
ax.set_xlabel('$\\alpha$')   # Also works

# Disable usetex if LaTeX not installed
plt.rcParams['text.usetex'] = False

# Mathtext (always available, no LaTeX install needed)
ax.text(x, y, r'$\int_0^\infty e^{-x} dx$')
```

### Text Cut Off
```python
plt.savefig('fig.png', bbox_inches='tight')
plt.subplots_adjust(left=0.15, right=0.85)
fig, ax = plt.subplots(constrained_layout=True)
```

### PDF Fonts Not Embedded
```python
# For readable PDF export
plt.rcParams['pdf.fonttype'] = 42   # TrueType
plt.rcParams['ps.fonttype'] = 42
```

## Color and Colormap Issues

### Colorbar Range Mismatch
```python
# Set explicit limits
im = ax.imshow(data, vmin=0, vmax=1, cmap='viridis')

# Shared norm across subplots
from matplotlib.colors import Normalize
norm = Normalize(vmin=data.min(), vmax=data.max())
im1 = ax1.imshow(d1, norm=norm, cmap='viridis')
im2 = ax2.imshow(d2, norm=norm, cmap='viridis')
```

### Unexpected Colors
```python
# Check color spec
ax.plot(x, y, color='blue')        # Named
ax.plot(x, y, color='#0000FF')     # Hex
ax.plot(x, y, color=(0, 0, 1))     # RGB tuple

# Verify colormap exists
print(plt.colormaps())

# Check scatter color array shape
ax.scatter(x, y, c=colors)  # len(colors) must equal len(x)
```

### Reversed Colormap
```python
ax.imshow(data, cmap='viridis_r')  # Append _r to reverse
```

## Axis and Scale Issues

### Axis Limits Not Working
```python
ax.plot(x, y)
ax.set_xlim(0, 10)       # Set AFTER plotting
ax.autoscale(False)        # Disable autoscaling
```

### Log Scale with Zero/Negative Values
```python
# Filter non-positive
mask = data > 0
ax.plot(x[mask], data[mask])
ax.set_yscale('log')

# Symlog for pos+neg data
ax.set_yscale('symlog')

# Small offset
ax.plot(x, data + 1e-10)
ax.set_yscale('log')
```

### Dates Not Displaying Correctly
```python
import matplotlib.dates as mdates
import pandas as pd

dates = pd.to_datetime(date_strings)
ax.plot(dates, values)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45, ha='right')
```

## Legend Issues

### Legend Covers Data
```python
ax.legend(loc='best')                                          # Auto-place
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')          # Outside right
ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)  # Below
ax.legend(framealpha=0.7)                                      # Transparent
```

### Too Many Legend Items
```python
# Label every Nth item
for i, y in enumerate(ys):
    ax.plot(x, y, label=f'S{i}' if i % 5 == 0 else None)

# Multiple columns
ax.legend(ncol=3)

# Custom legend with fewer entries
from matplotlib.lines import Line2D
handles = [Line2D([0], [0], color='r'), Line2D([0], [0], color='b')]
ax.legend(handles, ['Cat A', 'Cat B'])
```

## Saving and Export Issues

### White Background Not Preserved
```python
plt.savefig('fig.png', facecolor='white', dpi=300, bbox_inches='tight')
```

### Transparent Background
```python
plt.savefig('fig.png', transparent=True, dpi=300, bbox_inches='tight')
```

### Vector vs Raster
```python
# Vector (scalable, small for simple plots)
plt.savefig('fig.pdf')
plt.savefig('fig.svg')

# Raster (fixed resolution)
plt.savefig('fig.png', dpi=300)

# Hybrid (vector with rasterized elements)
ax.scatter(x, y, rasterized=True)
plt.savefig('fig.pdf', dpi=300)
```

## 3D Plot Issues

### 3D Plots Look Flat
```python
ax.view_init(elev=30, azim=45)   # Adjust angle
ax.grid(True)
scatter = ax.scatter(x, y, z, c=z, cmap='viridis')  # Depth cue via color
```

### 3D Axis Labels Cut Off
```python
fig.tight_layout(pad=3.0)
plt.savefig('3d.png', bbox_inches='tight', pad_inches=0.5)
```

## Seaborn-Specific Issues

### Legend Outside Plot
```python
g = sns.relplot(data=df, x='x', y='y', hue='group')
g._legend.set_bbox_to_anchor((0.9, 0.5))
# or for axes-level
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
```

### Overlapping Labels in Faceted Plots
```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
# or
for ax in g.axes.flat:
    ax.tick_params(axis='x', rotation=45)
```

### Figure Too Small
```python
# Figure-level: use height and aspect
sns.catplot(data=df, x='g', y='v', kind='box', height=6, aspect=1.5)
# Axes-level: use figsize
fig, ax = plt.subplots(figsize=(10, 6))
```

### Colors Not Distinct
```python
sns.set_palette("bright")
sns.set_palette(['#E64B35', '#4DBBD5', '#00A087', '#3C5488'])
```

### KDE Too Smooth or Jagged
```python
sns.kdeplot(data=df, x='value', bw_adjust=0.5)   # Less smooth
sns.kdeplot(data=df, x='value', bw_adjust=2.0)   # More smooth
```

## Common Errors

### "AxesSubplot is not subscriptable"
```python
# Wrong: single subplot returns ax, not array
fig, ax = plt.subplots()
ax[0].plot(x, y)  # Error!
# Fix:
ax.plot(x, y)
# Or force array:
fig, axes = plt.subplots(1, 1, squeeze=False)
axes[0, 0].plot(x, y)
```

### "x and y must have same first dimension"
```python
assert len(x) == len(y), f"Mismatch: x={len(x)}, y={len(y)}"
```

### "numpy.ndarray has no attribute 'plot'"
```python
# Wrong: calling plot on data
data.plot(x, y)
# Fix:
ax.plot(x, y)
# Pandas:
df.plot(x='col1', y='col2', ax=ax)
```

## Best Practices Checklist

1. Use OO interface: `fig, ax = plt.subplots()`
2. Use `constrained_layout=True` for spacing
3. Close figures: `plt.close(fig)` after saving
4. Set figsize at creation, not after
5. Use raw strings for math: `r'$\alpha$'`
6. Check data shapes before plotting
7. Use 300 DPI for print, 150 for web
8. Set `pdf.fonttype: 42` for PDF exports
9. Prefer `viridis`/`cividis` for colorblind safety
10. Always include axis labels and legends
