# Topic 3: proposed 60-page lecture structure

Status: reviewed discussion draft. Incorporates the user's finance-harness
comments and two reviews through Pi's Gemini 4 Argon. Slide sources are unchanged.

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

Exactly 60 pages, including title, contents, two breaks, lab, and debrief.
Four hours means 240 elapsed minutes, including 20 minutes of breaks.

| Pages | Count | Time | Purpose |
|---|---:|---|---|
| 1–4 | 4 | 00:00–00:15 | Product, acceptance, contents |
| 5–23 | 19 | 00:15–01:20 | Finance needs and the inner architecture |
| 24 | 1 | 01:20–01:30 | Break |
| 25–36 | 12 | 01:30–02:05 | Recovery, replay, authority, supervision, improvement |
| 37–45 | 9 | 02:05–02:45 | Inspect and operate QT |
| 46 | 1 | 02:45–02:55 | Break |
| 47–54 | 8 | 02:55–03:20 | Evolution demonstration and production boundary |
| 55–59 | 5 | 03:20–03:55 | Student lab, mostly independent work |
| 60 | 1 | 03:55–04:00 | Debrief |
| Total | 60 | 240 minutes | 220 minutes excluding breaks |

Keep three actual sections: **Design from Finance Needs**, **Build and Evolve
QT**, and **Integrated Lab**. Blocks below are planning groupings, not extra
sections or repeated roadmaps. Manual contents follow the product and acceptance
pages. No separate reference appendix or timetable slide.

## Page map

### Opening

1. **Long-Run Workflows.** Course title.
2. **Product: A Quant Research Package.** Use the plain-language product above and a visual of the delivered research package.
3. **Acceptance: When the Work Is Ready.** Use the four tests above; distinguish a supported rejection from an incomplete run.
4. **Contents.** The three sections only.

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
22. **Hooks: Automatic Event Checks.** A supervisor needs checks and records at every relevant boundary. Introduce a hook after the controller: an event triggers a script, such as logging a completed call.
23. **Hooks: Observe, Block, and Enforce.** Distinguish observation, host-permitted blocking, and controller enforcement. Critical acceptance remains in the controller. All Kimi event names, return codes, and timeouts are deferred to page 40 and the handout.

24. **Break: Ten Minutes.**

### Design from finance needs: continuity and governed change

25. **Interruption: What Was Actually Finished?** Operations inherits a stopped case. Contrast completed, pending, and uncertain work; identify what must be saved.
26. **Durable State: Save Verified Progress.** Case identity, pending step, versions, evidence locations, and open findings form a checkpoint. Use a readable state card, not JSON.
27. **Recovery: Reconcile Before Retrying.** Match the pending request; classify transient failure, invalid submission, altered evidence, and uncertain external effects. Demonstrate why retrying must not duplicate an action.
28. **Trace: Explain the Route.** Connect source snapshot, tool result, finding, control decision, and approval in one record. Capture observable actions and evidence; do not claim access to hidden model reasoning.
29. **Audit Exercise: Reconstruct One Decision.** Students identify evidence needed to explain a stopped case. Separate replaying saved numerical inputs from a fresh model call. Return to page 6's questions.
30. **Scoped Authority: A Mandate to Act.** Start with the research agent requesting paid data outside its mandate. Show approved purpose, amount, recipient, expiry, and approver. AP2 supplies one short payment parallel; Mastercard and Visa stay in speaker notes. This is a production illustration, not a QT capability.
31. **Untrusted Inputs: Protect the Boundary.** A retrieved document tells the agent to upload data. Show trust boundaries, restricted tools, and escalation. A prompt alone does not enforce host permissions.
32. **Supervision: A Named Owner.** Who monitors access, reviews actions, handles exceptions, and can stop the system? Use FINRA's agent considerations as a US broker-dealer example. Distinguish applicable requirements, supervisory considerations, and internal policy; international comparisons stay in notes.
33. **Repeated Failures: Improve the Workflow.** A case repair does not prevent next month's omission. Introduce evolution through a recorded, reproducible failure. Separate changing a prompt from searching strategy parameters.
34. **Change Control: Evaluate, Approve, Monitor.** Fix comparison cases and gates; evaluate the new version, obtain approval, retain rollback, and monitor after adoption. Model, tool, data, and policy changes also need impact assessment. QT versions only the Generator prompt.
35. **Three Loops: Three Different Changes.** Summarize tool execution, candidate repair, and harness improvement after all three have been motivated. Show what stays fixed in each.
36. **Architecture: Put the Controls Together.** One complete diagram and stakeholder-to-control check. Distinguish classroom mechanics from production targets such as shared limits and external mandates.

### Build and evolve QT: inspect a working case

37. **Plugin: Files and Two Commands.** Map roles and controls to commands, skills, agents, scripts, hooks, and workspace state. Introduce `/qt:start` and `/qt:evo` here.
38. **Delegation: Leads and Specialists.** One native agent profile and its permissions. Controller validation of report files does not prove separate agents ran; corroborate with host dispatch and response records. The sample Bash-event hook does not capture complete specialist provenance.
39. **Installation: Source and Runtime.** One install/reload path and the package/workspace boundary. Installation is pre-class preparation; this is a quick orientation.
40. **Hook: Register and Inspect.** Show the optional logger and one event; explain relevant failure behavior. Demonstrate duplicate delivery from a prepared fixture. Full setup and event inventory stay in the handout.
41. **Run: Follow One Research Case.** Inspect a prepared case at selected transitions. Show host dispatch evidence for live-team claims, or label the scripted rehearsal. A mode label alone does not prove live execution. Do not budget for an unbounded full model run.
42. **Barriers: What Permits Advancement?** Locate Generator completeness, numerical checks, Critic coverage, and termination evidence.
43. **Fault Injection: Reject Bad Evidence.** Introduce one missing specialist or stale request and inspect the blocked transition. Run one repair; other failure cases stay in the handout.
44. **Replay: Check the Evidence.** Map page 6 to three evidence rows: state/trace/artifacts for reconstruction, frozen-input numerical checks for calculation replay, and separate model-run records for behavioral comparison. Demonstrate the numerical check. A fresh evaluation needs a new case; starting an existing case resumes or reuses its state.
45. **Resume: Continue the Pending Step.** Interrupt at a prepared checkpoint, inspect identity and evidence integrity, and resume. Do not repeat completed effects.

46. **Break: Ten Minutes.**

### Build and evolve QT: improve and define the boundary

47. **Evolution: Start from a Recorded Failure.** Show `/qt:evo` and the diagnosis behind one bounded prompt edit. Use a prepared failure with evidence; label any illustrative scenario.
48. **Evaluation: Compare Versions.** Show pre-collected model outputs under fixed cases, criteria, and configuration, including repeated runs where appropriate. QT executes code regressions and validates submitted review fields; it does not independently run and grade this full behavioral comparison. Preserve held-out cases and attempted changes; label absent behavioral evidence as unverified.
49. **Adoption: Approve and Restore.** Inspect diff and evidence, approve a version for future cases, show its pointer, and restore the prior version. Collect model-output comparisons before class.
50. **Real Data: Replace the Fixture.** Map synthetic inputs to licensed feeds, dated universe membership, release times, and execution adapters. Mark absent capabilities.
51. **Validation: Challenge the Pipeline.** One temporal-leakage perturbation connects to page 7. Name cost stress and walk-forward testing as further requirements without a backtesting tutorial.
52. **Capital: From Suggestions to Fills.** Show portfolio constraints, execution approval, current positions, expiry, and fill reconciliation. Classroom acceptance does not authorize orders.
53. **Open Problems: The Whole System.** Discuss shared-model errors, agent interactions, aggregate limits, changing configurations, and responsibility across vendors. Distinguish implemented checks from unresolved assurance.
54. **Handoff: What the Owner Accepts.** Return to page 3: evidence, limits, recovery, accountable approval, and rollback. Introduce the lab as a small repair to one control.

### Integrated lab

55. **Lab: Repair One Control.** State deliverables, rubric, and the pre-provisioned workspace before students start.
56. **Contract: Define the Failure and the Check.** One standard classroom task: timestamp freshness with a prepared defect and starter tests. Fast finishers can add version-bound finding closure. Required-specialist and prompt-evaluation extensions move to the handout for work after class.
57. **Build and Verify.** Leave visible during work: reproduce the defect, edit one component, run source-local failing/passing and integration checks, save diff and evidence. Tests import the edited source directly; no plugin reinstall is needed for this lab. Native Kimi testing later requires reinstall/reload after source edits.
58. **Partner Replay.** Another student re-runs the check from saved evidence and explains why the route passed or blocked.
59. **Submit: Evidence and One Limitation.** One contract, diff, before/after evidence, version identity, and limitation. A documented unresolved result is acceptable; invented success is not.

60. **Debrief: Defend the Design.** Stakeholder request → failure → mechanism → evidence. Defend one control and distinguish replayability from correctness.

## Pacing and preparation

- **First architecture block, 65 minutes:** pages 5–8, 15 minutes; 9–12,
  12 minutes; 13–17, 17 minutes; 18–21, 15 minutes; 22–23, 6 minutes.
- **Continuity and change, 35 minutes:** pages 25–29, 17 minutes including
  a 5-minute exercise on page 29; 30–32, 8 minutes; 33–36, 10 minutes.
- **QT demonstration, 40 minutes:** pages 37–40, 10 minutes; 41–42,
  10 minutes; 43, 7 minutes; 44–45, 10 minutes; 3 minutes contingency.
  Rehearse this path and save a case at every transition before class.
- **Evolution and boundary, 25 minutes:** pages 47–49, 10 minutes;
  50–52, 7 minutes; 53–54, 5 minutes; 3 minutes contingency.
- **Lab, 35 minutes:** brief and choose, 5 minutes; edit/test, 20 minutes;
  partner replay, 7 minutes; submit, 3 minutes. These are persistent work
  instructions, not five mini-lectures.

Before teaching, prepare the standard freshness defect, starter contract/tests,
and instructor answer in an isolated source copy; these new lab materials are
not yet supplied by this structure proposal. Use the package's source-local
test runner for the exercise. Avoid setup and model-call latency during the lab.

Each page carries one exhibit or decision. The detailed notes above instruct the
author; they are not slide-body text. Retain the short body-text convention.
Do not reach 60 pages by squeezing 86 pages into smaller type.

## Material to merge or relocate

| Current material | Treatment |
|---|---|
| Seven architecture stages and repeated coverage checks | Initial harness, handoff graph, final architecture; test understanding with the case |
| Product, scope, authority, acceptance, unsupported-claims openings | Separate plain product and acceptance pages, then stakeholder sequence |
| Hook-event inventory, return codes, installation exercise | Two conceptual pages after control flow; one prepared implementation example; full detail in handout |
| Six specialist descriptions and manifest schemas | Team diagram, then one role profile and actual manifest inspection |
| China-market rule and adapter inventory | One calculation, one timing example, short production boundary; details in instructor materials |
| Public-system comparisons and source-list pages | Sources beside claims; bibliography in notes |
| Candidate-loop summaries | Preserve repair, finding memory, and stopping as distinct beats |
| Eight lab pages in the earlier proposal | Five instruction pages and a protected 27-minute edit/test/partner period |

## Review and factual controls

The initial Pi review identified late finance motivation, overcrowded candidate
revision, ambiguous determinism, an overloaded demo, and lab bloat. This revision
addresses those findings. Do not copy its suggested uniform market-rule values
or renamed terminal enum into the implementation.

The follow-up judged the plan conditionally ready. Its useful remaining changes
are incorporated: one classroom lab track, a more concrete replay exhibit,
theory/demo provenance distinctions, and extra audit-exercise time. The reviewer
misread page 23's deferral of runtime details; the wording now states page 40
explicitly. Its suggestion to treat every `/qt:start` call as a new model run
was rejected after reading the controller: existing cases resume or return
their terminal result. Its `accepted_for_research` label is not a QT enum;
the implementation's actual terminal state remains `ACCEPTED`.

The user's industry comments inform pages 6, 8, 13, 17, 28–34, and 48–53.
Source checks are in `../notes/2026-11-03-topic3-finance-harness-sources.md`:

- DFAH distinguishes replay dimensions; it does not establish that smaller
  models are generally more replayable.
- Benchmark scores are not production failure probabilities. Vals v2 and v2.1
  scores are not directly comparable.
- Generative/agentic AI is outside SR 26-2's scope, not outside governance.
- Existing model risk management includes monitoring and change management.
  Agentic systems intensify that problem; they do not invent it.
- Payment protocols illustrate authority; they are not QT dependencies.
- International examples do not define the legal requirements for the synthetic
  China-equity exercise.

After the structure is settled, apply the same map to English and Chinese,
build and validate both PDFs, and inspect every page. Slide files remain
unchanged during this structure discussion.
