#!/usr/bin/env python3
"""
Plot Template

Template demonstrating various plot types with best practices.
Use as a starting point for creating publication-quality visualizations.

Usage:
    python plot_template.py [--plot-type TYPE] [--style STYLE] [--output FILE]

Plot types:
    line, scatter, bar, histogram, heatmap, contour, box, violin, 3d, all
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import argparse


def set_publication_style():
    """Configure matplotlib for publication-quality figures."""
    plt.rcParams.update({
        'figure.figsize': (8, 5.5),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'lines.linewidth': 2,
        'axes.linewidth': 1.5,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })


def generate_sample_data():
    """Generate sample data for demonstrations."""
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    scatter_x = np.random.randn(200)
    scatter_y = np.random.randn(200)
    categories = ['A', 'B', 'C', 'D', 'E']
    bar_values = np.random.randint(10, 100, len(categories))
    hist_data = np.random.normal(0, 1, 1000)
    matrix = np.random.rand(10, 10)
    X, Y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
    Z = np.sin(np.sqrt(X**2 + Y**2))

    return {
        'x': x, 'y1': y1, 'y2': y2,
        'scatter_x': scatter_x, 'scatter_y': scatter_y,
        'categories': categories, 'bar_values': bar_values,
        'hist_data': hist_data, 'matrix': matrix,
        'X': X, 'Y': Y, 'Z': Z,
    }


def create_line_plot(data, ax=None):
    """Create line plot with best practices."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    ax.plot(data['x'], data['y1'], label='sin(x)', linewidth=2,
            marker='o', markevery=10, markersize=6)
    ax.plot(data['x'], data['y2'], label='cos(x)', linewidth=2, linestyle='--')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Line Plot Example')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')

    if created_fig:
        return ax.get_figure()
    return ax


def create_scatter_plot(data, ax=None):
    """Create scatter plot with color and size variations."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    colors = np.sqrt(data['scatter_x']**2 + data['scatter_y']**2)
    sizes = 50 * (1 + np.abs(data['scatter_x']))

    scatter = ax.scatter(data['scatter_x'], data['scatter_y'],
                         c=colors, s=sizes, alpha=0.6,
                         cmap='viridis', edgecolors='black', linewidth=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Scatter Plot Example')
    ax.grid(True, alpha=0.3, linestyle='--')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Distance from origin')

    if created_fig:
        return ax.get_figure()
    return ax


def create_bar_chart(data, ax=None):
    """Create a bar chart without inventing uncertainty estimates."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    x_pos = np.arange(len(data['categories']))
    bars = ax.bar(x_pos, data['bar_values'],
                  color='steelblue', edgecolor='black', linewidth=1.5,
                  capsize=5, alpha=0.8)

    colors = plt.cm.viridis(data['bar_values'] / data['bar_values'].max())
    for bar, color in zip(bars, colors):
        bar.set_facecolor(color)

    ax.set_xlabel('Category')
    ax.set_ylabel('Values')
    ax.set_title('Bar Chart Example')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(data['categories'])
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    if created_fig:
        return ax.get_figure()
    return ax


def create_histogram(data, ax=None):
    """Create an empirical histogram without assuming a distribution."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    ax.hist(data['hist_data'], bins=30, density=True,
            alpha=0.7, edgecolor='black', color='steelblue')

    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title('Histogram')
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    if created_fig:
        return ax.get_figure()
    return ax


def create_heatmap(data, ax=None):
    """Create heatmap with colorbar."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 8), constrained_layout=True)

    im = ax.imshow(data['matrix'], cmap='coolwarm', aspect='auto', vmin=0, vmax=1)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Value')

    ax.set_xlabel('X Index')
    ax.set_ylabel('Y Index')
    ax.set_title('Heatmap Example')

    if created_fig:
        return ax.get_figure()
    return ax


def create_contour_plot(data, ax=None):
    """Create contour plot with filled contours and labels."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 8), constrained_layout=True)

    contourf = ax.contourf(data['X'], data['Y'], data['Z'],
                            levels=20, cmap='viridis', alpha=0.8)
    contour = ax.contour(data['X'], data['Y'], data['Z'],
                         levels=10, colors='black', linewidths=0.5, alpha=0.4)
    ax.clabel(contour, inline=True, fontsize=8)
    cbar = plt.colorbar(contourf, ax=ax)
    cbar.set_label('Z value')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Contour Plot Example')
    ax.set_aspect('equal')

    if created_fig:
        return ax.get_figure()
    return ax


def create_box_plot(data, ax=None):
    """Create box plot comparing distributions."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    np.random.seed(42)
    box_data = [np.random.normal(0, std, 100) for std in range(1, 5)]
    bp = ax.boxplot(box_data, tick_labels=['Group 1', 'Group 2', 'Group 3', 'Group 4'],
                    patch_artist=True, showmeans=True,
                    boxprops=dict(facecolor='lightblue', edgecolor='black'),
                    medianprops=dict(color='red', linewidth=2),
                    meanprops=dict(marker='D', markerfacecolor='green', markersize=8))

    ax.set_xlabel('Groups')
    ax.set_ylabel('Values')
    ax.set_title('Box Plot Example')
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    if created_fig:
        return ax.get_figure()
    return ax


def create_violin_plot(data, ax=None):
    """Create violin plot showing distribution shapes."""
    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    np.random.seed(42)
    violin_data = [np.random.normal(0, std, 100) for std in range(1, 5)]
    parts = ax.violinplot(violin_data, positions=range(1, 5),
                          showmeans=True, showmedians=True)

    for pc in parts['bodies']:
        pc.set_facecolor('lightblue')
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')

    ax.set_xlabel('Groups')
    ax.set_ylabel('Values')
    ax.set_title('Violin Plot Example')
    ax.set_xticks(range(1, 5))
    ax.set_xticklabels(['Group 1', 'Group 2', 'Group 3', 'Group 4'])
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    if created_fig:
        return ax.get_figure()
    return ax


def create_3d_plot():
    """Create 3D surface plot."""
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    X = np.linspace(-5, 5, 50)
    Y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(X, Y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
    fig.colorbar(surf, ax=ax, shrink=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Surface Plot Example')
    ax.view_init(elev=30, azim=45)
    plt.tight_layout()
    return fig


def create_comprehensive_figure():
    """Create a comprehensive figure with multiple subplots."""
    data = generate_sample_data()

    fig = plt.figure(figsize=(16, 12), constrained_layout=True)
    gs = GridSpec(3, 3, figure=fig)

    ax1 = fig.add_subplot(gs[0, :2])
    create_line_plot(data, ax1)
    ax2 = fig.add_subplot(gs[0, 2])
    create_bar_chart(data, ax2)
    ax3 = fig.add_subplot(gs[1, 0])
    create_scatter_plot(data, ax3)
    ax4 = fig.add_subplot(gs[1, 1])
    create_histogram(data, ax4)
    ax5 = fig.add_subplot(gs[1, 2])
    create_box_plot(data, ax5)
    ax6 = fig.add_subplot(gs[2, :2])
    create_contour_plot(data, ax6)
    ax7 = fig.add_subplot(gs[2, 2])
    create_heatmap(data, ax7)

    fig.suptitle('Comprehensive Plot Template', fontsize=18, fontweight='bold')
    return fig


def main():
    """Main function to run the template."""
    parser = argparse.ArgumentParser(description='Plot template')
    parser.add_argument('--plot-type', type=str, default='all',
                        choices=['line', 'scatter', 'bar', 'histogram', 'heatmap',
                                 'contour', 'box', 'violin', '3d', 'all'],
                        help='Type of plot to create')
    parser.add_argument('--style', type=str, default='default',
                        help='Matplotlib style to use')
    parser.add_argument('--output', type=str, default='plot.png',
                        help='Output filename')
    parser.add_argument('--show', action='store_true', help='Open an interactive window')
    args = parser.parse_args()

    if args.style != 'default':
        plt.style.use(args.style)
    else:
        set_publication_style()

    data = generate_sample_data()

    plot_functions = {
        'line': create_line_plot,
        'scatter': create_scatter_plot,
        'bar': create_bar_chart,
        'histogram': create_histogram,
        'heatmap': create_heatmap,
        'contour': create_contour_plot,
        'box': create_box_plot,
        'violin': create_violin_plot,
    }

    if args.plot_type == '3d':
        fig = create_3d_plot()
    elif args.plot_type == 'all':
        fig = create_comprehensive_figure()
    else:
        fig = plot_functions[args.plot_type](data)

    fig.text(0.01, -0.02, 'Synthetic data — plotting demonstration only.', fontsize=9)
    fig.savefig(args.output, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {args.output}")
    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
