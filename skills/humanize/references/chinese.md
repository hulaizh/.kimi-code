# Humanize — Chinese (中文) Adaptation

Read this when the text to humanize is **Chinese**. The 29 patterns in `SKILL.md` are
English-native; this file (a) says which of them change or drop in Chinese, and (b) adds
the **Chinese-native AI tells** that the English list does not cover. The biggest source
of "AI 味" in Chinese is *structural scaffolding + 套话 + 翻译腔* — not the English
vocabulary list. Fix those first.

Goal is the same: remove AI artifacts **and** restore a human voice (有观点、有具体、有节奏).
Do not flatten the text into 干净但无灵魂的 press-release 中文. Every tell below carries a
**改前 → 改后** so you imitate the move, not just the rule.

**Mixed EN/中文 text** (common in Chinese econ/finance papers): apply BOTH this file and the
English patterns — de-slop the Chinese prose here, and fix English terms / dashes / quotes via
`SKILL.md` + `references/academic.md`.

---

## Part A — How the 29 English patterns map to Chinese

| EN pattern | In Chinese |
|---|---|
| 7 AI vocabulary | Replace with the **Chinese** slop list in Part C (the English words rarely appear). |
| 8 Copula avoidance ("serves as") | Chinese analogue = **弱动词框架**: 起到了…的作用 / 成为…的关键 / 扮演着…的角色 → 用实义动词 (是/有/能). |
| 9 Negative parallelism | 直接对应: 这不仅仅是…而是… / 与其说…不如说… → 直说要点. |
| 10 Rule of three | 对应排比堆砌 (见 B-4). |
| 13 Dashes/hyphens | 中文无连字符问题；但 **—— 破折号滥用**很常见 → 用逗号/句号. 英文连字符 N/A. |
| 16 Title Case headings | **不适用** (中文无大小写). Skip. |
| 18 Curly quotes | 中文本就用 「」/“”；真正的 tell 是**英文直引号 ' " 混入中文**，或全角/半角引号混用 → 统一中文引号. |
| 17 Emojis | 同样删除. |
| 22 Narrator intrusion | 强烈对应 (见 B-6: 值得注意的是 / 不难发现). |
| 25 Transition overuse | 对应**结构骨架词** (见 B-1: 首先/其次/最后, 此外/同时/然而). |
| 26 Section-ending summary | 对应 综上所述 / 总而言之 / 总的来说 (见 B-1). |
| 1,3,4,5,6,19,20,21,23,24 | Concepts transfer directly; rewrite using Chinese equivalents (具体事实、点名来源、删谄媚). |

Everything else (significance inflation, vague attribution, hedging, generic conclusions,
hourglass structure, soulless rhythm) applies the same way — just in Chinese.

---

## Part B — Chinese-native AI tells (the real work)

Each tell shows a **改前 → 改后**. Imitate the move.

### B-1. 结构骨架 / 套式过渡 (formulaic scaffolding)
The #1 AI tell in Chinese. The LLM forces ideas into a visible skeleton: 序数骨架
(**首先…其次…再次…最后**、**一方面…另一方面**), 收尾套话 (**综上所述 / 总而言之 /
总的来说 / 由此可见**), 过渡连词堆叠 (**此外 / 同时 / 然而 / 因此** at every sentence head).
- **改前:** 首先，本文研究了 X；其次，我们发现了 Y；再次，进一步分析表明 Z；最后，综上所述，本文具有重要意义。
- **改后:** 本文研究 X，发现 Y。进一步分析表明 Z。
- **Fix:** delete the skeleton; let logic carry the order. Keep an ordinal only when the sequence is real and load-bearing.

### B-2. 的的不休 / 冗余虚词 (over-stacked 的, 了, 着, 进行)
- **改前:** 这是一个具有重要现实意义的、行之有效的解决方案。
- **改后:** 这个方案有效。
- **Fix:** 拆长定语为短句，删可去的"的/地"，one 的 per noun phrase.

### B-3. 弱动词 + 介词框架 (verb weakening / preposition padding)
进行/予以/加以/作出 + 名词；对…进行 / 通过…的方式 / 在…方面 / 关于…的问题.
- **改前:** 本文对该问题进行了深入的研究，并通过实证的方式作出了分析。
- **改后:** 本文实证分析了该问题。
- **Fix:** use the real verb; drop the 对/通过/在…方面 shell.

### B-4. 排比 / 四字格堆砌 (forced parallelism & idiom stacking)
不仅…而且…更…；既…又…还…；四字成语连用 (日新月异、保驾护航、提质增效、行稳致远).
- **改前:** 该政策不仅提质增效，而且行稳致远，更为高质量发展保驾护航。
- **改后:** 该政策把企业合规成本降了约 8%，且没有抑制投资。
- **Fix:** keep at most one parallel pair that earns its place; replace idiom chains with one concrete fact.

### B-5. 背景套话开场 (boilerplate openers)
随着…的不断发展 / 在…的大背景下 / 在当今…的时代 / 近年来，随着… / 众所周知.
- **改前:** 随着数字经济的不断发展，在新时代的大背景下，数据已成为关键生产要素。
- **改后:** 2023 年中国数据要素市场规模达 1.2 万亿元。
- **Fix:** cut it; open on the specific claim.

### B-6. 叙述者插入 (narrator intrusions)
值得注意的是 / 需要指出的是 / 不难发现 / 我们可以看到 / 显而易见 / 由此可见 / 不可否认.
- **改前:** 值得注意的是，数据显示销量同比增长了 20%。
- **改后:** 销量同比增长 20%。
- **Fix:** delete; state the fact directly.

### B-7. 拔高 / 宣传腔 (significance & promo inflation, Chinese register)
至关重要 / 不可或缺 / 具有重要意义 / 起到了关键作用 / 极大地 / 显著地 / 有效地 / 切实 /
全面 / 深刻；动词流行语 助力 / 赋能 / 打造 / 构建 / 凸显 / 彰显 / 谱写…新篇章.
- **改前:** 该机制至关重要，极大地提升了市场效率，具有重要的理论意义。
- **改后:** 该机制使买卖价差收窄了约 15 个基点。
- **Fix:** replace with a concrete magnitude or mechanism.

### B-8. 空泛结论 (empty conclusions)
未来可期 / 前景广阔 / 任重道远 / 仍需进一步探索 / 必将….
- **改前:** 总之，该领域前景广阔、未来可期，仍需学界进一步探索。
- **改后:** 下一步可检验该机制在中小银行样本中是否仍成立。
- **Fix:** give a specific plan, number, or open question.

### B-9. 翻译腔 (machine-translation stiffness)
被动滥用 (被认为是 / 被广泛应用于)；英式量词 (一个 + 抽象名词 照搬 a/an)；生硬指代
(滥用 其/之/该/此；这使得…成为可能；作为一名…，我).
- **改前:** 这一发现被认为是具有开创性的，它使得对市场行为的理解成为可能。
- **改后:** 这一发现首次解释了散户为何在财报日后追涨。
- **Fix:** natural 中文 word order; drop redundant 一个/被; prefer active voice.

### B-10. 标点与排版 (punctuation / format tells)
—— 破折号滥用；全角/半角混用（中文里夹半角逗号/括号）；正文塞 "1. … 2. …" 编号或
"**重点：** 说明" 内联标题；中英标点不一致.
- **改前:** 本文研究了三个问题——市场结构、定价、以及福利, 并得出结论。
- **改后:** 本文研究市场结构、定价与福利三个问题。
- **Fix:** 统一全角中文标点；列表化结构改写成段落；—— 改逗号/句号.

---

## Part C — Chinese AI-vocabulary watchlist

Replace with plain words; these cluster in AI 中文:

**学术腔 slop:** 深入探讨、揭示、表明、进一步、持续、不断、显著、极大地、充分、有效、切实、
全面、深刻、重要意义、积极作用、有机结合、高度重视、相辅相成、奠定了坚实基础。

**互联网黑话:** 赋能、抓手、闭环、链路、沉淀、维度、颗粒度、底层逻辑、范式、生态、心智、
护城河、对齐、拉通、复盘、打法、势能。

**Over-correction guard:** these are *suspects, not bans*. Keep a word when it is the precise,
ordinary term ("显著" inside "统计显著" is correct; "构建模型" is fine in a theory paper).
Removing a tell must not change the meaning or strip a legitimate technical term — when in
doubt, rewrite the sentence rather than swapping the word.

---

## Part D — Academic / 国自然 Chinese

For Chinese papers, 基金申请 (国自然/面上/青年), and 中文 referee work, "voice" means
**precision and concrete magnitude**, not informality. Keep:
- 删骨架词 (首先/其次/综上所述) but keep genuine 逻辑连接.
- 立项依据 / 研究内容 should state specific mechanisms and numbers, not 至关重要/具有重要意义.
- Do **not** inject 第一人称 jokes or 网感; academic 中文 stays formal but **直接、具体、不堆砌**.
- This is the de-slop pass, not the drafting pass (use apply-fund to draft a grant; rr for 中文 referee responses).

---

## Part E — Worked example (full paragraph, two-pass)

**改前 (满是 AI 味):**
> 随着人工智能技术的不断发展，在数字经济的大背景下，AI 写作工具正在深刻地改变着内容生产的方式。首先，这些工具极大地提升了生产效率；其次，它们有效赋能了广大创作者；再次，更是助力了行业的提质增效。值得注意的是，这一变革不仅具有重要的现实意义，而且影响深远。综上所述，AI 写作的前景广阔、未来可期。

**Pass 1 — 哪里一眼像 AI？** 背景套话开场 (随着…大背景下)；骨架 (首先/其次/再次/综上所述)；拔高词 (极大地/深刻地/赋能/助力/提质增效)；叙述者插入 (值得注意的是)；空泛结论 (前景广阔、未来可期)；零具体事实。

**改后 (去味 + 有声音 + 有具体):**
> AI 写作工具正在改变内容生产——我对此感受复杂。它确实快，一篇初稿几秒就出来；可产出的文字往往一眼就能看出是机器写的：套话多、信息少。真正稀缺的从来不是把字凑齐，而是有人愿意为每一句话负责。

The 改后 has a point of view (感受复杂), a concrete contrast (快 vs. 一眼看出是机器写的),
and varied rhythm — it embodies "add soul", not just deletion.

---

## Part F — Quality score (改写后自评, /50)

Rate the rewrite 1–10 on each, target ≥ 8 (below 40/50 → run the two-pass audit again, see SKILL.md Output Format):
1. **自然度** — reads like a 中文 native wrote it (no 翻译腔, no 骨架).
2. **信息密度/具体性** — concrete facts & magnitudes replaced vague 拔高.
3. **语气/声音** — has a point of view and appropriate register (not press-release).
4. **结构/节奏** — varied sentence length; no 首先…最后…综上 skeleton.
5. **无AI痕迹** — none of the Part B/C tells remain; meaning unchanged.

---

## Attribution

Chinese pattern set adapted from **op7418/humanizer-zh** (which translates **blader/humanizer**
and the Wikipedia *Signs of AI writing* guide, plus the **hardikpandya/stop-slop** checklist &
scoring). The Chinese-native tells (Part B), worked example (Part E), and academic-Chinese
guidance (Part D) are additions beyond that source.
