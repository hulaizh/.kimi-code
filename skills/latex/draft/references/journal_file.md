# The journal file (`draft/journals/<code>.yaml`)

One file per journal, facts only: the journal's ACCEPTED-paper format as
recorded from its sources. No inheritance, no rule programming, no
defaults — a stated fact is applied and checked by `journal_format.py
apply/check`, an unstated fact is never checked and never touched, an
unknown key fails at load (`journal_rules.py` validates the schema). Adding
a journal is writing this file — no code changes. The file is applied ONCE,
when the paper is accepted at that journal (`/latex <code>`); every working
paper keeps the wp format (`wp.md`) and no gan gate reads a journal file
(user directive 2026-09-21).

```yaml
journal: JFQA                    # canonical code (aliases resolve via the gan plugin's map)
name: Journal of Financial and Quantitative Analysis
sources: ["...verified URL + date, or the bot-wall note..."]
verified:                        # ONLY when the journal's OWN current guidelines were read: the date and
  date: 2026-09-13               # the sections they settled; absent = the facts are carried (the gate,
  sections: [layout, length]     # `check` and the report say so — `journal_rules.provenance_note`)

layout:
  paper: letterpaper             # a4paper | letterpaper
  font_pt: 12
  font: times                    # times -> newtxtext,newtxmath; absent = any typeface
  class_options: [leqno]         # the EXACT extra documentclass options (absent = untouched)
  margins: 1in                   # scalar, or {top, bottom, left, right}
  spacing: double                # single | onehalf | double, or a list of accepted kinds
  ragged_right: true             # body prelude \raggedright (see below)
  hyphenation: false             # hyphen/exhyphen penalty 10000
  parindent: 0.5in               # \parindent set after \begin{document}
  preamble: ["\\usepackage{indentfirst}", "\\usepackage[tbtags]{amsmath}"]   # verbatim lines, inserted once in order; an option on an already-loaded package is reconciled onto that load (a grouped load is split)
length:
  pages: 45                      # main text before the appendix heading (report-only)
  pages_by_spacing: {onehalf: 32, double: 47}   # instead of `pages` (MS)
  appendix_pages: 25             # the posted/online appendix's own cap (report-only)
  abstract_words: 100            # report-only (the working-paper band is the gan gate's)
structure:
  numbering: {section: Roman, subsection: Alph, subsubsection: arabic}   # absent = arabic default
  exhibit_numbering: {table: arabic, figure: arabic}   # arabic | roman per kind (the wp template ships Roman for both)
  appendix_title: Supplementary Material     # heading renamed; in-text mentions listed for the house pass
  exhibits: end                  # end | inline
  float_markers: true            # [INSERT TABLE N ABOUT HERE] at first discussion
  title_page: blind              # blind | full
  jel: false
  keywords: false
citations:
  bst: JFQA                      # \bibliographystyle{X}; the .bst must sit beside main.tex
  bst_companions: [babelbst.tex] # files the .bst \inputs at bibtex time; `apply` refuses to start without them
  in_text: citet_in_parens       # citep | citet_in_parens
  full_authors_first: true       # natbib longnamesfirst
  equation_ref: "equation (N)"   # in-text equation-reference form
  stars: superscript             # significance stars in tables
house:                           # located by the engine, applied by Claude in the house pass
  - id: parenthetical_stats
    rule: No parenthetical statistic in running text; state it in prose.
    example: {before: "(t = 3.06)", after: ", with a t-statistic of 3.06"}
    locate: '\(\s*\$?\s*(t|p|z|F)\s*[=<>]'
```

`house:` item fields: `id`, `rule` (plain language), optional `example`
(`before`/`after`), optional `locate` (a regex; the engine lists candidate
lines before the pass and re-checks after it).

## What each fact does (`journal_format.py`)

| Fact | Check | Auto-fix |
|---|---|---|
| layout.paper, font_pt, class_options | documentclass rewritten in `main.tex` | yes |
| layout.font | font package in the preamble file | yes |
| layout.margins | geometry options in the preamble file | yes |
| layout.spacing | body spacing declaration in `main.tex` | yes |
| layout.ragged_right / hyphenation / parindent | one body prelude right after `\begin{document}` | yes |
| layout.preamble | each line present once in the preamble | yes |
| structure.numbering | `\the<section>` block in the preamble | yes |
| structure.exhibit_numbering | `\thetable` / `\thefigure` redefinitions rewritten or removed in the preamble file | yes |
| structure.appendix_title | the heading renamed in the appendix file | yes |
| structure.jel, keywords | required/dropped after the abstract | report |
| structure.title_page (blind) | author material in the body flagged | report |
| citations.bst | `\bibliographystyle` rewritten; missing `.bst` beside main.tex is a hard error | yes |
| citations.in_text | `\citep`/`\cite` rewritten in `sections/*.tex` | yes |
| citations.full_authors_first | natbib option | yes |
| citations.equation_ref | `Eq.~\ref` forms rewritten in `sections/*.tex` | yes |
| citations.stars | bare `0.123***` superscripted in `tables/*.tex` | yes |
| length.pages / pages_by_spacing | main-text pages measured and reported (an unstated cap is reported as unstated) | no |
| length.appendix_pages / abstract_words | recorded for the acceptance report only; the gan plugin gates the working-paper caps and band, never a journal's | no |
| structure.exhibits, float_markers | located; fixed in the house pass | no |

## Provenance

`journal_rules.provenance_note(code)` is the one line `journal_format.py
check` and the apply report print: whether the file's facts were verified
against the journal's own guidelines (`verified:` — date and sections) or
merely carried from its sources. A file with no `verified:` block is
carried — never presented as the journal's format.

## Always on (every journal, not in the YAML)

- A key repeated inside one citation command — the natbib year-collapse
  trigger — deduplicated in place.
- The natbib "same authors and year" warning in the compile log, and the
  rendered `(2003, 0)` / `(2003,?)` in the PDF text (blocking, needs a
  compile).
- booktabs rules in `tables/` (never `\hline`).
- No `\footnote{}` inside a float.

## Adding or updating a journal

Write the file from the journal's own author guidelines (verify the page
when reachable and record the read in `verified:`; carry and mark bot-walled
facts in `sources:` with the attempt, and leave `verified:` out), then add a
fixture case in `tests/test_latex.py`. Never put a journal's number in
Python.
