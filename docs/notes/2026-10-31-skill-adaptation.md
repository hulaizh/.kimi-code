# Skill adaptation

Historical adaptation record. The current practitioner review and verification
are documented in `2026-10-31-practitioner-review.md`; the older validation counts
below do not describe the current installed skill set.

## Scope

Updated the six skills in `~/.kimi-code/skills/` and the two shared skills in `~/.agents/skills/`. Teaching slides and materials were not edited. Original skills were preserved in Git and in `ai-finance-skills-workspace/industry-adaptation/skill-snapshot/`.

Descriptions define the operation, useful invocation cues, and boundaries. Course names, degree labels, and generic audience positioning are excluded. Explanation depth belongs in the body and follows the actual request.

## Skill roles

| Skill | Operation | Boundary |
|---|---|---|
| brainstorming | Resolve ambiguity and compare implementation approaches | Clear bounded tasks proceed directly |
| newproj | Create a conservative non-overwriting scaffold | Analysis is a separate step, continued if already requested |
| plot | Generate and verify static figures | Interactive UI belongs to frontend-design |
| frontend-design | Build working web interfaces | No decorative controls or hidden data failures |
| latex | Format, compile, and inspect concise A4 finance PDF reports | One memo template; no journal or paper-submission rules |
| humanize | Edit existing prose faithfully | No invented figures, attribution, or stronger conclusions |
| find-skills | Discover a missing reusable capability | Installed skills first; popularity does not establish correctness |
| skill-creator | Capture and test a repeatable workflow | Task-based descriptions and observable acceptance checks |

Examples now cover cash forecasts, budget variances, credit review, reconciliation, portfolio reporting, and management decisions. A first encounter receives a worked example; analytical work receives assumptions and sensitivity checks; a decision brief leads with findings and implications. Evidence requirements are unchanged across these modes.

## Supporting fixes

- Replaced the old paper/journal LaTeX bundle with one A4 finance memo template and a short report workflow. Removed journal files, paper fixtures, appendix templates, and journal-specific tests.
- Removed the academic humanize reference and the econometric/journal-only plotting resources. The remaining skills target finance practitioners.
- Removed the starter deck's missing figure dependency and hardcoded author; documented the separate Chinese compilation route.
- Fixed the DataFrame-to-drawdown example and a removed matplotlib boxplot keyword.
- Removed fabricated error bars and an automatic normal fit from the plotting demo; labeled synthetic output and made GUI display optional.
- Removed invented price moves and forecast attribution from prose-editing examples.
- Retained the established newproj directory tree; explicitly defer intermediate-data placement to project instructions.

## Validation

All eight skill frontmatters and relative Markdown links pass validation. The starter Beamer deck compiles. The plotting demo runs headlessly, and direct checks confirm no invented error bars, no implicit normal-fit overlay, and the expected -10% sample drawdown.

The legacy LaTeX suite returned 32 passed, 1 skipped, 2 failed. Both failures reproduce against the untouched snapshot: journal names are returned as `ecma`/`jfqa` where tests expect `Econometrica`/`JFQA`. These journal-conversion issues are outside the adapted report workflow and remain unresolved.

Three paired independent-agent exercises cover a cash-forecast app, budget-variance report, and reconciliation-skill draft. Results and review artifacts are in `ai-finance-skills-workspace/industry-adaptation/iteration-1/`. This is a small functional comparison, not an estimate of general reliability. Agents inherited the conversation context, so it is not a blind experiment.

Both versions passed all 13 assertions. The revised cash app received browser and mobile checks, but this comparison establishes no pass-rate gain. The grader identified uncovered extreme-number overflow and negative-variance formatting cases in the generated examples; they should not be treated as generalized production tools. Reconciliation outputs are drafts, not tested matching engines. Timing comparisons are omitted because work overlapped, and token counts were unavailable. The review viewer is `ai-finance-skills-workspace/industry-adaptation/review.html`.

Twenty-four invocation examples are saved across the skills' `evals/invocation_cases.json` files and combined in the workspace. They are a review set, not a measured runtime selection benchmark. No automatic description-optimization score is claimed.

The isolated validation environment is under the workspace `.venv/`; no global Python packages were changed.
