# Topic 3 structure review by Pi / Gemini 4 Argon

Historical review record: after these reviews, the user removed standalone
break pages and the separate lab, retaining a 60-page task-centered lecture.
The current proposal distributes participation through the QT workflow and
expands self-improvement to include QT tools, promptfoo, DSPy/GEPA, and MLflow.
That later reallocation supersedes the lab recommendations and page numbers
below; it has not been resubmitted to Pi.

Requested by the user on 3 November 2026. Reviewer: local Pi CLI, provider
`google`, model `gemini-4-argon`. First completed review used high reasoning.
The raw response is preserved in
`../../logs/topic-3/structure-review/gemini-first-review.txt` (gitignored).

The reviewer identified five issues in the first 60-page proposal:

1. Finance failures arrived after the abstractions and one market-gate page was
   overloaded.
2. Audit replay was confused with single-run verification; candidate revision
   and stopping received too little space.
3. The page/time table had a section-boundary error; the demo and lab were too
   crowded.
4. Product and acceptance lost tangible deliverables and clear ownership.
5. The production boundary needed explicit human authority and fill
   reconciliation.

The revised plan addresses these issues with separate product/acceptance pages,
early finance examples, three distinct replay tests, explicit code/agent/human
roles, separate repair/memory/stopping pages, prepared demos, five lab instruction
pages, and a restored capital handoff.

The review is advice, not an authority for factual claims. We did not adopt its
suggested universal A-share lot and price-limit values, its alternate terminal
enum, or its implied claim that deterministic gates alone establish correctness.
The accompanying source note checks the user's later industry comments.

A follow-up review of the revised structure and source qualifications completed
through Pi with `--thinking max`, provider `google`, and model
`gemini-4-argon`. The returned message confirms that provider/model identity and
a normal stop. Raw output is in
`../../logs/topic-3/structure-review/gemini-followup.jsonl`; the extracted review
is in `../../logs/topic-3/structure-review/gemini-followup-review.md`.

Its verdict was **conditionally ready, with targeted page-level adjustments**.
The revised proposal incorporates these recommendations without changing the
60-page or 240-minute totals:

- Start replay with one historical record; map reconstruction, deterministic
  checks, and fresh model comparisons explicitly to the demonstration.
- Allocate five minutes to the audit exercise and reduce domain switching by
  introducing scoped authority through the quant case's paid-data request.
- Keep AP2 as one short parallel and move Mastercard/Visa to speaker notes.
- Separate artifact validation from proof of live specialist dispatch, and
  distinguish local evolution mechanics from pre-collected model evaluations.
- Use one standard freshness lab; keep other options for fast finishers or
  post-class work. Source-local tests avoid plugin installation during the lab.
- Explicitly distinguish controller verdicts, workflow-version approval, and
  authority to deploy capital.

We checked the recommendations against `scripts/check.py`,
`runtime/quant_cn/orchestrator.py`, `runtime/quant_cn/evolution.py`, and the hook
exercise README. Three corrections to the reviewer were necessary:

1. Page 23 already deferred Kimi event/return-code details; it now points to
   page 40 explicitly to prevent misreading.
2. `/qt:start` with an existing case resumes or reuses recorded state; a fresh
   model evaluation needs a separate case. The review's proposed
   `accepted_for_research` enum is not an implementation identifier.
3. The sample hook records Bash-call metadata, not full specialist dispatch or
   response provenance. Live-team evidence must come from suitable host records.

This was a lecture-design review. It does not certify legal compliance, model
quality, or live runtime behavior. Rehearsed demonstrations remain preparation
tasks for the eventual slide edit. The previously proposed separate freshness
exercise was superseded by the user's subsequent task-centered direction.
