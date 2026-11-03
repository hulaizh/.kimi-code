# Topic 3: Build and Improve a Quant Research System

The English and Chinese decks each have 60 pages. One synthetic monthly-momentum
case supplies the reason for each control and the evidence for each activity.
There are two sections: Design the Quant System; Build and Improve the System.
Product and acceptance are stated in plain language before the contents.
Explanatory pages use short itemized lists; only pages 7, 11, 49, and 52 use
tables for worked data, calculations, and output comparisons.

Manual itemized contents pages at 4, 23, 36, and 45 mark the major transitions
and highlight the current subsection. The two sections contain Controlled
Research / Recovery and Governance, then Run and Verify QT / Improve the System.
There are no separate break slides, lab section, or reference appendix. Breaks
belong to the instructor schedule; participation occurs within the same task.

## Four-hour schedule

| Pages | Time | Teaching purpose |
|---|---|---|
| 1–4 | 00:00–00:15 | Product, acceptance, contents |
| 5–23 | 00:15–01:20 | Stakeholders, replay, authority, harness, loops, graph, hooks |
| — | 01:20–01:30 | Break; no slide |
| 24–35 | 01:30–02:05 | Durable state, recovery, evidence, supervision, change |
| 36–44 | 02:05–02:45 | Inspect QT, repair a submission, replay, and resume |
| — | 02:45–02:55 | Break; no slide |
| 45–56 | 02:55–03:45 | Capture, propose, evaluate, compare, version, adopt, restore |
| 57–60 | 03:45–04:00 | Production boundary and final product review |

This is 240 elapsed minutes, including 20 minutes of breaks. Retain three minutes
of contingency inside both the QT and improvement blocks. Use prepared
checkpoints rather than waiting for an entire live multi-agent run to finish.

## Participation inside the task

| Pages | Action | Minutes included above |
|---|---|---:|
| 18–20 | Write a repair criterion for the current finding | 5 |
| 28 | Reconstruct the case from saved evidence | 5 |
| 42 | Repair a blocked submission and inspect the next route | 7 |
| 46–47 | Define a regression case and propose one prompt edit | 6 |
| 49–52 | Inspect output differences and check a partner's claim | 8 |
| 54 | Defend adoption or rejection | 4 |

These 35 minutes are part of the schedule, not an additional lab. There is no
separate task menu or submission rubric.

## Core distinctions

An evidenced rejection can satisfy the system's delivery requirement while
rejecting a candidate strategy. Keep three decisions separate: the controller's
research verdict, the owner's approval of a prompt version, and authority to
deploy capital. QT does not send broker orders.

Page 6 introduces three tests, which recur on pages 28 and 43:

1. Audit reconstruction uses the original saved evidence and action records.
2. Calculation replay fixes inputs, code, configuration, and relevant environment.
3. A fresh model run can produce different decisions and paths.

Repetition does not prove correctness. A hash detects changed content; it does
not prove the original content was true. A replay must not repeat real payments
or orders. A new evaluation needs a new case; reopening an existing QT case
resumes or reuses recorded state.

Independent review means a separate context and evidence-based challenge. It
does not eliminate common model errors. The rule requiring two clean complete
reviews is a teaching implementation choice, not a universal assurance standard.

## Source package and preflight

The runnable package is [QT](../qt/README.md), with public commands
`/qt:start` and `/qt:evo`. State lives in the chosen workspace's `.qt/`
directory. Installation is pre-class preparation:

```text
/plugins install /absolute/path/to/qt
/reload
/plugins info qt
```

After editing plugin source, reinstall and reload before testing through Kimi.
Source-local tests import source directly and do not need reinstalling.

From a disposable workspace, using the chosen package path:

```sh
python3 /absolute/path/to/qt/scripts/check.py
python3 /absolute/path/to/qt/scripts/qt.py start --case rehearsal --idea 'Synthetic monthly momentum' --rehearse
```

The rehearsal executes numerical code with scripted specialist reports. It does
not call a model. Preserve that label. For a live-team demonstration, inspect
actual host dispatch and response records; the controller checks report files
but cannot establish that independent specialist contexts actually ran.

Prepare checkpoints for a pending Generator request, a complete numerical
result, a Critic finding, a corrected submission, and a terminal case. Use
disposable cases for fault injection. Do not modify sealed evidence in a case
you want to resume.

## Hooks

Page 22 combines event triggering, observation, host-permitted blocking, and
controller gates; page 23 introduces Recovery and Governance. Page 39 shows the
optional [Bash-event logging example](hooks/README.md).
It is not enabled in QT by default. Add its script and manifest fragment to a
plugin copy, then reinstall and reload.

Inspect event IDs and duplicate delivery. The script records event/session/tool/
call identifiers under an existing workspace's `.qt/hook_events/`. It does not
record complete specialist provenance or certify a candidate. Kimi hook errors
and timeouts are logged and permit continuation; mandatory acceptance checks
therefore remain in the controller. See the hook README for exact event rules
and official documentation.

## The research case

Use `/qt:start Test monthly momentum on the bundled synthetic teaching fixture`.
Inspect request identity, role assignments, saved numerical outputs, the Critic
ledger, and the route. A missing required report or stale request must block
advancement. The next submission must match the current request.

The exact QT states are:

- `ACCEPTED`: the same candidate passes all gates and two clean complete reviews.
- `WAITING`: an external role response is needed; this is not an accepted case.
- `EXHAUSTED`, `STALLED`, `REJECTED`, `BLOCKED`, and `USER_STOPPED`:
  distinct terminal reasons.

Candidate changes reset clean-review credit. Default wrapper budgets are four
rounds and four hours, checked at transitions. The elapsed-time check does not
cancel an in-flight model call. Host-level isolation, call cancellation, cost
accounting, and concurrent-writer controls remain separate production concerns.

## Self-improvement tools, pages 45–56

The toolchain is capture → propose → evaluate → approve/version. Teach the
evaluator before the optimizer so students know what a candidate must pass.

| Step | Concrete tool | Classroom status |
|---|---|---|
| Bind a completed case and parent prompt | QT `evo-prepare` | Implemented |
| Propose a reviewable edit | Generator team and Git diff | Existing workflow |
| Compare outputs against checks | promptfoo; custom Python assertions | External example |
| Propose prompt candidates from feedback | DSPy/GEPA | Extension requiring an adapter |
| Protect numerical/controller behavior | QT `scripts/check.py` | Implemented code checks |
| Track versions and evaluation evidence | QT registry; MLflow counterpart | QT exists; MLflow integration is an extension |
| Validate reviews, approve, restore | QT `evo-evaluate`, `evo-adopt`, `evo-rollback` | Implemented, with explicit approval |

These are internal actions, not additional public slash commands. QT's evolution
interface changes only the Generator prompt. It does not rewrite risk rules,
strategy parameters, arbitrary source code, or model weights.

Use [the companion example](improvement-tools/README.md) for pages 49 and 52:

```sh
python3 /absolute/path/to/topic-3/improvement-tools/check_example.py
```

Both outputs are manually written fixtures. The baseline violates execution
timing but cites a retained source; the candidate corrects timing but cites a
missing source. Both fail adoption. The standard-library script checks the
matrix plus time-zone, early-execution, false-availability, and malformed-output
boundaries. It makes no model calls.

An optional `promptfooconfig.json` uses the same local Python fixture provider
and assertions for viewing the comparison in promptfoo. The fixture assertions
were run during this slide revision; the promptfoo CLI itself is optional and
was not run. No API credentials are needed for this fixture. It is not evidence
of prompt improvement.

For real behavioral evaluation, collect actual outputs before class, keeping
model configuration, inputs, budgets, development cases, and final held-out
cases fixed as appropriate. Preserve attempted edits and repeated runs. Never
tune repeatedly on final cases until a proposal passes. Code regressions and
valid review fields alone do not establish semantic improvement.

Demonstrate approval only after inspecting the diff and evidence. Show the
active version pointer after adoption, and verify behavior in a separate new
case. Demonstrate authorized rollback while preserving the version history.
Existing cases do not silently migrate to a new configuration.

## Production boundary

The bundled fixture has fictional stocks and synthetic weekdays. It is not an
exchange calendar or a live feed. It lacks production ingestion, complete
corporate-action handling, portfolio-wide authority controls, and broker access.
Its historical sizing sheet is independent of the accepted research candidate.

For real deployment, require licensed dated inputs, historical membership and
delistings, availability timestamps, dated execution rules, risk checks, current
positions, approval expiry, and fill reconciliation. Financial validation needs
temporal-leakage tests, cost/slippage stress, and walk-forward evaluation.
Synthetic returns do not establish profitable alpha.

The payment mandate and aggregate-exposure exhibits are production illustrations.
FINRA is a US broker-dealer supervisory example, not the legal framework for the
synthetic China-equity exercise. An accountable human owner remains necessary
across tools and vendors.

## Sources and preparation records

- [Verified finance-harness sources](../../docs/notes/2026-11-03-topic3-finance-harness-sources.md)
- [Agreed structure and timing](../../docs/plans/2026-11-03-topic3-structure-shortening.md)
- [Earlier Pi review and corrections](../../docs/notes/2026-11-03-topic3-pi-review.md)
- [QT inner protocol](../qt/references/controller.md) and [evolution protocol](../qt/references/evolution.md)

Use the sources for bounded teaching claims. The current DFAH paper does not
establish that smaller models are generally more replayable. Vals scores are
not production failure probabilities or directly comparable across all versions.
SR 26-2 excludes agentic AI from its scope without removing broader governance.
