# Skill Benchmark: newproj

**Model**: Kimi Code subagent; exact model ID not reported
**Date**: 2026-10-31T03:30:48Z
**Evals**: 1, 2, 3 (1 run each per configuration)

## Summary

| Metric | With Skill | Old Skill Baseline | Delta |
|--------|------------|--------------------|-------|
| Pass Rate | 100% | 55% | +0.45 |
| Time | 54.4s | 41.2s | +13.2s |
| Tokens | Not reported | Not reported | N/A |

## Notes

- The baseline is the pre-change skill snapshot, not a run without any skill.
- Each case ran once per version; the table does not estimate run-to-run variance.
- Basic scaffold creation and no-overwrite behavior passed in both versions and do not distinguish the change.
- The old version failed the recognized-file routing and dry-run move-preview checks.
- Token counts were unavailable in the runtime notifications.