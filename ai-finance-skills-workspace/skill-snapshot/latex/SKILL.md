---
name: latex
description: "Use for every LaTeX formatting job in finance/economics. DRAFT class: papers, working papers and internet appendices in the ONE working-paper format every draft keeps (wp: a4paper 12pt, 1.5in/1in margins, one-half spacing, section files, two-level tables/figures, validate and compile), plus the journal pass ONLY once a paper is ACCEPTED (`/latex <code>`: AER, QJE, JPE, REStud, Econometrica, JF, RFS, JFE, RF, JFQA, Management Science). SLIDES class: Beamer lecture, seminar, conference, job-market and defense decks. Triggers: format my paper, main.tex, internet appendix, accepted at JFQA, final version for JF, production files, apply the JF format, beamer, slides.tex, latex-format, latex-draft, latex-slides, journal-style. NOT for scaffolding a repo (newproj); figure content (plot); revision letters (rr); content edits (copy-edit)."
---

# latex — draft (the working-paper format; a journal's format on acceptance) and slides

Every working paper keeps ONE format — wp (`draft/references/wp.md`): the
structure (section files, two-level exhibits, booktabs, citation commands,
theorem notation) and the layout (a4paper, 12pt, 1.5in top/bottom and 1in
side margins, one-half spacing, 60 manuscript pages plus a 40-page Internet
Appendix, a 100-word abstract). `validate_latex.py` and the gan S0 gate hold
every draft to it; no journal fact reaches a draft (user directive
2026-09-21). The target journal recorded in `.gan/state.json`
(`target_journal`, JF floor) is the REVIEW BAR only. A journal's own format
lives in `draft/journals/<code>.yaml` and is applied ONCE, when the paper is
accepted there — the journal pass on `/latex <code>`. The engine reuses the
gan plugin's LaTeX log parser and Codex pin when present (no gan GATE
consumes a journal fact — that is the decoupling).

| Request | Class | Read |
|---|---|---|
| paper, draft, manuscript, main.tex, internet appendix | draft | `draft/references/wp.md` |
| journal code — "/latex JF", "accepted at JFQA", "final version for JF", "production files" | draft (journal pass — accepted papers only) | `draft/references/journal_file.md` |
| slides, beamer, talk, deck, slides.tex | slides | `slides/references/slides_format.md` |

## Commands (`~/.claude/skills/latex/`)

| Task | Command |
|---|---|
| Validate a draft (structure + the working-paper layout) | `draft/scripts/validate_latex.py draft/main.tex` |
| Compile | `draft/scripts/compile_latex.py draft/main.tex` |
| Table wrapper | `draft/scripts/build_table_wrapper.py --label X --caption Y --content tables/X --description "…"` |
| Journal pass on an ACCEPTED paper: check (never writes) / apply + compile + report / one Codex round | `draft/scripts/journal_format.py {check|apply|codex} --journal jf draft/main.tex` |
| Slides init / validate | `slides/scripts/init_slides.py docs/slides/talk` · `slides/scripts/validate_slides.py slides.tex` |

## The journal pass, in order (accepted papers only)

Checkpoint commit → `apply` → house pass (each `house:` item in
`draft/journals/<code>.yaml`, edit the source, record counts) → `codex`,
apply what you accept, decline the rest with a reason → `apply` again
(≤3 recompiles total) → commit → report. Run it ONLY when the paper is
accepted at that journal (`/latex <code>`, "accepted at JF", "production
files") — never on a working paper, never at init, never on a target
change. Never a per-requirement question; the closing message is the report
summary. Journal files are facts only — the journal's ACCEPTED-paper format
as recorded from its sources (`verified:` names the sections read from the
journal's own guidelines): a stated fact is applied and checked, an unstated
fact is never checked and never defaulted, an unknown key is a load error.

## Two principles, every class

1. Exhibits live in `tables/` and `figures/`, pulled in via `\input{}` /
   `\includegraphics{}` — never inline tabular or TikZ in the main document.
2. booktabs rules (`\toprule`/`\midrule`/`\bottomrule`), never `\hline`.
