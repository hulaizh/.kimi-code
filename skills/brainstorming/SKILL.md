---
name: brainstorming
description: "Turn an underspecified idea into an implementable design. Use when the objective, inputs, deliverable, method, or acceptance checks need clarification, or when comparing approaches before building. Covers analyses, models, reports, applications, and recurring workflows. Do not invoke for an explicit, bounded task whose requirements are already clear."
---

# Brainstorming ideas into designs

Turn ideas into small, testable designs through collaborative dialogue. The goal is not paperwork; it is to expose the finance and implementation assumptions that determine whether the result answers the right question.

## Process

1. **Explore the current context.** Inspect relevant files, data descriptions, documents, and project conventions. Do not change them during brainstorming.
2. **Frame the task.** Identify the finance question, intended audience, available inputs, expected outputs, constraints, and how the user will judge success.
3. **Ask material questions one at a time.** Prefer concrete choices. Skip questions that do not change the design; a small classroom exercise should not face an enterprise requirements interview.
4. **Compare approaches when a real choice exists.** Present two or three approaches with trade-offs and a recommendation. For a straightforward task, one well-explained approach is enough.
5. **Present a brief design.** Cover the components, data flow, finance assumptions, error handling, outputs, and verification at a level matched to the task.
6. **Resolve consequential ambiguity.** Ask before choosing between materially different objectives. When implementation is already requested and the requirements are clear, state reasonable assumptions and proceed; do not create an extra approval gate.
7. **Carry the approved design into implementation.** Use the project's planning conventions. Do not create commits, plan documents, or additional scaffolding unless the user asks for them or project instructions require them.

## Task brief

Keep the brief conversational or use these headings when they add clarity:

- **Question:** What finance problem are we answering?
- **Audience:** Student demonstration, investment committee, analyst, portfolio manager, risk team, or another reader?
- **Inputs:** Files, data fields, sources, dates, and user-supplied assumptions.
- **Output:** Table, figure, memo, report, slides, dashboard, script, or workflow.
- **Method:** Transformations, calculations, models, and alternatives considered.
- **Checks:** Reconciliations, tests, human review, and known limitations.

Do not force the user to supply information that can be inspected locally. Do not invent missing market data or finance facts. Synthetic data is appropriate for an explicitly requested demonstration; label it and keep it separate from observed data.

## Calibrate the explanation

Infer familiarity from the request rather than asking for a degree or job title. For a first exercise, define the key terms and include one hand-checkable example. For an analytical task, explain method choices and sensitivity checks. For a decision brief, lead with the decision, alternatives, business impact, and limitations; put implementation details after them. Keep the same verification standard in all three cases.

## Routine workflows

| Task | Smallest useful design | Acceptance check |
|---|---|---|
| Budget versus actual | Align accounts and periods, calculate variances, explain major drivers | Detail reconciles to totals; cost and revenue sign conventions are explicit |
| Cash forecast | Opening balance, dated receipts/payments, closing balance, scenarios | Opening cash plus net flows equals closing cash; assumptions stay distinct from actuals |
| Credit review | Borrower figures, debt schedule, covenant definitions, exceptions | Ratios use the supplied covenant terms; missing inputs never imply a pass |
| Portfolio report | Holdings, prices, benchmark, returns, commentary | Weights and contributions reconcile; dates, fees, and cash flows are defined |
| Reconciliation | Two ledgers, matching keys, timing differences, exceptions | Matched and unmatched records account for both source totals |

For a recurring run, specify its input cutoff, unique run identifier, retained last successful output, failure state, and reviewer. Introduce scheduling or orchestration only when recurrence is requested.

## Match the workflow size

### Small interactive task

Use for a market snapshot, portfolio summary, company brief, peer table, or short memo. Define the input and output, use the simplest method, and verify the result directly.

### Short-running workflow

Use for stock screening, earnings takeaways, portfolio comparison, factor summaries, or analyst-style report support. Specify the ordered steps, intermediate artifacts, tool calls, and final output so another student can reproduce the run.

### Long-running workflow

Use for recurring portfolio reports, watchlist monitoring, earnings monitoring, or briefing packs. Discuss decomposition, checkpoints, handoffs, run state, quality gates, failure recovery, and review ownership. Start with the smallest useful workflow; orchestration is not a goal in itself.

## Finance design checks

Raise only the checks relevant to the question:

- Source, retrieval date, data-as-of date, and whether the data is real or illustrative.
- Units, currency, percentage conventions, frequency, calendar, and time zone.
- Price adjustment, corporate actions, delisting, missing values, and outliers.
- Look-ahead and survivorship risks when constructing historical investment analyses.
- Formula definitions for returns, volatility, drawdown, ratios, factors, and attribution.
- Reconciliation of displayed numbers with source data or generated result files.
- Separation of observed facts, calculated results, assumptions, and interpretation.
- Human review before an output informs a real financial decision.

## Design principles

- Keep components small enough for students to explain and test independently.
- Prefer the simplest approach that produces an auditable answer.
- Make generated and student-edited files clearly distinct.
- Treat errors, missing data, and stale data as expected cases.
- Revisit the design when new evidence changes the finance question or constraints.
