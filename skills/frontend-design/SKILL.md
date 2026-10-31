---
name: frontend-design
description: "Build or improve web interfaces with working interactions, responsive layouts, and accessible visual design. Use for dashboards, screeners, scenario tools, monitoring views, and HTML/CSS/JS or React/Vue components. Not for static charts (use plot), document layout (use latex), or data retrieval without a UI."
license: Complete terms in LICENSE.txt
---

# Frontend design

Build real, working interfaces rather than decorative mockups. Match the visual direction to the audience and task: an expressive demo can be bold, while an investment or risk dashboard usually needs calm density, precise hierarchy, and restrained motion.

## Design and implementation

1. **Understand the task.** Identify the user, decision or learning objective, data source, required interactions, framework, and project conventions.
2. **Choose an intentional aesthetic.** Commit to a clear direction such as editorial, industrial, minimal, terminal-inspired, retro-futuristic, or luxury. Boldness means coherence and specificity, not visual noise.
3. **Design the finance information hierarchy.** Lead with the question or decision, then key measures, supporting exhibits, and detail. Keep source, date, units, and assumptions close to the numbers they describe.
4. **Implement working behavior.** Filters, sorting, tabs, scenario controls, downloads, and navigation must function. Do not add controls merely to make a screenshot look complete.
5. **Verify the delivered interface.** Run the standard build, exercise the interactions, inspect representative viewport sizes, and reconcile displayed values with the underlying data.

## Implementation defaults

- Use the project's existing framework and dependencies. For a standalone exercise, prefer simple HTML/CSS/JavaScript unless the user requests a framework.
- Use real supplied data when available. If using demonstration data, label it visibly and do not present it as live market information.
- Keep the first version small: one clear workflow and a limited set of useful interactions.
- Include concise run instructions in the response rather than adding documentation files to the project unless requested.
- Explain any finance calculation that the interface implements, and test it against a small worked example.
- Match explanation depth to the request: explain inputs and one calculation for a beginner, expose assumptions and sensitivity for analytical work, and lead with exceptions and decisions for a management view.
- Keep credentials on the server; do not embed API keys or private customer records in browser code, fixtures, or downloadable examples.

## Finance interface requirements

Read [references/finance_ui.md](references/finance_ui.md) for detailed patterns when building dashboards, screeners, portfolio/risk views, or recurring monitors.

Always handle the relevant cases:

- **Context:** source, as-of timestamp, currency, units, frequency, and whether prices are adjusted.
- **Data states:** loading, empty, partial, stale, unavailable, and error. Never silently replace failed data retrieval with invented values.
- **Numbers:** consistent precision, thousands separators, explicit percentage and basis-point conventions, and aligned numeric columns.
- **Charts:** labeled axes and units, honest scales, readable legends, and a clear benchmark or comparison period where relevant.
- **Risk:** distinguish observed values, estimates, scenarios, and user assumptions. Do not imply that an illustrative score is a validated investment recommendation.
- **Accessibility:** keyboard-operable controls, visible focus, sufficient contrast, and meaning that does not depend on red/green alone.
- **Responsiveness:** preserve the main workflow on laptop and smaller screens; allow wide tables to scroll without trapping the page.

For recurring dashboards, make refresh time and failures visible. Preserve an auditable record of the data and parameters behind a generated view when the project supports it.

## Aesthetic guidance

- Use distinctive typography that remains legible for financial data; use a tabular numeric font or font features where appropriate.
- Build a cohesive palette with CSS variables. Use accent colors to encode meaning, not decoration alone.
- Use asymmetric layouts, editorial spacing, or controlled density when they support the content. Avoid generic card grids that give every metric equal importance.
- Use motion to clarify transitions and state changes. Respect reduced-motion preferences and avoid animation that delays reading values.
- Avoid default purple gradients, interchangeable hero sections, excessive glass effects, and decoration that makes a finance tool look like a marketing page.

The interface should feel designed for its specific finance question. A stock screener, risk report, and earnings monitor should not share the same information hierarchy merely because they use the same component library.
