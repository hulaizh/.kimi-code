# Conservative Student Project Scaffold

## Purpose

Redesign `newproj` for student coursework in AI Coding in Finance. Replace the existing GAN research scaffold with one fixed, conservative folder structure. The scaffold provides paths and folder conventions only; task-specific work begins through later user prompts.

## Project tree

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

Every folder and file belongs to the project directory. The scaffold contains no `README.md`, `CLAUDE.md`, notebook folder, configuration folder, GAN files, or starter Markdown documents in `docs/`.

Empty folders contain `.gitkeep` so the fixed structure survives version control.

## Starter files

`AGENTS.md` defines only the path structure and folder roles:

- `data/raw/` holds unchanged inputs; `data/processed/` holds generated data.
- `src/` holds reusable scripts.
- `output/figures/` and `output/tables/` hold generated exhibits.
- `report/` holds student-edited reports.
- `slides/` holds student-edited LaTeX/Beamer or HTML presentations.
- `tests/` holds code and reproducibility checks.
- `temp/` holds disposable files.
- `.state/` holds runtime state; `.logs/` holds execution logs.
- `docs/plans/` and `docs/notes/` hold documents created during later project work.

It does not contain task, data-source, or validation guidance.

`.gitignore` excludes credentials, common Python and LaTeX temporary files, OS files, and the contents of `data/`, `temp/`, `.state/`, and `.logs/`, while retaining their `.gitkeep` placeholders. Reports, slides, source code, documents, tests, and selected outputs remain trackable.

## Command behavior

`newproj NAME` creates `NAME/` in the current directory.

Options:

- `--path PATH`: scaffold a specific directory.
- `--title TITLE`: set the project title in `AGENTS.md`; default to the folder name.
- `--dry-run`: preview actions without writing anything.
- `--git`: initialize a Git repository on `main` without staging or committing files.
- `--force`: permit scaffolding into a nonempty directory without overwriting existing files.

The implementation uses only the Python standard library. It writes only within the selected project directory. Re-running it creates missing items and leaves existing files unchanged.

## Skill changes

- Rewrite `newproj/SKILL.md` around the fixed student scaffold and its commands.
- Replace the GAN implementation in `newproj/scripts/init_project.py`.
- Replace the research Git ignore template with the student template.
- Remove the unused GAN project instruction template from the active skill.
- Update trigger examples to student project setup rather than research project setup.

## Verification

Exercise the actual command to confirm:

1. A fresh scaffold produces exactly the approved tree and starter files.
2. `--dry-run` creates nothing.
3. A second run is idempotent and does not alter existing files.
4. An unexpected nonempty directory is refused without `--force`.
5. `--force` adds missing items without overwriting existing content.
6. `--git` initializes `main` without staging or committing files.
7. No generated path points outside the project directory.
8. No `README.md`, `CLAUDE.md`, GAN artifact, or starter document appears in `docs/`.
9. Git ignores the contents of `data/`, `temp/`, `.state/`, and `.logs/` while tracking their placeholders.
