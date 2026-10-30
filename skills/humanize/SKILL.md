---
name: humanize
allowed-tools: Read, Edit, Write, Grep, Glob, AskUserQuestion
license: MIT
description: "Edit existing prose to sound natural, precise, and appropriate for its audience while preserving facts, numbers, citations, and conclusions. Use for requests such as 'humanize this', 'de-slop', 'too robotic', 'sounds like AI', and Chinese 去AI味/降AI痕迹. Supports professional, academic, and general writing, including finance reports and commentary. NOT for drafting new analysis, changing conclusions, or evading required AI-use disclosure."
---

# Humanize writing

Edit existing prose so it reads as if a careful person wrote it for a specific reader. Natural writing is not casual by default: finance and academic texts become more human through precision, rhythm, specificity, and honest uncertainty.

This is an editing skill, not a way to conceal prohibited AI use. Follow the course or organization's disclosure rules.

## Process

1. **Read the full text and context.** Identify the document type, audience, purpose, and language. Read an author sample when supplied.
2. **Route the edit.** For finance documents, read [references/finance.md](references/finance.md). For Chinese text, read [references/chinese.md](references/chinese.md) first. For a substantial edit in any language, scan [references/patterns.md](references/patterns.md).
3. **Audit before rewriting.** Note repeated AI patterns, unsupported claims, vague magnitudes, and places where the tone does not fit the reader. Do not turn the audit into a long theoretical essay.
4. **Rewrite without changing meaning.** Preserve structure unless a small reordering clearly improves readability. Keep legitimate hedging and technical terminology.
5. **Check factual fidelity.** Compare numbers, dates, units, citations, names, recommendations, and qualifications with the original.
6. **Return the cleaned text and a short change note.** Flag factual or evidence problems that editing alone cannot resolve.

For short text, one clean rewrite and a brief fidelity confirmation are enough. For longer text, make a second pass specifically for remaining formulaic phrasing, over-claiming, and altered details.

## What to remove

- Empty promotion: groundbreaking, pivotal, transformative, robust, dynamic, or compelling when no evidence follows.
- Filler and throat-clearing: "It is important to note", "In today's fast-paced world", and generic introductions.
- Repetitive scaffolding: consecutive "Moreover/Furthermore/Additionally" openings, mechanical rule-of-three lists, and repetitive section summaries.
- Vague attribution: "experts say", "the market believes", or "studies show" without a supplied source.
- Inflated verbs: proves, guarantees, demonstrates universal superiority, or predicts with certainty when the evidence is narrower.
- Elegant variation that makes one company, metric, portfolio, or result sound like several different things.
- Long sentences stacked with clauses that obscure the actor, calculation, or conclusion.
- Chatbot artifacts, generic conclusions, excessive boldface, and unnecessary em-dash habits.

Do not replace every flagged word mechanically. Keep a term when it is precise, and preserve an author's reasonable style rather than imposing a uniform voice.

## Finance fidelity

Never silently alter:

- A number, date, currency, unit, ticker, company name, or citation.
- A rating, target price, investment stance, risk classification, scenario, or recommendation.
- The distinction between reported results, calculated values, estimates, forecasts, and opinion.
- A limitation, uncertainty, conflict disclosure, or compliance statement.

Prefer concrete statements such as "Revenue increased 8% year over year" over "The company delivered a strong performance." If the original says "strong" without evidence, retain the meaning but flag that support is missing; do not invent a number.

Separate the editorial fix from the analytical question. If the underlying analysis appears wrong, name the concern instead of polishing it into greater confidence.

## Academic and student writing

For student essays and papers, keep claims tied to supplied evidence and match the assigned register. Keep first-person plural and passive voice when they are appropriate. Preserve equations, symbols, definitions, and citation keys exactly.

Do not add citations, results, personal experiences, or arguments that the student did not supply. For advanced academic editing, [references/academic.md](references/academic.md) provides additional claim-evidence and LaTeX guidance.

## General prose

For emails, reflections, blogs, and presentations, allow more individual rhythm and perspective when the original supports them. Do not force jokes, confessions, fake opinions, tangents, or casual language into professional text. The goal is a believable voice, not a performance of informality.

## Chinese text

Follow [references/chinese.md](references/chinese.md) for Chinese-native patterns such as 套话、翻译腔、机械的“首先/其次/最后”结构、过度拔高 and 的不休. English word lists and punctuation rules do not transfer directly to Chinese.

## Output

Return:

1. The cleaned text.
2. A short note describing the main changes.
3. Any unresolved factual, evidence, or compliance concerns.
4. Confirmation that numbers, citations, and financial positions were preserved, or a precise list of accidental discrepancies found and corrected.

## References

| File | When to read |
|---|---|
| [references/finance.md](references/finance.md) | Required for investment, portfolio, risk, earnings, market, and other finance prose |
| [references/patterns.md](references/patterns.md) | Required scan for substantial edits |
| [references/chinese.md](references/chinese.md) | Read first for Chinese text |
| [references/academic.md](references/academic.md) | Optional advanced guidance for student academic papers and LaTeX prose |
