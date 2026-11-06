# Topic 3 Chinese: one-to-one alignment

The user's 7 November instruction adds the Chinese deck to the active task.
Translate the reviewed English 58-page deck page for page. The English version
after the Pi/Gemini repairs is authoritative; later English corrections must be
mirrored in Chinese before completion.

The user's subsequent instruction assigns final Chinese translation,
proofreading and copy editing directly to Gemini-4-Argon in the existing left
Pi session. The parallel translators' checkpoint `ab0e19c` is its working draft.
Gemini owns Chinese editing until its translation/editing pass is complete;
the root then independently rebuilds and checks bilingual correspondence.

## Required correspondence

- Exactly 58 pages in each language, with the same title, section/subsection
  sequence, examples, exercises, source links and qualifications.
- Same architecture on pages 4 and 36 within each language, including one
  Evolution enclosure and visible framing/synthesis. Detailed evolution is p31.
- Same O–G–C teaching on pp10–12, QT data/calculation examples on pp40–41,
  eight participation points and broad evolution principles.
- Translate all narrative, slide titles, table headings/explanations, figure
  labels, source-note wording and questions. Keep the same content allocation;
  do not summarize, add a claim or soften a qualification.
- Preserve commands, flags, paths, JSON/YAML keys, status constants, identifiers,
  mathematical expressions and worked data exactly. Preserve source URLs.
- Keep actual code/role-card excerpts and the English Generator-prompt patch
  verbatim: they are source artifacts being inspected, not Chinese prose.
  Translate their captions and surrounding explanation. Keep the actual English
  command/prompt examples in listings so they remain aligned with the source.
- Layout may adapt to Chinese glyph widths, without font shrinking as a general
  solution. No additional pages or hidden-only translations.

## Terminology

| English | Chinese convention |
|---|---|
| Orchestrator / Generator / Critic | Keep these role names; translate their responsibilities and surrounding prose |
| lead / specialist | 负责人 / 专项 Agent (use context naturally) |
| Harness | Harness; explain as 运行环境与控制 where useful |
| Loop / Graph / Evolution | 循环 / 图 / 演进; English labels may remain in the engineering ladder and section names |
| controller | 控制器 |
| gate | 检查关卡 or 必要检查, according to the sentence |
| mandate | 任务授权 / 授权范围 |
| candidate | 候选方案 in generic Harness/Graph design; 候选策略 in research; 候选版本 or 候选改动 in evolution |
| finding / carried findings | 问题项 / 上一轮未解决的问题项 |
| repair / review | 修复 / 审查 |
| approval / authority | 批准 / 授权或权限, according to the object |
| adoption / rollback | 采用或启用 / 回滚 |
| checkpoint / resume | 检查点 / 从已核验进度恢复运行 |
| reconstruct / recompute / fresh run | 重建已发生的运行 / 复算 / 新的模型运行 |
| fixture | 测试样例; 合成测试样例 for synthetic fixtures |
| invariant | 不变条件 / 必须始终满足的条件 |

Use fluent academic Chinese, not word-for-word English syntax. In particular,
preserve the difference between a requirement of the general design and what
the current QT prototype actually implements. The missing human-approver record,
rotated retry request ID, optional hook packaging and independent historical
trade-sheet fixture must be translated accurately.

## Draft ownership and final handoff

The root prepares the Chinese preamble and copies only the active English
sections/assets. A generated ownership manifest under
`logs/topic-3/redesign-58/cn-ownership.json` assigns each referenced asset to one
translator, so shared figures are translated once.

1. Opening/harness translator: section01, its assets and shared architecture.
2. Loop/graph/evolution translator: section02 and its nonshared assets.
3. Case translator: section03, its assets and verbatim source listings.

The root owns both main sources, the alignment audit and integration builds.
Keep the existing XeLaTeX/ctex setup and shared styles. The earlier Chinese deck
is preserved under the ignored run log's `cn-before/` snapshot.

All three draft translators have stopped editing. For the final pass, Gemini
may edit every active Chinese source/asset, including the main Chinese source
when necessary for compilation, while keeping English and shared styles read-only.

## Verification and review

Compile with XeLaTeX, inspect all 58 Chinese pages, and compare the two versions
for page structure, source/asset correspondence, numbers, formulas, identifiers,
commands and nuance. Run a bilingual proofreading/humanize pass that preserves
exact meaning. Ask Pi/Gemini to verify the English repairs and the Chinese
correspondence, then fix findings and recheck affected pages.

Commit both PDFs and editable sources with the final review/translation record.
