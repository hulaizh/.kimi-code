---
name: newproj
description: "Initialize a project directory, add missing scaffold files, and organize recognized loose files into standard folders without overwriting existing work. Use for project setup, folder scaffolding, dry-run previews, and optional Git initialization. Creates folder roles and project instructions; does not implement analysis, generate reports, or install dependencies."
---

# newproj: standard project setup

Create one fixed project structure and place recognized loose files in their owning folders. Later user prompts determine the analysis, deliverables, and validation work.

Use task-based names such as `cash-forecast`, `credit-review`, `portfolio-report`, or `budget-variance` when the user asks for a suggested name. Explain the input → script → output flow briefly for an unfamiliar user. Keep scaffolding separate from implementing the task, but continue with implementation when the user's original request already includes it.

## Standard tree

```text
project/
├── AGENTS.md
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── plans/
│   └── notes/
├── src/
├── output/
│   ├── figures/
│   └── tables/
├── report/
├── slides/
├── tests/
├── temp/
├── .state/
└── .logs/
```

The contents of `data/`, `temp/`, `.state/`, and `.logs/` are Git-ignored, while their placeholders remain trackable.

The fixed scaffold retains `data/processed/` for projects that use it. Project instructions take precedence: when intermediate data belongs in `temp/`, use that directory and leave `data/processed/` unused. Do not alter folder roles silently.

## Existing files

When the target already contains files, organize only regular files directly in its root; do not recurse into directories or move directories themselves. Route recognized files as follows:

- Source scripts and notebooks to `src/`; root test files named `test_*` or `*_test` to `tests/`.
- Tabular and serialized input data to `data/raw/`, preserving their contents.
- Report documents to `report/`, presentation files to `slides/`, and image files to `output/figures/`.

Leave unrecognized files, including existing README and configuration files, in place. If the destination already exists, leave the source file unchanged and report the skip rather than overwriting or renaming either file. A dry run lists planned moves without making them.

Do not add a README, `CLAUDE.md`, notebook folder, configuration folder, starter analysis code, prewritten report, or starter Markdown documents to `docs/`. Do not turn the scaffold into a larger workflow system unless the user separately requests one.

## Commands

Resolve `<newproj-skill-dir>` from this skill's location.

```bash
# Create NAME/ in the current directory
python3 <newproj-skill-dir>/scripts/init_project.py NAME

# Scaffold a specific directory
python3 <newproj-skill-dir>/scripts/init_project.py --path PATH

# Set the title recorded in AGENTS.md
python3 <newproj-skill-dir>/scripts/init_project.py NAME --title "Project Title"

# Preview scaffold creation and file moves without writing
python3 <newproj-skill-dir>/scripts/init_project.py NAME --dry-run

# Initialize Git on main without staging or committing
python3 <newproj-skill-dir>/scripts/init_project.py NAME --git

# Add missing items and organize loose files in a nonempty directory
python3 <newproj-skill-dir>/scripts/init_project.py --path PATH --force
```

Use `--title` only when the user supplies a title or asks for one to be inferred from the request. Otherwise, use the folder name.

## Behavior

- Preview when the target directory is surprising or the user is unsure.
- Refuse an unexpected nonempty directory unless the user approves `--force`.
- Allow an existing scaffold to be resumed or completed, including organizing newly recognized loose root files.
- Never overwrite an existing file, including under `--force`.
- Keep every scaffold path and moved file inside the selected project directory.
- Run Git initialization only with `--git`; do not stage, commit, or push.
- After scaffolding, report the project path and any skipped file moves. If setup was the entire request, stop there. If the user also requested analysis, continue with that task using the appropriate workflow.

`AGENTS.md` records the folder structure and folder roles only. Task briefs, source records, assumptions, validation notes, and other project documents belong to later interactions, not the initial template.
