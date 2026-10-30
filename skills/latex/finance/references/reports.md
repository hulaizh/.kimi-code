# Finance reports

Use this guide for analytical notes, company briefs, investment memos, portfolio and risk reports, and recurring briefing documents.

## Report structure

Scale the structure to the assignment. A short note may need only four sections; a longer report can use the full sequence.

1. **Executive summary:** answer the question and state the main evidence.
2. **Question and scope:** identify the entity, portfolio, period, audience, and comparison basis.
3. **Data and assumptions:** explain sources, sample dates, units, currency, adjustments, and important assumptions.
4. **Analysis:** present calculations, tables, figures, and interpretation in a logical order.
5. **Findings:** state what the analysis supports and how it relates to the audience's decision.
6. **Risks and limitations:** identify data gaps, model limits, uncertainty, and alternative explanations.
7. **Appendix:** include definitions, additional exhibits, and reproducibility details when needed.

Do not fill a section with generic prose to match the template. Remove optional sections that the task does not need.

## Professional finance conventions

- Put the report date and data-as-of date near the title.
- Use consistent names for companies, portfolios, benchmarks, and metrics.
- Define return, margin, growth, valuation, factor, and risk measures when definitions could differ.
- Distinguish reported values, calculated results, estimates, and scenarios.
- State currency and units once per exhibit where possible.
- Use percentage points for differences between percentages and basis points where that convention aids comparison.
- Keep sources and notes with the exhibit or statement they support.
- Do not include invented compliance language. Add internal-use or confidentiality labels only when the user requests them.

## Tables

Use `booktabs`. Author wrappers in `report/sections/tables.tex`, included from `report/main.tex`. Generated `output/tables/*.tex` contains only `\begin{tabular}...\end{tabular}` with booktabs: no float, caption, label, font sizing, minipage, footnote, or notes. Scripts generate content only. Captions, descriptions, sources, and significance explanations belong in the wrapper.

```latex
\begin{table}[htbp]
  \centering
  \caption{Peer valuation comparison}
  \label{tab:peer-valuation}
  {\footnotesize Multiples use the supplied fiscal-year estimates.
  Source: supplied peer data; replace with the actual cutoff.\par}
  \input{../output/tables/peer_comparison}
\end{table}
```

Use actual dates and definitions from the project. Keep numeric precision consistent and align decimal values where practical.

## Figures

Author wrappers in `report/sections/figures.tex` for the float, caption, label, and notes. Reference `../output/figures/` when compiling from `report/`, or the project's established content path. Keep axis labels in the figure and its caption/description in the wrapper.

Compile from `report/` so these relative paths resolve. If the project uses a different build directory, follow that convention and verify every input path. Do not put a wrapper and the content it inputs at the same path.

## Routine deliverables

| Deliverable | Main exhibits | Essential distinction |
|---|---|---|
| Management report | Budget/actual variances and business-unit totals | Revenue versus expense sign conventions |
| Treasury note | Opening cash, receipts, payments, closing cash | Actuals versus forecasts and scenarios |
| Credit memo | Debt schedule, ratios, covenant headroom | Contractual definitions versus generic ratios |
| Operations report | Matched transactions and unresolved exceptions | Timing differences versus confirmed errors |

Lead with the finding and requested decision. Explain unfamiliar metrics briefly, and put detailed methods or sensitivity checks in an appendix when needed. Journal-style validators and journal conversion utilities under `draft/` are legacy optional tools, not acceptance criteria for these reports. Do not run the legacy wrapper generator; write wrappers during drafting.

Captions should state what the reader needs to interpret the exhibit. Avoid repeating the entire analysis in the caption.

## Length and layout

For ordinary student reports, A4 paper, 11 or 12 point type, one-inch margins, and modest line spacing are readable defaults. Follow assignment requirements when supplied. Do not shrink fonts or margins to hide excess length; shorten the content or move supporting material to an appendix.

## Final review

- Compile from a clean enough state to catch missing files and stale references.
- Inspect the PDF page by page.
- Check title date, reporting period, table units, figure legends, and source notes.
- Confirm that every cross-reference resolves and every exhibit is discussed in the text.
- Reconcile narrative values with the generated exhibits.
- Remove placeholder text and optional sections that were not used.
