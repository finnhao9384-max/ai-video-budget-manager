# Data Guide

## Pricing

`pricing/tapnow-2026-09-26.json` is transcribed from the release Skill. It expands shared prices into explicit mode/model configurations: Sunburst and Flare share prices, Banana text/reference modes share prices, and video modes have separate records. Model labels, prices and duration limits originate from author-collected generation-page records and subsequent clarifications. This is a dated pricing snapshot; the project does not retrieve live tariffs.

## Examples

`examples/rough-story.txt` is an original fictional prompt prepared for a future trial. No TapNow result is claimed for it.

`examples/commercial-medium-plan.json` reconstructs the Commercial transcript's explicit Medium task quantities for deterministic checking. The 6,000-credit cap is an illustrative test input, not a recorded creator budget. The checker is not a parser of the original conversation.

## Transcripts

| File | Contents |
|---|---|
| `transcripts/aura.md` | 22-shot initial plan and 5,000-credit / minimum-720P follow-up |
| `transcripts/commercial.md` | 9-shot initial plan and three Medium alternatives |
| `transcripts/right-frequency.md` | 30-shot initial plan and MiniMax/Seedance comparison |

The project author ran these three trials in TapNow and exported the conversations. They were identified as tests of the latest Skill at the time, but the installed file hash, host-model identifiers, runtime settings and execution timestamps were not recorded. `transcripts/manifest.json` records source filenames, original byte hashes and normalization. Unicode line separators and fullwidth colons were normalized for readability; substantive prompts, responses and errors remain unchanged.

The transcripts include the screenplay material used in the tests. This repository does not grant redistribution rights to third-party source material.

## Actual Usage

`actual-usage/golden-touch.md` preserves the project author's corrected production summary. On 2026-10-04 the author corrected the record to show 18 tasks, rather than 19, in the single-attempt image group. The resulting rows sum to 37 image attempts, 555 image credits, 20 video attempts, 123 generated video seconds, 2,952 video credits and 3,507 total credits.

The source's label "single pass" is retained from the production log: the record includes multiple generation attempts. Here it denotes one production run including retries, not first-pass generation. Three different image models are mentioned under one 15-credit rate without model-specific settings; the summary does not establish the settings used for each model.

The author also acted as the creator in this production case: I used the Skill's model choices and attempt recommendations and found them helpful for controlling spending. This is my own qualitative assessment, not independent user feedback or a quantified saving.

The evaluation dataset does not include billing screenshots, an itemized settled ledger, a completed-video acceptance audit, or a matched baseline. The production summary is therefore a self-recorded cost record rather than independently verified billing.
