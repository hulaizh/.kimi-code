# Slides Format (Beamer presentations: lectures, seminars, conferences, job market talks, defense)

Format LaTeX Beamer slides for finance/economics academic style: figures and tables carry the argument, every word lives inside a structured container, and the audience tracks logic by scanning structure — not by reading sentences.

## Core principle

**Every visible element on a slide is structure.** A frame contains some combination of: a figure (`\input{figures/...}`), a table (`\input{tables/...}`), a display equation (often with `\underbrace` annotations), an `itemize`/`enumerate`, a `block`, or a TikZ diagram. Plain text between `\begin{frame}` and `\end{frame}` — prose paragraphs, centered italic lines, "Notation:" notes, parenthetical asides — has no place on a slide. If a sentence is worth saying, wrap it in a bullet or a block; if it can't be wrapped, the audience doesn't need it.

This is the economics/finance academic-talk standard (La Ferrara, Cox, Startz, Guren). Bullets are not the enemy; *unstructured prose dressed up as a slide* is.

### Operational rules

- **Lead every content frame with a figure, table, or display equation.** Text-only frames are for Roadmap, transitions, takeaways, and references.
- **≤50 words of natural language per frame** (math, table cells, axis labels, and figure annotations don't count). A frame that needs more is two frames.
- **Bullets carry sequential or parallel logic.** 3–5 per cluster, one idea each, parallel grammar, optionally `\textbf{Lead-in.}` form. They *cue* the speaker; they do not transcribe the script. Short — never longer than one printed line. Use `\pause` / `<+->` to reveal progressively when the argument builds.
- **For relationships (A vs B, A causes B), use a 2-column table or a labelled diagram** — not parallel bullets and not prose.
- **Italic (`\emph`, `\textit`) is for ≤3-word emphasis.** No sentence-long italics, no italic "Notation:" labels, no centered italic takeaways at frame foot. If the content matters, demote it to a bullet; if it doesn't, delete it.
- **Frame titles should be sentence-headline assertions** on content slides — `"Risk demand is elastic; preference demand is not"` beats `"Stage 2 results"`. Topic-noun titles ("Setup", "Roadmap") are fine for transitions only.
- **Two-column layouts** give the visual column ≥0.6\textwidth and the text column 2–4 short bullets that label the visual. A 50/50 split is allowed only when both columns hold visuals.
- **One strong visual per frame.** A multi-panel figure beats multiple competing small ones — bundle into a single `figures/X.tex`.

### Reformatting recipes for common prose patterns

When you find prose on a slide, convert it before keeping it. The destination is always a structured container.

| Prose pattern you found | Replace with |
|---|---|
| Running explanation of a model ("X and Y both depend on Z₁, Z₂…") | Display equation with `\underbrace{}` annotations on each term; ONE bullet stating the implication. |
| Centered italic summary line at frame foot | `\begin{block}{Takeaway} one sentence \end{block}` OR `\boxed{result}` display equation. |
| Italic mini-note ("\emph{Notation.} g denotes greenness…") | Bullet: `\item \textbf{Notation.} $g$ = greenness; empirical regressor $s = -g$.` |
| 2–3 sentence paragraph between equation and figure | Drop the prose. Annotate the equation with `\underbrace` and let the figure speak. If a claim must survive, ONE bullet below the visual. |
| Long `\emph{…}` (sentence with verb and period) | Bullet in `\textbf{Lead-in.}` form. Italic stays for ≤3-word emphasis. |
| "Validation: κ > 0.86, agreement > 95%…" written as italic note | Bullet: `\item \textbf{Validation.} $\kappa>0.86$, agreement $>95\%$.` Or a 2-row table. |
| Multi-sentence motivation introducing a frame | 2–3 bullets, each `\textbf{Lead-in.} short claim`. |
| Two parallel claims about A vs B | 2-column `\begin{tabular}` with A/B in headers. |
| Three claims that build sequentially | `enumerate`, one short clause per number, `\pause`-revealed if helpful. |

## Document structure

### Document class, title, body

```latex
\documentclass[handout,aspectratio=169,10pt]{beamer}
\input{misc/style}

\title{Title}
\date{\today}
\author{Hulai Zhang}
\institute[]{Institution Name}
\titlegraphic{\includegraphics[width=0.2\textwidth]{misc/logo.png}}

\begin{document}
\maketitle

\begin{frame}{Roadmap}
\tableofcontents
\end{frame}

\section{First Section}
% Content frames follow ...
```

Exactly one Roadmap frame after `\maketitle`.

### Two-column figure-led frame

```latex
\begin{frame}{Frame title as an assertion}
\begin{columns}[T]
\begin{column}{0.6\textwidth}
    \input{figures/diagram.tex}
\end{column}
\begin{column}{0.36\textwidth}
    \footnotesize
    \begin{itemize}
        \item Short label for the visual
        \item One-line takeaway
    \end{itemize}
\end{column}
\end{columns}
\end{frame}
```

### Block for takeaway (use sparingly)

```latex
\begin{block}{Key Takeaway}
    One sentence. No more.
\end{block}
```

## Figures and tables

Figures live in `./figures/*.tex` (TikZ source) or `./figures/*.pdf` (raster) and are pulled in via `\input{figures/X.tex}` or `\includegraphics{figures/X}`. Never put TikZ code directly in `slides.tex`.

Tables live in `./tables/*.tex` and are pulled in via `\input{tables/X}`. Use booktabs (`\toprule`/`\midrule`/`\bottomrule`), `\textbf{}` headers, and `\rowcolor{gray!10}` on alternate rows for readability:

```latex
% In tables/results.tex
\begin{table}
    \centering\footnotesize
    \renewcommand{\arraystretch}{1.2}
    \begin{tabular}{p{3cm}p{5cm}}
        \toprule
        \textbf{Column 1} & \textbf{Column 2} \\
        \midrule
        Row 1 & Data \\
        \rowcolor{gray!10}
        Row 2 & Data \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Colors

Defined in `misc/style.tex`: `red` (titles, emphasis), `blue` (enumerate, links), `forestgreen` (positive indicators), `darkred`, `steelblue`, `darkorange`, `gray!10` (table row alternation).

## Math and citations

```latex
\E[X]                                          % expectation macro
$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t}$         % inline math
\citet{author2021}                             % textual citation
\citep{author2021}                             % parenthetical citation
```

## Project layout

```
project/
├── misc/{style.tex, ref.bib, logo.png}
├── figures/
├── tables/
└── slides.tex
```

## Workflow

1. Initialize: `python ~/.claude/skills/latex/slides/scripts/init_slides.py my-talk` (or copy `misc/` and `slides_template.tex` manually).
2. Apply the operational rules and recipes above.
3. Validate: `python ~/.claude/skills/latex/slides/scripts/validate_slides.py slides.tex`. The validator is the authoritative checklist — it flags free-floating text, prose paragraphs, wordy frames (>50 words), long `\emph`/`\textit`, centered italic takeaways, bullet walls, missing visuals, and topic-noun titles. Fix every WARN; INFO items (e.g., topic-noun titles) are advisory.

## Scripts and assets

| Path | Purpose |
|---|---|
| `slides/scripts/init_slides.py` | Initialize a new project from the template |
| `slides/scripts/validate_slides.py` | Enforce the operational rules above |
| `slides/misc/style.tex` | Beamer theme, colors, fonts, custom commands |
| `slides/misc/slides_template.tex` | Full deck template |
| `slides/misc/ref.bib` | Bibliography seed |
| `slides/misc/logo.png` | Title-slide logo placeholder |
| `slides/references/style_spec.md` | Complete `style.tex` documentation |
| `slides/references/tikz_conventions.md` | TikZ figure guidelines |
