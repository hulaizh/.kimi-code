#!/usr/bin/env python3
"""
Compile LaTeX document with bibliography.

Usage:
    python compile_latex.py <path/to/main.tex> [--clean]

Runs: pdflatex -> bibtex -> pdflatex -> pdflatex
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path) -> tuple[bool, str]:
    """Run command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, f"Command not found: {cmd[0]}"


def compile_latex(tex_file: Path, clean: bool = False) -> bool:
    """Compile LaTeX document with bibliography."""
    if not tex_file.exists():
        print(f"Error: File not found: {tex_file}")
        return False

    cwd = tex_file.parent
    basename = tex_file.stem

    # Compilation sequence
    steps = [
        (["pdflatex", "-interaction=nonstopmode", tex_file.name], "First pdflatex pass"),
        (["bibtex", basename], "BibTeX"),
        (["pdflatex", "-interaction=nonstopmode", tex_file.name], "Second pdflatex pass"),
        (["pdflatex", "-interaction=nonstopmode", tex_file.name], "Third pdflatex pass"),
    ]

    for cmd, description in steps:
        print(f"Running: {description}...")
        success, output = run_command(cmd, cwd)

        if not success:
            # BibTeX can fail gracefully if no citations
            if "bibtex" in cmd[0].lower():
                if "I found no" in output or "empty" in output.lower():
                    print(f"  Warning: {description} - no citations found (continuing)")
                    continue
            print(f"  Error in {description}:")
            # Show last 20 lines of output
            lines = output.strip().split('\n')
            for line in lines[-20:]:
                if line.strip():
                    print(f"    {line}")
            return False
        print(f"  Done")

    pdf_file = cwd / f"{basename}.pdf"
    if pdf_file.exists():
        print(f"\n✅ Successfully compiled: {pdf_file}")

    # Clean auxiliary files if requested
    if clean:
        aux_extensions = ['.aux', '.bbl', '.blg', '.log', '.out', '.toc', '.lof', '.lot']
        for ext in aux_extensions:
            aux_file = cwd / f"{basename}{ext}"
            if aux_file.exists():
                aux_file.unlink()
        print("Cleaned auxiliary files")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python compile_latex.py <path/to/main.tex> [--clean]")
        sys.exit(1)

    tex_file = Path(sys.argv[1])
    clean = "--clean" in sys.argv

    success = compile_latex(tex_file, clean)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
