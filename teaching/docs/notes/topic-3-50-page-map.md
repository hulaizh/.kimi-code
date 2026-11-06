# Topic 3: 50-page revision

English deck: `slides/topic-3/3_long_run_workflows.tex` and its compiled PDF.
Revised on 6 November 2026. Baseline: commit `b89f4e2` (59 PDF pages).
The revised deck contains **50 pages, including the title**.

Nine related pairs were combined. All 171 original item-text occurrences
(including nested bullets) and four standalone prose lines remain verbatim,
as do all 36 exhibit references, six source links,
and eight hands-up exercises. Original commands, numerical examples, figures,
tables, qualifications, and discussion questions remain in the slides.
The four table-of-contents pages are retained.

Body font sizes are unchanged. Merged pages use tighter local line and list
spacing, with two columns where appropriate. The interruption-state diagram
was rearranged from two rows into one; all four states and labels are retained.
The English deck's recent division-of-labor edits are included. The Chinese deck
was outside this edit and retains its existing pagination.

## Combined pages

| Revised PDF page | Original PDF pages | Revised title |
|---:|---:|---|
| 17 | 17 + 19 | Timing Errors: Repair and Review |
| 22 | 23 + 24 | Checkpoints: State and Saved Progress |
| 24 | 26 + 27 | Audit Trail: Record and Reconstruct |
| 28 | 31 + 33 | Three Loops: Repair and Prevention |
| 35 | 39 + 40 | QT Research: Run and Check |
| 37 | 42 + 43 | Saved Evidence: Replay and Resume |
| 39 | 45 + 46 | Prompt Changes: Failure and Test Case |
| 40 | 47 + 50 | Evaluation: Criteria and Regressions |
| 45 | 53 + 54 | Prompt Versions: Adoption and Rollback |

## Complete page crosswalk

Numbers below refer to PDF pages, including the title. The old source's page
comments were stale; this crosswalk uses the actual 59-page baseline order.

| Revised PDF page | Original PDF page(s) | Content |
|---:|---:|---|
| 1 | 1 | Title |
| 2 | 2 | Agentic Quant System |
| 3 | 3 | Division of labor |
| 4 | 4 | When the system is ready |
| 5 | 5 | Table of contents |
| 6 | 6 | What finance professionals need |
| 7 | 7 | PIT Data: No look-ahead bias |
| 8 | 8 | Harness: the agent's working conditions |
| 9 | 9 | User Requests |
| 10 | 10 | Reproduce one calculation |
| 11 | 11 | Tool loop: act on the result |
| 12 | 12 | An independent review |
| 13 | 13 | Orchestrator: coordinate the work |
| 14 | 14 | Graph: dependencies and handoffs |
| 15 | 15 | Teams: parallel work and joins |
| 16 | 16 | Check the combined result |
| 17 | 17, 19 | Timing Errors: Repair and Review |
| 18 | 18 | Revision loop: repair and review |
| 19 | 20 | When to accept, revise, or stop |
| 20 | 21 | Hooks: events and control boundaries |
| 21 | 22 | Table of contents |
| 22 | 23, 24 | Checkpoints: State and Saved Progress |
| 23 | 25 | Check state before retrying |
| 24 | 26, 27 | Audit Trail: Record and Reconstruct |
| 25 | 28 | Authorize an external action |
| 26 | 29 | Handle untrusted inputs |
| 27 | 30 | Who is responsible? |
| 28 | 31, 33 | Three Loops: Repair and Prevention |
| 29 | 32 | Evaluate a change before adoption |
| 30 | 34 | The complete architecture |
| 31 | 35 | Table of contents |
| 32 | 36 | Plugin files, commands, and installation |
| 33 | 37 | Assign leads and specialists |
| 34 | 38 | Register and inspect a hook |
| 35 | 39, 40 | QT Research: Run and Check |
| 36 | 41 | Repair a rejected submission |
| 37 | 42, 43 | Saved Evidence: Replay and Resume |
| 38 | 44 | Table of contents |
| 39 | 45, 46 | Prompt Changes: Failure and Test Case |
| 40 | 47, 50 | Evaluation: Criteria and Regressions |
| 41 | 48 | promptfoo: compare the outputs |
| 42 | 49 | DSPy/GEPA: propose prompt changes |
| 43 | 51 | Decide from the evidence |
| 44 | 52 | Record the tested configuration |
| 45 | 53, 54 | Prompt Versions: Adoption and Rollback |
| 46 | 55 | Monitor later runs |
| 47 | 56 | Replace synthetic data |
| 48 | 57 | Test the research pipeline |
| 49 | 58 | Authorize and reconcile trades |
| 50 | 59 | Review the completed system |

## Verification

- Successful `latexmk -pdf` build; 50 PDF pages.
- No overfull/underfull boxes, undefined references, or LaTeX errors.
- Content comparison confirms every original item text and standalone prose line
  appears on its mapped destination page; exhibit and source-link counts match.
- Independent copy-editor review found no substantive omissions or meaning changes.
- All 50 pages were inspected visually; every merged page was also checked at
  full size. Initial overflows were fixed, and the final adoption/rollback page
  received extra clearance above its hands-up badge.
- The generic style validator does **not** fully pass: it already rejected the
  baseline's `Table of contents` title because it requires the literal title
  `Roadmap`, and flagged existing text-only pages and prose. It also flags the
  merged pages against its 50-word and whole-frame bullet-count preferences.
  These are style exceptions to preserve all material within the requested page
  cap; each individual list still has at most four items. No shared style file
  was changed. The inherited unused subcaption-setting warning remains.

Build logs, baseline snapshots, content/style reports, and page renders are in
`logs/topic-3/50-pages/` (gitignored).
