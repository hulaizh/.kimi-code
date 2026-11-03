# Topic 3: Build a Self-Evolving Quant Trading Agent System

Students build an installable QT plugin for Kimi Code. The product is an
Orchestrator–Generator–Critic system with specialist teams, executable quant
tools, persistent case state and an evaluated evolution loop. The lecture opens
by deriving that architecture step by step. The trading task supplies each
engineering requirement; Harness, Loop and Graph are not isolated chapters.

The two public commands are `/qt:start` and `/qt:evo`. The first runs an idea
through proposal, implementation, numerical checking, criticism, repair and
reporting. The second improves the reusable harness using completed cases,
evaluations, reviewed adoption and rollback. Status, interruption, resume and
rollback use ordinary conversation. Kimi also exposes native `/skill:qt:start`
and `/skill:qt:evo` aliases for those same workflows.

## Four-hour teaching schedule

| Time | Purpose | Engineering introduced |
|---|---|---|
| 00:00–00:15 | Claim the product | Outputs, scope, responsibilities, acceptance |
| 00:15–01:20 | Design the inner system | Harness, hooks, tool loop, independent Critic, Orchestrator, teams, graph, gates, stopping |
| 01:20–01:30 | Break | |
| 01:30–02:10 | Complete the architecture | Durable state, recovery, permissions, traces, evolution, fixed evaluations, rollback |
| 02:10–02:45 | Build and run `/qt:start` | Manifest, commands, skills, native agents, hook exercise, installation, evidence barriers |
| 02:45–02:55 | Break | |
| 02:55–03:20 | Build `/qt:evo` and market extensions | Proposal, independent evaluation, version adoption; real-data interfaces |
| 03:20–03:55 | Student lab | Contract, defect, edit, behavioral check, integration, partner replay |
| 03:55–04:00 | Debrief | Defend Harness, Loop, Graph and evolution choices |

The English and Chinese decks each contain 86 pages, including the title, one
manually written contents slide and breaks. Following Topic
2's opening pattern, the task comes before the contents. There are three main
sections: system design, plugin implementation and evolution, and the integrated
lab. There are no subsections, repeated roadmap pages or separate reference
appendix. The timetable above is instructor guidance rather than a student slide.

The architecture is finalized before the plugin implementation section. Use
discussion to derive each addition before revealing its exhibit. Explanatory
slides use short itemized points; eleven tables remain for comparisons,
numbers and the lab schedule. Harness, loop and graph coverage checks are taught
beside the relevant concepts. Implementation limits and source slides are part
of the corresponding design, demonstration and market-extension discussions.

## Hooks within the harness

Five slides teach hooks in context: event boundaries, event selection, failure
semantics, plugin registration and behavioral checks. A Skill supplies a
procedure, a tool performs an action, and a hook runs a script at a declared
lifecycle event. Use `PreToolUse` for a lightweight precheck, `PostToolUse` for
success metadata, `SubagentStop` for successful-completion observation, and
`PreCompact` for snapshots of already saved state (its return values are ignored).
The controller still owns team joins,
case transitions and numerical/risk acceptance.

Kimi's intentional exit-2 blocking applies only to blockable events. Hook errors
and timeouts allow the main flow to continue; post-tool and subagent completion
events cannot veto it. `Stop` controls a model turn, not a QT case outcome.
Bound requests for continuation. Matching hooks can run in parallel, so avoid
ordering assumptions and duplicate side effects.

The runnable exercise is in `materials/topic-3/hooks/`. Students copy its script
into their plugin's `hooks/` directory and merge the manifest fragment, then
reinstall and reload. QT 0.1.0 does not enable this example by default. It records
only event/session/tool/call IDs in an existing QT workspace and ignores
unrelated workspaces. Plugin hooks run from the plugin root; the event's `cwd`
identifies the session workspace. Run offline cases for normal logging,
duplicate delivery, unrelated workspaces, mismatched tools and malformed input;
verify actual event delivery separately in Kimi. A log file never certifies a
candidate or updates control state. See the exercise README for the full steps
and current official sources.

## Starter and installed package

Source: `teaching/materials/qt/`. Its README explains installation and scope.
It is self-contained; students do not need a separately named project. Kimi's
installer copies it into the managed plugin directory. Reinstall after editing
source, then reload or start a new session. Run from any chosen workspace; state
lives in that workspace's `.qt/` directory.

```text
/plugins install /absolute/path/to/qt
/reload
/plugins info qt
```

The instructor's package is already installed under
`~/.kimi-code/plugins/managed/qt`, enabled, and recognized by Kimi Code 2.4.1.
Native custom agent profiles have explicit subagent allowlists. The main session
is Orchestrator; `qt-generator` owns data/features/backtest specialists;
`qt-critic` owns PIT/robustness/execution specialists. No tmux or experimental
Tower mode is required. See `docs/notes/qt-kimi-team-capabilities.md`.

## Preflight and evidence boundary

From a disposable workspace, using the installed or source package path:

```sh
python3 /absolute/path/to/qt/scripts/check.py
python3 /absolute/path/to/qt/scripts/qt.py start --case rehearsal --idea 'Synthetic monthly momentum' --rehearse
```

Python 3.11+ and the standard library suffice. The installed runtime passed
35 tests. A scripted two-round rehearsal reached ACCEPTED. Native installation,
command discovery and configuration checks also passed. These results do not
establish live model-team behavior or prompt improvement. A rehearsal uses
scripted specialist reports and real numerical code, and is explicitly labelled
SCRIPTED_REHEARSAL. Never present it as actual agent execution.

Before teaching, test a live `/qt:start` session with the configured model and
inspect actual Agent calls, separate specialist contexts, outputs and the route.
Authentication/model availability is a separate dependency. If live access is
unavailable, show the labelled rehearsal and inspect the profile/manifest code.

## Inner-loop demonstration

Use `/qt:start Test monthly momentum on the bundled synthetic teaching fixture`.
Inspect the idea, request ID, role card and assigned output paths. Watch the
Generator lead dispatch all three specialists. The lead integrates their reports
into a candidate manifest; the controller checks complete coverage and executes
the candidate. Only after numerical gates pass does it dispatch the Critic.

Watch a fresh Critic lead collect three fresh specialist reviews. Inspect actual
evidence, carried finding IDs and explicit resolutions. The controller merges
the ledger and applies the route. A missing specialist, invented evidence ID,
stale request or changed sealed artifact must block advancement. The supplied
tests exercise these failures. Use disposable cases for manual fault injection.

Exact classroom stopping policy:

- ACCEPTED: same candidate, two consecutive clean full reviews, all gates pass,
  all findings closed. A candidate change resets clean credit.
- CONTINUE: more repair or confirmation is needed and budget remains.
- EXHAUSTED: four-round default or four-hour wrapper deadline is reached.
- STALLED: candidate, findings and verdicts repeat without progress.
- REJECTED: a Critic REJECT or FATAL finding.
- BLOCKED: two invalid submissions in a role dispatch, or an invalid sealed case.
- USER_STOPPED: explicit user interruption recorded through the controller.

Elapsed time is checked at transitions; it does not kill a running model call.
Per-call timeout, token/cost accounting, concurrent-writer locking and stronger
filesystem isolation are host/production extensions. The role cards' writing
restrictions are instructions, not a filesystem sandbox. Artifact validation
cannot prove that specialist contexts were distinct or claims were sound.

## Evolution demonstration

Use `/qt:evo` on a completed case with a reproducible failure. The example of
missing execution timing is illustrative; do not invent a history to match it.
The Generator team performs diagnosis, prompt design and evaluation design;
the fresh Critic team reviews evidence, regression and scope.

The executable slice versions the Generator role prompt only. It rejects
strategy-parameter, risk-rule and arbitrary code targets. The evaluator runs
fixed code regressions, while model-behavior comparisons require actual runs on
fixed development and held-out cases. Preserve model version, inputs, budget,
attempt history and observed results. Code-test success alone is not evidence of
a better prompt. The runtime validates evidence fields but does not independently
grade the semantic quality of the Critic's assessment.

After passing evaluation, show the diff and evidence at AWAITING_APPROVAL. Only
explicit adoption approval changes the workspace's active prompt pointer. Start
a new case and inspect the selected version. Then demonstrate an authorized
rollback, preserving both versions and the evidence. Do not tune repeatedly
against the same held-out answer until a proposal passes.

## China-market scope

The offline adapter uses five fictional stocks and 120 synthetic weekdays,
momentum lookback/top-N candidates, simplified costs and China equity constraints.
Its weekday fixture is not an exchange calendar. It lacks real-market ingestion,
corporate-action accounting, a production portfolio service and broker access.
The historical sizing sheet is independent of the accepted research candidate.

For real use, students must implement and test authorized data adapters, dated
universe membership and delistings, public/vendor availability, corporate actions,
board/security/date-specific trading rules, fees, risk constraints and current
positions. Historical database access or a search tool alone does not establish a
valid live feed. Real suggestions require current inputs, approval expiry and
fill reconciliation. No classroom result demonstrates profitable A-share alpha.

The amended `materials/quant-cn-codex-brief.md` supplies the broader component
requirements. Its production architecture is a target, not the implemented scope
of the small teaching plugin.

## Student lab

Students edit one component in their copy of the plugin source. Require a contract
before an AI-assisted edit: inputs, output, authority, failure and stop behavior.
Choose timestamp freshness, version-bound finding closure, an additional specialist
with a join barrier, or a prompt behavior comparison. Submit one diff, a
reproducible failing/passing case, integration evidence, version identity and a
remaining limitation. Reinstall to test native behavior. A partner replays it.
Do not score synthetic returns or presentation confidence.

## Public source references

- [Kimi plugins](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/plugins.html)
- [Kimi skills](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)
- [Kimi agents](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html)
- [Kimi hooks](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/hooks.html)
- [Kimi Tower](https://www.kimi.com/code/docs/en/kimi-code-cli/guides/tower.html)
- [RD-Agent](https://github.com/microsoft/RD-Agent): hypothesis, experiments, feedback.
- [TradingAgents](https://github.com/TauricResearch/TradingAgents): role decomposition and review.
- [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading): agent-host integration with tools and skills.
- [SSE Trading Rules](https://www.sse.com.cn/lawandrules/sselawsrules2025/trade/universal/c/c_20260424_10816492.shtml): consult current board/security/date applicability.

See `docs/notes/qt-public-system-references.md` for the comparison and its limits,
and `docs/notes/qt-deployment.md` for installation verification. The course's QT
architecture is a design synthesis, not a claim that public projects share its
exact control policy or demonstrate superior trading performance.
