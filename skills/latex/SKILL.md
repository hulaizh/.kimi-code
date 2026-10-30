---
name: latex
description: "Format and compile LaTeX reports, analytical notes, memos, and Beamer presentations. Use for main.tex, report structure, booktabs tables, figure inclusion, references, layout problems, and PDF verification. Supports report/ and slides/ project folders and includes finance-report conventions for data periods, units, sources, and assumptions. NOT for generating figures (use plot), project scaffolding (use newproj), or drafting analysis."
---

# LaTeX reports and presentations

Produce clear, compilable documents whose formatting supports the finance question rather than obscuring it. Keep editable prose separate from generated tables and figures.

## Route the request

| Request | Location | Required reading |
|---|---|---|
| Finance report, analytical note, investment memo, portfolio/risk report | `report/` | [finance/references/reports.md](finance/references/reports.md) |
| Beamer presentation, classroom deck, investment pitch, defense | `slides/` | [slides/references/slides_format.md](slides/references/slides_format.md) |

Use `report/` as the default for a new LaTeX document. Use `slides/` for either LaTeX/Beamer or HTML presentations; this skill handles the LaTeX path.

For an existing document, preserve its established structure unless the user asks to change it. Inspect the actual files before applying conventions.

## Report workflow

1. Identify the audience, document type, required length, and existing project structure.
2. Start from [finance/assets/report_template.tex](finance/assets/report_template.tex) only when the user wants a new report. Do not insert a template into an existing document piecemeal.
3. Keep report sections in the report source. For a longer report, use separate section files under `report/sections/`.
4. Put generated table wrappers in `report/tables/` and refer to generated content from `output/tables/` using the project's established build or copy process.
5. Put LaTeX figure wrappers in `report/figures/`; keep generated image files in `output/figures/`.
6. State the data period, units, currency, sources, assumptions, and limitations where the reader needs them.
7. Compile and inspect the final PDF, not just the source.

For a short exercise, a single `report/main.tex` is enough. Do not create a complex section hierarchy merely to satisfy a template.

## Tables and figures

- Use `booktabs` with `\toprule`, `\midrule`, and `\bottomrule`; do not use `\hline`.
- Keep substantial `tabular` and TikZ content in separate files loaded with `\input{}`.
- Align numeric columns and make units explicit in headers or notes.
- Give tables and figures informative captions and labels. Notes should explain definitions, sources, and sample periods needed to interpret the exhibit.
- Do not manually retype generated results into a wrapper when a reproducible input path is available.

## Commands

Resolve `<latex-skill-dir>` from this skill's location.

```bash
# Compile a report with bibliography passes
python3 <latex-skill-dir>/draft/scripts/compile_latex.py report/main.tex

# Initialize a Beamer deck in an existing slides/ directory
cd slides && python3 <latex-skill-dir>/slides/scripts/init_slides.py

# Validate Beamer structure
python3 <latex-skill-dir>/slides/scripts/validate_slides.py slides/slides.tex
```

The compile script accepts any main `.tex` path; it is not limited to a research directory. Use the project's own build command when one exists.

## Verification

Before delivering a document:

1. Run the standard build and fix LaTeX errors.
2. Check for undefined references and citations, missing files, and problematic overfull boxes.
3. Inspect every rendered page for clipping, tiny text, broken table alignment, and empty placeholders.
4. Reconcile numbers in narrative and exhibits with the supplied or generated results.
5. Remove build artifacts that the project does not track; keep the requested PDF.

A successful compile alone is not enough: a polished document can still contain an incorrect unit, an unexplained sample period, or an unreadable exhibit.
