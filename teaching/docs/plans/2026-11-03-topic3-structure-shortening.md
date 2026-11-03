# Topic 3 slide structure: 60-page version

Status: revised draft for discussion and Pi-agent review.

## Teaching spine

The lecture should begin with a finance problem that stakeholders already care
about: an analyst must be able to replay a recurring research decision later,
using the same information set, tools, evidence, and rules. The central need is
**audit replay and determinism**. Harness, loop, graph, hook, durable state,
and evolution are introduced only when that need creates a concrete design
problem.

The running case is a synthetic quant-research workflow. Students follow one
request from idea to candidate strategy, numerical checks, independent review,
repair, terminal decision, and later harness improvement. The deck should use
plain language for the product and acceptance criteria. Avoid code blocks in the
opening; reserve code, file trees, and manifests for the implementation section.

The target is exactly 60 pages in each language, counting the title page,
contents, two break pages, lab instructions, and debrief. This is longer than
the previous 45--50-page proposal so the lecturer can explain each concept
through its finance need without returning to the current 86-page repetition.

## Page and time budget

| Pages | Time | Purpose |
|---:|---|---|
| 1--4 | 00:00--00:15 | Product, stakeholder needs, acceptance, contents |
| 5--22 | 00:15--01:20 | Finance needs that force the inner architecture |
| 23 | 01:20--01:30 | Break |
| 24--34 | 01:30--02:10 | Durable execution, replay, and evolution |
| 35--43 | 02:10--02:45 | Build and run the QT plugin |
| 44 | 02:45--02:55 | Break |
| 45--51 | 02:55--03:20 | Evolve the harness and set the market boundary |
| 52--59 | 03:20--03:55 | Integrated student lab |
| 60 | 03:55--04:00 | Debrief |

The page budget assumes questions, live inspection, and the 35-minute lab. A
page is a teaching beat, not a promise to lecture at the same speed throughout.

## Proposed order

### Opening: product and acceptance in plain words

1. **Title: Long-Run Workflows.** Keep the course title and the Harness--Loop--Graph theme.
2. **Task: Build the quant agent system.** State the student deliverable in ordinary language: a reusable workflow that can research an idea, show its evidence, survive interruption, receive independent challenge, and improve under review.
3. **What stakeholders need.** Use a four-part visual: replay the same case later; know exactly which data and rules were used; identify who may act or approve; and improve the workflow without lowering the standard. Name audit replay and determinism explicitly.
4. **Contents.** Three sections: derive the system from finance needs; build and evolve QT; complete the integrated lab.

The current Product, Scope, Ownership, and Acceptance frames become pages 2--3.
There is no code block, schema dump, or implementation vocabulary in this
opening.

### Section 1: let finance needs force the architecture

Every concept follows the same rhythm: **need → failure without it → concept →
small exhibit → finance consequence**. The lecturer can ask the need question
before revealing the term.

5. **Recurring case: one research request.** Show the monthly momentum question, dated data, backtest, review, and handoff as a single chain.
6. **Need 1: replay the decision.** Ask what must be saved for another analyst to reproduce the same answer six weeks later.
7. **Failure: one agent is fluent but unsupported.** Combine the current one-agent diagram and confident-but-unsupported examples.
8. **Concept: Harness.** In plain words: the harness fixes what the worker may read, use, change, and return.
9. **Harness contract.** Inputs, scoped context, checked tools, output evidence, authority, and stated limitations.
10. **Need 2: deterministic tool use.** A result cannot be replayed if inputs, data vintage, or tool outputs are implicit.
11. **Concept: Tool loop.** Plan, act, observe; validate before and after each call; stop on a valid artifact, hard error, or budget cap.
12. **Need 3: automatic checks at boundaries.** Humans cannot remember every pre-call, post-call, or session event in a long run.
13. **Concept: Hook.** A hook runs a declared script at a lifecycle event; it records or blocks only within the event's authority.
14. **Hook limits.** One comparison of blockable events, logging-only events, timeouts, parallel delivery, and the controller's responsibility.
15. **Need 4: independent challenge.** The producer cannot certify its own evidence; self-agreement is not review.
16. **Concepts: Critic and Orchestrator.** The Generator proposes or repairs; the Critic challenges; the Orchestrator routes and owns state transitions.
17. **Need 5: legal handoffs.** A recurring workflow needs explicit dependencies, entry conditions, and a reason a node may advance.
18. **Concept: Graph.** Define node, edge, state, route, and barrier with one finance handoff example.
19. **Need 6: parallel expertise without partial completion.** Data, feature, backtest, PIT, robustness, and execution checks have different responsibilities.
20. **Concept: Team fan-out and join.** Show lead agents, specialist outputs, isolated paths, and a deterministic join barrier.
21. **Finance gates: information set and execution.** Combine point-in-time data, observation/trade timing, T+1, lots, fees, price limits, suspensions, and corporate actions.
22. **Evidence and repair.** Combine the candidate manifest, stable finding IDs, evidence-linked severity, testable repairs, carried findings, and terminal states.

Pages 5--22 replace the current sequence of separate architecture layers,
decomposition slides, team explanations, timing slides, repair slides, loop
memory, termination, and resource details. The order makes every abstract term
answer a stakeholder or finance-control question.

### Break

23. **Break: ten minutes.** Use the page to shift from designing one run to making the system durable across runs.

### Section 1 continued: durable execution and improvement

24. **Need 7: survive interruption.** A four-hour research run must resume without inventing completed work or repeating side effects.
25. **Concept: Durable state.** Persist case, request, candidate, role, round, deadline, artifact hashes, prompt version, and finding ledger.
26. **Recovery and retry.** Resume only from matching verified state; classify timeout, invalid schema, risk violation, and external side effect before retrying.
27. **Need 8: enforce authority and trust boundaries.** Prompt instructions alone cannot protect files or distinguish rules from retrieved market text.
28. **Authority and context.** Separate Generator, Critic, and Orchestrator working areas; treat retrieved text as data; enforce least privilege at the host.
29. **Need 9: explain every transition.** Audit replay requires data lineage, agent traces, graph routes, approvals, and artifact links.
30. **Observability and replay.** Show the minimum trace that lets another analyst reconstruct one decision.
31. **Three loops, three objects of change.** Tool execution changes an artifact; revision changes a candidate; evolution changes the reusable harness.
32. **Need 10: repeated failures should improve the system.** A repaired case is not enough if the same omission returns next month.
33. **Evolution loop.** Capture a real failure, diagnose it from artifacts, propose one bounded prompt change, and freeze the acceptance rules.
34. **Evaluation, adoption, and rollback.** Compare baseline and candidate on fixed development and held-out cases; require approval; version the prompt; preserve rollback evidence.

### Section checkpoint

35. **Final architecture and review.** Show the complete Orchestrator--Generator--Critic system with harnesses, hooks, state, teams, gates, and inner/outer loops. Ask four questions: who may act, what must be evidenced, which handoff is legal, and how is improvement verified?

The current separate durable-state, recovery, authority, context, observability,
three-loop, evolution, evaluation, adoption, final-architecture, graph-coverage,
interface, and public-system slides become pages 24--35. Public-system names and
URLs belong in the instructor guide or handout.

### Section 2: build and run QT

36. **Map the architecture to files.** Show the plugin package, commands, skills, agents, hooks, scripts, and workspace `.qt/` state boundary.
37. **Two public commands.** Explain `/qt:start` and `/qt:evo`; keep the command surface small while the controller enforces transitions.
38. **Native delegation.** Show lead-agent allowlists, leaf specialists, separate contexts, and the absence of a required `tmux` layer.
39. **Hook exercise.** Register the QT hook, record only event/session/tool/call IDs, test duplicate delivery and workspace scope, and state that a log never certifies a candidate.
40. **Install and reload.** One installation path from the source package; reinstall after edits and reload before testing.
41. **Run one `/qt:start` case.** Follow request identity, Generator specialists, candidate manifest, numerical execution, Critic specialists, ledger, and route.
42. **Inspect the four barriers.** Generator completeness, numerical validity, Critic evidence, and termination. Use fault injection while inspecting these barriers.
43. **Rehearsal, live behavior, and resume.** Distinguish scripted controller verification from live model behavior, then show interruption, saved hashes, request matching, and continuation.

The current plugin map, command, native runtime, hook registration and test,
installation, live case, barrier, rehearsal, verification caveat, fault
injection, and resume slides become these eight implementation pages.

### Break

44. **Break: ten minutes.**

### Section 2 continued: evolve the harness and set the market boundary

45. **Run `/qt:evo`.** Reuse the same teams with new contracts: diagnose, propose, evaluate, pause for approval, and version.
46. **One bounded change.** Use the recorded missing-timing example only when actual evidence supports it; keep numerical gates and risk rules fixed.
47. **Evaluation sheet.** Fix denominators, case splits, thresholds, model, inputs, budget, and held-out cases before comparison.
48. **Adopt or roll back.** Inspect the diff and archived outputs, approve the version pointer, start a fresh case, and demonstrate authorized rollback.
49. **Synthetic fixture versus real market.** Show the boundary: licensed data, dated universe membership, public/vendor release times, corporate actions, exchange rules, positions, and fills.
50. **Try to falsify the pipeline.** Perturb future prices, inject a restatement, hand-check a rebalance, and reject a fake evidence ID.
51. **Acceptance before real use.** Require walk-forward validation, cost/slippage stress, capacity/turnover checks, and explicit limits; passing gates does not establish live alpha.

### Section 3: integrated lab

52. **Lab brief and deliverable.** One contract, one diff, one reproducible failing/passing case, one integration check, one version identity, and one limitation.
53. **Contract before edit.** Students write inputs, outputs, authority, failure behavior, and stop behavior before using an AI assistant.
54. **Choose one extension.** Freshness gate; finding-closure hash; required specialist join; or held-out prompt comparison.
55. **Plan the behavioral check.** Define the failure trigger, expected block or route, evidence path, and rollback step.
56. **Implement the smallest change.** Keep `/qt:start` and `/qt:evo` unchanged; edit one component only.
57. **Run the failing and passing cases.** Reinstall, reload, inspect state and evidence, and record any unrun checks.
58. **Integration and partner replay.** A second student replays the case and tests the declared contract and remaining limitation.
59. **Lab review rubric.** Contract clarity, reproducibility, intact barriers, honest scope, and rollback evidence; synthetic returns earn no credit.

60. **Debrief: defend the architecture.** Explain the Harness, Loop, Graph, Hook, and evolution choice using the stakeholder need that motivated it.

## Editing rules

- Rewrite the opening in ordinary prose and visual callouts. Do not show JSON,
  schemas, manifests, or code blocks until the QT implementation section.
- Introduce every abstract term only after stating its finance or stakeholder
  need. “Audit replay and determinism” is the first control need and should
  recur at the end.
- Keep one running synthetic case visible across the architecture, QT run, and
  lab. Do not use seven separate architecture-reveal pages for the same idea.
- Preserve the existing figures and tables that support the argument, but merge
  their surrounding explanatory frames according to the page map above.
- Edit the English source first, then mirror the frame map in Chinese. Rebuild,
  validate, render, and inspect both versions after the structural edit.
