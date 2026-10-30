# Humanize: Academic Catalog (Layer 2 expansion — REQUIRED for academic text)

The full detail behind SKILL.md Layer 2: its compact entries 2.12–2.16 expand here (with
LaTeX detection regexes and allowed exceptions), unified with the rest of the academic
catalog as A1–A16. The 29 general patterns still apply, and the governing discipline is
Layer 4 of SKILL.md: every claim earns its number, figure, or citation, and no verb is
stronger than its evidence.

## Key Differences from General Writing

| Dimension | General writing | Academic writing |
|-----------|----------------|------------------|
| First person | Encouraged freely | Use sparingly; "we" for coauthored papers, "I" in single-author or referee reports |
| Hedging | Mostly eliminate | Appropriate when uncertainty is real ("may", "suggests"), but remove stacked hedges |
| Opinions | Inject personality | State claims with evidence; opinions belong in referee reports, not empirical sections |
| Sentence variety | Mix short and long | Aim for clarity; short is fine, but don't sacrifice precision for punchiness |
| Formality | Casual is fine | Maintain professional register throughout |

## Academic-Specific AI Patterns

### A1. Throat-Clearing and Formulaic Openers
- "This paper examines/explores/investigates the relationship between..."
- "In recent years, there has been growing interest in..." / "In recent years, X has
  attracted increasing attention."
- "With the rapid development of..." / "Despite recent advances,..."
- "A growing body of literature has focused on..."

**Fix:** Start with the finding, the question, or the structural gap — not meta-commentary
about the paper or a weather report on the field.

**Before:** "This paper investigates the causal effect of minimum wage increases on employment."
**After:** "Does raising the minimum wage reduce employment? We exploit state-level variation in..."

**Before:** "In recent years, tabular deep learning has attracted increasing attention."
**After:** "Tabular deep learning has a structural limitation: most models discard feature-type metadata and must relearn it from data."

### A2. Contribution Inflation and Clichéd Contribution Lists
- "This paper makes several important contributions to the literature"
- "We contribute to a growing body of research"; "Our findings have important implications for..."
- Contribution lists that restate the abstract: "(1) a novel method; (2) extensive
  experiments; (3) strong results."

**Fix:** Each contribution names a *specific* result. State what you do concretely; let
readers judge importance.

**Before:** "Our contributions are: (1) a novel method; (2) extensive experiments; (3) strong results."
**After:** "We (1) introduce a metadata-aware encoder that reaches 0.91 AUROC vs 0.86 for the strongest baseline; (2) show it stays within 2 points under 20% label noise where the baseline drops 9; (3) release the benchmark."

### A3. Passive Voice Pileup
- "It was found that...", "It can be argued that...", "It is shown that..."

**Fix:** Name the actor. "We find", "Table 3 shows", "Smith (2020) argues". (Passive stays
when the actor is genuinely irrelevant: "Samples were normalized to total protein.")

### A4. Hedge Stacking and Hedging-by-Vagueness
- "This could potentially suggest that there might be a possible relationship..."
- Vagueness quantifiers: "somewhat", "relatively", "fairly", "to some extent", "quite".

**Fix:** One calibrated hedge per claim; quantify or cut the vagueness words.

**Before:** "Performance is somewhat better and relatively robust."
**After:** "Accuracy is 3 points higher and varies by less than 1 point across five seeds."

### A5. Literature Review as Laundry List
- "Smith (2020) studies X. Jones (2021) finds Y. Lee (2022) examines Z."

**Fix:** Synthesize by theme, method, or finding. Group papers that reach similar conclusions.

### A6. Formulaic Transitions and Connective Overuse
- "Turning now to...", "Having established..., we now...", "Building on this analysis..."
- Consecutive sentences opening with Moreover/Furthermore/Additionally/In particular.

**Fix:** Let the logical structure carry the reader. If the connection is clear, no
transition phrase is needed.

**Before:** "Moreover, the method is fast. Furthermore, it is simple. Additionally, it scales."
**After:** "The method is fast and simple, and it scales to one million rows (Section 5)."

### A7. Empty Intensifiers and Magnifiers
- "extensive/comprehensive/thorough experiments", "a wide range of", "numerous", "various"
- "The results are striking/remarkable/noteworthy"; "a strong/robust/significant effect"
  with no number.

**Fix:** Name the datasets; report the magnitude. The reader decides whether it is striking.

**Before:** "We conduct extensive experiments on a wide range of datasets."
**After:** "We evaluate on three datasets (ImageNet, CIFAR-100, and iNaturalist)."

**Before:** "We find a strong effect."
**After:** "A one-standard-deviation increase in X raises Y by 15%."

### A8. Parenthetical t-stats and p-values in prose
- "The coefficient is $-0.004$ ($t = -8.00$)."
- "Treated firms underperform by 3.2% ($p < 0.01$)."
- "The estimate is $0.15$ ($t = 3.45$, $p = 0.001$)."

These bracketed statistical annotations read as a data dump, not argument. Top-5/Top-3 house
style keeps t-stats and p-values in table notes, and uses natural language in the running text.

**Fix:** Integrate the statistical claim into prose. Use "significant at the 1% level",
"with a t-statistic of $-3.45$", or "precisely estimated" rather than parenthetical
math-mode annotations.

**Before:** "Green investors underweight emissions-intensive stocks more than neutral investors ($t = -10.76$)."
**After:** "Green investors underweight emissions-intensive stocks more than neutral investors, with a t-statistic of $-10.76$."

**Before:** "The baseline coefficient of $0.032$ is significant at the 1% level ($t = 3.45$)."
**After:** "The baseline coefficient of $0.032$ is precisely estimated, statistically significant at the 1% level."

**Allowed exceptions:** table notes (`\textit{Notes:}` block) and results where no clean
verbal rendering exists — but these should be rare.

### A9. Italic Pseudo-Subsection Headings Followed by Throat-Clearing

LaTeX has structural commands for subparagraph headings (`\paragraph{}`,
`\subsubsection{}`). When AI-generated text wants to chunk a section without committing to
formal subsections, it falls back on an italic noun phrase masquerading as a heading,
usually followed by a "Table X reports..." opener.

**Anti-pattern:**
```latex
\medskip\noindent\textit{Reduced-Form Portfolio Weights.}

Table~\ref{tab:pw_co2} reports reduced-form regressions of log portfolio weights on NLP scores...
```

Two problems compound: the italic pseudo-heading is not a real LaTeX structural element (it
interrupts narrative flow without earning a TOC entry or anchor), and the "Table X
reports..." opener is throat-clearing that delays the actual claim. A reader skimming the
section sees three labels in a row with no connective tissue between them.

**Fix:** Write a topic sentence that introduces the next chunk *and* states the claim or
transition. The topic sentence makes the chunk's role explicit without a separate label,
and the section reads as a connected argument.

**Before:**
```latex
\medskip\noindent\textit{Demand Elasticity: Opposite Price Sensitivities.}

Table~\ref{tab:demand_elasticity} reports Stage~2 regressions where the dependent variable is the price-elasticity coefficient $\hat\beta_{0,i,t}$ from Stage~1.
```

**After:**
```latex
The level coefficient $\delta_1$ does not separate beliefs from tastes: both channels can produce a negative loading on emissions intensity for different reasons. The price-elasticity coefficient $\delta_0$ does separate them, and we turn to it now. Table~\ref{tab:demand_elasticity} reports Stage~2 regressions where the dependent variable is the price-elasticity coefficient $\hat\beta_{0,i,t}$ from Stage~1.
```

**`\paragraph{Heading.}` is not a clean substitute.** LaTeX's `\paragraph{Title.}` renders
as a bold inline heading followed by descriptive text on the same line — visually and
rhetorically the same heading-then-prose pattern that A9 and A10 are trying to eliminate.
The bold-noun-phrase-then-prose signature is what reads as machine-generated, regardless of
whether the LaTeX command is `\medskip\noindent\textit{}`, `\textbf{Label.}`, or
`\paragraph{Title.}`. In narrative sections, the only clean fix is to drop the heading
entirely and write a topic sentence.

**Allowed exception: proof scaffolding.** Inside theorem-proof environments, the convention
`\medskip\noindent\textit{Proof of Proposition X.}\phantomsection\label{pf:X}` is
established mathematical typography, not narrative throat-clearing. The label anchors the
proof for cross-referencing from the main text, and the italic marker signals a formal proof
block. This exception does not extend to derivation step markers in narrative theory
sections (which should use topic sentences) or to proposition wrappers (the
`\begin{proposition}` heading is itself sufficient).

**Detection regex:** `\\medskip\\s*\\noindent\\s*\\textit\{[^}]+\.\}\\s*\\n\\s*\\n\\s*Table~\\\\ref` — italic pseudo-heading immediately followed by a "Table~\ref{...}" opener.

### A10. Bold Label + Description (Pseudo-Bullet) Patterns

Closely related to A9. AI text often uses `\textbf{Label.} Description...` as inline
pseudo-bullets, especially inside numbered contribution lists or methodology summaries.

**Anti-pattern:**
```latex
\begin{itemize}
\item \textbf{Dependent variable.} The dependent variable is log portfolio weight.
\item \textbf{Sample.} Our sample covers 2011Q1--2024Q4.
\item \textbf{Identification.} Identification comes from cross-sectional variation.
\end{itemize}
```

This reads as a presentation slide pasted into a paper. Top finance journals do not use this
format — variable definitions belong in the data section as prose, identification belongs
in the methodology section as prose. The `\textbf{Label.}` opener is the same
throat-clearing problem as A9 in a different costume.

**Fix:** Convert each pseudo-bullet to a paragraph (or sentence) of prose. Define variables
in running text. Describe the sample in a sentence. State the identification in a connected
paragraph.

**Before:**
```latex
We make three contributions. \textbf{First, measurement.} We develop a new NLP measure. \textbf{Second, identification.} We propose a new instrument. \textbf{Third, decomposition.} We decompose the green premium.
```

**After:**
```latex
We make three contributions. First, we develop investor-level NLP measures of climate risk perception and green preference from mandatory Form ADV filings — the first regulatory-text source for this construct. Second, we propose a leave-one-out market-cap instrument that breaks the simultaneity between holdings and prices. Third, we decompose the equilibrium green premium into a belief contribution of $+3.6$ log points and a taste contribution of $-2.0$ log points.
```

**Allowed exceptions:**
- Theorem/proposition/lemma environments where `\textbf{Proof.}` or `\textbf{Theorem 1.}`
  are established mathematical conventions.
- Table captions where `\textbf{Panel A.}` / `\textbf{Notes.}` labels separate panels or
  annotation blocks from the main body — these are caption-internal formatting, not
  running-text headings.
- Algorithm-listing environments and pseudocode.

**Detection regex:** `\\textbf\{[A-Z][^}]*\.\}` immediately followed by descriptive prose
(not inside `\caption{}`, theorem environments, or algorithm listings). Particularly suspect
inside `\begin{itemize}` / `\begin{enumerate}` blocks and at the start of paragraphs.

### A11. Crutch Positioning Adjectives

A single positioning adjective — **"headline"**, "key", "central", "main", "crucial",
"core", "primary" — repeated across many different nouns as an all-purpose label for "the
thing that matters." Once is idiomatic ("our headline result"); the tell is the monotone
reuse. A human author varies the word to the referent: *preferred* specification, *baseline*
estimate, *main-text* coefficient, or simply names it (column 4, the Fama-MacBeth estimate).
The model instead bolts one adjective onto everything because it was primed with that word
as house vocabulary.

This is the mirror image of general pattern #11 (synonym cycling): synonym cycling rotates
*too many* labels for one concept; the crutch adjective applies *one* label to too many
concepts. Both read as machine-generated.

The signature is range, not just count: the same adjective attached to structurally unlike
nouns. From one real draft, "headline" appeared on *coefficient, specification,
Fama-MacBeth, standard-error object, control vector, price-elasticity results, pattern,
number* — eighteen times in one paper. No finance author writes "the headline
standard-error object."

**Fix:** Keep at most one use, for the genuine lead result. Replace the rest with the
specific referent — the noun already carries the meaning, so the adjective is usually
deletable:
- "the headline preference coefficient $\delta_1^P$" → "the preferred-specification coefficient $\delta_1^P$" or just "$\delta_1^P$ (column 4)"
- "the headline Fama-MacBeth specification" → "the Fama-MacBeth specification with active-management controls" (the qualifier already identifies it)
- "the headline standard-error object is the bootstrap" → "our primary standard error is the bootstrap"
- "confirms that the headline pattern is not an artifact" → "confirms that this is not an artifact"

**Allowed exceptions:** a single, deliberate use to flag the paper's lead result ("our
headline finding is..."); table *labels*/captions where one short tag distinguishes the main
row from robustness rows. The rule targets repetition in *running prose*, not a one-off or a
column tag.

**Detection heuristic:** count occurrences of each of {headline, key, central, crucial,
core, primary, main} as a pre-nominal adjective within a section; flag any that occurs **3+
times**. Inspect the attached nouns — if they are structurally diverse (a coefficient *and*
a specification *and* a standard error), it is a crutch, not a consistent term of art.

**Companion — vague crutch verbs (esp. "read").** The verb analog of the crutch adjective
is a vague verb standing in for a concrete operation. **"Read" as a drafting verb is
banned in ALL its uses** — "read", "read off", "reads off", "reading", "read through/into",
"we rest the reading on" — every one is a soft metaphor an AI drafts where a human names
the operation. **Fix by naming the operation:** extract-from-text → *extracted from*;
recover-a-coefficient/quantity → *recovered from* / *comes from* / *estimated from* /
*taken from*; interpret-a-result → *interpret ... as* / *treat ... as*;
infer-from-evidence → *inferred from*; derivation "reading off the slopes" → *collecting
the slopes*; "we rest the reading on" → *we rest the case on*. The noun **"reader" (the
person) is fine** ("the reader may wonder..."). Same logic extends to other vague stand-in
verbs (*leverage, capture, drive, speak to, get at*) when they replace a nameable
operation — for those, treat as a crutch when the construction recurs (**3+ per section**)
or a concrete verb is obviously available; for "read" the ban is unconditional.

### A12. Over-Claiming Verbs

Empirical work *shows* and *provides evidence*; it does not *prove* or *demonstrate*
universal truths.

**Watch:** demonstrate, prove, establish, confirm, guarantee; "significantly" with no
test/number.

**Before:** "We prove that our method significantly outperforms all prior approaches."
**After:** "Our method improves held-out accuracy by 4–7 points over the strongest prior approach (Table 3); the gain is significant at p < 0.01 by a paired test."

### A13. Significance Hype

**Watch:** paves the way for, a crucial/pivotal step toward, has the potential to
revolutionize, opens new avenues, sheds light on, of paramount importance, bridges the gap.

**Before:** "This work paves the way for a new paradigm and sheds light on a problem of paramount importance."
**After:** "This work addresses one failure mode of prior methods: error accumulation under long-horizon rollout (Section 4)."

### A14. Novelty Padding

**Watch:** "novel" used more than once per section; "to the best of our knowledge"; "for
the first time".

**Before:** "We propose a novel framework and, to the best of our knowledge, are the first to study this."
**After:** "We study online calibration under delayed labels, which prior calibration work (offline) does not address."

### A15. Citation Dumping

Cite the one or two works that matter and say why, not a bracketed list.

**Before:** "Many methods exist [3, 7, 9, 12, 15]."
**After:** "The closest prior method is TabNet [7], which encodes all features jointly; we instead condition on feature-type metadata."

### A16. Overlong, Clause-Stacked Sentences

AI favors long sentences that chain three or four clauses with commas and "which", "that",
"while", "with". **Watch:** sentences past ~30 words, or with 3+ subordinate clauses.

**Fix:** Split them — one idea per sentence — and cut subordinate clauses that carry no weight.

**Before:** "Existing methods, though promising, are largely empirical, with unclear principles underpinning their behavior, which limits their reliability and further progress."
**After:** "Existing methods stay empirical. Their principles are unclear, which limits reliability and progress."

## By Document Type

### Research Papers
- Apply all 29 general patterns + A1–A16 above + SKILL.md Layer 4 (claim-evidence discipline)
- Hedging is appropriate when warranted by identification strategy
- "We" is standard for coauthored empirical work
- Keep promotional language out of abstracts and introductions
- Report magnitudes, not adjectives
- Close prefixed words per journal house style (reestimate, nonlinear, subsample); see pattern 13

### Referee Reports
- Apply patterns 1-7 (content), 13 (dashes & hyphens), 19-24 (communication/filler) + A4, A12
- Be direct: "The identification strategy is unconvincing because..." not "It could potentially be argued that..."
- First person is natural: "I am not convinced that..."
- Skip patterns 14-17 (formatting patterns less relevant for reports)

### Literature Reviews
- Apply patterns 1, 3, 5, 7, 10, 11, 22, 23 most heavily + A15
- Pattern A5 (laundry list) is the dominant failure mode
- Synthesize by theme, not paper-by-paper
- Vague attributions (#5) are especially damaging -- always cite specifically

### Response to Referees
- Apply patterns 19, 21, 22, 23 (communication patterns)
- Respectful but direct: avoid sycophantic agreement with referee points you disagree with
- No filler: "We have revised the paper to address this concern" not "We greatly appreciate the reviewer's insightful suggestion and have thoroughly revised..."

### Funding Proposals
- Different register and discipline entirely — the full protocol is SKILL.md Layer 6
  (structure maps, first-pages primacy, weak moves, claim ↔ feasibility, funded-proposal
  craft); worked examples in [proposal_examples.md](proposal_examples.md). Do NOT apply
  the paper layers' trimming to vision statements.
- 国自然/中文 proposals: also read [chinese.md](chinese.md) Part D.

## Worked example (academic register, end to end)

**Before (AI tells + over-claim):**
> In recent years, graph representation learning has attracted increasing attention. In this
> paper, we propose a novel method and demonstrate through extensive experiments that it
> significantly outperforms existing approaches, paving the way for a new paradigm. To the
> best of our knowledge, this is the first work to delve into this crucial problem.

**After (academic-humanized):**
> Existing graph methods for imbalanced node classification reweight the loss but ignore
> label noise. We add a noise-aware reweighting term and evaluate it on three citation
> benchmarks, where it improves minority-class F1 by 3-6 points over focal loss while
> leaving majority-class accuracy within 1 point.

What changed: removed the formulaic opener, "novel", "extensive", "significantly"
(unquantified), "paving the way", and "to the best of our knowledge"; downgraded
"demonstrate" to "evaluate"; attached a range and the comparator; kept the precise factual
claims.
