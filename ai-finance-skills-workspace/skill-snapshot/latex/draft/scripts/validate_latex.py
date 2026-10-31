#!/usr/bin/env python3
"""
Validate LaTeX paper formatting against academic conventions.

Usage:
    python validate_latex.py <path/to/main.tex>

ADMISSION RULE (user directive, 2026-08-11): a check lives here ONLY if the
failure is (1) OFTEN-WRONG in practice — it occurs on a surface agents/users
actually edit (wrappers, sections, scripts' output, hand-added coauthors), or
sits under active incentive pressure (the page-cap gaming family: 11pt
downgrade was observed in the wild; margins and spacing are the adjacent
vectors) — AND (2) NECESSARY — the damage is silent (compiles fine, breaks
conventions or calibrations nobody re-reads). Template-carried conventions
that nothing normally disturbs (\\input{style}, chicago bib style, bib/tables
order, \\clearpage before the exhibit section inputs, Roman exhibit
numbering) are NOT checked: the template ships them and a missing/broken copy
either fails the compile loudly or cannot drift in the scaffolded flow.
"""

import re
import sys
from pathlib import Path


_DOCUMENTCLASS_RE = re.compile(r'\\documentclass\s*(?:\[([^\]]*)\])?\s*\{\s*([^}]*?)\s*\}')


def check_document_class_name(content: str) -> list[str]:
    """Drafting structure: the class is `article` (the section-file grammar,
    the two-level exhibits and the page-count arithmetic assume it;
    `report`/`book` add chapter pages and change the page capacity). The
    layout facts govern the OPTIONS only."""
    m = _DOCUMENTCLASS_RE.search(_strip_tex_comments(content))
    if not m:
        return ["main.tex has no live \\documentclass — the drafting structure requires "
                "\\documentclass[<paper>, <font>pt]{article}"]
    if m.group(2) != "article":
        return [f"Document class is {{{m.group(2)}}}; the drafting structure requires {{article}} "
                f"— use \\documentclass[{m.group(1) or '...'}]{{article}}"]
    return []


def check_document_class(content: str, font_pt: int = 12,
                         paper: str = "a4paper") -> list[str]:
    """The working-paper fallback layout's document class (a4paper 12pt),
    over the structure check (`check_document_class_name`). The option list
    is PARSED — any order and spacing of `[12pt,a4paper]` / `[a4paper, 12pt]`
    is the same class — and a downgrade from the required 12pt to 11pt (the
    page-cap gaming move observed in the wild) is named explicitly."""
    issues = check_document_class_name(content)
    if issues:
        return issues
    m = _DOCUMENTCLASS_RE.search(_strip_tex_comments(content))
    opts = [o.strip() for o in (m.group(1) or "").split(",") if o.strip()]
    sizes = [o for o in opts if re.fullmatch(r"\d+pt", o)]
    papers = [o for o in opts if o.endswith("paper")]
    extra = [o for o in opts if o not in sizes and o not in papers]
    if extra:
        # twocolumn / landscape / draft change page capacity or output — the
        # format allows the paper size and the font size, nothing else
        issues.append(
            f"Document class carries option(s) {extra} beyond the paper size and "
            f"font size the working-paper format allows. Use exactly "
            f"\\documentclass[{paper}, {font_pt}pt]{{article}}.")
    if sizes != [f"{font_pt}pt"]:
        if font_pt == 12 and sizes == ["11pt"]:
            issues.append(
                "Document class uses 11pt; the working-paper format requires 12pt. "
                f"Change to \\documentclass[{paper}, 12pt]{{article}}. Do NOT downgrade "
                "the font to fit the page cap — shorten the paper instead.")
        else:
            issues.append(
                f"Document class font size is {sizes or 'unset'}; the working-paper format "
                f"requires {font_pt}pt on {paper}. Change to "
                f"\\documentclass[{paper}, {font_pt}pt]{{article}}.")
    if papers != [paper]:
        issues.append(
            f"Document class paper size is {papers or 'unset'}; the working-paper format "
            f"requires {paper}. Change to \\documentclass[{paper}, {font_pt}pt]{{article}}.")
    return issues


_DEFAULT_MARGINS = {"top": "1.5in", "bottom": "1.5in", "left": "1in", "right": "1in"}


def check_geometry(style_content: str, margins: dict | None = None, main_content: str = "") -> list[str]:
    """Check style.tex geometry matches the working-paper margins (1-inch
    left/right, 1.5-inch top/bottom; the page cap is calibrated for them,
    and shrinking margins silently allows a longer paper than the real cap),
    and that no live \\geometry{} / \\newgeometry{} override (style.tex or
    main.tex) changes the layout after the package load.
    """
    margins = margins or _DEFAULT_MARGINS
    issues = []
    for label, text in (("style.tex", style_content), ("main.tex", main_content)):
        if re.search(r'\\(?:new)?geometry\s*\{', _strip_tex_comments(text or "")):
            issues.append(
                f"{label}: a \\geometry{{...}} / \\newgeometry{{...}} override changes the page layout after "
                f"the geometry package load — the page cap is calibrated for the working-paper margins; remove it.")
    if issues:
        return issues
    required = ", ".join(f"{k}={v}" for k, v in margins.items())
    if not style_content:
        return issues  # style.tex not present at this layer; skip
    # Comment-stripped: a commented-out compliant geometry line must not
    # satisfy while a live noncompliant one runs.
    style_content = _strip_tex_comments(style_content)
    # Accept any geometry declaration that names ALL four required margins
    # (any order, any whitespace).
    geom_match = re.search(r'\\usepackage\[(.*?)\]\{geometry\}', style_content, re.DOTALL)
    if not geom_match:
        issues.append(
            f"style.tex: missing \\usepackage[...]{{geometry}}. Required: "
            f"\\usepackage[{required}]{{geometry}} (working-paper format)."
        )
        return issues
    opts = geom_match.group(1)
    def has(key: str, val: str) -> bool:
        return bool(re.search(rf'\b{key}\s*=\s*{re.escape(val)}\b', opts))
    bad = [f"{k}={v}" for k, v in margins.items() if not has(k, v)]
    if bad:
        issues.append(
            f"style.tex geometry is missing {', '.join(bad)}. Required: "
            f"\\usepackage[{required}]{{geometry}}. The manuscript page cap is "
            f"calibrated for the working-paper geometry; deviations silently "
            f"break the cap."
        )
    return issues


# ---------------------------------------------------------------------------
# The admitted-main GRAMMAR (convention: main.tex STATES the manuscript's
# spacing). ONE parser, two consumers: S0 (this validator) admits a main.tex
# only when the grammar holds, and the GAN page-cap gate reads the same scan
# (the appendix boundary, the recorder's include graph) — so the gate never
# re-derives the manuscript from a second regex set that can drift.
#
#   PREAMBLE  before \begin{document}
#   FRONT     from \begin{document} to the first body marker (abstract input,
#             title page); the LAST depth-0 spacing token in PREAMBLE+FRONT
#             (outside the abstract environment and outside definitions) is
#             the declared body spacing and must be \doublespacing or
#             \onehalfspacing — any other spacing control there switches the
#             body to an unpriced spacing
#   BODY      from the first body marker (a \input/\include of a sections/
#             prose file, or \section/\part/\chapter outside the abstract
#             environment) through the LAST prose marker: NO spacing control
#             at all, at any brace depth; a brace group that both changes the
#             spacing and inputs body prose is a switch
#   BACK      after the last prose marker (bibliography, exhibit wrappers,
#             Internet Appendix): spacing is the template's own
#   Every \input/\include in the document body targets sections/…; a macro
#   or environment DEFINITION whose body carries a spacing control is
#   rejected wherever it appears (main.tex or a section file) — a spacing
#   command reaches the body only by being written in main.tex; section files
#   (sections/**/*.tex, except exactly sections/appendix.tex — the IA lies
#   outside the cap) carry no spacing control.
# ---------------------------------------------------------------------------
_SPACING_TOKEN_PAT = (r'(?<![\w\\@])\\(?:doublespacing|onehalfspacing|singlespacing|setstretch|linespread'
                      r'|doublespace|onehalfspace|singlespace|baselinestretch)(?![A-Za-z@])'
                      r'|\\baselineskip\s*=|\\setlength\s*\{\s*\\baselineskip\s*\}|\\addtolength\s*\{\s*\\baselineskip\s*\}'
                      r'|\\begin\s*\{\s*(?:spacing|doublespace|onehalfspace|singlespace)\s*\}'
                      r'|\\usepackage\s*\[[^\]]*?(?:doublespacing|onehalfspacing|singlespacing)[^\]]*\]\s*\{\s*setspace\s*\}'
                      r'|\\csname\b(?:(?!\\endcsname).)*?(?:spacing|stretch|space|linespread)(?:(?!\\endcsname).)*?\\endcsname')
_SPACING_TOKEN_RE = re.compile(_SPACING_TOKEN_PAT, re.DOTALL)
_SETSTRETCH_ARG_RE = re.compile(r'\s*\{\s*([0-9.]+)\s*\}')
_SETSTRETCH_KINDS = {"2": "doublespacing", "2.0": "doublespacing", "1.5": "onehalfspacing"}


def _spacing_kind(tok: str, text: str, end: int) -> str | None:
    """The spacing KIND a declaration states: \\doublespacing / \\onehalfspacing,
    their environment and package-option forms, and \\setstretch{2} /
    \\setstretch{1.5} — the two stretch values that are the same two kinds
    written as numbers (a journal whose double is 2.0 rather than setspace's
    1.667 states it that way). Anything else is not a kind (None)."""
    if tok.startswith("\\setstretch"):
        m = _SETSTRETCH_ARG_RE.match(text, end)
        return _SETSTRETCH_KINDS.get(m.group(1)) if m else None
    if tok.startswith("\\single"):
        return None
    m = re.search(r'(double|onehalf)spac', tok)
    if m and (tok.startswith("\\usepackage") or tok.startswith("\\begin")
              or tok in ("\\" + m.group(1) + "spacing", "\\" + m.group(1) + "space")):
        return m.group(1) + "spacing"
    return None
_DEFN_CMD_PAT = (r'\\(?:(?:re)?newcommand\*?|providecommand\*?|DeclareRobustCommand\*?'
                 r'|(?:New|Renew|Provide|Declare)(?:Expandable)?DocumentCommand|NewCommandCopy'
                 r'|(?:re)?newenvironment\*?|(?:New|Renew|Provide|Declare)DocumentEnvironment'
                 r'|def|edef|gdef|xdef|let|futurelet'
                 r'|AtBeginDocument|AtEndPreamble|AfterEndPreamble|AtEndOfClass|AtEndOfPackage|AddToHook|apptocmd|pretocmd'
                 r')(?![A-Za-z@])')
_DEFN_CMD_RE = re.compile(_DEFN_CMD_PAT)
_MAIN_TOKEN_RE = re.compile(
    r'\\\\|\\[{}%]|(?P<open>\{)|(?P<close>\})'
    r'|\\begin\s*\{\s*(?P<begin>document|abstract)\s*\}|\\end\s*\{\s*(?P<end>abstract|document)\s*\}'
    r'|(?P<sp>' + _SPACING_TOKEN_PAT + r')'
    r'|\\includeonly\s*\{\s*(?P<only>[^}]*)\}'
    r'|\\(?P<inpcmd>input|include)\s*\{\s*(?P<inp>[^}]+?)\s*\}'
    r'|(?P<sec>\\(?:section|part|chapter)\*?\s*(?=[{\[]))'
    r'|(?P<back>\\bibliography\s*\{|\\printbibliography\b|\\begin\s*\{\s*thebibliography\b)'
    r'|(?P<defn>' + _DEFN_CMD_PAT + r')', re.DOTALL)
_SECTIONING_RE = re.compile(r'(?<![\w\\@])\\(?:section|part|chapter)\*?\s*[{\[]')
_TAIL_NOISE_RE = re.compile(r'\\(?:clearpage|newpage|noindent|bigskip|medskip|smallskip|centering|raggedright)\b'
                            r'|\\vspace\*?\s*\{[^}]*\}|\s+')
_SECTION_INPUT_RE = re.compile(r'\\(?:input|include)\s*\{\s*([^}]+?)\s*\}')
# inclusion forms the grammar does not follow — a manuscript uses \input/\include with a braced sections/ path
_UNSUPPORTED_INCLUDE_RE = re.compile(r'(?<![\w\\@])\\(?:subfile|import|subimport|inputfrom|includefrom|subfileinclude'
                                     r'|input(?![A-Za-z@])(?!\s*\{))(?![A-Za-z@])')
_OPTIONAL_INPUT_RE = re.compile(r'\\InputIfFileExists\s*\{\s*([^}]+?)\s*\}')


def _norm_input(target: str) -> str:
    r"""An `\input`/`\include` target as TeX resolves it, normalized for the
    prefix rules: whitespace and a `.tex` suffix dropped, `.`/`..` segments
    collapsed (`sections/../outside` → `outside`), an absolute path kept
    absolute (never under sections/)."""
    import posixpath
    name = target.strip().replace("\\", "/")
    if name.endswith(".tex"):
        name = name[:-4]
    return posixpath.normpath(name) if name else name


def _foreign_extension(target: str) -> bool:
    """`sections/results.ltx` is a real file TeX would read; the grammar
    follows `.tex` files only, so any other extension is refused."""
    name = target.strip().rsplit("/", 1)[-1]
    return "." in name and not name.endswith(".tex")


def _balanced_group_end(text: str, i: int) -> int:
    """`i` at `{` → index just past its matching `}` (escaped braces skipped)."""
    n = len(text)
    depth = 0
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def _bracket_arg_end(text: str, i: int) -> int:
    """`i` at `[` → index just past the `]` that closes it, brace groups
    inside skipped (`[1][{]}]` is one optional argument)."""
    n = len(text)
    i += 1
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            i = _balanced_group_end(text, i)
            continue
        if c == "]":
            return i + 1
        i += 1
    return n


def _first_unescaped_brace(text: str, i: int) -> int:
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            return i
        i += 1
    return -1


def _definition_span_end(text: str, start: int) -> int:
    r"""End of the definition that starts at `start`: `\let`/`\futurelet` own
    the rest of their line; the `\def` family owns everything through the
    FIRST unescaped balanced brace group (its parameter text may carry any
    delimiter, `\{` included: `\def\x#1\{y\}#2{...}`); every other
    definition/hook command owns its name token, optional arguments (brace
    nesting inside `[...]` honored) and each balanced brace group that
    follows, across line breaks (`\newcommand{\x}\n  {...}`)."""
    n = len(text)
    m = re.match(_DEFN_CMD_PAT, text[start:])
    cmd = m.group(0)
    i = start + len(cmd)
    if cmd in ("\\let", "\\futurelet"):
        # \let<cs>[ ]?=?[ ]?<token>: the assigned token may sit on the next
        # line — own exactly the name, the optional `=` and ONE token
        m2 = re.match(r'\s*(?:\\[A-Za-z@]+|\\.)\s*=?\s*(?:\\[A-Za-z@]+|\\.|.)', text[i:], re.DOTALL)
        return i + (len(m2.group(0)) if m2 else 0)
    if cmd in ("\\def", "\\edef", "\\gdef", "\\xdef"):
        j = _first_unescaped_brace(text, i)
        return n if j < 0 else _balanced_group_end(text, j)
    # how many brace groups the command takes after its (optional) name and
    # optional arguments: environments and xparse environments take two
    # (begin/end code), hooks and commands one
    bare = cmd.lstrip("\\").rstrip("*")
    groups_wanted = 2 if ("environment" in bare or bare.endswith("Environment")) else 1
    if bare in ("NewDocumentCommand", "RenewDocumentCommand", "ProvideDocumentCommand", "DeclareDocumentCommand",
                "NewExpandableDocumentCommand", "AddToHook", "apptocmd", "pretocmd", "NewCommandCopy"):
        groups_wanted = 2  # <name>{arg spec}{body} / {hook}{code} / {cmd}{code}
    name_taken = False
    groups = 0
    while i < n and groups < groups_wanted:
        while i < n and text[i].isspace():
            i += 1
        if i >= n:
            break
        c = text[i]
        if c == "{":
            j = _balanced_group_end(text, i)
            is_env = "environment" in bare or bare.endswith("Environment")
            if not name_taken and groups == 0 and (is_env or re.fullmatch(r'\{\s*\\[A-Za-z@]+\s*\}', text[i:j] or "")) \
                    and bare not in ("AtBeginDocument", "AtEndPreamble", "AfterEndPreamble", "AtEndOfClass", "AtEndOfPackage", "AddToHook"):
                name_taken = True  # `{\x}` — the command being defined; `{name}` — the environment being defined
            else:
                groups += 1
            i = j
            continue
        if c == "[":
            i = _bracket_arg_end(text, i)
            continue
        if not name_taken and groups == 0 and c == "\\":
            m2 = re.match(r'\\[A-Za-z@]+|\\.', text[i:])
            i += len(m2.group(0)) if m2 else 1
            name_taken = True
            continue
        break
    return i


def _definition_spans(text: str) -> list:
    spans = []
    pos = 0
    while True:
        m = _DEFN_CMD_RE.search(text, pos)
        if not m:
            return spans
        end = _definition_span_end(text, m.start())
        spans.append((m.start(), end))
        pos = max(end, m.end())


def strip_inert_tex(text: str) -> str:
    """`text` reduced to what TeX typesets: comments removed, everything after
    `\\end{document}` dropped, definition/hook bodies blanked (positions
    preserved) — the surface a label or a float must sit in to exist."""
    body = re.split(r'\\end\s*\{\s*document\s*\}', _strip_tex_comments(text))[0]
    return _without_spans(body, _definition_spans(body))


def _in_spans(spans: list, pos: int) -> bool:
    return any(a <= pos < b for a, b in spans)


def _without_spans(text: str, spans: list) -> str:
    """`text` with every span blanked (positions preserved)."""
    out = text
    for a, b in spans:
        out = out[:a] + " " * (b - a) + out[b:]
    return out


def _carries_prose(sections_dir, name: str) -> bool:
    """Whether `sections/<name>` is a PROSE section (a sectioning command
    inside it, comment-stripped) rather than front matter (a title page).
    Consulted only BEFORE the body starts; unknown without the directory or
    an unreadable file counts as prose (fail closed)."""
    if sections_dir is None:
        return True
    try:
        body = _strip_tex_comments((Path(sections_dir) / f"{name}.tex").read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return True
    return bool(_SECTIONING_RE.search(body))


def _resolve_optional_inputs(text: str, root) -> str:
    """`\\InputIfFileExists{x}{}{}` — an existing file is input like `\\input{x}`
    (and follows every rule); an absent one is inert. Without a root the
    form is refused (rewritten to an unsupported token)."""
    def _sub(m):
        target = m.group(1).strip()
        if root is not None:
            cand = Path(root) / (target if target.endswith(".tex") else target + ".tex")
            return f"\\input{{{target}}}" if cand.is_file() else " " * len(m.group(0))
        return "\\inputfrom" + " " * max(0, len(m.group(0)) - 10)
    return _OPTIONAL_INPUT_RE.sub(_sub, text)


def _scan_main_text(content: str, sections_dir=None, root=None) -> dict:
    r"""The grammar over main.tex's text (see the block comment above):
    {spacing, declared_kinds, body_inputs, wrappers, appendix_wired,
    appendix_closes, preamble_inputs, issues}. `spacing` is "doublespacing"
    | "onehalfspacing" | None (nothing admissible declared, or the grammar
    is violated — never guess a looser cap from a violated main.tex).
    `body_inputs` are the sections/… prose files main.tex inputs, in order
    (names relative to sections/, `.tex` appended; before the body starts a
    sections/ input without a sectioning command — a title page — is front
    matter, judged with `sections_dir`; once the body has started every
    sections/ input is body prose); `wrappers` the exhibit wrappers input
    in the body; `appendix_wired` whether sections/appendix is input in the
    document outside a definition, `appendix_closes` whether that input is
    the LAST content marker (bibliography and wrappers before it) — only
    then can the compiled Internet Appendix be cut off the page count;
    `preamble_inputs` the files input before \begin{document} (style.tex).
    `\includeonly` is honored for `\include`."""
    text = re.split(r'\\end\s*\{\s*document\s*\}', _strip_tex_comments(content))[0]
    text = _resolve_optional_inputs(text, root)
    spans = _definition_spans(text)
    issues: list = []
    um = _UNSUPPORTED_INCLUDE_RE.search(text)
    if um:
        issues.append(
            f"main.tex includes content with `{um.group(0)}` — the grammar follows only a braced "
            "\\input/\\include of a sections/ path; other inclusion forms hide body prose from the page cap.")
    for a, b in spans:
        if _SPACING_TOKEN_RE.search(text[a:b]):
            issues.append(
                "main.tex defines a macro, environment or document hook whose body changes the line spacing "
                f"(`{text[a:b].strip().splitlines()[0][:60]}`) — spacing is written directly in main.tex, "
                "never through a definition (the page cap is keyed on what main.tex states).")
            break
    in_document = False
    in_abstract = False
    depth = 0
    open_groups: list = []
    next_group = 0
    marker_groups: set = set()
    spacing_tokens: list = []  # (pos, end, token, depth, open-group ids)
    body_inputs: list = []
    wrappers: list = []
    preamble_inputs: list = []
    document_inputs: list = []  # every sections/ file input in the document, in order
    appendix_wired = False
    appendix_pos = -1
    includeonly: set | None = None
    inert_spans: list = []  # excluded \include commands: typeset nothing
    first_marker = None
    last_prose_pos = -1
    back_marks: list = []  # positions of BACK markers (bibliography, wrappers, IA)
    for m in _MAIN_TOKEN_RE.finditer(text):
        if _in_spans(spans, m.start()):
            continue  # inside a definition: not executed here
        if m.group("open"):
            depth += 1
            open_groups.append(next_group)
            next_group += 1
            continue
        if m.group("close"):
            if open_groups:
                open_groups.pop()
            depth = max(0, depth - 1)
            continue
        if m.group("begin") == "document":
            in_document = True
            continue
        if m.group("begin") == "abstract":
            in_abstract = True
            continue
        if m.group("end") == "abstract":
            in_abstract = False
            continue
        if m.group("only") is not None:
            includeonly = {_norm_input(x) for x in m.group("only").split(",") if x.strip()}
            continue
        if m.group("sp"):
            if m.group("sp").startswith("\\csname"):
                issues.append(
                    f"main.tex builds a spacing control with `{m.group('sp')[:60]}` — the grammar cannot read it; "
                    "write the spacing command directly.")
            elif not in_abstract:
                spacing_tokens.append((m.start(), m.end(), m.group("sp"), depth, set(open_groups)))
            continue
        if m.group("defn"):
            continue
        if m.group("back") is not None:
            back_marks.append(m.start())
            continue
        if m.group("sec") is not None:
            if not in_abstract:
                first_marker = m.start() if first_marker is None else first_marker
                last_prose_pos = m.start()
                marker_groups.update(open_groups)
            continue
        target = m.group("inp")
        if target is None:
            continue
        if _foreign_extension(target):
            issues.append(
                f"main.tex inputs `{target.strip()}` — only `.tex` files are followed by the grammar; "
                "rename the file or fold it into a sections/*.tex file.")
            continue
        name = _norm_input(target)
        if not in_document:
            preamble_inputs.append(name)
            continue
        if m.group("inpcmd") == "include" and includeonly is not None and name not in includeonly:
            inert_spans.append((m.start(), m.end()))
            continue  # excluded by \includeonly: not typeset
        if not name.startswith("sections/"):
            issues.append(
                f"main.tex inputs `{target.strip()}` inside the document body — body content lives in "
                "sections/*.tex only (the section-file grammar and the page cap read nothing else).")
            continue
        sec = name[len("sections/"):]
        if f"{sec}.tex" in document_inputs:
            issues.append(
                f"main.tex inputs sections/{sec}.tex twice inside the document — every exhibit, label and "
                "paragraph in it is typeset twice (one live inclusion per file).")
            continue
        document_inputs.append(f"{sec}.tex")
        if sec == "abstract":
            continue
        if sec == "appendix":
            appendix_wired = True
            appendix_pos = m.start()
            back_marks.append(m.start())
            continue
        if sec in ("tables", "figures"):
            wrappers.append(f"{sec}.tex")
            back_marks.append(m.start())
            continue
        if first_marker is None and not _carries_prose(sections_dir, sec):
            continue  # front matter (a title page) before the body: no prose, no marker
        body_inputs.append(f"{sec}.tex")
        first_marker = m.start() if first_marker is None else first_marker
        last_prose_pos = m.start()
        marker_groups.update(open_groups)
    body_end = min([p for p in back_marks if p > last_prose_pos] or [len(text)]) if first_marker is not None else len(text)
    appendix_closes = appendix_wired and appendix_pos > last_prose_pos and all(p <= appendix_pos for p in back_marks)
    if appendix_wired and not appendix_closes:
        # an in-cap appendix (before the bibliography or the wrappers) is body
        # prose: counted, priced, and subject to the section-file rule
        body_inputs.append("appendix.tex")
    declared = None
    declared_kinds: list = []
    for pos, end, tok, d, groups in spacing_tokens:
        in_body = first_marker is not None and first_marker < pos < body_end
        tail_back = False
        if in_body and pos > last_prose_pos:
            # the tail of the body: a switch is a switch only when prose
            # follows it before the back matter (the template's bibliography
            # / exhibit spacing sits directly before its marker); an excluded
            # \include typesets nothing
            tail = _SPACING_TOKEN_RE.sub(" ", _without_spans(text, inert_spans)[end:body_end])
            tail_back = not _TAIL_NOISE_RE.sub("", tail).strip()
        kind = _spacing_kind(tok, text, end)
        if kind and d == 0 and (not in_body or tail_back):
            if kind not in declared_kinds:
                declared_kinds.append(kind)
        if in_body:
            if tail_back:
                continue
            issues.append(
                f"main.tex switches the spacing with `{tok}` inside the BODY (over body prose) — "
                "the manuscript's spacing is stated once before the first section.")
            continue
        if first_marker is not None and pos >= body_end:
            continue  # BACK: bibliography / exhibits / IA spacing is the template's own
        if d > 0:
            if groups & marker_groups:
                issues.append(
                    f"main.tex changes the spacing with `{tok}` inside a brace group that also inputs body "
                    "prose — the body renders at a spacing main.tex does not state.")
            continue
        declared = tok
        declared_end = end
    spacing = None
    if declared is not None:
        # \doublespacing / \onehalfspacing, their environment-begin forms
        # (\doublespace … \enddoublespace, \begin{doublespace}), the
        # setspace package option, and \setstretch{2} / {1.5} all declare the kind
        spacing = _spacing_kind(declared, text, declared_end)
        if spacing is None:
            issues.append(
                f"main.tex switches the BODY spacing with `{declared}` before the first section; a "
                "manuscript states \\onehalfspacing or \\doublespacing (or \\setstretch{2} / {1.5}; a local "
                "\\singlespacing block after the body — bibliography, exhibits — is fine).")
    return {"spacing": spacing, "declared_kinds": declared_kinds, "body_inputs": body_inputs,
            "wrappers": wrappers, "appendix_wired": appendix_wired, "appendix_closes": appendix_closes,
            "preamble_inputs": preamble_inputs, "document_inputs": document_inputs, "issues": issues}


def scan_manuscript(main_tex: Path) -> dict:
    """The grammar over the whole manuscript, the ONE include graph:
    `_scan_main_text` on main.tex (front matter told apart by content), the
    body files' own sections/ inputs followed transitively (definitions and
    comments removed) into `body_inputs`, the preamble inputs (style.tex)
    scanned for any spacing control, and the section-file rule over
    sections/**/*.tex other than exactly sections/appendix.tex: no spacing
    control (a definition included), and every `\\input`/`\\include` targets
    sections/, tables/ or figures/ after normalization — body prose reaches
    the compiled manuscript only through files the grammar reads. A missing
    main.tex yields no spacing and one issue."""
    try:
        content = main_tex.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {"spacing": None, "declared_kinds": [], "body_inputs": [], "wrappers": [],
                "appendix_wired": False, "appendix_closes": False, "preamble_inputs": [],
                "document_inputs": [], "live_files": [],
                "issues": [f"{main_tex.name} is missing — nothing states the manuscript's spacing"]}
    root = main_tex.parent
    sections_dir = root / "sections"
    scan = _scan_main_text(content, sections_dir if sections_dir.is_dir() else None, root)

    def _read(path: Path):
        try:
            return _strip_tex_comments(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            return None

    # preamble inputs (style.tex …), followed transitively: any spacing control
    # in them, and any inclusion form the grammar cannot follow, is an issue
    pre_queue = list(scan["preamble_inputs"])
    pre_seen: list = []
    while pre_queue:
        name = pre_queue.pop(0)
        if name in pre_seen:
            continue
        pre_seen.append(name)
        body = _read(root / f"{name}.tex")
        if body is None:
            continue
        body = _resolve_optional_inputs(body, root)
        um = _UNSUPPORTED_INCLUDE_RE.search(body)
        if um:
            scan["issues"].append(f"{name}.tex (input in the preamble): includes content with `{um.group(0)}` — unsupported inclusion form.")
        m = _SPACING_TOKEN_RE.search(body)
        if m:
            scan["issues"].append(
                f"{name}.tex (input in the preamble): spacing control `{m.group(0)[:60]}` — line spacing is "
                "stated in main.tex only; a preamble file that sets or defines spacing hides it from the page cap.")
        for im in _SECTION_INPUT_RE.finditer(body):
            if _foreign_extension(im.group(1)):
                scan["issues"].append(f"{name}.tex (input in the preamble): inputs `{im.group(1).strip()}` — only `.tex` files are followed.")
                continue
            pre_queue.append(_norm_input(im.group(1)))
    # the body files' own sections/ inputs are body prose too (counted, priced);
    # every other document input (abstract, wrappers, appendix) is walked for
    # nested inputs as well, so nothing reachable from main.tex is unmodeled
    queue = list(scan["body_inputs"])
    seen: list = []
    reached: list = []
    edges: dict = {}  # parent -> children, the inclusion graph below main.tex
    walk = list(dict.fromkeys(scan["document_inputs"] + scan["body_inputs"]))
    while walk:
        name = walk.pop(0)
        if name in reached:
            continue
        reached.append(name)
        body = _read(sections_dir / name)
        if body is None:
            continue
        body = _without_spans(_resolve_optional_inputs(body, root), _definition_spans(body))
        for im in _SECTION_INPUT_RE.finditer(body):
            if _foreign_extension(im.group(1)):
                continue  # reported by the section-file rule below
            child = _norm_input(im.group(1))
            if child.startswith("sections/"):
                cname = child[len("sections/"):] + ".tex"
                edges.setdefault(name, []).append(cname)
                walk.append(cname)
                if name in scan["body_inputs"] or name in seen:
                    if cname not in ("abstract.tex", "tables.tex", "figures.tex", "appendix.tex") and cname not in seen:
                        seen.append(cname)  # nested body prose
    scan["body_inputs"] = list(dict.fromkeys(scan["body_inputs"] + seen))

    _inclusions: dict = {}
    for _kids in edges.values():
        for _k in _kids:
            _inclusions[_k] = _inclusions.get(_k, 0) + 1
    for _k, _n in sorted(_inclusions.items()):
        if _n > 1 or _k in scan["document_inputs"]:
            scan["issues"].append(
                f"sections/{_k} is input {_n + (1 if _k in scan['document_inputs'] else 0)} times below main.tex — "
                "its exhibits, labels and paragraphs are typeset that many times (one live inclusion per file).")

    def _closure(roots: list) -> set:
        out, stack = set(), list(roots)
        while stack:
            n = stack.pop()
            if n in out:
                continue
            out.add(n)
            stack.extend(edges.get(n, []))
        return out
    # a file's ROLE follows its inclusion ancestry, never its name: the
    # Internet Appendix is sections/appendix.tex and what only it reaches; a
    # file also reached from a body section or a wrapper is main-body content
    _ia_all = _closure(["appendix.tex"]) if scan["appendix_wired"] else set()
    _main_all = _closure([n for n in scan["document_inputs"] if n != "appendix.tex"] + scan["body_inputs"])
    scan["ia_files"] = sorted(_ia_all - _main_all) if scan["appendix_closes"] else []
    # the compiled manuscript: main.tex and every sections/ file it reaches —
    # the section-file rule and every downstream label/prose consumer read
    # exactly these; a file nothing inputs is inert (an old draft left on
    # disk blocks nothing)
    live_rel = list(dict.fromkeys(scan["document_inputs"] + reached + scan["body_inputs"]))
    live = [main_tex] + [sections_dir / n for n in live_rel if (sections_dir / n).is_file()]
    # the recorder (`pdflatex -recorder` → main.fls, written by the plugin's
    # compile) is the ground truth of what TeX read: every .tex file under
    # the manuscript root it lists must be one the grammar modeled — a file
    # reached through an inclusion form the grammar does not follow (a macro
    # that expands to \input, \subfile, an unbraced \include) is an issue,
    # and it joins the live set so every rule still scans it
    recorded = _recorded_tex_inputs(main_tex)
    scan["recorder"] = {"present": recorded is not None, "unmodeled": []}
    if recorded is not None:
        modeled = {p.resolve() for p in live} | {(root / f"{n}.tex").resolve() for n in scan["preamble_inputs"]} | {(root / f"{n}.tex").resolve() for n in pre_seen}
        content_dirs = ((root / "tables").resolve(), (root / "figures").resolve())  # the two-level architecture's exhibit CONTENT files (pure tabular, input by the wrappers; purity is S0's check_content_file_purity)
        for rp in recorded:
            rr = rp.resolve()
            if any(str(rr).startswith(str(d) + "/") for d in content_dirs):
                continue
            if rr not in modeled:
                scan["recorder"]["unmodeled"].append(str(rp.relative_to(root)) if str(rp).startswith(str(root)) else str(rp))
                scan["issues"].append(
                    f"the compile read `{rp.relative_to(root) if str(rp).startswith(str(root)) else rp}` (main.fls) but main.tex "
                    "reaches it through no \\input/\\include the grammar follows — an inclusion form outside the convention; "
                    "input the file with a braced \\input of a sections/ path.")
                if rp.is_file() and rp not in live:
                    live.append(rp)
    scan["live_files"] = [str(p) for p in live]
    for p in live:
        if p == main_tex:
            continue
        try:
            rel = p.relative_to(sections_dir).as_posix()
        except ValueError:
            rel = f"../{p.relative_to(root).as_posix()}" if str(p).startswith(str(root)) else str(p)
        if rel == "appendix.tex" and scan["appendix_closes"]:
            continue  # the Internet Appendix lies outside the cap; its spacing is its own
        body = _read(p)
        if body is None:
            continue
        body = _resolve_optional_inputs(body, root)
        um = _UNSUPPORTED_INCLUDE_RE.search(body)
        if um:
            scan["issues"].append(f"sections/{rel}: includes content with `{um.group(0)}` — unsupported inclusion form.")
        m = _SPACING_TOKEN_RE.search(body)
        if m:
            scan["issues"].append(
                f"sections/{rel}: spacing control `{m.group(0)[:60]}` — line spacing is stated in main.tex "
                "only (the page cap is keyed on what main.tex states); remove it from the section file.")
        for im in _SECTION_INPUT_RE.finditer(body):
            if _foreign_extension(im.group(1)):
                scan["issues"].append(f"sections/{rel}: inputs `{im.group(1).strip()}` — only `.tex` files are followed by the grammar.")
                break
            target = _norm_input(im.group(1))
            if not target.startswith(("sections/", "tables/", "figures/")):
                scan["issues"].append(
                    f"sections/{rel}: inputs `{im.group(1).strip()}` — a section file inputs only sections/, "
                    "tables/ or figures/ paths (body prose outside sections/ is invisible to the grammar and the page cap).")
                break
    return scan


def _recorded_tex_inputs(main_tex: Path):
    """The `.tex` files under the manuscript root that TeX read, from the
    recorder file the plugin's compile writes (`<main>.fls`: a `PWD` line
    then `INPUT`/`OUTPUT` lines, paths absolute or relative to PWD). None
    when no recorder file exists (the grammar then stands alone)."""
    fls = main_tex.with_suffix(".fls")
    if not fls.is_file():
        return None
    root = main_tex.parent.resolve()
    pwd = root
    out: list = []
    seen: set = set()
    try:
        lines = fls.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return None
    for ln in lines:
        if ln.startswith("PWD "):
            pwd = Path(ln[4:].strip())
            continue
        if not ln.startswith("INPUT "):
            continue
        raw = ln[6:].strip()
        if not raw.endswith(".tex"):
            continue
        p = Path(raw) if raw.startswith("/") else pwd / raw
        try:
            rp = p.resolve()
        except OSError:
            continue
        if str(rp).startswith(str(root) + "/") and rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out


def appendix_heading_text(main_tex: Path) -> str:
    """The Internet Appendix's own opening heading, as it will print — from
    sections/appendix.tex's first centered block or first `\\section{}`,
    with `\\Title` expanded from main.tex and TeX markup stripped; normalized
    (lower-case, letters/digits/spaces). The page-cap scan binds the IA
    boundary to THIS text, never to a generic phrase a caption could share.
    Empty when there is no appendix file or no heading in it."""
    root = main_tex.parent
    try:
        app = _strip_tex_comments((root / "sections" / "appendix.tex").read_text(encoding="utf-8", errors="ignore"))
        main = _strip_tex_comments(main_tex.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return ""
    m = re.search(r'\\begin\s*\{center\}(.*?)\\end\s*\{center\}', app, re.DOTALL) or re.search(r'\\section\*?\s*\{((?:[^{}]|\{[^{}]*\})*)\}', app)
    if not m:
        return ""
    heading = m.group(1)
    tm = re.search(r'\\newcommand\*?\s*\{\s*\\Title\s*\}\s*\{((?:[^{}]|\{[^{}]*\})*)\}', main) or re.search(r'\\title\s*\{((?:[^{}]|\{[^{}]*\})*)\}', main)
    heading = heading.replace("\\Title", tm.group(1) if tm else "")
    return normalize_heading(heading)


def normalize_heading(text: str) -> str:
    """Letters, digits and single spaces, lower-case — the same reduction for
    a TeX heading and for a pdftotext page opening."""
    text = re.sub(r'\\[A-Za-z@]+\*?', ' ', str(text or ""))
    text = re.sub(r'[{}`\'"“”‘’\\]', ' ', text)
    return " ".join(re.findall(r'[^\W_]+', text)).lower()


def check_line_spacing(scan: dict, spacings: tuple = ("onehalfspacing",)) -> list[str]:
    """The manuscript declares an accepted body spacing under the grammar
    (`scan_manuscript`). The working-paper format accepts only
    \\onehalfspacing (its page cap is calibrated for 1.5 spacing). A prohibited
    body-kind spacing (\\doublespacing / \\onehalfspacing, command or
    environment form) is flagged wherever main.tex declares it outside the
    body — beside the accepted declaration or before the bibliography — since
    a 1.5-spaced body followed by a late \\doublespacing is not a double-spaced
    manuscript; a \\singlespacing block after the body is the template's own."""
    issues = list(scan["issues"])
    accepted = " or ".join(f"\\{s}" for s in spacings)
    spacing = scan["spacing"]
    kinds = set(scan.get("declared_kinds") or []) | ({spacing} if spacing else set())
    for s in sorted(kinds - set(spacings)):
        issues.append(
            f"main.tex declares \\{s} (or its \\{s[:-3]}e environment form); the "
            f"working-paper format accepts only {accepted}. Remove it and "
            f"declare {accepted} throughout (bibliography and exhibits included).")
    if spacing is None and not issues:
        issues.append(
            f"main.tex is missing a line-spacing declaration ({accepted}); add it "
            f"after the abstract \\input.")
    return issues


def check_author_format(content: str) -> list[str]:
    """Check author format uses literal 'and' with single \\thanks.

    Coauthors are added in the \\newcommand{\\Author}{...} macro (the
    observed edit surface — the \\author{...} wrapper is template text that
    just references \\Author), so BOTH bodies are inspected: \\and or a
    second \\thanks inside the macro would otherwise pass unseen."""
    issues = []
    # Comment-stripped: a commented-out \Author draft line must neither
    # falsely flag (bad commented, good live) nor mask (good commented,
    # bad live) — only live declarations count.
    content = _strip_tex_comments(content)
    author_text = ""
    author_match = re.search(r'\\author\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)
    if author_match:
        author_text = author_match.group(1)
    # Balanced-brace extraction: multiline \Author definitions are real
    # (long thanks blocks) and a line-bound regex would let \and or a second
    # \thanks inside them pass unseen.
    macro_head = re.search(r'\\newcommand\{\\Author\}\s*\{', content)
    if macro_head:
        depth, i = 1, macro_head.end()
        start = i
        while i < len(content) and depth:
            c = content[i]
            if c == '\\':
                i += 2
                continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
            i += 1
        if depth == 0:
            author_text += "\n" + content[start:i - 1]
    if author_text:
        # Check for \and (should be literal "and")
        if re.search(r'\\and\b', author_text):
            issues.append("Use literal 'and' between authors, not \\and")
        # Check for multiple \thanks
        thanks_count = len(re.findall(r'\\thanks\{', author_text))
        if thanks_count > 1:
            issues.append(f"Use single \\thanks{{}} for all authors (found {thanks_count})")

    return issues


def check_abstract(content: str, project_dir: Path) -> list[str]:
    """Check abstract single-source-of-truth.

    Enforces the single-source rule for abstracts:
      CANONICAL: main.tex has \\input{sections/abstract} AND sections/abstract.tex
                 contains a \\begin{abstract}...\\end{abstract} block with JEL + Keywords.
      LEGACY OK: main.tex has inline \\begin{abstract}...\\end{abstract} block AND
                 sections/abstract.tex does NOT exist.

    DRIFT (blocked): main.tex has inline \\begin{abstract} AND sections/abstract.tex
                     also exists — these will silently diverge.
    ORPHAN (blocked): sections/abstract.tex exists but main.tex does NOT \\input it.
    """
    issues = []
    section_file = project_dir / "sections" / "abstract.tex"
    has_inline = bool(re.search(r'\\begin\{abstract\}', content))
    has_input = bool(re.search(r'\\input\{sections/abstract(?:\.tex)?\}', content))
    has_section_file = section_file.exists()

    # Drift: both exist
    if has_inline and has_section_file:
        issues.append(
            "Abstract drift: main.tex contains an inline \\begin{abstract} block AND "
            "sections/abstract.tex exists. Single source of truth violated — the two "
            "copies will diverge. Delete the inline block in main.tex and replace it with "
            "\\input{sections/abstract}."
        )

    # Orphan: section file exists but not included
    if has_section_file and not has_input:
        issues.append(
            "Orphan abstract: sections/abstract.tex exists but main.tex does not "
            "\\input{sections/abstract}. Edits to sections/abstract.tex will not reach "
            "the compiled PDF. Add \\input{sections/abstract} to main.tex."
        )

    # Input-without-file: main.tex inputs a nonexistent section
    if has_input and not has_section_file:
        issues.append(
            "Missing abstract file: main.tex uses \\input{sections/abstract} but "
            "sections/abstract.tex does not exist. Create the file or remove the \\input."
        )

    # Determine which source to validate contents against
    abstract_text: str | None = None
    if has_input and has_section_file:
        section_content = section_file.read_text()
        m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', section_content, re.DOTALL)
        if m:
            abstract_text = m.group(1)
        else:
            issues.append(
                "sections/abstract.tex exists but does not contain "
                "\\begin{abstract}...\\end{abstract}."
            )
    elif has_inline and not has_section_file:
        m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
        if m:
            abstract_text = m.group(1)

    if abstract_text is None and not (has_inline or has_input):
        issues.append(
            "No abstract found: main.tex should \\input{sections/abstract} "
            "(canonical) or contain an inline \\begin{abstract}...\\end{abstract} block."
        )

    if abstract_text is not None:
        if 'JEL' not in abstract_text:
            issues.append("Abstract missing JEL Classification")
        if 'Keywords' not in abstract_text and 'keywords' not in abstract_text:
            issues.append("Abstract missing Keywords")

    return issues


def check_main_section_inputs(content: str) -> list[str]:
    """Check main.tex uses the modular section layout in the expected order.

    Section PRESENCE is advisory (user decision 2026-08-14): a missing
    standard section yields a WARNING-prefixed entry steering toward the
    standard file names — always prefer them (the GAN per-section machinery
    keys on the canonical sections/*.tex chain) — but never a blocker. A
    paper may carry no theoretical model; may develop its estimator inside
    the results section rather than a separate methodology one; and may
    house its robustness work in the appendix — demanding files forces empty
    or duplicative sections, which games the gate instead of satisfying it.
    ORDER of the canonical sections that ARE present stays enforced (a real
    layout error). Consumers route entries by the "WARNING: " prefix;
    everything else from this module is blocking.

    Comment-stripped: commenting out a section input is a natural mid-draft
    move ("drop robustness for now"), and a commented input must not count
    as live — a silently missing section would escape the per-section
    machinery, which is exactly what the warning surfaces."""
    content = _strip_tex_comments(content)
    issues = []
    # The standard set the warning steers toward. "model" is intentionally
    # absent — it exists only when the paper carries a theoretical model, so
    # its absence is never even warned; and its POSITION is the paper's
    # choice (a theory-first paper opens with it, an empirical paper whose
    # model rationalizes the findings places it after the results), so it
    # takes no part in the order check either.
    standard_inputs = [
        "introduction",
        "data",
        "methodology",
        "results",
        "robustness",
        "conclusion",
    ]
    canonical_order = [
        "introduction", "data", "methodology",
        "results", "robustness", "conclusion",
    ]

    positions: list[tuple[str, int]] = []
    missing: list[str] = []
    for name in canonical_order:
        # Optional .tex extension: \input{sections/data.tex} is the same
        # live input — classifying it missing would also silently skip the
        # (blocking) order check over the real chain.
        m = re.search(rf'\\input\{{sections/{name}(?:\.tex)?\}}', content)
        if m is None and name in standard_inputs:
            missing.append(name)
        positions.append((name, m.start() if m else -1))
    if missing:
        issues.append(
            "WARNING: no live \\input{sections/<name>} for: "
            + ", ".join(missing)
            + ". Always prefer the standard section files — introduction, "
              "data, methodology, results, robustness, conclusion — the "
              "per-section round machinery keys on these names. A "
              "deliberate fold-in (e.g. methodology inside the framework "
              "section) is accepted; this is advisory only."
        )

    present_positions = [(name, pos) for name, pos in positions if pos >= 0]
    if any(
        present_positions[i][1] >= present_positions[i + 1][1]
        for i in range(len(present_positions) - 1)
    ):
        issues.append(
            "Main-text section inputs should appear in order: introduction, "
            "data, [methodology,] results, [robustness,] conclusion (a model "
            "section may sit anywhere between introduction and conclusion)"
        )

    return issues


def check_floats_in_wrappers_only(scan: dict) -> list[str]:
    """Two-level architecture: every table/figure float of the compiled
    manuscript sits in sections/tables.tex, sections/figures.tex or the
    Internet Appendix (sections/appendix.tex). A float inside a body section
    (results.tex, a nested part) is invisible to the wrapper checks and to
    the narrative trim gate that allocates the main body — move it to the
    wrapper and `\\ref` it."""
    issues: list = []
    wrappers = set(scan.get("wrappers") or [])
    for path in scan.get("live_files") or []:
        p = Path(path)
        # the role main.tex gives a file: a wrapper it inputs as such, the
        # closing Internet Appendix (sections/appendix.tex and the files under
        # sections/appendix*/ or named appendix_*.tex that it inputs) — never a basename alone
        rel = ""
        for anc in p.parents:
            if anc.name == "sections":
                rel = p.relative_to(anc).as_posix()
                break
        is_appendix = rel in set(scan.get("ia_files") or [])  # by inclusion ancestry (the grammar), never by name
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        body = strip_inert_tex(raw)
        # a macro DEFINITION is inert to the scanners — so a float or exhibit
        # material hidden inside one (typeset wherever the macro is invoked)
        # is refused at the definition
        _raw_nc = strip_tex_comments(raw)
        for (_s, _e) in _definition_spans(_raw_nc):
            seg = _raw_nc[_s:_e]
            if any(env_re.search(seg) for env_re in _EXHIBIT_ENV_RE.values()) or _exhibit_material(seg):
                issues.append(f"{p.name}: a macro definition carries a float or exhibit material ({seg[:40]!r}) — exhibits are written where they are typeset, never hidden in a definition")
                break
        if rel in wrappers or is_appendix:
            # an exhibit surface: floats belong here, but exhibit material
            # OUTSIDE a float (a content file input straight into the page, a
            # bare tabular/image) belongs to no exhibit — and a wrapper
            # carries ITS kind only (the exhibit parser reads tables.tex as
            # tables and figures.tex as figures; a figure float in tables.tex
            # is an exhibit no allocation sees)
            own_kind = {"tables.tex": "table", "figures.tex": "figure"}.get(rel) if rel in wrappers else None
            for kind, env_re in _EXHIBIT_ENV_RE.items():
                if own_kind and kind != own_kind and env_re.search(body):
                    issues.append(
                        f"{p.name}: a {kind} float in the {own_kind}s wrapper — {kind}s live in sections/{kind}s.tex")
            outside = body
            for env_re in _EXHIBIT_ENV_RE.values():
                outside = env_re.sub(lambda mm: " " * len(mm.group(0)), outside)
            sm = _exhibit_material(outside)
            if sm:
                issues.append(
                    f"{p.name}: exhibit material outside a float ({sm[:40]}) — every \\input of a tables/ or figures/ "
                    f"content file, image or tabular sits inside a \\begin{{table}}/\\begin{{figure}} float with its caption and label")
            continue
        m = None
        for kind, env_re in _EXHIBIT_ENV_RE.items():
            m = env_re.search(body)
            if m:
                issues.append(
                    f"{p.name}: a {kind} float outside the exhibit wrappers — exhibits live in "
                    f"sections/{kind}s.tex (or the closing Internet Appendix) and are referenced from the prose")
                break
        if m is None:
            # exhibit MATERIAL without a float — a content file input straight
            # into the prose, an image, a bare tabular or TikZ picture — is
            # typeset but belongs to no exhibit
            sm = _exhibit_material(body)
            if sm:
                issues.append(
                    f"{p.name}: exhibit material outside the exhibit wrappers ({sm[:40]}) — table and figure "
                    f"content is input from sections/tables.tex / sections/figures.tex inside a float with its caption and label")
    return issues


def _exhibit_material(text: str):
    """The first piece of exhibit material in `text`: an `\\input`/`\\include`
    whose NORMALIZED target lies under tables/ or figures/ (`./tables/x`,
    `tables/x.tex`), an `\\includegraphics`, a bare tabular/tabularx/longtable,
    or a tikzpicture; None when there is none."""
    for im in re.finditer(r'\\(?:input|include)\s*\{\s*([^}]+?)\s*\}', text):
        if _norm_input(im.group(1)).startswith(("tables/", "figures/")):
            return im.group(0)
    sm = re.search(r'\\includegraphics\b|\\begin\s*\{(?:tabular\*?|tabularx|longtable|tikzpicture)\}', text)
    return sm.group(0) if sm else None


def check_section_file(filepath: Path, section_type: str) -> list[str]:
    """Check tables.tex or figures.tex for proper formatting."""
    issues = []
    if not filepath.exists():
        return issues

    content = filepath.read_text()

    # Exhibit material lives INSIDE a float: an \\input / \\includegraphics /
    # tabular / tikzpicture outside every recognized float environment is
    # typeset but belongs to no exhibit — no caption, no label, nothing the
    # narrative trim gate can allocate. Comment-stripped; floats masked out.
    _env = _EXHIBIT_ENV_RE["table" if section_type == "tables" else "figure"]
    _outside = _env.sub(lambda m: " " * len(m.group(0)), _strip_tex_comments(content))
    _stray = re.search(r'\\(?:input|include|includegraphics)\s*\*?\s*(?:\[[^\]]*\])?\s*\{'
                       r'|\\begin\s*\{(?:tabular\*?|tabularx|longtable|tikzpicture)\}', _outside)
    if _stray:
        issues.append(
            f"{filepath.name}: exhibit material outside a float ({_stray.group(0).strip()}) — "
            f"every \\input / \\includegraphics / tabular in a wrapper sits inside a "
            f"\\begin{{{'table' if section_type == 'tables' else 'figure'}}} float with its caption and label")

    if section_type == "tables":
        # Check for booktabs commands in referenced files or this file
        if '\\hline' in content and '\\toprule' not in content:
            issues.append(f"{filepath.name}: Use booktabs (\\toprule/\\midrule/\\bottomrule) instead of \\hline")

        # Walk consecutive \begin{table} floats and require \clearpage between
        # TITLED tables — a float carrying \caption{...} (optional [short]
        # form included; comment-stripped so a commented-out caption does not
        # count). A float without a titled caption is a body/continuation
        # float: the canonical two-table pattern in assets/tables_template.tex
        # puts the title + footnotesize notes in a caption-only float, then a
        # second float carrying the tabular body on the same page — with
        # \caption*{} / \caption*{Panel ...} or (landscape / single-panel
        # tables) no caption at all. Counting \begin{table} instead of titled
        # captions mis-read every caption-less body float as a second table.
        body = _strip_tex_comments(content)
        # the ONE tokenizer (table, table*, sidewaystable, spaced \begin)
        titled_seen = 0
        prev_titled_pos = None
        for i, m in enumerate(_TABLE_ENV_RE.finditer(body)):
            pos, this_table = m.start(), m.group(0)
            if not has_titled_caption(this_table):
                continue
            titled_seen += 1
            if prev_titled_pos is not None and \
                    '\\clearpage' not in body[prev_titled_pos:pos]:
                issues.append(f"{filepath.name}: Missing \\clearpage between tables "
                              f"(titled table {titled_seen}, float {i+1})")
            prev_titled_pos = pos

    elif section_type == "figures":
        # Check for clearpage between figures (comment-stripped: a commented
        # figure is not a figure)
        body = _strip_tex_comments(content)
        fig_starts = [m.start() for m in _FIGURE_ENV_RE.finditer(body)]
        for i, pos in enumerate(fig_starts):
            if i > 0:
                between = body[fig_starts[i-1]:pos]
                if '\\clearpage' not in between:
                    issues.append(f"{filepath.name}: Missing \\clearpage between figures (figure {i+1})")

        # Check for self-contained descriptions. Accept either the manual
        # {\footnotesize\justifying...} block or the \notes{} macro (defined in
        # style.tex), which expands to the same idiom — mirroring the
        # \notes-awareness of check_notes_justified below.
        figs = [m.group(0) for m in _FIGURE_ENV_RE.finditer(body)]
        for i, fig in enumerate(figs):
            if '\\footnotesize' not in fig and not re.search(r'\\notes\s*\{', fig):
                issues.append(
                    f"{filepath.name}: Figure {i+1} missing self-contained description "
                    f"(use the \\notes{{}} macro or a {{\\footnotesize\\justifying...}} block)"
                )

    return issues


def check_content_file_purity(tables_dir: Path) -> list[str]:
    """Check that table content files are PURE tabular (no wrappers).

    Two-level table architecture:
      Level 1 (tables/*.tex): PURE \\begin{tabular}...\\end{tabular} with booktabs.
      Level 2 (sections/tables.tex): wrappers with \\caption, \\label, \\footnotesize.
    Content files must NEVER contain \\begin{table}, \\caption, \\label,
    \\footnotesize, \\footnote, \\textit{Notes:}, or \\begin{minipage}.
    """
    issues = []
    if not tables_dir.exists():
        return issues

    forbidden_patterns = [
        (r'\\begin\{table\*?\}', '\\begin{table}'),
        (r'\\caption\{', '\\caption{}'),
        (r'\\caption\*\{', '\\caption*{}'),
        (r'\\label\{', '\\label{}'),
        (r'\\footnotesize', '\\footnotesize'),
        (r'\\footnote\{', '\\footnote{}'),
        (r'\\textit\{Notes', '\\textit{Notes:}'),
        (r'\\begin\{minipage\}', '\\begin{minipage}'),
        (r'\\begin\{tablenotes\}', '\\begin{tablenotes}'),
    ]

    for tex_file in sorted(tables_dir.glob("*.tex")):
        content = tex_file.read_text()
        for pattern, desc in forbidden_patterns:
            if re.search(pattern, content):
                issues.append(
                    f"tables/{tex_file.name}: Contains {desc} — content files must be "
                    f"PURE tabular only (two-level architecture violation)"
                )
    return issues


_IA_OPT_OUT_RE = re.compile(r'(?m)^\s*%+\s*no-internet-appendix\b')
# \clearpage (not \newpage) immediately before the IA \input in main.tex:
# \clearpage FLUSHES held-over floats, so the header is the first typeset
# object on the IA's opening page.
_MAIN_IA_CLEARPAGE_RE = re.compile(
    r'\\clearpage\s*(?:\\appendix\s*)?\\(?:input|include)\s*\{\s*sections/appendix(?:\.tex)?\s*\}'
)


def check_internet_appendix(filepath: Path, main_content: str = "") -> list[str]:
    """Check the Internet Appendix opens a fresh page.

    The IA title header itself — wording AND presence — is TEMPLATE-CARRIED
    and NOT validated here (user decision 2026-08-14, extending the
    admission rule of 2026-08-11): assets/appendix_template.tex ships the
    canonical `Internet Appendix for ``\\Title''` header, "Internet
    Appendix" is the standard wording whenever the pipeline's template is
    used, and re-checking the header name invites false blocks on
    legitimate typography. The authoritative header consumer is the
    compiled-page scan (shared_patterns.INTERNET_APPENDIX_HEADER_RE) at
    pre-submission, where a deleted or mangled header surfaces loudly as an
    over-cap page count — never silently.

    What IS still checked is the fresh-page property, because it sits on an
    actively-edited surface: the scaffold ships the IA wired (manuscript and
    IA compile to ONE pdf), a project that reorders its back matter re-adds
    the wiring by hand, and dropping the \\clearpage there is a natural slip.
    Use \\clearpage, NOT \\newpage — \\clearpage flushes held-over floats so
    the header is the first typeset object on the IA's opening page, which
    is what the page-limit scan keys on.

    Enforcement is skipped on an explicit opt-out (`% no-internet-appendix`
    marker) or when the fragment is not wired into main.tex (inert — a
    project that has commented the wiring out).

    Detection is COMMENT-STRIPPED on both sides: a project that keeps the
    wiring as `% \\input{sections/appendix}` must not be misclassified as
    wired.
    """
    issues = []
    if not filepath.exists():
        return issues

    raw = filepath.read_text()
    # The opt-out marker IS a TeX comment -> scan the RAW text for it.
    if _IA_OPT_OUT_RE.search(raw):
        return issues

    content = _strip_tex_comments(raw)
    main_stripped = _strip_tex_comments(main_content)

    is_wired = _scan_main_text(main_content, root=filepath.parent.parent)["appendix_wired"]
    if not is_wired:
        return issues  # inert fragment — nothing reaches the compiled paper

    if (not _MAIN_IA_CLEARPAGE_RE.search(main_stripped)
            and not re.match(r'\s*\\clearpage\b', content)):
        issues.append(
            "sections/appendix.tex: the Internet Appendix must open a fresh "
            "page — put \\clearpage before \\input{sections/appendix} in main.tex "
            "(or at the top of the fragment). Use \\clearpage, NOT \\newpage: "
            "\\clearpage flushes held-over floats so the IA header is the first "
            "thing on the page, which is what the page-limit scan looks for."
        )

    return issues


def _note_suppresses_indent(block: str) -> bool:
    """True if a note block kills the first-line paragraph indent — via
    \\noindent, or by zeroing \\parindent (\\setlength{\\parindent}{0...} /
    \\parindent=0... / \\parindent\\z@). Zeroing \\parindent is preferred
    because it also kills the re-indent that follows a display equation in
    the note; \\noindent only fixes the first line."""
    if '\\noindent' in block:
        return True
    if re.search(r'\\setlength\s*\{\s*\\parindent\s*\}\s*\{\s*(?:0|\\z@)', block):
        return True
    if re.search(r'\\parindent\s*=?\s*(?:0|\\z@)', block):
        return True
    return False


def check_notes_justified(filepath: Path) -> list[str]:
    """Table/figure notes paragraphs must be justified AND flush-left — same
    idiom for both.

    Three failure modes are flagged for any \\begin{table}/\\begin{figure}
    float that carries a manual {\\footnotesize ...} notes paragraph:

    1. **No \\justifying inside a \\centering float.** The \\centering declaration
       raggs every paragraph in the float, including the notes, so they render
       NOT aligned to both margins. Fix: \\justifying (ragged2e) on the notes.

    2. **Misplaced idiom `\\footnotesize{\\justifying ...}`** (any float). Here
       \\justifying sits in a transient inner group that closes before the
       paragraph breaks, so its line-breaking parameters are reverted and the
       notes do NOT justify. This is the asymmetry that left figures ragged
       while tables (which use `{\\footnotesize\\justifying ...}`) justified.

    3. **No indent suppression on a justified note.** The note paragraph
       inherits the default \\parindent, so its first line (and any line after
       a display equation) is indented. Fix: \\setlength{\\parindent}{0pt}
       (scoped to the note group) or \\noindent.

    Canonical form for BOTH tables and figures: keep \\footnotesize, \\justifying,
    and the indent reset in the SAME group as the text —
    `{\\footnotesize\\justifying\\setlength{\\parindent}{0pt} ...}` — or use the
    \\notes{} macro. Floats whose notes use \\notes{} (no literal \\footnotesize)
    inherit the macro's full idiom and are not flagged.
    """
    issues = []
    if not filepath.exists():
        return issues
    content = filepath.read_text()
    for m in re.finditer(r'\\begin\{(table|figure)\}.*?\\end\{\1\}', content, re.DOTALL):
        block = m.group(0)
        kind = m.group(1)
        if '\\footnotesize' not in block:
            continue  # uses \notes{} macro or has no manual notes paragraph
        # Mode 2: misplaced idiom — wrong regardless of \centering.
        if re.search(r'\\footnotesize\s*\{\s*\\justifying', block):
            issues.append(
                f"{filepath.name}: a {kind} notes block uses the misplaced "
                f"`\\footnotesize{{\\justifying ...}}` idiom — \\justifying sits in "
                f"an inner group that closes before the paragraph breaks, so the "
                f"notes will not justify. Use `{{\\footnotesize\\justifying ...}}` "
                f"(both in the same group as the text) or the \\notes{{}} macro."
            )
            continue
        # Mode 1: \centering float whose notes lack \justifying entirely.
        if '\\justifying' not in block:
            if '\\centering' in block:
                issues.append(
                    f"{filepath.name}: a {kind} notes block inside \\centering is not "
                    f"justified — its {{\\footnotesize ...}} notes will render centered/"
                    f"ragged, not aligned to both margins. Add \\justifying (needs "
                    f"\\usepackage{{ragged2e}}) to the notes, or use the \\notes{{}} macro."
                )
            continue
        # Mode 3: properly justified note, but the first line still indents.
        if not _note_suppresses_indent(block):
            issues.append(
                f"{filepath.name}: a {kind} notes block is justified but its first "
                f"line will indent (default \\parindent). Add \\setlength{{\\parindent}}"
                f"{{0pt}} (scoped to the note group, preferred) or \\noindent — e.g. "
                f"`{{\\footnotesize\\justifying\\setlength{{\\parindent}}{{0pt}} ...}}` "
                f"— or use the \\notes{{}} macro."
            )
    return issues


# TeX comment stripping, PARITY-aware: a `%` behind an ODD number of
# backslashes is an escaped percent sign; behind an EVEN number (`\\%` =
# line break + comment) it starts a comment. The naive `(?<!\\)%` form kept
# a commented-out `\end{table}` after `\\%` and truncated the float. The ONE
# stripper — the GAN hook and round-end layers import it from here.
_TEX_COMMENT_RE = re.compile(r'(?<!\\)((?:\\\\)*)%.*')


def strip_tex_comments(text: str) -> str:
    return "\n".join(_TEX_COMMENT_RE.sub(r'\1', ln) for ln in text.splitlines())


def _strip_tex_comments(text: str) -> str:
    return strip_tex_comments(text)


# Two-float exhibit contract (see assets/tables_template.tex): the TITLED float
# carries \caption{Title} + the notes block and NO body; the BODY float carries
# \caption*{...} + the tabular/\input and NO titled caption. A single
# \begin{table} float combining a titled \caption{} with tabular/\input content
# is the collapsed Title->Table->Description antipattern (see
# scripts/build_table_wrapper.py, which emits the correct form).
# NOTE: the GAN plugin's edit-time hook (plugins/gan/hooks/check_table_format.py)
# mirrors these patterns via its shared_patterns helpers; a cross-fixture test in
# the plugin's round_end_checks.py --test pins the two implementations together.
# The ONE exhibit tokenizer / caption scanner (the GAN plugin's edit-time hook
# and round-end warn layer import these from here — no second copy anywhere).
_TABLE_ENV_RE = re.compile(
    r'\\begin\s*\{(table\*?|sidewaystable\*?)\}.*?\\end\s*\{\1\}', re.DOTALL)
_FIGURE_ENV_RE = re.compile(
    r'\\begin\s*\{(figure\*?|sidewaysfigure\*?)\}.*?\\end\s*\{\1\}', re.DOTALL)
_EXHIBIT_ENV_RE = {"table": _TABLE_ENV_RE, "figure": _FIGURE_ENV_RE}
_CAPTION_CMD_RE = re.compile(r'\\caption(?![*A-Za-z@])')
_TABLE_BODY_RE = re.compile(r'\\begin\s*\{(?:tabular\*?|tabularx|longtable)\}|\\input\s*\{')


def iter_table_floats(text: str):
    """Complete table floats in order — `table`, `table*`, `sidewaystable(*)`,
    whitespace before the brace allowed (`\\begin {table}`)."""
    return (m.group(0) for m in _TABLE_ENV_RE.finditer(text))


def has_titled_caption(tok: str) -> bool:
    """`\\caption{...}` / `\\caption[short]{...}` present in a float — NOT
    `\\caption*` (panel floats) and not `\\captionsetup`. The optional argument
    is scanned as LaTeX reads it: braces balance and the FIRST `]` outside a
    brace group ends it (square brackets do not nest), so a short title such
    as `[Results for {$x_{[t]}$}]` or `[Results [robust]` is one argument and
    the mandatory `{` that follows is still found. A regex stopping at the
    first `]` let a collapsed float with a brace-nested bracket escape."""
    n = len(tok)
    for m in _CAPTION_CMD_RE.finditer(tok):
        i = m.end()
        while i < n and tok[i].isspace():
            i += 1
        if i < n and tok[i] == '[':
            i += 1
            braces = 0
            while i < n:
                c = tok[i]
                if c == '\\':
                    i += 2
                    continue
                if c == '{':
                    braces += 1
                elif c == '}':
                    braces = max(0, braces - 1)
                elif c == ']' and braces == 0:
                    i += 1
                    break
                i += 1
            while i < n and tok[i].isspace():
                i += 1
        if i < n and tok[i] == '{':
            return True
    return False


def collapsed_table_floats(text: str) -> list[int]:
    """1-based indices of complete table floats that collapse a TITLED
    caption together with tabular/\\input body content — the two-float
    contract violation. `text` must already be comment-stripped."""
    out: list[int] = []
    for i, blk in enumerate(iter_table_floats(text), 1):
        if has_titled_caption(blk) and _TABLE_BODY_RE.search(blk):
            out.append(i)
    return out


def check_no_collapsed_floats(filepath: Path) -> list[str]:
    """Two-float contract for wrapper files (sections/tables.tex,
    sections/figures.tex, sections/appendix.tex).

    Tables: a \\begin{table} float may carry EITHER the titled \\caption{} +
    notes OR the \\caption*{} + body content — never both (collapsed
    single-float). Figures: \\caption must precede the image content
    (\\includegraphics / tikzpicture) — canonical order is
    caption -> notes -> image."""
    issues = []
    if not filepath.exists():
        return issues
    content = _strip_tex_comments(filepath.read_text())

    # \caption*{...} (body/panel floats) is allowed alongside content; only
    # a TITLED \caption{} / \caption[..]{..} plus body content collapses.
    for i in collapsed_table_floats(content):
        issues.append(
            f"{filepath.name}: table float {i} collapses \\caption{{}} and "
            f"tabular/\\input into ONE \\begin{{table}} — use the two-float "
            f"pattern (titled caption + notes float, then \\caption*{{}} body "
            f"float; scripts/build_table_wrapper.py emits it)"
        )

    for i, m in enumerate(_FIGURE_ENV_RE.finditer(content), 1):
        blk = m.group(0)
        cap = blk.find('\\caption')
        img_positions = [p for p in (blk.find('\\includegraphics'),
                                     blk.find('\\begin{tikzpicture}')) if p != -1]
        img = min(img_positions) if img_positions else -1
        if img != -1 and (cap == -1 or img < cap):
            issues.append(
                f"{filepath.name}: figure {i} places its image before \\caption — "
                f"order must be caption -> notes -> image"
            )
    return issues


_INPUT_GRAPHICS_RE = re.compile(
    r'\\(input|includegraphics)\s*\*?\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}'
)
_GRAPHICSPATH_RE = re.compile(r'\\graphicspath\s*\{((?:\{[^{}]*\}|[^{}])*)\}')


def check_path_self_containment(main_tex: Path) -> list[str]:
    """Self-contained paper root: no \\input/\\includegraphics/\\graphicspath
    target may contain '../' or be absolute — the paper must build from a
    copied/zipped directory (journal/arXiv submission drops everything
    outside it). Exhibits live in the LOCAL tables/ and figures/ dirs; in GAN
    projects those are a compile-time mirror of output/ (the single
    script-write home), refreshed by compile_with_provenance.py — never
    reference ../output/ from the draft."""
    issues = []
    project_dir = main_tex.parent
    files = [main_tex] + sorted((project_dir / 'sections').glob('*.tex'))

    def flag(fname: str, cmd: str, target: str) -> None:
        issues.append(
            f"{fname}: \\{cmd}{{{target}}} escapes the paper root — the draft "
            f"must be self-contained (reference LOCAL tables/ and figures/ "
            f"copies; never '../' or absolute paths)"
        )

    for f in files:
        if not f.exists():
            continue
        content = _strip_tex_comments(f.read_text())
        for m in _INPUT_GRAPHICS_RE.finditer(content):
            target = m.group(2).strip()
            if '../' in target or target.startswith('/'):
                flag(f.name, m.group(1), target)
        for m in _GRAPHICSPATH_RE.finditer(content):
            entries = re.findall(r'\{([^}]*)\}', m.group(1)) or [m.group(1)]
            for entry in entries:
                entry = entry.strip()
                if '../' in entry or entry.startswith('/'):
                    flag(f.name, 'graphicspath', entry)
    return issues


def _always_on_citation_issues(main_tex: Path) -> list[str]:
    """journal_format's always-on CITATION checks — a key repeated inside one
    citation command (the natbib year-collapse trigger) and the collapse in
    the compile log / rendered PDF when a compile sits beside main.tex — run
    on every draft, journal or not: one engine, no journal facts."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_validate_latex_journal_format", Path(__file__).resolve().parent / "journal_format.py")
    jf = sys.modules.get(spec.name)
    if jf is None:
        jf = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = jf     # dataclasses resolve their module through sys.modules
        spec.loader.exec_module(jf)
    out = []
    for v in jf.check_facts(main_tex, {}):
        if not v.rule.startswith("citation."):
            continue
        loc = f"{v.file}:{v.line}" if v.line else v.file
        line = f"[{v.rule}] {loc}: {v.message}"
        out.append(line if v.severity == "block" else f"WARNING: {line}")
    return out


def validate(main_tex: Path) -> list[str]:
    """Run every validation check: the drafting STRUCTURE (author macros,
    abstract single-source, section inputs, two-level exhibits, the admitted-
    main grammar, path self-containment) and the ONE working-paper LAYOUT
    every draft keeps (12pt, a4paper, the 1.5in/1in geometry,
    \\onehalfspacing) — a journal's format is applied only on acceptance by
    journal_format.py and is never checked here (user directive 2026-09-21).
    The `article` class is drafting structure."""
    all_issues = []

    if not main_tex.exists():
        return [f"File not found: {main_tex}"]

    content = main_tex.read_text()
    project_dir = main_tex.parent

    # Read style.tex for the geometry check — ONLY when main.tex actually
    # imports it (comment-stripped). Without this guard an unused style.tex
    # on disk would satisfy the geometry check while the real document uses
    # different inline settings. The inverse drift — style.tex present but
    # its import commented out/removed — silently disables EVERY
    # style-carried setting (geometry, bib style, exhibit numbering, the
    # \notes macro), so it is flagged loudly instead of skipping quietly.
    style_tex = project_dir / "style.tex"
    style_imported = bool(re.search(
        r'\\input\s*\{\s*style(?:\.tex)?\s*\}', _strip_tex_comments(content)))
    if style_tex.exists() and not style_imported:
        all_issues.append(
            "style.tex exists but main.tex does not \\input{style} (live, "
            "uncommented) — the style file (geometry, bibliography style, "
            "exhibit numbering, \\notes) is inert. Restore \\input{style} "
            "after \\documentclass."
        )
    style_content = (style_tex.read_text()
                     if style_tex.exists() and style_imported else "")

    # Layout: the working-paper format the three layout checks carry in
    # their signatures; the grammar's own issues (a spacing switch inside the
    # body) ride with the spacing check.
    manuscript = scan_manuscript(main_tex)
    all_issues.extend(check_document_class(content))
    all_issues.extend(check_line_spacing(manuscript))
    all_issues.extend(check_geometry(style_content, main_content=content))
    all_issues.extend(_always_on_citation_issues(main_tex))
    all_issues.extend(check_author_format(content))
    all_issues.extend(check_abstract(content, project_dir))
    all_issues.extend(check_main_section_inputs(content))

    # Section file checks
    tables_file = project_dir / "sections" / "tables.tex"
    figures_file = project_dir / "sections" / "figures.tex"
    appendix_file = project_dir / "sections" / "appendix.tex"
    tables_dir = project_dir / "tables"

    all_issues.extend(check_section_file(tables_file, "tables"))
    all_issues.extend(check_section_file(figures_file, "figures"))
    all_issues.extend(check_internet_appendix(appendix_file, content))
    all_issues.extend(check_floats_in_wrappers_only(manuscript))

    # Two-level architecture: content files must be pure tabular
    all_issues.extend(check_content_file_purity(tables_dir))

    # Notes blocks inside \centering floats must be \justifying (both-margin alignment)
    all_issues.extend(check_notes_justified(tables_file))
    all_issues.extend(check_notes_justified(figures_file))
    all_issues.extend(check_notes_justified(appendix_file))

    # Two-float wrapper contract: no collapsed caption+content floats; figures
    # keep caption -> notes -> image order
    all_issues.extend(check_no_collapsed_floats(tables_file))
    all_issues.extend(check_no_collapsed_floats(figures_file))
    all_issues.extend(check_no_collapsed_floats(appendix_file))

    # Path self-containment: no ../ or absolute \input/\includegraphics/
    # \graphicspath targets anywhere in main.tex + sections/*.tex
    all_issues.extend(check_path_self_containment(main_tex))

    return all_issues


def _run_self_test() -> int:
    """Synthetic fixture tests for the structural checks. Returns 0 on pass."""
    import tempfile

    failures: list[str] = []
    # the ONE caption scanner reads the optional argument as LaTeX does:
    # a brace-nested `]` does not end it, so a collapsed float with such a
    # short caption is caught; table* / sidewaystable / spaced \begin count
    _collapsed = ("\\begin{table}\n\\caption[Results for {$x_{[t]}$}]{Main}\n"
                  "{\\footnotesize d}\n\\input{tables/a}\n\\end{table}\n")
    if collapsed_table_floats(_collapsed) != [1]:
        failures.append("collapsed float with a brace-nested ] in the short caption escaped")
    if collapsed_table_floats("\\begin{table*}\\caption{A}\\input{tables/a}\\end{table*}") != [1]:
        failures.append("collapsed table* float escaped")
    if collapsed_table_floats("\\begin{table}[ht]\\caption{A}{\\footnotesize d}\\begin{tabular*}{\\textwidth}{lc}A & B\\\\\\end{tabular*}\\end{table}") != [1]:
        failures.append("collapsed float with a tabular* body escaped")
    if collapsed_table_floats("\\begin {sidewaystable}\\caption{A}\\begin{tabular}{l}x\\end{tabular}\\end {sidewaystable}") != [1]:
        failures.append("collapsed spaced sidewaystable float escaped")
    if collapsed_table_floats("\\begin{table}\\caption{A}{\\footnotesize d}\\end{table}\n"
                              "\\begin{table}\\caption*{P}\\input{tables/a}\\end{table}"):
        failures.append("canonical two-float exhibit flagged as collapsed")
    if has_titled_caption("\\caption[Results [robust]{A}") is not True \
            or has_titled_caption("\\caption*{P}") or has_titled_caption("\\captionsetup{font=small}"):
        failures.append("titled-caption scanner wrong on unbraced [ / starred / captionsetup")
    # parity-aware stripping: `\\\\%` is a line break followed by a comment
    _par = ("\\begin{table}\n\\mbox{}\\\\% \\end{table}\n\\caption{A}\n{\\footnotesize d}\n"
            "\\begin{tabular}{l}x\\\\\\end{tabular}\n\\end{table}\n")
    if collapsed_table_floats(strip_tex_comments(_par)) != [1]:
        failures.append("comment after \\\\ not stripped: collapsed float escaped")
    if strip_tex_comments("50\\% of firms") != "50\\% of firms":
        failures.append("escaped percent sign stripped as a comment")
    # two table* exhibits without \\clearpage between them are caught by the
    # tokenizer-based clear-page check
    import tempfile as _t2
    with _t2.TemporaryDirectory() as _d2:
        _f2 = Path(_d2) / "tables.tex"
        _f2.write_text("\\begin{table*}\\caption{A}\\notes{d}\\end{table*}\n"
                       "\\begin{table*}\\caption*{}\\input{tables/a}\\end{table*}\n"
                       "\\begin{table*}\\caption{B}\\notes{d}\\end{table*}\n"
                       "\\begin{table*}\\caption*{}\\input{tables/b}\\end{table*}\n")
        if not any("clearpage" in i for i in check_section_file(_f2, "tables")):
            failures.append("two table* exhibits without \\clearpage not reported")

    TWO_FLOAT_OK = r"""
\clearpage
\begin{table}[htp!]
\caption{Alpha Results}
\label{tab:alpha}
{\footnotesize\justifying\setlength{\parindent}{0pt}
This table presents the alpha regression results. $^{*}p<.1$.}
\end{table}
\vspace{-1.5cm}
\begin{table}[ht!]\centering \caption*{}
    \input{tables/alpha_results}
\end{table}
"""
    COLLAPSED = r"""
\clearpage
\begin{table}[htp!]
\caption{Alpha Results}
\label{tab:alpha}
\begin{tabular}{lc}\toprule x & 1 \\ \bottomrule\end{tabular}
{\footnotesize Notes below the table.}
\end{table}
"""
    FIG_OK = r"""
\clearpage
\begin{figure}[htpb]
\caption{Trend} \label{fig:trend}
\notes{This figure presents the trend in the outcome variable.}
\begin{center}
    \includegraphics[width=.8\textwidth]{figures/trend_plot.pdf}
\end{center}
\end{figure}
"""
    FIG_IMG_FIRST = r"""
\clearpage
\begin{figure}[htpb]
\begin{center}
    \includegraphics[width=.8\textwidth]{figures/trend_plot.pdf}
\end{center}
\caption{Trend} \label{fig:trend}
\end{figure}
"""
    LANDSCAPE_PAIR_OK = r"""
\clearpage
\begin{landscape}
\begin{table}[htp!]
\caption{Wide Results}
\label{tab:wide}
{\footnotesize\justifying\setlength{\parindent}{0pt}
This table presents the wide regression results.}
\end{table}
\begin{table}[ht!]\centering
  \resizebox{\linewidth}{!}{\input{tables/wide_results}}
\end{table}
\end{landscape}
"""
    TWO_TITLED_NO_CLEARPAGE = r"""
\clearpage
\begin{table}[htp!]
\caption{Alpha Results}
{\footnotesize\justifying Notes.}
\end{table}
\begin{table}[htp!]
\caption{Beta Results}
{\footnotesize\justifying Notes.}
\end{table}
"""

    with tempfile.TemporaryDirectory(prefix="vlx_") as td:
        root = Path(td)
        (root / "sections").mkdir()

        # F1: canonical two-float pair -> clean
        p = root / "sections" / "tables.tex"
        p.write_text(TWO_FLOAT_OK)
        if check_no_collapsed_floats(p):
            failures.append(f"F1: two-float pair flagged: {check_no_collapsed_floats(p)}")

        # F2: collapsed float -> flagged
        p.write_text(COLLAPSED)
        if not check_no_collapsed_floats(p):
            failures.append("F2: collapsed float not flagged")

        # F2b: commented-out collapsed float -> clean
        p.write_text("\n".join("% " + ln for ln in COLLAPSED.splitlines()))
        if check_no_collapsed_floats(p):
            failures.append("F2b: commented-out collapsed float flagged")

        # F3: figure caption->notes->image ok; image-before-caption flagged
        q = root / "sections" / "figures.tex"
        q.write_text(FIG_OK)
        if check_no_collapsed_floats(q):
            failures.append("F3a: caption-first figure flagged")
        q.write_text(FIG_IMG_FIRST)
        if not check_no_collapsed_floats(q):
            failures.append("F3b: image-before-caption figure not flagged")

        # F4: \notes{} figure passes the description check (row: the literal
        # \footnotesize grep false-positived on the skill's own macro)
        q.write_text(FIG_OK)
        if check_section_file(q, "figures"):
            failures.append(f"F4a: \\notes{{}} figure flagged: {check_section_file(q, 'figures')}")
        q.write_text(FIG_IMG_FIRST)  # no notes at all
        if not check_section_file(q, "figures"):
            failures.append("F4b: description-less figure not flagged")

        # F4c: clearpage-between-tables counts TITLED floats. A caption-less
        # body float (landscape / single-panel layout) on the same page as
        # its caption float is one exhibit; two titled tables without a
        # \clearpage between them are two.
        p.write_text(LANDSCAPE_PAIR_OK)
        cp = [x for x in check_section_file(p, "tables") if "clearpage" in x]
        if cp:
            failures.append(f"F4c: caption-less body float flagged as a second table: {cp}")
        p.write_text(TWO_TITLED_NO_CLEARPAGE)
        cp = [x for x in check_section_file(p, "tables") if "clearpage" in x]
        if not cp:
            failures.append("F4d: two titled tables without \\clearpage not flagged")
        # F4e: \caption[Short]{Long} is a titled caption; a commented-out
        # \caption{} inside a body float is not.
        p.write_text(TWO_TITLED_NO_CLEARPAGE.replace("\\caption{Beta Results}",
                                                     "\\caption[Beta]{Beta Results}"))
        cp = [x for x in check_section_file(p, "tables") if "clearpage" in x]
        if not cp:
            failures.append("F4e: optional-arg titled caption not counted as a table")
        p.write_text(LANDSCAPE_PAIR_OK.replace("\\begin{table}[ht!]\\centering",
                                               "\\begin{table}[ht!]\\centering % \\caption{obsolete}"))
        cp = [x for x in check_section_file(p, "tables") if "clearpage" in x]
        if cp:
            failures.append(f"F4f: commented-out caption made a body float titled: {cp}")
        # F4g: a caption-less body float BEFORE the first titled table is not
        # a predecessor exhibit — no \clearpage is owed to it.
        p.write_text("\\begin{table}[ht!]\\centering\n\\input{tables/lead}\n\\end{table}\n"
                     "\\begin{table}[htp!]\n\\caption{Alpha Results}\n"
                     "{\\footnotesize\\justifying Notes.}\n\\end{table}\n")
        cp = [x for x in check_section_file(p, "tables") if "clearpage" in x]
        if cp:
            failures.append(f"F4g: leading body float owed a clearpage: {cp}")

        # F5: path self-containment
        main_tex = root / "main.tex"
        main_tex.write_text(r"\input{style}" "\n" r"\input{sections/tables}" "\n")
        (root / "sections" / "tables.tex").write_text(TWO_FLOAT_OK)
        (root / "sections" / "figures.tex").write_text(FIG_OK)
        if check_path_self_containment(main_tex):
            failures.append(f"F5a: local paths flagged: {check_path_self_containment(main_tex)}")
        (root / "sections" / "tables.tex").write_text(
            TWO_FLOAT_OK.replace(r"\input{tables/alpha_results}",
                                 r"\input{../output/tables/alpha_results}")
        )
        if not any("../output/tables/alpha_results" in i
                   for i in check_path_self_containment(main_tex)):
            failures.append("F5b: ../-escape \\input not flagged")
        (root / "sections" / "tables.tex").write_text(TWO_FLOAT_OK)
        (root / "sections" / "figures.tex").write_text(
            r"\graphicspath{{figures/}{../output/figures/}}" + FIG_OK
        )
        if not any("../output/figures/" in i
                   for i in check_path_self_containment(main_tex)):
            failures.append("F5c: ../-escape \\graphicspath entry not flagged")
        (root / "sections" / "figures.tex").write_text(
            FIG_OK.replace("{figures/trend_plot.pdf}", "{/somewhere/abs/trend_plot.pdf}")
        )
        if not any("/somewhere/abs/trend_plot.pdf" in i
                   for i in check_path_self_containment(main_tex)):
            failures.append("F5d: absolute \\includegraphics path not flagged")
        (root / "sections" / "figures.tex").write_text(
            "% \\input{../output/tables/alpha_results} commented out\n" + FIG_OK
        )
        if check_path_self_containment(main_tex):
            failures.append("F5e: commented-out ../-escape flagged")

        # F8: a commented-out section input is not live.
        live_inputs = "\n".join(
            f"\\input{{sections/{s}}}" for s in
            ("introduction", "data", "methodology", "results",
             "robustness", "conclusion")
        )
        if check_main_section_inputs(live_inputs):
            failures.append("F8a: live section chain flagged")
        commented = live_inputs.replace("\\input{sections/data}",
                                        "% \\input{sections/data}")
        if not any("data" in i and i.startswith("WARNING")
                   for i in check_main_section_inputs(commented)):
            failures.append("F8b: commented-out section input counted as live")
        # F8c: missing standard sections WARN (advisory, standard-name
        # steer) — a lean architecture must yield only WARNING-prefixed
        # entries, never a blocking issue.
        lean = "\n".join(
            f"\\input{{sections/{s}}}" for s in
            ("introduction", "data", "results", "conclusion")
        )
        partial = check_main_section_inputs(lean)
        if not (len(partial) == 1 and partial[0].startswith("WARNING")
                and "methodology" in partial[0] and "robustness" in partial[0]):
            failures.append("F8c: lean architecture must yield exactly ONE "
                            "warning naming every missing standard section")
        # F8d: sections that ARE present still participate in the (blocking)
        # order check.
        disordered = "\n".join(
            f"\\input{{sections/{s}}}" for s in
            ("introduction", "methodology", "data", "results", "conclusion")
        )
        if not any("order" in i and not i.startswith("WARNING")
                   for i in check_main_section_inputs(disordered)):
            failures.append("F8d: out-of-order present section not flagged")
        # F8d2: "model" is position-flexible — a model section after the
        # empirics (an empirical paper whose model rationalizes the
        # findings) is a legitimate order, never flagged.
        model_late = live_inputs.replace(
            "\\input{sections/data}",
            "\\input{sections/data}\n\\input{sections/model}")
        if any("order" in i and not i.startswith("WARNING")
               for i in check_main_section_inputs(model_late)):
            failures.append("F8d2: a model section after the empirics was flagged")
        # F8e: the .tex-extension spelling is the same live input — it must
        # neither warn as missing nor bypass the blocking order check.
        ext_chain = live_inputs.replace("\\input{sections/data}",
                                        "\\input{sections/data.tex}")
        if check_main_section_inputs(ext_chain):
            failures.append("F8e: .tex-extension input flagged as missing")
        ext_disordered = disordered.replace("\\input{sections/methodology}",
                                            "\\input{sections/methodology.tex}")
        if not any("order" in i and not i.startswith("WARNING")
                   for i in check_main_section_inputs(ext_disordered)):
            failures.append("F8e2: .tex-extension input bypassed the order check")

        # F9: coauthor edits land in \newcommand{\Author}{...} — \and and a
        # second \thanks inside the macro must be caught.
        good_author = ("\\newcommand{\\Author}{Ann One and Bob Two}\n"
                       "\\author{\\Author\\thanks{Affiliations.}}\n")
        if check_author_format(good_author):
            failures.append("F9a: literal-and macro author flagged")
        bad_and = ("\\newcommand{\\Author}{Ann One \\and Bob Two}\n"
                   "\\author{\\Author\\thanks{Affiliations.}}\n")
        if not any("\\and" in i for i in check_author_format(bad_and)):
            failures.append("F9b: \\and inside \\Author macro not flagged")
        bad_thanks = ("\\newcommand{\\Author}{Ann One\\thanks{A.} and Bob Two}\n"
                      "\\author{\\Author\\thanks{B.}}\n")
        if not any("single \\thanks" in i for i in check_author_format(bad_thanks)):
            failures.append("F9c: second \\thanks inside \\Author macro not flagged")
        # F9d: MULTILINE \Author definitions are real (long thanks blocks) —
        # the balanced-brace extraction must still see \and inside them.
        multiline = ("\\newcommand{\\Author}{Ann One\n"
                     "  \\and\n"
                     "  Bob Two}\n"
                     "\\author{\\Author\\thanks{Affiliations.}}\n")
        if not any("\\and" in i for i in check_author_format(multiline)):
            failures.append("F9d: \\and in a multiline \\Author macro not flagged")
        # F9e/F9f: only LIVE declarations count — a commented bad draft line
        # must not flag, and a commented good line must not mask a live bad one.
        commented_bad = ("% \\newcommand{\\Author}{Ann \\and Bob}\n"
                         + good_author)
        if check_author_format(commented_bad):
            failures.append("F9e: commented-out bad \\Author draft falsely flagged")
        commented_good = ("% " + good_author.splitlines()[0] + "\n" + bad_and)
        if not any("\\and" in i for i in check_author_format(commented_good)):
            failures.append("F9f: commented good \\Author masked a live \\and")

    # F6: the pristine scaffold assembled from this skill's own assets passes
    # validate() end-to-end (templates and validator must never drift apart).
    assets = Path(__file__).resolve().parent.parent / "assets"
    if (assets / "paper_template.tex").exists():
        with tempfile.TemporaryDirectory(prefix="vlx_scaffold_") as td:
            root = Path(td)
            (root / "sections").mkdir()
            (root / "tables").mkdir()
            (root / "figures").mkdir()
            shutil_copy = __import__("shutil").copy2
            shutil_copy(assets / "paper_template.tex", root / "main.tex")
            shutil_copy(assets / "style.tex", root / "style.tex")
            for sec in ("abstract", "introduction", "model", "data", "methodology",
                        "results", "robustness", "conclusion"):
                src = assets / f"section_{sec}.tex"
                if src.exists():
                    shutil_copy(src, root / "sections" / f"{sec}.tex")
            shutil_copy(assets / "tables_template.tex", root / "sections" / "tables.tex")
            shutil_copy(assets / "figures_template.tex", root / "sections" / "figures.tex")
            shutil_copy(assets / "appendix_template.tex", root / "sections" / "appendix.tex")
            (root / "tables" / "main_results.tex").write_text(
                "\\begin{tabular}{lc}\\toprule a & b \\\\ \\bottomrule\\end{tabular}\n"
            )
            issues = validate(root / "main.tex")
            if issues:
                failures.append(f"F6: pristine scaffold fails validate(): {issues}")

            # F6b: style.tex present but its import commented out — the
            # inert style file must be flagged, not silently skipped.
            pristine_main = (root / "main.tex").read_text()
            (root / "main.tex").write_text(
                pristine_main.replace("\\input{style}", "% \\input{style}")
            )
            if not any("inert" in i for i in validate(root / "main.tex")):
                failures.append("F6b: commented-out \\input{style} with a "
                                "style.tex on disk must be flagged")
            (root / "main.tex").write_text(pristine_main)

            # F7: the scaffold ships the Internet Appendix WIRED — manuscript
            # and IA compile to ONE pdf, and F6 above already pins that state
            # against the IA checks (template and validator never drift apart
            # on the IA). A project that comments the wiring out must still
            # pass, with the fragment inert.
            wiring = "\\clearpage\n\\appendix\n\\input{sections/appendix}"
            if wiring not in pristine_main:
                failures.append("F7: the scaffold must ship the IA wiring live")
            (root / "main.tex").write_text(pristine_main.replace(
                wiring, "% \\clearpage\n% \\appendix\n% \\input{sections/appendix}"))
            issues = validate(root / "main.tex")
            if issues:
                failures.append(f"F7: unwired scaffold fails validate(): {issues}")
            (root / "main.tex").write_text(pristine_main)

            # F7b: wired appendix with the \clearpage dropped from the main.tex
            # wiring (the natural hand-edit slip) must be flagged; restoring
            # either the main.tex \clearpage or a fragment-top \clearpage
            # satisfies it. The header itself is template-carried — deleting
            # it must NOT flag (header checks live in the compiled-page scan).
            main_no_cp = (root / "main.tex").read_text().replace(
                "\\clearpage\n\\appendix", "\\appendix"
            )
            frag = root / "sections" / "appendix.tex"
            frag.write_text("\\section{Extra Material}\nSome prose.\n")
            if not any("fresh" in i for i in
                       check_internet_appendix(frag, main_no_cp)):
                failures.append("F7b: wired IA without \\clearpage not flagged")
            frag.write_text("\\clearpage\n\\section{Extra Material}\nSome prose.\n")
            if check_internet_appendix(frag, main_no_cp):
                failures.append("F7b2: fragment-top \\clearpage must satisfy")
            frag.write_text("\\clearpagebreak\n\\section{Extra Material}\n")
            if not check_internet_appendix(frag, main_no_cp):
                failures.append("F7b2b: a longer command sharing the "
                                "\\clearpage prefix must NOT satisfy")
            frag.write_text("\\section{Extra Material}\nSome prose.\n")
            if check_internet_appendix(frag, (root / "main.tex").read_text()):
                failures.append("F7b3: header-less appendix must not be flagged "
                                "(header is template-carried, not validated)")

            # F7c: the explicit opt-out marker silences IA enforcement.
            (root / "sections" / "appendix.tex").write_text(
                "% no-internet-appendix\n\\section{Extra Material}\nSome prose.\n"
            )
            issues = [i for i in check_internet_appendix(
                          root / "sections" / "appendix.tex", main_no_cp)]
            if issues:
                failures.append(f"F7c: opt-out marker must silence IA checks: {issues}")
            # F8: the ONE working-paper layout is the validator's own: the
            # pristine scaffold passes; a font downgrade, a paper-size change,
            # a spacing change and a margin change each fail; {report} fails
            # the article-class structure check. No journal fact reaches the
            # validator — a journal's format is applied on acceptance by
            # journal_format.py, whose own tests pin the conversion.
            (root / "main.tex").write_text(pristine_main)
            (root / "sections" / "appendix.tex").write_text(
                (assets / "appendix_template.tex").read_text())
            if [i for i in validate(root / "main.tex") if not i.startswith("WARNING")]:
                failures.append(f"F8: the pristine scaffold must pass bare: {validate(root / 'main.tex')[:3]}")
            for _old, _new, _what in (("12pt", "11pt", "font downgrade"),
                                      ("a4paper", "letterpaper", "paper-size change"),
                                      ("\\onehalfspacing", "\\doublespacing", "spacing change")):
                if _old not in pristine_main:
                    failures.append(f"F8: the scaffold must carry {_old!r}")
                    continue
                (root / "main.tex").write_text(pristine_main.replace(_old, _new, 1))
                if not [i for i in validate(root / "main.tex") if not i.startswith("WARNING")]:
                    failures.append(f"F8: a {_what} must fail the working-paper layout")
            (root / "main.tex").write_text(pristine_main)
            _style_txt = (root / "style.tex").read_text()
            if "top=1.5in" not in _style_txt:
                failures.append("F8: the scaffold's style.tex must carry the 1.5in top margin")
            (root / "style.tex").write_text(_style_txt.replace("top=1.5in", "top=1in", 1))
            if not any("geometry" in i for i in validate(root / "main.tex")):
                failures.append("F8: a margin change must fail the working-paper geometry")
            (root / "style.tex").write_text(_style_txt)
            (root / "main.tex").write_text(pristine_main.replace("\\input{style}", "\\input{style}\n\\geometry{margin=0.5in}", 1))
            if not any("override" in i for i in validate(root / "main.tex")):
                failures.append("F8: a \\geometry override in main.tex must fail the working-paper geometry")
            _report = re.sub(r"\\documentclass(\[[^\]]*\])?\{article\}", r"\\documentclass\1{report}", pristine_main, count=1)
            (root / "main.tex").write_text(_report)
            if not any("{report}" in i and "{article}" in i for i in validate(root / "main.tex")):
                failures.append("F8: {report} must fail the article-class structure check")
            (root / "main.tex").write_text(pristine_main)
    else:
        print("SKIP F6: article assets not found; scaffold round-trip not run.")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    # exhibit material outside a float is a wrapper defect; figure* order is checked
    import tempfile as _tf_ex
    with _tf_ex.TemporaryDirectory() as _xd:
        _tw = Path(_xd) / "tables.tex"
        _tw.write_text("\\clearpage\n\\begin{table}\\caption{A}\\label{tab:a}\\notes{n}\\end{table}\n"
                       "\\begin{table}\\caption*{}\\input{tables/a}\\end{table}\n\\input{tables/offspine}\n", encoding="utf-8")
        assert any("outside a float" in i for i in check_section_file(_tw, "tables")), check_section_file(_tw, "tables")
        _tw.write_text("\\clearpage\n\\begin{table}\\caption{A}\\label{tab:a}\\notes{n}\\end{table}\n"
                       "\\begin{table}\\caption*{}\\input{tables/a}\\end{table}\n", encoding="utf-8")
        assert not any("outside a float" in i for i in check_section_file(_tw, "tables")), check_section_file(_tw, "tables")
        _tw.write_text("\\clearpage\n\\begin{table}\\caption{A}\\label{tab:a}\\notes{n}\\end{table}\n\\include{tables/offspine}\n", encoding="utf-8")
        assert any("outside a float" in i for i in check_section_file(_tw, "tables")), "\\include outside a float"
        _fw = Path(_xd) / "figures.tex"
        _fw.write_text("\\begin{figure*}\\includegraphics{figures/x.pdf}\\caption{X}\\label{fig:x}\\notes{n}\\end{figure*}\n", encoding="utf-8")
        assert any("image before" in i for i in check_no_collapsed_floats(_fw)), check_no_collapsed_floats(_fw)
        _fw.write_text("% \\begin{figure*}\\caption{old}\\end{figure*}\n\\clearpage\n\\begin{figure}\\caption{X}\\label{fig:x}\\notes{n}\\includegraphics{figures/x.pdf}\\end{figure}\n", encoding="utf-8")
        assert not check_section_file(_fw, "figures"), f"a commented-out figure is not a figure: {check_section_file(_fw, 'figures')}"
        _sd2 = Path(_xd) / "sections"; _sd2.mkdir()
        _rs = _sd2 / "results.tex"
        _rs.write_text("\\section{Results}\n\\begin{table}\\caption{Hidden}\\label{tab:hidden}\\end{table}\n", encoding="utf-8")
        assert any("float outside the exhibit wrappers" in i for i in check_floats_in_wrappers_only({"live_files": [str(_rs)], "wrappers": ["tables.tex"]})), "a float in a body section"
        _fw2 = _sd2 / "figures.tex"; _fw2.write_text(_fw.read_text(), encoding="utf-8")
        assert not check_floats_in_wrappers_only({"live_files": [str(_fw2)], "wrappers": ["figures.tex"]})
        assert check_floats_in_wrappers_only({"live_files": [str(_fw2)], "wrappers": []}), "a figures.tex nothing inputs as a wrapper is a body file"
        _mn = Path(_xd) / "main.tex"; _mn.write_text("\\begin{document}\\begin{figure}\\caption{x}\\end{figure}\\end{document}\n", encoding="utf-8")
        assert check_floats_in_wrappers_only({"live_files": [str(_mn)], "wrappers": []}), "a float in main.tex"
        for _mat in ("\\input{tables/offspine}", "\\input{./tables/offspine}", "\\include{tables/offspine}", "\\begin{tikzpicture}\\end{tikzpicture}"):
            _rs.write_text(f"\\section{{Results}}\n{_mat}\n", encoding="utf-8")
            assert any("exhibit material outside" in i for i in check_floats_in_wrappers_only({"live_files": [str(_rs)], "wrappers": ["tables.tex"]})), f"exhibit material in the prose: {_mat}"
        _ap0 = _sd2 / "appendix.tex"; _ap0.write_text("\\section{IA}\n\\input{tables/dumped}\n", encoding="utf-8")
        assert any("outside a float" in i for i in check_floats_in_wrappers_only({"live_files": [str(_ap0)], "wrappers": [], "appendix_closes": True, "ia_files": ["appendix.tex"]})), "raw material in the closing IA"
        (_sd2 / "appendix_tables.tex").write_text("\\begin{table}\\caption{IA}\\end{table}\n", encoding="utf-8")
        assert not check_floats_in_wrappers_only({"live_files": [str(_sd2 / "appendix_tables.tex")], "wrappers": [], "appendix_closes": True, "ia_files": ["appendix_tables.tex"]}), "a file only the appendix reaches shares the IA role"
        assert check_floats_in_wrappers_only({"live_files": [str(_sd2 / "appendix_tables.tex")], "wrappers": [], "appendix_closes": True, "ia_files": []}), "a file a body section reaches is main body whatever its name"
        _hid = _sd2 / "results.tex"; _hid.write_text("\\newcommand{\\hidden}{\\begin{table}\\caption{H}\\end{table}}\n\\hidden\n", encoding="utf-8")
        assert any("macro definition carries a float" in i for i in check_floats_in_wrappers_only({"live_files": [str(_hid)], "wrappers": [], "appendix_closes": False, "ia_files": []})), "a float hidden in a macro definition is refused"
        _hid.unlink()
        _tw = _sd2 / "tables.tex"; _tw.write_text("\\begin{table}\\caption{T}\\label{tab:t}\\end{table}\n\\begin{figure}\\caption{Picture}\\label{fig:hidden}\\begin{picture}(1,1)\\end{picture}\\end{figure}\n", encoding="utf-8")
        assert any("figure float in the tables wrapper" in i for i in check_floats_in_wrappers_only({"live_files": [str(_tw)], "wrappers": ["tables.tex"], "appendix_closes": False, "ia_files": []})), "a wrapper carries its own kind only"
        _tw.unlink()
        _ap = _sd2 / "appendix.tex"; _ap.write_text("\\begin{table}\\caption{IA}\\end{table}\n", encoding="utf-8")
        assert check_floats_in_wrappers_only({"live_files": [str(_ap)], "wrappers": [], "appendix_closes": False, "ia_files": []}), "an in-cap appendix is a body file"
        assert not check_floats_in_wrappers_only({"live_files": [str(_ap)], "wrappers": [], "appendix_closes": True, "ia_files": ["appendix.tex"]})
        assert "tab:" not in strip_inert_tex("\\newcommand{\\x}{\\label{tab:def}}\nbody\n\\end{document}\n\\label{tab:after}"), strip_inert_tex("\\newcommand{\\x}{\\label{tab:def}}\nbody\n\\end{document}\n\\label{tab:after}")
    # the admitted-main grammar: ONE parser behind S0 and the page cap
    import tempfile as _tf_sp
    with _tf_sp.TemporaryDirectory() as _sd:
        _d = Path(_sd); _secs = _d / "sections"; _secs.mkdir()
        (_secs / "results.tex").write_text("\\onehalfspacing text\n", encoding="utf-8")
        (_secs / "data.tex").write_text("% \\doublespacing in a comment\nclean\n", encoding="utf-8")
        (_secs / "appendix.tex").write_text("\\singlespacing IA\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\onehalfspacing\n\\begin{document}\n\\input{sections/results}\n\\end{document}\n", encoding="utf-8")
        _sc = scan_manuscript(_d / "main.tex")
        assert _sc["spacing"] == "onehalfspacing" and len(_sc["issues"]) == 1 and "results.tex" in _sc["issues"][0], _sc
        assert not check_line_spacing({"spacing": "onehalfspacing", "issues": []}), "clean scan must pass"
        assert any("accepts only" in i for i in check_line_spacing({"spacing": "doublespacing", "issues": []})), "prohibited body spacing"
        assert any("missing" in i for i in check_line_spacing({"spacing": None, "issues": []})), "missing declaration"
    for _label, _tex, _want, _bad in (
            ("template shape", "\\onehalfspacing\n\\begin{document}\n\\begin{abstract}\\input{sections/abstract}\\end{abstract}\n"
                               "\\doublespacing\n\\input{sections/introduction}\n\\input{sections/results}\n\\onehalfspace\n"
                               "\\bibliography{ref}\n\\singlespacing\n\\input{sections/tables}\n\\input{sections/figures}\n"
                               "\\clearpage\\input{sections/appendix}\n\\end{document}\n", "doublespacing", False),
            ("single before the body", "\\onehalfspacing\n\\begin{document}\n\\singlespacing\n\\input{sections/introduction}\n\\end{document}\n", None, True),
            ("switch between body sections", "\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\singlespacing\n\\input{sections/results}\n\\end{document}\n", "onehalfspacing", True),
            ("environment switch in the body", "\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\begin{singlespace}\n\\section{X}\n\\end{singlespace}\n\\end{document}\n", "onehalfspacing", True),
            ("brace group over body prose", "\\onehalfspacing\n\\begin{document}\n\\section{A}\n{\\singlespacing\\input{sections/results}}\n\\end{document}\n", "onehalfspacing", True),
            ("brace-scoped prose inside the body", "\\doublespacing\n\\begin{document}\n\\section{A}\nProse.\n{\\onehalfspacing more prose}\n\\section{B}\n\\end{document}\n", "doublespacing", True),
            ("prose after a tail switch", "\\doublespacing\n\\begin{document}\n\\section{Results}\nMain result prose.\n\\onehalfspacing\nMore result prose.\n\\end{document}\n", "doublespacing", True),
            ("tail switch directly before the bibliography", "\\doublespacing\n\\begin{document}\n\\section{Results}\nProse.\n\\clearpage\n\\onehalfspacing\n\\bibliography{ref}\n\\end{document}\n", "doublespacing", False),
            ("abstract-local spacing is not the declaration", "\\onehalfspacing\n\\begin{document}\n\\begin{abstract}\\doublespacing\\input{sections/abstract}\\end{abstract}\n\\input{sections/introduction}\n\\end{document}\n", "onehalfspacing", False),
            ("a spacing-carrying macro is rejected", "\\newcommand{\\compact}{\\onehalfspacing}\n\\doublespacing\n\\begin{document}\n\\compact\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True),
            ("a delimited def is rejected", "\\def\\compact#1.{\\onehalfspacing}\n\\doublespacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True),
            ("a document hook is rejected", "\\doublespacing\n\\AtBeginDocument{\\onehalfspacing}\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True),
            ("an xparse command is rejected", "\\NewDocumentCommand\\compact{}{\\onehalfspacing}\n\\doublespacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True),
            ("csname is unreadable", "\\doublespacing\n\\begin{document}\n\\csname onehalfspacing\\endcsname\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True),
            ("setspace package option declares", "\\usepackage[onehalfspacing]{setspace}\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "onehalfspacing", False),
            ("a multi-line unused definition is not executed", "\\newcommand{\\ia}{\n  \\input{sections/appendix}\n}\n\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "onehalfspacing", False),
            ("a body input outside sections/ is rejected", "\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\input{body}\n\\end{document}\n", "onehalfspacing", True),
            ("\\linespread is a spacing control", "\\linespread{1.3}\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", None, True),
            ("includeonly excludes a later chapter", "\\includeonly{sections/introduction}\n\\onehalfspacing\n\\begin{document}\n\\include{sections/introduction}\n\\singlespacing\n\\include{sections/results}\n\\end{document}\n", "onehalfspacing", False),
            ("no declaration", "\\begin{document}\n\\section{A}\n\\end{document}\n", None, False),
            ("a body input escaping sections/ is rejected", "\\onehalfspacing\n\\begin{document}\n\\input{sections/../outside}\n\\end{document}\n", "onehalfspacing", True),
            ("a definition body on the next line is owned", "\\newcommand{\\compact}\n  {\\singlespacing}\n\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "onehalfspacing", True),
            ("a brace-nested optional argument is owned", "\\newcommand{\\compact}[1][{]}]\n  {\\singlespacing}\n\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "onehalfspacing", True),
            ("an escaped brace in a def parameter text is not the body", "\\def\\foo#1\\{foo\\}#2{plain}\n\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\input{outside}\n\\end{document}\n", "onehalfspacing", True),
            ("an input after the body started is body prose", "\\doublespacing\n\\begin{document}\n\\section{Conclusion}\n\\singlespacing\n\\input{sections/conclusion}\n\\bibliography{ref}\n\\end{document}\n", "doublespacing", True),
            ("\\let assigns the token on the next line", "\\let\\bodyspace=\n\\doublespacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", None, True),
            ("a foreign extension is refused", "\\onehalfspacing\n\\begin{document}\n\\input{sections/results.ltx}\n\\end{document}\n", "onehalfspacing", True),
            ("\\subfile is an unsupported inclusion", "\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\subfile{sections/tables}\n\\end{document}\n", "onehalfspacing", True),
            ("an unbraced \\input is unsupported", "\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\input\\bodyfile\n\\end{document}\n", "onehalfspacing", True),
            ("\\let without = owns exactly one token", "\\doublespacing\n\\begin{document}\n\\let\\a\\b\n\\input{outside}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True),
            ("\\let does not swallow the declaration after it", "\\let\\a\\b\n\\doublespacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", False),
            ("the setspace environment-begin form declares", "\\doublespace\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", False),
            ("\\setlength{\\baselineskip} is a spacing control", "\\doublespacing\n\\begin{document}\n\\section{A}\n\\setlength{\\baselineskip}{8pt}\nProse.\n\\end{document}\n", "doublespacing", True),
            ("a definition owns only its own groups", "\\newcommand{\\noop}{x}\n{\\input{sections/results}}\n\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "onehalfspacing", False),
            ("an environment's end code is part of its definition", "\\newenvironment{compact}{}{\\onehalfspacing}\n\\doublespacing\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n", "doublespacing", True)):
        _sc = _scan_main_text(_tex)
        assert _sc["spacing"] == _want and bool(_sc["issues"]) == _bad, (_label, _sc)
    _sc = _scan_main_text("\\begin{document}\n\\input{sections/introduction}\n\\input{sections/tables}\n\\bibliography{ref}\n\\input{sections/appendix}\n\\end{document}\n")
    assert _sc["appendix_closes"] and _sc["document_inputs"] == ["introduction.tex", "tables.tex", "appendix.tex"], _sc
    _sc = _scan_main_text("\\newcommand{\\noop}{x}\n{\\input{sections/results}}\n\\begin{document}\n\\input{sections/introduction}\n\\end{document}\n")
    assert "results.tex" not in _sc["body_inputs"], _sc  # a preamble group is not the document
    _sc = _scan_main_text("\\begin{document}\n\\input{sections/introduction}\n\\input{sections/appendix}\n\\input{sections/tables}\n\\end{document}\n")
    assert _sc["appendix_wired"] and not _sc["appendix_closes"] and "appendix.tex" in _sc["body_inputs"], _sc
    with _tf_sp.TemporaryDirectory() as _sd:
        _d = Path(_sd); _secs = _d / "sections"; _secs.mkdir()
        (_secs / "titlepage.tex").write_text("\\maketitle\n", encoding="utf-8")
        (_secs / "introduction.tex").write_text("\\section{Introduction}\nProse.\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\begin{document}\n\\input{sections/titlepage}\n\\onehalfspacing\n\\input{sections/introduction}\n\\end{document}\n", encoding="utf-8")
        _sc = scan_manuscript(_d / "main.tex")
        assert _sc["spacing"] == "onehalfspacing" and not _sc["issues"] and _sc["body_inputs"] == ["introduction.tex"], _sc
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n\\input{body}\n", encoding="utf-8")
        assert any("inputs `body`" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "a section file inputting outside sections/"
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n\\input{sections/../outside}\n", encoding="utf-8")
        assert any("inputs `sections/../outside`" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "a section file escaping sections/"
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n\\input{sections/parts/intro_a}\n\\newcommand{\\x}{\\input{sections/unused}}\n", encoding="utf-8")
        (_secs / "parts").mkdir()
        (_secs / "parts" / "intro_a.tex").write_text("Prose.\n", encoding="utf-8")
        _sc = scan_manuscript(_d / "main.tex")
        assert _sc["body_inputs"] == ["introduction.tex", "parts/intro_a.tex"] and not _sc["issues"], _sc
        # roles by ancestry: a file the appendix alone reaches is IA; one a body section reaches is not
        (_secs / "appendix.tex").write_text("\\input{sections/appendix_tables}\n", encoding="utf-8")
        (_secs / "appendix_tables.tex").write_text("\\begin{table}\\caption{IA}\\end{table}\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\bibliography{ref}\n\\input{sections/appendix}\n\\end{document}\n", encoding="utf-8")
        assert scan_manuscript(_d / "main.tex")["ia_files"] == ["appendix.tex", "appendix_tables.tex"], scan_manuscript(_d / "main.tex")["ia_files"]
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n\\input{sections/appendix_tables}\n", encoding="utf-8")
        _sc2 = scan_manuscript(_d / "main.tex")
        assert _sc2["ia_files"] == ["appendix.tex"], "a body section's input is main body whatever its name"
        assert any("appendix_tables.tex is input 2 times" in i for i in _sc2["issues"]), _sc2["issues"]
        # the same file input twice at main level, or once at main level and once below, is typeset twice
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n", encoding="utf-8")
        (_secs / "tables.tex").write_text("\\begin{table}\\caption{T}\\label{tab:t}\\end{table}\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\input{sections/tables}\n\\input{sections/tables}\n\\end{document}\n", encoding="utf-8")
        _sc3 = scan_manuscript(_d / "main.tex")
        assert _sc3["wrappers"] == ["tables.tex"] and any("sections/tables.tex twice" in i for i in _sc3["issues"]), _sc3
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n\\input{sections/tables}\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\input{sections/tables}\n\\end{document}\n", encoding="utf-8")
        assert any("tables.tex is input 2 times" in i for i in scan_manuscript(_d / "main.tex")["issues"]), scan_manuscript(_d / "main.tex")["issues"]
        (_secs / "tables.tex").unlink()
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n", encoding="utf-8")
        (_secs / "appendix.tex").unlink(); (_secs / "appendix_tables.tex").unlink()
        (_d / "style.tex").write_text("\\newcommand{\\compact}{\\singlespacing}\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\input{style}\n\\begin{document}\n\\input{sections/titlepage}\n\\onehalfspacing\n\\input{sections/introduction}\n\\end{document}\n", encoding="utf-8")
        assert any("preamble" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "a preamble file defining spacing"
        (_d / "style.tex").write_text("\\input{nested}\n", encoding="utf-8")
        (_d / "nested.tex").write_text("\\renewcommand{\\section}{\\singlespacing}\n", encoding="utf-8")
        assert any("nested.tex (input in the preamble)" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "a nested preamble input defining spacing"
        (_d / "nested.tex").write_text("plain\n", encoding="utf-8")
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n\\subfile{sections/parts/intro_a}\n", encoding="utf-8")
        assert any("unsupported inclusion" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "\\subfile in a section file"
        (_secs / "introduction.tex").write_text("\\section{Introduction}\n", encoding="utf-8")
        # an unwired section file is inert; an optional input is followed only when present
        (_secs / "old_results.tex").write_text("\\singlespacing stale\n", encoding="utf-8")
        _sc = scan_manuscript(_d / "main.tex")
        assert not _sc["issues"] and str(_secs / "old_results.tex") not in _sc["live_files"], _sc
        (_d / "main.tex").write_text("\\InputIfFileExists{local-options}{}{}\n\\begin{document}\n\\input{sections/titlepage}\n\\onehalfspacing\n\\input{sections/introduction}\n\\end{document}\n", encoding="utf-8")
        assert not scan_manuscript(_d / "main.tex")["issues"], "an absent optional input is inert"
        (_d / "local-options.tex").write_text("\\singlespacing\n", encoding="utf-8")
        assert any("local-options.tex (input in the preamble)" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "a present optional input is followed"
        (_d / "local-options.tex").unlink()
        # the recorder is the ground truth: a file TeX read that the grammar did not model is an issue
        (_secs / "hidden.tex").write_text("\\singlespacing hidden prose\n", encoding="utf-8")
        (_d / "main.fls").write_text(f"PWD {_d}\nINPUT main.tex\nINPUT sections/titlepage.tex\nINPUT sections/introduction.tex\nINPUT sections/hidden.tex\nINPUT /usr/share/texmf/tex/latex/base/article.cls\n", encoding="utf-8")
        _sc = scan_manuscript(_d / "main.tex")
        assert _sc["recorder"]["unmodeled"] == ["sections/hidden.tex"] and any("main.fls" in i for i in _sc["issues"]) and any("hidden.tex: spacing control" in i for i in _sc["issues"]), _sc
        (_d / "tables").mkdir(exist_ok=True); (_d / "tables" / "main_results.tex").write_text("\\begin{tabular}{l}x\\end{tabular}\n", encoding="utf-8")
        (_d / "main.fls").write_text(f"PWD {_d}\nINPUT main.tex\nINPUT sections/titlepage.tex\nINPUT sections/introduction.tex\nINPUT ./tables/main_results.tex\n", encoding="utf-8")
        assert not scan_manuscript(_d / "main.tex")["issues"], scan_manuscript(_d / "main.tex")["issues"]  # exhibit content files are the wrappers' inputs
        (_d / "main.fls").unlink(); (_secs / "hidden.tex").unlink()
        # a nested input reached from the abstract is modeled too
        (_secs / "abstract.tex").write_text("\\begin{abstract}x\\end{abstract}\\input{sections/results}\n", encoding="utf-8")
        (_secs / "results.tex").write_text("\\section{Results}\\singlespacing\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\onehalfspacing\n\\begin{document}\n\\input{sections/abstract}\n\\input{sections/introduction}\n\\end{document}\n", encoding="utf-8")
        assert any("results.tex: spacing control" in i for i in scan_manuscript(_d / "main.tex")["issues"]), "an input reached from the abstract is live"
        (_secs / "abstract.tex").unlink(); (_secs / "results.tex").unlink()
        # the IA heading is the appendix file's own, with \\Title expanded
        (_secs / "appendix.tex").write_text("\\setcounter{page}{1}\n\\begin{center}\n{\\Large \\bf Internet Appendix for \\\\ ``\\Title''}\n\\end{center}\n\\section{Proofs}\n", encoding="utf-8")
        (_d / "main.tex").write_text("\\newcommand{\\Title}{A Generic Paper Title}\n\\onehalfspacing\n\\begin{document}\n\\input{sections/introduction}\n\\input{sections/appendix}\n\\end{document}\n", encoding="utf-8")
        assert appendix_heading_text(_d / "main.tex") == "internet appendix for a generic paper title", appendix_heading_text(_d / "main.tex")
    _sc = _scan_main_text("\\begin{document}\n\\input{sections/introduction}\n\\input{sections/chapter/results.tex}\n\\input{sections/tables}\n"
                          "\\begingroup\\include {sections/appendix}\\endgroup\n\\end{document}\n")
    assert _sc["body_inputs"] == ["introduction.tex", "chapter/results.tex"] and _sc["wrappers"] == ["tables.tex"] and _sc["appendix_wired"], _sc
    assert not _scan_main_text("\\newcommand{\\ia}{\\input{sections/appendix}}\n\\begin{document}\n\\ia\n\\end{document}\n")["appendix_wired"]

    print("All validate_latex self-tests passed (collapsed floats, figure order, "
          "\\notes{} descriptions, path self-containment, scaffold round-trip, "
          "wired-IA round-trip, admitted-main grammar).")
    return 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--test":
        sys.exit(_run_self_test())

    import argparse
    ap = argparse.ArgumentParser(
        description="Validate the drafting structure of a LaTeX paper and the "
                    "working-paper layout every draft keeps (a journal's format is "
                    "applied on acceptance by journal_format.py, never checked here)."
    )
    ap.add_argument("main_tex", help="path/to/main.tex")
    args = ap.parse_args()

    main_tex = Path(args.main_tex)
    results = validate(main_tex)
    warnings = [r for r in results if r.startswith("WARNING")]
    issues = [r for r in results if not r.startswith("WARNING")]

    if issues:
        print(f"Found {len(issues)} issue(s):\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    for w in warnings:
        print(f"  ⚠ {w}")
    if issues:
        sys.exit(1)
    if not warnings:
        print("✅ All checks passed!")
    sys.exit(0)


if __name__ == "__main__":
    main()
