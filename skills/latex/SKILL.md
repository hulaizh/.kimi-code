---
name: latex
description: "Create, format, compile, and inspect concise A4 finance PDF reports and analytical memos. Use for company briefs, peer comparisons, portfolio notes, risk summaries, management reports, and report layout fixes. Keeps generated tables and figures separate from authored captions and notes."
---

# Finance PDF reports

Use this skill for a practical finance memo or short analytical report. The
default deliverable is a readable A4 PDF built from the bundled memo template.

## Workflow

1. Read the task, project instructions, source notes, and checked outputs.
2. Copy `finance/assets/report_template.tex` to the project's `report/main.tex`
   when starting a new report. Preserve an existing report structure when the
   user asks for a layout fix.
3. State the question, audience, date or cutoff, units, sources, assumptions,
   findings, limitations, and verification status.
4. Keep generated table content in `output/tables/` and generated figures in
   `output/figures/`. Author captions, labels, descriptions, and source notes in
   `report/sections/`.
5. Compile from the `report/` directory with `latexmk -pdf -halt-on-error
   main.tex`, then inspect every PDF page.

## Memo structure

The bundled template uses the course memo layout: title and report/data dates;
`Question`; `Inputs`; `Result`; tables and figures; `Checks`; and `Limits`.
Remove sections that do not help the decision. Lead with the finding and keep
technical detail close to the number it explains.

## Exhibits

Generated table files contain only a booktabs `tabular`. Generated figure files
contain the chart or image. Wrappers in `report/sections/` own captions, labels,
source notes, and descriptions. Do not put floats or captions in generated
content files.

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

Use the project's XeLaTeX setup and available CJK fonts for Chinese text. Keep
the same memo structure and evidence requirements.
