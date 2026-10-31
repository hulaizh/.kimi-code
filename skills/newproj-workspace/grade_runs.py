#!/usr/bin/env python3

import json
from pathlib import Path

ITERATION = Path(__file__).parent / "iteration-1"


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def moved(project, relative):
    destination = project / relative
    return destination.is_file() and not (project / destination.name).exists() and destination.stat().st_size > 0


def result(text, passed, evidence):
    return {"text": text, "passed": bool(passed), "evidence": evidence}


def grade(eval_dir, run_name):
    metadata = json.loads(read(eval_dir / "eval_metadata.json"))
    run_dir = eval_dir / run_name
    outputs = run_dir / "outputs"
    project = outputs / "project"
    log = read(outputs / "run.log")
    assertions = metadata["assertions"]
    results = []

    if metadata["eval_id"] == 1:
        checks = [
            moved(project, "src/analysis.py"),
            moved(project, "tests/test_analysis.py"),
            all(
                moved(project, relative)
                for relative in [
                    "data/raw/prices.csv",
                    "output/figures/chart.png",
                    "report/memo.pdf",
                    "slides/deck.pptx",
                ]
            ),
            (project / "notes.txt").is_file() and (project / "pyproject.toml").is_file(),
            (project / "AGENTS.md").is_file()
            and all((project / relative).is_dir() for relative in ["data/raw", "src", "tests", "report", "slides"]),
        ]
        evidence = [
            "Checked src/analysis.py exists, is nonempty, and root analysis.py is absent.",
            "Checked tests/test_analysis.py exists, is nonempty, and root test_analysis.py is absent.",
            "Checked all four destination files exist, are nonempty, and their root counterparts are absent.",
            "Checked notes.txt and pyproject.toml remain in the project root.",
            "Checked AGENTS.md and representative standard directories exist.",
        ]
    elif metadata["eval_id"] == 2:
        checks = [
            read(project / "analysis.py") == "source",
            read(project / "src/analysis.py") == "destination",
            read(project / "data/raw/prices.csv") == "date,price\n2026-01-01,100\n" and not (project / "prices.csv").exists(),
            "Skipped" in log and "analysis.py" in log and "destination exists" in log,
        ]
        evidence = [
            f"Root analysis.py content: {read(project / 'analysis.py')!r}.",
            f"Destination analysis.py content: {read(project / 'src/analysis.py')!r}.",
            "Checked exact CSV content at data/raw/prices.csv and absence at the root.",
            "Checked run.log for the explicit collision skip message.",
        ]
    else:
        original_files = sorted(path.name for path in project.iterdir()) == ["analysis.py", "prices.csv"]
        checks = [
            read(project / "analysis.py") == 'print("ok")\n' and read(project / "prices.csv") == "date,price\n2026-01-01,100\n",
            original_files,
            "Would move" in log and "src/analysis.py" in log and "data/raw/prices.csv" in log,
            "Would create" in log and "\nMoved " not in log and not log.startswith("Moved "),
        ]
        evidence = [
            "Checked exact contents of both root files.",
            f"Project root entries after the run: {sorted(path.name for path in project.iterdir())}.",
            "Checked run.log for both planned move destinations.",
            "Checked for scaffold preview messages and absence of actual move messages.",
        ]

    for text, passed, detail in zip(assertions, checks, evidence):
        results.append(result(text, passed, detail if passed else f"Failed. {detail}"))
    passed_count = sum(item["passed"] for item in results)
    grading = {
        "expectations": results,
        "summary": {
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "total": len(results),
            "pass_rate": passed_count / len(results),
        },
    }
    (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n", encoding="utf-8")


for eval_dir in sorted(ITERATION.glob("eval-*")):
    for run_name in ["with_skill", "old_skill"]:
        if (eval_dir / run_name / "outputs").is_dir():
            grade(eval_dir, run_name)
