---
name: newproj
description: "Create a standard project folder structure with AGENTS.md, data, docs, src, output, report, slides, tests, temp, and hidden runtime folders. Use when initializing or scaffolding a new project, previewing a project setup, or adding missing folders to an existing project. Supports dry-run previews, non-overwriting completion, and optional Git initialization without automatic commits."
---

# newproj: standard project setup

Create one fixed project structure. The scaffold establishes folder ownership only. Later user prompts determine the analysis, deliverables, and validation work.

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

# Preview without writing
python3 <newproj-skill-dir>/scripts/init_project.py NAME --dry-run

# Initialize Git on main without staging or committing
python3 <newproj-skill-dir>/scripts/init_project.py NAME --git

# Add missing items to a nonempty directory without overwriting files
python3 <newproj-skill-dir>/scripts/init_project.py --path PATH --force
```

Use `--title` only when the user supplies a title or asks for one to be inferred from the request. Otherwise, use the folder name.

## Behavior

- Preview when the target directory is surprising or the user is unsure.
- Refuse an unexpected nonempty directory unless the user approves `--force`.
- Allow an existing scaffold to be resumed or completed.
- Never overwrite an existing file, including under `--force`.
- Keep every scaffold path inside the selected project directory.
- Run Git initialization only with `--git`; do not stage, commit, or push.
- After scaffolding, report the project path and ask what the user wants to work on. Do not invent the assignment or populate task-specific content.

`AGENTS.md` records the folder structure and folder roles only. Task briefs, source records, assumptions, validation notes, and other project documents belong to later interactions, not the initial template.
