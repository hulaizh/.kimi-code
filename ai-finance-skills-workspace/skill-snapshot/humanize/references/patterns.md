# AI Writing Patterns: Full Reference

29 patterns based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

## Must-scan checklist (quick fixes)

Scan every non-trivial text against ALL of these; the full before/after examples follow below.

### Content (patterns 1-6)
| # | Pattern | Fix |
|---|---------|-----|
| 1 | **Significance inflation** -- "pivotal moment", "testament to", "evolving landscape" | State what happened concretely |
| 2 | **Notability name-dropping** -- listing media outlets without context | Cite one source with a specific claim |
| 3 | **Superficial -ing phrases** -- "highlighting", "showcasing", "reflecting". Key tell: inanimate subject doing the -ing ("The discovery highlights..." vs. "She highlights...") | Remove or expand with actual evidence |
| 4 | **Promotional language** -- "nestled", "vibrant", "groundbreaking", "stunning" | Use neutral factual descriptions |
| 5 | **Vague attributions** -- "Experts argue", "Industry reports" | Name the specific source |
| 6 | **Formulaic challenges** -- "Despite challenges... continues to thrive" | State specific facts about actual problems |

### Language (patterns 7-12)
| # | Pattern | Fix |
|---|---------|-----|
| 7 | **AI vocabulary** -- Additionally, align with, bolstered, crucial, delve, enhance, enduring, fostering, garner, interplay, intricate, key, landscape, meticulous, pivotal, realm, seamless, showcase, tapestry, testament, underscore, valuable, vibrant | Replace with plain words |
| 8 | **Copula avoidance** -- "serves as", "stands as", "boasts", "features" | Use "is", "has", "are" |
| 9 | **Negative parallelisms** -- "It's not just X, it's Y" | State the point directly |
| 10 | **Rule of three** -- forcing ideas into groups of three | Use the natural number of items |
| 11 | **Synonym cycling** -- protagonist/main character/central figure/hero | Pick one term and repeat it |
| 12 | **False ranges** -- "from X to Y" where X and Y aren't on a scale | List items directly |

### Style (patterns 13-18½)
| # | Pattern | Fix |
|---|---------|-----|
| 13 | **Dash & hyphen misuse** -- three tells: (a) *em-dash overuse* (clauses split with dashes; LaTeX `---`) -- in academic/proposal prose remove em-dashes entirely; (b) *en-dash absence* in ranges ("2020-2025" should be "2020–2025"; LaTeX `--`); (c) *hyphen overuse* -- needless hyphens in prefixes (re-estimate, non-linear, sub-sample), noun compounds (car-age, firm-size), and -ly adverbs (statistically-significant) | (a) recast with commas, colons, parentheses, or separate sentences; (b) en dash for ranges; (c) close the prefix (reestimate, nonlinear, subsample), open the noun compound (car age, firm size), drop the -ly hyphen (statistically significant). Keep the hyphen in compound modifiers before a noun (two-way fixed effects, long-run effect), self-/quasi- (self-selection), ambiguity (re-cover ≠ recover), misreadable closures (co-opt, de-escalate), and before caps/numbers (non-OECD, pre-2008) |
| 14 | **Boldface overuse** | Remove mechanical emphasis |
| 14½ | **Bold lead sentences** -- paragraphs starting with a bold sentence followed by normal text | Remove the bold; let the paragraph carry its own weight |
| 15 | **Inline-header lists** -- "**Topic:** description" | Convert to prose |
| 16 | **Title Case Headings** | Use sentence case |
| 17 | **Emojis** | Remove |
| 18 | **Curly quotes** | Replace with straight quotes |
| 18½ | **Horizontal rule separators** -- `---` used to segment definitions, explanations, or concept boundaries; reads like structured output, not prose | Remove; use paragraph breaks or transitions instead |

### Communication (patterns 19-21)
| # | Pattern | Fix |
|---|---------|-----|
| 19 | **Chatbot artifacts** -- "I hope this helps!", "Let me know if...", refusal remnants ("As an AI language model..."), markup placeholders (citeturn0search0) | Remove entirely |
| 20 | **Knowledge-cutoff disclaimers** -- "based on available information" | Find sources or remove |
| 21 | **Sycophantic tone** -- "Great question!", "You're absolutely right!" | Respond directly |

### Filler and hedging (patterns 22-24)
| # | Pattern | Fix |
|---|---------|-----|
| 22 | **Filler phrases + editorial commentary** -- "In order to", "Due to the fact that". Also narrator intrusions: "It is important to note", "It is worth noting", "It should be emphasized that", "Notably,", "Importantly," | Compress fillers ("To", "Because"); eliminate narrator voice entirely -- if it matters, the sentence shows it |
| 23 | **Excessive hedging** -- "could potentially possibly" | One hedge per claim: "may" |
| 24 | **Generic conclusions** -- "The future looks bright" | Replace with specific facts or plans |

### Structure and flow (patterns 25-27)
| # | Pattern | Fix |
|---|---------|-----|
| 25 | **Transitional conjunction overuse** -- "Moreover", "Furthermore", "Additionally", "On the other hand", "However" at sentence starts | Remove or restructure; let logical flow carry the reader |
| 26 | **Section-ending summaries** -- "In conclusion", "In summary", "Overall" restating what was just said | Cut entirely; the reader just read it |
| 27 | **Hourglass structure** -- broad opening synthesis -> narrow specifics -> broad closing synthesis; paragraphs of suspiciously even length | Vary paragraph length; don't bookend with syntheses |

---

## Table of contents

- **Content** (1-6): Significance inflation, Notability name-dropping, Superficial -ing, Promotional language, Vague attributions, Formulaic challenges
- **Language** (7-12): AI vocabulary, Copula avoidance, Negative parallelisms, Rule of three, Synonym cycling, False ranges
- **Style** (13-18½): Dash & hyphen misuse, Boldface overuse, Bold lead sentences (14½), Inline-header lists, Title case, Emojis, Curly quotes, Horizontal rule separators (18½)
- **Communication** (19-21): Chatbot artifacts, Knowledge-cutoff disclaimers, Sycophantic tone
- **Filler** (22-24): Filler phrases + editorial commentary, Excessive hedging, Generic conclusions
- **Structure** (25-27): Transitional conjunction overuse, Section-ending summaries, Hourglass structure
- **Full example**: Two-pass audit demonstration

---

## CONTENT PATTERNS

### 1. Significance Inflation

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

### 2. Notability Name-Dropping

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

### 3. Superficial -ing Analyses

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

### 4. Promotional Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

### 5. Vague Attributions

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

### 6. Formulaic "Challenges and Future Prospects"

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## LANGUAGE AND GRAMMAR PATTERNS

### 7. AI Vocabulary Words

**High-frequency words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

### 8. Copula Avoidance

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

### 9. Negative Parallelisms

Constructions like "Not only...but..." or "It's not just about..., it's..." are overused.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

### 10. Rule of Three

LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

### 11. Synonym Cycling (Elegant Variation)

AI's repetition penalty causes excessive synonym substitution.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

### 12. False Ranges

"From X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## STYLE PATTERNS

### 13. Dash & Hyphen Misuse

AI mishandles all three dash-family characters: it overuses the em dash, skips the en dash in ranges, and sprinkles hyphens into words that should be closed up or left open. The first two are sentence punctuation; the third is word formation. All three are tells.

#### 13a. Em-dash overuse

AI splits clauses with em dashes where a comma or period reads cleaner. (LaTeX em dash is `---`.)

**Before:**
> The term is primarily promoted by Dutch institutions--not by the people themselves. You don't say "Netherlands, Europe" as an address--yet this mislabeling continues--even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

#### 13b. En-dash absence in ranges

Numeric and span ranges take an en dash, not a hyphen. (LaTeX en dash is `--`.)

**Before:** "Over 2020-2025, returns rose 8-12%, see pages 30-45."
**After:** "Over 2020–2025, returns rose 8–12%, see pages 30–45."

#### 13c. Hyphen overuse

AI inserts hyphens that economics and finance house style (Chicago Manual of Style) closes up or leaves open. Three moves.

**Close prefixed words.** Most prefixes are set solid -- `re-`, `pre-`, `non-`, `co-`, `sub-`, `multi-`, `semi-`, `over-`, `under-`, `inter-`, `counter-`, `de-`:

| AI form | Fix | AI form | Fix |
|---------|-----|---------|-----|
| re-estimate | reestimate | non-linear | nonlinear |
| re-examine | reexamine | sub-sample | subsample |
| pre-treatment | pretreatment | multi-period | multiperiod |
| co-movement | comovement | semi-parametric | semiparametric |
| over-identified | overidentified | counter-factual | counterfactual |

**Open noun compounds.** A noun-noun pair used as a plain noun takes no hyphen: car-age becomes "car age", firm-size becomes "firm size", sample-period becomes "sample period", interest-rate becomes "interest rate". (As a single noun, data-set becomes "dataset".)

**Drop -ly adverb hyphens.** An adverb ending in -ly is never hyphenated to the word it modifies: statistically-significant becomes "statistically significant", highly-correlated becomes "highly correlated", publicly-traded becomes "publicly traded", economically-meaningful becomes "economically meaningful". This covers only true adverbs: "family-owned firm" and "early-stage funding" keep the hyphen because family and early are not -ly adverbs.

**Keep the hyphen when it does real work -- do not overcorrect:**
- **Compound modifiers before a noun:** "two-way fixed effects", "long-run equilibrium", "difference-in-differences design", "cross-sectional variation". The same pair is open as a noun but hyphenated as a modifier: "we aggregate to the firm level" vs. "firm-level data". But established open compounds used attributively stay open per journal convention -- "interest rate risk", "stock market volatility" -- do not force a hyphen into a fixed term.
- **self- and quasi-:** "self-selection", "self-reported", "quasi-experiment", "quasi-natural" (hyphenated); but theory compounds "quasilinear" and "quasiconcave" are conventionally closed -- do not add a hyphen to them.
- **Ambiguity (the hyphen changes the word):** "re-cover" ≠ "recover", "re-creation" ≠ "recreation", "re-sign" ≠ "resign", "re-present" ≠ "represent".
- **Misreadable closures:** keep the hyphen when closing produces a non-word or a vowel pile-up -- "co-opt", "co-op", "de-escalate", "de-identified", "semi-independent". Merriam-Webster governs: lexicalized closures like reexamine, reenter, and cooperate stay closed.
- **Before a capital or number:** "non-OECD", "pre-2008", "post-1990", "mid-1980s".

The error runs both ways: AI also drops hyphens from genuine compound modifiers. Hyphenate a multiword modifier when it sits before the noun, open it when it follows the verb -- "long run equilibrium" should be "long-run equilibrium", but "the effect is long run" is correct.

**Before:**
> We re-estimate the model on a sub-sample of publicly-traded firms, allowing for non-linear and time-varying effects of firm-size over the 2010-2020 period.

**After:**
> We reestimate the model on a subsample of publicly traded firms, allowing for nonlinear and time-varying effects of firm size over the 2010–2020 period.

(Note that "time-varying" stays hyphenated -- it is a compound modifier before "effects".)

### 14. Boldface Overuse

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

### 14½. Bold Lead Sentences

**Problem:** AI outputs frequently start paragraphs with a bold sentence followed by normal text, creating a mechanical "topic sentence + elaboration" structure that reads like a formatted outline rather than prose.

**Before:**
> **The identification strategy relies on geographic variation in policy adoption.** We exploit staggered rollout across states to estimate treatment effects using a difference-in-differences design with two-way fixed effects.
>
> **Robustness checks confirm the main findings.** We reestimate the model using alternative specifications, including propensity score matching and instrumental variables.

**After:**
> The identification strategy relies on geographic variation in policy adoption. We exploit staggered rollout across states to estimate treatment effects using a difference-in-differences design with two-way fixed effects.
>
> Robustness checks confirm the main findings. We reestimate the model using alternative specifications, including propensity score matching and instrumental variables.

---

### 15. Inline-Header Lists

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

### 16. Title Case in Headings

**Before:** `## Strategic Negotiations And Global Partnerships`
**After:** `## Strategic negotiations and global partnerships`

### 17. Emojis

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity

**After:**
> The product launches in Q3. User research showed a preference for simplicity.

### 18. Curly Quotation Marks

ChatGPT uses curly quotes ("\u201c...\u201d") instead of straight quotes ("..."). Replace curly with straight.

### 18½. Horizontal Rule Separators

**Problem:** AI-generated text frequently uses `---` (horizontal rules) to segment definitions, explanations, or concept boundaries. This creates a structured, outline-like appearance -- as if the text was generated from a template rather than written by a person. Human writers rarely insert horizontal rules mid-prose to separate ideas; they use paragraph breaks or transitions instead.

**Before:**
> Liquidity risk refers to the possibility that a firm cannot meet its short-term financial obligations due to an inability to convert assets into cash without significant loss.
>
> ---
>
> Market risk, on the other hand, arises from fluctuations in market prices -- including interest rates, equity prices, and exchange rates -- that affect the value of a portfolio.
>
> ---
>
> Credit risk is the potential for loss resulting from a borrower's failure to repay a loan or meet contractual obligations.

**After:**
> Liquidity risk is the possibility that a firm cannot meet short-term obligations because it cannot convert assets to cash quickly enough. Market risk comes from price fluctuations -- interest rates, equities, exchange rates -- that move portfolio values. Credit risk is the chance a borrower defaults.

---

## COMMUNICATION PATTERNS

### 19. Chatbot Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 20. Knowledge-Cutoff Disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Before:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.

### 21. Sycophantic Tone

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.

---

## FILLER AND HEDGING

### 22. Filler Phrases + Editorial Commentary

**Filler compression:**
- "In order to achieve this goal" -> "To achieve this"
- "Due to the fact that it was raining" -> "Because it was raining"
- "At this point in time" -> "Now"
- "In the event that you need help" -> "If you need help"
- "The system has the ability to process" -> "The system can process"

**Editorial commentary (distinct from mere filler -- these insert an invisible narrator):**
- "It is important to note that the data shows" -> "The data shows"
- "It is worth noting that..." -> cut entirely
- "No discussion would be complete without..." -> cut entirely
- "It bears mentioning that..." -> cut entirely

The difference: filler inflates length; editorial commentary inserts a narrator who decides what is "important" or "worth noting." The fix is not just compression but elimination of the narrator voice.

### 23. Excessive Hedging

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

### 24. Generic Positive Conclusions

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.

---

## STRUCTURE AND FLOW PATTERNS

### 25. Transitional Conjunction Overuse

**Words to watch:** Moreover, Furthermore, Additionally, On the other hand, However, Consequently, Nevertheless, In addition

**Problem:** AI text overuses formal transition words at sentence starts, creating an essay-like cadence rare in natural writing.

**Before:**
> The policy reduced emissions by 12%. Moreover, it created 3,000 jobs in the renewable sector. Furthermore, it attracted $2B in private investment. Additionally, neighboring states began adopting similar measures.

**After:**
> The policy reduced emissions by 12% and created 3,000 jobs in the renewable sector. It also attracted $2B in private investment. Neighboring states began adopting similar measures.

### 26. Section-Ending Summaries

**Words to watch:** In conclusion, In summary, Overall, To summarize, Taken together

**Problem:** AI restates what was just said at the end of sections, mimicking a school-essay habit.

**Before:**
> The study found higher returns for small-cap stocks, stronger effects during recessions, and persistence over 20 years. Overall, these results suggest that the size premium is robust across specifications and time periods.

**After:**
> The study found higher returns for small-cap stocks, stronger effects during recessions, and persistence over 20 years.

### 27. Hourglass Structure / Symmetric Paragraphing

**Problem:** AI-generated text follows a predictable structure: broad opening synthesis -> narrow specifics -> broad closing synthesis. Paragraphs are suspiciously even in length, with visual balance appearing to take precedence over content flow.

**Before (notice the symmetry):**
> Financial technology has transformed the banking industry in recent years. [broad opener]
>
> Mobile banking adoption grew from 15% to 78% between 2015 and 2023. Fintech lending reached $50B in 2022. Digital payments processed $8.5T in transaction volume. [three evenly paced specific paragraphs]
>
> These developments collectively illustrate how financial technology continues to reshape the banking landscape. [broad closer mirroring opener]

**After (varied structure):**
> Mobile banking adoption grew from 15% to 78% between 2015 and 2023. Fintech lending hit $50B in 2022.
>
> The payments side is even bigger: $8.5T in digital transaction volume, though most of that is just replacing checks and wire transfers rather than creating new economic activity.

---

## FULL BEFORE/AFTER EXAMPLE (TWO-PASS AUDIT)

**Before (AI-sounding):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools--nestled at the intersection of research and practice--are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies--including hallucinations, bias, and accountability--the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you'd like me to expand on any section!

**Draft rewrite:**
> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.
>
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless. It means they are tools. They do not replace judgment, and they do not eliminate the need for tests. If you do not have tests, you cannot tell whether the suggestion is right.

**"What makes the below so obviously AI generated?"**
- The rhythm is still a bit too tidy (clean contrasts, evenly paced paragraphs)
- The closer leans a touch slogan-y ("If you do not have tests...") rather than sounding like a person talking

**Final rewrite:**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.
