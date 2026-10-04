# Evaluation Methods and Findings

## Objective and Evidence

This evaluation assesses Budget Manager as a planning aid: calculation correctness, traceable prices, valid parameters, budget-fit reasoning, task coverage, actionable alternatives, and honest treatment of uncertainty.

Evidence consists of three TapNow conversations recorded by the project author (each with an initial answer and one follow-up), a corrected grouped production-cost summary, and the author's experience using the Skill. It is a small convenience sample, not a held-out benchmark or repeated-run reliability study. The exact installed Skill hash and host model for each run were not captured; the author tested the version then considered current.

## Why Final-Spend Error Is Not the Primary Score

The original planning document proposed a MAPE target of at most 25% across held-out shots from three pilots. That target has not been demonstrated. The final evaluation instead emphasizes useful and correct planning because attempt counts are allowances and the creator may add, modify or abandon work.

An estimate is only comparable to actual consumption when scope, parameters and acceptance criteria are aligned. The Golden Touch run changed scope: the original Medium plan had 13 images and 9 video tasks, whereas the actual grouped record describes 26 image tasks and 6 video shots. The difference between 5,295 planned credits and 3,507 recorded credits therefore does not measure savings or forecast accuracy.

## Reproduction

Run from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 evals/run_checks.py
```

The first command tests the separate checker against known arithmetic, budget boundaries, model-specific minima, unsupported settings, duplicate IDs, invalid attempts and promotion expiry. Passing these does not establish that the LLM follows the Skill.

The second command reads `test_cases.json` and retained transcripts, writes `results/calculation-checks.json`, and exposes both successful checks and the recorded AURA detail-to-summary inconsistency. A successful audit execution does not mean every observed output passed.

## Scored Calculation Checks

Each initial Low/Medium/High total is a separate case. The nine cases are manually extracted into groups of quantity or seconds, unit price, and attempt count. Summing these terms checks arithmetic conditional on the output's declared plan, not whether the plan is optimal or creatively sufficient.

- Initial tier totals: 9 of 9 reconcile.
- AURA fixed-budget detail table: listed subtotals sum to 4,066, but it reports 4,087. Its summary calculation for 21 text-to-image images plus one reference image supports 4,087; the detailed table lists only 20 text-to-image images. This is an internal scope reconciliation issue within one response. Shot additions, removals or revisions during later production are normal and are not scored as this type of error. The record does not identify a scope revision explaining the difference within this response.
- Right Frequency shot table: 30 rows sum to 189 final-edit seconds and 200 generated seconds. A five-second model minimum gives 210 seconds. Its 218-second timeline end marker is a separate ambiguity requiring review before production.

No overall success percentage is calculated. Selected totals and one targeted inconsistency are not a representative random sample of all calculations.

## Qualitative Findings

| Observation | Evidence | Assessment |
|---|---|---|
| Three tiers and explicit attempts | All three initial outputs | Present in the recorded examples |
| MiniMax visibility | Candidate tables and follow-ups | Present; quality recommendations are assessed separately from model coverage |
| Fixed-budget follow-up | AURA: 5,000 credits and minimum 720P | Offers custom 7-image/2-video attempt plans and discloses default Low-tier insufficiency; custom counts are not a standard tier |
| Experience-based quality recommendations | Judgments about particle handling, motion, text clarity and consistency | The author identifies creative experience and community perceptions as their basis; no specific community sources or controlled project benchmark are documented |
| Incomplete cost comparison | Commercial labels H3 2K as pricier than a Seedance 2.0 1080P comparison, while its listed subtotals show 1,044 versus 2,160 | Different retry needs could change cost per usable result, but the comparison does not quantify them; the listed costs alone do not establish a Seedance cost advantage |
| Model-name precision | Right Frequency uses MiniMax at family level when discussing the absence of 480P | H3 has no 480P option in the snapshot; H3 Max does. The statement should identify H3 specifically, rather than generalize to the family |
| Overbroad affordability explanation | AURA excludes H3 2K as leaving insufficient first-pass margin; its listed rates imply 2,552 video + 81 image = 2,633, below 5,000 | Exclusion rationale is unsupported; under a different retry policy feasibility must be recalculated |
| Presentation constraints | Some output tables exceed six columns | Instruction-following limitation |
| Author experience | The author used the model and attempt recommendations during production | Positive self-evaluation; no independent participant |

## Interpreting Model Recommendations

The author considers Seedance 2.0 stronger overall than MiniMax H3 based on creative experience and describes different models as having scene-specific strengths recognized in the creator community. This is the author's stated basis for recommendation, not a quality result measured by this project. Specific community references have not been catalogued.

A useful cost comparison must consider both the price of an attempt and the number of attempts needed to obtain usable material. A model with a higher unit price may be more economical if it requires fewer attempts. The current records do not establish model-specific retry rates or matched acceptance criteria, so they do not demonstrate that advantage. Future comparisons should state the assumed attempts for each model and recalculate the full scenario rather than infer total cost from perceived capability alone.

## Production Evidence

After the author corrected an overcount in the single-attempt image group, the record reconciles to 37 image attempts at 15 credits = 555, and 123 generated video seconds at 24 credits = 2,952. Total: 3,507 credits. Individual video groups used one to six attempts. This illustrates heterogeneous iteration needs, not a calibrated distribution of success probabilities.

In this production case, I found that the model-selection advice and attempt recommendations helped me control spending. As the project author and test creator, I cannot treat this self-evaluation as independent validation or evidence of causal savings. No independent itemized billing ledger or matched no-Skill production baseline is available.

## Remaining Evaluation Gaps

Rough-story behavior, repeated-run consistency, independently verified capability constraints, live settlement agreement, cross-platform portability, and comparative creator outcomes remain unmeasured. These results describe the recorded trials only. Future revisions will need separate versioned test records.
