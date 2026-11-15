# Offline follow-up: why 36 versus 44 model requests?

This is a post-hoc analysis of the existing two executions, not another trial. No model request, provider query, implementation change, production action or publication was performed for this analysis. Original artifacts and reports remain unchanged. Four offline extraction/accounting tests pass.

## Main finding: one capped response is a major cost outlier

Pi-Bolt request **12** has the following evidence:

- Provider-reported completion tokens: **65,536**, exactly the configured cap; 438 reported reasoning tokens are included in that total.
- Raw SSE: normalized `finish_reason="tool_calls"`, **`native_finish_reason="length"`**.
- The assembled raw function call is `bash` with arguments **`{}`**. There is no `command`.
- The native tool then reports `Validation failed for tool "bash": command: missing`.
- Request **13** supplies a valid command writing `client/fleet.tsx`.
- Request 12's settled cost: **USD 0.01961726368**, including **USD 0.019267584** completion cost.
- Its relay request interval was **269.767 seconds**, an instrumented observation including upstream/network/relay work, not a clean model-generation latency.

This one response represents **52.90% of Bolt's reported completion tokens and 34.22% of its settled coding bill**.

The empty arguments exist in the saved upstream stream, before native tool validation. The relay captures and forwards those SSE lines without rewriting tool arguments or finish reasons (apart from credential redaction). The evidence therefore does not support blaming Pi-Bolt's parser for replacing a valid delivered command with `{}`.

**We cannot tell from these records why the provider reports 65,536 completion tokens while exposing an empty tool call.** We cannot reconstruct undisclosed generated content, distinguish an upstream generation/serialization/accounting problem, or establish how Pi would have handled the same response. No such same-response replay was performed. Earlier shorthand about Bolt “generating more code” would overstate the evidence: these are provider-reported completion tokens, not measured useful code volume.

The outlier remains fully included in the original totals. Removing it would not create a valid counterfactual run.

## Where the eight net additional requests appear

Both agents first obtained a passing **full project suite at request 21**. This is directly visible in their tool results: 38/38 for Pi and 40/40 for Bolt. It is not the later independent acceptance evaluation, nor proof the task was already complete.

Using the first project-file write and that first full-suite pass as post-hoc milestones:

| Phase | Pi requests | Bolt requests | Difference | Pi / Bolt tool calls |
|---|---:|---:|---:|---:|
| Initial exploration | 1–7: **7** | 1–9: **9** | +2 | 14 / 14 |
| First project write through first full-suite pass | 8–21: **14** | 10–21: **12** | −2 | 16 / 14 |
| Later refinement, documentation and verification | 22–35: **14** | 22–43: **22** | **+8** | 18 / 28 |
| Final response | **1** | **1** | 0 | 0 / 0 |
| Total | **36** | **44** | **+8** | **48 / 56** |

The initial exploration used the same number of tool calls, grouped into different numbers of model requests. This was not eight extra initial search calls.

The later Bolt trajectory includes observable actions such as:
- R22: a contract/JSON-schema inspection command.
- R23: standalone/scroll-container changes.
- R29–30 and R34: additional schema aliases and accepted component-prop aliases.
- R33: deployment-card/navigation changes in the shell.
- R35–36: repeated tests, typecheck and boundary checks.
- R37–39: CI inspection/update and README command updates.
- R40–42: source inspection, optional health-field changes and an additional unknown-active-deliveries label.
- R43: another typecheck/boundary/Fleet test group.

Pi also continued beyond green tests: documentation, display/refinement and alias changes, repeated checks and a package dry-run. We are not calling every post-green action unnecessary; documentation/CI and untested acceptance requirements can still need work. These are counts of different trajectories, **not eight independently matched unnecessary steps**.

## Was it more failure recovery?

Not in the aggregate tool-error count:
- Pi: **6** error events, including an intentional initial red test, import/type errors, assertion repairs and the first full-suite integration failure.
- Bolt: **4** error events: a filesystem-search exit, the empty-command validation failure, a Fleet test run and a foundation test run.

All tool calls in both executions used `bash`; neither used the dedicated `edit` tool. There is no evidence for eight extra dedicated edit-tool retries. Ordinary model-driven recovery after a tool error is distinct from automatic HTTP retries; no automatic provider retry was introduced.

## What explains the bill arithmetically?

Every request reconciles to the same observed rates: USD 0.098 per million uncached prompt tokens, USD 0.00294 per million cached prompt tokens, and USD 0.294 per million completion tokens.

| Billed component | Pi | Bolt | Difference | Share of bill increase |
|---|---:|---:|---:|---:|
| Uncached prompt | $0.007274148 | $0.008271004 | $0.000996856 | 3.79% |
| Cached prompt | $0.00872309760 | $0.01263870720 | $0.00391560960 | 14.87% |
| Completion | $0.015011640 | $0.036425130 | **$0.021413490** | **81.34%** |
| Total | **$0.03100888560** | **$0.05733484120** | **$0.02632595560** | 100% |

Thus **22.22% more requests did not mechanically produce 84.90% more cost**. Token volume and composition differ; most of the cost increase is completion billing, with the capped response a major concentration.

Aggregate prompt tokens were 3,041,266 versus 4,383,278. These are repeated context processing across requests, not unique context sizes. Maximum single-request prompt sizes were **122,472 versus 141,314 tokens**. Both context growth and additional turns contribute to the aggregate difference; no causal split is identified here.

### Cache and first-response caveats

Identical initial requests did not mean identical cache state: the first Pi request reported **0 cached tokens out of 2,775**, while Bolt's reported **2,688 cached tokens out of 2,775**. The second arm therefore did not start with an equivalent cold provider cache. No claim is made that this is the only cache difference or that the benchmark caused the cache hit.

The first returned actions already differ (for example, the directory listing uses `head -200` versus `head -100`). Divergence therefore starts in the response to the identical initial request, before later implementation paths can be compared. Subsequent conversations are not identical prompts or a controlled response replay.

## What can and cannot be concluded

Supported:
1. Both original outputs passed the common independent tests and browser checks.
2. Bolt made eight more requests in total; the net phase-count difference appears after the first passing full suite.
3. Bolt's bill is dominated more by completion tokens, including one capped empty-tool response already visible on the upstream wire.
4. The original timing failures remain; all timings here are instrumented observations.

Not established:
- That Pi-Bolt's runtime caused the empty tool call or the longer trajectory.
- That Pi would avoid the same outlier under another draw.
- That either runtime has better reasoning, general coding efficiency or reliability.
- Why the upstream response's reported completion volume is not exposed as a usable tool command.

## Reproducible local evidence

- `trajectory_analysis.py`: offline extraction; no network or model calls.
- `test_trajectory_analysis.py`, `trajectory-analysis-{red,green}.log`: four tests and preserved initial failure.
- `results/coding-pair/trajectory-analysis/analysis.json`: all 80 request rows, visible tool commands, errors, usage, stream finish reasons and phase summaries. Reasoning text is not extracted.
- `results/coding-pair/trajectory-analysis/source-manifest.json`: hashes of all source artifacts read.
- `results/coding-pair/pi-bolt/relay/0012-response.sse`: raw capped empty-tool response.
- `results/coding-pair/pi-bolt/relay/events.jsonl`: request 12's settled charge and timing.
- Both `delivery/.bench-artifacts/measurement/stdout.bin` files: original tool validation and subsequent recovery.

The main pilot report remains `REPORT.md`; this supplement refines its token/trajectory interpretation without replacing or cleaning the original observations.
