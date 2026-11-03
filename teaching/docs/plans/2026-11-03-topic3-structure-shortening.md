# Topic 3 slide structure: four-hour version

Status: draft for discussion. This note redesigns the structure before editing
the English and Chinese source decks.

## Design decision

The current deck has 86 pages (85 frames plus the title page). It asks the
audience to learn the architecture, Kimi's packaging model, hook semantics,
the QT implementation, China-market extensions, and a lab through many small
explanatory frames. The shorter version should make one argument:

> A recurring finance task becomes dependable when the system makes evidence,
> authority, state, handoffs, review, and improvement explicit.

Use one synthetic quant-research case throughout. Each new engineering idea
should answer a failure in that case. The deck should contain roughly 45--50
pages, including title, contents, two breaks, and the lab instructions. The
instructor guide can retain operational detail that students do not need on
screen.

## Time and page budget

| Time | Teaching purpose | Page budget |
|---|---|---:|
| 00:00--00:15 | Product, scope, responsibility, acceptance | 3 |
| 00:15--01:20 | Derive the inner system: harness, loop, graph, review | 13--14 |
| 01:20--01:30 | Break | 1 |
| 01:30--02:10 | Durable state, recovery, observability, evolution | 7--8 |
| 02:10--02:45 | Map the architecture to QT and run one case | 7--8 |
| 02:45--02:55 | Break | 1 |
| 02:55--03:20 | Evolve the harness and define the real-market boundary | 4--5 |
| 03:20--03:55 | Integrated student lab | 5--6 |
| 03:55--04:00 | Debrief and handoff | 1 |
| **Total** |  | **42--47** |

The page budget assumes discussion, live inspection, and the two hands-on
periods. A dense 60-page deck would recreate the current pacing problem.

## Proposed order

### Opening: claim the product

1. **Task: Build the quant agent system.** Show the final student deliverable.
2. **Contents.** Three sections only: design the system; build and evolve QT;
   integrated lab.
3. **Product and acceptance.** Combine the current product, scope, ownership,
   and acceptance frames. State the case output, human authority, and the three
   acceptance dimensions: evidence, recoverability, and improvement.

This keeps the task before the contents while eliminating a separate scope
and ownership detour.

### Section 1: derive the inner system

4. **Failure: one agent is fluent but unsupported.** Combine the one-agent
   architecture and the three failure examples.
5. **Harness: make the task executable.** Inputs, scoped context, checked
   tools, output manifest, and authority.
6. **Tool loop: plan, act, observe.** Put pre-call and post-call validation on
   the same exhibit.
7. **Hooks at event boundaries.** Explain Skill, tool, and hook together; show
   only the event choices needed for this course.
8. **Hook limits.** One compact comparison of blockable events, logging-only
   events, timeouts, and the controller's responsibility.
9. **Independent critic.** Explain why self-agreement is not verification.
10. **Orchestrator and legal graph.** Combine role separation with node, edge,
    state, and route.
11. **Teams and the join barrier.** Show Generator and Critic leads, their
    specialists, fan-out, and deterministic join.
12. **Quant evidence gates.** Combine PIT data, timing/lag, execution rules,
    and the three Critic axes in one finance-specific table or diagram.
13. **Candidate and repair packet.** Combine the manifest, stable finding IDs,
    evidence-linked severity, and testable closure.
14. **Revision state machine.** Combine revision, carried findings,
    ACCEPTED/CONTINUE/REJECTED/BLOCKED/EXHAUSTED, and loop budgets.
15. **Design checkpoint.** Ask students to identify which component owns each
    gate before revealing the complete architecture.

The current frames on decomposition, separate team integration, loop memory,
and resources become parts of these five exhibits rather than separate stops.

### Break

16. **Break: ten minutes.** Keep the break page because it marks the change
    from inner-run mechanics to durable system design.

### Section 1 continued: make the system durable and improvable

17. **Durable state.** Identity, active role, round, evidence hashes, and the
    finding ledger.
18. **Recovery and retries.** Resume only from verified state; classify
    transient, invalid, risk, and side-effect failures before retrying.
19. **Authority, context, and trace.** Combine working-area permissions,
    untrusted retrieved text, and observability into one control-boundary
    frame.
20. **Three loops.** Distinguish tool execution, candidate revision, and
    harness evolution by their object of change.
21. **Evolution loop.** Capture a failure, diagnose it, propose one bounded
    prompt change, and preserve fixed gates.
22. **Evaluation and adoption.** Compare baseline and candidate on fixed
    development/held-out cases, require approval, version the prompt, and
    support rollback.
23. **Final architecture.** One diagram showing roles, teams, barriers, state,
    and the inner/outer loops.
24. **Architecture review.** Four questions: harness, loop, graph, evolution.

The current separate frames on recovery, authority, context, observability,
loop coverage, evolution capture, one-change-at-a-time, evaluation, adoption,
graph coverage, interface, and public systems collapse into these eight frames.
Public-system comparisons and detailed source lists move to the instructor
guide or handout.

### Section 2: build and run QT

25. **Map architecture to files.** Show the plugin tree and workspace `.qt/`
    state boundary.
26. **Two public commands.** Explain `/qt:start` and `/qt:evo`; keep the public
    surface small while Python enforces state transitions.
27. **Native delegation and hooks.** Combine plugin registration, role
    allowlists, and the hook exercise into one implementation frame.
28. **Install and reload.** Show the one installation path and the reload rule
    after source edits.
29. **Run one case.** Walk from request identity through Generator team,
    numerical gates, Critic team, ledger, and terminal route.
30. **Four barriers.** Generator completeness, numerical validity, Critic
    evidence, and termination. Use this as the live inspection checklist.
31. **Rehearsal versus live behavior.** State exactly what the scripted
    rehearsal proves and what only a live model run can establish.
32. **Interrupt and resume.** One compact demonstration of saved state,
    request matching, and continuity after interruption.

The current native-interface source slide, separate hook registration/demo
slides, verification caveats, fault-injection slide, and resume slide become
these eight implementation frames. Fault injection is shown during the
barrier demonstration rather than taught as a separate topic.

### Break

33. **Break: ten minutes.**

### Section 2 continued: evolve and set the market boundary

34. **Run `/qt:evo`.** Reuse the teams with new contracts: diagnose, propose,
    evaluate, and pause for approval.
35. **Evaluation sheet.** Fix denominators, case splits, thresholds, model,
    inputs, and budget before comparison.
36. **Adopt or roll back.** Show the prompt diff, approval state, active version
    pointer, and rollback evidence.
37. **From synthetic fixture to real market.** Combine adapter, point-in-time
    universe, corporate actions, exchange constraints, current holdings, and
    fill reconciliation into a boundary diagram.
38. **Acceptance before real use.** Walk-forward tests, cost/slippage stress,
    capacity/turnover, and the rule that gate passage does not establish live
    alpha.

The current market-source, portfolio-extension, and manual-handoff frames are
folded into the final two finance-boundary frames. Detailed URLs remain in the
instructor materials.

### Section 3: integrated lab

39. **Lab brief and deliverable.** One contract, one diff, one failing/passing
    case, one integration check, and one limitation.
40. **Choose one extension.** Freshness gate; finding-closure hash; required
    specialist join; or held-out prompt comparison.
41. **Build from the contract.** Inputs, outputs, authority, failure, and stop
    behavior must be written before editing.
42. **Test and integrate.** Reinstall, run the behavioral check, inspect state,
    and preserve evidence.
43. **Partner replay.** A second student replays the case and checks the
    declared contract.
44. **Debrief.** Defend the Harness, Loop, Graph, and evolution choices.

## What leaves the student-facing deck

- The four-hour timetable (keep it in `INSTRUCTOR.md`).
- Separate public-system comparison and URL/source frames.
- Repeated architecture diagrams whose only change is another added layer;
  retain the failure-to-final progression in three exhibits: one agent,
  harness plus critic/orchestrator, and final teams/graph.
- Detailed hook event inventories and all edge-case semantics beyond the
  contract students must use in the exercise.
- Separate slides for portfolio sizing, manual handoff, and the synthetic
  fixture disclaimer; fold them into the real-market boundary and acceptance
  frames.

## Editing rule for the next pass

Edit the English source first, then apply the same frame map to the Chinese
source. Keep all existing exhibits that carry the argument, but reassign them
to the merged frames above. Do not delete figures or tables until the revised
deck compiles and the live teaching path has been checked. After the structure
is approved, rebuild, validate, render, and inspect both language versions.
