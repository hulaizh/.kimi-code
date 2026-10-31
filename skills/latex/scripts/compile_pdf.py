#!/usr/bin/env python3
"""Compile an A4 finance PDF report from report/main.tex."""
import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=Path("report/main.tex"))
    parser.add_argument("--engine", choices=("pdflatex", "xelatex", "lualatex"), default="pdflatex")
    args = parser.parse_args()
    target = args.source.expanduser().resolve()
    if not target.is_file():
        raise SystemExit(f"Missing report source: {target}")
    engine_flag = {"pdflatex": "-pdf", "xelatex": "-xelatex", "lualatex": "-lualatex"}[args.engine]
    result = subprocess.run(
        ["latexmk", engine_flag, "-halt-on-error", "-interaction=nonstopmode", target.name],
        cwd=target.parent,
        text=True,
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
