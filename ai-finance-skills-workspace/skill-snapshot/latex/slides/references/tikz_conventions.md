# TikZ Figure Conventions

This document specifies conventions for creating TikZ figures in academic finance/economics lecture slides.

## File Organization

### Directory Structure

```
project/
├── slides.tex            # Main slides file
├── misc/
│   ├── style.tex
│   ├── references.bib
│   └── logo.png
├── figures/
│   ├── concept_diagram.tex
│   ├── timeline.tex
│   ├── comparison_bars.tex
│   └── ...
└── tables/
```

### Naming Conventions

- Use descriptive snake_case names
- Prefix with topic or paper name for clarity
- Examples:
  - `greenium_concept.tex`
  - `painter_maturity_effect.tex`
  - `gb_market_growth_bars.tex`
  - `coase_trading.tex`

## Basic Figure Template

```latex
% Description of what this figure shows
\begin{tikzpicture}[scale=0.8]
    % Define any custom styles inline
    \tikzstyle{mybox}=[rectangle, draw=blue, fill=blue!10, rounded corners]

    % TikZ drawing code
    % Include comments explaining calculations/coordinates

\end{tikzpicture}
```

## Scale Guidelines

| Figure Complexity | Recommended Scale |
|-------------------|-------------------|
| Simple (2-3 elements) | 0.8-1.0 |
| Medium (4-6 elements) | 0.7-0.8 |
| Complex (7+ elements) | 0.6-0.7 |
| Full-width diagrams | 0.5-0.6 |

## Color Usage

### Primary Colors (from style.tex)

```latex
% Use these colors directly
blue        % (20, 0, 110) - curves, links, enumerate
red         % (150, 0, 20) - emphasis, important
forestgreen % (34, 139, 34) - positive, environmental
gray!60     % Medium gray - secondary elements
```

### Color Opacity

```latex
% For fills, use opacity modifiers
\fill[blue, fill opacity=0.3] (0,0) rectangle (2,4);
\fill[red, opacity=0.2] (0,0) -- (1,1) -- (2,0) -- cycle;
```

### Standard Color Combinations

| Element Type | Line Color | Fill Color |
|--------------|------------|------------|
| Positive/Green | forestgreen | black!60!green, opacity=0.3 |
| Negative/Risk | red | red, opacity=0.2 |
| Neutral | blue | blue!10 |
| Background | gray!60 | gray!60, fill opacity=0.3 |

## Common Figure Types

### 1. Economic Diagrams (Supply/Demand)

```latex
\begin{tikzpicture}[scale=0.6]
% Axes
\draw[->,thick] (0,0) -- (6.5,0) node[right] {$Q$};
\draw[->,thick] (0,0) -- (0,5.5) node[above] {$P$};

% Curves
\draw[thick,blue] (0.5,0.8) -- (5.5,3.2) node[right,font=\small] {MC};
\draw[thick,forestgreen] (0.5,4.5) -- (5.5,1) node[right,font=\small] {$D$};

% Equilibrium point
\filldraw[blue] (3.0, 2.5) circle (3pt);
\node[below,font=\scriptsize] at (3.0, 2.5) {$Q^*$};

% Shaded area (deadweight loss, surplus, etc.)
\fill[red,opacity=0.2] (2.0, 2.0) -- (3.0, 2.5) -- (3.0, 3.0) -- cycle;
\end{tikzpicture}
```

### 2. Comparison Bar Charts

```latex
\begin{tikzpicture}[scale=0.8]
% Bars
\fill[gray!60, fill opacity=0.3] (0,0) rectangle (2,4);
\fill[black!60!green, fill opacity=0.3] (4,0) rectangle (6,3.5);

% Labels
\node[below, font=\small] at (1,0) {Category A};
\node[below, font=\small] at (5,0) {Category B};

% Value labels
\node[above, font=\small] at (1,4) {$y_A$};
\node[above, font=\small] at (5,3.5) {$y_B$};

% Difference arrow
\draw[<->, thick, red] (6.5,3.5) -- (6.5,4);
\node[right, font=\small, red] at (6.6,3.75) {$\Delta < 0$};

% Axes
\draw[thick, ->] (-0.5,0) -- (-0.5,5) node[above, font=\small] {Value};
\draw[thick, ->] (-0.5,0) -- (7,0);
\end{tikzpicture}
```

### 3. Timelines

```latex
\begin{tikzpicture}[scale=0.9]
% Main timeline
\draw[thick, ->] (0,0) -- (12,0);

% Year markers
\foreach \x/\year in {0/2007, 3/2013, 6/2016, 9/2020, 11/2024} {
    \draw[thick] (\x,0.1) -- (\x,-0.1);
    \node[below, font=\scriptsize] at (\x,-0.2) {\year};
}

% Events (alternating above/below)
\node[above, font=\scriptsize, text width=2cm, align=center] at (0,0.3) {First Event};
\node[below, font=\scriptsize, text width=2cm, align=center] at (3,-0.5) {Second Event};
\node[above, font=\scriptsize, text width=2cm, align=center] at (6,0.3) {Third Event};
\end{tikzpicture}
```

### 4. Flowcharts

```latex
\begin{tikzpicture}[
    scale=0.8,
    box/.style={rectangle, draw=blue, fill=blue!10, rounded corners,
                minimum width=2.5cm, minimum height=0.8cm, font=\small},
    arrow/.style={->, thick, >=stealth}
]

% Nodes
\node[box] (step1) at (0,0) {Step 1};
\node[box] (step2) at (4,0) {Step 2};
\node[box] (step3) at (8,0) {Step 3};

% Arrows
\draw[arrow] (step1) -- (step2);
\draw[arrow] (step2) -- (step3);

% Labels on arrows
\node[above, font=\scriptsize] at (2,0.1) {Process};
\end{tikzpicture}
```

### 5. Concept Maps

```latex
\begin{tikzpicture}[
    scale=0.7,
    concept/.style={ellipse, draw=blue, fill=blue!10,
                    minimum width=2cm, minimum height=1cm, font=\small},
    subcon/.style={rectangle, draw=gray, fill=gray!10,
                   rounded corners, font=\scriptsize}
]

% Central concept
\node[concept] (main) at (0,0) {Main Concept};

% Sub-concepts
\node[subcon] (sub1) at (-3,-2) {Sub 1};
\node[subcon] (sub2) at (0,-2) {Sub 2};
\node[subcon] (sub3) at (3,-2) {Sub 3};

% Connections
\draw[->] (main) -- (sub1);
\draw[->] (main) -- (sub2);
\draw[->] (main) -- (sub3);
\end{tikzpicture}
```

### 6. Pie Charts

```latex
\begin{tikzpicture}[scale=0.8]
% Define data (must sum to 360)
\def\angleA{144}  % 40%
\def\angleB{108}  % 30%
\def\angleC{72}   % 20%
\def\angleD{36}   % 10%

% Draw slices
\fill[blue!70] (0,0) -- (0:2) arc (0:\angleA:2) -- cycle;
\fill[forestgreen!70] (0,0) -- (\angleA:2) arc (\angleA:\angleA+\angleB:2) -- cycle;
\fill[red!70] (0,0) -- (\angleA+\angleB:2) arc (\angleA+\angleB:\angleA+\angleB+\angleC:2) -- cycle;
\fill[gray!70] (0,0) -- (\angleA+\angleB+\angleC:2) arc (\angleA+\angleB+\angleC:360:2) -- cycle;

% Labels (positioned at midpoint of each arc)
\node[font=\small] at (72:1.3) {40\%};
\node[font=\small] at (198:1.3) {30\%};
\node[font=\small] at (270:1.3) {20\%};
\node[font=\small] at (342:1.3) {10\%};
\end{tikzpicture}
```

## Text and Labels

### Font Sizes

```latex
\node[font=\tiny] ...       % Very small annotations
\node[font=\scriptsize] ... % Small labels
\node[font=\small] ...      % Standard labels (DEFAULT)
\node[font=\normalsize] ... % Larger labels
```

### Text Positioning

```latex
% Relative to node
\node[above] at (x,y) {text};
\node[below] at (x,y) {text};
\node[left] at (x,y) {text};
\node[right] at (x,y) {text};
\node[above right] at (x,y) {text};

% With offset
\node[above=0.3cm] at (x,y) {text};
```

### Multi-line Labels

```latex
\node[text width=3cm, align=center] at (x,y) {First line\\Second line};
```

## Mathematical Labels

```latex
% Inline math in labels
\node at (x,y) {$P = \sum C/(1+r)^t$};

% Greek letters
\node at (x,y) {$\alpha$, $\beta$, $\gamma$};

% Subscripts/superscripts
\node at (x,y) {$Q^*$, $P_0$};
```

## Arrow Styles

```latex
% Standard arrow
\draw[->] (0,0) -- (2,0);

% Thick arrow
\draw[->, thick] (0,0) -- (2,0);

% Double-headed arrow
\draw[<->] (0,0) -- (2,0);

% Stealth arrow (pointed)
\draw[->, >=stealth] (0,0) -- (2,0);

% Colored arrow
\draw[->, thick, red] (0,0) -- (2,0);
```

## Decorations

### Braces

```latex
\usetikzlibrary{decorations.pathreplacing}

\draw[decorate, decoration={brace, amplitude=5pt}] (0,0) -- (2,0)
    node[midway, below=5pt] {Label};
```

### Dashed Lines

```latex
\draw[dashed] (0,0) -- (2,2);
\draw[dotted] (0,0) -- (2,2);
\draw[dash pattern=on 5pt off 3pt] (0,0) -- (2,2);
```

## Including in Slides

### Basic Include

```latex
\begin{frame}{Frame Title}
\begin{center}
\input{figures/diagram.tex}
\end{center}
\end{frame}
```

### Scaled Include

```latex
\begin{center}
\resizebox{0.75\textwidth}{!}{\input{figures/diagram.tex}}
\end{center}
```

### In Two-Column Layout

```latex
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{center}
\input{figures/diagram.tex}
\end{center}
\end{column}
\begin{column}{0.48\textwidth}
% Explanation text
\end{column}
\end{columns}
```

## Debugging Tips

### Show Bounding Box

```latex
\begin{tikzpicture}[show background rectangle]
% Your code
\end{tikzpicture}
```

### Grid Overlay

```latex
\begin{tikzpicture}
\draw[help lines, step=1] (-1,-1) grid (10,6);
% Your code
\end{tikzpicture}
```

### Coordinate Labels

```latex
\foreach \x in {0,1,2,3,4,5} {
    \foreach \y in {0,1,2,3} {
        \node[font=\tiny, gray] at (\x,\y) {(\x,\y)};
    }
}
```

## Common Mistakes to Avoid

1. **Hardcoding colors** - Always use named colors from style.tex
2. **Missing scale** - Always include `scale=X` for consistent sizing
3. **Undefined styles** - Define all custom styles inline in the figure file
4. **Missing comments** - Document calculations and coordinate logic
5. **Inconsistent fonts** - Use `\small` or `\scriptsize` for all labels
6. **Poor contrast** - Ensure text is readable against fills
7. **Crowded labels** - Use adequate spacing between elements
