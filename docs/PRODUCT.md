# Product Definition

## Persona

An AI video creator using a credit-based infinite canvas, working from a rough story or detailed storyboard and deciding how to allocate a limited generation budget. The creator judges whether outputs are usable and retains control over production.

## Inputs and Outputs

Inputs: story/script/storyboard, target runtime, existing assets, aspect ratio, model or resolution requirements, and an optional credit cap. Missing nonessential information becomes an explicit provisional assumption.

Outputs: reusable asset inventory, shot and generation-task breakdown, three specific model/parameter plans, attempt allowances, first-pass and scenario costs, budget-fit explanations, operating steps, exclusions and follow-up choices. All release Skill outputs are instructed to be English.

## Design Trade-offs

- **Foundation model versus rules:** the host LLM interprets incomplete creative language; explicit price rules make the intended calculation inspectable. Rules alone cannot reliably invent a sensible shot plan from a rough story. However, embedding formulas in instructions does not make runtime arithmetic deterministic.
- **Build versus buy:** the project uses TapNow's existing Agent and canvas interface. The project-specific work consists of the Skill, pricing snapshot, planning rules, examples, and evaluation tooling. This avoids an additional API integration but introduces dependence on the host's capabilities and model behavior.
- **Skill versus separate application:** a single upload lowers setup effort and fits an existing workflow. It offers less control over runtime, tool invocation, model version and output consistency than a standalone application.
- **Snapshot versus live pricing:** versioned prices enable reproduction and audit. They can become stale; the MVP does not retrieve live tariffs or account-specific discounts.
- **Scenario allowance versus statistical prediction:** explicit attempts are understandable and editable, but not calibrated success probabilities. They do not guarantee final costs.
- **Portability versus integration:** platform-neutral task concepts can be reused. Pricing rules and host-specific installation still need validation on each platform.

## Metrics

| Metric | Intended target | Evidence currently reached |
|---|---|---|
| Tier arithmetic | All scored totals reconcile | 9/9 selected initial tier totals reconcile; a separate AURA detail-to-summary inconsistency remains |
| Price and parameter validity | Every priced task maps to a valid recorded configuration | Checker validates entered configurations; complete semantic transcript audit not finished |
| Budget-fit classification | Correct decisions at tested cap boundaries | Offline checker boundary tests; recorded AURA interaction contains qualified reduced-attempt options and documented issues |
| Planning coverage | Required shots represented and shared assets not duplicated | Transcripts present 22, 9 and 30 shots; this is not an independent creative-quality score |
| Recommendation transparency | Distinguish recorded specifications, experience-based judgments and measured results | The author identifies creative experience and community perceptions as the basis for quality advice; specific community sources and controlled comparisons are not documented |
| Creator usefulness | Clear, actionable model and attempt advice | The author used both during production and reported that they helped control spending; no independent user study |
| Actual-consumption MAPE | Originally proposed <=25% | Not established; no comparable frozen-scope production benchmark |

Targets are listed separately from observed results. The three recorded examples use detailed scripts/storyboards; rough-draft handling still requires a recorded test.

## Future Work

Connect a deterministic calculator to the host if supported; add independently checked live pricing; evaluate rough scripts and repeated runs; introduce recorded per-task charges and acceptance decisions; compare against ordinary Agent prompting without the Skill; validate a second platform. These are future directions, not implemented features.
