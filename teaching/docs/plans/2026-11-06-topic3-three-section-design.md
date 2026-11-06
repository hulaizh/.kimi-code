# Topic 3: 58-page design and production plan

Status: revised and ready for generation, 6 November 2026. The user accepts
50–60 pages and has confirmed **broad evolution principles**. They authorize
parallel slide generation, humanize, proofreading, a further proofread in the
existing left Pi session, a Gemini-4-Argon review through Pi, and revision.

Current-page references use the 50-page English PDF at commit `7e125eb`.
This plan supersedes the earlier 50-page proposal in this file.

## Fixed design decisions

- Page 2 reuses Topic 2 page 2, with a box highlighting the upper harness/loop/graph area.
- Page 4 shows the complete operating architecture inside **one enclosing
  Evolution box**. It contains no separate diagnosis/proposal/evaluation workflow.
- Pages 5–6 develop the four stakeholder needs carefully; page 7 synthesizes the
  financial system requirements with primary-source support.
- Section 2.1 introduces Orchestrator–Generator–Critic immediately: what, why,
  contracts and authority, then the harness around each role.
- PIT and momentum are QT-specific data/calculation examples. They belong to
  the case on pages 40–41. Harness design teaches the general mechanism that
  attaches such domain checks, rather than teaching those checks as its essence.
- Evolution covers prompts/context, skills, tools/code and role/workflow
  structure. The prompt-only QT implementation is a concrete case, not the
  definition or limit of evolution.
- Page 36 closes Section 2 by repeating the exact page-4 architecture. The
  detailed evolution workflow belongs on page 31.
- Preserve all current substantive materials, worked examples, source links,
  commands, caveats and eight participation points. Rewriting and redrawing are
  allowed; hiding distinct content in notes is not the preservation strategy.
- Work on the English deck in this task, retaining the recent division-of-labor edits.

## Allocation

| Part | Pages | Count |
|---|---:|---:|
| Title and engineering ladder | 1–2 | 2 |
| 1. Introduction | 3–8 | 6 |
| 2. Design roadmap | 9 | 1 |
| 2.1 Harness | 10–18 | 9 |
| 2.2 Loop | 19–24 | 6 |
| 2.3 Graph | 25–29 | 5 |
| 2.4 Evolution | 30–35 | 6 |
| Whole-architecture recap | 36 | 1 |
| 3. Case roadmap | 37 | 1 |
| 3.1 Build | 38–49 | 12 |
| 3.2 Evolve | 50–57 | 8 |
| Final system review | 58 | 1 |
| Total | 1–58 | 58 |

Keep the user's opening positions. Section 1 starts on page 3; its orientation
can be carried on page 2. Section roadmaps are pages 9 and 37. Mark subsection
starts without adding full-page dividers. Page 36 remains the final design page.

## Page-4 / page-36 architecture specification

Retain the recognizable geometry of the existing complete architecture:
Orchestrator above, Generator and Critic teams below, executable checks and
evidence handoffs, structured repair packet, shared state and evidence. Draw
one outer rectangle labelled **Evolution** around the complete system.
The enclosing box denotes the scope of future evaluated changes. It does not
mean the system can rewrite its own mandate or permission limits during a run.
Human policy/approval authority stays explicit at the system boundary.

Do not draw evolution as a second chain under the operating system on these
two overview pages. Use the SAME figure file on pages 4 and 36. The latter
can add a short identification exercise or four small callouts without
changing the diagram's layout.

Page 31 separately expands the evolution process: recorded failures →
diagnosis → scoped Generator-team proposal → fixed evaluations and fresh
Critic-team review → owner approval/rejection/deferral → versioned deployment
and rollback. Existing cases remain bound to their starting configuration.

## Finance opening: teaching argument

The three pages should establish **consequences → operational demands →
engineering requirements**, rather than list generic software virtues.

**Page 5: Consequences and Accountability.** Preserve the auditor/risk-manager
split. A financial recommendation or action can affect money, customer treatment
or institutional obligations. The auditor asks what evidence and configuration
actually produced a decision. The risk manager asks whether the action is
authorized and within limits. Separate evidence supporting a conclusion from
permission to act. Keep named responsibility. JSON/Git are implementation
examples later; Git authorship alone does not establish action approval.

**Page 6: Reliability Through Time and Change.** Preserve the operations/system-
owner split. Operations needs verified progress, reconciliation of uncertain
actions and safe recovery after failures. The owner needs evidence about
behavior under changed prompts, tools, models and dependencies. Distinguish
recomputing financial numbers, reconstructing the actual recorded run and
testing a fresh model run. Identical model wording is not a universal target.
Common providers and interacting components make end-to-end behavior relevant,
beyond the quality of an isolated response.

**Page 7: From Requirements to Design.** Use a compact six-row exhibit:

| Requirement | What the financial system must demonstrate | Design connection |
|---|---|---|
| Reliability | Critical constraints hold; failed checks stop advancement | Executable gates and evidence-based review |
| Reproducibility / auditability | Recompute results and reconstruct actual decisions | Frozen inputs, versions and retained traces |
| Bounded authority | Actions stay within mandate and approvals | Permissions, controller and accountable owner |
| Operational resilience | Recover without repeating uncertain consequential actions | Checkpoints, reconciliation and bounded retries |
| Confidentiality | Sensitive data stays within authorized paths | Access and tool boundaries |
| Governed change | New versions preserve controls and improve tested behavior | Evaluation, independent review, versions and rollback |

Shared exposures and third-party dependencies motivate system-level checks and
monitoring on pages 6, 28 and 35. Reliability also matters in other consequential
domains: the contrast is with low-stakes draft assistance, not all nonfinancial
software. The degree of control depends on the specific financial use case.

Primary support: [FSB final AI sound practices, 15 October 2026](https://www.fsb.org/uploads/P151026-1.pdf),
especially its agentic-AI controls, oversight, recovery and lifecycle discussion;
[MAS SAFR v1.1, 9 October 2026](https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf),
especially pages 4–8 on consequential actions and runtime authority; and the
existing [FINRA 2026 report](https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf),
printed pages 24–27. These sources support the concerns. The specific O–G–C
architecture is our design choice, not a regulatory prescription.
See the companion source note for checked claims and limits.

## O–G–C: what and why

| Role | Responsibility | Output | Authority boundary |
|---|---|---|---|
| Orchestrator | Bind the task, delegate, collect evidence and route the run | Requests, state transitions and next-step decision | Controller code validates transitions; no role silently expands policy |
| Generator | Propose, implement and test a candidate | Candidate artifact, tests, evidence and limitations | Cannot certify its own work as finally accepted |
| Critic | Challenge claims against evidence using the fixed criteria | Findings, evidence, verified resolutions and verdict | Cannot rewrite the candidate or weaken acceptance criteria |

The purpose is separation of production, challenge and process control. Separate
contexts can improve the opportunity to catch errors but do not guarantee
independent mistakes or correctness. Code gates and human accountability remain.
An orchestrator is a role implemented by agent coordination plus controller
code; it need not mean a third unconstrained LLM verdict.

The pattern combines delegation and evaluator/reviser ideas documented by
[Anthropic](https://www.anthropic.com/research/building-effective-agents).
Use it when decomposition and independent checking add value. Do not imply
three roles are universally optimal or that increasing agent count proves quality.

## Full page design

| Page | Proposed title | Content and visible evidence | Current material |
|---:|---|---|---|
| 1 | Title | Existing lecture title and course identity. | 1 |
| 2 | The Engineering Ladder | Reuse Topic 2 p2; outline the upper harness/loop/graph region and label it This Lecture. | Topic 2 p2 |
| 3 | Building the Agentic Quant System | Task, deliverables and acceptance: trace, reproduce, resume and restore. | 2 + 4 |
| 4 | The Complete Architecture | Show the operating O–G–C architecture inside ONE enclosing Evolution box; no detailed evolution workflow here. | 30; new enclosure |
| 5 | Finance: Consequences and Accountability | Auditor and risk manager: consequential decisions, reconstructible evidence, authority, limits and named responsibility. | 6 + 27; strengthened sources |
| 6 | Finance: Reliability Through Time and Change | Operations and system owner: interruptions, reproducible calculations, retained execution records, controlled changes and shared dependencies. | 6; strengthened sources |
| 7 | Finance: From Requirements to Design | Synthesize reliability, reproducibility/auditability, bounded authority, resilience, confidentiality and governed change into system requirements. | New evidence-based synthesis |
| 8 | Division of Labor | Preserve the human judgment/capital-decision diagram and the model/code/human boundary. | 3 |
| 9 | Design Roadmap | Harness, Loop, Graph, Evolution; locate the current section. | Navigation |
| 10 | The Orchestrator–Generator–Critic Design | What each role does: coordinate/control, produce/test, independently challenge. Introduce the complete three-role pattern immediately. | 13 + 18 + 30 |
| 11 | Why Separate the Three Roles? | Avoid producer self-certification; distinguish evidence review from workflow control; preserve fresh contexts and acknowledge correlated errors. | 12 + 13; new explanation |
| 12 | Role Contracts and Authority | Table of each role's inputs, outputs and permitted changes. Controller code validates transitions; critics return findings; only authorized actors change policy. | New explicit contract |
| 13 | Inside Each Role's Harness | Context/instructions, tools, state/memory and output checks surround each role; a harness is more than three role prompts. | 8 |
| 14 | Task and Artifact Contracts | Mandate, completion/failure conditions and typed evidence-bearing outputs; keep the current research request's scope and restrictions. | 9; new contract exhibit |
| 15 | Permissions and Untrusted Inputs | Host-enforced access; retrieved text is data. Retain the paid-data/AP2 example and supplier, purpose, budget, expiry and approval checks. | 25 + 26 |
| 16 | Hooks, Gates and Validation | Event-triggered observation, host-supported blocking and mandatory controller gates. | 20 |
| 17 | State and Checkpoints | Case/request/candidate/version IDs, role/round/budget/deadline, artifact hashes, open findings and verified completion. | 22 |
| 18 | Evidence and Audit Records | Link dated inputs, calculations, findings, routes and approvals; retain observable execution evidence rather than reconstructed model stories. | 24 |
| 19 | Loop: Act, Observe, Decide | Tool-result feedback, bounded continuation and failed-call handling. | 11 |
| 20 | Loop: Generate, Check, Critique | Research revision loop; retain the missing-cost example and separate-context limitations; keep mandate and criteria fixed. | 12 + 18 |
| 21 | Loop: Findings and Verified Repairs | Same-close timing exercise, pit-001 ledger, carried findings and evidence-based closure. | 17; exercise |
| 22 | Loop: Acceptance and Completion | Checks, closed findings and QT's same-candidate/two-clean-full-review rule; distinguish task completion from profitable returns. | Acceptance part of 19 |
| 23 | Loop: Budgets and Terminal Outcomes | Revise only with progress and budget; distinguish rejection, blocking, exhaustion, stalling and user stop. | Stop-rule part of 19 |
| 24 | Loop: Recovery and Safe Retry | Check actual completion, repair role submissions, investigate changed evidence and reconcile uncertain side effects before retrying. | 23 + recovery aspects of 37 |
| 25 | Graph: Dependencies and Handoffs | Task nodes, prerequisites, success/failure edges and feedback cycles; avoid calling the complete cyclic workflow a DAG. | 14 |
| 26 | Graph: Artifact Contracts and Shared State | Request/candidate IDs, statuses, paths/hashes and findings cross edges; workers return artifacts and the controller owns control state. | 22/35/36; new focused exhibit |
| 27 | Graph: Teams, Fan-Out and Joins | Detailed Generator data/features/backtest and Critic PIT/robustness/execution teams; complete reports, evidence checks and joins. | 15 + 30 |
| 28 | Graph: Combined Results and Shared Limits | Retain the two-proposal aggregate-risk example and the fixture's missing portfolio-wide control. | 16 |
| 29 | Graph: Conditional Routing and Recovery | Show wait, repair, continue and terminal branches; route from validated status and invalidate dependent work when inputs change. | 14/23/35/37; new focused exhibit |
| 30 | Evolution: What Can Change? | Broad principles: prompts/context, skills, tools/code and role/workflow structure; distinguish candidate revision from reusable-system change. | 28 + expanded scope |
| 31 | Evolution: The Detailed Improvement System | HERE expand diagnosis, Generator change proposal, evaluation, fresh Critic review, owner decision, version adoption and rollback. | 29; expanded O–G–C outer workflow |
| 32 | Evolution: Evidence and Evaluation | Failure cases, baseline, fixed criteria, development feedback and held-out assessment; preserve timing, source support and authorization criteria. | 39 + evaluation half of 40 |
| 33 | Evolution: Regression and Independent Review | Software tests versus model-behavior comparisons; test scope, permissions and existing behavior. Proposals cannot quietly weaken their own acceptance standard. | Regression half of 40 |
| 34 | Evolution: Versions, Approval and Rollback | Bind tested configuration and evidence; approve changes for new runs; retain prior versions and keep in-flight cases pinned. | 44 + 45 principles |
| 35 | Evolution: Monitoring and Change Triggers | Monitor later runs and dependency changes; collect recurring failures; update future systems through evaluated changes. | 46 |
| 36 | The Complete Architecture: Putting It Together | Repeat the SAME overview as p4, with the SAME enclosing Evolution box. Identify harness, loops, graph and evolution now that students know the parts. | 4 repeated; section synthesis |
| 37 | Case Roadmap: Build and Evolve | The same QT system; two public workflow entry points. | Navigation |
| 38 | Build: Package and Entry Points | Plugin files, installation/reinstall/reload, /qt:start, /qt:evo and workspace .qt/ separation. | 32 |
| 39 | Build: Leads and Specialists | Role-card and specialist allowlist construction; verify actual host dispatch rather than inferring teams from files. | 33 |
| 40 | Build: Point-in-Time Inputs | The original release/restatement timeline; explain availability and information sets as QT's domain contract. | 7; moved out of Harness |
| 41 | Build: Verified Numerical Tools | Original momentum formula, 21 prices, 12/10-1=20%, stable ranking; short code/tool contract and known-answer test. | 10; moved out of Harness |
| 42 | Build: The Orchestrator and Gates | Request/manifest, numerical checks, fresh reviews and controller-owned transitions; show a short real-code excerpt and test. | 13 + 35; construction view |
| 43 | Build: Register and Inspect a Hook | Original hook manifest, deduplication, incomplete coverage and Kimi timeout/error behavior. | 34 |
| 44 | Build: Run One Research Case | /qt:start and retained request, reports, numerical evidence and route; label scripted versus live execution. | 35 |
| 45 | Build: Repair a Rejected Submission | Missing specialist/stale ID in a disposable case; verify hashes and keep sealed evidence intact. | 36; exercise |
| 46 | Build: Replay, Audit and Resume | Original reconstruction questions, frozen numerical replay, separate model runs, pending-step resume and fresh-case rules. | 24 + 37; exercise |
| 47 | Build: Production Data and Adapters | Licensed dated data, historical universe/suspensions/delistings, board/date rules and fees, host isolation and tested adapters. | 47 |
| 48 | Build: Research Validation | Future-price perturbation, restatements, cost stress and walk-forward checks; passing does not establish excess returns. | 48 |
| 49 | Build: Capital Authority and Reconciliation | Draft/reviewed/reconciled; positions, shared limits, approval expiry, fills and accountable capital decisions. | 49 |
| 50 | Evolve: Capture the Failure | /qt:evo and evo-prepare; evidence-bound case, parent version, required behavior and separate evaluation cases. | Capture part of 39 |
| 51 | Evolve: Propose One Prompt Change | Original timing diff and missing-evidence instruction; explain why it addresses the failure; state this is one concrete example of broad evolution. | Diff part of 39; exercise |
| 52 | Evolve: Compare Outputs with promptfoo | Original dates, PRICE_01/MISSING_02, config and companion checks; verify semantic timing and evidence. | 41; exercise |
| 53 | Evolve: Generate Candidates with DSPy/GEPA | Callable program, development cases, metric, feedback and search budget; preserve external-extension status. | 42 |
| 54 | Evolve: Judge the Evidence | Original timing-pass/evidence-fail comparison; repair and independently check before adoption. | 43; exercise |
| 55 | Evolve: Record the Tested Version | QT prompt registry and MLflow counterpart; model/tools/policy/data versions and separate approval record. | 44 |
| 56 | Evolve: Approve or Reject Adoption | evo-evaluate, AWAITING_APPROVAL, explicit evo-adopt; examine actual behavioral comparison beyond schema/code checks. | Adoption half of 45; exercise |
| 57 | Evolve: Roll Back and Monitor | Approved evo-rollback, retained versions/evidence, verify a new case and monitor later failures; current cases keep original versions. | Rollback half of 45 + 46 |
| 58 | Review the Completed System | Defend one control against a stakeholder need; show tests, supported conclusions and remaining implementation gaps. | 50 + 4; exercise |

## Preservation map

| Current page(s) | New page(s) |
|---|---|
| 1 | 1 |
| 2, 4 | 3, 58 |
| 3 | 8 |
| 5, 21, 31, 38 | 2, 9, 37 and subsection navigation |
| 6 | 5–6 |
| 7 | 40 |
| 8 | 13 |
| 9 | 14 |
| 10 | 41 |
| 11 | 19 |
| 12, 18 | 10–11, 20 |
| 13 | 10–12, 42 |
| 14 | 25, 29 |
| 15, 30 | 4, 27, 36 |
| 16 | 28 |
| 17 | 21 |
| 19 | 22–23 |
| 20 | 16 |
| 22 | 17 |
| 23 | 24 |
| 24 | 18, 46 |
| 25, 26 | 15 |
| 27 | 5, 7 |
| 28 | 30 |
| 29 | 31 |
| 32 | 38 |
| 33 | 39 |
| 34 | 43 |
| 35 | 42, 44 |
| 36 | 45 |
| 37 | 24, 46 |
| 39 | 32, 50–51 |
| 40 | 32–33, 41, 52 |
| 41 | 52 |
| 42 | 53 |
| 43 | 54 |
| 44 | 34, 55 |
| 45 | 34, 56–57 |
| 46 | 35, 57 |
| 47 | 47 |
| 48 | 48 |
| 49 | 49 |
| 50 | 58 |

Retain the original participation at new pages 21, 45, 46, 51, 52, 54, 56 and 58.
Preserve source links for AP2, FINRA, Kimi hooks, promptfoo, DSPy/GEPA and MLflow.
Keep examples labelled illustrative; retain synthetic-fixture limitations,
missing production adapters, and separate research/version/capital approvals.

## Parallel generation and review

1. Snapshot the current English deck and assets under ignored run logs.
2. Opening/harness author: pages 2–18 and shared overview diagram.
3. Loop/graph/evolution author: pages 19–36; reuse the overview for page 36.
4. Case author: pages 37–58, preserving exact commands and worked numbers.
5. Main agent owns the title/preamble, section assembly, crosswalk, builds and
   integration. Do not alter shared `slides/misc/style.tex`.
6. Generate figures in `figures/`, pure table content in `tables/`, and prose
   in section sources. Keep fonts readable; favor 58 pages over dense compression.
7. Apply humanize, then independent copy editing/proofreading. Verify coverage,
   figures, commands, facts and sources; compile and inspect every PDF page.
8. Send concrete review requests to the existing left Pi session. Request its
   further proofread and a Gemini-4-Argon review through Pi at maximum reasoning.
   Retain the actual returned reviews and provider/model evidence.
9. Fix findings, rebuild, recheck affected pages and run a final whole-deck check.
   Commit source and compiled PDF. Record anything unresolved or unimplemented.

This plan sets broad evolution principles without authorizing automatic changes
to the QT implementation. The existing prompt-evolution case demonstrates one
realizable slice of the broader design.
