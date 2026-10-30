#!/usr/bin/env python3
"""Regression suite for the latex skill — pytest fails if any of these regress.

Runs under pytest and as a plain script (`python3 tests/test_latex.py`).

fixtures/wp/                     a minimal project in the working-paper layout
    (the assets newproj copies) — the ONE format every draft keeps; the
    validator must pass it, and journal_format's fix pass converts it to a
    journal's accepted-paper format.
fixtures/natbib_year_collapse/   the natbib year-collapse: a key repeated inside
    one \\citet after a consolidation, and two entries sharing authors + year.
    Detected at the source (duplicate keys, auto-fixed), in the compile log and
    in the rendered PDF text ('(2003,?)' / '(2003, 0)') when pdflatex + bibtex
    are available.
fixtures/banned/                 one file per pattern: parenthetical statistics
    in prose (a JFQA house item), the wrong document class / margins / spacing /
    citation form / appendix title / equation-reference form under JFQA,
    \\hline in a table, a footnote inside a float.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

try:
    import pytest
except ImportError:  # the plain runner (python3 tests/test_latex.py) needs no pytest
    pytest = None


class _Skip(Exception):
    pass


def _skip(msg: str):
    raise (pytest.skip.Exception if pytest else _Skip)(msg)  # type: ignore[union-attr]


_SKIPS: tuple = (_Skip,) + ((pytest.skip.Exception,) if pytest else ())  # type: ignore[union-attr]


@contextmanager
def _raises(exc_type, match: str):
    try:
        yield
    except exc_type as exc:
        assert match in str(exc), f"{exc_type.__name__} raised without {match!r}: {exc}"
        return
    raise AssertionError(f"{exc_type.__name__} not raised")

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "draft" / "scripts"
FIX = ROOT / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import journal_format as jf  # noqa: E402
import journal_rules  # noqa: E402
import validate_latex  # noqa: E402

_HAVE_TEX = all(shutil.which(x) for x in ("pdflatex", "bibtex", "pdftotext"))


def _copy(src: Path, td: str) -> Path:
    dst = Path(td) / src.name
    shutil.copy(src, dst)
    for sib in src.parent.iterdir():
        if sib.suffix in (".bib", ".bst") and not (Path(td) / sib.name).exists():
            shutil.copy(sib, Path(td) / sib.name)
    return dst


def _rules(vs) -> set[str]:
    return {v.rule for v in vs}


def _check(path: Path, journal: str):
    _, vs = jf.run_checks(path, journal)
    return vs


def _compile(tex: Path) -> None:
    cwd = str(tex.parent)
    for cmd in (["pdflatex", "-interaction=nonstopmode", tex.name], ["bibtex", tex.stem],
                ["pdflatex", "-interaction=nonstopmode", tex.name], ["pdflatex", "-interaction=nonstopmode", tex.name]):
        subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)


# ---------------------------------------------------------------------------
# journal files
# ---------------------------------------------------------------------------

def test_every_journal_file_loads_and_is_facts_only():
    want = {"AER", "QJE", "JPE", "RES", "Econometrica", "JF", "RFS", "JFE", "RF", "JFQA", "MS"}
    assert want <= set(journal_rules.available_journals()), journal_rules.available_journals()
    for j in want:
        doc = journal_rules.load_journal(j)
        assert set(doc["facts"]) == {"layout", "length", "structure", "citations"}
        assert isinstance(doc["house"], list)
        for item in doc["house"]:
            assert item["id"] and item["rule"]
        assert isinstance(doc["verified"], dict) and (not doc["verified"] or isinstance(doc["verified"]["date"], str))
        # a file whose sources record a bot-walled fetch carries no `verified` block
        srcs = " ".join(doc["sources"]).lower()
        if "bot-walled" in srcs and "verified" not in srcs.split("bot-walled")[0]:
            assert not doc["verified"], f"{j}: a carried file must not claim verification"
    assert journal_rules.load_journal("ecma")["journal"] == "Econometrica"
    assert journal_rules.load_journal("jfqa")["facts"]["citations"]["bst"] == "JFQA"
    assert journal_rules.load_journal("MS")["facts"]["length"]["pages_by_spacing"] == {"onehalf": 32, "double": 47}


def test_provenance_names_verification_and_nothing_is_defaulted():
    """The provenance line says whether a file's facts were VERIFIED against
    the journal's own guidelines (the `verified:` block) or merely carried;
    `check` and the report print it. No working-paper default ever stands
    in for an unstated fact — an unstated fact is unchecked."""
    assert "verified 2026-09-20" in journal_rules.provenance_note("JF")
    silent = next(j for j in journal_rules.available_journals() if not journal_rules.load_journal(j)["facts"]["layout"])
    assert "NEVER verified" in journal_rules.provenance_note(silent)
    assert not hasattr(journal_rules, "effective_facts") and not hasattr(journal_rules, "WP_FACTS")
    with _raises(ValueError, "`verified` must be"):
        journal_rules._validate({"journal": "X", "verified": {"date": "yesterday", "sections": ["layout"]}}, Path("x.yaml"))
    with _raises(ValueError, "`verified` must be"):
        journal_rules._validate({"journal": "X", "verified": {"date": "2026-01-01", "sections": ["prose"]}}, Path("x.yaml"))
    with _raises(ValueError, "`verified` must be"):
        journal_rules._validate({"journal": "X", "verified": {"date": "2026-01-01", "sections": [None]}}, Path("x.yaml"))
    with _raises(ValueError, "`verified` must be"):
        journal_rules._validate({"journal": "X", "verified": {"date": "2026-01-01", "sections": ["layout"], "by": "me"}}, Path("x.yaml"))
    r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "check", "--journal", silent, "--json", str(FIX / "wp" / "main.tex")],
                       capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert "NEVER verified" in out["provenance"] and "stage" not in out, r.stdout
    assert "layout." not in json.dumps(out["violations"]), "an unstated layout fact is never checked"
    r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "check", "--journal", silent, str(FIX / "wp" / "main.tex")],
                       capture_output=True, text=True)
    assert "facts: " in r.stdout and "NEVER verified" in r.stdout and "accepted-paper format" in r.stdout, r.stdout


def test_journal_file_is_the_accepted_paper_format():
    """A journal file states the ACCEPTED-paper format and nothing else: JF
    publishes double-spaced, so its file says `double`; there is no
    submission stage, no `accepted:` override block and no --accepted flag."""
    assert journal_rules.load_journal("JF")["facts"]["layout"]["spacing"] == "double"
    with _raises(ValueError, "unknown top-level key 'accepted'"):
        journal_rules._validate({"journal": "X", "accepted": {"layout": {"spacing": "double"}}}, Path("x.yaml"))
    r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "check", "--journal", "jf", "--accepted", str(FIX / "wp" / "main.tex")],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "--accepted" in r.stderr, r.stderr
    assert jf.default_report_path(FIX / "wp" / "main.tex", "JF").name == "latex-jf.md"


def test_unknown_key_is_rejected_at_load():
    with _raises(ValueError, "unknown key layout.papers"):
        journal_rules._validate({"journal": "X", "layout": {"papers": "a4paper"}}, Path("x.yaml"))
    with _raises(ValueError, "unknown top-level key"):
        journal_rules._validate({"journal": "X", "rules": []}, Path("x.yaml"))
    with _raises(FileNotFoundError, "known:"):
        journal_rules.load_journal("bogus")


# ---------------------------------------------------------------------------
# the wp validator
# ---------------------------------------------------------------------------

def test_wp_fixture_passes_the_wp_validator():
    issues = [i for i in validate_latex.validate(FIX / "wp" / "main.tex") if not i.startswith("WARNING")]
    assert issues == [], issues


def test_wp_validator_flags_a_journal_layout():
    """A JFQA-shaped draft is NOT a working paper: the validator must say so."""
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        main = Path(td) / "wp" / "main.tex"
        main.write_text(main.read_text().replace("\\documentclass[a4paper, 12pt]{article}",
                                                 "\\documentclass[letterpaper, 12pt]{article}"))
        issues = validate_latex.validate(main)
        assert any("letterpaper" in i or "Document class" in i for i in issues), issues


def test_validator_holds_the_working_paper_layout_only():
    """`validate(main)` has no journal path: the wp fixture passes bare, each
    layout deviation fails, `--journal` is gone, and a JF-converted draft
    (double-spaced) FAILS the working-paper validator — the accepted format
    is never a drafting format."""
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        main = Path(td) / "wp" / "main.tex"
        pristine = main.read_text()
        assert [i for i in validate_latex.validate(main) if not i.startswith("WARNING")] == []
        r = subprocess.run([sys.executable, str(SCRIPTS / "validate_latex.py"), "--journal", "jf", str(main)],
                           capture_output=True, text=True)
        assert r.returncode == 2 and "--journal" in r.stderr, r.stderr
        for old, new in (("12pt", "11pt"), ("a4paper", "letterpaper"), ("\\onehalfspacing", "\\doublespacing")):
            assert old in pristine, old
            main.write_text(pristine.replace(old, new, 1))
            assert [i for i in validate_latex.validate(main) if not i.startswith("WARNING")], (old, new)
        main.write_text(pristine.replace("\\input{style}", "\\input{style}\n\\geometry{margin=0.5in}", 1))
        assert any("override" in i for i in validate_latex.validate(main)), "a \\geometry override defeats the cap calibration"
        main.write_text(pristine)
        assert jf.apply_all(main, "JF") >= 1
        issues = [i for i in validate_latex.validate(main) if not i.startswith("WARNING")]
        assert any("doublespacing" in i for i in issues), issues
        # the structure checks are layout-independent
        main.write_text(pristine.replace("\\input{sections/introduction}", ""))
        assert any("introduction" in i for i in validate_latex.validate(main))


def test_appendix_pages_is_a_journal_fact():
    assert journal_rules.load_journal("Econometrica")["facts"]["length"]["appendix_pages"] == 25
    with _raises(ValueError, "unknown key length.appendix"):
        journal_rules._validate({"journal": "X", "length": {"appendix": 25}}, Path("x.yaml"))


def test_unstated_facts_are_never_checked():
    """A journal file's facts are what `check`/`apply` consume — nothing is
    defaulted in: a journal stating no layout raises no layout violation on
    any manuscript and never touches its spacing; its page cap is None."""
    silent = next(j for j in journal_rules.available_journals() if not journal_rules.load_journal(j)["facts"]["layout"])
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        main = Path(td) / "wp" / "main.tex"
        main.write_text(main.read_text().replace("\\onehalfspacing", "\\doublespacing", 1))
        assert not any(r.startswith("layout.") for r in _rules(_check(main, silent))), sorted(_rules(_check(main, silent)))
        assert jf.page_cap(journal_rules.load_journal(silent)["facts"], main) is None
        jf.apply_all(main, silent)
        assert "\\doublespacing" in main.read_text(), "apply never touches an unstated fact"
    ms = journal_rules.load_journal("MS")["facts"]["length"]
    assert "pages" not in ms and ms["pages_by_spacing"], "the journal's own spacing-keyed cap stands"


def test_also_fragments_are_fixed_before_they_are_wired_in():
    """`apply_all(..., also=)` covers a fragment main.tex does not input yet
    (an appendix a project has unwired): its heading carries the journal's
    appendix title, so re-wiring it later passes at once."""
    code = next(j for j in journal_rules.available_journals()
                if journal_rules.load_journal(j)["facts"]["structure"].get("appendix_title")
                not in (None, "Internet Appendix"))
    title = journal_rules.load_journal(code)["facts"]["structure"]["appendix_title"]
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        root = Path(td) / "wp"
        main, appendix = root / "main.tex", root / "sections" / "appendix.tex"
        wired = main.read_text()
        assert "\n\\input{sections/appendix}" in wired, "the fixture ships the appendix wired in (one pdf)"
        main.write_text(wired.replace("\\appendix\n\\input{sections/appendix}",
                                      "% \\appendix\n% \\input{sections/appendix}"))
        for name in ("JFQA.bst", "babelbst.tex", "englbst.tex"):
            (root / name).write_text("% stub\n")
        jf.apply_all(main, code)
        assert "Internet Appendix for" in appendix.read_text(), "a fragment the graph does not reach is untouched"
        jf.apply_all(main, code, also=sorted((root / "sections").glob("*.tex")))
        assert f"{title} for" in appendix.read_text() and "Internet Appendix for" not in appendix.read_text()
        main.write_text(main.read_text().replace("% \\appendix", "\\appendix")
                        .replace("% \\input{sections/appendix}", "\\input{sections/appendix}"))
        assert "structure.appendix_title" not in _rules(_check(main, code))
        assert jf.apply_all(main, code, also=sorted((root / "sections").glob("*.tex"))) == 0, "idempotent"


def test_bare_validator_keeps_the_always_on_citation_checks():
    """A key repeated inside one citation command (the natbib year-collapse
    trigger) is a blocking issue on every draft — journal_format's always-on
    citation checks run in the bare validator, no journal facts involved."""
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        main = Path(td) / "wp" / "main.tex"
        assert not any("[citation." in i for i in validate_latex.validate(main))
        intro = Path(td) / "wp" / "sections" / "introduction.tex"
        intro.write_text(intro.read_text() + "\nAs shown by \\citet{alpha,alpha}.\n")
        out = validate_latex.validate(main)
        assert any(i.startswith("[citation.duplicate_keys]") for i in out), out


def test_missing_geometry_repair_states_no_paper_the_journal_leaves_unstated():
    """JF states margins but no paper size: the repair for a manuscript with
    no geometry line writes the four margins and nothing else (never a
    literal `None` option, which is a fatal keyval error at compile)."""
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        main = Path(td) / "wp" / "main.tex"
        style = Path(td) / "wp" / "style.tex"
        style.write_text("\n".join(l for l in style.read_text().splitlines() if "{geometry}" not in l) + "\n")
        assert "layout.margins" in _rules(_check(main, "JF"))
        assert jf.apply_all(main, "JF") >= 1
        live = main.read_text() + style.read_text()
        assert "None" not in live
        assert re.search(r"\\usepackage\[top=1.5in,bottom=1.5in,left=1in,right=1in\]\{geometry\}", live), live
        assert "layout.margins" not in _rules(_check(main, "JF"))


def test_article_class_is_structure():
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        main = Path(td) / "wp" / "main.tex"
        main.write_text(main.read_text().replace("{article}", "{report}", 1))
        assert any("{report}" in i and "{article}" in i for i in validate_latex.validate(main))
        assert "layout.documentclass" not in _rules(_check(main, "JF")), "the journal engine governs the options only"


# ---------------------------------------------------------------------------
# the natbib year-collapse (always on)
# ---------------------------------------------------------------------------

def test_duplicate_cite_key_is_detected_and_auto_fixed():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "natbib_year_collapse" / "collapse.tex", td)
        vs = _check(tex, "JFQA")
        dup = [v for v in vs if v.rule == "citation.duplicate_keys"]
        assert len(dup) == 1 and dup[0].line == 15 and "kamstra2003winter" in dup[0].message, dup
        assert dup[0].auto_fixable and dup[0].proposal.count("kamstra2003winter") == 1
        assert jf.apply_fixes(tex, dup) == 1
        assert "citation.duplicate_keys" not in _rules(_check(tex, "JFQA"))
        assert "\\citet{kamstra2003winter,kamstra2015seasonal}" in tex.read_text()


def test_year_collapse_surfaces_in_log_and_pdf_after_compile():
    if not _HAVE_TEX:
        _skip("pdflatex/bibtex/pdftotext unavailable")
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "natbib_year_collapse" / "collapse.tex", td)
        _compile(tex)
        assert tex.with_suffix(".pdf").is_file(), "fixture must compile"
        rules = _rules(_check(tex, "JF"))
        assert "citation.natbib_collapse_log" in rules and "citation.natbib_collapse_pdf" in rules, rules
        vs = _check(tex, "JF")
        assert jf.apply_fixes(tex, [v for v in vs if v.rule == "citation.duplicate_keys"]) == 1
        _compile(tex)
        assert not {"citation.natbib_collapse_log", "citation.natbib_collapse_pdf",
                    "citation.duplicate_keys"} & _rules(_check(tex, "JF"))


# ---------------------------------------------------------------------------
# JFQA facts: detect, apply, idempotence, owning file
# ---------------------------------------------------------------------------

_JFQA_FACT_IDS = ("layout.documentclass", "layout.margins", "layout.spacing", "layout.font",
                  "layout.preamble", "layout.body", "structure.numbering", "structure.appendix_title",
                  "citations.bst", "citations.form", "citations.equation_ref")


def test_jfqa_facts_detect_apply_and_are_idempotent():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        (Path(td) / "JFQA.bst").write_text("% stub\n")
        vs = _check(tex, "JFQA")
        rules = _rules(vs)
        for rid in _JFQA_FACT_IDS:
            assert rid in rules, f"{rid} not detected: {sorted(rules)}"
        by = {v.rule: v for v in vs}
        assert by["layout.documentclass"].line == 1 and "11pt" in by["layout.documentclass"].message
        assert by["structure.appendix_title"].line == 13
        assert "\\citet{kamstra2003winter}, \\citet{kamstra2015seasonal}" in by["citations.form"].proposal
        # already-parenthesized \citep keeps its parentheses (no doubling)
        assert "((" not in by["citations.form"].proposal
        n = jf.apply_all(tex, "JFQA")
        assert n >= 10, n
        left = _rules(_check(tex, "JFQA"))
        for rid in _JFQA_FACT_IDS:
            assert rid not in left, f"{rid} still reported after apply"
        text = tex.read_text()
        assert "\\documentclass[letterpaper, 12pt, leqno]{article}" in text
        assert "top=1in,bottom=1in,left=1in,right=1in" in text
        assert "\\doublespacing" in text and "\\onehalfspacing" not in text
        assert "newtxtext" in text and "longnamesfirst" in text and "\\bibliographystyle{JFQA}" in text
        assert "Supplementary Material for" in text and "Internet Appendix for" not in text
        assert "\\renewcommand{\\thesection}{\\Roman{section}}" in text
        assert "equation~\\eqref{eq:one}" in text and "\\usepackage[tbtags]{amsmath}" in text
        assert text.count("{amsmath}") == 1, "options reconcile onto the existing load, never a second load"
        assert "\\raggedright" in text and "\\def\\doublespacing" not in text, \
            "no spacing definition in the preamble: the validator forbids it (the page cap is keyed on main.tex)"
        assert text.index("\\usepackage{setspace}") < text.index("\\usepackage{indentfirst}"), "YAML order kept"
        # the JFQA-applied draft must pass the validator's own spacing grammar
        assert not [i for i in validate_latex._scan_main_text(text)["issues"] if "line spacing" in i], validate_latex._scan_main_text(text)["issues"]
        assert any(h["id"] == "true_double_spacing" for h in journal_rules.load_journal("JFQA")["house"])
        # the house rule's prescription is admitted by the validator's grammar, and the house locate hits
        hits = [ln for item, f, ln, _ in jf.house_candidates(tex, journal_rules.load_journal("JFQA")["house"]) if item["id"] == "true_double_spacing"]
        assert hits, "the true_double_spacing locate must find the body's \\doublespacing"
        stretched = text.replace("\\doublespacing", "\\setstretch{2}", 1)
        assert validate_latex._scan_main_text(stretched)["spacing"] == "doublespacing", validate_latex._scan_main_text(stretched)["issues"]
        assert validate_latex._scan_main_text(text.replace("\\doublespacing", "\\setstretch{1.5}", 1))["spacing"] == "onehalfspacing"
        assert validate_latex._scan_main_text(text.replace("\\doublespacing", "\\setstretch{1.3}", 1))["spacing"] is None
        # a legacy definition from an earlier apply is removed by apply, never left to fail S0
        legacy = tex.read_text().replace("\\usepackage{setspace}", "\\usepackage{setspace}\n\\def\\doublespacing{\\setstretch{2}}   % legacy", 1)
        tex.write_text(legacy)
        vs = [v for v in _check(tex, "JFQA") if v.rule == "preamble.spacing_definition"]
        assert vs and vs[0].auto_fixable, [(v.rule, v.message) for v in _check(tex, "JFQA")]
        assert jf.apply_all(tex, "JFQA") >= 1 and "\\def\\doublespacing" not in tex.read_text()
        assert "(\\citet{kamstra2003winter}, \\citet{kamstra2015seasonal})" in text and "((" not in text
        # idempotent: a second pass applies nothing
        assert jf.apply_all(tex, "JFQA") == 0


def test_fixes_land_in_the_owning_file():
    """geometry/font in the preamble file that carries them, stars in tables/,
    citations in sections/ — never flattened into main.tex."""
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        root = Path(td) / "wp"
        (root / "sections" / "results.tex").write_text(
            "\\section{Results}\nSee \\citep{k2003} and Eq.~\\ref{eq:x}.\n\\begin{equation}\\label{eq:x} y=x \\end{equation}\n")
        (root / "tables" / "main_results.tex").write_text("\\begin{tabular}{lc}\n\\toprule\nx & 0.123*** \\\\\n\\bottomrule\n\\end{tabular}\n")
        (root / "JFQA.bst").write_text("% stub\n")
        main = root / "main.tex"
        jf.apply_all(main, "JFQA")
        style1, main1 = (root / "style.tex").read_text(), main.read_text()
        assert "top=1in,bottom=1in,left=1in,right=1in" in style1 and "newtxtext" in style1
        assert "top=1in" not in main1 and "newtxtext" not in main1
        # JFQA numbers exhibits in Arabic: the wp template's \Roman redefinitions leave style.tex
        assert "\\renewcommand{\\thetable}" not in style1 and "\\renewcommand{\\thefigure}" not in style1
        # the grouped amsmath load is split: the option goes to amsmath ALONE
        assert "\\usepackage[tbtags]{amsmath}" in style1 and "tbtags]{amsmath," not in style1
        assert "amssymb" in style1
        assert "(\\citet{k2003})" in (root / "sections" / "results.tex").read_text()
        assert "equation~\\eqref{eq:x}" in (root / "sections" / "results.tex").read_text()
        assert "0.123$^{***}$" in (root / "tables" / "main_results.tex").read_text()
        assert "\\documentclass[letterpaper, 12pt, leqno]{article}" in main1
        # the wp template declares the bib style in style.tex — that is the owning file
        assert "\\bibliographystyle{JFQA}" in style1 and "\\bibliographystyle" not in main1


def test_missing_bst_is_a_hard_block():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        tex.write_text(tex.read_text().replace("\\bibliographystyle{chicago}", "\\bibliographystyle{JFQA}"))
        vs = [v for v in _check(tex, "JFQA") if v.rule == "citations.bst"]
        assert vs and vs[0].severity == "block" and not vs[0].auto_fixable and "JFQA.bst" in vs[0].message


def test_jf_facts_are_the_accepted_paper_format():
    """jf.yaml records JF's accepted-paper format: the 60-page cap and the
    layout the Submission Guidelines (Rev. 2024-03-12, 1.e) state — 12pt,
    1-inch sides and 1.5-inch top/bottom, a 100-word abstract — with the
    production spacing (double, JF Style February 2017); the style guide
    supplies structure and the house list, including the unnumbered untitled
    introduction that the wp scaffold violates."""
    doc = journal_rules.load_journal("JF")
    lay, length = doc["facts"]["layout"], doc["facts"]["length"]
    assert length["pages"] == 60 and length["abstract_words"] == 100
    assert "appendix_pages" not in length, "JF caps nothing on the Internet Appendix"
    assert lay["spacing"] == "double" and lay["font_pt"] == 12
    assert lay["margins"] == {"top": "1.5in", "bottom": "1.5in", "left": "1in", "right": "1in"}
    assert any("Submission Guidelines" in s and "2024" in s for s in doc["sources"]), doc["sources"]
    ids = {h["id"] for h in doc["house"]}
    assert {"introduction_unnumbered_untitled", "reference_first_names", "production_double_spacing", "closing_summary"} <= ids
    cands = jf.house_candidates(FIX / "wp" / "main.tex", doc["house"])
    hits = {item["id"]: (f, ln) for item, f, ln, _ in cands}
    assert hits.get("introduction_unnumbered_untitled", ("",))[0] == "sections/introduction.tex", hits
    # the first-name and production-spacing items are whole-manuscript, stage-aware instructions: no locate
    assert {"reference_first_names", "production_double_spacing"}.isdisjoint(hits), hits


def test_jf_acceptance_converts_a_wp_draft():
    """JF's ACCEPTED-paper format (Roman/A numbering, Roman tables + Arabic
    figures, the (Tufano (1996)) citation form, double spacing) is NOT the
    working-paper format: converting a wp draft to JF changes all of it."""
    vs = _check(FIX / "wp" / "main.tex", "JF")
    rules = _rules(vs)
    assert {"structure.numbering", "structure.exhibit_numbering", "layout.spacing"} <= rules, sorted(rules)
    by = {v.rule: v for v in vs}
    assert by["structure.exhibit_numbering"].file == "style.tex" and "figure" in by["structure.exhibit_numbering"].message


# ---------------------------------------------------------------------------
# house items and the always-on table conventions
# ---------------------------------------------------------------------------

def test_house_candidates_locate_parenthetical_stats_in_prose_only():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "paren_stats.tex", td)
        doc = journal_rules.load_journal("JFQA")
        hits = [(f, ln) for item, f, ln, _ in jf.house_candidates(tex, doc["house"]) if item["id"] == "parenthetical_stats"]
        assert [ln for _, ln in hits] == [5], hits   # not the footnote (6), not the caption (8)


def test_table_conventions_always_on():
    with tempfile.TemporaryDirectory() as td:
        tables = Path(td) / "tables"
        tables.mkdir()
        shutil.copy(FIX / "banned" / "table_hline.tex", tables / "reg.tex")
        main = Path(td) / "main.tex"
        main.write_text("\\documentclass[letterpaper, 12pt, leqno]{article}\n\\usepackage[letterpaper,margin=1in]{geometry}\n"
                        "\\begin{document}\n\\doublespacing\n\\begin{table}\\caption{T}\\input{tables/reg}\\end{table}\n\\end{document}\n")
        vs = _check(main, "JFQA")
        assert "tables.booktabs" in _rules(vs)
        stars = [v for v in vs if v.rule == "citations.stars"]
        assert stars and stars[0].auto_fixable and "$^{***}$" in stars[0].proposal
        jf.apply_all(main, "JFQA")
        assert "0.123$^{***}$" in (tables / "reg.tex").read_text()
        assert "citations.stars" not in _rules(_check(main, "JFQA"))
        # booktabs is journal-agnostic
        assert "tables.booktabs" in _rules(_check(main, "JF"))


def test_footnote_inside_float_always_on():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "float_footnote.tex", td)
        vs = [v for v in _check(tex, "JF") if v.rule == "tables.no_footnote_in_float"]
        assert vs and vs[0].line == 6


def test_wp_to_jfqa_conversion_compiles():
    """The real thing: a wp scaffold (grouped amsmath load, Roman exhibits,
    1.5 spacing) converted to JFQA must COMPILE — the grouped-import split and
    the exhibit renumbering are exercised on the shipped template."""
    if not _HAVE_TEX or not shutil.which("latexmk"):
        _skip("latexmk/pdflatex/bibtex/pdftotext unavailable")
    bst = Path.home() / "proj" / "risk-aversion" / "draft" / "JFQA.bst"
    if not bst.is_file():
        _skip("JFQA.bst not available locally")
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        root = Path(td) / "wp"
        for name in ("JFQA.bst", "babelbst.tex", "englbst.tex"):
            shutil.copy(bst.parent / name, root / name)
        (root / "tables" / "main_results.tex").write_text("\\begin{tabular}{lc}\n\\toprule\nx & 0.123 \\\\\n\\bottomrule\n\\end{tabular}\n")
        for name in ("panel_a", "panel_b", "extended_results", "ia_robustness"):
            (root / "tables" / f"{name}.tex").write_text("\\begin{tabular}{lc}\n\\toprule\nx & 1 \\\\\n\\bottomrule\n\\end{tabular}\n")
        main = root / "main.tex"
        # drop the figure wrappers (no PDFs in the fixture); the Internet
        # Appendix stays live — its one figure becomes a rule of the same width
        main.write_text(main.read_text().replace("\\input{sections/figures}", "% figures dropped in the fixture"))
        appendix = root / "sections" / "appendix.tex"
        appendix.write_text(appendix.read_text().replace(
            "\\includegraphics[width=.8\\textwidth]{figures/ia_results.pdf}", "\\rule{.8\\textwidth}{3cm}"))
        r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "apply", "--journal", "jfqa", str(main)],
                           capture_output=True, text=True, timeout=600)
        assert "compile=ok" in r.stdout, r.stdout + r.stderr
        assert (root / "main.pdf").is_file()
        r2 = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "apply", "--journal", "jfqa", str(main)],
                            capture_output=True, text=True, timeout=600)
        assert "fixed=0" in r2.stdout and "compile=ok" in r2.stdout, r2.stdout


def test_style_asset_fills_pdf_metadata():
    """The shipped style fills the PDF's Title/Author from \\title/\\author
    (hyperref pdfusetitle) — the gan pdf_metadata gate requires both — and an
    explicit \\hypersetup still wins. Bibliography-independent: two pdflatex
    passes, no bibtex."""
    if not (shutil.which("pdflatex") and shutil.which("pdfinfo")):
        _skip("pdflatex/pdfinfo unavailable")
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(FIX / "wp", Path(td) / "wp")
        root = Path(td) / "wp"
        for name in ("main_results", "panel_a", "panel_b", "extended_results", "ia_robustness"):
            (root / "tables" / f"{name}.tex").write_text("\\begin{tabular}{lc}\n\\toprule\nx & 1 \\\\\n\\bottomrule\n\\end{tabular}\n")
        main = root / "main.tex"
        src = main.read_text().replace("\\input{sections/figures}", "% figures dropped in the fixture")
        appendix = root / "sections" / "appendix.tex"
        appendix.write_text(appendix.read_text().replace(
            "\\includegraphics[width=.8\\textwidth]{figures/ia_results.pdf}", "\\rule{.8\\textwidth}{3cm}"))
        title = re.search(r"\\newcommand\{\\Title\}\{(.+?)\}\n", src).group(1)
        author = re.search(r"\\newcommand\{\\Author\}\{(.+?)\}\n", src).group(1)

        def compile_and_info(text: str) -> dict:
            main.write_text(text)
            for _ in range(2):
                r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"],
                                   cwd=root, capture_output=True, text=True, timeout=300)
            assert (root / "main.pdf").is_file(), r.stdout[-1500:]
            info = subprocess.run(["pdfinfo", "main.pdf"], cwd=root, capture_output=True, text=True).stdout
            return {k.strip(): v.strip() for k, v in (ln.split(":", 1) for ln in info.splitlines() if ":" in ln)}

        meta = compile_and_info(src)
        assert meta.get("Title") == title, meta
        assert meta.get("Author") == author, meta
        meta = compile_and_info(src.replace("\\input{style}", "\\input{style}\n\\hypersetup{pdftitle={Override Title}}", 1))
        assert meta.get("Title") == "Override Title" and meta.get("Author") == author, "an explicit \\hypersetup must win"


def test_partial_facts_never_crash():
    """A journal stating only a paper size (or only a font size, or only class
    options) checks THAT and leaves the rest untouched."""
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        for facts in ({"layout": {"paper": "letterpaper"}}, {"layout": {"font_pt": 12}},
                      {"layout": {"class_options": ["leqno"]}}):
            fmt = jf.checkable_facts(facts)
            vs = jf.check_documentclass(jf.Manuscript(tex), fmt, {"id": "layout.documentclass", "severity": "block", "auto_fixable": True})
            assert len(vs) == 1, (facts, vs)
        vs = jf.check_documentclass(jf.Manuscript(tex), jf.checkable_facts({"layout": {"paper": "a4paper"}}),
                                    {"id": "layout.documentclass", "severity": "block", "auto_fixable": True})
        assert vs == [], "a4paper 11pt with paper-only facts states no paper violation"


def test_ms_page_cap_follows_the_declared_spacing():
    facts = journal_rules.load_journal("MS")["facts"]
    with tempfile.TemporaryDirectory() as td:
        tex = Path(td) / "main.tex"
        tex.write_text("\\documentclass{article}\n\\begin{document}\n\\onehalfspacing\nx\n\\end{document}\n")
        assert jf.page_cap(facts, tex) == 32
        tex.write_text("\\documentclass{article}\n\\begin{document}\n\\doublespacing\nx\n\\end{document}\n")
        assert jf.page_cap(facts, tex) == 47
        tex.write_text("\\documentclass{article}\n\\begin{document}\n\\setstretch{2}\nx\n\\end{document}\n")
        assert jf.page_cap(facts, tex) == 47
        tex.write_text("\\documentclass{article}\n\\begin{document}\nx\n\\end{document}\n")
        assert jf.page_cap(facts, tex) == 32, "undeclared spacing takes the strictest cap"


def test_missing_bst_stops_apply_before_any_edit():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        before = tex.read_bytes()
        r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "apply", "--journal", "jfqa", str(tex)],
                           capture_output=True, text=True)
        assert r.returncode == 2 and "JFQA.bst" in r.stderr, r.stderr
        assert tex.read_bytes() == before, "nothing may change when the .bst is missing"


def test_second_apply_keeps_the_agent_sections_of_the_report():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        report = Path(td) / "report.md"
        doc = journal_rules.load_journal("JFQA")
        fake = {"ok": True, "rc": 0, "errors": [], "warnings": [], "boxes": [], "pages": 3, "main_pages": 3, "seconds": 1}
        jf.write_report(report, doc=doc, main_tex=tex, violations=[], applied=1, compile_result=fake,
                        house_items=doc["house"], candidates=[])
        txt = report.read_text().replace("_(the agent fills this: per-item edit counts and notable rewrites)_",
                                         "- headings_title_case: 4 edits")
        txt = txt.replace("_(what no rule can decide: page overrun, abstract cut, any compile error that survived the bounded recompiles)_",
                          "Page overrun: 55 vs 45 — trim Section IV.")
        report.write_text(txt)
        jf.write_report(report, doc=doc, main_tex=tex, violations=[], applied=0, compile_result=fake,
                        house_items=doc["house"], candidates=[])
        again = report.read_text()
        assert "- headings_title_case: 4 edits" in again and "trim Section IV" in again, again


# ---------------------------------------------------------------------------
# CLI contract
# ---------------------------------------------------------------------------

def test_cli_exit_codes_and_required_journal():
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        eng = str(SCRIPTS / "journal_format.py")
        r = subprocess.run([sys.executable, eng, "check", str(tex)], capture_output=True, text=True)
        assert r.returncode == 2 and "--journal" in r.stderr
        r = subprocess.run([sys.executable, eng, "check", "--journal", "bogus", str(tex)], capture_output=True, text=True)
        assert r.returncode == 2 and "known:" in r.stderr
        r = subprocess.run([sys.executable, eng, "check", "--journal", "jfqa", str(tex)], capture_output=True, text=True)
        assert r.returncode == 1
        assert f"{tex.name}:1: [layout.documentclass]" in r.stdout, r.stdout
        assert "[house.headings_title_case] candidate" in r.stdout
        r = subprocess.run([sys.executable, eng, "check", "--journal", "jfqa", "--json", str(tex)], capture_output=True, text=True)
        doc = json.loads(r.stdout)
        assert doc["journal"] == "JFQA" and doc["violations"] and doc["house_candidates"]
        r = subprocess.run([sys.executable, eng, "check", str(Path(td) / "nope.tex"), "--journal", "jfqa"], capture_output=True, text=True)
        assert r.returncode == 2


def test_codex_verb_runs_exactly_one_bounded_round_on_a_disposable_copy():
    """A stub `codex` on PATH records its invocation: one call, cwd = a copy
    (never the manuscript directory), JSON findings pass through."""
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "jfqa_wrong_format.tex", td)
        bindir = Path(td) / "bin"
        bindir.mkdir()
        log = Path(td) / "codex_calls.log"
        stub = bindir / "codex"
        stub.write_text("#!/bin/sh\n"
                        f"echo \"$PWD\" >> '{log}'\n"
                        f"echo \"$*\" >> '{log}.args'\n"
                        "cat >/dev/null\n"
                        "echo 'codex'\n"
                        "echo '[{\"file\": \"main.tex\", \"line\": 9, \"house_id\": \"headings_case\", \"before\": \"x\", \"after\": \"y\"}]'\n")
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
        env = dict(os.environ, PATH=f"{bindir}:{os.environ['PATH']}")
        r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "codex", "--journal", "jfqa", str(tex)],
                           capture_output=True, text=True, env=env)
        assert r.returncode == 0, r.stderr
        findings = json.loads(r.stdout)
        assert findings[0]["house_id"] == "headings_case"
        calls = log.read_text().splitlines()
        assert len(calls) == 1, calls
        assert Path(calls[0]).resolve() != Path(td).resolve() and "journal-format-codex-" in calls[0]
        assert not (Path(calls[0])).exists(), "the disposable copy is gone after the round"
        args = Path(f"{log}.args").read_text()
        assert "--skip-git-repo-check" in args and "--dangerously-bypass-approvals-and-sandbox" in args, args
        assert "-m gpt-6-astra" in args and "model_reasoning_effort=high" in args, args
        # a failing or malformed round is an error object and exit 1, never a silent success
        stub.write_text("#!/bin/sh\ncat >/dev/null\necho 'not json'\nexit 3\n")
        r = subprocess.run([sys.executable, str(SCRIPTS / "journal_format.py"), "codex", "--journal", "jfqa", str(tex)],
                           capture_output=True, text=True, env=env)
        assert r.returncode == 1 and json.loads(r.stdout)["error"], r.stdout


# ---------------------------------------------------------------------------
# a check whose silence must mean conformance: wrapped citations, the
# manuscript/appendix page boundary, and who owns the printed page cap
# ---------------------------------------------------------------------------

def test_wrapped_citation_is_checked_and_rewritten_whole():
    """A \\citep whose argument brace closes on the next line is a citation
    like any other under citet_in_parens: reported at its first line, joined
    and rewritten by apply; one with pre/post notes is reported for a hand
    rewrite and left in place."""
    with tempfile.TemporaryDirectory() as td:
        tex = _copy(FIX / "banned" / "wrapped_citep.tex", td)
        vs = [v for v in _check(tex, "JF") if v.rule == "citations.form"]
        assert [v.line for v in vs] == [4, 6], [(v.line, v.message) for v in vs]
        # the joined span 4-5 carries the wrapped \\citep AND line 5's bare \\cite: one rewrite
        assert "wrapped across lines 4-5" in vs[0].message and vs[0].auto_fixable
        assert "\\cite{gamma2003} -> \\citet{gamma2003}" in vs[0].message
        assert not vs[1].auto_fixable and "hand" in vs[1].message and "wrapped across lines 6-7" in vs[1].message
        assert jf.apply_fixes(tex, vs) == 1, "one joined rewrite; the noted one is not fixable"
        body = tex.read_text()
        assert "(\\citet{alpha2001}, \\citet{beta2002}) finds this; so does \\citet{gamma2003}." in body
        assert "\\citep{alpha2001" not in body and "\\citep[see][p.~3]{delta2004,\n" in body, body
        left = [v for v in _check(tex, "JF") if v.rule == "citations.form"]
        assert [v.line for v in left] == [5] and not left[0].auto_fixable, "the noted one stays for the hand rewrite"


def test_wrapped_citation_edge_cases_never_break_the_source():
    """The reviewed edge cases: a comment inside the span is reported, never
    joined; an unrelated group closing earlier on the line cannot hide the
    citation; a duplicate key inside the span composes with the duplicate-key
    fix (one \\citet, no leftover violation); a span that never closes is
    reported for a hand rewrite."""
    with tempfile.TemporaryDirectory() as td:
        tex = Path(td) / "edge.tex"
        tex.write_text("\\documentclass[12pt]{article}\n\\usepackage{natbib}\n\\begin{document}\n"
                       "See \\citep{alpha,% keep this comment\nbeta} here.\n"
                       "\\emph{Prior work\nends here} \\citep{gamma,\ndelta} too.\n"
                       "Twice \\citep{eps,\neps} once.\n"
                       "Open \\citep{zeta,\n" + "more,\n" * 45 + "\\end{document}\n")
        vs = [v for v in _check(tex, "JF") if v.rule == "citations.form"]
        by = {v.line: v for v in vs}
        assert sorted(by) == [4, 7, 9, 11], [(v.line, v.message) for v in vs]
        assert not by[4].auto_fixable and "comment inside the span" in by[4].message, by[4].message
        assert by[7].auto_fixable and "wrapped across lines 7-8" in by[7].message, by[7].message
        assert by[9].auto_fixable and "(\\citet{eps})" in by[9].message, by[9].message
        assert not by[11].auto_fixable and "does not close" in by[11].message, by[11].message
        assert jf.apply_fixes(tex, vs) == 2, "the two clean wrapped spans; the commented and the unclosed ones are not fixable"
        body = tex.read_text()
        assert "\\citep{alpha,% keep this comment\nbeta}" in body, "the commented span is untouched"
        assert "ends here} (\\citet{gamma}, \\citet{delta}) too." in body, body
        assert "Twice (\\citet{eps}) once." in body and "\\citet{eps}, \\citet{eps}" not in body, body
        left = {v.line for v in _check(tex, "JF") if v.rule in ("citations.form", "citation.duplicate_keys")}
        assert left == {4, 9}, left   # the commented span and the unclosed one remain (shifted by the two joins), nothing else


def test_appendix_start_page_is_a_heading_after_references():
    """The page split that the journal cap measures: with the manuscript's
    own heading, only the page opening with it; without one, a wrapped
    in-text mention or a post-References exhibit note naming the appendix is
    not the boundary, the title as a page's first line is; without a
    References page nothing is excluded."""
    pages = ["Title page\nAbstract", "Body. We relegate the proofs to the\nInternet Appendix for brevity.\nMore body.",
             "References\nAlpha, A. 2001.",
             "Table I\nWe report the tests from the\nInternet Appendix for each specification\nPanel A: Results",
             "Internet Appendix for\n``A Working Paper Fixture''\nIA.1 Proofs"]
    heading = "internet appendix for a working paper fixture"
    assert jf.appendix_start_page(pages, "Internet Appendix", heading) == 5
    assert jf.appendix_start_page(pages, "Internet Appendix") == 5, "fallback: the exhibit note on page 4 is not a page's first line"
    assert jf.appendix_start_page(pages[:4], "Internet Appendix", heading) is None
    assert jf.appendix_start_page([pages[0], pages[1], pages[4]], "Internet Appendix", heading) is None, "no References page: fail closed"
    assert jf.appendix_start_page(["T", "References", "Internet Appendix", "IA text"], "Internet Appendix") == 3
    assert jf.appendix_start_page(["T", "References", "Internet Appendix: Extra Tables\nTable IA.I"], "Internet Appendix") == 3
    ms = jf.Manuscript(FIX / "wp" / "main.tex", also=[FIX / "wp" / "sections" / "appendix.tex"])
    assert jf.appendix_heading_text(ms, "Internet Appendix") == heading


def test_duplicate_key_is_detected_across_a_wrapped_citation():
    """The natbib collapse trigger hides in a wrapped argument as easily as in
    a flat one: `\\citet{alpha,\\nalpha}` is found on the joined span, deduplicated
    into one line; a commented span is reported, never joined."""
    with tempfile.TemporaryDirectory() as td:
        tex = Path(td) / "dup.tex"
        tex.write_text("\\documentclass[12pt]{article}\n\\usepackage{natbib}\n\\begin{document}\n"
                       "As \\citet{alpha,\nalpha} showed.\n"
                       "And \\citet{beta,% note\nbeta} too.\n\\end{document}\n")
        vs = [v for v in _check(tex, "JFQA") if v.rule == "citation.duplicate_keys"]
        assert [v.line for v in vs] == [4, 6], [(v.line, v.message) for v in vs]
        assert vs[0].auto_fixable and "wrapped across lines 4-5" in vs[0].message
        assert not vs[1].auto_fixable and "comment inside the span" in vs[1].message
        assert jf.apply_fixes(tex, vs) == 1
        body = tex.read_text()
        assert "As \\citet{alpha} showed." in body and "\\citet{beta,% note\nbeta}" in body, body
    # the same span carries a duplicate key AND a \\citep under citet_in_parens, and a paragraph
    # break follows: both fixes land on the current lines, the blank line survives
    with tempfile.TemporaryDirectory() as td:
        tex = Path(td) / "both.tex"
        tex.write_text("\\documentclass[12pt]{article}\n\\usepackage{natbib}\n\\begin{document}\n"
                       "First \\citep{alpha,\nalpha} here.\n\nSecond paragraph stays.\n"
                       "Open \\citet{zeta,\n" + "more,\n" * 45 + "\\end{document}\n")
        vs = [v for v in _check(tex, "JF") if v.rule in ("citation.duplicate_keys", "citations.form")]
        assert {v.rule for v in vs if v.line == 4} == {"citation.duplicate_keys", "citations.form"}, [(v.rule, v.line) for v in vs]
        assert any(v.rule == "citation.duplicate_keys" and "does not close" in v.message for v in vs), "an unresolved span is reported by the duplicate-key check too"
        jf.apply_all(tex, "JF")
        body = tex.read_text()
        assert "First (\\citet{alpha}) here.\n\nSecond paragraph stays." in body, body


def _main() -> int:
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f" [OK] {name}")
        except _SKIPS as exc:  # pytest's skip derives from BaseException, not Exception
            print(f" [SKIP] {name}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            import traceback
            print(f" [FAIL] {name}: {type(exc).__name__}: {exc}")
            traceback.print_exc()
    print(f"{len(tests) - failed}/{len(tests)} latex tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_main())
