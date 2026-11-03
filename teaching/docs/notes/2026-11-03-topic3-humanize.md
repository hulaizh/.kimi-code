# Topic 3 humanize pass

Scope: English and Chinese slide prose and awkward labels in referenced
exhibits. The pass follows the explicitly invoked Codex humanize skill and its
academic-writing guidance. Professional lecture language calls for directness
and precise conditions, not invented anecdotes or personality.

## Draft rewrite

First-pass source snapshots are saved under `teaching/logs/topic-3/humanize/` as
`en-draft.tex` and `cn-draft.tex`. The pre-edit decks are in `en-before/` and
`cn-before/`. These are working records, not alternate student decks.

The first pass replaces most repeated bold-label prefixes with direct sentences
or questions. Itemized lists remain because the user requested them. Titles are
shortened, English titles use sentence case, and technical labels stay where
they help distinguish roles, loops, or outcomes. The user's recent opening-slide
edits and deletions are preserved.

## What still sounded generated after the first pass?

- Too many instructions used a generic label before saying what to do.
- Several titles repeated abstract nouns already explained by the figure.
- Some Chinese phrases added ceremony or certainty without information:
  “无缝恢复,” “一键回滚,” “具名责任人,” and “演化闭环.”
- Some claims overstated what tests, monitoring, or a source identifier could
  establish. Those qualifications needed precision, not more confident wording.
- Shortening had to retain retry limits, the fixed evaluation metric, version
  records, and board/date-specific execution rules.

## Final rewrite

The final versions are the normal slide source files and compiled PDFs. Examples:

| Earlier wording | Final wording |
|---|---|
| Where a chat transcript stops is not reliable evidence of which steps completed. | The last line of a conversation does not tell us which steps actually finished. |
| QT's implemented evolution slice versions only the Generator role prompt. | QT currently versions only the Generator's role prompt. |
| Your turn: state what must be fixed and re-verified before this prompt can be adopted. | What must be repaired and checked before adopting it? |
| Governance rule: moving a registry alias selects a version; it does not prove human approval. | A registry alias selects a version; approval needs its own record. |

The final pass also distinguishes rejecting a bad submission from terminating
an entire case, states the two-consecutive-clean-review condition, requires
sources to support claims as well as exist, and removes assurances that
monitoring or passing tests guarantees reliability or compliance. These are
corrections to overstatements, consistent with the recorded QT behavior and
earlier source checks.

The page sequence, four itemized contents pages, feedback arrow on page 2,
figures, numerical examples, code identifiers, and source URLs are retained.
Technical examples remain explicitly illustrative; no model results were
created. Build and visual checks are recorded under the same log directory.

## Verification

Both versions compile to 60 pages without overfull boxes, missing glyphs, or
undefined references. All pages received visual inspection, including a separate
copy-editor's review of the Chinese deck. The final check restored the explicit
fresh-review condition and the named approver in the paid-data example.

Source URLs, exhibit order, mathematical examples, code identifiers, and the
complete page-2 feedback diagram are preserved. The four manual contents pages
remain at 4, 23, 36, and 45. The English page-2 introductory sentence is retained
as requested by the user's recent edit; its legacy validator warning is a known
exception, alongside manual contents and text-only itemized explanations.
