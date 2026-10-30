---
name: latex
description: "Format, compile, and inspect LaTeX documents and Beamer presentations. Use for report structure, tables, figure inclusion, citations, layout fixes, and PDF build problems. Keeps generated exhibit content separate from captions and notes. Not for Word/PowerPoint files, chart generation (use plot), or inventing analytical content."
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
4. Write table wrappers in `report/sections/tables.tex`. Generated `output/tables/*.tex` contains only booktabs `tabular` content; input it directly or use the project's established copy into `report/tables/`.
5. Write figure wrappers in `report/sections/figures.tex`; keep generated image files in `output/figures/` or the established content directory. Wrappers are authored during drafting, never by estimation scripts.
6. State the data period, units, currency, sources, assumptions, and limitations where the reader needs them.
7. Compile and inspect the final PDF, not just the source.

For a short exercise, a single `report/main.tex` is enough. Do not create a complex section hierarchy merely to satisfy a template.

## Tables and figures

- Use `booktabs` with `\toprule`, `\midrule`, and `\bottomrule`; do not use `\hline`.
- Keep substantial `tabular` and TikZ content in separate files loaded with `\input{}`.
- Align numeric columns and make units explicit in headers or notes.
- Give tables and figures informative captions and labels. Notes should explain definitions, sources, and sample periods needed to interpret the exhibit.
- Do not manually retype generated results into a wrapper when a reproducible input path is available.
- Content files contain no floats, captions, labels, font-size commands, footnotes, minipages, or notes. Captions, descriptions, source notes, and significance explanations belong in section wrappers. Place a caption followed by a `{\footnotesize ...}` description and the content input there.

## Match the deliverable

Use a short analytical note for a focused calculation, an appendix for methods and sensitivity, and an executive summary for decisions and exceptions. Explain unfamiliar metrics at first use; do not impose journal submission conventions on a credit memo, budget report, or investment committee pack. Preserve the requested language. The bundled compiler uses pdfLaTeX; for Chinese text use a suitable XeLaTeX/LuaLaTeX setup with CJK fonts and the project's build command rather than sending it through that helper.

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
