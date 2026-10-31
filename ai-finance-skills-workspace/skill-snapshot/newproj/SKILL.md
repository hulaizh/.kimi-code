---
name: newproj
description: "Use when initializing/scaffolding a new GAN research-paper project — folder structure, data/temp symlinks, .gitignore, project CLAUDE.md, GAN state, and the LaTeX article skeleton (defaults: JF journal, author Hulai Zhang). Triggers: newproj, new project, set up a new research project, start a new paper, create project scaffolding, new GAN project, scaffold a paper repo. Every project is a GAN project. NOT for replicating/reproducing a published paper (use replication); NOT for finding or brainstorming a research topic/idea (use ideate)."
---

# newproj

## Overview

Scaffolds a new GAN research project (or maintains a live one) with the
standard folder structure, data/temp symlinks, `.gitignore`, GAN state, the
LaTeX article skeleton, and a project-specific `CLAUDE.md`.

Every project created by this skill is a **GAN project** — there is no non-GAN
mode. The folder contract is owned by ONE document:
`~/.claude/plugins/gan/references/project_layout.md`. This skill implements it;
it does not restate it.

## Defaults — do NOT prompt the user

| Setting | Default | When to override |
|---|---|---|
| Mode | GAN | never — GAN is the only mode |
| Target journal | **JF** | only if the user explicitly names a different journal — the GAN review bar only (every draft keeps the working-paper format; a journal's format is applied on acceptance) |
| Author | **Hulai Zhang** | only if the user explicitly names a different author |

Treat JF and Hulai Zhang as silent defaults. Pass `--journal` / `--author`
**only** when the user's request explicitly states a different value.

Author note: pass the **bare name** to `--author`. The affiliation `\thanks{}`
footnote is hardcoded in the latex skill's paper template
(`skills/latex/draft/assets/paper_template.tex`) — never pass a `\thanks{}`
block (doing so double-prints the footnote and breaks the Internet
Appendix header).

## Usage

| Situation | Command |
|---|---|
| New project (canonical) | `~/.claude/skills/newproj/scripts/init_project.py NAME --title "Paper Title"` |
| Different journal (only on explicit request) | `… --title "..." --journal RFS` |
| Maintain a live GAN project | `… --path <dir>` (missing dirs, skeleton iff no `draft/main.tex`, registry-regenerated `.gitignore`; untrack list printed, `--force` executes it) |
| Scaffold into an existing non-GAN directory | `… --path <dir> --force` (create-if-absent throughout) |
| Preview | `… --dry-run` (works with every mode) |
| Merge template sections into `CLAUDE.md` | `… --merge-claude --backup` |
| Migrate data dirs to symlinks | `… --migrate-data --backup` |

### Options

| Option | Description |
|--------|-------------|
| `project_name` | Defaults to current directory name |
| `--path PATH` | Project path (default: current directory) |
| `--title TITLE` | Paper title (default: "Untitled Research Project") |
| `--author AUTHOR` | Bare author name (default: "Hulai Zhang") |
| `--journal J` | AER, Econometrica, QJE, JPE, RES, JF, JFE, RFS (default: JF; the review bar only — the skeleton is the working-paper format whatever the journal; any other venue is floored to JF) |
| `--entry-point T` | `user_topic` (default), `ideate`, `brainstorm`, `polished_project` |
| `--dry-run` | Preview without writing |
| `--backup` | Back up files to `.claude/backups/` before modifying |
| `--merge-claude` | Add missing sections to existing `CLAUDE.md` |
| `--migrate-data` | Convert `data/`,`temp/` dirs to symlinks |
| `--force` | Existing non-GAN directory: scaffold in place. Live GAN project: execute the volatile `.gan/` untrack list |

## What gets created

The tree in `project_layout.md`, scaffolded as: `src tests draft/{sections,tables,figures}
output/{tables,figures,results} docs/{plans,notes,slides,submission} logs .claude .proofs .gan/rounds`, the
`data/` and `temp/` symlinks to `/data/{user}/{project}/`, and:

- **`.gan/current_proposal.json`** — GAN-TEMPLATE proposal envelope
  (`materialization_status: "template"`); the Generator materializes it in Validate
  round 1. `.gan/state.jsonl` via the gan plugin's `state_manager.init_state`
  (fail-loud if the plugin is absent). `.gan/infra_issues.jsonl` capture journal and
  `.claude/settings.json` `autoCompactWindow=200000` are seeded here too.
- **LaTeX skeleton** copied from the `/latex` skill's draft assets; title
  substituted, `\input{sections/model}` commented out — the working-paper
  format every draft keeps, whatever journal is recorded (a journal's format
  is applied only on acceptance, `/latex <code>`; a live GAN project's
  existing draft is never rewritten). `draft/tables/` and
  `draft/figures/` carry READMEs stating the compile-time mirror contract;
  `output/results/README.md` states the JSON-handoff contract.
- **`.gitignore`** from `scripts/gitignore_template.txt`: research-focused
  patterns, root-anchored `/data` `/temp` `/logs`, and the `.gan/` block GENERATED
  from the producer registry (`gan_producer_registry.py --gitignore`), bounded by
  `# >>> gan producer registry` / `# <<< gan producer registry` markers so
  every maintenance run regenerates it in place. Never hand-edit that block.
- **`CLAUDE.md`** from `scripts/gan_claude_md_template.txt`: Project Overview,
  a Project Structure section that POINTS at the layout owner and holds only
  project-specific annotation, and Notes.
- **Git repo** — `git init -b main` plus an initial commit. The branch is pinned
  explicitly, never left to git's `init.defaultBranch` fallback, so a first push
  never makes GitHub adopt a `master` default.

## Behavior details

- **Three states, nothing inferred from partial contents.** `.gan/state.jsonl`
  present → **maintain** (missing layout dirs, the whole LaTeX skeleton only
  when `draft/main.tex` is absent, the registry-regenerated `.gitignore`,
  runtime seeds; `--merge-claude` / `--migrate-data` opt in). Otherwise a
  directory holding `.git`, `CLAUDE.md`, `.gitignore`, or `src/` → **refuse**
  unless `--force`, which scaffolds in place (also the retry for a scaffold
  that failed part-way). Anything else → **scaffold**.
- **A draft with a `main.tex` is the project's own**: template `.tex` files
  are never patched into it piecemeal.
- **Git hygiene**: the untrack list is registry-scoped — the exact
  `git rm --cached` set from `gan_producer_registry.gan_index_cleanup` (git's own
  `check-ignore` against the generated policy). Printed on every maintenance
  run; executed under `--force`. Working-tree copies are never touched.
- **Smart merge**: `--merge-claude` appends only missing sections under a
  dated header. **Backup**: `--backup` writes `filename.YYYYMMDD_HHMMSS.bak`
  to `.claude/backups/`.

