#!/usr/bin/env python3
"""
Style Configurator

Configure matplotlib style preferences and generate custom style sheets.
Creates a preview of the style and optionally saves it as a .mplstyle file.

Usage:
    python style_configurator.py --preset publication --preview
    python style_configurator.py --preset journal --output my_style.mplstyle
    python style_configurator.py --list
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import argparse


# Predefined style presets
STYLE_PRESETS = {
    'publication': {
        'figure.figsize': (8, 6),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica'],
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'axes.linewidth': 1.5,
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'lines.linewidth': 2,
        'lines.markersize': 8,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.size': 6,
        'ytick.major.size': 6,
        'xtick.major.width': 1.5,
        'ytick.major.width': 1.5,
        'legend.fontsize': 10,
        'legend.frameon': True,
        'legend.framealpha': 1.0,
        'legend.edgecolor': 'black',
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    },
    'journal': {
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
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
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
    },
    'presentation': {
        'figure.figsize': (12, 8),
        'figure.dpi': 100,
        'savefig.dpi': 150,
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
        'pdf.fonttype': 42,
    },
    'web': {
        'figure.figsize': (10, 6),
        'figure.dpi': 96,
        'savefig.dpi': 150,
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'lines.linewidth': 2,
        'axes.grid': True,
        'grid.alpha': 0.2,
        'grid.linestyle': '--',
        'pdf.fonttype': 42,
    },
    'dark': {
        'figure.facecolor': '#1e1e1e',
        'figure.edgecolor': '#1e1e1e',
        'axes.facecolor': '#1e1e1e',
        'axes.edgecolor': 'white',
        'axes.labelcolor': 'white',
        'text.color': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'grid.color': 'gray',
        'grid.alpha': 0.3,
        'axes.grid': True,
        'legend.facecolor': '#1e1e1e',
        'legend.edgecolor': 'white',
        'savefig.facecolor': '#1e1e1e',
        'pdf.fonttype': 42,
    },
    'minimal': {
        'figure.figsize': (10, 6),
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': False,
        'axes.spines.bottom': False,
        'axes.grid': False,
        'xtick.bottom': True,
        'ytick.left': True,
        'axes.axisbelow': True,
        'lines.linewidth': 2.5,
        'font.size': 12,
        'pdf.fonttype': 42,
    },
}


def generate_preview_data():
    """Generate sample data for style preview."""
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) + 0.1 * np.random.randn(100)
    y2 = np.cos(x) + 0.1 * np.random.randn(100)
    scatter_x = np.random.randn(100)
    scatter_y = 2 * scatter_x + np.random.randn(100)
    categories = ['A', 'B', 'C', 'D', 'E']
    bar_values = [25, 40, 30, 55, 45]
    return {
        'x': x, 'y1': y1, 'y2': y2,
        'scatter_x': scatter_x, 'scatter_y': scatter_y,
        'categories': categories, 'bar_values': bar_values,
    }


def create_style_preview(style_dict=None):
    """Create a preview figure demonstrating the style."""
    if style_dict:
        plt.rcParams.update(style_dict)

    data = generate_preview_data()

    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Line plot
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(data['x'], data['y1'], label='sin(x)', marker='o', markevery=10)
    ax1.plot(data['x'], data['y2'], label='cos(x)', linestyle='--')
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_title('Line Plot')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Scatter plot
    ax2 = fig.add_subplot(gs[0, 1])
    colors = np.sqrt(data['scatter_x']**2 + data['scatter_y']**2)
    scatter = ax2.scatter(data['scatter_x'], data['scatter_y'],
                          c=colors, cmap='viridis', alpha=0.6, s=50)
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_title('Scatter Plot')
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('Distance')

    # Bar chart
    ax3 = fig.add_subplot(gs[1, 0])
    bars = ax3.bar(data['categories'], data['bar_values'],
                   edgecolor='black', linewidth=1)
    bar_colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(bars)))
    for bar, color in zip(bars, bar_colors):
        bar.set_facecolor(color)
    ax3.set_xlabel('Categories')
    ax3.set_ylabel('Values')
    ax3.set_title('Bar Chart')

    # Fill between
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(data['x'], data['y1'], label='Signal 1', linewidth=2)
    ax4.fill_between(data['x'], data['y1'] - 0.2, data['y1'] + 0.2, alpha=0.3)
    ax4.plot(data['x'], data['y2'], label='Signal 2', linewidth=2)
    ax4.fill_between(data['x'], data['y2'] - 0.2, data['y2'] + 0.2, alpha=0.3)
    ax4.set_xlabel('X axis')
    ax4.set_ylabel('Y axis')
    ax4.set_title('Time Series with Uncertainty')
    ax4.legend()

    fig.suptitle('Style Preview', fontsize=16, fontweight='bold')
    return fig


def save_style_file(style_dict, filename):
    """Save style dictionary as .mplstyle file."""
    categories = {
        'Figure': ['figure.'],
        'Font': ['font.'],
        'Axes': ['axes.'],
        'Lines': ['lines.'],
        'Ticks': ['tick.', 'xtick.', 'ytick.'],
        'Grid': ['grid.'],
        'Legend': ['legend.'],
        'Savefig': ['savefig.'],
        'Text': ['text.'],
        'PDF': ['pdf.', 'ps.'],
    }

    with open(filename, 'w') as f:
        f.write("# Custom matplotlib style\n")
        f.write("# Generated by style_configurator.py\n\n")

        for category, prefixes in categories.items():
            items = {k: v for k, v in style_dict.items()
                     if any(k.startswith(p) for p in prefixes)}
            if items:
                f.write(f"# {category}\n")
                for key, value in sorted(items.items()):
                    if isinstance(value, (list, tuple)):
                        value_str = ', '.join(str(v) for v in value)
                    else:
                        value_str = str(value)
                    f.write(f"{key}: {value_str}\n")
                f.write("\n")

    print(f"Style saved to {filename}")


def print_style_info(style_dict):
    """Print information about the style."""
    print("\n" + "=" * 60)
    print("STYLE CONFIGURATION")
    print("=" * 60)

    groups = {
        'Figure': ['figure.'],
        'Font': ['font.'],
        'Axes': ['axes.'],
        'Lines': ['lines.'],
        'Grid': ['grid.'],
        'Legend': ['legend.'],
        'PDF Export': ['pdf.', 'ps.', 'savefig.'],
    }

    for group, prefixes in groups.items():
        items = {k: v for k, v in style_dict.items()
                 if any(k.startswith(p) for p in prefixes)}
        if items:
            print(f"\n{group}:")
            for key, value in sorted(items.items()):
                print(f"  {key}: {value}")

    print("\n" + "=" * 60 + "\n")


def list_available_presets():
    """Print available style presets."""
    print("\nAvailable style presets:")
    print("-" * 50)
    descriptions = {
        'publication': 'Sans-serif, clean, suitable for general publication',
        'journal': 'Serif, compact, optimized for economics/finance journals',
        'presentation': 'Large fonts for slides and talks',
        'web': 'Optimized for web display',
        'dark': 'Dark background theme',
        'minimal': 'Minimal, clean style with no spines',
    }
    for preset, desc in descriptions.items():
        print(f"  {preset:15s} - {desc}")
    print("-" * 50 + "\n")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Matplotlib style configurator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python style_configurator.py --list
  python style_configurator.py --preset publication --preview
  python style_configurator.py --preset journal --output my_style.mplstyle
  python style_configurator.py --preset journal --preview --output journal.mplstyle
        """
    )
    parser.add_argument('--preset', type=str, choices=list(STYLE_PRESETS.keys()),
                        help='Use a predefined style preset')
    parser.add_argument('--output', type=str,
                        help='Save style to .mplstyle file')
    parser.add_argument('--preview', action='store_true',
                        help='Show style preview')
    parser.add_argument('--list', action='store_true',
                        help='List available presets')

    args = parser.parse_args()

    if args.list:
        list_available_presets()
        print("Built-in matplotlib styles:")
        print("-" * 50)
        for style in sorted(plt.style.available):
            print(f"  {style}")
        return

    if args.preset:
        style_dict = STYLE_PRESETS[args.preset].copy()
        print(f"Using '{args.preset}' preset")
    else:
        print("No preset specified. Use --preset to select one, or --list to see options.")
        style_dict = {}

    if style_dict:
        print_style_info(style_dict)

    if args.output and style_dict:
        save_style_file(style_dict, args.output)

    if args.preview:
        print("Creating style preview...")
        fig = create_style_preview(style_dict if style_dict else None)

        if args.output:
            preview_filename = args.output.replace('.mplstyle', '_preview.png')
            plt.savefig(preview_filename, dpi=150, bbox_inches='tight')
            print(f"Preview saved to {preview_filename}")

        plt.show()


if __name__ == "__main__":
    main()
