# Topic 3 revision checks

Both English and Chinese PDFs contain exactly 60 pages, with two sections,
no standalone break or lab pages, and four worked tables (pages 7, 11, 49, 52).
Twenty-one explanatory table frames were converted to short itemized lists at
the user's request. The instructor guide matches the 240-minute schedule.

Both decks compile successfully with no overfull boxes, missing glyphs, or
undefined references. All 120 pages received visual inspection. English
diagram-label breaks and the Chinese page-9 overlap were corrected and
rechecked at full-page scale. A separate copy-editor reviewed bilingual meaning,
all Chinese pages, and the manually written comparison fixtures.

The legacy validator has no unexpected findings. Its Roadmap-title requirement,
relative style-path warning, and visual-primacy warnings are documented
exceptions to match the user's manual contents and itemize preferences.

The offline companion example passes its expected timing/evidence matrix and
boundary checks. It calls no model. The optional promptfoo CLI and live
DSPy/GEPA/MLflow integrations were not run; the slides identify the external
tools as examples or extensions. No measured prompt-improvement claim is made.

Build logs, rendered pages, extracted text, fixture results, and PDF hashes are
under `teaching/logs/topic-3/revision/` (gitignored). Compiled PDFs are committed
with their source changes; temporary LaTeX files are cleaned after validation.
