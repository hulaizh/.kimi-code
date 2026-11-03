# Topic 3: proposed 60-page lecture structure

Status: implemented and verified in both language versions, 3 November 2026.
Incorporates the user's direction:
60 pages, no standalone break pages, no separate lab, and explicit tools for
self-improvement. Earlier drafts received two Pi / Gemini 4 Argon reviews;
this later reallocation has not been resubmitted. Both language sources now
follow this map. The subsequent itemize preference replaces explanatory tables
with short bullets; only pages 7, 11, 49, and 52 retain worked comparison tables.

## Purpose and opening language

Build a reusable quant research workflow that produces an evidence-backed
research package. Use one synthetic monthly-momentum case throughout. Finance
stakeholders supply the requirements; engineering terms name the mechanisms
that meet them.

**Product, in words suitable for page 2:**

Given a trading idea and dated data, produce a research package: a precise
strategy, runnable backtest, checked results, independent critique, and a clear
recommendation to accept for research, revise, or stop. Keep the evidence so
another analyst can inspect and continue the work. Classroom data are synthetic.

**Acceptance, in words suitable for page 3:**

- Another analyst can trace the recommendation and reproduce its calculations.
- Missing evidence, failed checks, and unresolved findings prevent acceptance.
- Interrupted work resumes from the last verified step.
- A named person approves material changes; tested versions can be restored.

Research acceptance is separate from authority to deploy capital. An evidenced
rejection satisfies the system's delivery standard while rejecting the candidate:
a working system need not find a profitable strategy. Keep three decisions
distinct: the controller's research verdict, the owner's approval of a workflow
change, and a separately authorized capital action. The latter is outside QT.

Keep product and acceptance on separate pages. Use prose, a sample research
package, and short visual callouts. No code block, JSON, or field-name inventory
in the opening.

## Stakeholder needs that motivate the concepts

These are requirements for the teaching case, not a claim that one legal regime
prescribes every mechanism.

| Stakeholder request | Failure to demonstrate | Mechanism introduced |
|---|---|---|
| Auditor: reconstruct what supported this decision | A later download differs; the original evidence is gone | Retained evidence, trace, replay specification |
| Risk manager: the model cannot grant itself authority | A convincing strategy bypasses a risk limit | Harness, permissions, code-enforced gates, human approval |
| Analyst: check the actual calculation | The agent reports success after a failed tool call | Checked tools and the tool loop |
| Research head: challenge and repair the case | A finding disappears without a fix | Independent critic, revision loop, persistent findings |
| Team lead: all necessary checks must finish | The fastest reply is treated as a complete review | Graph, dependencies, team join, system-level checks |
| Operations: continue safely after interruption | A pending action is repeated or treated as completed | Durable state, reconciliation, controlled retries |
| Supervisor: controls must run at every relevant event | Checks depend on someone remembering to run them | Hooks, mandatory controller gates, monitoring and escalation |
| Accountable owner: improve without weakening controls | A prompt edit changes downstream behavior unexpectedly | Fixed evaluation, version approval, rollback and ongoing monitoring |

Introduce the need before naming its mechanism, usually on the same page or the
preceding page. Avoid a separate numbered “Need” slide for every term. Use the
same case and a few recurring stakeholder questions.

## Replay and determinism: teach the distinction early

Page 6 separates three questions:

1. **Audit reconstruction:** what happened, which evidence was used, which
   version and permissions applied, and who approved the action?
2. **Calculation and control replay:** with frozen inputs, code, configuration,
   and environment, do calculations and control decisions repeat? Specify
   numerical tolerances where relevant.
3. **Model rerun:** does another invocation choose the same tools or conclusion?
   Measure variation; do not promise identical text or paths.

Replay without external effects uses recorded responses or a simulator. It must
not resubmit a payment or order. A hash detects changed content; it does not
establish truth. Repetition does not establish correctness. Separate factual
support, numerical validity, and repeatability.

## Page and time budget

Exactly 60 pages, including title, contents, and conclusion. There are no
break slides and no separate lab section. Breaks remain in the instructor's
240-minute schedule. Practice happens within the same quant-system task.

| Pages | Count | Time | Purpose |
|---|---:|---|---|
| 1–4 | 4 | 00:00–00:15 | Product, acceptance, contents |
| 5–23 | 19 | 00:15–01:20 | Finance needs and the inner architecture |
| — | 0 | 01:20–01:30 | Instructor-scheduled break; no slide |
| 24–35 | 12 | 01:30–02:05 | Recovery, replay, authority, supervision, improvement |
| 36–44 | 9 | 02:05–02:45 | Build, inspect, repair, and replay QT |
| — | 0 | 02:45–02:55 | Instructor-scheduled break; no slide |
| 45–56 | 12 | 02:55–03:45 | Improve the system with concrete tools |
| 57–60 | 4 | 03:45–04:00 | Production boundary and final acceptance |
| Total | 60 | 240 minutes | 220 teaching/practice minutes |

Use two actual sections: **Design the Quant System** and **Build and Improve
the System**. Their major subsections are Controlled Research / Recovery and
Governance, and Run and Verify QT / Improve the System. Manual itemized contents
pages at 4, 23, 36, and 45 highlight the current subsection.
All activities advance one research case and its reusable workflow.
There is no disconnected capstone exercise, lab menu, or new assessment task.
The manually written contents remains after the product and acceptance pages.

## Page map

### Opening

1. **Long-Run Workflows.** Course title.
2. **Product: A Quant Research Package.** Use the plain-language product above and a visual of the delivered research package.
3. **Acceptance: When the Work Is Ready.** Use the four tests above; distinguish a supported rejection from an incomplete run.
4. **Contents: Controlled Research.** Show both sections and their two major subsections in itemize; highlight Controlled Research.

### Design from finance needs: one controlled run

5. **Stakeholders: What They Need.** Auditor, risk manager, operations, and accountable owner ask concrete questions about the momentum case. Bridge from Topic 2: reusable prompts and skills now need control across steps and sessions.
6. **Audit Replay and Determinism.** Start with one historical decision record. Contrast reconstructing that record, repeating its calculation with frozen inputs, and asking the model again. This is a requirements exhibit; persistence is implemented later.
7. **Information Set: What Was Known Then?** Show one release/restatement and observation-to-trade timeline. A later value cannot support an earlier decision. This motivates controlled inputs before naming the harness.
8. **Authority: Suggest, Check, Approve.** Agents propose and challenge; code checks rules and transitions; a named human owns policy. Distinguish a research verdict, approval of a workflow version, and authority to deploy capital. Ask who may change the risk cap. Code enforces only specified, tested rules.
9. **Harness: The Agent's Working Conditions.** Introduce context, tools, authority, evidence, state, and gates as the surrounding system needed to answer pages 5–8. Show one agent with those boundaries.
10. **Harness: One Task Contract.** Show the question, dated inputs, permitted actions, expected output, and escalation condition in ordinary language. Preserve Topic 2's context principles without reteaching skills.
11. **Tools: Reproduce One Calculation.** Work through one signal or cash calculation with fixed inputs and a dated execution rule. Validate inputs and returned evidence. Keep board-specific execution details in the handout; do not imply one rule fits all A-shares.
12. **Tool Loop: Act on the Result.** A failed or incomplete calculation determines the next action. Show plan, call, observe, and stop; a retry needs a reason and a bound.
13. **Review: Independent Challenge.** A plausible result needs financial judgment. Introduce the Critic using a timing or cost defect. Separate context supports challenge but does not eliminate shared model errors. A benchmark motivates verification; it establishes neither a production failure probability nor the benefit of adding a Critic.
14. **Orchestrator: Control the Handoffs.** Separate production, review, and routing. The main agent coordinates; the controller enforces encoded transitions and the human retains policy authority. Review findings cannot silently authorize action.
15. **Graph: Dependencies and Routes.** The backtest needs validated inputs; review needs saved outputs. Introduce nodes, edges, conditional routing, and waiting through this dependency diagram.
16. **Teams: Fan Out and Join.** Decompose only checks needing separate expertise. Use a small parallel Critic-team example; label all six specialist responsibilities in the handout. All required reports must arrive and pass validation before the join.
17. **System Checks: Beyond Each Agent.** Illustrative example: two individually allowed proposals together exceed a shared exposure limit. Check the combined result and shared state. This production extension is not implemented by the classroom research fixture.
18. **Feedback: Evidence and a Repair Criterion.** Show one finding, its artifact, why it matters, and the test that would close it. Avoid a schema dump.
19. **Revision Loop: Repair and Review.** Introduce candidate revision after the concrete defect. The Generator repairs; a fresh review checks changed evidence; the mandate stays fixed.
20. **Finding Memory: Silence Is Not Closure.** Carry one finding through two rounds; closure must cite the repaired version. Show why a fresh agent needs saved issue history.
21. **Stopping: Accept, Revise, or Escalate.** Teach passing checks, unresolved defects, fatal defects, exhaustion, stalled progress, and human stop in plain language. The plugin's two-clean-review rule is a course implementation choice, not a universal assurance standard.
22. **Hooks: Events and Control Boundaries.** Combine automatic event triggering with observation, host-permitted blocking, and controller enforcement. A hook log cannot certify a candidate. Runtime details remain on page 39 and in the handout.
23. **Contents: Recovery and Governance.** Repeat the manual itemized hierarchy and highlight the next major subsection.

### Design the quant system: continuity and governed change

24. **Interruption: What Was Actually Finished?** Operations inherits a stopped case. Contrast completed, pending, and uncertain work; identify what must be saved.
25. **Durable State: Save Verified Progress.** Case identity, pending step, versions, evidence locations, and open findings form a checkpoint. Use a readable state card, not JSON.
26. **Recovery: Reconcile Before Retrying.** Match the pending request; classify transient failure, invalid submission, altered evidence, and uncertain external effects. Explain why retrying must not duplicate an action.
27. **Trace: Explain the Route.** Connect snapshot, tool result, finding, control decision, and approval. Capture observable actions and evidence, not purported hidden reasoning.
28. **Audit Replay: Reconstruct the Case.** Students inspect the current case's evidence and explain its route. Separate reconstructing its history, reproducing a calculation, and invoking the model again.
29. **Scoped Authority: A Mandate to Act.** The research agent requests paid data outside its mandate. Show purpose, amount, recipient, expiry, and approver. AP2 supplies one short parallel; Mastercard and Visa remain in speaker notes. This is a production illustration.
30. **Untrusted Inputs: Protect the Boundary.** A retrieved document asks the agent to upload data. Show restricted tools and escalation. A prompt alone does not enforce host permissions.
31. **Supervision: A Named Owner.** Identify who monitors access, reviews actions, handles exceptions, and can stop the system. FINRA's agent considerations are a US broker-dealer example, with requirements distinguished from guidance and internal policy.
32. **Repeated Failures: Improve the Workflow.** A repaired case does not prevent next month's omission. Introduce evolution through a recorded failure; distinguish prompt improvement from strategy-parameter search.
33. **Change Control: Evaluate, Approve, Monitor.** Fix comparison cases and gates, assess the change, approve a version, and preserve rollback. Model, tool, data, and policy changes also need impact assessment. QT currently versions only the Generator prompt.
34. **Three Loops: Three Different Changes.** Summarize tool execution, candidate repair, and harness improvement after all have been motivated. State what stays fixed in each.
35. **Architecture: Put the Controls Together.** One complete diagram and stakeholder-to-control check. Separate classroom mechanics from production targets such as shared limits and external mandates.

### Build and improve the system: operate the research workflow

36. **Contents: Run and Verify QT.** Start the second section with the manual hierarchy; highlight Run and Verify QT.
37. **Plugin: Files, Commands, and Installation.** Map roles and controls to files, introduce `/qt:start` and `/qt:evo`, and include the install/reload step and package/workspace boundary.
38. **Delegation: Leads and Specialists.** Show one agent profile and distinguish report validation from evidence of actual host dispatch and independent specialist contexts.
39. **Hook: Register and Inspect.** Show the optional logger, one event, relevant failure behavior, and duplicate delivery. Students inspect the record within the ongoing task.
40. **Run: Follow One Research Case.** Inspect a prepared case at selected transitions. Show host evidence for live-team claims or label the scripted rehearsal. A mode label alone is not provenance.
41. **Barriers: What Permits Advancement?** Locate Generator completeness, numerical checks, Critic coverage, and termination evidence.
42. **Repair: Reject Bad Evidence.** Introduce one missing report or stale request. Students identify the failed condition, repair the submitted artifact, and verify the permitted route in the same case.
43. **Replay: Check the Evidence.** Map page 6 to retained state/trace/artifacts, frozen-input numerical checks, and separate model-run records. Demonstrate a numerical replay. A fresh evaluation needs a new case; existing cases resume or reuse state.
44. **Resume: Continue the Pending Step.** Inspect a prepared interruption, verify identity and evidence integrity, and resume without duplicating effects.

### Build and improve the system: make improvement measurable

45. **Contents: Improve the System.** Repeat the manual itemized hierarchy and highlight the improvement subsection. The following pages connect capture, proposal, evaluation, versioning, and restoration to the same failure.
46. **Capture: Turn a Failure into a Test Case.** Use `/qt:evo` and the internal `evo-prepare` action to bind the completed case and parent prompt. Students identify the failing evidence, write the expected behavior, and keep separate development and held-out cases.
47. **Proposal: Change One Instruction.** Inspect a prompt diff addressing the observed timing omission. Students draft one change without changing strategy parameters, risk limits, or acceptance rules. Git records the proposed edit; the running prompt stays unchanged.
48. **Evaluator: Define What Better Means.** Show inputs, expected evidence, observation/trade ordering, allowed actions, and pass criteria. Separate schema validity, factual support, financial correctness, and control failures. Presence of a date field alone is insufficient.
49. **promptfoo: Compare Old and New Outputs.** Use one prepared evaluation configuration and a results matrix. Custom Python checks examine timing and evidence references; reviewed judgments handle claims needing interpretation. Students inspect a remaining failure. This is an external evaluation example, not an existing QT integration.
50. **DSPy/GEPA: Propose Better Prompts.** Explain feedback-driven prompt optimization through one recorded proposal and its evaluation feedback. Show the required callable program, development cases, metric, and search budget. Export a candidate for independent testing; no automatic adoption or risk-rule edits. The adapter is an extension, not bundled QT functionality.
51. **Regression: Preserve Existing Controls.** Run QT's `scripts/check.py` and inspect behavioral regression cases. Missing reports, stale evidence, and invalid permissions must remain blocked. Code tests and model-behavior tests answer different questions.
52. **Comparison: Decide from the Evidence.** Compare baseline/candidate cases, repeated-run variation where relevant, remaining failures, and resource use. A partner checks one claim against the retained output. Reserve final held-out cases from prompt search; a stronger score cannot override a critical control failure.
53. **Versioning: Track the Tested Configuration.** Start with QT's versioned prompt files and active pointer. Show MLflow as a larger-system counterpart for prompt versions, evaluation records, and traces. Capture the model, tool, policy, and data configuration too; an alias by itself is not approval evidence.
54. **Adoption: Promote the Tested Version.** Show `evo-evaluate` reaching `AWAITING_APPROVAL`, then an explicitly approved `evo-adopt`. Students state what evidence justifies adoption or rejection. QT runs code regressions and validates review fields; it does not independently establish the full behavioral comparison's correctness.
55. **Rollback: Restore the Prior Version.** Use authorized `evo-rollback`, inspect the active pointer, and start a separate new case under the restored prompt. Existing case fingerprints do not silently migrate. Preserve both versions and their evidence.
56. **Monitoring: Feed New Failures Back.** Show new failures returning to the case library. Trigger review when data, tools, models, or permissions change. Keep system-wide outcomes and correlated errors visible; improvement is measured under a fixed standard, not guaranteed by the optimizer.

### Complete the same task: production boundary and acceptance

57. **Real Data: Replace the Fixture.** Map synthetic inputs to licensed feeds, dated universe membership, release times, and execution adapters. Mark absent capabilities.
58. **Validation: Challenge the Pipeline.** Demonstrate one temporal-leakage perturbation from page 7. Name cost stress and walk-forward testing as further requirements without turning this into a backtesting lecture.
59. **Capital: From Suggestions to Fills.** Show portfolio constraints, execution approval, positions, expiry, and reconciliation. Research acceptance does not authorize orders. Identify the accountable owner across component/vendor boundaries.
60. **Product Review: Defend the Completed System.** Return to page 3: evidence, unresolved findings, recovery, approved change, and rollback. Students defend one mechanism through the stakeholder need. Distinguish implemented controls, measured behavior, and remaining limitations.

## Pacing and participation within the task

The previously separate 35-minute lab is redistributed across the actual
workflow. There is no new exercise brief, separate deliverable, or lab section.

| Point in the task | Student action | Minutes already included in block |
|---|---|---:|
| Pages 18–20 | Write a repair criterion for the current case's finding | 5 |
| Page 28 | Reconstruct the case's decision from saved evidence | 5 |
| Page 42 | Repair a blocked submission and verify the next route | 7 |
| Pages 46–47 | Turn the observed failure into a case and draft one prompt edit | 6 |
| Pages 49–52 | Compare recorded outputs and check a partner's claim | 8 |
| Page 54 | Defend adoption or rejection of that edit | 4 |
| Total | Distributed participation in the same task | 35 |

- **First architecture block, 65 minutes:** pages 5–8, 15 minutes; 9–12,
  12 minutes; 13–17, 17 minutes; 18–21, 15 minutes including the repair
  discussion; 22–23, 6 minutes.
- **Continuity and change, 35 minutes:** pages 24–28, 17 minutes including
  the five-minute audit activity; 29–31, 8 minutes; 32–35, 10 minutes.
- **QT workflow, 40 minutes:** pages 36–39, 10 minutes; 40–41,
  10 minutes; 42, 7 minutes; 43–44, 10 minutes; 3 minutes contingency.
- **Self-improvement, 50 minutes:** pages 45–47, 12 minutes; 48–52,
  20 minutes; 53–56, 15 minutes; 3 minutes contingency. Student participation
  above is included, not added to these times.
- **Production boundary and product review, 15 minutes:** pages 57–59,
  10 minutes; page 60, 5 minutes.

Rehearse the workflow before class and prepare actual evidence for each stopping
point. Install required tools and collect model comparisons beforehand.
Present external optimization and tracking tools through a small prepared
example of the same defect; do not spend class time installing three frameworks.
Use recorded, labelled outputs when live latency would consume practice time.
Do not invent an optimizer result or call a scripted report a live model run.

## Self-improvement tool map

| Need in the task | Tool and slide | Input → retained output | Status |
|---|---|---|---|
| Preserve the incident and baseline | QT `evo-prepare`, page 46 | Completed case and parent prompt → bound change request | Existing QT tool |
| Propose a reviewable change | Generator team and Git diff, page 47 | Failure and fixed mandate → one proposed prompt edit | Existing workflow; Git supplies edit history |
| Compare behavior | promptfoo and Python assertions, page 49 | Prompts, cases, provider, checks → output/check comparison | External example; QT adapter not implemented |
| Search prompt improvements | DSPy/GEPA, page 50 | Callable program, development cases, metric/feedback → candidate prompt | External extension; requires adapter and separate held-out evaluation |
| Prevent controller regressions | QT `scripts/check.py`, page 51 | Edited source and fixtures → test results | Existing code checks; not semantic evaluation |
| Connect versions to evidence | QT registry; MLflow counterpart, page 53 | Prompt versions, run configuration, evaluations → version/trace record | QT exists; MLflow integration is an extension |
| Validate and approve adoption | QT `evo-evaluate`, `evo-adopt`, page 54 | Proposal, reviews, regressions, explicit approval → selected version | Existing QT tools, with stated semantic-validation limits |
| Restore the earlier behavior | QT `evo-rollback`, page 55 | Approval and retained prior version → restored active pointer | Existing QT tool; verify in a new case |

Only `/qt:start` and `/qt:evo` are public workflow commands. The Python
actions above explain what the system does internally; they are not new student
slash commands.

Sources checked for the external-tool examples:
[promptfoo configuration](https://www.promptfoo.dev/docs/configuration/guide/),
[Python assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/python/),
[DSPy GEPA documentation](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/diving-deeper/gepa-in-depth.md),
[MLflow Prompt Registry](https://www.mlflow.org/docs/latest/genai/prompt-registry/),
and [MLflow trace evaluation](https://www.mlflow.org/docs/latest/genai/eval-monitor/running-evaluation/traces/).
These support capability descriptions, not a claim that they are already
connected to QT or that using them guarantees better financial decisions.

## Material to merge or relocate

| Previous material | Treatment |
|---|---|
| Two standalone break pages | Removed; breaks appear only in the instructor schedule |
| Separate lab section and freshness exercise | Removed; students act on the same case throughout the build |
| Lab brief, option menu, submission rubric, partner-replay pages | Replaced by case capture, evaluation, optimization, versioning, and monitoring content |
| Repeated architecture stages and coverage checks | Initial harness, handoff graph, final architecture; reuse the same case |
| Full hook inventory, six specialist descriptions, and manifest schemas | Selected exhibit on screen; remaining details in the handout |
| Extensive market-rule and regulatory comparisons | One calculation, one timing example, a short production boundary, and sourced notes |
| Generic self-evolution claims | Named tools, concrete inputs/outputs, independent evaluation, approval, and rollback |

Each page carries one decision or teaching point. Use short itemized lists for
explanations and retain diagrams where they explain process or dependencies.
Tables are reserved for worked data, calculations, and output comparisons.
Detailed page notes are author instructions, not slide-body text. Keep product
and acceptance in plain words; do not squeeze more text into each slide.

## Review and factual controls

Earlier Pi reviews improved finance motivation, the replay distinction,
candidate revision, demo provenance, and pacing. The user's later task-centered
direction supersedes the standalone-lab recommendation. The raw reviews describe
the earlier page map; their page numbers should not be read as current.

The industry-comments source check remains in
`../notes/2026-11-03-topic3-finance-harness-sources.md`. Preserve these limits:

- Distinguish audit reconstruction, calculation replay, and new model runs.
  Existing QT cases resume or return their recorded terminal result.
- Report-file validation and the sample Bash-event logger do not establish full
  live-team provenance.
- DFAH does not establish a general causal advantage for smaller models.
- Benchmark scores are not production failure rates; Vals versions differ.
- SR 26-2 excludes agentic AI from its scope without removing broader governance.
- Existing model risk management includes monitoring and change control.
- Payment protocols and aggregate-risk controls are production illustrations.
- Prompt search uses development feedback; final evaluation remains separate.
  Model weights, risk limits, and strategy parameters do not evolve through QT's
  Generator-prompt interface.

This 60-page map has been applied in English and Chinese. Rebuild and validate
both PDFs after changes, then inspect every page. The instructor guide and
manually written comparison fixtures accompany the revised decks.
