# Finance memo guidance

Use a short A4 memo for a focused finance question. The reader should identify
the question, source and date, main result, supporting exhibit, and limitation
without reading a long methods section.

## Recommended order

1. **Question:** entity or portfolio, period, audience, and comparison basis.
2. **Inputs:** source, retrieval date, units, currency, definitions, and assumptions.
3. **Result:** the main number or decision-relevant finding.
4. **Evidence:** a table, chart, calculation, or source passage.
5. **Checks:** independent arithmetic, source tie-out, or reconciliation.
6. **Limits:** missing data, mismatched periods, model assumptions, and uncertainty.

Use the bundled `report_template.tex` as the starting point. Remove optional
sections rather than filling them with generic prose.

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
honest scales.

## Final pass

Compile from `report/`, inspect every page, remove placeholders, and compare all
displayed values with the checked outputs. State any check that remains incomplete.
