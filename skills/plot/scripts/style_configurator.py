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
}


def write_style(name, output):
    lines = [f"# Practitioner chart style: {name}"]
    for key, value in PRESETS[name].items():
        if isinstance(value, tuple): value = ", ".join(map(str, value))
        elif isinstance(value, bool): value = str(value)
        lines.append(f"{key}: {value}")
    Path(output).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=PRESETS, default="finance")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    if args.output: write_style(args.preset, args.output)
    if args.preview:
        import matplotlib.pyplot as plt
        with plt.style.context(PRESETS[args.preset]):
            fig, ax = plt.subplots(); ax.plot([0, 1, 2], [0, 1, .7]); ax.set_title(args.preset)
            plt.show()
    if not args.output and not args.preview:
        print("Available practitioner presets:", ", ".join(PRESETS))


if __name__ == "__main__": main()
