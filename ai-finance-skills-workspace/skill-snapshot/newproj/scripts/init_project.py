#!/usr/bin/env python3
"""
init_project.py - Initialize or update a project with standard structure.

Supports both new and existing projects with smart merge capabilities.
"""

import argparse
import getpass
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

GAN_SCRIPTS_DIR = Path.home() / ".claude" / "plugins" / "gan" / "scripts"
if str(GAN_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(GAN_SCRIPTS_DIR))



class ProjectInitializer:
    """Initialize or update a project with standard structure."""

    FOLDERS = [
        "src", "tests", "draft", "draft/sections", "draft/tables", "draft/figures",
        "output", "output/tables", "output/figures", "output/results",
        "docs", "docs/plans", "docs/notes", "docs/slides", "docs/submission", "logs",
        ".claude", ".proofs", ".gan", ".gan/rounds",
    ]
    RAW_DATA_PATH = Path("/data/raw")
    USERNAME = getpass.getuser()
    DATA_BASE = Path(f"/data/{USERNAME}")
    GAN_SCRIPTS = Path.home() / ".claude" / "plugins" / "gan" / "scripts"
    GAN_TEMPLATES = Path.home() / ".claude" / "plugins" / "gan" / "references" / "templates"

    def __init__(
        self,
        project_name: str,
        project_path: Path,
        dry_run: bool = False,
        backup: bool = False,
        merge_claude: bool = False,
        migrate_data: bool = False,
        force: bool = False,
        title: str = "Untitled Research Project",
        author: str = "Hulai Zhang",
        entry_point: str = "user_topic",
        target_journal: str = "JF",
    ):
        self.project_name = project_name
        self.project_path = project_path.resolve()
        self.dry_run = dry_run
        self.backup = backup
        self.merge_claude = merge_claude
        self.migrate_data = migrate_data
        self.force = force
        self.title = title
        self.author = author
        self.entry_point = entry_point
        self.target_journal = target_journal

        self.script_dir = Path(__file__).parent
        self.backup_dir = self.project_path / ".claude" / "backups"
        self.data_target = self.DATA_BASE / project_name / "data"
        self.temp_target = self.DATA_BASE / project_name / "temp"

        self.actions: list[str] = []
        self.warnings: list[str] = []
        self._skeleton_created = False

    def log(self, message: str, action: bool = False) -> None:
        """Log a message, optionally recording it as an action."""
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")
        if action:
            self.actions.append(message)

    def warn(self, message: str) -> None:
        """Log a warning."""
        print(f"WARNING: {message}")
        self.warnings.append(message)

    def is_existing_project(self) -> bool:
        """Detect if this is an existing project."""
        indicators = [
            self.project_path / ".git",
            self.project_path / "CLAUDE.md",
            self.project_path / ".gitignore",
            self.project_path / "src",
        ]
        return any(p.exists() for p in indicators)

    def create_backup(self, file_path: Path) -> Optional[Path]:
        """Create a timestamped backup of a file."""
        if not file_path.exists():
            return None

        if self.dry_run:
            self.log(f"Would backup: {file_path}", action=True)
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = self.backup_dir / f"{file_path.name}.{timestamp}.bak"
        shutil.copy2(file_path, backup_path)
        self.log(f"Backed up: {file_path} -> {backup_path}", action=True)
        return backup_path

    def create_folders(self) -> None:
        """Create the standard GAN project folder structure."""
        for folder in self.FOLDERS:
            folder_path = self.project_path / folder
            if folder_path.exists():
                continue
            if self.dry_run:
                self.log(f"Would create folder: {folder}", action=True)
            else:
                folder_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Created folder: {folder}", action=True)

        # docs/slides and docs/submission exist LOCALLY from initiation with no
        # placeholder file: git stores only files, so both stay invisible to
        # git until a deck or a submission round lands in them (user directive
        # 2026-09-12 — never a .gitkeep, never an ignore rule).

        # Pin output/results/ with a README so the dir survives `git add` and
        # documents the agent-native JSON-handoff contract for future readers.
        results_readme = self.project_path / "output" / "results" / "README.md"
        if not results_readme.exists():
            content = (
                "# output/results/\n\n"
                "Single home for project results. Two kinds of files live here:\n\n"
                "1. **Agent-native JSON summaries** emitted by estimation scripts via\n"
                "   `result.to_agent_summary()`. The GAN Critic's internal-consistency\n"
                "   sub-check 1 (code↔draft alignment) reads these to verify that\n"
                "   numbers in `draft/` tables match the underlying estimation output.\n"
                "2. **Manually curated results** — final tables and figures hand-picked\n"
                "   for the paper (LaTeX-ready). Manual edits OK here, unlike\n"
                "   `output/tables/` and `output/figures/` which scripts overwrite.\n\n"
                "Filenames for JSON summaries mirror the corresponding table or figure\n"
                "stem (e.g., `main_results.json` for `output/tables/main_results.tex`).\n"
            )
            if self.dry_run:
                self.log("Would create output/results/README.md", action=True)
            else:
                results_readme.write_text(content)
                self.log("Created output/results/README.md", action=True)

        # Pin draft/tables + draft/figures with READMEs stating the mirror
        # contract: output/ is the single script-write home; these dirs are a
        # compile-time COPIED mirror so wrappers use LOCAL paths and draft/
        # stays submission-portable (never \input{../output/...}).
        mirror_refs = {
            "tables": r"`\input{tables/<name>}` in `sections/tables.tex`",
            "figures": (r"`\graphicspath{{figures/}}` + "
                        r"`\includegraphics{figures/<name>.pdf}` in `sections/figures.tex`"),
        }
        for sub, src_glob in (("tables", "output/tables/*.tex"),
                              ("figures", "output/figures/*.pdf|png")):
            mirror_readme = self.project_path / "draft" / sub / "README.md"
            if mirror_readme.exists():
                continue
            content = (
                f"# draft/{sub}/\n\n"
                f"Compile-time MIRROR of `{src_glob}` — `output/` is the single\n"
                f"home scripts write to; this directory is refreshed automatically by\n"
                f"`compile_with_provenance.py` before every compile (copy-if-changed,\n"
                f"never deletes).\n\n"
                f"- NEVER hand-edit files here; edit the generating script and re-run it.\n"
                f"- Wrappers reference LOCAL paths — {mirror_refs[sub]} —\n"
                f"  never `../output/...` (the draft must build from a copied dir).\n"
                f"- Manual refresh: `python3 ~/.claude/plugins/gan/scripts/"
                f"compile_with_provenance.py --project-dir . --sync-only`\n"
            )
            if self.dry_run:
                self.log(f"Would create draft/{sub}/README.md", action=True)
            else:
                mirror_readme.write_text(content)
                self.log(f"Created draft/{sub}/README.md", action=True)

    def create_data_directories(self) -> None:
        """Create data directories on /data/ drive."""
        for target in [self.data_target, self.temp_target]:
            if target.exists():
                continue
            if self.dry_run:
                self.log(f"Would create: {target}", action=True)
            else:
                target.mkdir(parents=True, exist_ok=True)
                self.log(f"Created: {target}", action=True)

    def handle_symlink(self, name: str, target: Path) -> None:
        """Handle symlink creation with migration support."""
        link_path = self.project_path / name

        # Already a correct symlink
        if link_path.is_symlink():
            current_target = link_path.resolve()
            if current_target == target.resolve():
                self.log(f"Symlink {name}/ already correct")
                return
            else:
                self.warn(f"Symlink {name}/ points to {current_target}, expected {target}")
                if not self.force:
                    return
                if self.dry_run:
                    self.log(f"Would update symlink: {name}/ -> {target}", action=True)
                else:
                    link_path.unlink()
                    link_path.symlink_to(target)
                    self.log(f"Updated symlink: {name}/ -> {target}", action=True)
                return

        # Real directory exists
        if link_path.is_dir():
            if self.migrate_data:
                contents = list(link_path.iterdir())
                if contents:
                    if self.dry_run:
                        self.log(f"Would migrate {len(contents)} items from {name}/ to {target}", action=True)
                        self.log(f"Would create symlink: {name}/ -> {target}", action=True)
                    else:
                        # Ensure target exists
                        target.mkdir(parents=True, exist_ok=True)
                        # Move contents
                        for item in contents:
                            dest = target / item.name
                            if dest.exists():
                                self.warn(f"Skipping {item.name}: already exists at destination")
                                continue
                            shutil.move(str(item), str(dest))
                            self.log(f"Moved: {item.name} -> {target}", action=True)
                        # Remove empty directory and create symlink
                        link_path.rmdir()
                        link_path.symlink_to(target)
                        self.log(f"Created symlink: {name}/ -> {target}", action=True)
                else:
                    if self.dry_run:
                        self.log(f"Would remove empty {name}/ and create symlink", action=True)
                    else:
                        link_path.rmdir()
                        link_path.symlink_to(target)
                        self.log(f"Replaced empty dir with symlink: {name}/ -> {target}", action=True)
            else:
                self.warn(f"Directory {name}/ exists (not a symlink). Use --migrate-data to convert.")
            return

        # Nothing exists, create symlink
        if self.dry_run:
            self.log(f"Would create symlink: {name}/ -> {target}", action=True)
        else:
            link_path.symlink_to(target)
            self.log(f"Created symlink: {name}/ -> {target}", action=True)

    def create_symlinks(self) -> None:
        """Create data and temp symlinks."""
        self.handle_symlink("data", self.data_target)
        self.handle_symlink("temp", self.temp_target)


    LATEX_ASSETS = Path.home() / ".claude" / "skills" / "latex" / "draft" / "assets"

    def create_draft_skeleton(self) -> None:
        """The whole LaTeX skeleton (style.tex, main.tex, ref.bib, sections/)
        from the latex skill's draft assets — written only when
        draft/main.tex is ABSENT. A draft with a main.tex is the project's
        own; template files are never patched into it piecemeal. The skeleton
        IS the working-paper format every draft keeps (a journal's format is
        applied only on acceptance, by the latex skill's journal_format.py)."""
        draft_dir = self.project_path / "draft"
        if (draft_dir / "main.tex").exists():
            self.log("draft/main.tex present — LaTeX skeleton untouched")
            return

        # Assets were verified by _preflight_assets() at the top of run()
        # (existence + substitution-anchor literals, before ANY write). The
        # assets carry the working-paper structure and layout — the one
        # format every draft keeps.
        style_src = self.LATEX_ASSETS / "style.tex"
        paper_template = self.LATEX_ASSETS / "paper_template.tex"

        if not self.dry_run:  # dry-run must not mutate (codex sweep F3)
            draft_dir.mkdir(parents=True, exist_ok=True)

        # style.tex — copy from the latex skill's draft assets.
        style_path = draft_dir / "style.tex"
        if not style_path.exists() and style_src.exists():
            if self.dry_run:
                self.log("Would copy style.tex from the latex skill's draft assets",
                         action=True)
            else:
                style_path.write_text(style_src.read_text())
                self.log("Copied draft/style.tex from the latex skill's draft assets",
                         action=True)

        # main.tex — copy paper_template.tex from the latex skill's draft assets
        # with title/author substitution and model-line comment-out. Fail-fast
        # if the asset is missing or has drifted; the inline fallback was
        # removed, so a silent skip would scaffold a broken GAN project.
        tex_path = draft_dir / "main.tex"
        if not tex_path.exists():
            if not paper_template.exists():
                raise FileNotFoundError(
                    f"Required latex skill asset not found: {paper_template}. "
                    f"Install or repair ~/.claude/skills/latex/draft/assets/."
                )
            if self.dry_run:
                # Validate the asset (read + literal-presence checks) without
                # writing, so asset drift surfaces in the safest preview path.
                self._render_main_tex(paper_template, None, self.title, self.author)
                self.log("Would create draft/main.tex (from paper_template.tex)", action=True)
            else:
                self._render_main_tex(paper_template, tex_path, self.title, self.author)
                self.log("Created draft/main.tex (from paper_template.tex)", action=True)
            self._skeleton_created = True

        # ref.bib
        bib_path = draft_dir / "ref.bib"
        if not bib_path.exists():
            if self.dry_run:
                self.log("Would create draft/ref.bib", action=True)
            else:
                bib_path.write_text(f"% Bibliography for {self.title}\n")
                self.log("Created draft/ref.bib", action=True)

        # sections/*.tex — modular section stubs plus tables/figures/appendix wrappers
        template_map = {
            "draft/sections/abstract.tex": "section_abstract.tex",
            "draft/sections/introduction.tex": "section_introduction.tex",
            "draft/sections/model.tex": "section_model.tex",
            "draft/sections/data.tex": "section_data.tex",
            "draft/sections/methodology.tex": "section_methodology.tex",
            "draft/sections/results.tex": "section_results.tex",
            "draft/sections/robustness.tex": "section_robustness.tex",
            "draft/sections/conclusion.tex": "section_conclusion.tex",
            "draft/sections/tables.tex": "tables_template.tex",
            "draft/sections/figures.tex": "figures_template.tex",
            "draft/sections/appendix.tex": "appendix_template.tex",
        }
        for dest_rel, asset_name in template_map.items():
            dest_path = self.project_path / dest_rel
            if dest_path.exists():
                continue
            asset_path = self.LATEX_ASSETS / asset_name
            if asset_path.exists():
                if self.dry_run:
                    self.log(f"Would copy {dest_rel} from the latex skill {asset_name}", action=True)
                else:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(asset_path, dest_path)
                    self.log(f"Copied {dest_rel} from the latex skill {asset_name}", action=True)
            else:
                self.warn(f"latex skill asset not found: {asset_path}")

    def _recorded_target_journal(self) -> str:
        """The target journal the project records (the .gan/state.jsonl head,
        floored by the state writer), else the one this run was given."""
        sm = self._load_state_manager()
        try:
            return sm.load_state(str(self.project_path)).get("target_journal") or self.target_journal
        except (OSError, RuntimeError, ValueError, AttributeError):
            return self.target_journal

    def create_gan_state(self) -> None:
        """The GAN machine layer: .gan/current_proposal.json (template
        envelope), .gan/state.jsonl via the plugin's state_manager, and the
        runtime seeds. Each piece is created only if absent."""
        # .gan/current_proposal.json — the canonical proposal envelope,
        # seeded from the JSON template (design §7: drop the root md
        # write; the v5 migration converter handles legacy md→json).
        # materialization_status="template" with GAN-TEMPLATE marker
        # values; the Generator replaces it in Validate round 1.
        proposal_path = self.project_path / ".gan" / "current_proposal.json"
        if not proposal_path.exists():
            proposal_template = self.GAN_TEMPLATES / "current_proposal_template.json"
            if proposal_template.exists():
                if self.dry_run:
                    self.log("Would create .gan/current_proposal.json (template envelope)", action=True)
                else:
                    import json as _json
                    payload = _json.loads(proposal_template.read_text())
                    payload["title"] = payload["title"].replace(
                        "{TITLE}", self.title) if "{TITLE}" in payload.get("title", "") else payload.get("title", self.title)
                    proposal_path.parent.mkdir(parents=True, exist_ok=True)
                    proposal_path.write_text(
                        _json.dumps(payload, indent=2, ensure_ascii=False),
                        encoding="utf-8")
                    self.log("Created .gan/current_proposal.json (template envelope)", action=True)
            else:
                self.warn(f"gan plugin template not found: {proposal_template}")

        # .gan/state.jsonl — via the gan plugin's state_manager (fail-loud if absent)
        state_path = self.project_path / ".gan" / "state.jsonl"
        if not state_path.exists():
            if self.dry_run:
                self.log("Would create .gan/state.jsonl", action=True)
            else:
                state_path.parent.mkdir(parents=True, exist_ok=True)
                self._init_gan_state()
                self.log("Created .gan/state.jsonl", action=True)

        # Runtime seedings (SINGLE OWNER — the gan wrapper used to add these
        # after delegating, so a direct /newproj run missed both;
        # 2026-08-10 consistency sweep moved them here):
        self._seed_runtime_settings()

    def _seed_runtime_settings(self) -> None:
        """Seed the /evo capture ledger and the project's autoCompactWindow.

        - .gan/infra_issues.jsonl: typed capture journal (v2 fold) so the
          /evo capture layer works from initialization. Idempotent: an
          existing journal is never touched (an empty transaction appends
          nothing).
        - .claude/settings.json autoCompactWindow=200000: the within-round
          context backstop — EVERY claude session in the project dir (lead
          AND teammate panes) auto-compacts mid-turn instead of wedging at
          100% context. Harness contract: integer tokens, 100000–1000000;
          200000 is the harness's own recommendation. Merge-preserving:
          never overwrite a user-set value, never drop other keys, leave an
          unreadable/non-dict file untouched.
        """
        import json as _json
        import infra_issues
        if not infra_issues.ledger_path(str(self.project_path)).exists():
            if self.dry_run:
                self.log("Would create .gan/infra_issues.jsonl (capture journal)", action=True)
            else:
                with infra_issues.ledger_transaction(str(self.project_path), op="seed"):
                    pass
                self.log("Created .gan/infra_issues.jsonl (capture journal)", action=True)

        settings_path = self.project_path / ".claude" / "settings.json"
        try:
            settings = (_json.loads(settings_path.read_text())
                        if settings_path.exists() else {})
        except (OSError, _json.JSONDecodeError):
            settings = None
        if isinstance(settings, dict) and "autoCompactWindow" not in settings:
            if self.dry_run:
                self.log("Would seed .claude/settings.json autoCompactWindow=200000", action=True)
            else:
                settings["autoCompactWindow"] = 200000
                settings_path.parent.mkdir(parents=True, exist_ok=True)
                settings_path.write_text(_json.dumps(settings, indent=2) + "\n")
                self.log("Seeded .claude/settings.json autoCompactWindow=200000", action=True)

    _OLD_GEOM = ("\\usepackage[top=1.5in, bottom=1.5in, "
                 "left=1in, right=1in]{geometry}")
    _OLD_DC = "\\documentclass[a4paper, 12pt]{article}"
    _OLD_TITLE = r"\newcommand{\Title}{Paper Title: A Subtitle if Needed}"
    _OLD_AUTHOR = r"\newcommand{\Author}{Hulai Zhang}"
    _UNCOMMENTED_MODEL_PATTERN = r"(?m)^[ \t]*\\input\{sections/model\}"

    def _preflight_assets(self) -> None:
        """UNCONDITIONAL asset preflight (every run, dry-run included),
        run at the top of run() BEFORE any folder or file creation: both
        latex skill assets must exist, the
        assets carrying the literals this initializer substitutes
        (title/author via _render_main_tex; the fallback geometry and
        documentclass anchors). A missing/drifted asset must fail with NO
        partial scaffold behind."""
        style_src = self.LATEX_ASSETS / "style.tex"
        paper_template = self.LATEX_ASSETS / "paper_template.tex"
        for asset in (style_src, paper_template):
            if not asset.exists():
                raise FileNotFoundError(
                    f"Required latex skill asset not found: {asset}. "
                    f"Install or repair "
                    f"~/.claude/skills/latex/draft/."
                )
        if self._OLD_GEOM not in style_src.read_text():
            raise RuntimeError(
                "style.tex asset has drifted: expected geometry line not "
                "found. Update the asset or this script."
            )
        template_text = paper_template.read_text()
        if self._OLD_DC not in template_text:
            raise RuntimeError(
                "paper_template.tex has drifted: expected documentclass "
                "line not found. Update the asset or this script."
            )
        # The _render_main_tex substitution anchors too — a drift in ANY
        # anchor must fail here, before folders/symlinks exist, not from
        # inside create_draft_skeleton (_render_main_tex re-validates locally,
        # but by then the scaffold is partially written).
        import re as _re
        if self._OLD_TITLE not in template_text:
            raise RuntimeError(
                "paper_template.tex has drifted: expected \\newcommand{\\Title} "
                "line not found. Update the asset or this script."
            )
        if self._OLD_AUTHOR not in template_text:
            raise RuntimeError(
                "paper_template.tex has drifted: expected literal author "
                "block not found. Update the asset or this script."
            )
        if not _re.search(self._UNCOMMENTED_MODEL_PATTERN, template_text):
            raise RuntimeError(
                "paper_template.tex has drifted: expected live "
                "\\input{sections/model} line not found. Update the asset "
                "or this script."
            )

    def _render_main_tex(self, template_path: Path, dst: Optional[Path], title: str, author: str) -> None:
        """Copy paper_template.tex with title/author substitution; comment out optional model input.

        Fail-fast: raise on any asset drift (missing literal title/author/model lines)
        so silent regressions in latex skill assets surface as hard errors instead of
        scaffolding the wrong text into every new project.

        If dst is None, validate the asset only (used by --dry-run); no file is written.
        """
        import re

        text = template_path.read_text()
        OLD_TITLE = self._OLD_TITLE
        OLD_AUTHOR = self._OLD_AUTHOR
        # Match an UN-commented \input{sections/model} at line start (any indent), to
        # detect the live line both before substitution and as a post-condition. Comment
        # markers like %% \input{...} won't match because the regex anchors to start of line.
        UNCOMMENTED_MODEL_RE = re.compile(self._UNCOMMENTED_MODEL_PATTERN)

        if OLD_TITLE not in text:
            raise RuntimeError(
                f"paper_template.tex has drifted: expected \\newcommand{{\\Title}} "
                f"line not found. Update {template_path} or this script."
            )
        if OLD_AUTHOR not in text:
            raise RuntimeError(
                f"paper_template.tex has drifted: expected literal author block not found. "
                f"Update {template_path} or this script."
            )
        if not UNCOMMENTED_MODEL_RE.search(text):
            raise RuntimeError(
                f"paper_template.tex no longer has an uncommented \\input{{sections/model}}; "
                f"verify asset version at {template_path}."
            )

        text = text.replace(OLD_TITLE, fr"\newcommand{{\Title}}{{{title}}}", 1)
        text = text.replace(OLD_AUTHOR, fr"\newcommand{{\Author}}{{{author}}}", 1)
        text = UNCOMMENTED_MODEL_RE.sub(
            r"%% \\input{sections/model}  %% Uncomment if paper has a theoretical model",
            text,
            count=1,
        )

        if "Paper Title: A Subtitle if Needed" in text:
            raise RuntimeError("literal title leaked into rendered main.tex")
        if UNCOMMENTED_MODEL_RE.search(text):
            raise RuntimeError("\\input{sections/model} not commented out in rendered main.tex")

        if dst is not None:
            dst.write_text(text)

    def _load_state_manager(self):
        """Import the gan plugin's state_manager or RAISE (no fallback).

        The retired inline fallback minted a PRE-WIDE-era schema — every
        field the live loop no longer reads. state_manager.DEFAULT_STATE is
        the single schema owner; without it, GAN state init fails loud.
        Also used as the run() PREFLIGHT so the failure lands before any
        scaffold mutation."""
        if self.GAN_SCRIPTS.exists():
            try:
                import importlib.util
                mod_spec = importlib.util.spec_from_file_location(
                    "state_manager", self.GAN_SCRIPTS / "state_manager.py"
                )
                if mod_spec and mod_spec.loader:
                    sm = importlib.util.module_from_spec(mod_spec)
                    mod_spec.loader.exec_module(sm)
                    return sm
            except Exception as e:
                self.warn(f"state_manager import failed ({e}) — state init "
                          f"cannot proceed (no inline fallback)")
        raise RuntimeError(
            f"GAN state init requires the gan plugin's state_manager "
            f"({self.GAN_SCRIPTS / 'state_manager.py'}) — it is missing or "
            f"failed to import. Install/repair the gan plugin and re-run; "
            f"everything scaffolded so far is idempotent."
        )

    def _init_gan_state(self) -> dict:
        """Initialize GAN state via the gan plugin's state_manager (the
        single schema owner) — fail-loud, no inline fallback. Errors from
        `init_state` itself — FileExistsError (a concurrent creator already
        won the create-only race), validation ValueErrors, anything else —
        PROPAGATE; an overwrite must never be the "recovery" from a refused
        canonical create.
        """
        sm = self._load_state_manager()  # raises when unavailable — no fallback
        result = sm.init_state(
            str(self.project_path),
            entry_point=self.entry_point,
            idea={"title": self.title},
            target_journal=self.target_journal,
        )
        self.log(f"Initialized GAN state via state_manager (entry: {self.entry_point})")
        return result

    def parse_gitignore(self, content: str) -> tuple[set[str], list[str]]:
        """Parse gitignore content into patterns and sections."""
        patterns = set()
        sections = []
        current_section = None

        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("# =") and "=" in stripped:
                # Section header
                current_section = stripped
                sections.append(current_section)
            elif stripped and not stripped.startswith("#"):
                patterns.add(stripped)

        return patterns, sections

    def merge_gitignore_file(self) -> None:
        """Create .gitignore from the template, or regenerate the
        producer-registry block IN PLACE, append the template patterns still
        missing, and list the volatile .gan/ files the git index still
        tracks (executed under --force, print-only otherwise — design §7:
        cleanup is never silent)."""
        gitignore_path = self.project_path / ".gitignore"
        template_path = self.script_dir / "gitignore_template.txt"

        if not gitignore_path.exists():
            if self.dry_run:
                self.log("Would create .gitignore from template", action=True)
            else:
                shutil.copy(template_path, gitignore_path)
                self.log("Created .gitignore from template", action=True)
            self._untrack_volatile(execute=self.force)
            return

        from gan_producer_registry import generate_gitignore_block, replace_block
        existing_content = gitignore_path.read_text()
        template_content = template_path.read_text()
        updated = replace_block(existing_content, generate_gitignore_block())

        existing_patterns, _ = self.parse_gitignore(updated)
        template_patterns, _ = self.parse_gitignore(template_content)
        block_patterns, _ = self.parse_gitignore(generate_gitignore_block())
        missing = sorted((template_patterns - block_patterns) - existing_patterns)
        if missing:
            updated = updated.rstrip("\n") + (
                f"\n\n# =============================================================================\n"
                f"# Added by init_project ({datetime.now().strftime('%Y-%m-%d')})\n"
                f"# =============================================================================\n"
                + "\n".join(missing) + "\n")

        if updated == existing_content:
            self.log(".gitignore already current (registry block + template patterns)")
        elif self.dry_run:
            self.log(f"Would rewrite .gitignore (registry block regenerated in place"
                     f"{', +' + str(len(missing)) + ' template patterns' if missing else ''})",
                     action=True)
        else:
            if self.backup:
                self.create_backup(gitignore_path)
            gitignore_path.write_text(updated)
            self.log(f"Rewrote .gitignore (registry block regenerated in place"
                     f"{', +' + str(len(missing)) + ' template patterns' if missing else ''})",
                     action=True)
        self._untrack_volatile(execute=self.force)

    def _git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        r = subprocess.run(["git", "-C", str(self.project_path), *args],
                           capture_output=True, text=True)
        if check and r.returncode:
            raise RuntimeError(f"git {' '.join(args[:3])}… failed (rc={r.returncode}): {r.stderr.strip()[:500]}")
        return r

    def _is_git_repo(self) -> bool:
        return (self.project_path / ".git").exists()

    def _untrack_volatile(self, *, execute: bool) -> None:
        """Registry-scoped index cleanup: the exact `git rm --cached` list
        from gan_producer_registry.gan_index_cleanup (git's own check-ignore in a
        scratch repo against the generated policy). Working-tree copies are
        never touched."""
        if not self._is_git_repo():
            return
        from gan_producer_registry import gan_index_cleanup
        commands = list(gan_index_cleanup(str(self.project_path))["commands"])
        if not commands:
            self.log("git index: no volatile .gan/ files tracked")
            return
        paths = [c.split(" ", 3)[3] for c in commands]
        if not execute or self.dry_run:
            verb = "Would untrack" if (execute and self.dry_run) else "REVIEW — run to untrack"
            self.log(f"{verb} {len(paths)} volatile tracked file(s):", action=execute)
            for c in commands:
                print(f"    {c}")
            return
        self._git("rm", "--cached", "-q", "-f", "--", *paths)  # -f: staged renames differ from HEAD; --cached never touches the tree
        self.log(f"Untracked {len(paths)} volatile file(s) from the git index "
                 f"(working tree untouched)", action=True)

    def parse_claude_md_sections(self, content: str) -> dict[str, str]:
        """Parse CLAUDE.md into sections by ## headers."""
        sections = {}
        current_header = None
        current_content = []

        for line in content.splitlines():
            if line.startswith("## "):
                if current_header:
                    sections[current_header] = "\n".join(current_content)
                current_header = line[3:].strip()
                current_content = []
            elif current_header:
                current_content.append(line)

        if current_header:
            sections[current_header] = "\n".join(current_content)

        return sections

    def merge_claude_md_file(self) -> None:
        """Merge template sections into existing CLAUDE.md."""
        claude_path = self.project_path / "CLAUDE.md"
        template_path = self.script_dir / "gan_claude_md_template.txt"

        if not template_path.exists():
            raise FileNotFoundError(f"CLAUDE.md template missing: {template_path}")

        template_content = template_path.read_text() % {
            "title": self.title,
            "target_journal": self.target_journal,
            "hypothesis": "TBD — populate after Stage 1 (Validate) converges",
        }

        if not claude_path.exists():
            if self.dry_run:
                self.log("Would create CLAUDE.md from GAN template", action=True)
            else:
                claude_path.write_text(template_content)
                self.log("Created CLAUDE.md from GAN template", action=True)
            return

        if not self.merge_claude:
            self.log("Skipping CLAUDE.md (already exists, use --merge-claude to update)")
            return

        existing_content = claude_path.read_text()
        existing_sections = self.parse_claude_md_sections(existing_content)
        template_sections = self.parse_claude_md_sections(template_content)

        # Find missing sections
        missing_headers = set(template_sections.keys()) - set(existing_sections.keys())
        if not missing_headers:
            self.log("CLAUDE.md already contains all template sections")
            return

        if self.backup:
            self.create_backup(claude_path)

        # Append missing sections
        append_content = f"\n\n<!-- Added by init_project ({datetime.now().strftime('%Y-%m-%d')}) -->\n"
        for header in sorted(missing_headers):
            append_content += f"\n## {header}\n{template_sections[header]}\n"

        if self.dry_run:
            self.log(f"Would add {len(missing_headers)} sections to CLAUDE.md: {', '.join(missing_headers)}", action=True)
        else:
            with open(claude_path, "a") as f:
                f.write(append_content)
            self.log(f"Added {len(missing_headers)} sections to CLAUDE.md", action=True)

    def init_git(self) -> None:
        """Initialize git repository if needed.

        The branch is pinned to `main` explicitly rather than left to git's
        fallback: `init.defaultBranch` is unset on this machine, so a bare
        `git init` produced `master` and every project then pushed a `master`
        that GitHub adopted as the repo default (2026-09-13).
        """
        git_dir = self.project_path / ".git"
        if git_dir.exists():
            self.log("Git repository already exists")
            return

        if self.dry_run:
            self.log("Would initialize git repository on branch main", action=True)
            self.log("Would create initial commit", action=True)
        else:
            subprocess.run(["git", "init", "-b", "main"], cwd=self.project_path, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=self.project_path, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial project setup"],
                cwd=self.project_path,
                check=True,
                capture_output=True,
            )
            self.log("Initialized git repository with initial commit", action=True)

    def run(self) -> bool:
        """Three explicit states, nothing inferred from partial contents:

        - live GAN project (.gan/state.jsonl present) → MAINTENANCE: missing
          layout dirs, the LaTeX skeleton iff draft/main.tex is absent, the
          registry-regenerated .gitignore (untrack list printed; --force
          executes it), runtime seeds; --merge-claude / --migrate-data opt in.
        - existing non-GAN directory (.git / CLAUDE.md / .gitignore / src)
          → refused without --force (a mis-aimed invocation must never
          scaffold an arbitrary cwd); --force scaffolds in place,
          create-if-absent throughout — also the retry for a scaffold that
          failed part-way.
        - anything else → full scaffold.
        """
        # PREFLIGHT: state init fails loud without the gan plugin's
        # state_manager — verify it BEFORE any scaffold mutation, so a failed
        # run creates nothing that a retry would misclassify. The same module
        # owns the journal tier: the raw --journal value is normalized and
        # floored ONCE here, so the header, CLAUDE.md and .gan/state.jsonl
        # carry the same code.
        self.target_journal = self._load_state_manager().journal_floor(self.target_journal)

        state_path = self.project_path / ".gan" / "state.jsonl"
        if state_path.exists():
            mode = "maintain"
        elif (self.project_path / ".gan" / "state.json").exists():
            mode = "migrate"
        elif self.is_existing_project():
            mode = "scaffold" if self.force else "refuse"
        else:
            mode = "scaffold"

        print(f"\n{'='*60}")
        print(f"Project: {self.project_name}")
        print(f"Path: {self.project_path}")
        print(f"Mode: {mode}")
        print(f"GAN adversarial research system | Target journal: "
              f"{self._recorded_target_journal() if mode == 'maintain' else self.target_journal}")
        if self.dry_run:
            print("DRY RUN - No changes will be made")
        print(f"{'='*60}\n")

        if mode == "migrate":
            # a fresh journal beside the legacy document would shadow the
            # project's identity and history (state_manager.create_state
            # refuses it too); the converter is the only way forward
            print("GAN project on the legacy .gan/state.json layout — nothing changed.")
            print("  Migrate it first: python3 ~/.claude/plugins/gan/scripts/"
                  f"journal_migrate.py {self.project_path}")
            return False

        if mode == "refuse":
            print("Existing directory without GAN state — nothing changed.")
            print("  --force            Scaffold the GAN project in place (create-if-absent)")
            print("\nUse --dry-run to preview changes.")
            return True

        if mode == "maintain":
            self.create_folders()
            if self.migrate_data:
                self.create_data_directories()
                self.create_symlinks()
            self._preflight_assets()
            self.create_draft_skeleton()
            self.merge_gitignore_file()
            self.merge_claude_md_file()
            self._seed_runtime_settings()
            self._print_summary()
            return True

        # ASSET PREFLIGHT: both latex skill assets must exist and carry the
        # literals this initializer substitutes — checked BEFORE any folder
        # or file is created.
        self._preflight_assets()

        self.create_folders()
        self.create_data_directories()
        self.create_symlinks()
        self.create_draft_skeleton()
        self.create_gan_state()
        self.merge_gitignore_file()
        self.merge_claude_md_file()
        self.init_git()
        self._print_summary()
        return True

    def _print_summary(self) -> None:
        print(f"\n{'='*60}")
        print("Summary")
        print(f"{'='*60}")

        if self.actions:
            print(f"\nActions performed: {len(self.actions)}")
            for action in self.actions:
                print(f"  - {action}")

        if self.warnings:
            print(f"\nWarnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"  ! {warning}")

        if not self.actions and not self.dry_run:
            print("\nNo changes needed - project already configured.")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize or update a GAN research project with standard structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # New project — JF and Hulai Zhang are silent defaults
  %(prog)s my-new-project --title "My Paper Title"

  # Override journal only when explicitly requested by the user
  %(prog)s my-new-project --title "..." --journal RFS
  %(prog)s my-new-project --title "..." --journal QJE    # the review bar only; every draft keeps the working-paper format
  # a venue outside the top-5 / top-3 tier is floored to JF by the plugin's state writer

  # Maintain a live GAN project (missing dirs, skeleton if no main.tex,
  # registry-regenerated .gitignore; --force executes the untrack list)
  %(prog)s --path ~/proj/NAME [--force]

  # Preview any mode
  %(prog)s --path ~/proj/NAME --dry-run

  # Opt-in maintenance: CLAUDE.md sections / data symlinks
  %(prog)s --path ~/proj/NAME --merge-claude --backup

  # Migrate data directories to symlinks
  %(prog)s --migrate-data --backup
""",
    )

    parser.add_argument(
        "project_name",
        nargs="?",
        help="Project name (defaults to current directory name)",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Project path (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without making them",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Backup files before modifying",
    )
    parser.add_argument(
        "--merge-claude",
        action="store_true",
        help="Add missing sections to existing CLAUDE.md",
    )
    parser.add_argument(
        "--migrate-data",
        action="store_true",
        help="Convert data/temp directories to symlinks",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Existing non-GAN directory: scaffold the GAN project in place (create-if-absent). Live GAN project: execute the volatile .gan/ untrack list instead of printing it",
    )
    parser.add_argument(
        "--title",
        default="Untitled Research Project",
        help="Paper title (default: 'Untitled Research Project')",
    )
    parser.add_argument(
        "--author",
        default="Hulai Zhang",
        help=(
            "Author name, bare (default: 'Hulai Zhang'). The affiliation "
            "\\thanks{} footnote is hardcoded in the latex skill's paper "
            "template — do NOT pass a \\thanks{} block here. Override only "
            "when the user explicitly requests a different author."
        ),
    )
    parser.add_argument(
        "--entry-point",
        choices=["user_topic", "ideate", "brainstorm", "polished_project"],
        default="user_topic",
        help="GAN entry point: user_topic, ideate, brainstorm, or polished_project",
    )
    parser.add_argument(
        "--journal",
        # No `choices`: a code, abbreviation or full name is normalized and
        # any venue outside the top-5 econ / top-3 finance tier is floored to
        # JF by the state writer (state_manager.journal_floor) — never an
        # argparse refusal.
        default="JF",
        help="Target journal (default: JF; override only on explicit user "
             "request): AER, Econometrica, QJE, JPE, RES, JF, JFE or RFS (code "
             "or full name); any other venue is floored to JF. It is the GAN "
             "review bar only: every draft keeps the working-paper format; a "
             "journal's format is applied on acceptance (latex journal_format.py).",
    )

    args = parser.parse_args()

    project_path = args.path.resolve()
    project_name = args.project_name or project_path.name

    initializer = ProjectInitializer(
        project_name=project_name,
        project_path=project_path,
        dry_run=args.dry_run,
        backup=args.backup,
        merge_claude=args.merge_claude,
        migrate_data=args.migrate_data,
        force=args.force,
        title=args.title,
        author=args.author,
        entry_point=args.entry_point,
        target_journal=args.journal,
    )

    success = initializer.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
