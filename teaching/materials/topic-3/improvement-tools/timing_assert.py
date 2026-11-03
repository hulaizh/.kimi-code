"""Check output fields against the retained teaching-case inputs."""
import json
from datetime import datetime


def get_assert(output, context):
    values = context["vars"]
    try:
        record = json.loads(output)
        if values["criterion"] == "timing":
            available = datetime.fromisoformat(values["available_at"])
            declared = datetime.fromisoformat(record["signal_available_at"])
            execution = datetime.fromisoformat(record["execution_at"])
            earliest = datetime.fromisoformat(values["earliest_execution_at"])
            passed = all(t.utcoffset() is not None for t in [available, declared, execution, earliest])
            passed = passed and declared == available and execution > available and execution >= earliest
            reason = "Compare execution with retained availability and earliest permitted time"
        elif values["criterion"] == "evidence":
            passed = record["evidence_id"] in values["source_ids"]
            reason = "The cited source must exist in the retained case"
        else:
            raise ValueError("Unknown criterion")
    except (ValueError, TypeError, KeyError):
        passed, reason = False, "Missing or invalid structured output"
    return {"pass": bool(passed), "score": int(bool(passed)), "reason": reason}
