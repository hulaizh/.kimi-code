# Topic 3: inspect a proposed improvement

Companion evidence for slides 49 and 52. The two outputs are manually written
fixtures. No model is called and no prompt-improvement measurement is claimed.
They demonstrate why fixing timing while losing a valid evidence reference
does not justify adoption.

The retained case fixes availability at 29 September 2026, 15:00 +08:00, and
the earliest permitted execution at 30 September 2026, 09:30 +08:00. These are
synthetic fixture assumptions, not an exchange-calendar service.

Run the checks using Python's standard library:

```sh
python3 check_example.py
```

Expected matrix:

| Fixture | Timing | Evidence reference |
|---|---|---|
| Baseline | Fail: execution at the signal's availability | Pass: PRICE_01 exists |
| Candidate | Pass: execution at the permitted next timestamp | Fail: MISSING_02 does not exist |

The test also rejects a false availability declaration, an early trade, a naive
timestamp, malformed output, and missing fields, while accepting an equivalent
timezone representation. These checks validate this narrow teaching contract;
they do not establish complete financial correctness or operational safety.

For the promptfoo comparison UI, use an already installed promptfoo CLI:

```sh
PROMPTFOO_PYTHON=python3 promptfoo eval --config promptfooconfig.json
promptfoo view
```

The evaluation intentionally contains failures. This is a local Python provider;
no provider credentials are needed. The promptfoo CLI is optional. The standard
library script reproduces the same checks without installing it.

For actual prompt evaluation, replace the scripted provider with a configured
model provider or QT adapter, remove fixture-selection markers, preserve the
complete task, archive actual outputs, and evaluate on independent held-out
cases. Do not present the fixture matrix as model performance. DSPy/GEPA and
MLflow are taught as external extensions; this example does not integrate them
into QT.
