#!/usr/bin/env python3
"""Generate the canonical two-table caption+content wrapper used in academic finance papers.

GAN error log #31 documents that Generator scripts consistently get this pattern wrong
when they hand-write it: they collapse caption + content into a single \\begin{table}
block, or omit the \\vspace{-1.5cm} spacer. This script writes the correct pattern
deterministically, so neither the Generator nor the Critic has to reconstruct it.

The output is a Level-2 wrapper destined for `sections/tables.tex`. It pulls in the
Level-1 content file (`tables/<label>.tex`) via \\input.

Usage (CLI, prints to stdout — pipe / redirect into sections/tables.tex):

    python build_table_wrapper.py \\
      --label main_results \\
      --caption "Main DID estimates of policy effect on log earnings" \\
      --content tables/main_results \\
      --description "Coefficients from the staggered DID specification..." \\
      --equation 'y_{it} = \\beta D_{it} + X_{it}\\gamma + \\alpha_i + \\delta_t + \\varepsilon_{it}' \\
      --se-cluster firm \\
      --sample "Compustat 2000-2020, manufacturing firms" \\
      --fe "firm and year fixed effects"

Or as a Python module:

    from build_table_wrapper import build_wrapper
    tex = build_wrapper(
        label='main_results',
        caption='Main DID estimates...',
        content_path='tables/main_results',
        description='Coefficients from the staggered DID specification...',
        equation='y_{it} = \\beta D_{it} + ...',
        se_cluster='firm',
    )
    Path('sections/tables.tex').write_text(tex, ...)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SIG_STARS = r'$^{*}p<.1; ^{**}p<.05; ^{***}p<.01$'

TEMPLATE = r"""\clearpage
\begin{{table}}[htp!]
\caption{{{caption}}} \label{{tab:{label}}}
{{\footnotesize\justifying\setlength{{\parindent}}{{0pt}}
{description_block}}}
\end{{table}}

\vspace{{-1.5cm}}

\begin{{table}}[ht!]\centering \caption*{{}}
    \input{{{content_path}}}
\end{{table}}
"""


def build_wrapper(
    *,
    label: str,
    caption: str,
    content_path: str,
    description: str,
    equation: str | None = None,
    se_cluster: str | None = None,
    se_clusters: list[str] | None = None,
    sample: str | None = None,
    fe: str | None = None,
    extra_notes: str | None = None,
    significance_stars: bool = True,
    wide: bool = False,
) -> str:
    """Build a single Level-2 table wrapper following the two-table pattern.

    Required:
      label         — LaTeX label suffix (becomes `tab:<label>`); also matches the content filename stem
      caption       — Title that appears in the caption row
      content_path  — Path of the content file (without `.tex`), passed to `\\input{...}`
      description   — Self-contained prose description (will be augmented with equation, sample, FE, SE clusters, stars)

    Optional pieces of the description block — each becomes its own sentence:
      equation      — A LaTeX math expression (no surrounding $); stated once as ONE inline-math
                      sentence — never a display equation — unless the text numbers it, in which
                      case put `equation (\\ref{eq:...})` in the description and omit this
      se_cluster    — Single clustering level (string)
      se_clusters   — Multiple clustering levels (list); takes precedence over se_cluster if both given
      sample        — Sample description (e.g., "Compustat 2000-2020")
      fe            — Fixed effects description (e.g., "firm and year fixed effects")
      extra_notes   — Any additional notes appended verbatim
      significance_stars — Whether to append the standard `$^{*}p<.1; ...$` line (default True)
      wide          — If True, wrap the content in `\\resizebox{\\textwidth}{!}{...}`
    """
    parts: list[str] = [description.rstrip()]

    if equation:
        eq = equation.strip()
        # Strip surrounding $$ or $ if user mistakenly added them
        eq = eq.lstrip('$').rstrip('$').strip()
        parts.append(f'The specification is ${eq}$.')

    if sample:
        parts.append(f'Sample: {sample}.')
    if fe:
        parts.append(f'Specifications include {fe}.')
    if se_clusters:
        clust_str = ' and '.join(se_clusters)
        parts.append(f'Standard errors clustered by {clust_str} in parentheses.')
    elif se_cluster:
        parts.append(f'Standard errors clustered by {se_cluster} in parentheses.')
    if extra_notes:
        parts.append(extra_notes.rstrip())
    if significance_stars:
        parts.append(SIG_STARS + '.')

    description_block = '\n'.join(parts)

    if wide:
        # Inject \resizebox into the second table block
        wide_template = TEMPLATE.replace(
            r'\input{{{content_path}}}',
            r'\resizebox{{\textwidth}}{{!}}{{\input{{{content_path}}}}}',
        )
        tex = wide_template.format(
            caption=caption, label=label,
            description_block=description_block,
            content_path=content_path,
        )
    else:
        tex = TEMPLATE.format(
            caption=caption, label=label,
            description_block=description_block,
            content_path=content_path,
        )

    return tex


def _cli() -> int:
    p = argparse.ArgumentParser(
        description="Generate canonical two-table caption+content wrapper for sections/tables.tex.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument('--label', required=True, help="Label suffix; becomes tab:<label>")
    p.add_argument('--caption', required=True, help="Caption / title text")
    p.add_argument('--content', required=True, help="Path of the content file without .tex (e.g., tables/main_results)")
    p.add_argument('--description', required=True, help="Self-contained prose description")
    p.add_argument('--equation', default=None,
                   help="Specification in LaTeX (without surrounding $), stated as one inline-math "
                        "sentence; omit it when the description references the text's numbered equation")
    p.add_argument('--se-cluster', dest='se_cluster', default=None,
                   help="Single clustering level (e.g., 'firm')")
    p.add_argument('--se-clusters', dest='se_clusters', nargs='+', default=None,
                   help="Multiple clustering levels (e.g., --se-clusters firm year)")
    p.add_argument('--sample', default=None, help="Sample description")
    p.add_argument('--fe', default=None, help="Fixed effects description (e.g., 'firm and year fixed effects')")
    p.add_argument('--extra', dest='extra_notes', default=None, help="Additional notes appended verbatim")
    p.add_argument('--no-stars', dest='significance_stars', action='store_false',
                   help="Suppress the standard significance-stars footnote")
    p.add_argument('--wide', action='store_true', help="Wrap content in \\resizebox{\\textwidth}{!}{...}")
    p.add_argument('--out', default=None, help="Append output to this file instead of stdout")
    args = p.parse_args()

    tex = build_wrapper(
        label=args.label,
        caption=args.caption,
        content_path=args.content,
        description=args.description,
        equation=args.equation,
        se_cluster=args.se_cluster,
        se_clusters=args.se_clusters,
        sample=args.sample,
        fe=args.fe,
        extra_notes=args.extra_notes,
        significance_stars=args.significance_stars,
        wide=args.wide,
    )

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'a') as f:
            f.write(tex)
            f.write('\n')
    else:
        sys.stdout.write(tex)
    return 0


if __name__ == '__main__':
    sys.exit(_cli())
