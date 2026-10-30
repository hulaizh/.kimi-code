---
name: brainstorming
description: "Clarify requirements and design before creative or build work. Use for analyses, applications, dashboards, models, reports, presentations, new features, and workflows when a request needs scoping, approach comparison, or validation planning. Define objectives, inputs, outputs, assumptions, implementation steps, and checks before substantial work begins."
---

# Brainstorming ideas into designs

Turn ideas into small, testable designs through collaborative dialogue. The goal is not paperwork; it is to expose the finance and implementation assumptions that determine whether the result answers the right question.

## Process

1. **Explore the current context.** Inspect relevant files, data descriptions, documents, and project conventions. Do not change them during brainstorming.
2. **Frame the task.** Identify the finance question, intended audience, available inputs, expected outputs, constraints, and how the user will judge success.
3. **Ask material questions one at a time.** Prefer concrete choices. Skip questions that do not change the design; a small classroom exercise should not face an enterprise requirements interview.
4. **Compare approaches when a real choice exists.** Present two or three approaches with trade-offs and a recommendation. For a straightforward task, one well-explained approach is enough.
5. **Present a brief design.** Cover the components, data flow, finance assumptions, error handling, outputs, and verification at a level matched to the task.
6. **Get approval for substantial work.** For a new project, multi-step workflow, or behavior change, wait for approval before implementation. For a small explicit action request, a short statement of assumptions is enough when no material ambiguity remains.
7. **Carry the approved design into implementation.** Use the project's planning conventions. Do not create commits, plan documents, or additional scaffolding unless the user asks for them or project instructions require them.

## Task brief

Keep the brief conversational or use these headings when they add clarity:

- **Question:** What finance problem are we answering?
- **Audience:** Student demonstration, investment committee, analyst, portfolio manager, risk team, or another reader?
- **Inputs:** Files, data fields, sources, dates, and user-supplied assumptions.
- **Output:** Table, figure, memo, report, slides, dashboard, script, or workflow.
- **Method:** Transformations, calculations, models, and alternatives considered.
- **Checks:** Reconciliations, tests, human review, and known limitations.

Do not force the user to supply information that can be inspected locally. Do not invent missing market data or finance facts. If illustrative data would help, ask whether it is acceptable and label it clearly.

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
