# Practitioner skill cleanup: comprehensive review

Reviewed commits `46dc556` and `edfc4f8` against `17587c9`, the complete active
six-skill library, its scripts and references, the shared skill descriptions,
Kimi configuration, and the installed plugin manifest. The earlier cleanup
removed the journal bundle, but it was not complete or fully correct.

## Findings and corrections

| Priority | Finding | Correction |
|---|---|---|
| P1 | The report template used the Topic 2 DCF note structure, not the research memo displayed in Lecture 1. | Rebuilt the single template around Lecture 1's dated header, team block, finding, narrative column, data/chart sidebar, and source notes, adapted to A4. |
| P1 | The cleanup retained humanizing examples that introduced unsupported numbers and claims: 8% cost savings, RMB 1.2 trillion, 15 basis points, new mechanisms, and personal opinions. The general guide also encouraged specificity without consistently preserving source facts. | Replaced those examples with faithful finance edits. Numbers, conditions, forecasts, approval status, and uncertainty must survive; unsupported judgments get a separate evidence-gap note. |
| P2 | The new compiler helper accepted only pdfLaTeX, while the skill advertised Chinese reports; the guide/helper were no longer linked from the entrypoint. | Added explicit pdflatex/xelatex/lualatex options, restored resource links, and documented the Chinese switch in the same template. |
| P2 | The plot-helper rewrite dropped nonacademic dark/minimal presets and stopped saving preview images. | Restored those practitioner features; kept the journal preset removed. Tested exported styles by parsing and rendering them. |
| P2 | Practitioner cleanup remained inconsistent across references and generated project instructions: paper-oriented examples and Student-edited labels remained. | Removed the academic writing examples and made project/report labels neutral. Preserved the exact newproj directories and its internal recognition marker so existing projects remain resumable. |
| P2 | No Kimi-specific practitioner profile existed; the datasource plugin still advertises academic routes. | Added the supported global AGENTS.md profile for finance practice. Kept vendor files intact; academic backend routes remain technically available. |

The last item is a limitation, not a claim that academic tools have been disabled.
The managed datasource plugin combines finance and academic sources behind the
same tools. Kimi's native MCP permission rules match tool names, not individual
data-source argument values. A blanket tool denial would remove finance retrieval
too. No custom blocking hook or vendor-server modification was introduced.

## Scope boundaries

Retained investment research, research memos, investment theses, factor exposures,
risk analysis, citations/source locators, and generic plotting APIs: these are
valid practitioner capabilities. The isolated historical snapshots and run logs
remain outside the configured skill discovery directories. They were not deleted
or treated as current instructions. The vendor plugin, credentials, model selection,
permission mode, shared ~/.agents skills, Lecture 1, and teaching files were not edited.

There is one active LaTeX template. It does not embed the Lecture 1 company's
figures or the FISF/student branding. It follows that memo's visual structure,
sized for A4 rather than the example PDF's US Letter. Table/figure content stays
separate from authored wrappers; sidebar wrappers use captionof because floats
cannot appear inside minipages. Longer reports must use normal page flow rather
than overflow a fixed sidebar layout.

## Verification

- All six skill frontmatters pass the skill validator. Active Markdown links,
  JSON files, and Python syntax pass checks; no references to deleted resources
  remain in active skills.
- A standalone copy of the template compiles without any external exhibit files.
  English and Chinese specimens with real wrapper inputs compile without errors,
  missing glyphs, unresolved references, or overflow. PDF geometry is A4 and the
  specimens are one page. LuaLaTeX also compiled the English specimen.
- Wrong-engine Chinese compilation and missing-source invocation fail explicitly.
  Source filenames containing spaces work.
- Finance, presentation, web, dark, and minimal styles export, parse with matplotlib,
  render, and save preview images. This retains useful chart behavior without
  reinstating academic presets.
- newproj preview writes nothing; creation and resumption retain existing work.
  Its directory paths and recognition marker are unchanged.
- One actual Kimi humanize run handled English and Chinese financial text and an
  unsupported profitability claim. It preserved RMB 12 million / 人民币1200万元,
  the payment condition, forecast status, conditional approval, and unreviewed
  guarantee; it added no numbers to the unsupported claim. This is a functional
  smoke check, not a statistical estimate of model reliability.
- Kimi 2.4.1 doctor validates config.toml and tui.toml. The installed datasource
  plugin remains enabled. No external data retrieval was needed for this review.

Review artifacts are under logs/practitioner-review/: original Lecture 1 rendering,
before-change snapshots, compile logs, style checks, Kimi trace, and the A4 preview.
Validation used the existing plotting environment and Anaconda's YAML installation;
no global packages were installed.

## Documentation checked

- [Kimi global and project instructions](https://moonshotai.github.io/kimi-code/en/customization/agents.html): supports ~/.kimi-code/AGENTS.md as Kimi-specific global instructions.
- [Kimi configuration and permissions](https://moonshotai.github.io/kimi-code/en/configuration/config-files.html): MCP tools use name matching rather than argument-pattern rules.
- [Kimi skill discovery](https://moonshotai.github.io/kimi-code/en/customization/skills): user/project discovery directories and precedence.

Start a new Kimi session to use the new global profile and refreshed skill text.
