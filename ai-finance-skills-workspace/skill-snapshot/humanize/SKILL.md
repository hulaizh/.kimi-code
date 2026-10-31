---
name: humanize
allowed-tools: Read, Edit, Write, Grep, Glob, AskUserQuestion
license: MIT
description: "Use when making AI-assisted prose read like a careful human wrote it — 'humanize this', 'sounds like ChatGPT/AI', 'too robotic', 'de-slop', 'clean up the AI tone', 去AI味/降AI痕迹 (English and Chinese): strips slop vocabulary, em-dash overuse, rule-of-three and the other Wikipedia 'Signs of AI writing' patterns; for ACADEMIC prose also enforces claim-evidence discipline and venue voice; for FUNDING-PROPOSAL prose (NSF, NIH, 国自然) polishes register and claim-feasibility WITHOUT flattening vision. The final anti-AI pass after gan:draft, literature-review, referee reports or copy-editor. Never changes a number, result or citation. NOT for grammar/clarity copy-editing (use copy-editor); NOT for new prose or sections (use gan:draft); NOT for structuring a point-by-point R&R response to referees (use rr — humanize only polishes replies that already exist); NOT for drafting or restructuring grant sections (use apply-fund)."
---

# Academic Humanizer

Improve the clarity and voice of AI-assisted *academic* writing while keeping the precise,
evidence-bound voice that scholarship requires and matching the author's own style. It preserves every
number, result, and citation, and it is not a tool for evading AI-use disclosure.

## When to use
Editing or reviewing academic prose: paper sections, abstracts, rebuttals, related work, and **funding
proposals** (NSF Project Summary/Description, NIH Specific Aims, fellowship and foundation proposals;
see Layer 6). **Not** for blogs, marketing, or personal essays, and **never** inject opinion, humor, or
first-person "personality" into a manuscript. For technical writing, neutral and precise *is* the human
voice. One caveat for proposals: their register is different from a paper's, since they are sold on
vision and feasibility, so the ambition language a paper would trim is appropriate there; apply Layer 6,
not the paper layers' stricter trimming, to vision statements.

Two explicit extensions of that scope:
- **中文 text** (papers, 国自然, or any prose): read [references/chinese.md](references/chinese.md)
  FIRST — the English tells below are English-native; Chinese AI 味 comes mainly from
  结构骨架/套话/翻译腔/的的不休, which that file covers (and it notes which English patterns drop in
  Chinese).
- **An explicit de-AI request on existing general prose** ("humanize this", "de-slop", "sounds like
  ChatGPT") IS in scope even for non-academic text: apply Layer 1 + the general-prose voice note in
  Layer 5, and never carry the academic register into it.

## Core principle
Academic writing already has a correct human voice: neutral, precise, third-person plural ("we"), every
claim tied to its evidence. The job is to (1) strip the AI *tells* without casualizing, and (2) enforce
the discipline a general humanizer misses: **every claim earns its number, figure, or citation, and no
verb is stronger than its evidence.**

## Process
1. **Read** the manuscript and any author writing sample; note the language (中文 →
   [references/chinese.md](references/chinese.md) FIRST, including its quality-score rubric) and the
   document type (paper vs. funding proposal vs. general prose) and the target venue or funding agency.
   For proposals, also apply Layer 6 and preserve appropriate vision. For academic text,
   [references/academic.md](references/academic.md) is REQUIRED reading.
2. **Audit** (do not edit yet): list each detected pattern with its location and proposed fix, and each
   empirical claim's evidence status. Scan against the full must-scan checklist in
   [references/patterns.md](references/patterns.md) on every non-trivial pass — the Layer 1 catalog
   below is the summary, not the whole list.
3. **Rewrite**: same structure and content, all claims and citations preserved, tells removed, over-claims
   matched to evidence, legitimate hedging kept.
4. **Report**: cleaned text plus a short change log (patterns removed, claims softened or given evidence
   pointers, voice notes). Cover everything the original covered: if it had five paragraphs, so does the
   rewrite. For longer texts, run the two-pass audit before finalizing (see Output).

---

## Layer 1: General AI-tell catalog
Scan for and fix the general patterns, subject to the academic exceptions in Layer 3:
inflated significance ("marking a pivotal moment"); superficial "-ing" tails that fake depth
("..., highlighting..."); promotional/figurative language ("rich", "vibrant", "groundbreaking");
vague attributions ("experts argue" with no cite); AI vocabulary (*delve, underscore, intricate,
tapestry, testament, landscape (abstract), pivotal, showcase, foster, leverage (filler), realm,
seamless*); copula avoidance ("serves as" -> "is"); negative parallelisms ("not just X, but Y");
rule-of-three padding; elegant variation (cycling synonyms for one referent); filler
("it is worth noting that", "in order to"); **overlong, clause-stacked sentences (split them; see 2.11)**;
and **em-dashes (remove entirely; recast with commas, colons, parentheses, or separate sentences)**.

**Before:** *Additionally, an enduring testament to the method's value is its ability to delve into
intricate dependencies, showcasing a seamless integration that underscores its pivotal role.*
**After:** *The method also captures higher-order dependencies, which the baselines miss (Table 2).*

This paragraph is the summary. The **full 29-pattern must-scan checklist** — including the classes it
compresses away (notability name-dropping, false ranges, chatbot artifacts, knowledge-cutoff
disclaimers, sycophancy, generic conclusions, section-ending summaries, hourglass structure, boldface
and bold-lead-sentence overuse, inline-header lists, Title Case headings, emojis, curly quotes,
horizontal-rule separators, and the full dash-and-hyphen typography rules: en dashes for ranges,
prefix closure, noun-compound opening, -ly-adverb hyphens) — lives in
[references/patterns.md](references/patterns.md) with before/after examples; scan against it on every
non-trivial pass. The no-em-dash rule above governs academic and proposal prose; in general prose,
apply the checklist's em-dash *overuse* rule instead.

---

## Layer 2: Academic AI tells (remove or fix)

### 2.1 Over-claiming verbs
Empirical work *shows* and *provides evidence*; it does not *prove* or *demonstrate* universal truths.
**Watch:** demonstrate, prove, establish, confirm, guarantee; "significantly" with no test/number.
**Before:** *We prove that our method significantly outperforms all prior approaches.*
**After:** *Our method improves held-out accuracy by 4--7 points over the strongest prior approach
(Table 3); the gain is significant at p < 0.01 by a paired test.*

### 2.2 Significance hype
**Watch:** paves the way for, a crucial/pivotal step toward, has the potential to revolutionize, opens
new avenues, sheds light on, of paramount importance, bridges the gap.
**Before:** *This work paves the way for a new paradigm and sheds light on a problem of paramount
importance.*
**After:** *This work addresses one failure mode of prior methods: error accumulation under long-horizon
rollout (Section 4).*

### 2.3 Empty intensifiers
**Watch:** extensive/comprehensive/thorough experiments, a wide range of, numerous, various.
**Before:** *We conduct extensive experiments on a wide range of datasets.*
**After:** *We evaluate on three datasets (ImageNet, CIFAR-100, and iNaturalist).*

### 2.4 Novelty padding
**Watch:** "novel" used more than once per section; "to the best of our knowledge"; "for the first time".
**Before:** *We propose a novel framework and, to the best of our knowledge, are the first to study this.*
**After:** *We study online calibration under delayed labels, which prior calibration work (offline) does
not address.*

### 2.5 Formulaic openers
**Watch:** "In recent years, X has attracted increasing attention"; "With the rapid development of...";
"Despite recent advances,..."; "This paper examines/explores/investigates...".
**Before:** *In recent years, tabular deep learning has attracted increasing attention.*
**After:** *Tabular deep learning has a structural limitation: most models discard feature-type metadata
and must relearn it from data.*

### 2.6 Connective overuse
Do not start consecutive sentences with Moreover/Furthermore/Additionally/In particular; let logic carry.
**Before:** *Moreover, the method is fast. Furthermore, it is simple. Additionally, it scales.*
**After:** *The method is fast and simple, and it scales to one million rows (Section 5).*

### 2.7 Contribution-list cliches
Each contribution names a *specific* result, not a restatement of the abstract.
**Before:** *Our contributions are: (1) a novel method; (2) extensive experiments; (3) strong results.*
**After:** *We (1) introduce a metadata-aware encoder that reaches 0.91 AUROC vs 0.86 for the strongest
baseline; (2) show it stays within 2 points under 20% label noise where the baseline drops 9; (3) release
the benchmark.*

### 2.8 Citation dumping
Cite the one or two works that matter and say why, not a bracketed list.
**Before:** *Many methods exist [3, 7, 9, 12, 15].*
**After:** *The closest prior method is TabNet [7], which encodes all features jointly; we instead
condition on feature-type metadata.*

### 2.9 Hedging-by-vagueness
**Watch:** somewhat, relatively, fairly, to some extent, quite. Quantify or cut.
**Before:** *Performance is somewhat better and relatively robust.*
**After:** *Accuracy is 3 points higher and varies by less than 1 point across five seeds.*

### 2.10 Boilerplate emphasis
**Watch:** "It is worth noting that", "It should be emphasized that", "Notably,", "Importantly,".
If it matters, the sentence shows it.
**Before:** *It is worth noting that, importantly, the gain holds across scenarios.*
**After:** *The gain holds across all three scenarios (Table 4).*

### 2.11 Overlong, clause-stacked sentences
AI favors long sentences that chain three or four clauses with commas and "which", "that", "while", "with".
Split them: one idea per sentence, and cut subordinate clauses that carry no weight. **Watch:** sentences
past ~30 words, or with 3+ subordinate clauses.
**Before:** *Existing methods, though promising, are largely empirical, with unclear principles
underpinning their behavior, which limits their reliability and further progress.*
**After:** *Existing methods stay empirical. Their principles are unclear, which limits reliability and
progress.*

### 2.12 Passive-voice pileup
**Watch:** "It was found that...", "It can be argued that...", "It is shown that...".
**Before:** *It was found that the treatment effect is concentrated in small firms.*
**After:** *We find the treatment effect is concentrated in small firms (Table 5).*
Name the actor: "We find", "Table 3 shows", "Smith (2020) argues". (Passive stays when the actor is
genuinely irrelevant — Layer 3.)

### 2.13 Literature review as laundry list
**Watch:** "Smith (2020) studies X. Jones (2021) finds Y. Lee (2022) examines Z."
**Fix:** synthesize by theme, method, or finding; group papers that reach similar conclusions
(full guidance: [references/academic.md](references/academic.md) A5).

### 2.14 Parenthetical t-stats and p-values in prose
**Watch:** "The coefficient is $-0.004$ ($t = -8.00$)"; "underperform by 3.2% ($p < 0.01$)".
Top-5/top-3 house style keeps t-stats and p-values in table notes; the running text argues in natural
language.
**Before:** *Green investors underweight emissions-intensive stocks more than neutral investors ($t = -10.76$).*
**After:** *Green investors underweight emissions-intensive stocks more than neutral investors, with a
t-statistic of $-10.76$.*
(Exceptions and detail: [references/academic.md](references/academic.md) A8.)

### 2.15 Pseudo-headings and pseudo-bullets (LaTeX)
**Watch:** `\textit{Label.}` italic pseudo-subsection headings followed by "Table X reports..."
throat-clearing; `\textbf{Label.} description` inline pseudo-bullets in narrative sections — a
presentation slide pasted into a paper.
**Fix:** drop the label and write a topic sentence that states the claim or transition; convert
pseudo-bullets to connected prose. Detection regexes and the allowed exceptions (proof scaffolding,
`\textbf{Panel A.}` captions, theorem environments, algorithms):
[references/academic.md](references/academic.md) A9–A10.

### 2.16 Crutch positioning adjectives
**Watch:** one adjective — "headline", "key", "central", "main", "crucial", "core", "primary" — bolted
onto structurally unlike nouns 3+ times per section (a coefficient *and* a specification *and* a
standard-error object). The mirror image of elegant variation: one label for too many concepts.
**Fix:** keep at most one use for the genuine lead result; elsewhere name the referent ("column 4", "the
Fama-MacBeth estimate") — the noun already carries the meaning. (Detection heuristic and worked
examples: [references/academic.md](references/academic.md) A11.)

For academic text, [references/academic.md](references/academic.md) is REQUIRED reading: it carries the
full merged catalog (A1–A16) with LaTeX detection regexes and allowed exceptions, plus the
by-document-type maps (research papers / referee reports / literature reviews / responses to referees).

---

## Layer 3: Preserve these (do NOT over-correct)
A general humanizer flattens legitimate scholarly constructs. Keep them.

- **Evidence-tied hedging is correct and required.** Keep "suggests", "is consistent with", "we
  hypothesize that", "may indicate", "appears to" when the claim is genuinely uncertain.
  *Wrong fix:* turning *"the results suggest X"* into *"the results prove X"*: this manufactures
  over-claiming. Keep the calibrated verb.
- **Passive voice** is fine when the actor is irrelevant: *"Samples were normalized to total protein."*
- **First-person plural "we"** is standard; do not rewrite to avoid it.
- **Semicolons and an occasional triple** are fine in moderation. Em-dashes are the exception: remove
  them entirely (Layer 1), recasting with commas, colons, parentheses, or separate sentences.
- **Formal definitions, named methods/metrics, technical terms, equations, and symbols** stay verbatim.
- **Established scholarly typography** stays: proof scaffolding
  (`\textit{Proof of Proposition X.}`), `\textbf{Panel A.}` / `\textbf{Notes.}` inside table captions,
  theorem/proposition environments, and algorithm listings (see academic.md A9/A10 exceptions).
- **Never invent, drop, or alter a number, equation, or citation.** Same content; preserve every cite key.

---

## Layer 4: Claim-evidence discipline
For every empirical claim, check (a) is it backed by a number, figure, table, or citation in the text,
and (b) does the verb match the strength of that evidence?

- **Unbacked claim -> add the evidence pointer or soften.**
  *Before:* *Our method is more robust.*  *After:* *Our method's accuracy drops by 2 points under
  distribution shift, versus 11 points for the baseline (Figure 3).*
- **Verb stronger than evidence -> downgrade.**
  *Before:* *This demonstrates that our method is universally superior.*
  *After:* *On these three datasets, our method matches or exceeds the strongest baseline (Table 2).*
- **Vague magnitude -> a number or RANGE, attributed.**
  *Before:* *a large improvement.*  *After:* *a 2--6% improvement in balanced accuracy over the strongest
  baseline.*
  Prefer ranges (e.g., "2--6%") over single averaged values unless the averaging method is stated, and
  attribute each number to its method, metric, and baseline. When comparing, lead with the comparison
  against the strongest competitor, not the trivial baseline.

---

## Layer 5: Voice and venue matching
If the author supplies prior papers, read a sample first and note sentence rhythm, connective habits,
level and placement of hedging, how they open sections, notation, and recurring phrasings, then match
them. Match the venue's register too (e.g., ICLR/NeurIPS: terse, direct, results-forward; Nature/PNAS:
more expository; top-5 econ / top-3 finance: terse, direct, magnitudes in prose, statistics in table
notes). Absent a sample, default to clean, precise, venue-appropriate prose, not the casual,
opinionated voice of a general-purpose humanizer.

### General (non-academic) prose only: add voice
When the input is general prose under the explicit de-AI exception ("When to use"), removing patterns
is half the job — sterile, voiceless text is as obviously machine-made as slop:

- **Have opinions.** Don't just report facts -- react to them. "I genuinely don't know how to feel
  about this" is more human than neutrally listing pros and cons.
- **Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where
  they're going. Mix it up.
- **Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of
  unsettling" beats "This is impressive."
- **Use "I" when it fits.** First person isn't unprofessional -- it's honest. "I keep coming back
  to..." signals a real person thinking.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed
  thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but "there's something unsettling about
  agents churning away at 3am while nobody's watching."

**Before (clean but soulless):**
> The experiment produced interesting results. The agents generated 3 million lines of code. Some
> developers were impressed while others were skeptical. The implications remain unclear.

**After (has a pulse):**
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the
> humans presumably slept. Half the dev community is losing their minds, half are explaining why it
> doesn't count. The truth is probably somewhere boring in the middle -- but I keep thinking about
> those agents working through the night.

None of this ever enters a manuscript, referee report, or proposal — there, precision, directness, and
concrete magnitudes ARE the voice.

## Layer 6: Funding-proposal mode (NSF, NIH)
A proposal is not a paper. It is sold on **vision plus feasibility**, not on finished results, and
reviewers score it. The register shift matters: ambition language that the paper layers would trim
("long-term goal", "pioneer", "transformative", "establish a foundation") is *appropriate and expected*
here, provided a credible plan and evidence back it. So in proposal mode, **do not flatten the vision**;
enforce a different discipline instead: **claim <-> feasibility**.

Scope notes: 国自然/中文 proposals — also read [references/chinese.md](references/chinese.md) Part D.
Transforming a paper INTO a grant application, filling agency templates, or restructuring sections is
the `apply-fund` skill's job; this mode edits proposal prose that already exists. Worked before/after
examples (NIH Aims page, NSF Project Summary):
[references/proposal_examples.md](references/proposal_examples.md).

### 6.1 Know the structure; the score lives in the first pages
Reviewers form a score from the opening, then skim the rest to confirm it. Put most editing effort there.
- **NSF.** A one-page **Project Summary** with the three review-criteria heads spelled out:
  **Overview**, **Intellectual Merit**, **Broader Impacts**, each self-contained. The Project
  Description then opens with **long-term vision -> this proposal's goal -> the gap -> the specific
  thrusts/aims -> the payoff**, ideally within the first 1--2 pages, with one overview figure. Broader
  Impacts must be substantive and integrated, never an afterthought.
- **NIH (R01).** The **Specific Aims page is the whole proposal in one page**, and is the most-read,
  most-decisive page. Standard arc: (1) opening: the problem, what is known, the **gap / critical need**;
  (2) the **long-term goal** and the **central hypothesis** with its rationale; (3) "**The objective of
  this application is...**" plus how the hypothesis was formed; (4) **2--3 Aims**, each a one-line goal +
  a phrase on approach + the expected outcome; (5) a **payoff** paragraph: what changes if it succeeds.
  Then **Significance, Innovation, Approach** as separately scored sections.

### 6.2 First-3-pages primacy (edit these hardest)
By the end of page 1 (NIH Aims) or pages ~2--3 (NSF), the reader must already hold: the **hook** (why it
matters, concretely), the **gap** (what is missing and the cost of the gap), the **central idea** (your
approach in one sentence), the **aims/thrusts** (crisp and parallel), and the **payoff**. If any is
missing or buried, fix that before touching later sections. A reviewer unconvinced by page 3 does not
recover on page 10.

### 6.3 Proposal-specific weak moves to fix
- **Vague importance.** *Watch:* "this is an important/timely problem", "X has many applications".
  **Before:** *Understanding this problem is critically important.*
  **After:** *Without bounds on how measurement noise propagates to diagnosis, clinical models are tuned by
  trial and error, the inefficiency this proposal removes.*
- **Method-as-aim** (an aim naming a technique instead of a question or outcome).
  **Before:** *Aim 2: Apply transfer learning to the dataset.*
  **After:** *Aim 2: Determine whether fusing wearable and lab signals improves early detection, and for
  which patient subgroups it helps or hurts.*
- **Dominoed aims** (Aim 2/3 collapse if Aim 1 fails; reviewers flag this as fragile). *Fix:* phrase
  aims as **parallel and independently valuable**; where one depends on another, state the fallback.
- **Ambition without feasibility.** Every bold claim needs a footing: preliminary data, a prior
  result/publication, a classical theorem you build on, or a collaborator/letter. *Fix:* attach the
  evidence beside the claim ("our preliminary result in Fig. X shows...", "building on a classical minimax
  lower bound...").
- **Boilerplate Broader Impacts / training plan.** *Watch:* "we will mentor students and disseminate via
  talks and papers." *Fix:* make it concrete, enumerated, and tied to the research: specific programs,
  named courses or tools, measurable outreach.
- **Hedged central hypothesis.** The Aims-page hypothesis is a falsifiable commitment, not "we will
  explore whether possibly...". Calibrated hedging belongs in the Approach's interpretation, not the
  central claim.

### 6.4 Preserve and deploy (funded-proposal craft)
These read as strength; keep or add them rather than editing them out.
- **Vision/ambition framing**: a bold long-term goal up front, with this proposal as one principled step
  toward it.
- **Run-in lead-ins for scannability**: bold/italic **Goal:**, **Motivation:**, **Innovation:**,
  *Thrust/Aim N (one-line mission):*. Reviewers skim; visible structure earns time. (Contrast with
  paper mode: 2.15 removes these from manuscripts — proposals are the genre where they belong.)
- **A concrete running example or protagonist** to make an abstract method vivid and consistent across aims.
- **Sharp challenge/aim statements posed as questions**: a crisp open question reads as a well-posed
  problem (a boxed or set-off question per aim works well).
- **Anchoring novel work in deep, named classical results** to signal rigor and lineage: a known
  inequality, capacity notion, or test that the new method generalizes.
- **Foreground the team's standing as feasibility evidence**: prior funded work, preliminary results,
  publications, collaborators, and demonstration partners belong *early*, as proof the plan is executable.
  A real track record is evidence, not boasting; place it where it de-risks the aims. *(Use only the PI's
  own real, supplied record; never invent funding, results, partners, or letters.)*

### 6.5 Claim <-> feasibility (the proposal analog of Layer 4)
For every aim and promised outcome, check: is the ambition matched by a credible means, such as
preliminary data, a prior method, a classical foundation, a collaborator, or staged de-risking? If yes,
keep the ambitious verb. If no, attach the missing evidence or scale the claim to what the plan supports.
Never invent preliminary results, prior funding, partners, or letters; if the support does not exist, flag
the gap for the author rather than papering over it.

---

## Chinese mode (中文)

All of the above is English-native. For Chinese text — papers, 国自然 proposals, referee work, or
general prose — [references/chinese.md](references/chinese.md) is the operating file: which English
patterns drop in Chinese, the Chinese-native tells (结构骨架 首先/其次/综上所述, 套话拔高
赋能/助力/至关重要, 翻译腔, 的的不休), the zh AI-vocabulary watchlist, academic/国自然 notes (Part D),
and the /50 quality score. Read it FIRST (Process step 1), before applying anything else here.

---

## Output
Return the cleaned text plus a short change report: patterns removed (by type), claims softened or given
evidence pointers, and any voice/venue notes. Confirm that no number, equation, or citation was altered.

For longer text (multiple paragraphs or more), run the two-pass audit before finalizing:
1. **Draft rewrite**
2. **"What makes the below so obviously AI generated?"** — brief bullets identifying remaining tells
3. **Final rewrite** (revised after the audit)
4. **Change report** (as above)

For short text (a paragraph or less), a single clean rewrite plus the no-numbers-altered confirmation is
sufficient — the two-pass audit adds overhead without much benefit on small inputs.

## References

| File | When to read |
|------|-------------|
| [references/patterns.md](references/patterns.md) | REQUIRED scan on every non-trivial pass: the 29-pattern must-scan checklist + full before/after examples (typography, chatbot artifacts, structure tells) |
| [references/academic.md](references/academic.md) | REQUIRED for academic text: the full merged catalog (A1–A16) with LaTeX detection regexes + allowed exceptions + by-document-type maps (papers, referee reports, lit reviews, R&R) |
| [references/proposal_examples.md](references/proposal_examples.md) | Layer 6 worked examples: NIH Specific Aims opening + NSF Project Summary, before/after with change notes |
| [references/chinese.md](references/chinese.md) | **中文 adaptation** (read FIRST for Chinese text): Chinese-native AI tells, zh AI-vocab watchlist, 国自然 notes, /50 quality score |
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | Primary source for the general catalog, maintained by WikiProject AI Cleanup |

