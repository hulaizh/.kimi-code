# Topic 3: final teaching revision

The English and Chinese decks have 54 corresponding pages. This revision
implements the user's latest instructions and supersedes the earlier 58-page
and intermediate 52/53-page layouts. Page references below use the final PDFs,
including the title.

The Chinese translation was completed locally. The user will request any further
Pi proofreading independently; no further Pi review is part of this revision.
Earlier Gemini reviews and translation work remain historical evidence in
`logs/topic-3/redesign-58/`, not approval of this revised layout.

## Request-to-slide map

| User request | Final implementation |
|---|---|
| Merge and simplify the finance motivation | Page 5: four major distinctions with short subitems; no stakeholder figures or separate requirements table |
| Remove all visible Sources | No source-attribution blocks or URLs on slide surfaces; research/source notes remain available separately |
| Improve the logic of the old requirements page | Folded into page 5: consequences, dated evidence, authority, continuity/change |
| Manual contents pages for sections and subsections | Pages 7, 16, 22, 27, 35 and 46 use manual itemize/subitemize |
| Use fewer tables without removing useful figures | Only the two real output-comparison tables remain, on pages 49–50; process diagrams are retained with ordinary bullets beneath |
| Restore the harness figure and number its four components | Page 11: (1) Context, (2) Tools, (3) State, (4) Checks, in both languages |
| Explain the purpose of contracts and permissions | Page 12: contract defines required work/evidence; boundary defines permitted actions |
| Clarify hooks versus state control | Page 13: event callback versus workflow decision authority, with two independent diagram paths and a concrete missing-report example |
| Flat layout for the loop introduction | Page 17: one loop diagram above itemized text; the roadmap is its own preceding page |
| Merge stopping and recovery | Page 21: one conditional recovery diagram and a concise bullet list |
| Flat graph explanation with its figure | Page 23: dependency diagram above bullets |
| Explain combined limits | Pages 25–26: joins inspect combined exposure; the existing QT fixture's missing portfolio-wide gate is explicit |
| Restore a routing figure | Page 26: validated state branches to Wait, Repair, Advance or Stop; these are alternatives, not a serial chain |
| Flat evolution layout | Page 27 is a standalone manual roadmap; pages 28–33 explain broad evolution without a sidebar wrapper |
| Shorter frame titles | Titles identify the concept or action directly; retained role names are not abbreviated ambiguously |
| Remove standalone PIT/momentum QT detours | Removed from the main deck; page 40 focuses on the runnable request and artifacts. Worked details remain in companion notes |
| Remove the standalone GEPA detour | Removed from the main deck; external optimization details remain in companion notes |
| Use Git for version control | Page 51: reviewed commit → test evidence/configuration → approved tag; distinguish Git history from QT's active-prompt registry |
| Evaluate → Test → Approve | Page 52: literal three-stage diagram, with the actual QT command sequence explained accurately |
| Itemize the concluding review | Page 54: Evidence, Control, Continuity, Improvement, followed by the discussion prompt |
| Remove Illustrative badges | No Illustrative/示例 badges or review labels in either rendered deck; substantive synthetic-fixture limitations remain in ordinary prose |
| Improve Critic specialties | Pages 4, 25 and 34 show Data & Evidence, Robustness, Execution, Risk & Controls; page 37 distinguishes QT's three existing Critic profiles |
| Keep Chinese consistent | Same 54 pages, sections, figures, examples, identifiers and eight participation points; fluent Chinese prose follows the English meaning |

## Final structure

| Part | Pages |
|---|---:|
| Title, ladder and introduction | 1–6 |
| Harness | 7–15 |
| Loop | 16–21 |
| Graph | 22–26 |
| Evolution and architecture recap | 27–34 |
| QT: Build | 35–45 |
| QT: Evolve and final review | 46–54 |

The full architecture uses the same figure on pages 4 and 34. Human authority
stays outside the single Evolution enclosure. Detailed evolution appears on
page 29. The eight discussion prompts are on pages 19, 41, 42, 48, 49, 50, 52
and 54.

## Companion material

The detailed PIT/momentum examples, optional GEPA/MLflow discussion and source
records are retained in the existing teaching materials and the final case
handoff notes. Removing these standalone lecture slides does not change the QT
runtime or create new production functionality.

The design's four Critic specialties are broader than QT's current three-profile
fixture. Git-to-registry linkage is also a design extension. The slides retain
those boundaries and distinguish research acceptance, version approval and
capital authorization.

## Verification record

Build, alignment, source checks and final page renders are under
`logs/topic-3/final-polish/`. Both complete PDFs compile to 54 pages with zero
overfull/underfull boxes, missing glyphs or undefined references. All pages were
visually inspected; the independent bilingual review has no open findings.

All 53 content-frame pairs match in exhibit order, code identifiers, mathematics,
item counts and exercise placement. The seven active source listings are
byte-identical across languages. Only the two numerical output-comparison tables
remain. PDF-text checks confirm zero visible source-attribution or Illustrative
labels. The four harness component numbers and the Evaluate/Test/Approve labels
are present in both versions.

The generic style validator still reports preferences for fewer bullets and
exhibit-led text pages, and it does not recognize the Chinese roadmap titles.
Those checks conflict with the user's explicit manual itemize/subitemize and
translation requirements; they are not treated as layout failures. The existing
unused-subcaption warning and Chinese font-script metadata warning remain, with
no missing characters in the rendered output.

No QT runtime logic changed. Earlier runtime checks passed all 35 tests, and the
actual retry-request refresh behavior was verified separately. This revision
does not claim new live-agent performance or production readiness.
