"""Reproduce the slide matrix and test temporal/evidence boundaries offline."""
import json
from pathlib import Path

from fixture_provider import call_api
from timing_assert import get_assert

root = Path(__file__).resolve().parent
config = json.loads((root / "promptfooconfig.json").read_text())
results = []
for version in ["baseline", "candidate"]:
    prompt = (root / f"{version}.txt").read_text()
    row = {"version": version}
    for criterion in ["timing", "evidence"]:
        context = {"vars": {**config["defaultTest"]["vars"], "criterion": criterion}}
        output = call_api(prompt, {}, context)["output"]
        row[criterion] = get_assert(output, context)["pass"]
    results.append(row)
assert results == [
    {"version": "baseline", "timing": False, "evidence": True},
    {"version": "candidate", "timing": True, "evidence": False},
]

context = {"vars": {**config["defaultTest"]["vars"], "criterion": "timing"}}
valid = json.loads(call_api((root / "candidate.txt").read_text(), {}, context)["output"])
for changes in [
    {"execution_at": "2026-09-29T15:00:00+08:00"},
    {"execution_at": "2026-09-30T09:29:59+08:00"},
    {"execution_at": "2026-09-30T09:30:00"},
    {"signal_available_at": "2026-09-29T14:00:00+08:00"},
]:
    assert not get_assert(json.dumps({**valid, **changes}), context)["pass"]
assert not get_assert("{}", context)["pass"]
assert not get_assert("not JSON", context)["pass"]
utc_record = {**valid, "execution_at": "2026-09-30T01:30:00+00:00"}
assert get_assert(json.dumps(utc_record), context)["pass"]
print(json.dumps({"provenance": "MANUALLY_WRITTEN_FIXTURES", "checks": results}, indent=2))
