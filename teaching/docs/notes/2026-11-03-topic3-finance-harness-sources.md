# Topic 3 finance-harness claims: source checks

Checked 3 November 2026 to inform the lecture structure. These checks support
specific teaching claims; they are not a literature review or a compliance
opinion. Source dates are separate from the course's financial-data cutoff.

Local lookup: `/kbase/topecon.db` was unavailable. The Zotero/SQLite wrapper
returned no DFAH match; direct Zotero searches for all four supplied arXiv IDs
returned no matches in Top.Economics, Working.Papers, or the personal library.
The sources below were therefore checked externally, using primary sources.

## Replay, authority, and interacting agents

| Supplied claim | Check and teaching decision |
|---|---|
| DFAH establishes that smaller schema-first agents replay better than larger free-form agents | **Narrow the claim.** The current version is v4, revised 21 October 2026. Its descriptive synthetic experiments separate decision agreement from tool-path agreement; model, prompt, provider, and runtime factors vary together. The paper explicitly does not identify their separate causal effects. Teach the comparison dimensions and preserved evidence, not a general model-size result. |
| Determinism/capability tension does not occur in coding | **Remove the categorical contrast.** Build and test reproducibility also matter in software. Finance adds the specific authority, exposure, evidence, and accountability needs illustrated in this course. |
| Agent inference should be separate from financial authority | **Supported as an architecture proposal.** AIS validates identity, mandate, policy, state, approvals, and economic intent outside the inference layer. Its reported attacks are synthetic evaluation fixtures, not proof of production safety. Human policy ownership remains necessary. |
| Permissioned ledgers can bind decisions to evidence | **Supported as a proposed approach.** The DLT paper describes permissioned audit trails. A ledger is optional in this course; an auditable record does not require teaching blockchain. |
| Agents can pass local controls while causing collective harm | **Supported as a research problem.** ARIA proposes population-level governance and illustrates it with simulations, explicitly without a production-effectiveness claim. Use a labelled portfolio-exposure example to motivate a system-level check. |

Primary papers:

- [DFAH v4](https://arxiv.org/html/2601.15322v4), especially sections 3, 5.4–5.5 and 6.3.
- [Authority-Inference Separation](https://arxiv.org/abs/2608.30519).
- [Compliant AI Infrastructure for Regulated Finance](https://arxiv.org/abs/2609.27632).
- [Compliant with Local Controls, Collectively Discriminatory](https://arxiv.org/abs/2609.27994).

Lecture rule: distinguish audit reconstruction, reproducible calculations and
control transitions, and a fresh model rerun. Retain the actual evidence and
observable actions. Neither identical wording nor matching hashes establishes
financial correctness. Replay must not repeat real payments or orders.

## Benchmark evidence

[Vals Finance Agent v2.1](https://www.vals.ai/benchmarks/fabv2-1), updated
29 October 2026, reports a leading score of 67.85%. Its primary metric gives
severity-weighted partial credit, subject to mandatory checks; all-pass is a
separate metric. Consequently, 100 minus the headline score is not the share of
analyst tasks that fail, much less a production failure probability.

Vals explicitly states that v2.1 scores are not comparable with v2 because
questions, rubrics, the grading jury, and hedged-answer treatment changed.
Do not draw a clean May-to-October improvement line across versions. The
[archived v2 methodology](https://www.vals.ai/benchmarks/fabv2) documents the
tool harness and evaluation conditions. The lesson is to evaluate the whole
configured workflow under stated criteria, with consequences determining
escalation. The lecture does not need a live model leaderboard.

## Supervision and accountability

**FINRA:** The [2026 Annual Regulatory Oversight Report](https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf)
was published in December 2025. Pages 24–27 discuss technology-neutral
obligations, supervision, and agent-specific considerations. Page 27 identifies
system access/data handling, human oversight, action/decision tracking, and
behavioral controls. Use these as the concrete supervisory questions on page 31
of the lecture. Distinguish the report's considerations from binding rules and
avoid claiming that the report mandates this particular QT architecture.

**US bank model risk:** [SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm)
and [OCC Bulletin 2026-13](https://occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html)
were issued 17 April 2026 and replace the earlier guidance. Generative and
agentic AI are excluded from their scope. Footnote 3 of the
[joint guidance](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf)
nevertheless points institutions to their broader risk-management and governance
practices for excluded tools and systems. The bulletin announced plans for an
RFI. This check does not establish the RFI's current publication status or that
it will settle accountability. Do not teach either “no applicable governance”
or “the RFI will decide who is accountable.”

**Changing systems:** The [current supervisory guidance](https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm)
includes ongoing model monitoring, responses to deterioration, and controls
through the lifecycle. “Traditional model risk management validates once and
then deploys forever” is inaccurate. The teaching problem is the frequency,
composition, and scope of agent-workflow changes, including prompts, tools,
models, retrieved data, permissions, and policy versions.

**Other jurisdictions:** Keep comparisons in instructor notes rather than add
a regulatory survey to the 60-page deck.

- [IMDA's agentic-AI framework announcement](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/new-model-ai-governance-framework-for-agentic-ai), 22 January 2026, emphasizes human accountability and technical/non-technical measures. It is a governance framework, not a universal legal mandate.
- [MAS SAFR](https://www.mas.gov.sg/publications/monographs-or-information-paper/2026/safeguards-for-agentic-finance-at-runtime), 3 July 2026, is a directly relevant finance example addressing action authorization, human oversight, and decision records.
- [European Commission AI Act timeline](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) confirms a 2 August 2026 milestone with exceptions and later high-risk deadlines. Do not imply all requirements began on that date.
- [PRA SS1/23, April 2026 version](https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2026/liaf0126app5.pdf) is a banking model-risk reference. Applicability depends on the institution and use case.

## Payments as a short authority example

The [official AP2 v0.2 specification](https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/specification.md)
describes direct and autonomous modes. In the latter, a user approves
constraints, the agent signs a transaction-specific mandate, and verifying
parties check the mandate chain. This is a useful example of separately
authorized, bounded action. Signed intent does not by itself prove delivery,
correctness of the financial decision, or compliance with every applicable rule.

[Mastercard's Verifiable Intent announcement](https://www.mastercard.com/us/en/news-and-trends/stories/2026/verifiable-intent.html),
5 March 2026, describes evidence linking identity, intent, and action; the
announcement's integration plans should not be reported as universal rollout.
[Visa's BILL/Billtrust announcement](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.22856.html),
20 October 2026, describes a live pilot for approved invoice payments using
agent identity and tokenized credentials. Label it as a pilot. Protocols differ
in scope; avoid claiming all implement identical caps, merchant restrictions,
or human-approval policies.

Use AP2 for one diagram, with the other two as short parallels. No payment
integration or cryptography implementation is required by the QT teaching task.

## Tools for the self-improvement stage

Added after the user's direction to integrate all practice into the same task
and include concrete self-improving-system tools. The current proposal assigns
pages 45–56 to this stage, without standalone lab or break pages.

- [promptfoo configuration](https://www.promptfoo.dev/docs/configuration/guide/)
  compares prompts over test cases;
  [Python assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/python/)
  provide custom checks. The lesson uses timing and evidence checks on the same
  QT failure. An evaluator must check meaning where presence/schema checks are
  insufficient.
- [DSPy GEPA documentation](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/diving-deeper/gepa-in-depth.md)
  describes an optimizer that proposes instructions using feedback. Teach one
  candidate and its evaluation record. A callable-program adapter, development
  cases, and a metric are needed; held-out evaluation and adoption remain
  separate decisions.
- [MLflow Prompt Registry](https://www.mlflow.org/docs/latest/genai/prompt-registry/)
  supports prompt versions, aliases, and lineage.
  [Trace evaluation](https://www.mlflow.org/docs/latest/genai/eval-monitor/running-evaluation/traces/)
  can score retained execution records. Use it as a counterpart to QT's local
  prompt registry, not an assertion that an alias change proves approval.

These are documented external capabilities. They have not been installed,
integrated into QT, or benchmarked in this task. QT's existing internal
`evo-prepare`, `evo-evaluate`, `evo-adopt`, and `evo-rollback` actions remain the
classroom implementation. Public workflow commands remain `/qt:start` and
`/qt:evo`. No claimed improvement should be shown without actual retained
comparison outputs.

## Claims left out pending better evidence

- The claimed March 2026 FINRA prompt-injection publication was not located in
  the targeted primary-source searches. Teach the illustrated trust-boundary
  failure without that date-specific attribution.
- The specific Aaron Linsky quotation was found in secondary reporting, not
  verified against a first-person source. Do not put it on a slide as a direct
  quotation. The security topic is already supported by FINRA's discussion of
  sensitive data and agent authority.
- No source checked here supports a universal requirement that every agent
  reproduce the exact original token sequence, or that this classroom plugin
  is production-ready or compliant in any jurisdiction.
