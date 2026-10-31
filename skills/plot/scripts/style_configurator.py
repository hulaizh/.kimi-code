#!/usr/bin/env python3
"""Create a small matplotlib style for finance charts and reports."""
from pathlib import Path
import argparse

PRESETS = {
    "finance": {
        "figure.figsize": (8, 4.5), "figure.dpi": 100, "savefig.dpi": 300,
        "savefig.bbox": "tight", "font.size": 10, "axes.labelsize": 10,
        "axes.titlesize": 12, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "legend.frameon": False, "pdf.fonttype": 42,
        "ps.fonttype": 42,
    },
    "presentation": {
        "figure.figsize": (12, 7), "figure.dpi": 100, "savefig.dpi": 150,
        "savefig.bbox": "tight", "font.size": 16, "axes.labelsize": 20,
        "axes.titlesize": 24, "axes.linewidth": 1.5, "lines.linewidth": 2.5,
        "legend.fontsize": 15, "axes.grid": True, "grid.alpha": 0.3,
    },
    "web": {
        "figure.figsize": (8, 4.5), "figure.dpi": 100, "savefig.dpi": 160,
        "savefig.bbox": "tight", "font.size": 11, "axes.labelsize": 11,
        "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": True,
    },
    "dark": {
        "figure.facecolor": "#1e1e1e", "figure.edgecolor": "#1e1e1e",
        "axes.facecolor": "#1e1e1e", "axes.edgecolor": "white",
        "axes.labelcolor": "white", "text.color": "white",
        "xtick.color": "white", "ytick.color": "white",
        "grid.color": "gray", "grid.alpha": 0.3, "axes.grid": True,
        "legend.facecolor": "#1e1e1e", "legend.edgecolor": "white",
        "savefig.facecolor": "#1e1e1e", "pdf.fonttype": 42,
    },
    "minimal": {
        "figure.figsize": (10, 6), "axes.spines.top": False,
        "axes.spines.right": False, "axes.spines.left": False,
        "axes.spines.bottom": False, "axes.grid": False,
        "xtick.bottom": True, "ytick.left": True, "axes.axisbelow": True,
        "lines.linewidth": 2.5, "font.size": 12, "pdf.fonttype": 42,
    },
}


def write_style(name, output):
    lines = [f"# Practitioner chart style: {name}"]
    for key, value in PRESETS[name].items():
        if isinstance(value, tuple): value = ", ".join(map(str, value))
        elif isinstance(value, bool): value = str(value)
        elif isinstance(value, str) and value.startswith("#"): value = f'"{value}"'
        lines.append(f"{key}: {value}")
    Path(output).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=PRESETS, default="finance")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--list", action="store_true", help="List practitioner presets")
    args = parser.parse_args()
    if args.list:
        print("Available practitioner presets: " + ", ".join(PRESETS))
        return
    if args.output: write_style(args.preset, args.output)
    if args.preview:
        import matplotlib.pyplot as plt
        with plt.style.context(PRESETS[args.preset]):
            fig, ax = plt.subplots()
            ax.plot([0, 1, 2], [0, 1, .7])
            ax.set_title(f"{args.preset} style (illustrative)")
            if args.output:
                fig.savefig(args.output.with_name(args.output.stem + "_preview.png"), dpi=150, bbox_inches="tight")
            plt.show()
            plt.close(fig)
    if not args.output and not args.preview:
        print("Available practitioner presets:", ", ".join(PRESETS))


if __name__ == "__main__": main()
