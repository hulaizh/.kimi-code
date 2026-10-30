# Working-Paper Structure (wp) — research papers, manuscripts, internet appendices

The ONE format every LaTeX research paper keeps from scaffold to acceptance
(user directive 2026-09-21): the drafting STRUCTURE — section files,
title/author macros, the two-level table and figure architecture, booktabs,
the citation commands, theorem notation, the Internet Appendix fragment —
and the LAYOUT: a4paper, 12pt, 1.5in top/bottom and 1in side margins,
`\onehalfspacing`, arabic sections, Roman-numbered tables and figures,
figures before tables, `\citep`/`\citet`, a 100-word abstract (90–120
band), 60 manuscript pages plus a 40-page Internet Appendix. A journal's own
format (`draft/journals/<code>.yaml`, `journal_file.md`) is applied by
`journal_format.py` only once the paper is accepted there.

## Quick Start

**New project:** scaffold with the `newproj` skill
(`~/.claude/skills/newproj/scripts/init_project.py NAME --title "..."`),
which copies every asset below into `draft/`.

## Workflow

1. Read source file to understand structure
2. Check project directories exist (`sections/`, `tables/`, `figures/`)
3. Apply the structure (do NOT modify content):
   - Style import: `\input{style}`
   - Tables/figures: one per page, at end
   - Bibliography: `chicago` style (defined in style.tex), before tables
   - Document class, margins, spacing: the working-paper layout (template-carried)
4. Validate: `python ~/.claude/skills/latex/draft/scripts/validate_latex.py main.tex`
5. Compile: `python ~/.claude/skills/latex/draft/scripts/compile_latex.py main.tex`

## Document Structure

```latex
\documentclass[a4paper, 12pt]{article}
\input{style}

% Title and author as bare macros (no formatting, no \thanks) so the
% Internet Appendix header can reuse them. Wrappers go on \title/\author.
\newcommand{\Title}{Paper Title}
\newcommand{\Author}{Author One and Author Two}

\title{\textbf{\Title}}
\author{\Author\thanks{Author One: Affiliation. Email. Author Two: Affiliation. Email. Acknowledgments.}}
\date{\today}

\begin{document}
\maketitle

% Abstract lives in sections/abstract.tex (single source of truth — never inline)
\input{sections/abstract}

\onehalfspacing
\clearpage
\setcounter{page}{1}

\input{sections/introduction}
%% \input{sections/model}  %% Uncomment if paper has a theoretical model
\input{sections/data}
\input{sections/methodology}
\input{sections/results}
\input{sections/robustness}
\input{sections/conclusion}

\onehalfspace
\bibliography{ref}

\clearpage
\input{sections/figures}
\clearpage
\input{sections/tables}
\end{document}
```

**Section order:** Introduction → [Model (if applicable)] → Data → Methodology → Results → Robustness → Conclusion → Bibliography → Figures → Tables → Appendix (figures before tables everywhere, the appendix included)

Literature discussion is integrated into the end of the Introduction (contribution positioning), not a separate section.

## Authors and Acknowledgments

Use literal "and" (not `\and`), single `\thanks{}` for all:

```latex
\author{Author One and Author Two\thanks{Author One: Affiliation One. Email: \href{mailto:a@b.edu}{a@b.edu}. Author Two: Affiliation Two. Email: \href{mailto:c@d.edu}{c@d.edu}. Acknowledgments: We thank [names] for helpful comments.}}
```

## Exhibit Numbering

Main-text exhibits are numbered in **Roman numerals**, tables and figures
alike — Table I, Figure II in the main text; Table IA.I, Figure IA.I in the
Internet Appendix — in `style.tex` (a journal's own numbering is
`journal_format.py apply`'s business, on acceptance):

```latex
\renewcommand{\thetable}{\Roman{table}}
\renewcommand{\thefigure}{\Roman{figure}}
```

The IA fragment renews these to `IA.\Roman` at its start (see Internet
Appendix below). `validate_latex.py` checks only the IA fragment's `IA.\Roman`
setup, which is easy to omit when writing `sections/appendix.tex` by hand.
Cross-references always go through `\ref{tab:...}` / `\ref{fig:...}` —
never hardcode a rendered number in prose, so the numeral style stays a
pure style.tex concern.

## Tables (One Per Page)

Two-table pattern with `\vspace{-1.5cm}`. **Wrapper** (`sections/tables.tex`):

```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\clearpage
\begin{table}[htp!]
\caption{Main Results}
\label{tab:main}
{\footnotesize\justifying\setlength{\parindent}{0pt}
This table presents the main regression results. The dependent variable is $y_{it}$.
The independent variable of interest is $x_{it}$. Columns (1)--(3) include firm fixed effects.
Columns (4)--(6) add time fixed effects. Standard errors are clustered by firm and quarter
and are reported in parentheses. $^{*}p<.1; ^{**}p<.05; ^{***}p<.01$.}
\end{table}

\vspace{-1.5cm}

\begin{table}[ht!]\centering \caption*{}
    \input{tables/main_results}
\end{table}
```

**Content** (`tables/main_results.tex`) — pure tabular, booktabs only:

```latex
\begin{tabular}{l*{6}{c}}
    \toprule
    & (1) & (2) & (3) & (4) & (5) & (6)  \\
    \midrule
    $x_t(n)$ & 0.012$^{***}$ & 0.012$^{***}$ & 0.012$^{***}$ & 0.012$^{***}$ & 0.012$^{***}$ & 0.012$^{***}$ \\
          & (0.003) & (0.003) & (0.003) & (0.003) & (0.003) & (0.003) \\
    \midrule
    Obs.     & 38150 & 38150 & 38150 & 38150 & 38150 & 38150 \\
    $R^2$  & 0.481 & 0.485 & 0.485 & 0.484 & 0.488 & 0.488 \\
    Firm FEs & Yes & Yes & Yes & Yes & Yes & Yes  \\
    \bottomrule
\end{tabular}
```

**Bundled helper:** to avoid hand-coding the two-table pattern, use the script:
```bash
python ~/.claude/skills/latex/draft/scripts/build_table_wrapper.py \
  --label main_results \
  --caption "Main DID estimates" \
  --content tables/main_results \
  --description "Stage-2 estimates of policy effect on log earnings..." \
  --equation 'y_{it} = \beta D_{it} + X_{it}\gamma + \alpha_i + \delta_t + \varepsilon_{it}' \
  --se-cluster firm \
  >> sections/tables.tex
```
`--equation` renders the specification as one inline-math sentence; omit it when the description already references the text's numbered equation.

**Self-contained descriptions (CRITICAL):** Every table description must be fully self-contained so a reader can understand it without reading the main text. Include ALL of the following:

1. **Dependent variable**: What is being regressed or measured
2. **Key independent variables**: Define every variable that appears in the table rows, using natural English names (see Variable Naming below)
3. **Specification**: named by the text's numbered equation (`estimates of equation (\ref{eq:main})`) or, when none exists, stated once in one inline-math sentence (`$y_{it} = \beta x_{it} + \alpha_i + \gamma_t + \varepsilon_{it}$`). Never a display equation inside the notes (`$$...$$`, `\[...\]`, `equation`), and nothing the equation already conveys (which fixed effect absorbs what, collinearity drops, estimator mechanics)
4. **Sample**: Time period, unit of observation, sample size or key restrictions
5. **Fixed effects**: Which FEs are included (e.g., "investor and year fixed effects")
6. **Standard errors**: Clustering level (e.g., "Standard errors clustered by firm in parentheses")
7. **Significance convention**: Always end with `$^{*}p<.1; ^{**}p<.05; ^{***}p<.01$`

A description that says only "Stage 2 estimates weighted by AUM" is unacceptable. It must define what "Stage 2 estimates" means, what the dependent variable is, what the key regressors are, the sample, FEs, and clustering.

**Variable naming in content files (CRITICAL):** All variable names displayed in table rows must use natural, self-explanatory English labels. Never use code-style variable names from scripts (e.g., `if_signed`, `ln_tna`, `employee_number_log`). Instead use descriptive labels:

| Bad (code-style) | Good (natural) |
|-------------------|----------------|
| `if\_signed` | PRI Signatory |
| `ln\_tna` | Log(TNA) |
| `employee\_number\_log` | Log(Employees) |
| `gdp\_per\_cap\_log` | Log(GDP per Capita) |
| `personal\_avg` | Avg.\ Personal Assets |
| `crisk` | Risk Score |
| `pos\_crisk` | $\mathbb{1}$(Risk $> 0$) |

This rule applies to BOTH content files (`tables/*.tex`) and figure axis labels/legends. Scripts that generate tables must map internal variable names to display names before writing LaTeX output.

**Panel tables:**

```latex
\begin{table}[htp!]
\caption{Asymmetric Results}
\label{tab:asym}
{\footnotesize\justifying\setlength{\parindent}{0pt}
This table shows asymmetric responses. Panel A shows... Panel B shows...}
\end{table}

\begin{table}[ht!]\centering \caption*{Panel A: Positive Shocks}
    \input{tables/panel_a}
\end{table}

\begin{table}[ht!]\centering \caption*{Panel B: Negative Shocks}
    \input{tables/panel_b}
\end{table}
```

**Wide tables:**

```latex
\begin{table}[ht!]\centering \caption*{}
\resizebox{\textwidth}{!}{
    \input{tables/wide_table}
}
\end{table}
```

## Figures (One Per Page)

```latex
\clearpage
\begin{figure}[htpb]
\caption{Distribution of Results} \label{fig:distribution}
{\footnotesize\justifying\setlength{\parindent}{0pt} This figure presents the distribution of the main variable.
The sample period is 1999Q1 to 2023Q4. Values are trimmed at the 1st and 99th percentiles.}
\begin{center}
    \includegraphics[width=.8\textwidth]{figures/distribution.pdf}
\end{center}
\end{figure}
```

**Self-contained figure descriptions**: Same principle as tables — a reader must understand the figure without the main text.

**Natural axis labels and legends**: Figure axis labels and legends must use natural English. Scripts that generate figures must map internal names to display labels.

**Event-study figures** — the description names the plotted statistic and its specification by the numbered equation (or one inline-math sentence), never as a display equation:

```latex
\begin{figure}[htpb]
\caption{Dynamic Effects} \label{fig:dynamic}
{\footnotesize\justifying\setlength{\parindent}{0pt} This figure plots the coefficients $\beta_h$, $h \in \{-2, -1, 0, 1, \ldots, 8\}$, from equation (\ref{eq:event_study}) with 95\% confidence intervals: the response of the outcome $h$ quarters after the shock. The sample is firm-quarters, 2000--2020. Standard errors are clustered by firm.}
\begin{center}
    \includegraphics[width=.8\textwidth]{figures/event_study.pdf}
\end{center}
\end{figure}
```

**TikZ conceptual diagrams** — structure over prose; blue = direct effects,
red/dashed = feedback:

```latex
\begin{figure}[htpb]
\caption{The Multiplier Effect} \label{fig:multiplier}
{\footnotesize\justifying\setlength{\parindent}{0pt} This figure presents how shocks propagate. Blue arrows show direct effects.
Red arrows show feedback effects.}
\begin{center}
\begin{tikzpicture}[
    every node/.style={draw, rectangle, minimum width=2.5cm, minimum height=1cm},
    every path/.style={->, thick},
    node distance=2.5cm and 2.5cm
]
\node[fill=blue!20,draw=none] (demand) {Investor Demand};
\node[fill=yellow!20,draw=none] (price) [below left=of demand] {Stock Price};
\node[fill=red!20,draw=none] (investment) [below right=of demand] {Firm Investment};
\draw [blue] ($(demand.south) + (-0.15, 0)$) -- ($(price.north) + (-0.15, 0)$);
\draw [red, dashed] ($(demand.south) + (0.15, 0)$) -- ($(price.north) + (0.15, 0)$);
\draw [blue] ($(price.east) + (0, -0.1)$) -- ($(investment.west) + (0, -0.15)$);
\draw [red, dashed] ($(price.east) + (0, 0.1)$) -- ($(investment.west) + (0, 0.15)$);
\draw [red] (investment) to (demand);
\end{tikzpicture}
\end{center}
\end{figure}
```

See `~/.claude/skills/latex/slides/references/tikz_conventions.md` for the full TikZ idiom.

## Citations

Every draft uses the natbib commands below (`\citep` / `\citet`); a
journal's own in-text form (`citet_in_parens` at JF and JFQA — each cited
year in its own parentheses) is `journal_format.py apply`'s business, on
acceptance.

```latex
% Textual (author as subject)
\citet{koijen2019demand} introduce the demand-system approach.
Following \citet{gabaix2021search}, I use granular instruments.

% Parenthetical (author in parentheses)
The stock market is inelastic \citep{van2021flow,haddad2021competitive}.
This is consistent with prior work \citep[see][for a review]{bond2012real}.

% Multiple citations
Prior studies document this effect \citep{edmans2012real,hau2013real,dessaint2019noisy}.

% Footnote citations
This finding is consistent with prior literature.\footnote{See \citet{author2020}
and \citet{author2021} for related evidence.}
```

## Mathematical Notation

**Custom commands** (carried by `style.tex`): `\E` (expectation),
`\Var`/`\Cov`/`\Corr`/`\diag` (operators), `\argmax`/`\argmin` (subscript
below in display), `\Prob`, `\Normal`, `\iid`, and the number sets
`\R`/`\N`/`\Z`.

**Equation styles:**

```latex
% Inline
$\hat{\beta} = (X'X)^{-1}X'y$

% Display, unnumbered
\[
y_{it} = \alpha_i + \gamma_t + \beta x_{it} + \varepsilon_{it}
\]

% Numbered
\begin{equation} \label{eq:main}
    y_{it} = \alpha_i + \gamma_t + \beta x_{it} + \varepsilon_{it}
\end{equation}

% Aligned multi-line
\begin{align}
    \Delta Q^{F}_{t} &= \Lambda_t^{F} (\zeta^{P}_{t}+\Lambda_t^{F})^{-1} \Delta D_{t} \label{eq:financing} \\
    \Delta X_{t} &= \Lambda_t^{X} (\zeta^{P}_{t}+\Lambda_t^{F})^{-1} \Delta D_{t} \label{eq:investment}
\end{align}

% Cases
\begin{equation*}
    \Phi(I_t, K_t) =
    \begin{cases}
        \frac{a_1}{2}\frac{I_t^2}{K_t}, & \text{if } I_t \geq 0 \\
        \frac{a_2}{2}\frac{I_t^2}{K_t}, & \text{if } I_t < 0
    \end{cases}
\end{equation*}
```

## Theorem Environments

`style.tex` defines `prop`, `obs`, `lemma`, `theorem`, `assumption`,
`corollary`, `definition`, `remark`, `hypothesis`. The formal ones — `theorem`,
`prop`, `lemma`, `corollary` — state the paper's OWN results and each is
machine-verified in Lean under GAN (gate `theorem_proofs`, every Build round);
never restate a published result in one of them (cite it in prose). An
empirical prediction is a `hypothesis`: stated and tested, never proved.

```latex
\begin{assumption} \label{asp:exclusion}
    The idiosyncratic shocks are uncorrelated with systematic shocks:
    $\varepsilon_{i,t}(n) \perp \eta_t(n)$.
\end{assumption}

\begin{prop} \label{prop:equilibrium}
    In equilibrium, the multiplier effects are:
    \begin{align}
        \Delta Q^{F}_{t} &= M^F \Delta D_{t} \\
        \Delta X_{t} &= M^X \Delta D_{t}
    \end{align}
\end{prop}

\begin{proof}
    The proof follows from Lemma~\ref{lemma:hayashi}. See Appendix~\ref{app:proof}.
\end{proof}
```

## Project Structure

```
project/
├── main.tex           # Main document preamble + \input{sections/...}
├── style.tex          # Packages and commands
├── ref.bib            # Bibliography
├── sections/
│   ├── abstract.tex       # Abstract + JEL + Keywords (single source of truth)
│   ├── introduction.tex
│   ├── model.tex          # Optional (if paper has a model)
│   ├── data.tex
│   ├── methodology.tex
│   ├── results.tex
│   ├── robustness.tex
│   ├── conclusion.tex
│   ├── tables.tex     # Table wrappers (one per page)
│   ├── figures.tex    # Figure wrappers (one per page)
│   └── appendix.tex   # Internet appendix (uses \Title)
├── tables/            # Table content (*.tex)
└── figures/           # Figures (*.pdf, *.tex)
```

**Path self-containment (enforced by `validate_latex.py`):** every
`\input`/`\includegraphics`/`\graphicspath` target must be LOCAL to the paper
root — never `../` and never absolute. The paper must build from a
copied/zipped directory (journal and arXiv submission silently drop anything
outside it).

### Exhibit mirror contract (projects with an `output/` pipeline)

In research projects where estimation scripts emit exhibits into a sibling
`output/` directory (the GAN project layout), the paper root keeps TWO copies
by design:

- `output/tables/` + `output/figures/` — the SINGLE home scripts write to;
  regenerated on every run.
- `<paper root>/tables/` + `<paper root>/figures/` — a self-contained COPIED
  mirror the wrappers `\input` with local paths.

The mirror is refreshed automatically at compile time (the GAN plugin's
`compile_with_provenance.py` copies changed files before pass 1; it never
deletes). Never hand-edit mirror files, and never point a wrapper at
`../output/...` to "save the copy" — that breaks submission portability and
fails the validator. Standalone papers without an `output/` pipeline are
unaffected (`compile_latex.py` stays sync-free).

## Two-Level Table/Figure Architecture

**Level 1 — Content** (generated by estimation scripts):
- `tables/*.tex` — pure `\begin{tabular}...\end{tabular}` with booktabs
- `figures/*.pdf` — plot output from matplotlib/seaborn

**Level 2 — Wrapper** (in `sections/tables.tex` and `sections/figures.tex`):
- `\caption{Title}` + `{\footnotesize\justifying\setlength{\parindent}{0pt} Self-contained description}` + `\input{tables/...}` (or the `\notes{}` macro)
- One per page with `\clearpage`
- NO `\footnote{}` — everything in the description block
- **Two-float form** (see `assets/tables_template.tex`): the titled
  `\caption{}` + description live in one float; the body (`\caption*{}` +
  `\input{tables/...}`) lives in a second float. Never collapse caption and
  tabular into a single `\begin{table}` — `validate_latex.py` flags it.
  Figures keep `\caption` → notes → image order inside one float.

Scripts NEVER generate wrappers. Wrappers are written during paper drafting/formatting.

## Internet Appendix

The Internet Appendix is an **in-paper section**, not a separate document.
`sections/appendix.tex` is a fragment `\input` into `main.tex`, so it inherits
`\Title` and the preamble from `main.tex`. NEVER redefine `\Title` in the
appendix — change it once in `main.tex` and the IA header updates
automatically. The IA header shows the **title only** — do NOT list authors in
the Internet Appendix.

The scaffold wires it into `main.tex` after the body (before `\end{document}`), so
manuscript and Internet Appendix compile to ONE pdf:

```latex
\clearpage
\appendix
\input{sections/appendix}
```

Use `\clearpage` (NOT `\newpage`): it flushes held-over floats so the IA
header opens a fresh page — that header is what the page-limit check scans
for to exclude IA pages from the manuscript page cap. `validate_latex.py`
checks only the fresh-page wiring on any appendix wired into `main.tex`;
the IA header itself — the standard `Internet Appendix for ``\Title''`
wording — and the full IA setup block (counter resets, `IA.*` renumbering)
are TEMPLATE-carried by `assets/appendix_template.tex`, not
validator-checked (the compiled-page scan at pre-submission is the header's
authority). For the rare in-paper appendix that is deliberately NOT an
Internet Appendix, opt out with a `% no-internet-appendix` comment at the
top of `sections/appendix.tex`.

`sections/appendix.tex` is a fragment (NO `\documentclass`, NO
`\begin{document}`). Uses `IA.` prefix with Roman numerals for tables/figures
(the same `\Roman` style the main text uses — see Exhibit Numbering above):

```latex
% IA.* numbering
\setcounter{page}{1}
\renewcommand{\theequation}{IA.\arabic{equation}}
\renewcommand{\thefigure}{IA.\Roman{figure}}
\renewcommand{\thetable}{IA.\Roman{table}}
\setcounter{equation}{0}
\setcounter{figure}{0}
\setcounter{table}{0}
\setcounter{section}{0}
\renewcommand{\thesection}{IA.\arabic{section}}
% Subsections render "IA.1.1, IA.1.2, ..." (NOT flat "IA.1, IA.2" which
% collides visually with section numbers).
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}

% Title block — \Title inherited from main.tex; no authors in the IA
\begin{center}
{\Large \bf Internet Appendix for \\ ``\Title''}
\end{center}
```

**Section order:** Proofs → Variable Definitions → Additional Figures → Additional Tables

Appendix exhibits show FIGURES first, then tables — in any appendix (Internet
Appendix or in-paper). Figures come before tables here exactly as in the main text.

See `draft/assets/appendix_template.tex` for the full fragment.

## Verification

Run `validate_latex.py` for the automated subset, then
verify the rest manually. The validator deliberately checks ONLY often-wrong
and necessary points (see the admission rule in its module docstring) —
template-carried conventions (`\input{style}`, chicago bib style,
bibliography-before-tables order, `\clearpage` before the exhibit section
inputs, the IA.* setup block) are shipped by the templates and are NOT
validator-checked; the manual rows below still list them for papers being
converted from foreign formats. Layout and length rows are the working-paper
format every draft keeps (a journal's facts apply on acceptance).

- [ ] Document class `[a4paper, 12pt]{article}`
- [ ] Geometry `top=1.5in, bottom=1.5in, left=1in, right=1in`
- [ ] Line spacing `\onehalfspacing`, declared in main.tex after the abstract
- [ ] Manuscript within 60 pages excluding the Internet Appendix, the appendix within 40 (gan/scripts/pre_submission_checks.py)
- [ ] Style: `\input{style}` after documentclass
- [ ] Title/author macros: `\newcommand{\Title}{...}` and `\newcommand{\Author}{...}` (bare, no formatting/`\thanks`), used as `\title{\textbf{\Title}}` and `\author{\Author\thanks{...}}`
- [ ] Authors: `Author1 and Author2` in `\Author` (literal "and"), single `\thanks{...}` on `\author`
- [ ] Abstract lives at `sections/abstract.tex` and is included via `\input{sections/abstract}` in `main.tex` — NEVER inline `\begin{abstract}...\end{abstract}` in `main.tex`
- [ ] Abstract has JEL and Keywords, 90–120 words (the 100-word bound; over 100 warns)
- [ ] Main text uses `\input{sections/...}` for Introduction, [Model,] Data, Methodology, Results, Robustness, and Conclusion
- [ ] Tables use booktabs (`\toprule/\midrule/\bottomrule`)
- [ ] Tables/figures: one per page with `\clearpage`
- [ ] Main-text tables/figures numbered in Roman (`\thetable`/`\thefigure` renewed to `\Roman` in style.tex)
- [ ] Figures before tables, in the main text and in the appendix
- [ ] Table descriptions are self-contained (dependent variable, regressors defined, specification by numbered equation or one inline sentence — no display math — sample, FEs, clustering, significance stars)
- [ ] Table/figure variable names are natural English (no code-style names)
- [ ] Bibliography uses `chicago` style (in style.tex), appears before tables
- [ ] Table/figure note blocks are justified AND flush-left (`{\footnotesize\justifying\setlength{\parindent}{0pt} ...}` or `\notes{}` — same idiom for both; no first-line indent)
- [ ] Two-float wrapper form: no `\begin{table}` float combines a titled `\caption{}` with tabular/`\input` content; figures keep `\caption` → notes → image order
- [ ] Path self-containment: no `../` or absolute `\input`/`\includegraphics`/`\graphicspath` targets (exhibits live in local `tables/` + `figures/`)
- [ ] Internet Appendix: `IA.` prefix, Roman numerals for tables/figures, uses `\Title`
- [ ] Internet Appendix subsections numbered `IA.N.M` (via `\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}`), not flat `IA.M`
- [ ] Internet Appendix header shows the title only — NO authors listed in the IA

## Scripts

| Script | Usage |
|--------|-------|
| `validate_latex.py` | `python ~/.claude/skills/latex/draft/scripts/validate_latex.py main.tex` — Check the structure and the working-paper layout |
| `compile_latex.py` | `python ~/.claude/skills/latex/draft/scripts/compile_latex.py main.tex [--clean]` — Compile with bibtex |
| `build_table_wrapper.py` | Generate two-table caption+content pattern for `sections/tables.tex` |
| `journal_format.py` | The journal pass on an ACCEPTED paper (`/latex <code>`); see `journal_file.md` |

## Assets

Located at `~/.claude/skills/latex/draft/assets/`:

| File | Description |
|------|-------------|
| `style.tex` | Packages, theorem envs, math commands |
| `paper_template.tex` | Full paper template |
| `appendix_template.tex` | Internet appendix template |
| `tables_template.tex` | Table section with examples |
| `figures_template.tex` | Figure section with examples |
| `section_*.tex` | Section stubs copied into `sections/*.tex` |
| `table_example.tex` | Example regression table |
