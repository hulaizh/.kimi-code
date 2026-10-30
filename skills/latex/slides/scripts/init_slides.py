#!/usr/bin/env python3
"""
Initialize a new Beamer slides project with standard structure.

Usage:
    python init_slides.py [project_name]

If project_name is provided, creates a new directory.
If omitted, initializes in current directory.
"""

import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1] / "assets"


def init_slides(project_dir: Path):
    """Initialize a Beamer slides project with standard structure."""

    # Create directories
    dirs = ["misc", "figures", "tables"]
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)

    # Copy template files
    files_to_copy = [
        ("style.tex", "misc/style.tex"),
        ("slides_template.tex", "slides.tex"),
        ("ref.bib", "misc/ref.bib"),
        ("logo.png", "misc/logo.png"),
    ]

    for src, dst in files_to_copy:
        src_path = SKILL_DIR / src
        dst_path = project_dir / dst
        if src_path.exists() and not dst_path.exists():
            shutil.copy(src_path, dst_path)
            print(f"  Created: {dst}")
        elif dst_path.exists():
            print(f"  Skipped (exists): {dst}")
        else:
            print(f"  Warning: Template not found: {src}")

    print(f"\nProject initialized at: {project_dir}")
    print("\nStructure:")
    print("  slides.tex        Main Beamer file")
    print("  misc/style.tex    Theme and formatting")
    print("  misc/ref.bib      Bibliography")
    print("  misc/logo.png     Title slide logo")
    print("  figures/           TikZ and image files")
    print("  tables/            Table .tex files")
    print("\nNext steps:")
    print("  1. Edit slides.tex with your content")
    print("  2. Add references to misc/ref.bib")
    print("  3. Put TikZ figures in figures/")
    print("  4. Put tables in tables/")


def main():
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
        project_dir = Path.cwd() / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
    else:
        project_dir = Path.cwd()

    print("Initializing Beamer slides project...")
    init_slides(project_dir)


if __name__ == "__main__":
    main()
