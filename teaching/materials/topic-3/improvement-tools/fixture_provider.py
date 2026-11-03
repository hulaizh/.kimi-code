"""Return manually written outputs to demonstrate checks, without calling a model."""
import json


def call_api(prompt, options, context):
    values = context["vars"]
    if prompt.startswith("FIXTURE: baseline"):
        execution_at = values["available_at"]
        evidence_id = "PRICE_01"
    elif prompt.startswith("FIXTURE: candidate"):
        execution_at = values["earliest_execution_at"]
        evidence_id = "MISSING_02"
    else:
        raise ValueError("This provider accepts only the two labelled fixtures")
    return {"output": json.dumps({
        "signal_available_at": values["available_at"],
        "execution_at": execution_at,
        "evidence_id": evidence_id,
        "provenance": "MANUALLY_WRITTEN_FIXTURE"
    })}
