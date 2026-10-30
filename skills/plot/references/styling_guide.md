# Styling Guide

## Table of Contents
- [Colormaps](#colormaps)
- [Creating Custom Colormaps](#creating-custom-colormaps)
- [Color Palettes and Cycles](#color-palettes-and-cycles)
- [Style Sheets](#style-sheets)
- [Typography and Math Text](#typography-and-math-text)
- [Spines, Grids, and Legends](#spines-grids-and-legends)
- [Layout and Spacing](#layout-and-spacing)
- [Publication-Ready Journal Presets](#publication-ready-journal-presets)
- [Seaborn Theming](#seaborn-theming)
- [Color Accessibility](#color-accessibility)
- [Dark Theme](#dark-theme)

## Colormaps

### Categories

| Category | Colormaps | Use Case |
|----------|-----------|----------|
| Perceptually uniform | `viridis`, `plasma`, `inferno`, `magma`, `cividis` | Ordered data, default choice |
| Sequential | `Blues`, `Greens`, `Reds`, `YlOrRd`, `BuPu` | Increasing/decreasing data |
| Diverging | `coolwarm`, `RdBu`, `RdYlBu`, `PiYG`, `PuOr` | Data with meaningful center |
| Qualitative | `tab10`, `tab20`, `Set1`, `Set2`, `Set3`, `Paired` | Categorical data |
| Cyclic | `twilight`, `twilight_shifted`, `hsv` | Phase, angle data |

**Best practices:**
1. Avoid `jet` (not perceptually uniform, misleading)
2. Use `viridis`/`cividis` for colorblind-friendly defaults
3. Reverse any colormap by appending `_r`: `viridis_r`
4. Center diverging maps at zero: `vmin=-1, vmax=1` or `center=0`

**Seaborn-specific palettes:**
- Qualitative: `"deep"`, `"muted"`, `"pastel"`, `"bright"`, `"dark"`, `"colorblind"`
- Sequential: `"rocket"`, `"mako"`, `"flare"`, `"crest"`
- Diverging: `"vlag"`, `"icefire"`

## Creating Custom Colormaps

```python
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm

# From color list
colors = ['blue', 'white', 'red']
cmap = LinearSegmentedColormap.from_list('custom', colors, N=100)

# Discrete colormap
cmap = plt.cm.viridis
bounds = np.linspace(0, 10, 11)
norm = BoundaryNorm(bounds, cmap.N)
im = ax.imshow(data, cmap=cmap, norm=norm)

# Two-slope norm (asymmetric diverging)
from matplotlib.colors import TwoSlopeNorm
norm = TwoSlopeNorm(vmin=-5, vcenter=0, vmax=10)
im = ax.imshow(data, cmap='RdBu_r', norm=norm)
```

## Color Palettes and Cycles

```python
# Matplotlib color cycle
from cycler import cycler
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

# Combine color and line style
plt.rcParams['axes.prop_cycle'] = (
    cycler(color=colors) + cycler(linestyle=['-', '--', ':', '-.'])
)

# Extract N colors from colormap
n = 5
colors = plt.cm.viridis(np.linspace(0, 1, n))

# Seaborn palettes
sns.set_palette("colorblind")
custom_pal = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F']
sns.set_palette(custom_pal)

# Colorblind-friendly discrete colors (validated)
cb_colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC',
             '#CA9161', '#949494', '#ECE133', '#56B4E9']
```

## Style Sheets

### Built-in Styles
```python
print(plt.style.available)  # List all

plt.style.use('seaborn-v0_8-whitegrid')
plt.style.use(['seaborn-v0_8-whitegrid', 'seaborn-v0_8-poster'])  # Stack

# Temporary style
with plt.style.context('ggplot'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```

**Popular styles:** `default`, `ggplot`, `bmh`, `fivethirtyeight`, `grayscale`, `seaborn-v0_8-whitegrid`, `seaborn-v0_8-ticks`

### Custom .mplstyle File
```
# custom_style.mplstyle
figure.figsize: 8, 5.5
figure.dpi: 100
font.family: serif
font.serif: Times New Roman, DejaVu Serif
font.size: 10
axes.labelsize: 11
axes.titlesize: 12
axes.linewidth: 0.8
axes.spines.top: False
axes.spines.right: False
lines.linewidth: 1.5
xtick.labelsize: 9
ytick.labelsize: 9
xtick.direction: in
ytick.direction: in
legend.fontsize: 9
legend.frameon: False
savefig.dpi: 300
savefig.bbox: tight
pdf.fonttype: 42
```

Load: `plt.style.use('path/to/custom_style.mplstyle')`

## Typography and Math Text

### Font Configuration
```python
# Serif (academic papers)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

# Sans-serif (presentations, web)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# Font properties in text
ax.text(x, y, 'Text', fontsize=14, fontweight='bold', fontstyle='italic')

# Specific font file
from matplotlib import font_manager
prop = font_manager.FontProperties(fname='path/to/font.ttf')
ax.text(x, y, 'Text', fontproperties=prop)
```

### LaTeX Math Text
```python
# Built-in mathtext (always available, no LaTeX needed)
ax.set_title(r'$\alpha > \beta$')
ax.set_xlabel(r'$\mu \pm \sigma$')
ax.text(x, y, r'$\int_0^\infty e^{-x} dx = 1$')

# Full LaTeX rendering (requires LaTeX installation)
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
ax.set_title(r'\textbf{Bold Title}')
```

### Font Embedding for PDF
```python
# CRITICAL for journal submissions
plt.rcParams['pdf.fonttype'] = 42   # TrueType fonts
plt.rcParams['ps.fonttype'] = 42    # TrueType in PostScript
```

## Spines, Grids, and Legends

### Spine Customization
```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_linewidth(1.5)

# Seaborn shortcut
sns.despine(left=False, bottom=False, offset=10, trim=True)
```

### Grid Customization
```python
ax.grid(True, which='major', linestyle='--', linewidth=0.8, alpha=0.3)
ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.2)
ax.grid(True, axis='y')       # Horizontal lines only
ax.set_axisbelow(True)         # Grid behind data
```

### Legend Positioning and Styling
```python
# Location
ax.legend(loc='best')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')      # Outside right
ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)  # Below

# Styling
ax.legend(fontsize=10, frameon=True, framealpha=0.9, fancybox=True,
          shadow=False, ncol=2, title='Groups', edgecolor='black')

# Custom handles
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
handles = [Line2D([0], [0], color='r', lw=2, label='Line'),
           Patch(facecolor='blue', alpha=0.5, label='Area')]
ax.legend(handles=handles)
```

## Layout and Spacing

```python
# Constrained layout (preferred)
fig, axes = plt.subplots(2, 2, constrained_layout=True)

# Tight layout
plt.tight_layout(pad=1.5, h_pad=2.0, w_pad=2.0)

# Manual adjustment
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15,
                    hspace=0.3, wspace=0.4)
```

## Publication-Ready Journal Presets

### Economics (AER, QJE, JPE, Econometrica, REStud)

```python
def setup_econ_style():
    """Style for economics journals (single-column ~3.4in, double ~6.75in)."""
    plt.rcParams.update({
        'figure.figsize': (6.5, 4.5),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'Computer Modern Roman', 'DejaVu Serif'],
        'font.size': 9,
        'axes.labelsize': 10,
        'axes.titlesize': 11,
        'axes.linewidth': 0.6,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'lines.linewidth': 1.2,
        'lines.markersize': 4,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.size': 3,
        'ytick.major.size': 3,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'legend.fontsize': 8,
        'legend.frameon': False,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })
```

### Finance (JF, JFE, RFS)

```python
def setup_finance_style():
    """Style for finance journals (~6.5in wide)."""
    plt.rcParams.update({
        'figure.figsize': (6.5, 4.0),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 9,
        'axes.labelsize': 10,
        'axes.titlesize': 11,
        'axes.linewidth': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'lines.linewidth': 1.5,
        'lines.markersize': 5,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'legend.fontsize': 8,
        'legend.frameon': False,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })
```

### Presentation / Talk

```python
def setup_presentation_style():
    """Large fonts for slides and talks."""
    plt.rcParams.update({
        'figure.figsize': (12, 7),
        'font.size': 16,
        'axes.labelsize': 20,
        'axes.titlesize': 24,
        'axes.linewidth': 2,
        'lines.linewidth': 3,
        'lines.markersize': 12,
        'xtick.labelsize': 16,
        'ytick.labelsize': 16,
        'legend.fontsize': 16,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'savefig.dpi': 150,
    })
```

## Seaborn Theming

```python
# Quick theme setup
sns.set_theme(style='ticks', context='paper', palette='colorblind',
              font='serif', font_scale=1.0)

# Styles: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
# Contexts: 'paper', 'notebook', 'talk', 'poster'

# Customize with rc overrides
sns.set_theme(context='paper', style='ticks', rc={
    'pdf.fonttype': 42,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'legend.frameon': False,
})

# Remove top/right spines
sns.despine(offset=10, trim=True)
```

## Color Accessibility

### Colorblind-Friendly Choices

```python
# Colormaps: viridis, cividis (best for colorblind)
# Seaborn palette: "colorblind"
# Validated discrete palette:
cb_safe = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC',
           '#CA9161', '#949494', '#ECE133', '#56B4E9']

# Additional strategies:
# 1. Use different markers/line styles in addition to color
# 2. Add patterns/hatching to bars
bars = ax.bar(x, y, color='white', edgecolor='black', hatch='//')
# 3. Use shape + color encoding
sns.scatterplot(data=df, x='x', y='y', hue='group', style='group')
```

### High Contrast
```python
plt.rcParams.update({
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'xtick.major.width': 2,
    'ytick.major.width': 2,
})
```

## Dark Theme

```python
# Quick
plt.style.use('dark_background')

# Manual
plt.rcParams.update({
    'figure.facecolor': '#1e1e1e',
    'axes.facecolor': '#1e1e1e',
    'axes.edgecolor': 'white',
    'axes.labelcolor': 'white',
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'grid.color': 'gray',
    'legend.facecolor': '#1e1e1e',
    'legend.edgecolor': 'white',
    'savefig.facecolor': '#1e1e1e',
})
```
