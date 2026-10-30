#!/usr/bin/env python3
"""journal_format.py — the one-shot journal house-style engine.

    journal_format.py check --journal jfqa path/to/main.tex [--json]
    journal_format.py apply --journal jfqa path/to/main.tex [--report PATH]
    journal_format.py codex --journal jfqa path/to/main.tex

`--journal` is REQUIRED on every verb and never inferred from the manuscript.
The engine runs ONLY once a paper is accepted at a journal (user directive
2026-09-21): every working paper keeps the one working-paper format (the
latex skill's wp scaffold, held by validate_latex.py and the gan S0 gate),
and `/latex <code>` converts the ACCEPTED manuscript. Facts live in
journals/<code>.yaml (facts only — references/journal_file.md); every verb
consumes the file's STATED facts (`journal_rules.load_journal`): an unstated
fact is never checked and never defaulted. The gan plugin's LaTeX log parser
and Codex pin are reused when present (no gan GATE consumes a journal fact —
that is the decoupling), with standalone fallbacks.

check   — every stated fact against the manuscript (main.tex plus every
          \\input it reaches); every violation as `file:line: [layout.spacing]
          message`; candidate lines for every `house:` item that carries a
          `locate` regex. Never writes. Exit 1 on any violation.

apply   — fixes every mechanical fact in place (each fix in the OWNING file,
          nothing flattened into main.tex), runs latexmk once, parses the log
          (errors, warnings, boxes, the natbib year-collapse warning), scans
          the PDF text for the rendered collapse, counts main-text pages
          before the appendix heading, prints ONE status line, and writes the
          report's deterministic sections (docs/submission/latex-<code>.md by
          default), leaving headed sections for the agent's house pass.
          Idempotent. Exit 2 on a compile error (first error with file:line).

codex   — exactly ONE `codex exec` (model/effort pinned in the gan plugin's
          references/codex_invocation.json) over a disposable copy of the
          manuscript directory, with the journal's facts and house list as
          the review sheet; prints a JSON list of findings. Never a second
          round.

Always on for every journal, not in the YAML: a key repeated inside one
citation command (the natbib year-collapse trigger, fixed at source), the
collapse in the log and in the rendered PDF (blocking, need a compile),
booktabs rules in tables/, and no \\footnote{} inside a float.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from journal_rules import available_journals, journal_file, load_journal, normalize_journal, provenance_note  # noqa: E402

_GAN_SCRIPTS = Path.home() / ".claude" / "plugins" / "gan" / "scripts"
if str(_GAN_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_GAN_SCRIPTS))
try:  # the ONE LaTeX log parser (errors / warnings / boxes / undefined refs)
    from compile_with_provenance import parse_latex_log  # type: ignore
except ImportError:  # standalone install without the plugin
    def parse_latex_log(log_text: str) -> dict:  # minimal fallback
        errs = re.findall(r"^(?:\./)?([^\n:]+\.tex):(\d+):\s*(.+)$", log_text, re.M)
        return {"errors": [f"{f}:{l}: {m}" for f, l, m in errs],
                "warnings": re.findall(r"^(?:LaTeX|Package)[^\n]*Warning:[^\n]*$", log_text, re.M),
                "undefined_refs": [], "undefined_citations": [], "page_count_log": 0, "rerun_requested": False}


# ---------------------------------------------------------------------------
# manuscript model
# ---------------------------------------------------------------------------

_COMMENT_RE = re.compile(r'(?<!\\)((?:\\\\)*)%.*')
_INPUT_RE = re.compile(r'\\(?:input|include)\s*\{\s*([^}]+?)\s*\}')
_FLOAT_BEGIN_RE = re.compile(r'\\begin\s*\{(table\*?|figure\*?|sidewaystable|sidewaysfigure|landscape|equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|tabular\*?|tabularx|longtable|thebibliography)\}')
_FLOAT_END_RE = re.compile(r'\\end\s*\{(table\*?|figure\*?|sidewaystable|sidewaysfigure|landscape|equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|tabular\*?|tabularx|longtable|thebibliography)\}')
_FOOTNOTE_RE = re.compile(r'\\footnote\s*\{')


def strip_comments(line: str) -> str:
    return _COMMENT_RE.sub(r"\1", line)


@dataclass
class TexFile:
    path: Path
    lines: list[str]                       # raw lines (no trailing newline)
    stripped: list[str] = field(default_factory=list)
    in_preamble: list[bool] = field(default_factory=list)
    in_float: list[bool] = field(default_factory=list)   # inside a float/math/tabular env
    is_table_content: bool = False         # a pure tabular content file under tables/

    def rebuild(self, preamble_start: bool = True) -> None:
        """`preamble_start`: main.tex starts in the preamble; a fragment starts
        wherever its \\input sits — style.tex (input before \\begin{document})
        is preamble, sections/*.tex (input after it) are BODY. A fragment
        never carries \\begin{document} itself, so without this flag every
        section file would count as preamble and escape every body check."""
        self.stripped = [strip_comments(ln) for ln in self.lines]
        pre, depth = preamble_start, 0
        self.in_preamble, self.in_float = [], []
        for ln in self.stripped:
            if r"\begin{document}" in ln:
                pre = False
            self.in_preamble.append(pre)
            self.in_float.append(depth > 0 or bool(_FLOAT_BEGIN_RE.search(ln)))
            depth += len(_FLOAT_BEGIN_RE.findall(ln)) - len(_FLOAT_END_RE.findall(ln))
            depth = max(depth, 0)
        self.is_table_content = "tables" in self.path.parts[-2:-1] and not any(
            r"\begin{table" in ln for ln in self.stripped)


def _footnote_spans(line: str) -> list[tuple[int, int]]:
    """Character spans of \\footnote{...} arguments on one line (brace-balanced)."""
    spans = []
    for m in _FOOTNOTE_RE.finditer(line):
        i, depth = m.end(), 1
        while i < len(line) and depth:
            if line[i] == "{" and line[i - 1] != "\\":
                depth += 1
            elif line[i] == "}" and line[i - 1] != "\\":
                depth -= 1
            i += 1
        spans.append((m.start(), i))
    return spans


def _mask_footnotes(line: str) -> str:
    out = line
    for a, b in reversed(_footnote_spans(line)):
        out = out[:a] + " " * (b - a) + out[b:]
    return out


class Manuscript:
    """main.tex plus every file it reaches through a live \\input, in reach
    order; `also` — body fragments the manuscript does not input yet (an
    appendix a project has unwired) — are loaded after the graph, so a
    fix pass covers what a later re-wiring will input."""

    def __init__(self, main: Path, also: tuple[Path, ...] | list[Path] = ()):
        self.main = main.resolve()
        self.root = self.main.parent
        self.also = [Path(p).resolve() for p in also]
        self.files: list[TexFile] = []
        self.reload()

    def reload(self) -> None:
        self.files = []
        seen: set[Path] = set()
        for queue in ([(self.main, True)], [(p, False) for p in self.also]):
            while queue:
                p, preamble_start = queue.pop(0)
                if p in seen or not p.is_file():
                    continue
                seen.add(p)
                tf = TexFile(p, p.read_text(encoding="utf-8", errors="replace").split("\n"))
                tf.rebuild(preamble_start=preamble_start)
                self.files.append(tf)
                for i, ln in enumerate(tf.stripped):
                    for m in _INPUT_RE.finditer(ln):
                        tgt = m.group(1).strip()
                        if not tgt.endswith(".tex"):
                            tgt += ".tex"
                        q = (self.root / tgt) if not tgt.startswith("/") else Path(tgt)
                        if q.is_file():
                            queue.append((q.resolve(), tf.in_preamble[i]))
        self.by_path = {f.path: f for f in self.files}

    @property
    def main_file(self) -> TexFile:
        return self.files[0]

    @property
    def preamble_files(self) -> list[TexFile]:
        """main.tex plus every file it inputs BEFORE \\begin{document} (style.tex)."""
        out = [self.main_file]
        for tf in self.files[1:]:
            if all(tf.in_preamble) or tf.path.name == "style.tex":
                out.append(tf)
        return out

    def rel(self, p: Path) -> str:
        try:
            return str(p.relative_to(self.root))
        except ValueError:
            return str(p)

    def write(self, tf: TexFile) -> None:
        tf.path.write_text("\n".join(tf.lines), encoding="utf-8")

    # compile products beside main.tex
    @property
    def log_path(self) -> Path:
        return self.main.with_suffix(".log")

    @property
    def pdf_path(self) -> Path:
        return self.main.with_suffix(".pdf")

    def pdf_text(self) -> str:
        if not self.pdf_path.is_file() or not shutil.which("pdftotext"):
            return ""
        try:
            return subprocess.run(["pdftotext", "-layout", str(self.pdf_path), "-"],
                                  capture_output=True, text=True, timeout=120).stdout
        except (subprocess.SubprocessError, OSError):
            return ""


# ---------------------------------------------------------------------------
# violations
# ---------------------------------------------------------------------------

@dataclass
class Violation:
    rule: str
    file: str
    line: int
    message: str
    severity: str = "block"
    auto_fixable: bool = False
    original: str = ""
    proposal: str | None = None            # the fixed line (or a prose proposal)
    fixed: bool = False
    _apply: object = field(default=None, repr=False, compare=False)

    def public(self) -> dict:
        d = asdict(self)
        d.pop("_apply", None)
        return d


def _preview(s: str, n: int = 110) -> str:
    s = s.strip()
    return s if len(s) <= n else s[: n - 3] + "..."


# ---------------------------------------------------------------------------
# fact normalization
# ---------------------------------------------------------------------------

_SPACING_KIND = {"single": "singlespacing", "onehalf": "onehalfspacing", "double": "doublespacing"}


def _norm_margins(m) -> dict:
    if isinstance(m, dict):
        return {k: str(v) for k, v in m.items()}
    return {k: str(m) for k in ("top", "bottom", "left", "right")}


def _norm_spacings(s) -> tuple:
    kinds = s if isinstance(s, list) else [s]
    return tuple(_SPACING_KIND[k] for k in kinds)


def checkable_facts(facts: dict) -> dict:
    """The fact sections flattened to the shapes the checks read. Absent keys
    stay absent — a fact that is not stated is never checked."""
    lay, cit = dict(facts.get("layout") or {}), dict(facts.get("citations") or {})
    out: dict = {}
    if {"paper", "font_pt", "class_options"} & lay.keys():
        out["paper"] = lay.get("paper")
        out["font_pt"] = lay.get("font_pt")
        out["class_options"] = list(lay["class_options"]) if "class_options" in lay else None
    if "margins" in lay:
        out["margins"] = _norm_margins(lay["margins"])
    if "spacing" in lay:
        out["spacings"] = _norm_spacings(lay["spacing"])
    if "font" in lay:
        out["font_family"] = lay["font"]
    if "bst" in cit:
        out["bst"] = cit["bst"]
    if "in_text" in cit:
        out["parenthetical"] = cit["in_text"]
    if "full_authors_first" in cit:
        out["first_cite_full_authors"] = bool(cit["full_authors_first"])
    return out


# ---------------------------------------------------------------------------
# detectors — each: (ms, facts, rule) -> list[Violation]
# a detector that can fix attaches `_apply`: a callable (ms) -> bool
# ---------------------------------------------------------------------------

_DOCCLASS_RE = re.compile(r'\\documentclass\s*(?:\[([^\]]*)\])?\s*\{([^}]+)\}')
_GEOMETRY_PKG_RE = re.compile(r'\\usepackage\s*(?:\[([^\]]*)\])?\s*\{\s*geometry\s*\}')
_GEOMETRY_CMD_RE = re.compile(r'\\geometry\s*\{([^}]*)\}')
_USEPACKAGE_RE = re.compile(r'\\usepackage\s*(?:\[([^\]]*)\])?\s*\{([^}]*)\}')
_SPACING_DECL_RE = re.compile(r'(?<![\w\\@])\\(doublespacing|onehalfspacing|singlespacing)\b')
_SETSTRETCH_RE = re.compile(r'(?<![\w\\@])\\setstretch\s*\{\s*([0-9.]+)\s*\}')
_CITE_RE = re.compile(r'\\(cite|citet|citep|citealt|citealp|citeauthor|citeyear|citeyearpar|Citet|Citep)\*?'
                      r'((?:\s*\[[^\]]*\]){0,2})\s*\{([^}]*)\}')
_THE_SEC_RE = re.compile(r'\\renewcommand\s*\{\\the(section|subsection|subsubsection)\}\s*\{((?:[^{}]|\{[^{}]*\})*)\}')
_ABSTRACT_ENV_RE = re.compile(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', re.DOTALL)
_ABSTRACT_CMD_RE = re.compile(r'\\abstract\s*\{((?:[^{}]|\{[^{}]*\})*)\}', re.DOTALL)
_BIBSTYLE_RE = re.compile(r'\\bibliographystyle\s*\{([^}]*)\}')
_BIBLIOGRAPHY_RE = re.compile(r'\\bibliography\s*\{')

_FONT_FAMILY_PACKAGES = {"times": ("newtxtext", "newtx", "mathptmx", "times", "tgtermes", "txfonts")}
_NUMBERING_MACRO = {"arabic": r"\arabic", "Roman": r"\Roman", "roman": r"\roman",
                    "Alph": r"\Alph", "alph": r"\alph"}


def _find_line(tf: TexFile, regex: re.Pattern, *, preamble_only=False) -> int | None:
    for i, ln in enumerate(tf.stripped):
        if preamble_only and not tf.in_preamble[i]:
            continue
        if regex.search(ln):
            return i
    return None


def _first_preamble_hit(ms: Manuscript, regex: re.Pattern):
    for tf in ms.preamble_files:
        i = _find_line(tf, regex, preamble_only=True)
        if i is not None:
            return tf, i
    return None, None


def _set_line(ms: Manuscript, tf: TexFile, i: int, new: str) -> bool:
    if tf.lines[i] == new:
        return False
    # a replacement may carry a newline (a grouped \usepackage split in two)
    tf.lines[i:i + 1] = new.split("\n")
    ms.write(tf)
    ms.reload()
    return True


def _replace_in_line(ms: Manuscript, tf: TexFile, i: int, pairs: list[tuple[str, str]]) -> bool:
    """Apply (old -> new) fragment replacements to the line AS IT IS NOW, so two
    rules editing one line compose instead of overwriting each other."""
    cur = ms.by_path[tf.path].lines[i]
    new = cur
    for old, rep in pairs:
        new = new.replace(old, rep, 1)
    return _set_line(ms, ms.by_path[tf.path], i, new)


def _sub_in_line(ms: Manuscript, tf: TexFile, i: int, regex, repl) -> bool:
    cur = ms.by_path[tf.path].lines[i]
    new = regex.sub(repl, cur)
    return _set_line(ms, ms.by_path[tf.path], i, new)


def _join_lines(ms: Manuscript, tf: TexFile, i: int, j: int, new: str) -> bool:
    """Replace physical lines i..j (inclusive) with the single line `new` — a
    citation command whose argument wrapped across lines is rewritten whole."""
    cur = ms.by_path[tf.path]
    if cur.lines[i:j + 1] == [new]:
        return False
    cur.lines[i:j + 1] = [new]
    ms.write(cur)
    ms.reload()
    return True


def _insert_before_line(ms: Manuscript, tf: TexFile, i: int, new_lines: list[str]) -> bool:
    tf.lines[i:i] = new_lines
    ms.write(tf)
    ms.reload()
    return True


def _preamble_end(ms: Manuscript) -> tuple[TexFile, int]:
    """(file, index) of \\begin{document} in main — the insertion point."""
    mf = ms.main_file
    i = _find_line(mf, re.compile(r'\\begin\{document\}'))
    return mf, (i if i is not None else len(mf.lines))


def _hyperref_or_end(ms: Manuscript) -> tuple[TexFile, int]:
    """Insert packages before hyperref (it must load last) when present."""
    tf, i = _first_preamble_hit(ms, re.compile(r'\\usepackage\s*(?:\[[^\]]*\])?\s*\{\s*hyperref\s*\}'))
    if tf is not None:
        return tf, i
    return _preamble_end(ms)


def check_documentclass(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    mf = ms.main_file
    i = _find_line(mf, _DOCCLASS_RE, preamble_only=True)
    if i is None:
        return [Violation(rule["id"], ms.rel(mf.path), 1, "no \\documentclass found", rule.get("severity", "block"))]
    m = _DOCCLASS_RE.search(mf.stripped[i])
    opts = [o.strip() for o in (m.group(1) or "").split(",") if o.strip()]
    sizes = [o for o in opts if re.fullmatch(r"\d+pt", o)]
    papers = [o for o in opts if o.endswith("paper")]
    extras = [o for o in opts if o not in sizes and o not in papers]
    # every part is checked only when the journal STATES it (absent = untouched)
    want_pt = f"{int(fmt['font_pt'])}pt" if fmt.get("font_pt") else (sizes[0] if sizes else None)
    want_paper = fmt.get("paper") or (papers[0] if papers else None)
    class_opts_stated = fmt.get("class_options") is not None
    extras_allowed = list(fmt.get("class_options") or []) if class_opts_stated else extras
    paper_elsewhere = _paper_from_geometry(ms)
    problems = []
    if fmt.get("font_pt") and sizes != [want_pt]:
        problems.append(f"font size {sizes or 'unset'} must be {want_pt}")
    if fmt.get("paper"):
        if papers and papers != [want_paper]:
            problems.append(f"paper size {papers} must be {want_paper}")
        if not papers and paper_elsewhere not in (None, want_paper):
            problems.append(f"paper size {paper_elsewhere} (geometry) must be {want_paper}")
        if not papers and paper_elsewhere is None:
            problems.append(f"paper size is unstated (documentclass or geometry) — the journal requires {want_paper}")
    bad_extras = [o for o in extras if o not in extras_allowed]
    if bad_extras:
        problems.append(f"option(s) {bad_extras} are outside the journal's format "
                        f"(allowed beyond size/paper: {extras_allowed or 'none'})")
    missing_extras = [o for o in extras_allowed if o not in opts] if class_opts_stated else []
    if missing_extras:
        problems.append(f"required option(s) {missing_extras} missing")
    if not problems:
        return []
    keep = [o for o in extras if o in extras_allowed] + missing_extras
    new_opts = ", ".join([o for o in (want_paper, want_pt) if o] + keep)
    v = Violation(rule["id"], ms.rel(mf.path), i + 1, "; ".join(problems), rule.get("severity", "block"),
                  auto_fixable=bool(rule.get("auto_fixable")), original=mf.lines[i],
                  proposal=mf.lines[i].replace(m.group(0), f"\\documentclass[{new_opts}]{{{m.group(2)}}}", 1))
    v._apply = lambda ms_, tf=mf, idx=i, old=m.group(0), rep=f"\\documentclass[{new_opts}]{{{m.group(2)}}}": _replace_in_line(ms_, tf, idx, [(old, rep)])
    return [v]


def _geometry_hits(ms: Manuscript) -> list[tuple[TexFile, int, str]]:
    out = []
    for tf in ms.preamble_files:
        for i, ln in enumerate(tf.stripped):
            if not tf.in_preamble[i]:
                continue
            m = _GEOMETRY_PKG_RE.search(ln)
            if m:
                out.append((tf, i, m.group(1) or ""))
            for m2 in _GEOMETRY_CMD_RE.finditer(ln):
                out.append((tf, i, m2.group(1)))
    return out


def _parse_geometry_opts(opts: str) -> dict:
    d: dict = {}
    for tok in [t.strip() for t in opts.split(",") if t.strip()]:
        if "=" in tok:
            k, v = [x.strip() for x in tok.split("=", 1)]
            d[k] = v
        else:
            d[tok] = True
    return d


def _paper_from_geometry(ms: Manuscript) -> str | None:
    for _, _, opts in _geometry_hits(ms):
        d = _parse_geometry_opts(opts)
        for k in d:
            if k.endswith("paper"):
                return k
        if "paper" in d and isinstance(d["paper"], str):
            return d["paper"]
    return None


def _effective_margins(opts: dict) -> dict:
    m: dict = {}
    if "margin" in opts:
        m = {k: opts["margin"] for k in ("top", "bottom", "left", "right")}
    if "hmargin" in opts:
        m["left"] = m["right"] = opts["hmargin"]
    if "vmargin" in opts:
        m["top"] = m["bottom"] = opts["vmargin"]
    for k in ("top", "bottom", "left", "right"):
        if k in opts:
            m[k] = opts[k]
    return m


def _norm_len(s) -> str:
    s = str(s).strip().replace(" ", "")
    m = re.fullmatch(r"([0-9]*\.?[0-9]+)(in|cm|mm|pt)", s)
    if not m:
        return s
    return f"{float(m.group(1)):g}{m.group(2)}"


def check_geometry_margins(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    want = {k: _norm_len(v) for k, v in fmt["margins"].items()}
    hits = _geometry_hits(ms)
    if not hits:
        tf, i = _preamble_end(ms)
        opts = ([fmt["paper"]] if fmt.get("paper") else []) + [f"{k}={want[k]}" for k in ("top", "bottom", "left", "right")]
        line = f"\\usepackage[{','.join(opts)}]{{geometry}}"
        v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                      f"no geometry settings — the journal requires margins {want}", rule.get("severity", "block"),
                      auto_fixable=bool(rule.get("auto_fixable")), original="", proposal=line)
        v._apply = lambda ms_, tf=tf, idx=i, new=line: _insert_before_line(ms_, ms_.by_path[tf.path], idx, [new])
        return [v]
    out = []
    for tf, i, opts in hits:
        d = _parse_geometry_opts(opts)
        got = {k: _norm_len(v) for k, v in _effective_margins(d).items()}
        wrong = {k: (got.get(k), want[k]) for k in want if got.get(k) != want[k]}
        if not wrong:
            continue
        # rewrite: keep non-margin options, set the four margins explicitly
        keep = [k if v is True else f"{k}={v}" for k, v in d.items()
                if k not in ("margin", "hmargin", "vmargin", "top", "bottom", "left", "right")]
        new_opts = ",".join(keep + [f"{k}={want[k]}" for k in ("top", "bottom", "left", "right")])
        old = tf.lines[i]
        if _GEOMETRY_PKG_RE.search(tf.stripped[i]):
            rx, rep = _GEOMETRY_PKG_RE, f"\\\\usepackage[{new_opts}]{{geometry}}"
        else:
            rx, rep = _GEOMETRY_CMD_RE, f"\\\\geometry{{{new_opts}}}"
        v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                      "margins " + ", ".join(f"{k}={g or 'unset'} (journal: {w})" for k, (g, w) in wrong.items()),
                      rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                      original=old, proposal=rx.sub(rep, old, 1))
        v._apply = lambda ms_, tf=tf, idx=i, rx=rx, rep=rep: _sub_in_line(ms_, tf, idx, rx, rep)
        out.append(v)
    return out


def check_line_spacing(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    """The body spacing main.tex declares must be one of the journal's accepted
    kinds; every other body-kind declaration is rewritten to the first accepted."""
    accepted = list(fmt["spacings"])
    body_kinds = {"doublespacing", "onehalfspacing"}
    out = []
    mf = ms.main_file
    declared = []
    for i, ln in enumerate(mf.stripped):
        if mf.in_preamble[i] or mf.in_float[i]:
            continue
        for m in _SPACING_DECL_RE.finditer(ln):
            declared.append((i, m.group(1), m))
    body_declared = [(i, k, m) for i, k, m in declared if k in body_kinds]
    if not body_declared:
        # a \setstretch{2} counts as doublespacing, {1.5} as onehalfspacing
        for i, ln in enumerate(mf.stripped):
            if mf.in_preamble[i]:
                continue
            for m in _SETSTRETCH_RE.finditer(ln):
                kind = {"2": "doublespacing", "2.0": "doublespacing", "1.5": "onehalfspacing"}.get(m.group(1))
                if kind:
                    body_declared.append((i, kind, m))
    if not body_declared:
        tf, i = mf, (_find_line(mf, re.compile(r'\\begin\{document\}')) or 0) + 1
        v = Violation(rule["id"], ms.rel(mf.path), i + 1,
                      f"main.tex declares no body line spacing; the journal accepts {' or '.join('\\' + s for s in accepted)}",
                      rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                      original="", proposal=f"\\{accepted[0]}")
        v._apply = lambda ms_, tf=tf, idx=i, new=f"\\{accepted[0]}": _insert_before_line(ms_, ms_.by_path[tf.path], idx, [new])
        return [v]
    for i, kind, m in body_declared:
        if kind in accepted:
            continue
        new = mf.lines[i].replace(m.group(0), f"\\{accepted[0]}", 1)
        v = Violation(rule["id"], ms.rel(mf.path), i + 1,
                      f"\\{kind} declared; the journal accepts only {' or '.join('\\' + s for s in accepted)}",
                      rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                      original=mf.lines[i], proposal=new)
        v._apply = lambda ms_, tf=mf, idx=i, old=m.group(0), rep=f"\\{accepted[0]}": _replace_in_line(ms_, tf, idx, [(old, rep)])
        out.append(v)
    return out


def check_font_family(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    family = fmt.get("font_family")
    if not family:
        return []
    pkgs = _FONT_FAMILY_PACKAGES.get(family, ())
    for tf in ms.preamble_files:
        for i, ln in enumerate(tf.stripped):
            if not tf.in_preamble[i]:
                continue
            for m in _USEPACKAGE_RE.finditer(ln):
                names = {n.strip() for n in m.group(2).split(",")}
                if names & set(pkgs):
                    return []
    tf, i = _hyperref_or_end(ms)
    new = "\\usepackage{newtxtext,newtxmath}  % journal: Times New Roman body text"
    v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                  f"no {family} font package loaded (one of {pkgs}); the journal requires {family} body text",
                  rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")), original="", proposal=new)
    v._apply = lambda ms_, tf=tf, idx=i, new=new: _insert_before_line(ms_, ms_.by_path[tf.path], idx, [new])
    return [v]


def _norm_preamble_line(ln: str) -> str:
    """A required preamble line, compared ignoring its trailing comment."""
    return strip_comments(ln).strip()


def check_preamble_lines(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """layout.preamble: verbatim lines, each of which must exist in the
    preamble (compared comment-insensitively); missing ones are inserted as
    ONE block, in YAML order (a `\\usepackage` and the `\\def` that depends on
    it keep their relative order). A required `\\usepackage[opts]{name}` line
    whose package is ALREADY loaded reconciles its options onto the existing
    load — inserting a second load would be a fatal option clash."""
    required = list((facts.get("layout") or {}).get("preamble") or [])
    present: set[str] = set()
    for tf in ms.preamble_files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i]:
                present.add(_norm_preamble_line(ln))
    out: list[Violation] = []
    missing_plain: list[str] = []
    for want in required:
        m_want = _USEPACKAGE_RE.search(_norm_preamble_line(want))
        if not (m_want and m_want.group(1)):
            if _norm_preamble_line(want) not in present:
                missing_plain.append(want)
            continue
        names = {n.strip() for n in m_want.group(2).split(",")}
        want_opts = [o.strip() for o in m_want.group(1).split(",") if o.strip()]
        hit = None
        for tf in ms.preamble_files:
            for i, ln in enumerate(tf.stripped):
                if not tf.in_preamble[i]:
                    continue
                m = _USEPACKAGE_RE.search(ln)
                if m and ({n.strip() for n in m.group(2).split(",")} & names):
                    hit = (tf, i, m)
                    break
            if hit:
                break
        if hit:
            tf, i, m = hit
            have_opts = [o.strip() for o in (m.group(1) or "").split(",") if o.strip()]
            need = [o for o in want_opts if o not in have_opts]
            if need:
                loaded = [n.strip() for n in m.group(2).split(",") if n.strip()]
                target = next(n for n in loaded if n in names)
                opts = have_opts + need
                if len(loaded) == 1:
                    rep = f"\\usepackage[{','.join(opts)}]{{{target}}}"
                else:
                    # a grouped load (amsmath,amssymb,bm,amsthm): the option belongs
                    # to ONE package — split it out, never pass it to the group
                    rest = ",".join(n for n in loaded if n != target)
                    head = f"\\usepackage[{','.join(have_opts)}]" if have_opts else "\\usepackage"
                    rep = f"\\usepackage[{','.join(opts)}]{{{target}}}\n{head}{{{rest}}}"
                pair = (m.group(0), rep)
                v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                              f"\\usepackage{{{target}}} lacks option(s) {need} (required line: `{want}`)",
                              rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                              original=tf.lines[i], proposal=tf.lines[i].replace(pair[0], pair[1], 1))
                v._apply = lambda ms_, tf=tf, idx=i, pair=pair: _replace_in_line(ms_, tf, idx, [pair])
                out.append(v)
        elif _norm_preamble_line(want) not in present:
            missing_plain.append(want)
    if missing_plain:
        tf, i = _preamble_end(ms)
        v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                      "preamble lacks " + " ; ".join(f"`{w}`" for w in missing_plain),
                      rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                      original="", proposal="\n".join(missing_plain))
        v._apply = lambda ms_, tf=tf, idx=i, block=missing_plain: _insert_before_line(ms_, ms_.by_path[tf.path], idx, block)
        out.append(v)
    return out


def check_body_prelude(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """layout.ragged_right / hyphenation / parindent — the body prelude right
    after \\begin{document} (\\raggedright zeroes \\parindent, so the journal's
    indent is re-set after it)."""
    lay = facts.get("layout") or {}
    lines: list[str] = []
    if lay.get("ragged_right"):
        lines.append("\\raggedright")
    if lay.get("parindent"):
        lines.append(f"\\parindent={lay['parindent']}%")
    if lay.get("hyphenation") is False:
        lines += ["\\hyphenpenalty=10000", "\\exhyphenpenalty=10000"]
    if not lines:
        return []
    body = [(i, ln) for i, ln in enumerate(ms.main_file.stripped) if not ms.main_file.in_preamble[i]]
    missing = []
    for want in lines:
        rx = re.compile(re.escape(want.split("=")[0].rstrip("%")))
        if not any(rx.search(ln) for _, ln in body):
            missing.append(want)
    if not missing:
        return []
    mf = ms.main_file
    bd = _find_line(mf, re.compile(r'\\begin\{document\}'))
    i = (bd + 1) if bd is not None else 0
    block = ["% journal body prelude: left-align / no hyphenation / first-line indent"] + lines
    v = Violation(rule["id"], ms.rel(mf.path), i + 1,
                  f"body lacks {', '.join(missing)} after \\begin{{document}}",
                  rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                  original="", proposal="\n".join(block))
    v._apply = lambda ms_, idx=i, block=block: _insert_before_line(ms_, ms_.main_file, idx, block)
    return [v]


def check_bst(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    """citations.bst: \\bibliographystyle{X}, and the .bst file itself must sit
    beside main.tex — the reference list cannot be built without it."""
    want = fmt["bst"]
    bst_path = ms.root / f"{want}.bst"
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            m = _BIBSTYLE_RE.search(ln)
            if not m:
                continue
            if m.group(1).strip() == want:
                if not bst_path.is_file():
                    return [Violation(rule["id"], ms.rel(ms.main), 0,
                                      f"{want}.bst is not beside main.tex — copy it into {ms.root}; "
                                      f"the reference list cannot be built without it",
                                      rule.get("severity", "block"))]
                return []
            new = tf.lines[i].replace(m.group(0), f"\\bibliographystyle{{{want}}}", 1)
            v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                          f"\\bibliographystyle{{{m.group(1)}}} — the journal's style is {want}"
                          + ("" if bst_path.is_file() else f" (and {want}.bst must be copied beside main.tex)"),
                          rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                          original=tf.lines[i], proposal=new)
            v._apply = lambda ms_, tf=tf, idx=i, old=m.group(0), rep=f"\\bibliographystyle{{{want}}}": _replace_in_line(ms_, tf, idx, [(old, rep)])
            return [v]
    # no \bibliographystyle anywhere: insert one before \bibliography in main
    mf = ms.main_file
    i = _find_line(mf, _BIBLIOGRAPHY_RE)
    if i is None:
        i = len(mf.lines) - 1
    v = Violation(rule["id"], ms.rel(mf.path), i + 1,
                  f"no \\bibliographystyle — the journal's style is {want}"
                  + ("" if bst_path.is_file() else f" (and {want}.bst must be copied beside main.tex)"),
                  rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                  original="", proposal=f"\\bibliographystyle{{{want}}}")
    v._apply = lambda ms_, idx=i, new=f"\\bibliographystyle{{{want}}}": _insert_before_line(ms_, ms_.main_file, idx, [new])
    return [v]


def _tex_words(s: str) -> int:
    s = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}$]", " ", s)
    return len([w for w in s.split() if re.search(r"[A-Za-z0-9]", w)])


def check_abstract_words(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    limit = int((facts.get("length") or {})["abstract_words"])
    for tf in ms.files:
        text = "\n".join(tf.stripped)
        m = _ABSTRACT_ENV_RE.search(text) or _ABSTRACT_CMD_RE.search(text)
        if not m:
            continue
        body = m.group(1)
        # JEL / Keywords lines (and the spacing commands around them) are not abstract prose
        body = "\n".join(
            ln for ln in body.split("\n")
            if not re.match(r"^\s*(?:\\noindent\s*)?(?:\\(?:textbf|emph|textit)\{)?\s*(?:JEL|Keywords?)\b", ln))
        n = _tex_words(body)
        line = text[: m.start()].count("\n") + 1
        if n > limit:
            return [Violation(rule["id"], ms.rel(tf.path), line,
                              f"abstract is {n} words; the journal limit is {limit}",
                              rule.get("severity", "block"), original=_preview(body, 80),
                              proposal=f"cut {n - limit} word(s) — the {limit}-word limit is a ceiling")]
        return []
    return [Violation(rule["id"], ms.rel(ms.main), 1, "no abstract (\\begin{abstract} or \\abstract{}) found", "warn")]


_APPENDIX_TITLE_RE = re.compile(
    r"(Internet\s+Appendix|Online\s+Appendix|Supplementary\s+Material|Supplemental\s+Appendix|"
    r"Supplementary\s+Appendix|Online\s+Supplement|Electronic\s+Companion|Web\s+Appendix)", re.IGNORECASE)


def check_appendix_title(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    want = (facts.get("structure") or {}).get("appendix_title")
    if not want:
        return []
    out = []
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i]:
                continue
            heading_like = bool(re.search(r"\\(?:section|chapter|part)\*?\s*[\[{]|\\(?:Large|LARGE|large|huge|Huge)\b|\\begin\{center\}|\\centerline", ln))
            m = _APPENDIX_TITLE_RE.search(ln)
            if not (m and heading_like):
                continue
            if re.sub(r"\s+", " ", m.group(1)).lower() == want.lower():
                continue
            new = tf.lines[i][: m.start()] + want + tf.lines[i][m.end():] if tf.lines[i] == tf.stripped[i] else \
                tf.lines[i].replace(m.group(1), want, 1)
            v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                          f"appendix heading reads '{m.group(1)}'; the journal calls it '{want}'",
                          rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                          original=tf.lines[i], proposal=new)
            v._apply = lambda ms_, tf=tf, idx=i, old=m.group(1), rep=want: _replace_in_line(ms_, tf, idx, [(old, rep)])
            out.append(v)
    return out


def check_appendix_mentions(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """In-text references that still use another journal's appendix name —
    located here, rewritten by Claude in the house pass."""
    want = (facts.get("structure") or {}).get("appendix_title")
    if not want:
        return []
    out = []
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i]:
                continue
            for m in _APPENDIX_TITLE_RE.finditer(ln):
                if re.sub(r"\s+", " ", m.group(1)).lower() == want.lower():
                    continue
                if re.search(r"\\(?:section|chapter|part)\*?\s*[\[{]|\\(?:Large|LARGE|large)\b", ln):
                    continue  # the heading rule owns headings
                out.append(Violation(rule["id"], ms.rel(tf.path), i + 1,
                                     f"in-text '{m.group(1)}' — the journal's term is '{want}'",
                                     rule.get("severity", "warn"), original=tf.lines[i],
                                     proposal=tf.lines[i].replace(m.group(1), want)))
                break
    return out


def check_section_numbering(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    want = (facts.get("structure") or {}).get("numbering") or {}
    if not want:
        return []
    found: dict[str, tuple[TexFile, int, str]] = {}
    for tf in ms.preamble_files:
        for i, ln in enumerate(tf.stripped):
            if not tf.in_preamble[i]:
                continue
            for m in _THE_SEC_RE.finditer(ln):
                found[m.group(1)] = (tf, i, m.group(2))
    expected = {
        "section": f"{_NUMBERING_MACRO[want['section']]}{{section}}",
        "subsection": f"\\thesection.{_NUMBERING_MACRO[want['subsection']]}{{subsection}}",
        "subsubsection": f"\\thesubsection.{_NUMBERING_MACRO[want['subsubsection']]}{{subsubsection}}",
    }
    default_ok = want == {"section": "arabic", "subsection": "arabic", "subsubsection": "arabic"}
    problems = []
    for level, exp in expected.items():
        got = found.get(level)
        if got is None:
            if default_ok:
                continue
            problems.append(f"\\the{level} not redefined (journal: {exp})")
        elif got[2].replace(" ", "") != exp.replace(" ", ""):
            problems.append(f"\\the{level} is {{{got[2]}}} (journal: {{{exp}}})")
    if not problems:
        return []
    block = [f"\\renewcommand{{\\the{lvl}}}{{{exp}}}" for lvl, exp in expected.items()]
    tf, i = (found["section"][0], found["section"][1]) if "section" in found else _preamble_end(ms)
    v = Violation(rule["id"], ms.rel(tf.path), i + 1, "; ".join(problems), rule.get("severity", "block"),
                  auto_fixable=bool(rule.get("auto_fixable")),
                  original=tf.lines[i] if "section" in found else "", proposal="\n".join(block))

    def _apply(ms_, block=block):
        changed = False
        for tf_ in ms_.preamble_files:
            keep = [ln for ln in tf_.lines if not _THE_SEC_RE.search(strip_comments(ln))]
            if len(keep) != len(tf_.lines):
                tf_.lines = keep
                ms_.write(tf_)
                changed = True
        ms_.reload()
        tf_, idx = _preamble_end(ms_)
        _insert_before_line(ms_, tf_, idx, ["% journal section numbering"] + block)
        return True
    v._apply = _apply
    return [v]


_THE_EXHIBIT_RE = re.compile(r'\\renewcommand\s*\{\\the(table|figure)\}\s*\{((?:[^{}]|\{[^{}]*\})*)\}')


def check_exhibit_numbering(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """structure.exhibit_numbering: {table: arabic|roman, figure: arabic|roman}.
    LaTeX's default is arabic, so `arabic` means NO \\the<kind> redefinition in
    the preamble (the template's style.tex ships \\Roman for both); `roman` means one.
    The redefinition is rewritten or removed in its owning file."""
    want = (facts.get("structure") or {}).get("exhibit_numbering") or {}
    macro = {"arabic": r"\arabic", "roman": r"\Roman"}
    out = []
    found: dict[str, tuple[TexFile, int, str]] = {}
    for tf in ms.preamble_files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i]:
                for m in _THE_EXHIBIT_RE.finditer(ln):
                    found[m.group(1)] = (tf, i, m.group(2))
    for kind, style in want.items():
        exp = f"{macro[style]}{{{kind}}}"
        got = found.get(kind)
        if got is None:
            if style == "arabic":
                continue
            tf, i = _preamble_end(ms)
            line = f"\\renewcommand{{\\the{kind}}}{{{exp}}}"
            v = Violation(rule["id"], ms.rel(tf.path), i + 1, f"\\the{kind} not redefined (journal: {exp})",
                          rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                          original="", proposal=line)
            v._apply = lambda ms_, tf=tf, idx=i, new=line: _insert_before_line(ms_, ms_.by_path[tf.path], idx, [new])
            out.append(v)
            continue
        tf, i, body = got
        if body.replace(" ", "") == exp.replace(" ", ""):
            continue
        old = tf.lines[i]
        m = _THE_EXHIBIT_RE.search(strip_comments(old))
        rep = "" if style == "arabic" else f"\\renewcommand{{\\the{kind}}}{{{exp}}}"
        v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                      f"\\the{kind} is {{{body}}} (journal: {style} — {exp if style != 'arabic' else 'the LaTeX default'})",
                      rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                      original=old, proposal=old.replace(m.group(0), rep, 1).rstrip())
        v._apply = lambda ms_, tf=tf, idx=i, old_=m.group(0), rep=rep: _replace_in_line(ms_, tf, idx, [(old_, rep)])
        out.append(v)
    return out


def _cite_keys(arg: str) -> list[str]:
    return [k.strip() for k in arg.split(",") if k.strip()]


def _dedup_keys_rewrite(ln: str, raw: str) -> tuple[list[list[str]], str]:
    """Every citation command on one logical line whose argument repeats a
    key: [[duplicated keys], ...] and the raw line with each deduplicated."""
    hits: list[list[str]] = []
    new_line = raw
    for m in _CITE_RE.finditer(ln):
        keys = _cite_keys(m.group(3))
        dedup = list(dict.fromkeys(keys))
        if len(dedup) != len(keys):
            hits.append(sorted({k for k in keys if keys.count(k) > 1}))
            new_line = new_line.replace(m.group(0), m.group(0).replace("{" + m.group(3) + "}", "{" + ",".join(dedup) + "}"), 1)
    return hits, new_line


def _redup_span(ms: Manuscript, tf: TexFile, i: int, j: int) -> bool:
    """Apply-time fix for a wrapped span: recomputed from the lines AS THEY
    ARE NOW, then written as one line (the same shape as _rejoin_span)."""
    cur = ms.by_path[tf.path]
    j = _current_span_end(cur, i)
    stripped = " ".join(strip_comments(s).strip() for s in cur.lines[i:j + 1])
    raw = " ".join(s.strip() for s in cur.lines[i:j + 1])
    _, new = _dedup_keys_rewrite(stripped, raw)
    return _join_lines(ms, tf, i, j, new)


def check_citation_duplicate_keys(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    """The natbib year-collapse trigger: the same key twice inside ONE citation
    (a leftover of consolidating two citations) prints as `(2003, 0)` /
    `(2003,?)` with only a log warning. Deduplicated in place — on logical
    lines, so a citation whose argument wraps (`\\citet{alpha,\\nalpha}`) is
    seen like an unwrapped one; a wrapped span carrying a % comment is
    reported for a hand rewrite, never joined."""
    out = []
    for tf in ms.files:
        for i, j, ln, raw, resolved in _logical_lines(tf):
            if tf.in_preamble[i]:
                continue
            if not resolved:
                out.append(Violation(rule["id"], ms.rel(tf.path), i + 1,
                                     f"a citation command opened on line {i + 1} does not close within {_CITE_SPAN_MAX} lines — "
                                     "its keys cannot be checked for the natbib collapse; close or rewrite it by hand",
                                     rule.get("severity", "block"), original=tf.lines[i]))
                continue
            hits, new_line = _dedup_keys_rewrite(ln, raw)
            if not hits:
                continue
            commented = j > i and any(strip_comments(s) != s for s in tf.lines[i:j + 1])
            fixable = bool(rule.get("auto_fixable")) and not commented
            wrapped = (f" (wrapped across lines {i + 1}-{j + 1}; " + ("joined" if fixable else "a comment inside the span — dedup by hand") + ")") if j > i else ""
            v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                          "duplicate key inside one citation (natbib year-collapse trigger): "
                          + "; ".join(",".join(h) for h in hits) + wrapped,
                          rule.get("severity", "block"), auto_fixable=fixable,
                          original=raw, proposal=new_line if fixable else None)
            if fixable and j > i:
                v._apply = lambda ms_, tf=tf, a=i, b=j: _redup_span(ms_, tf, a, b)
            elif fixable:
                v._apply = lambda ms_, tf=tf, idx=i, new=new_line: _set_line(ms_, ms_.by_path[tf.path], idx, new)
            out.append(v)
    return out


_CITE_OPEN_RE = re.compile(r'\\(?:cite|citet|citep|citealt|citealp|citeauthor|citeyear|citeyearpar|Citet|Citep)\*?'
                           r'(?:\s*\[[^\]]*\]){0,2}\s*\{')
_BRACE_RE = re.compile(r'(?<!\\)[{}]')
_CITE_SPAN_MAX = 40


def _brace_delta(s: str) -> int:
    """Opening minus closing braces in `s`, escaped braces (\\{ \\}) ignored."""
    return sum(1 if m.group(0) == "{" else -1 for m in _BRACE_RE.finditer(s))


def _logical_lines(tf: TexFile):
    """(i, j, stripped, raw, resolved): each body line as the engine sees it.
    A citation command whose argument brace opens on line i and closes on a
    later line j is yielded ONCE as the joined span, so a wrapped \\citep is
    checked — and rewritten — exactly like an unwrapped one; the engine's
    silence on a citation then means conformance, never blindness. Balance
    is tracked from the citation's OWN opening brace (an \\emph{} group
    closing earlier on the line cannot hide it) with escaped braces ignored;
    a span that never balances within _CITE_SPAN_MAX lines is yielded with
    resolved=False so the caller reports it instead of scanning past it."""
    i, n = 0, len(tf.stripped)
    while i < n:
        j, resolved = i, True
        opens = [m for m in _CITE_OPEN_RE.finditer(tf.stripped[i])
                 if _brace_delta(tf.stripped[i][m.end() - 1:]) > 0]
        if opens:
            depth = _brace_delta(tf.stripped[i][opens[0].end() - 1:])
            for k in range(i + 1, min(n, i + _CITE_SPAN_MAX)):
                depth += _brace_delta(tf.stripped[k])
                if depth <= 0:
                    j = k
                    break
            else:
                j, resolved = min(n - 1, i + _CITE_SPAN_MAX - 1), False
        stripped = " ".join(s.strip() for s in tf.stripped[i:j + 1]) if j > i else tf.stripped[i]
        raw = " ".join(s.strip() for s in tf.lines[i:j + 1]) if j > i else tf.lines[i]
        yield i, j, stripped, raw, resolved
        i = j + 1


def _parenthetical_rewrite(ln: str, raw: str) -> tuple[list[tuple[str, str | None]], str]:
    """The citet_in_parens rewrite of one logical line: [(offending command,
    replacement or None when it needs a hand rewrite)], and the rewritten raw
    line. Keys are deduplicated in place (a repeated key is the natbib
    year-collapse trigger), so this composes with the duplicate-key fix
    whichever runs first."""
    bad: list[tuple[str, str | None]] = []
    new_line = raw
    for m in _CITE_RE.finditer(ln):
        cmd, optargs, arg = m.group(1), m.group(2), m.group(3)
        if cmd not in ("citep", "cite", "Citep"):
            continue
        if optargs.strip():
            bad.append((m.group(0), None))   # pre/post notes need a hand rewrite
            continue
        keys = list(dict.fromkeys(_cite_keys(arg)))
        if cmd == "cite":
            repl = "\\citet{" + ",".join(keys) + "}"
        else:
            inner = ", ".join(f"\\citet{{{k}}}" for k in keys)
            # a \citep already wrapped in literal parentheses keeps those
            # parentheses — adding our own would double them
            before = ln[: m.start()].rstrip()
            after = ln[m.end():].lstrip()
            repl = inner if before.endswith("(") and after.startswith(")") else "(" + inner + ")"
        bad.append((m.group(0), repl))
        new_line = new_line.replace(m.group(0), repl, 1)
    return bad, new_line


def _current_span_end(tf: TexFile, i: int) -> int:
    """The last line of the citation span that opens on line i AS THE FILE IS
    NOW: another fix may already have collapsed the span (a duplicate-key
    dedup and a citation-form rewrite target the same lines), and a stale
    end would join the paragraph break after it. i itself when no citation
    opens on line i or the span never balances."""
    opens = [m for m in _CITE_OPEN_RE.finditer(tf.stripped[i]) if _brace_delta(tf.stripped[i][m.end() - 1:]) > 0]
    if not opens:
        return i
    depth = _brace_delta(tf.stripped[i][opens[0].end() - 1:])
    for k in range(i + 1, min(len(tf.stripped), i + _CITE_SPAN_MAX)):
        depth += _brace_delta(tf.stripped[k])
        if depth <= 0:
            return k
    return i


def _rejoin_span(ms: Manuscript, tf: TexFile, i: int, j: int) -> bool:
    """Apply-time fix for a wrapped span: recomputed from the lines AS THEY
    ARE NOW (another rule may have edited a line inside the span, or already
    collapsed it, since the check ran), then written as one line."""
    cur = ms.by_path[tf.path]
    j = _current_span_end(cur, i)
    stripped = " ".join(strip_comments(s).strip() for s in cur.lines[i:j + 1])
    raw = " ".join(s.strip() for s in cur.lines[i:j + 1])
    _, new = _parenthetical_rewrite(stripped, raw)
    return _join_lines(ms, tf, i, j, new)


def check_citation_form(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    """`citations.in_text: citet_in_parens` (each cited year in its own
    parentheses) forbids \\citep and bare \\cite; `full_authors_first`
    requires natbib's longnamesfirst."""
    out = []
    if fmt.get("parenthetical") == "citet_in_parens":
        for tf in ms.files:
            for i, j, ln, raw, resolved in _logical_lines(tf):
                if tf.in_preamble[i]:
                    continue
                if not resolved:
                    out.append(Violation(rule["id"], ms.rel(tf.path), i + 1,
                                         f"a citation command opened on line {i + 1} does not close within "
                                         f"{_CITE_SPAN_MAX} lines — close or rewrite it by hand; nothing after it "
                                         "on this span was checked", rule.get("severity", "block"),
                                         original=tf.lines[i]))
                    continue
                bad, new_line = _parenthetical_rewrite(ln, raw)
                if not bad:
                    continue
                # a span carrying a % comment is never joined (the comment would
                # swallow the rest of the line): reported for a hand rewrite
                commented = j > i and any(strip_comments(s) != s for s in tf.lines[i:j + 1])
                fixable = all(r is not None for _, r in bad) and bool(rule.get("auto_fixable")) and not commented
                wrapped = (f" (wrapped across lines {i + 1}-{j + 1}; "
                           + ("joined" if fixable else "a comment inside the span — join by hand" if commented else "joined once fixable")
                           + ")") if j > i else ""
                v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                              "parenthetical citation form: " + "; ".join(
                                  f"{o} -> {r}" if r else f"{o} carries pre/post notes — rewrite by hand as (\\citet{{...}}, note)"
                                  for o, r in bad) + wrapped,
                              rule.get("severity", "block"), auto_fixable=fixable,
                              original=raw, proposal=new_line if fixable else None)
                if fixable and j > i:
                    v._apply = lambda ms_, tf=tf, a=i, b=j: _rejoin_span(ms_, tf, a, b)
                elif fixable:
                    v._apply = lambda ms_, tf=tf, idx=i, pairs=[(o, r) for o, r in bad]: _replace_in_line(ms_, tf, idx, pairs)
                out.append(v)
    if fmt.get("first_cite_full_authors"):
        tf, i = _first_preamble_hit(ms, re.compile(r'\\usepackage\s*(?:\[[^\]]*\])?\s*\{\s*natbib\s*\}'))
        if tf is None:
            out.append(Violation(rule["id"], ms.rel(ms.main), 1, "natbib is not loaded; the journal's author-year form needs it", rule.get("severity", "block")))
        else:
            m = _USEPACKAGE_RE.search(tf.stripped[i])
            opts = [o.strip() for o in (m.group(1) or "").split(",") if o.strip()]
            if "longnamesfirst" not in opts:
                pair = (m.group(0), f"\\usepackage[{','.join(opts + ['longnamesfirst'])}]{{natbib}}")
                new = tf.lines[i].replace(pair[0], pair[1], 1)
                v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                              "natbib lacks longnamesfirst — the journal lists all authors on a work's first citation",
                              rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                              original=tf.lines[i], proposal=new)
                v._apply = lambda ms_, tf=tf, idx=i, pair=pair: _replace_in_line(ms_, tf, idx, [pair])
                out.append(v)
    return out


_NATBIB_COLLAPSE_LOG_RE = re.compile(r"Package natbib Warning: Multiple citation on page (\d+): same authors and year", re.M)
_PDF_COLLAPSE_RE = re.compile(r"\(\s*(?:[^()]{0,80}?,\s*)?\d{4}[a-z]?,\s*[0?]\s*\)|\b\d{4}[a-z]?,\s*[0?]\)")


def check_natbib_collapse_log(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    if not ms.log_path.is_file():
        return []
    log = ms.log_path.read_text(encoding="utf-8", errors="replace")
    return [Violation(rule["id"], ms.rel(ms.log_path), 0,
                      f"natbib: multiple citation on page {m.group(1)} with the same authors and year and no "
                      f"distinguishing letter — the year prints as '0'/'?'. Remove the duplicate key from the citation, "
                      f"or give the two entries distinct years (2003a/2003b via the .bst)",
                      rule.get("severity", "block"))
            for m in _NATBIB_COLLAPSE_LOG_RE.finditer(log)]


def check_natbib_collapse_pdf(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    text = ms.pdf_text()
    if not text:
        return []
    out = []
    for m in _PDF_COLLAPSE_RE.finditer(text):
        page = text[: m.start()].count("\f") + 1
        out.append(Violation(rule["id"], ms.rel(ms.pdf_path), page,
                             f"rendered citation '{_preview(m.group(0), 60)}' on PDF page {page}: a year collapsed to '0'/'?' "
                             f"(natbib same-author-year collision)", rule.get("severity", "block")))
    return out


def check_exhibits_placement(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """`exhibits: end` — table/figure floats belong after the bibliography, never
    in the running text (located; the move is the house pass's job)."""
    if ((facts.get("structure") or {}).get("exhibits") or "end") != "end":
        return []
    out = []
    bib_seen = False
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i]:
                continue
            if re.search(r"\\bibliography\s*\{|\\printbibliography|\\begin\{thebibliography\}|\\clearpage\s*\\input\{sections/tables\}", ln):
                bib_seen = True
            if bib_seen:
                continue
            if re.search(r"\\begin\{(?:table|figure|sidewaystable|sidewaysfigure)\*?\}", ln) and tf.path.name not in ("tables.tex", "figures.tex", "appendix.tex"):
                out.append(Violation(rule["id"], ms.rel(tf.path), i + 1,
                                     "a float sits in the running text before the bibliography; the journal wants tables and figures at the end "
                                     "(leave a `[INSERT TABLE N ABOUT HERE]` marker where it belongs)",
                                     rule.get("severity", "warn"), original=tf.lines[i]))
    return out


def check_float_markers(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """`float_markers: true` — every exhibit label printed at the end should
    have an `[INSERT TABLE/FIGURE N ABOUT HERE]` marker in the text."""
    if not (facts.get("structure") or {}).get("float_markers"):
        return []
    body = "\n".join(ln for tf in ms.files for i, ln in enumerate(tf.stripped) if not tf.in_preamble[i])
    main_part = re.split(r"(?m)^\s*\\appendix\b", body, maxsplit=1)[0]
    labels = re.findall(r"\\begin\{(table|figure)\*?\}.*?\\label\{([^}]+)\}", main_part, re.S)
    markers = set(re.findall(r"\\floathere\{[^}]*\}\{([^}]+)\}", body))
    markers |= set(re.findall(r"INSERT\s+(?:TABLE|FIGURE)\s*~?\\ref\{([^}]+)\}", body))
    return [Violation(rule["id"], ms.rel(ms.main), 0,
                      f"exhibit \\label{{{lab}}} has no placement marker in the text — write "
                      f"[INSERT {kind.upper()}~\\ref{{{lab}}} ABOUT HERE] where it belongs", rule.get("severity", "warn"))
            for kind, lab in labels if lab not in markers]


def check_title_page(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    st = facts.get("structure") or {}
    tp_blind = st.get("title_page") == "blind"
    mf = ms.main_file
    text = "\n".join(mf.stripped)
    out = []
    if not re.search(r"\\maketitle|\\begin\{titlepage\}", text):
        out.append(Violation(rule["id"], ms.rel(mf.path), 1, "no \\maketitle / titlepage", rule.get("severity", "warn")))
    if st.get("jel") or st.get("keywords"):
        abs_text = ""
        for tf in ms.files:
            m = _ABSTRACT_ENV_RE.search("\n".join(tf.stripped))
            if m:
                abs_text = "\n".join(tf.stripped)[m.start(): m.end() + 600]
                break
        if st.get("jel") and not re.search(r"\bJEL\b", abs_text):
            out.append(Violation(rule["id"], ms.rel(mf.path), 1, "no JEL classification after the abstract", rule.get("severity", "warn")))
        if st.get("keywords") and not re.search(r"\bKeywords?\b", abs_text, re.I):
            out.append(Violation(rule["id"], ms.rel(mf.path), 1, "no Keywords line after the abstract", rule.get("severity", "warn")))
    if tp_blind:
        for i, ln in enumerate(mf.stripped):
            if not mf.in_preamble[i] and re.search(r"\\thanks\s*\{|\\author\s*\{", ln):
                out.append(Violation(rule["id"], ms.rel(mf.path), i + 1,
                                     "the reviewed manuscript is blind: author names, affiliations and acknowledgments belong on the separate title page file",
                                     rule.get("severity", "warn"), original=ln))
                break
    return out


def check_equation_refs(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """`citations.equation_ref: "equation (N)"` — in-text equation references
    read 'equation (3)' (\\eqref), never 'Eq. 3' / 'Equation 3'."""
    form = (facts.get("citations") or {}).get("equation_ref")
    if not form:
        return []
    out = []
    rx = re.compile(r"\b(Eq\.?|Eqs\.?|Equation|Equations)\s*~?\s*\\ref\{")
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i] or tf.in_float[i]:
                continue
            m = rx.search(ln)
            if m:
                new = _EQ_SINGLE_RE.sub(r"equation~\\eqref{\2}", tf.lines[i])
                new = _EQ_PLURAL_RE.sub(r"equations~\\eqref{\2}", new)
                v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                              f"'{m.group(0)}...' — the journal's in-text form is '{form}' (equation~\\eqref{{...}})",
                              rule.get("severity", "warn"), auto_fixable=bool(rule.get("auto_fixable")),
                              original=tf.lines[i], proposal=new)

                def _eq_apply(ms_, tf=tf, idx=i):
                    a = _sub_in_line(ms_, tf, idx, _EQ_SINGLE_RE, r"equation~\\eqref{\2}")
                    b = _sub_in_line(ms_, tf, idx, _EQ_PLURAL_RE, r"equations~\\eqref{\2}")
                    return a or b
                v._apply = _eq_apply
                out.append(v)
    return out


_EQ_SINGLE_RE = re.compile(r"\b(Eq\.?|Equation)\s*~?\s*\\ref\{([^}]+)\}")
_EQ_PLURAL_RE = re.compile(r"\b(Eqs\.?|Equations)\s*~?\s*\\ref\{([^}]+)\}")
_BARE_STARS_RE = re.compile(r"(?<=[0-9)])(\*{1,3})(?![\w*}])")


def check_significance_stars(ms: Manuscript, facts: dict, rule: dict) -> list[Violation]:
    """`citations.stars: superscript` — significance stars in table cells are
    set as superscripts ($^{***}$), never bare `0.123***`."""
    if (facts.get("citations") or {}).get("stars") != "superscript":
        return []
    out = []
    for tf in ms.files:
        if not tf.is_table_content:
            continue
        for i, ln in enumerate(tf.stripped):
            if "$^{" in ln and not _BARE_STARS_RE.search(ln.replace("$^{***}$", "").replace("$^{**}$", "").replace("$^{*}$", "")):
                continue
            if _BARE_STARS_RE.search(ln):
                v = Violation(rule["id"], ms.rel(tf.path), i + 1, "bare significance stars after a number — set them as superscripts",
                              rule.get("severity", "warn"), auto_fixable=bool(rule.get("auto_fixable")),
                              original=tf.lines[i],
                              proposal=_BARE_STARS_RE.sub(lambda m: f"$^{{{m.group(1)}}}$", tf.lines[i]))
                v._apply = lambda ms_, tf=tf, idx=i: _sub_in_line(ms_, tf, idx, _BARE_STARS_RE, lambda m: f"$^{{{m.group(1)}}}$")
                out.append(v)
    return out


# always-on table conventions (every journal; the drafting structure carries them too)
_HLINE_RE = re.compile(r'\\hline')


def check_booktabs(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    out = []
    for tf in ms.files:
        if not tf.is_table_content:
            continue
        for i, ln in enumerate(tf.stripped):
            if _HLINE_RE.search(ln):
                out.append(Violation(rule["id"], ms.rel(tf.path), i + 1,
                                     "\\hline in a table — use \\toprule / \\midrule / \\bottomrule (booktabs)",
                                     rule.get("severity", "warn"), original=tf.lines[i]))
    return out


_SPACING_DEFINITION_RE = re.compile(
    r'\\(?:def|(?:re)?newcommand\*?|providecommand\*?)\s*\{?\\(?:double|onehalf|single)spacing\}?'
    r'|\\(?:def|(?:re)?newcommand\*?|providecommand\*?)\s*\{?\\[A-Za-z@]+\}?[^%\n]*?\\(?:setstretch|linespread|baselinestretch)\b')


def check_no_spacing_definition(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    """Always on: no preamble line DEFINES a spacing command or a macro whose
    body changes the spacing (`\\def\\doublespacing{\\setstretch{2}}`) — the
    validator's grammar refuses it because the page cap is keyed on what
    main.tex states, so such a line makes every applied draft fail S0. A
    journal's true stretch is written where the body spacing is declared
    (\\setstretch{2}), never behind a definition. Auto-fix: the line goes."""
    out = []
    for tf in ms.preamble_files:
        for i, ln in enumerate(tf.stripped):
            if not tf.in_preamble[i] or not _SPACING_DEFINITION_RE.search(ln):
                continue
            v = Violation(rule["id"], ms.rel(tf.path), i + 1,
                          f"a preamble definition changes the line spacing ({_preview(ln, 70)}) — the page cap is "
                          f"keyed on what main.tex states; write the stretch where the body spacing is declared",
                          rule.get("severity", "block"), auto_fixable=bool(rule.get("auto_fixable")),
                          original=tf.lines[i], proposal="")
            v._apply = lambda ms_, tf=tf, idx=i: _set_line(ms_, ms_.by_path[tf.path], idx, "")
            out.append(v)
    return out


def check_no_footnote_in_float(ms: Manuscript, fmt: dict, rule: dict) -> list[Violation]:
    out = []
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i] or not tf.in_float[i]:
                continue
            if _FOOTNOTE_RE.search(ln):
                out.append(Violation(rule["id"], ms.rel(tf.path), i + 1,
                                     "\\footnote inside a float — move it to the table/figure notes",
                                     rule.get("severity", "warn"), original=tf.lines[i]))
    return out


# ---------------------------------------------------------------------------
# fact-key dispatch
# ---------------------------------------------------------------------------

def _fact_checks(facts: dict) -> list[tuple[str, object, dict]]:
    """(check id, check fn, rule meta) for every fact the journal states."""
    lay = facts.get("layout") or {}
    st = facts.get("structure") or {}
    cit = facts.get("citations") or {}
    fmt = checkable_facts(facts)
    checks: list[tuple[str, object, dict]] = []
    if {"paper", "font_pt", "class_options"} & lay.keys():
        checks.append(("layout.documentclass", check_documentclass,
                       {"severity": "block", "auto_fixable": True}))
    if "margins" in lay:
        checks.append(("layout.margins", check_geometry_margins,
                       {"severity": "block", "auto_fixable": True}))
    if "spacing" in lay:
        checks.append(("layout.spacing", check_line_spacing,
                       {"severity": "block", "auto_fixable": True}))
    if "font" in lay:
        checks.append(("layout.font", check_font_family,
                       {"severity": "block", "auto_fixable": True}))
    if lay.get("preamble"):
        checks.append(("layout.preamble", check_preamble_lines,
                       {"severity": "block", "auto_fixable": True}))
    if {"ragged_right", "hyphenation", "parindent"} & lay.keys():
        checks.append(("layout.body", check_body_prelude,
                       {"severity": "warn", "auto_fixable": True}))
    if (facts.get("length") or {}).get("abstract_words") is not None:
        checks.append(("length.abstract_words", check_abstract_words,
                       {"severity": "block", "auto_fixable": False}))
    if st.get("numbering"):
        checks.append(("structure.numbering", check_section_numbering,
                       {"severity": "block", "auto_fixable": True}))
    if st.get("exhibit_numbering"):
        checks.append(("structure.exhibit_numbering", check_exhibit_numbering,
                       {"severity": "block", "auto_fixable": True}))
    if st.get("appendix_title"):
        checks.append(("structure.appendix_title", check_appendix_title,
                       {"severity": "block", "auto_fixable": True}))
        checks.append(("structure.appendix_mentions", check_appendix_mentions,
                       {"severity": "warn", "auto_fixable": False}))
    if {"title_page", "jel", "keywords"} & st.keys():
        checks.append(("structure.title_page", check_title_page,
                       {"severity": "warn", "auto_fixable": False}))
    if st.get("exhibits"):
        checks.append(("structure.exhibits", check_exhibits_placement,
                       {"severity": "warn", "auto_fixable": False}))
    if st.get("float_markers"):
        checks.append(("structure.float_markers", check_float_markers,
                       {"severity": "warn", "auto_fixable": False}))
    if "bst" in cit:
        checks.append(("citations.bst", check_bst,
                       {"severity": "block", "auto_fixable": True}))
    if "in_text" in cit or "full_authors_first" in cit:
        checks.append(("citations.form", check_citation_form,
                       {"severity": "block", "auto_fixable": True}))
    if cit.get("equation_ref"):
        checks.append(("citations.equation_ref", check_equation_refs,
                       {"severity": "warn", "auto_fixable": True}))
    if cit.get("stars"):
        checks.append(("citations.stars", check_significance_stars,
                       {"severity": "warn", "auto_fixable": True}))
    return [(cid, fn, {"id": cid, **meta, "_fmt": fmt}) for cid, fn, meta in checks]


def _always_on() -> list[tuple[str, object, dict]]:
    return [
        ("citation.duplicate_keys", check_citation_duplicate_keys,
         {"id": "citation.duplicate_keys", "severity": "block", "auto_fixable": True, "_fmt": {}}),
        ("tables.booktabs", check_booktabs,
         {"id": "tables.booktabs", "severity": "warn", "auto_fixable": False, "_fmt": {}}),
        ("tables.no_footnote_in_float", check_no_footnote_in_float,
         {"id": "tables.no_footnote_in_float", "severity": "warn", "auto_fixable": False, "_fmt": {}}),
        ("preamble.spacing_definition", check_no_spacing_definition,
         {"id": "preamble.spacing_definition", "severity": "block", "auto_fixable": True, "_fmt": {}}),
        ("citation.natbib_collapse_log", check_natbib_collapse_log,
         {"id": "citation.natbib_collapse_log", "severity": "block", "auto_fixable": False, "_fmt": {}}),
        ("citation.natbib_collapse_pdf", check_natbib_collapse_pdf,
         {"id": "citation.natbib_collapse_pdf", "severity": "block", "auto_fixable": False, "_fmt": {}}),
    ]


def check_facts(main_tex: Path, facts: dict, also=()) -> list[Violation]:
    """Every violation of `facts` (the journal-file vocabulary: layout,
    length, structure, citations) plus the always-on checks, sorted by
    location. `facts` is the journal file's stated facts
    (`journal_rules.load_journal(code)["facts"]`); `also` lists fragments
    the manuscript does not input yet (Manuscript)."""
    ms = Manuscript(main_tex, also)
    out: list[Violation] = []
    for cid, fn, rule in _fact_checks(facts) + _always_on():
        if fn in (check_documentclass, check_geometry_margins, check_line_spacing,
                  check_font_family, check_bst, check_citation_form):
            out.extend(fn(ms, rule["_fmt"], rule))
        else:
            out.extend(fn(ms, facts, rule))
    out.sort(key=lambda v: (v.file, v.line, v.rule))
    return out


def run_checks(main_tex: Path, journal: str, also=()) -> tuple[dict, list[Violation]]:
    """The journal document and every violation of its stated facts."""
    doc = load_journal(journal)
    return doc, check_facts(main_tex, doc["facts"], also)


def house_candidates(main_tex: Path, house: list[dict]) -> list[tuple[dict, str, int, str]]:
    """(item, file, line, preview) for every house item with a locate regex —
    running text only (never the preamble, floats or footnotes: table notes
    and footnotes may carry what the prose may not)."""
    ms = Manuscript(main_tex)
    out = []
    for item in house:
        locate = item.get("locate")
        if not locate:
            continue
        rx = re.compile(locate)
        for tf in ms.files:
            if tf.is_table_content:
                continue
            for i, ln in enumerate(tf.stripped):
                if tf.in_preamble[i] or tf.in_float[i]:
                    continue
                if rx.search(_mask_footnotes(ln)):
                    out.append((item, ms.rel(tf.path), i + 1, _preview(ln, 110)))
    return out


def apply_fixes(main_tex: Path, violations: list[Violation], also=()) -> int:
    """Apply every auto-fixable violation's canonical fix (bottom-up per file so
    line numbers stay valid), then return the count applied."""
    ms = Manuscript(main_tex, also)
    applied = 0
    for v in sorted([v for v in violations if v.auto_fixable and v._apply is not None],
                    key=lambda v: (v.file, -v.line)):
        try:
            if v._apply(ms):
                v.fixed = True
                applied += 1
        except Exception as exc:  # noqa: BLE001 — one failing fix must not hide the rest
            v.message += f" [fix failed: {type(exc).__name__}: {exc}]"
        ms.reload()
    return applied


def apply_all(main_tex: Path, journal: str, max_rounds: int = 3, also=()) -> int:
    """Bounded fix rounds: one fix's detection can depend on another's write
    (an inserted package line reveals the next check; a block insert shifts a
    captured index) — re-check and re-apply until a round applies nothing,
    at most `max_rounds`. Returns the total applied. Idempotent: a second
    call on a converted manuscript returns 0. `also`: fragments the
    manuscript does not input yet, fixed alongside (Manuscript)."""
    applied = 0
    for _ in range(max_rounds):
        _, before = run_checks(main_tex, journal, also)
        n = apply_fixes(main_tex, before, also) if before else 0
        applied += n
        if n == 0:
            break
    return applied


# ---------------------------------------------------------------------------
# compile + report (the apply verb)
# ---------------------------------------------------------------------------

_BOX_RE = re.compile(r"^(Overfull|Underfull)\s+\\([hv]box)\s+\(([^)]*)\)([^\n]*)", re.M)
_BOX_LINES_RE = re.compile(r"(?:at lines?|in paragraph at lines?)\s+(\d+)(?:--(\d+))?")


def compile_once(main_tex: Path, timeout: int = 600, appendix_title: str | None = None) -> dict:
    """latexmk -pdf; {ok, rc, errors, warnings, boxes, pages, main_pages, log}.
    `main_pages` counts the pages before the appendix heading (the journal cap
    applies to the main text; the appendix is excluded)."""
    cwd = main_tex.parent
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "-halt-on-error", main_tex.name]
    if not shutil.which("latexmk"):
        return {"ok": False, "rc": 127, "errors": ["latexmk not found on PATH"], "warnings": [],
                "boxes": [], "pages": 0, "main_pages": 0, "log": "", "seconds": 0,
                "undefined_refs": [], "undefined_citations": []}
    t0 = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    log_path = main_tex.with_suffix(".log")
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.is_file() else ""
    parsed = parse_latex_log(log)
    boxes = []
    for m in _BOX_RE.finditer(log):
        kind, box, amount, rest = m.groups()
        lm = _BOX_LINES_RE.search(rest or "")
        boxes.append({"kind": kind, "box": box, "amount": amount.strip(),
                      "lines": (lm.group(1) + (f"--{lm.group(2)}" if lm.group(2) else "")) if lm else "?"})
    pdf = main_tex.with_suffix(".pdf")
    pages = 0
    if pdf.is_file() and shutil.which("pdfinfo"):
        try:
            out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=60).stdout
            pm = re.search(r"^Pages:\s+(\d+)", out, re.M)
            pages = int(pm.group(1)) if pm else 0
        except (subprocess.SubprocessError, OSError):
            pages = 0
    if not pages:
        pages = int(parsed.get("page_count_log") or 0)
    main_pages = pages
    if pdf.is_file() and appendix_title and shutil.which("pdftotext"):
        try:
            text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=120).stdout
            start = appendix_start_page(text.split("\f"), appendix_title,
                                        appendix_heading_text(Manuscript(main_tex), appendix_title))
            if start:
                main_pages = start - 1
        except (subprocess.SubprocessError, OSError):
            pass
    errors = list(parsed.get("errors") or [])
    return {"ok": rc == 0 and not errors and pdf.is_file(), "rc": rc, "errors": errors, "main_pages": main_pages,
            "warnings": [w for w in (parsed.get("warnings") or []) if not w.startswith(("Overfull", "Underfull"))],
            "undefined_refs": parsed.get("undefined_refs") or [], "undefined_citations": parsed.get("undefined_citations") or [],
            "boxes": boxes, "pages": pages, "seconds": round(time.monotonic() - t0, 1), "log": log}


_REFERENCES_PAGE_RE = re.compile(r"^\s*(?:References|Bibliography)\s*$", re.M | re.I)
_TITLE_MACRO_RE = re.compile(r"\\newcommand\s*\{\\Title\}\s*\{((?:[^{}]|\{[^{}]*\})*)\}")


def _normalize_heading(text: str) -> str:
    """Letters, digits and single spaces, lower-case — the same reduction for
    a TeX heading and for a pdftotext page opening (twin of
    validate_latex.normalize_heading; kept local because validate_latex
    imports this module)."""
    text = re.sub(r"\\[A-Za-z@]+\*?", " ", str(text or ""))
    text = re.sub(r"[{}`'\"“”‘’\\]", " ", text)
    return " ".join(re.findall(r"[^\W_]+", text)).lower()


def appendix_heading_text(ms: Manuscript, appendix_title: str) -> str:
    """The manuscript's OWN appendix heading, normalized — the template's
    `Internet Appendix for ``\\Title''` with \\Title expanded from main.tex —
    or '' when no body line carries the title in a heading-like context."""
    title = ""
    for tf in ms.preamble_files:
        for ln in tf.stripped:
            m = _TITLE_MACRO_RE.search(ln)
            if m:
                title = m.group(1)
                break
        if title:
            break
    rx = re.compile(re.escape(appendix_title), re.I)
    for tf in ms.files:
        for i, ln in enumerate(tf.stripped):
            if tf.in_preamble[i] or not rx.search(ln):
                continue
            if re.search(r"\\(?:section|chapter|part)\*?\s*[\[{]|\\(?:Large|LARGE|large|huge|Huge)\b|\\begin\{center\}|\\centerline", ln):
                return _normalize_heading(ln.replace("\\Title", title))
    return ""


def appendix_start_page(page_texts: list[str], appendix_title: str, heading: str = "") -> int | None:
    """1-based page on which the appendix HEADING opens the page, or None.
    The manuscript the journal cap measures ends where the appendix begins,
    and only a heading begins it, after the References page. With the
    manuscript's own heading (`appendix_heading_text`, normalized) the
    boundary is the first page whose opening five lines contain it — a
    caption or a body sentence naming the appendix never qualifies. Without
    one, the fallback is the title as the FIRST line of a page: alone, or
    followed by for/to/of or a colon/dash, not a sentence. No References
    page → nothing is excluded (the count stays the whole document: fail
    closed). Same rule as the gan L1 gate's page measurement."""
    ref_page = next((k for k, pt in enumerate(page_texts, start=1) if _REFERENCES_PAGE_RE.search(pt)), 0)
    if not ref_page:
        return None
    head = re.compile(r"^\s*" + re.escape(appendix_title) + r"(?:\s*$|\s+(?:for|to|of)\b|\s*[:—–-])", re.I)
    for k, pt in enumerate(page_texts, start=1):
        if k <= ref_page:
            continue
        lines = [ln.strip() for ln in pt.splitlines() if ln.strip()]
        if heading:
            if heading in _normalize_heading(" ".join(lines[:5])):
                return k
            continue
        first = lines[0] if lines else ""
        nxt = lines[1] if len(lines) > 1 else ""
        if first and len(first) <= 120 and not first.endswith(".") and head.match(first) and not (nxt and nxt[0].islower()):
            return k
    return None


def page_cap(facts: dict, main_tex: Path) -> int | None:
    """length.pages, or the spacing-keyed cap resolved from what main.tex declares
    (LaTeX's `doublespacing` / `\\setstretch{2}` map to the YAML vocabulary)."""
    length = facts.get("length") or {}
    by_spacing = length.get("pages_by_spacing") or {}
    if "pages" in length:
        return int(length["pages"])
    if by_spacing:
        ms = Manuscript(main_tex)
        kind = None
        for i, ln in enumerate(ms.main_file.stripped):
            if ms.main_file.in_preamble[i]:
                continue
            m = _SPACING_DECL_RE.search(ln)
            if m:
                kind = {"doublespacing": "double", "onehalfspacing": "onehalf", "singlespacing": "single"}[m.group(1)]
                break
            m = _SETSTRETCH_RE.search(ln)
            if m:
                kind = {"2": "double", "2.0": "double", "1.5": "onehalf", "1": "single"}.get(m.group(1))
                break
        if kind in by_spacing:
            return int(by_spacing[kind])
        return int(min(by_spacing.values()))
    return None


def _pt(amount: str) -> float:
    m = re.search(r"([0-9.]+)pt", amount)
    return float(m.group(1)) if m else 0.0


def _diff(original: str, proposal: str, path: str, line: int) -> str:
    """A fragment diff: the changed span with ~40 characters of context on each
    side, so a one-word edit inside a 900-character paragraph reads as one."""
    if "\n" in original or "\n" in proposal:
        a, b = original.split("\n"), proposal.split("\n")
        out = list(difflib.unified_diff(a, b, fromfile=f"a/{path}", tofile=f"b/{path}", lineterm="", n=0))
        return "\n".join(f"@@ -{line} +{line} @@" if s_.startswith("@@") else s_ for s_ in out)
    i = 0
    while i < min(len(original), len(proposal)) and original[i] == proposal[i]:
        i += 1
    j = 0
    while (j < min(len(original), len(proposal)) - i
           and original[len(original) - 1 - j] == proposal[len(proposal) - 1 - j]):
        j += 1
    ctx = 40
    lo = max(0, i - ctx)
    pre = ("…" if lo > 0 else "") + original[lo:i]
    old_mid = original[i: len(original) - j]
    new_mid = proposal[i: len(proposal) - j]
    post = original[len(original) - j: len(original) - j + ctx] + ("…" if len(original) - j + ctx < len(original) else "")
    return f"--- a/{path}:{line}\n+++ b/{path}:{line}\n-{pre}{old_mid}{post}\n+{pre}{new_mid}{post}"


_AGENT_SECTIONS = ("## House style edits", "## Codex round", "## Decisions")


def _agent_sections(existing: str) -> dict[str, str]:
    """The agent-owned section bodies of an existing report, so a second
    `apply` refreshes the deterministic sections without erasing the house
    pass, the Codex dispositions or the decisions already recorded."""
    out: dict[str, str] = {}
    for head in _AGENT_SECTIONS:
        m = re.search(re.escape(head) + r"\n(.*?)(?=\n## |\Z)", existing, re.S)
        if m and m.group(1).strip() and not m.group(1).strip().startswith("_("):
            out[head] = m.group(1).rstrip("\n")
    return out


def write_report(path: Path, *, doc: dict, main_tex: Path, violations: list[Violation],
                 applied: int, compile_result: dict, house_items: list[dict],
                 candidates: list[tuple[dict, str, int, str]]) -> None:
    facts = doc["facts"]
    kept = _agent_sections(path.read_text(encoding="utf-8")) if path.is_file() else {}
    cap = page_cap(facts, main_tex)
    cap_note = f"cap {cap}: {doc['journal']} states it" if cap else f"{doc['journal']} states no page cap"
    appendix_title = (facts.get("structure") or {}).get("appendix_title", "appendix")
    L: list[str] = []
    L.append(f"# Journal conversion — {doc['name']} ({doc['journal']}, accepted-paper format)")
    L.append("")
    L.append(f"Manuscript: `{main_tex}`  ")
    L.append(f"Generated by `journal_format.py` on {time.strftime('%Y-%m-%d %H:%M')}; {applied} mechanical fix(es) applied.  ")
    L.append(f"Facts: {provenance_note(doc['journal'])}  ")
    L.append("")
    L.append("## Build")
    L.append("")
    L.append(f"- compile: {'OK' if compile_result['ok'] else 'FAILED'} (latexmk rc {compile_result['rc']}, {compile_result.get('seconds', '?')}s)")
    mp, tp = compile_result.get("main_pages", 0), compile_result.get("pages", 0)
    L.append(f"- pages: **{mp} main text** ({cap_note}{' — OVER' if cap and mp > cap else ''}); "
             f"{tp} total including the {appendix_title}")
    ov = [b for b in compile_result["boxes"] if b["kind"] == "Overfull"]
    un = [b for b in compile_result["boxes"] if b["kind"] == "Underfull"]
    L.append(f"- boxes: {len(ov)} overfull, {len(un)} underfull")
    for e in compile_result["errors"]:
        L.append(f"- ERROR: `{e}`")
    for u in compile_result.get("undefined_refs") or []:
        L.append(f"- undefined reference: `{u}`")
    for u in compile_result.get("undefined_citations") or []:
        L.append(f"- undefined citation: `{u}`")
    if ov or un:
        L.append("")
        L.append("| kind | box | amount | lines |")
        L.append("|---|---|---|---|")
        for b in sorted(compile_result["boxes"], key=lambda b: (b["kind"] != "Overfull", -_pt(b["amount"]))):
            L.append(f"| {b['kind']} | {b['box']} | {b['amount']} | {b['lines']} |")
    L.append("")
    blocks = [v for v in violations if v.severity == "block"]
    warns = [v for v in violations if v.severity != "block"]
    L.append(f"## Remaining facts — {len(blocks)} blocking, {len(warns)} advisory")
    L.append("")
    for v in violations:
        loc = f"`{v.file}:{v.line}`" if v.line else f"`{v.file}`"
        item = f"- {loc} — `{v.rule}`: {v.message}"
        if v.proposal and v.original and v.proposal != v.original and "\n" not in v.original:
            item += "\n"
            item += "\n  ```diff\n" + "\n".join("  " + s for s in _diff(v.original, v.proposal, v.file, v.line).split("\n")) + "\n  ```"
        L.append(item)
    L.append("")
    L.append("## House pass")
    L.append("")
    L.append("Worked by the agent in the source; record the edit count per item below.")
    L.append("")
    for item in house_items:
        hits = [c for c in candidates if c[0] is item]
        L.append(f"- **{item['id']}** — {item['rule']}"
                 + (f" ({len(hits)} candidate line(s))" if item.get("locate") else " (whole prose)"))
        if item.get("example"):
            L.append(f"  - example: `{item['example']['before']}` -> `{item['example']['after']}`")
        for _, f, ln, prev in hits[:20]:
            L.append(f"  - `{f}:{ln}`: {prev}")
        L.append("  - edits applied: ")
    L.append("")
    L.append("## House style edits")
    L.append("")
    L.append(kept.get("## House style edits", "_(the agent fills this: per-item edit counts and notable rewrites)_"))
    L.append("")
    L.append("## Codex round")
    L.append("")
    L.append(kept.get("## Codex round", "_(the agent fills this after `journal_format.py codex`: findings applied and declined, with reasons)_"))
    L.append("")
    L.append("## Decisions")
    L.append("")
    L.append(kept.get("## Decisions", "_(what no rule can decide: page overrun, abstract cut, any compile error that survived the bounded recompiles)_"))
    L.append("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def default_report_path(main_tex: Path, code: str) -> Path:
    root = main_tex.parent.parent if main_tex.parent.name == "draft" else main_tex.parent
    return root / "docs" / "submission" / f"latex-{code.lower()}.md"


# ---------------------------------------------------------------------------
# one bounded Codex round (the codex verb)
# ---------------------------------------------------------------------------

def codex_review(main_tex: Path, doc: dict, timeout: int = 1500) -> str:
    """Exactly one `codex exec` over a DISPOSABLE copy of the manuscript
    directory; prints a JSON list of findings (or the reason it did not run)."""
    if not shutil.which("codex"):
        return json.dumps({"error": "codex CLI not found on PATH"})
    inv = {"model": "gpt-6-astra", "reasoning_effort": "high"}
    pin = Path.home() / ".claude" / "plugins" / "gan" / "references" / "codex_invocation.json"
    if pin.is_file():
        try:
            p = json.loads(pin.read_text(encoding="utf-8"))
            inv["model"] = p.get("model") or inv["model"]
            inv["reasoning_effort"] = (p.get("effort") or p.get("reasoning_effort")
                                       or p.get("model_reasoning_effort") or inv["reasoning_effort"])
        except (OSError, ValueError):
            pass
    facts = doc["facts"]
    house = [{"id": h["id"], "rule": h["rule"]} for h in doc["house"]]
    with tempfile.TemporaryDirectory(prefix="journal-format-codex-") as td:
        work = Path(td) / "paper"
        shutil.copytree(main_tex.parent, work, ignore=shutil.ignore_patterns("*.pdf", "*.synctex.gz", "*.aux", "*.log", ".git"))
        prompt = f"""You are an independent house-style reviewer. ONE round: report findings, do not edit files, do not ask questions.

Manuscript directory: {work} (a disposable copy). Main file: {main_tex.name}. Target journal: {doc['name']} ({doc['journal']}).

The journal's stated facts (the deterministic engine already enforces these; do NOT repeat them):
{json.dumps(facts, indent=1, default=str)}

The journal's house rules (apply THESE — find every violation you can):
{json.dumps(house, indent=1)}

Read the manuscript in full and report EVERY house-rule violation plus anything a copy editor at this journal would flag. Respond with ONLY a JSON array, each element {{"file": "...", "line": N, "house_id": "...", "before": "the offending text verbatim", "after": "the exact replacement"}}. `file` is relative to the manuscript directory. No prose outside the JSON array."""
        pf = Path(td) / "prompt.md"
        pf.write_text(prompt, encoding="utf-8")
        cmd = ["codex", "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox",
               "-m", inv["model"], "-c", f"model_reasoning_effort={inv['reasoning_effort']}", "-"]
        try:
            with pf.open("r", encoding="utf-8") as fh:
                proc = subprocess.run(cmd, stdin=fh, capture_output=True, text=True, timeout=timeout, cwd=str(work))
        except subprocess.TimeoutExpired:
            return json.dumps({"error": f"codex round exceeded the {timeout}s bound and was stopped"})
        except OSError as exc:
            return json.dumps({"error": f"codex could not be started: {exc}"})
        out = (proc.stdout or "").strip()
        parts = re.split(r"(?m)^codex\s*$", out)
        final = (parts[-1] if len(parts) > 1 else out).strip()
        m = re.search(r"\[.*\]", final, re.S)
        if m and proc.returncode == 0:
            try:
                findings = json.loads(m.group(0))
                if isinstance(findings, list) and all(
                        isinstance(f, dict) and {"file", "line", "house_id", "before", "after"} <= f.keys()
                        for f in findings):
                    return json.dumps(findings, ensure_ascii=False)
                return json.dumps({"error": "codex findings do not match {file, line, house_id, before, after}",
                                   "raw": final[-2000:]}, ensure_ascii=False)
            except ValueError:
                pass
        return json.dumps({"error": f"codex returned no parsable JSON (rc {proc.returncode})",
                           "raw": final[-2000:]}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# verbs
# ---------------------------------------------------------------------------

def _require_journal(args) -> str:
    code = normalize_journal(args.journal)
    if not code:
        print("--journal is required (the project's recorded target journal; never inferred from the manuscript). "
              f"Known journals: {', '.join(available_journals())}", file=sys.stderr)
        raise SystemExit(2)
    try:
        journal_file(code)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
    return code


def cmd_check(args) -> int:
    main_tex = Path(args.main_tex)
    if not main_tex.is_file():
        print(f"{main_tex}: no such file", file=sys.stderr)
        return 2
    code = _require_journal(args)
    doc, violations = run_checks(main_tex, code)
    candidates = house_candidates(main_tex, doc["house"])
    if args.json:
        print(json.dumps({"journal": doc["journal"], "name": doc["name"],
                          "provenance": provenance_note(code),
                          "violations": [v.public() for v in violations],
                          "house_candidates": [{"id": c[0]["id"], "file": c[1], "line": c[2], "text": c[3]}
                                               for c in candidates]}, indent=2, ensure_ascii=False))
    else:
        for v in violations:
            loc = f"{v.file}:{v.line}" if v.line else v.file
            print(f"{loc}: [{v.rule}] {v.message}")
        for item, f, ln, prev in candidates:
            print(f"{f}:{ln}: [house.{item['id']}] candidate: {prev}")
        blocks = sum(1 for v in violations if v.severity == "block")
        print(f"{doc['journal']} ({doc['name']}, accepted-paper format): {len(violations)} violation(s) ({blocks} block, "
              f"{len(violations) - blocks} warn), {len(candidates)} house candidate line(s)")
        print(f"facts: {provenance_note(code)}")
    return 1 if any(v.severity == "block" for v in violations) else 0


def cmd_apply(args) -> int:
    main_tex = Path(args.main_tex)
    if not main_tex.is_file():
        print(f"{main_tex}: no such file", file=sys.stderr)
        return 2
    code = _require_journal(args)
    doc = load_journal(code)
    cit = doc["facts"].get("citations") or {}
    bst = cit.get("bst")
    root = main_tex.resolve().parent
    needed = ([f"{bst}.bst"] if bst else []) + list(cit.get("bst_companions") or [])
    missing = [f for f in needed if not (root / f).is_file()]
    if missing:
        # hard stop BEFORE any edit or compile: the reference list cannot be built
        print(f"{', '.join(missing)} not beside {main_tex.name} — copy the journal's bibliography files in first; "
              f"nothing was changed", file=sys.stderr)
        return 2
    candidates = house_candidates(main_tex, doc["house"])
    applied = apply_all(main_tex, code)
    appendix_title = (doc["facts"].get("structure") or {}).get("appendix_title")
    compile_result = compile_once(main_tex, appendix_title=appendix_title)
    if not compile_result["ok"] and not compile_result["errors"]:
        tail = [ln.strip() for ln in (compile_result["log"] or "").splitlines() if ln.strip()][-3:]
        compile_result["errors"] = [f"latexmk exited {compile_result['rc']} with no parsed LaTeX error "
                                    f"— inspect the log (often bibtex/the .bst): {' | '.join(tail)}"]
    _, remaining = run_checks(main_tex, code)     # with the log + PDF now available
    blocks = [v for v in remaining if v.severity == "block"]
    ov = sum(1 for b in compile_result["boxes"] if b["kind"] == "Overfull")
    un = sum(1 for b in compile_result["boxes"] if b["kind"] == "Underfull")
    cap = page_cap(doc["facts"], main_tex)
    print(f"apply: fixed={applied} remaining={len(remaining)} (block={len(blocks)}, "
          f"warn={len(remaining) - len(blocks)}) compile={'ok' if compile_result['ok'] else 'FAIL'} "
          f"errors={len(compile_result['errors'])} overfull={ov} underfull={un} "
          f"pages={compile_result['main_pages']}/{compile_result['pages']}"
          + (f" (cap {cap}: {code} states it)" if cap else f" ({code} states no page cap)"))
    report = Path(args.report) if args.report else default_report_path(main_tex, code)
    report.parent.mkdir(parents=True, exist_ok=True)
    write_report(report, doc=doc, main_tex=main_tex, violations=remaining, applied=applied,
                 compile_result=compile_result, house_items=doc["house"], candidates=candidates)
    print(f"report: {report}")
    if not compile_result["ok"] and compile_result["errors"]:
        print(f"compile error: {compile_result['errors'][0]}", file=sys.stderr)
        return 2
    return 1 if blocks else 0


def cmd_codex(args) -> int:
    main_tex = Path(args.main_tex)
    if not main_tex.is_file():
        print(f"{main_tex}: no such file", file=sys.stderr)
        return 2
    code = _require_journal(args)
    doc = load_journal(code)
    out = codex_review(main_tex, doc, timeout=args.timeout)
    print(out)
    return 1 if out.startswith("{") else 0   # an error object, not a findings list


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="verb", required=True)
    for name in ("check", "apply", "codex"):
        sp = sub.add_parser(name)
        sp.add_argument("main_tex")
        sp.add_argument("--journal", required=True,
                        help="journal code or alias (REQUIRED — the project's recorded target journal, never inferred)")
        if name == "check":
            sp.add_argument("--json", action="store_true")
        if name == "apply":
            sp.add_argument("--report", help="report path (default: docs/submission/latex-<code>.md)")
        if name == "codex":
            sp.add_argument("--timeout", type=int, default=1500)
    args = ap.parse_args(argv)
    return {"check": cmd_check, "apply": cmd_apply, "codex": cmd_codex}[args.verb](args)


if __name__ == "__main__":
    sys.exit(main())
