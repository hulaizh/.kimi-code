#!/usr/bin/env python3
"""Compile an A4 finance PDF report from report/main.tex."""
from pathlib import Path
import subprocess
import sys


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "report/main.tex")
    if not target.exists():
        raise SystemExit(f"Missing report source: {target}")
    result = subprocess.run(
        ["latexmk", "-pdf", "-halt-on-error", "-interaction=nonstopmode", target.name],
        cwd=target.parent,
        text=True,
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
