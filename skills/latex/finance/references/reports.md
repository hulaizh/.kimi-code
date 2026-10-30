# Student finance reports

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

Use `booktabs`. A typical wrapper in `report/tables/` contains the float, caption, label, notes, and an `\input{}` for generated tabular content.

```latex
\begin{table}[htbp]
  \centering
  \caption{Peer valuation comparison}
  \label{tab:peer-valuation}
  \input{tables/peer_comparison}
  \begin{minipage}{0.95\linewidth}
    \footnotesize Notes: Multiples use the supplied fiscal-year estimates.\\
    Source: User-supplied peer data; data as of 30 September 2026.
  \end{minipage}
\end{table}
```

Use actual dates and definitions from the project. Keep numeric precision consistent and align decimal values where practical.

## Figures

Use a wrapper in `report/figures/` for the float, caption, label, and notes. Reference a local copied figure or the project's established path to `output/figures/`; do not create a second unrelated set of figure files.

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
