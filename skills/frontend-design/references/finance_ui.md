# Finance interface patterns

## Operating finance views

- **Budget versus actual:** period and business-unit filters, totals, variance amount and percentage, and drill-down to accounts. Label expense overruns as unfavorable even when numerically positive. A zero budget produces n/a percentage variance.
- **Cash forecast:** opening balance, receipts, payments, closing balance, and separately labeled scenario controls. Recompute the cash identity when assumptions change; keep actuals fixed.
- **Credit review:** borrower, statement period, ratio definitions, covenant thresholds, headroom, and source detail. Undefined inputs produce an unresolved state, never a passing badge.
- **Reconciliation queue:** matched/unmatched counts and amounts, exception reasons, duplicate-key visibility, and downloadable filtered records. Filtered totals must match the rows shown; retain a separate full-source total.

Use local sanitized fixtures for demonstrations. Avoid displaying personal account identifiers or credentials. A browser refresh failure must remain visible rather than substituting plausible values.

Use this guide for dashboards, screeners, monitoring tools, and report-support interfaces. Choose only the pattern that matches the user's task.

## Information hierarchy

A finance interface should let the reader answer these questions in order:

1. What am I looking at?
2. What period and units does it cover?
3. What changed or deserves attention?
4. What explains the change?
5. Where did the numbers come from, and what are their limitations?

Do not give every metric the same visual weight. Lead with the measures needed for the task and move definitions or detailed tables into supporting views.

## Common layouts

### Market snapshot

Use a compact header for the as-of time and data state, a small set of headline measures, one or two comparison charts, and a detailed table. Separate previous close, intraday, and delayed data. Do not label a snapshot "live" unless the feed actually supports it.

### Company or earnings view

Lead with the reporting period and the key reported measures. Show actual versus comparison-period values, then drivers, segment detail, and valuation or peer context. Distinguish reported figures, calculated figures, and estimates. Keep earnings per share, margins, and growth rates in consistent units.

### Stock screener

Make filter definitions visible and reproducible. Show how many securities passed, the universe and as-of date, and the fields used in ranking. A score should expose its components rather than appear as an unexplained black box. Handle missing values explicitly instead of treating them as zero.

### Portfolio view

Separate allocation, performance, and risk. State the base currency, valuation date, benchmark, and whether positions are long, short, leveraged, or netted. Reconcile weights and attribution totals. A high-level performance number should be traceable to positions or result files.

### Risk view

Lead with the risk measure and horizon, then exposures, concentration, scenarios, and changes since the previous run. Label historical simulation, parametric estimates, stress scenarios, and user-defined shocks as different kinds of information. Do not use a reassuring green state when data is missing or stale.

### Recurring monitor

Show the last successful run, latest attempted run, data freshness, and failed or skipped items. Preserve the previous successful result when a refresh fails, but mark it stale rather than presenting it as current. Provide a compact run summary before detailed logs.

## Data states

Design these states before styling the ideal case:

- **Loading:** explain what is loading without flashing fabricated values.
- **Empty:** distinguish no rows from no matching filters.
- **Partial:** identify missing fields or entities and keep their cells distinct from zero.
- **Stale:** show the last successful timestamp and a visible warning.
- **Error:** describe the failed step in plain language and preserve a path to retry or inspect details.
- **Demo:** label illustrative data globally and near exported figures where appropriate.

## Numbers and tables

- Use tabular numerals and right-align numeric columns.
- Keep decimal precision consistent within a column.
- Show currency and units in the header rather than repeating symbols in every cell when possible.
- Distinguish `8%`, `8 percentage points`, and `8 bp`.
- Use an em dash or `n/a` for unavailable values according to project style, with a note explaining missing data.
- Support sorting and filtering with real state and visible active criteria.
- Preserve the user's filter context when moving between summary and detail.

## Charts in web interfaces

Static chart generation belongs to the `plot` skill, but a web interface may render interactive charts itself. Keep the same finance discipline: labeled axes, aligned periods, explicit units, honest baselines, and source context. Provide tooltips as supplements, not as the only way to read essential values.

Avoid dual axes unless the relationship is central and the different units are unmistakable. Do not animate values in a way that suggests live updates when only the view changed.

## Visual design

Use a deliberate visual concept without sacrificing data legibility. Editorial typography, strong grids, restrained terminal motifs, or industrial density can all work. Financial data benefits from precise spacing and alignment more than from glass effects or dramatic gradients.

Use color consistently:

- One accent for selection or navigation.
- A small categorical palette for series.
- Semantic colors for positive, negative, warning, and unavailable states.
- Text, icons, or patterns alongside color so meaning survives color-vision differences.

## Verification checklist

Exercise the interface with realistic and problematic data:

1. Reconcile headline values and table totals with the input data.
2. Test every visible control and link.
3. Test loading, empty, partial, stale, and error states.
4. Test long company names, large values, negative values, and missing values.
5. Navigate by keyboard and inspect focus states.
6. Inspect narrow and wide viewports.
7. Confirm that demo data cannot be mistaken for current market data.
8. Run the project's build and browser checks.
