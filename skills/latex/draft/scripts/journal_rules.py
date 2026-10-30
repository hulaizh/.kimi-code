#!/usr/bin/env python3
"""journal_rules.py — loader + schema validator for the facts-only journal files.

`journals/<code>.yaml` is the single owner of every journal fact the latex
skill consumes: layout, length, structure, citations, and the plain-language
`house:` copyediting list. No inheritance, no rule programming; an UNKNOWN
key fails at load so the files cannot silently drift from the schema (see
references/journal_file.md).

A journal file is the journal's ACCEPTED-paper format as recorded from its
sources, applied ONLY once a paper is accepted there (`journal_format.py
apply --journal <code>`; user directive 2026-09-21). Every working paper
keeps the one working-paper format (validate_latex.py, the gan S0 gate),
which no journal file touches. `load_journal(code)["facts"]` is what the
acceptance pass applies and checks — the STATED facts and nothing else: a
fact the file leaves unstated is never checked and never defaulted.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

JOURNALS_DIR = Path(__file__).resolve().parent.parent / "journals"

# canonical code -> file stem, where they differ (Econometrica -> ecma.yaml)
_FILE_STEM = {"Econometrica": "ecma"}
_CODE_FOR_STEM = {v: k for k, v in _FILE_STEM.items()}

# Journal aliases live in the GAN plugin's shared_patterns (the ONE map every
# journal-keyed surface normalizes through); imported by path so this skill
# needs no package install, with a plain strip when the plugin is absent.
_GAN_SCRIPTS = Path.home() / ".claude" / "plugins" / "gan" / "scripts"


def normalize_journal(journal) -> str:
    if str(_GAN_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(_GAN_SCRIPTS))
    try:
        from shared_patterns import normalize_journal as _nj  # type: ignore
        return _nj(journal)
    except ImportError:
        return str(journal or "").strip()


_SECTIONS = ("layout", "length", "structure", "citations")
_KNOWN = {
    "layout": {"paper", "font_pt", "font", "class_options", "margins", "spacing",
               "ragged_right", "hyphenation", "parindent", "preamble"},
    "length": {"pages", "pages_by_spacing", "appendix_pages", "abstract_words"},
    "structure": {"numbering", "exhibit_numbering", "appendix_title", "exhibits", "float_markers",
                  "title_page", "jel", "keywords"},
    "citations": {"bst", "bst_companions", "in_text", "full_authors_first", "equation_ref", "stars"},
}


def available_journals() -> list[str]:
    return sorted(_CODE_FOR_STEM.get(p.stem, p.stem.upper())
                  for p in JOURNALS_DIR.glob("*.yaml") if not p.name.startswith("_"))


def journal_file(code: str) -> Path:
    p = JOURNALS_DIR / f"{_FILE_STEM.get(code, code.lower())}.yaml"
    if not p.is_file():
        raise FileNotFoundError(
            f"no journal file for {code!r} — expected {p}; known: {', '.join(available_journals())}")
    return p


def _validate(doc: dict, path: Path) -> None:
    for k in doc:
        if k not in ("journal", "name", "sources", "house", "verified", *_SECTIONS):
            raise ValueError(f"{path.name}: unknown top-level key {k!r}")
    v = doc.get("verified")
    if v is not None:
        secs = v.get("sections") if isinstance(v, dict) else None
        if (not isinstance(v, dict) or set(v) != {"date", "sections"}
                or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v.get("date", "")))
                or not isinstance(secs, list) or not secs
                or not all(isinstance(s, str) and s in _SECTIONS for s in secs)):
            raise ValueError(f"{path.name}: `verified` must be exactly {{date: YYYY-MM-DD, sections: [layout|length|structure|citations ...]}} "
                             f"— the date the journal's OWN current guidelines were read and the sections they settled")
    for sec in _SECTIONS:
        body = doc.get(sec) or {}
        if not isinstance(body, dict):
            raise ValueError(f"{path.name}: `{sec}` must be a mapping")
        for k in body:
            if k not in _KNOWN[sec]:
                raise ValueError(f"{path.name}: unknown key {sec}.{k}")
    for i, item in enumerate(doc.get("house") or []):
        if not isinstance(item, dict) or not item.get("id") or not item.get("rule"):
            raise ValueError(f"{path.name}: house[{i}] needs at least `id` and `rule`")


def load_journal(journal: str) -> dict:
    """{journal, name, sources, facts, house, verified} for an alias-normalized
    code. `facts` is every section (possibly empty) — the stated facts only.
    Raises FileNotFoundError for an unknown code, ValueError for schema drift."""
    code = normalize_journal(journal)
    path = journal_file(code)
    with path.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    if not isinstance(doc, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    _validate(doc, path)
    return {
        "journal": code,
        "name": doc.get("name", code),
        "sources": doc.get("sources") or [],
        "facts": {sec: dict(doc.get(sec) or {}) for sec in _SECTIONS},
        "house": list(doc.get("house") or []),
        "verified": ({**doc["verified"], "date": str(doc["verified"].get("date", ""))}
                     if isinstance(doc.get("verified"), dict) else {}),
    }


def provenance_note(journal: str) -> str:
    """One line for `check` and the apply report: whether the file's facts
    were VERIFIED against the journal's own guidelines (the `verified:`
    block — date and sections) or merely carried from its sources."""
    doc = load_journal(journal)
    v = doc.get("verified") or {}
    if not v:
        return f"{doc['journal']}: NEVER verified against the journal's own guidelines (facts carried; see its sources)"
    rest = sorted(set(_SECTIONS) - set(v["sections"]))
    tail = f"; {', '.join(rest)} carried from its sources" if rest else ""
    return f"{doc['journal']}: verified {v['date']} for {', '.join(v['sections'])}{tail}"


if __name__ == "__main__":
    import json
    code = sys.argv[1] if len(sys.argv) > 1 else "JF"
    print(json.dumps(load_journal(code), indent=2, ensure_ascii=False, default=str))
