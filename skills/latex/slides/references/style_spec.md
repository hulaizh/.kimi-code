# Style.tex Specification

This document provides the complete specification for the centralized `style.tex` file used in academic finance/economics lecture slides.

## Beamer Theme and Color Configuration

### Theme Settings

```latex
\usetheme{Madrid}
\usecolortheme{beaver}
\setbeamercolor{titlelike}{bg=white}
```

**Madrid theme** provides:
- Professional appearance
- Clear section navigation
- Consistent block formatting

**Beaver color theme** provides:
- Red-based accent colors
- Clean, academic appearance
- Good contrast for readability

### Custom Color Definitions

```latex
% Primary accent color (titles, emphasis)
\definecolor{red}{RGB}{150, 0, 20}

% Secondary accent color (enumerate items, links)
\definecolor{blue}{RGB}{20, 0, 110}

% Additional colors for figures
\definecolor{darkred}{RGB}{139,0,0}
\definecolor{lightgray}{RGB}{245,245,245}
\definecolor{forestgreen}{RGB}{34,139,34}
\definecolor{steelblue}{RGB}{70,130,180}
\definecolor{darkorange}{RGB}{255,140,0}
```

### Title Color Application

```latex
\setbeamercolor{title}{fg=red}
\setbeamercolor{frametitle}{fg=red}
```

## Template Configuration

### Footer and Navigation

```latex
% Minimal footer with page numbers
\setbeamertemplate{footline}{\hspace*{0.9\textwidth} \insertframenumber/\inserttotalframenumber \vspace{0.1in}}

% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}
```

### Itemize Bullets

```latex
\setbeamertemplate{itemize item}[circle]
\setbeamertemplate{itemize subitem}[circle]
\setbeamertemplate{itemize subsubitem}[circle]

% With custom bullet style
\setbeamertemplate{itemize item}{\textbullet}
```

### Enumerate Style

```latex
\setbeamertemplate{enumerate item}{(\insertenumlabel)}
\renewcommand{\insertenumlabel}{\textcolor{blue}{\arabic{enumi}}}
\setbeamercolor{enumerate item}{fg=blue}
```

### Block Styling

```latex
\setbeamercolor{block title}{fg=red, bg=white}
\setbeamercolor{block body}{fg=black, bg=white}
```

## Font Configuration

### Main Font

```latex
\usefonttheme{serif}
\usepackage{palatino}
\usepackage[T1]{fontenc}
\usepackage[latin9]{inputenc}
```

**Palatino** is used because:
- Highly readable serif font
- Professional academic appearance
- Good math symbol integration
- Clear at various sizes

### Line Spacing

```latex
\renewcommand{\baselinestretch}{1.2}
```

## Required Packages

### Core Packages

```latex
\usepackage{array,booktabs, xcolor, graphicx, caption, subcaption}
\usepackage{amsmath,amssymb,cases,bm}
\usepackage{appendixnumberbeamer}
```

### Citation Package

```latex
\usepackage[authoryear]{natbib}
```

### TikZ Configuration

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, patterns}
```

### Table Packages

```latex
\usepackage{array}
\usepackage{multicol,multirow}
\usepackage{booktabs}
\usepackage{colortbl}
```

### Table Row Spacing

```latex
\renewcommand{\arraystretch}{0.8}  % Default (override in slides as needed)
```

### Custom Column Types

```latex
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
```

## Custom Commands

### Mathematical Notation

```latex
% Expectation operator
\newcommand{\E}{\mathbb{E}}

% Diagonal operator
\newcommand{\diag}{\text{diag}}

% Score variable
\newcommand{\score}{s}

% Environmental score
\newcommand{\Env}{\mathcal{E}}
```

### Custom Environments

```latex
\newtheorem{proposition}{Proposition}
```

## Figure Configuration

```latex
\usepackage{graphicx}
\usepackage{subcaption}
\setbeamertemplate{caption}[numbered]
```

## Complete Style.tex Template

```latex
% language
\usepackage{array,booktabs, xcolor, graphicx, caption, subcaption}
\usepackage{amsmath,amssymb,cases,bm}
\usepackage{appendixnumberbeamer}

% reference
\usepackage[authoryear]{natbib}

% Custom commands
\newcommand{\E}{\mathbb{E}}
\newcommand{\diag}{\text{diag}}
\newcommand{\score}{s}
\newcommand{\Env}{\mathcal{E}}

% format
\usepackage{geometry}
\special{papersize=\the\paperwidth,\the\paperheight}
\renewcommand{\baselinestretch}{1.2}
\usepackage{setspace}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, patterns}

% Beamer theme and color
\usetheme{Madrid}
\usecolortheme{beaver}
\setbeamercolor{titlelike}{bg=white}
\definecolor{red}{RGB}{150, 0, 20}
\setbeamercolor{title}{fg=red}
\setbeamercolor{frametitle}{fg=red}

% Beamer templates and styles
\setbeamertemplate{footline}[text line]{}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{itemize item}[circle]
\setbeamertemplate{itemize subitem}[circle]
\setbeamertemplate{itemize subsubitem}[circle]
\setbeamertemplate{footline}{\hspace*{0.9\textwidth} \insertframenumber/\inserttotalframenumber \vspace{0.1in}}

% Beamer font
\usefonttheme{serif}
\usepackage{palatino}
\usepackage[T1]{fontenc}
\usepackage[latin9]{inputenc}

% itemize style
\definecolor{blue}{RGB}{20, 0, 110}
\setbeamertemplate{enumerate item}{(\insertenumlabel)}
\renewcommand{\insertenumlabel}{\textcolor{blue}{\arabic{enumi}}}
\setbeamertemplate{itemize item}{\textbullet}
\setbeamercolor{enumerate item}{fg=blue}

% Additional colors for figures
\definecolor{darkred}{RGB}{139,0,0}
\definecolor{lightgray}{RGB}{245,245,245}
\definecolor{forestgreen}{RGB}{34,139,34}
\definecolor{steelblue}{RGB}{70,130,180}
\definecolor{darkorange}{RGB}{255,140,0}

% Block styling
\setbeamercolor{block title}{fg=red, bg=white}
\setbeamercolor{block body}{fg=black, bg=white}

% Custom environments
\newtheorem{proposition}{Proposition}

% table
\usepackage{array}
\usepackage{multicol,multirow}
\usepackage{booktabs}
\usepackage{colortbl}
\renewcommand{\arraystretch}{0.8}
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

% figure
\usepackage{graphicx}
\usepackage{subcaption}
\setbeamertemplate{caption}[numbered]
```

## Notes for Lecture Files

Individual lecture files may need additional packages:

```latex
% For euro symbol
\usepackage{eurosym}

% For chemical formulas (if needed)
\usepackage{chemformula}

% For additional TikZ libraries
\usetikzlibrary{decorations.pathreplacing}  % For braces
\usetikzlibrary{shapes.symbols}              % For cloud shapes
```

These should be added in the slides.tex preamble AFTER the `\input{misc/style}` line, not in style.tex itself.
