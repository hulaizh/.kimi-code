#!/usr/bin/env python3
"""
Validate Beamer slides against latex-slides conventions.

Checks for common issues:
- Missing Roadmap frame
- Inline TikZ (should be in figures/)
- Inline tables (should be in tables/)
- Missing frame titles
- Appendix usage
- Document class settings
- Visual Primacy violations:
  * content frames without any figure/table/equation
  * bullet walls (>=5 \\item per frame)
  * frame word count > 50 (math/figures/tables excluded)
  * running prose paragraphs (>=2 sentences without list/equation structure)
  * \\emph / \\textit holding sentence-long content (anti-pattern: italic asides)
  * \\centering\\emph or \\centering\\textit "takeaway" lines at frame foot

Usage:
    python validate_slides.py slides.tex
    python validate_slides.py path/to/slides.tex
"""

import re
import sys
from pathlib import Path


def validate_slides(filepath):
    """
    Validate a Beamer .tex file against latex-slides conventions.

    Parameters
    ----------
    filepath : str or Path
        Path to the .tex file.

    Returns
    -------
    list of dict
        Each dict has keys: line, severity, message.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        return [{"line": 0, "severity": "ERROR", "message": f"File not found: {filepath}"}]

    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    issues = []

    def add(line_num, severity, msg):
        issues.append({"line": line_num, "severity": severity, "message": msg})

    # --- Document class ---
    docclass_match = re.search(r"\\documentclass(\[.*?\])?\{beamer\}", text)
    if not docclass_match:
        add(1, "ERROR", "Document class is not beamer")
    else:
        opts = docclass_match.group(1) or ""
        if "aspectratio=169" not in opts:
            line_num = _find_line(lines, "\\documentclass")
            add(line_num, "WARN", "Missing aspectratio=169 in document class options")

    # --- Style import ---
    if "\\input{misc/style}" not in text:
        add(_find_line(lines, "\\input") or 1, "WARN", "Missing \\input{misc/style}")

    # --- Roadmap frame ---
    roadmap_count = sum(1 for l in lines if re.search(r"\\begin\{frame\}\{Roadmap\}", l))
    if roadmap_count == 0:
        add(0, "ERROR", "No Roadmap frame found (expected one after \\maketitle)")
    elif roadmap_count > 1:
        for i, l in enumerate(lines, 1):
            if re.search(r"\\begin\{frame\}\{Roadmap\}", l):
                add(i, "WARN", "Multiple Roadmap frames found (expected exactly one)")

    # --- Inline TikZ ---
    in_frame = False
    tikz_depth = 0
    for i, line in enumerate(lines, 1):
        if re.search(r"\\begin\{frame\}", line):
            in_frame = True
        if re.search(r"\\end\{frame\}", line):
            in_frame = False

        if in_frame and re.search(r"\\begin\{tikzpicture\}", line):
            add(i, "WARN", "Inline TikZ in frame — move to figures/*.tex and use \\input{}")
            tikz_depth += 1
        if re.search(r"\\end\{tikzpicture\}", line):
            tikz_depth -= 1

    # --- Inline tables ---
    in_frame = False
    for i, line in enumerate(lines, 1):
        if re.search(r"\\begin\{frame\}", line):
            in_frame = True
        if re.search(r"\\end\{frame\}", line):
            in_frame = False

        if in_frame and re.search(r"\\begin\{tabular\}", line):
            add(i, "WARN", "Inline table in frame — move to tables/*.tex and use \\input{}")

    # --- Missing frame titles ---
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == "\\begin{frame}":
            add(i, "WARN", "Frame without title — add descriptive title: \\begin{frame}{Title}")
        if re.match(r"\\begin\{frame\}\{Frame\s*\d+\}", stripped):
            add(i, "WARN", "Numbered frame title — use descriptive title instead")

    # --- Appendix ---
    appendix_lines = [i for i, l in enumerate(lines, 1) if "\\appendix" in l]
    if appendix_lines:
        # Check that appendix is near the end
        last_appendix = appendix_lines[-1]
        if last_appendix < len(lines) * 0.5:
            add(last_appendix, "WARN", "\\appendix appears early in document — usually placed near the end")

    # --- hline usage ---
    for i, line in enumerate(lines, 1):
        if "\\hline" in line:
            add(i, "WARN", "Use booktabs (\\toprule, \\midrule, \\bottomrule) instead of \\hline")

    # --- Column alignment ---
    for i, line in enumerate(lines, 1):
        if re.search(r"\\begin\{columns\}\[c\]", line):
            add(i, "WARN", "Use [T] alignment for columns instead of [c]")

    # --- Visual Primacy: every content frame should contain a figure,
    #     table, equation, or diagram. Roadmap, References, and frames
    #     whose title contains "Conclusion"/"Takeaway"/"Summary" are
    #     exempt because they're legitimate text-only stops.
    exempt_title_re = re.compile(
        r"Roadmap|References|Conclusion|Takeaway|Summary|Outline|Agenda|Thank",
        re.IGNORECASE,
    )
    visual_token_re = re.compile(
        r"\\input\{(figures|tables)/|"        # \input{figures/X} or \input{tables/X}
        r"\\includegraphics|"                   # raster figures
        r"\\begin\{(equation|align|gather)\*?\}|"  # display math
        r"\\\[",                                # \[ ... \] display math
    )
    item_re = re.compile(r"\\item\b")
    # \centering followed by \emph/\textit on the same logical block — the
    # "bottom-center italic takeaway" anti-pattern.
    centered_italic_re = re.compile(
        r"\\(centering|begin\{center\})[^\n]{0,80}\\(emph|textit)\{",
        re.MULTILINE,
    )
    # Long \emph or \textit content (sentence-long italic).
    italic_span_re = re.compile(r"\\(emph|textit)\{([^{}]*)\}")
    sentence_punct_re = re.compile(r"[.!?](\s|\\\\|$)")

    def _frame_word_count(body):
        """Count natural-language words in a frame body.

        Strips display math, inline math, equation/align/gather environments,
        \\input{figures|tables/...}, \\includegraphics{...}, and LaTeX
        commands. Counts only tokens with at least one alphabetic character.
        """
        b = body
        # Strip display math
        b = re.sub(r"\$\$.*?\$\$", " ", b, flags=re.S)
        b = re.sub(r"\\\[.*?\\\]", " ", b, flags=re.S)
        b = re.sub(
            r"\\begin\{(equation|align|gather|aligned|cases|split|multline)\*?\}.*?\\end\{\1\*?\}",
            " ",
            b,
            flags=re.S,
        )
        # Strip inline math
        b = re.sub(r"\$[^$]*\$", " ", b)
        # Strip visual includes (these have no narrative text)
        b = re.sub(r"\\(input|includegraphics|resizebox)\{[^}]*\}", " ", b)
        # Strip command names + their first {} arg (rough)
        b = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", b)
        # Strip braces and backslashes
        b = re.sub(r"[{}\\&%~]", " ", b)
        words = [w for w in b.split() if any(c.isalpha() for c in w)]
        return len(words)

    def _looks_like_prose(line):
        """Heuristic: a line of natural language ≥2 sentences with no
        list/visual/equation command on the same line."""
        stripped = line.strip()
        if not stripped:
            return False
        # Skip lines that ARE structure
        if re.match(
            r"\\(item|begin|end|input|includegraphics|caption|footnote|"
            r"section|subsection|subsubsection|paragraph|centering|"
            r"hypertarget|label|bibliography|frametitle|institute|"
            r"vspace|smallskip|medskip|bigskip|vfill|hfill|noindent|"
            r"goto|tableofcontents|maketitle|titlegraphic|title|author|"
            r"date|textcolor|definecolor)",
            stripped,
        ):
            return False
        # Skip lines that contain a visual include
        if re.search(r"\\(input|includegraphics)\{", stripped):
            return False
        # Skip lines that are mostly math
        no_math = re.sub(r"\$[^$]*\$", "", stripped)
        if len(no_math) < 0.4 * len(stripped):
            return False
        # Count sentence terminators on this line
        sentences = len(sentence_punct_re.findall(stripped))
        # Long line + ≥2 sentence terminators = prose paragraph
        return len(stripped) > 100 and sentences >= 2

    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r"\\begin\{frame\}(?:\[[^\]]*\])?(?:\{(.*?)\})?", line)
        if not m:
            i += 1
            continue
        frame_start = i
        frame_title = (m.group(1) or "").strip()
        # Collect frame body until \end{frame}
        body_lines = []
        j = i + 1
        while j < len(lines) and r"\end{frame}" not in lines[j]:
            body_lines.append(lines[j])
            j += 1
        body = "\n".join(body_lines)
        i = j + 1

        # Exempt frames (Roadmap, References, conclusions, etc.)
        is_exempt = bool(exempt_title_re.search(frame_title))

        # --- Visual presence ---
        if not is_exempt and not visual_token_re.search(body):
            add(
                frame_start + 1,
                "WARN",
                f"Text-only content frame ({frame_title!r}) — Visual Primacy: "
                "add a figure (\\input{figures/...}), table (\\input{tables/...}), "
                "or display equation",
            )

        # --- Bullet wall ---
        item_count = len(item_re.findall(body))
        if item_count >= 5:
            add(
                frame_start + 1,
                "WARN",
                f"Bullet wall in frame ({frame_title!r}): {item_count} \\item entries "
                "— split into multiple frames or replace with a table/diagram",
            )

        # --- Word budget (skip exempt frames) ---
        if not is_exempt:
            wc = _frame_word_count(body)
            if wc > 50:
                add(
                    frame_start + 1,
                    "WARN",
                    f"Wordy frame ({frame_title!r}): {wc} words of natural language "
                    "(budget 50) — split, or replace prose with a labelled diagram / "
                    "annotated equation",
                )

        # --- Centered-italic takeaway anti-pattern ---
        if centered_italic_re.search(body):
            # find the line of the match relative to frame_start
            for k, bl in enumerate(body_lines):
                if re.search(r"\\(centering|begin\{center\})", bl) and re.search(
                    r"\\(emph|textit)\{", bl
                ):
                    add(
                        frame_start + 2 + k,
                        "WARN",
                        "Centered italic 'takeaway' line — use "
                        "\\begin{block}{Takeaway} (1 sentence) or a boxed display "
                        "equation; never \\centering\\emph{...}",
                    )
                    break
            else:
                # Multi-line case (\centering on one line, \emph two lines later)
                add(
                    frame_start + 1,
                    "WARN",
                    f"Centered italic block in frame ({frame_title!r}) — convert to "
                    "\\begin{block}{Takeaway} or boxed equation",
                )

        # --- Sentence-long or label-pattern \emph / \textit ---
        for em_match in italic_span_re.finditer(body):
            content = em_match.group(2).strip()
            cmd = em_match.group(1)
            words = len(content.split())
            has_sentence_punct = bool(sentence_punct_re.search(content))
            too_long = len(content) > 30
            too_many_words = words > 5

            if not (has_sentence_punct or too_long or too_many_words):
                continue

            upto = body[: em_match.start()]
            line_offset = upto.count("\n")

            # Classify the violation so the message is informative
            if has_sentence_punct and words <= 2:
                reason = (
                    f"\\{cmd}{{{content[:30]}}} is a label/mini-note in italic — "
                    "drop the italic; render as upright \\footnotesize text or merge into a bullet"
                )
            elif words > 5 or too_long:
                reason = (
                    f"\\{cmd}{{...}} contains {words}-word sentence-style content — "
                    "italic is for ≤3-word emphasis. Convert to a bullet or drop the italic"
                )
            else:
                reason = (
                    f"\\{cmd}{{...}} contains sentence punctuation — italic is for ≤3-word "
                    "emphasis only. Convert to a bullet or drop the italic"
                )

            add(frame_start + 2 + line_offset, "WARN", reason)

        # --- Prose paragraph ---
        for k, bl in enumerate(body_lines):
            if _looks_like_prose(bl):
                add(
                    frame_start + 2 + k,
                    "WARN",
                    "Running prose paragraph — convert to bullets, equation "
                    "annotations (\\underbrace), or a 2-column table",
                )

        # --- Free-floating text outside structured containers ---
        # Logic Structure principle: every line of text must live inside
        # itemize/enumerate/block/table/equation/diagram. Walk the frame
        # body and flag lines of natural-language text that fall outside
        # any open container. Skip exempt frames (Roadmap, References, etc.).
        if is_exempt:
            continue
        container_open = re.compile(
            r"\\begin\{(itemize|enumerate|block|exampleblock|alertblock|"
            r"tabular|columns|column|equation|align|gather|aligned|cases|"
            r"split|multline|tikzpicture|center|figure|table)\*?\}"
        )
        container_close = re.compile(
            r"\\end\{(itemize|enumerate|block|exampleblock|alertblock|"
            r"tabular|columns|column|equation|align|gather|aligned|cases|"
            r"split|multline|tikzpicture|center|figure|table)\*?\}"
        )
        structure_line = re.compile(
            r"\\(item|input|includegraphics|caption|footnote|"
            r"hypertarget|label|frametitle|titlegraphic|"
            r"vspace|smallskip|medskip|bigskip|vfill|hfill|noindent|"
            r"goto|tableofcontents|maketitle|title|author|date|"
            r"resizebox|smallskip|medskip|bigskip|setbeamercolor|"
            r"setbeamerfont|centering|raggedright|raggedleft|"
            r"footnotesize|scriptsize|tiny|small|normalsize|large|"
            r"renewcommand|newcommand|setlength|arraystretch|"
            r"rule|hrule|par)\b"
        )
        depth = 0
        first_offender_line = None
        for k, bl in enumerate(body_lines):
            stripped = bl.strip()
            if not stripped:
                continue
            # Update depth for opens/closes on this line
            opens = len(container_open.findall(bl))
            closes = len(container_close.findall(bl))
            # If we're already inside a container, anything goes
            if depth > 0:
                depth += opens - closes
                if depth < 0:
                    depth = 0
                continue
            depth += opens - closes
            if depth < 0:
                depth = 0
            # depth == 0 here: line is at frame top level
            # Skip lines that ARE container open/close
            if container_open.search(bl) or container_close.search(bl):
                continue
            # Skip pure-structure lines
            if structure_line.match(stripped):
                continue
            # Skip pure-math lines: line is wholly inside $...$ or \[...\]
            if re.match(r"\\\[", stripped) or stripped.endswith("\\]"):
                continue
            if re.match(r"^\$+.*\$+$", stripped):
                continue
            # Skip comment lines
            if stripped.startswith("%"):
                continue
            # Skip lines with only punctuation / control
            if not re.search(r"[A-Za-z]{4,}", stripped):
                continue
            # This is a natural-language line at frame top level outside
            # any container — Logic Structure violation.
            if first_offender_line is None:
                first_offender_line = frame_start + 2 + k
                preview = re.sub(r"\s+", " ", stripped)[:80]
                add(
                    first_offender_line,
                    "WARN",
                    f"Free-floating text outside any structure: \"{preview}…\" — "
                    "wrap in \\begin{itemize}, \\begin{block}, a table, or equation "
                    "annotation. Bullets cue your speech; bare text doesn't",
                )

        # --- Topic-only frame title (no verb) ---
        # Skip very short titles ("Roadmap"), exempt frames, and titles
        # that already look like assertions (contain a verb-like word).
        if (
            not is_exempt
            and frame_title
            and 2 <= len(frame_title.split()) <= 6
            and not re.search(
                r"\b(is|are|was|were|has|have|do|does|did|can|cannot|"
                r"shows|show|implies|imply|reduces|reduce|drives|drive|"
                r"explains|explain|narrows|widens|increases|decreases|"
                r"matters|holds|fits|misses|differ|differs|differs"
                r")\b",
                frame_title,
                re.IGNORECASE,
            )
            and not frame_title.endswith("?")
        ):
            # Heuristic: if no verb-like cue and no question mark, it's
            # likely a topic-noun title. Only mention this once per file
            # to avoid spam; treat as INFO not WARN.
            add(
                frame_start + 1,
                "INFO",
                f"Topic-noun title ({frame_title!r}) — consider rewriting as a "
                "sentence-headline assertion (e.g. \"X drives Y\")",
            )

    return issues


def _find_line(lines, pattern):
    """Find the first line number containing pattern."""
    for i, line in enumerate(lines, 1):
        if pattern in line:
            return i
    return 0


def print_report(issues, filepath):
    """Print a formatted validation report."""
    print(f"Validating: {filepath}")
    print("=" * 60)

    if not issues:
        print("All checks passed.")
        return

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]
    infos = [i for i in issues if i["severity"] == "INFO"]

    for issue in issues:
        line_str = f"L{issue['line']:>4}" if issue["line"] > 0 else "     "
        sev = issue["severity"]
        print(f"  {line_str}  [{sev:>5}]  {issue['message']}")

    print("-" * 60)
    print(f"  {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_slides.py <slides.tex>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    issues = validate_slides(filepath)
    print_report(issues, filepath)
    sys.exit(1 if any(i["severity"] == "ERROR" for i in issues) else 0)


if __name__ == "__main__":
    main()
