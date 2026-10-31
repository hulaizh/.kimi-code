# Finance memo guidance

Use a short A4 memo for a focused finance question. The reader should identify
the question, source and date, main result, supporting exhibit, and limitation
without reading a long methods section.

## Layout

The single [template](../assets/report_template.tex) follows the research memo
displayed in Lecture 1: sans-serif text, a blue title/team block, a full-width
finding, narrative on the left, compact key data and a chart on the right, and
preparer/coverage/source notes below. The lecture PDF used US Letter; this template
adapts that layout to the requested A4 size. It does not reuse the lecture's
company figures, institution name, or student labels.

Replace the header macros and bracketed prompts with actual report content.
Keep the question, comparison basis, units, dates, findings, and limitations clear.
Use the report date separately from the data cutoff. Omit unused sections rather
than inventing analysis or filling the memo with generic prose.

## Finance conventions

- Keep company, portfolio, and metric names consistent.
- Define growth, margin, return, valuation, and risk measures when their meaning
  could vary.
- State currency, units, period, and data-as-of date near each exhibit.
- Use percentage points for differences between percentages.
- Separate reported facts, calculated results, assumptions, estimates, scenarios,
  and interpretation.
- Keep source locators with the claim or exhibit they support.
- Do not imply a recommendation or causal result unless the supplied evidence
  supports it.

## Tables and figures

Generated `output/tables/*.tex` files contain only `tabular` content with
`\toprule`, `\midrule`, and `\bottomrule`. Captions, labels, notes, and source
descriptions belong in authored files under `report/sections/`. Generated figures
belong under `output/figures/` and should have readable axes, units, dates, and
honest scales. The sidebar wrappers must be non-floating because they are included
inside a minipage. For a table wrapper in `report/sections/tables.tex`:

```latex
\captionof{table}{Key data}\label{tab:key-data}
{\footnotesize State the actual units, periods, and source.\par}
\input{../output/tables/key_data.tex}
```

Use `\captionof{figure}` and `\includegraphics[width=\linewidth]{...}` for the chart
wrapper. The sidebar is about 6.2 cm wide: prepare charts for that display width
with legible final labels, rather than scaling a large figure down indiscriminately.
A wide table belongs in a full-width section outside the sidebar; do
not squeeze it until labels are unreadable. Keep longer prose in normal page
flow rather than an overfull minipage. Preserve an existing report's layout when
the request is only a correction.

## Compilation

From the project root, substitute the installed skill directory:

```sh
python3 <latex-skill-dir>/scripts/compile_pdf.py report/main.tex
python3 <latex-skill-dir>/scripts/compile_pdf.py report/main.tex --engine xelatex
```

The helper compiles in the source file's directory so exhibit paths resolve.
For Chinese, set `\ChineseMemotrue` in the same template and translate its labels;
XeLaTeX loads the bundled Fandol fonts. Do not send Chinese text to pdfLaTeX.

## Final pass

Compile from `report/`, inspect every page, remove placeholders, and compare all
displayed values with the checked outputs. State any check that remains incomplete.
