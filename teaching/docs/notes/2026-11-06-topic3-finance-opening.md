# Finance opening: source checks and teaching decisions

Checked 6 November 2026 for the Topic 3 redesign. This is focused source checking
for three teaching slides, not a literature review or jurisdictional compliance
assessment.

## Local evidence

Read the existing finance-harness source note, instructor guide, architecture
notes and historical review corrections. The SQLite mirror is available at
`/Users/hulaizh/kbase/topecon.db` although `/kbase/` is absent on this host.
Targeted title searches found no agentic-finance, deterministic-financial-harness
or authority–inference paper. A broader search found related financial-stability
metadata, which is insufficient support for the specific architecture claims.

Zotero searches across the configured libraries for `Agentic Finance` and
`Authority Inference` returned no matches. `Deterministic Financial` returned an
unrelated dividend-signaling paper, which was excluded. The older note's academic
claims should not be expanded on this evidence.

## Primary sources checked

| Source | Relevant support | Teaching limit |
|---|---|---|
| [FSB, final AI sound practices, 15 October 2026](https://www.fsb.org/uploads/P151026-1.pdf), particularly PDF pages 56–58 and the lifecycle/third-party sections | Discusses code-enforced boundaries, human intervention, checking agent accounts against other evidence, safe stopping/recovery, clear responsibility and oversight of delegation. Also addresses changes and dependencies. | Practices are proportionate to use-case risk. They do not prescribe three agents or establish that deterministic controls alone ensure correctness. Use the final report rather than June's consultation. |
| [MAS SAFR v1.1, 9 October 2026](https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf), pages 4–8 and 13 | Connects financial actions to customer/economic consequences, limited reversibility, authority, assessment before execution and an independently retained action record. | An industry reference approach, not a new regulation. It does not require identical LLM output on rerun. The webpage's July date describes the first publication; the PDF contains the October revision. |
| [FINRA 2026 oversight report](https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf), printed pages 24–27 | Supports attention to agent scope, sensitive data, human oversight and recorded actions/decisions. | US broker-dealer context; retain its scope when used for a China-equity classroom case. |
| [FSB, monitoring AI vulnerabilities, October 2025](https://www.fsb.org/2025/10/monitoring-adoption-of-artificial-intelligence-and-related-vulnerabilities-in-the-financial-sector/) | Identifies common providers and correlated behavior as system-level concerns. | Do not equate a portfolio-aggregation teaching example with empirical proof of market-wide instability. |
| [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), section 3 | Reliability, accountability and resilience are relevant across consequential AI applications. | Avoid claiming finance has exclusive requirements or that nonfinancial coding systems do not need reproducibility. |
| [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents), orchestrator/workers and evaluator/optimizer sections | Describes delegation and critique/refinement patterns with explicit conditions for their use. | Our O–G–C arrangement combines these ideas. It is a design choice to assess, not a universal architecture or a guarantee of independent errors. |

## Concrete changes to pages 5–7

Page 5 retains the auditor and risk manager but starts from the consequence of
the decision. Ask what supported it, who permitted the action and who owns an
exception. Source evidence and authority are different objects. A Git author or
timestamp alone does not constitute approval of an action.

Page 6 retains operations and the system owner. Use interruption and later
change to motivate durable state, reconciliation, reproducible calculations and
evaluations tied to a version. Keep the three replay distinctions from the local
instructor notes: recover the actual execution record; recompute frozen numerical
work; evaluate a new model run whose path may differ.

Page 7 maps requirements to mechanisms: reliability → gates and independent
review; reproducibility/auditability → snapshots, versions and retained traces;
authority → permissions and control state; resilience → checkpoint/recovery;
confidentiality → access boundaries; governed change → evaluations and rollback.
This mapping is a teaching synthesis. It is not a quoted regulatory checklist.

PIT restatements, the momentum formula and market execution rules are specific
QT checks and move to the case. The harness provides the general mechanism to
register and enforce those checks. Keeping this distinction makes the design
section transferable to credit, treasury, reporting and other finance systems.

No model leaderboard score, causal claim about model size, universal perfect-
determinism requirement or production-readiness claim is needed for these pages.
