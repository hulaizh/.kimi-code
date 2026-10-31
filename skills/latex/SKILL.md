---
name: latex
description: "Create, format, compile, and inspect concise A4 finance PDF reports and analytical memos. Use for company briefs, peer comparisons, portfolio notes, risk summaries, management reports, and report layout fixes. Keeps generated tables and figures separate from authored captions and notes."
---

# Finance PDF reports

Use this skill for a practical finance memo or short analytical report. The
default deliverable is a readable A4 PDF built from the bundled memo template.

## Workflow

1. Read the task, project instructions, source notes, and checked outputs.
2. Copy [the report template](finance/assets/report_template.tex) to `report/main.tex`
   when starting a new report. Preserve an existing report structure when the
   user asks for a layout fix.
3. State the question, audience, date or cutoff, units, sources, assumptions,
   findings, limitations, and verification status.
4. Keep generated table content in `output/tables/` and generated figures in
   `output/figures/`. Author captions, labels, descriptions, and source notes in
   `report/sections/`.
5. Use the project's build command, or the [compiler helper](scripts/compile_pdf.py),
   then inspect every PDF page. See [the memo guide](finance/references/reports.md)
   for exhibit placement and the Chinese build route.

## Memo structure

The template reproduces the research-memo layout shown in Lecture 1 on A4:
a dated title and team block, a prominent finding, narrative on the left,
key data and a chart on the right, and source/check notes below. Replace all
bracketed fields with supported content and the user's actual team details.
Keep the memo concise without cutting necessary qualifications or shrinking text.

## Exhibits

Generated table files contain only a booktabs `tabular`. Generated figure files
contain the chart or image. Wrappers in `report/sections/` own captions, labels,
source notes, and descriptions. The template's sidebar uses non-floating wrappers
with `\captionof{table}` or `\captionof{figure}`; ordinary floats cannot go inside
its minipages. Do not put captions or notes in generated content files.

Use actual source dates, units, currencies, and definitions. Distinguish reported
values, calculations, assumptions, estimates, scenarios, and judgments. Never
invent missing data or a source note.

## Checks

- compile successfully and resolve missing inputs;
- inspect the PDF page by page for clipping, overflow, and unreadable exhibits;
- reconcile narrative numbers with the table and figure;
- check units, dates, denominators, and source locators;
- record incomplete checks instead of implying they passed.

## Chinese reports

Use the same template: change `\ChineseMemofalse` to `\ChineseMemotrue`, translate
the labels, and compile with the helper's `--engine xelatex` option. It uses bundled
CJK fonts. For an existing report, preserve its working font and build settings.
