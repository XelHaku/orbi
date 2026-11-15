# Pi / Pi-Bolt coding pilot: both implementations passed

**Exactly two coding executions completed, with no replay or LLM reviewer. Both original implementations passed the same independent acceptance and browser checks.** In this single observed pair, standard Pi finished sooner and used less model spend and sampled memory. These are **instrumented, descriptive observations**, not a clean-speed benchmark, statistical conclusion or AOT-only comparison.

## Results

| Metric | Standard Pi | Pi-Bolt |
|---|---:|---:|
| Native completion | Normal | Normal |
| Wall time, instrumented | **6m41.782s** | **13m13.493s** |
| Coding generation cost | **$0.03100888560** | **$0.05733484120** |
| Model requests | 36 | 44 |
| Subtree CPU, raw | 53.329 s | 84.144 s |
| Sampled peak subtree PSS | 668.83 MiB | 860.25 MiB |
| Sampled peak private memory | 618.47 MiB | 805.05 MiB |
| Observer CPU | 5.192 s | 6.688 s |
| Observer CPU / wall | 1.292% | 0.843% |
| Prompt tokens, including cached tokens | 3,041,266 | 4,383,278 |
| Completion tokens | 51,060 | 123,895 |
| Of completion tokens: reasoning | 31,672 | 37,408 |
| Tool calls | 48 bash | 56 bash |
| Tool error events, including intermediate test failures | 6 | 4 |
| Delivered project tests, independently rerun | 38 passed | 40 passed |
| Typecheck | Passed | Passed |
| Boundary tests, included in project totals | 4 passed | 4 passed |
| **Same independent acceptance suite** | **5 passed** | **5 passed** |
| **Same actual-component browser fixture** | **Passed** | **Passed** |

Both products had the same four tools available, but these executions used bash for their tool work. Different numbers of generated tests are not a quality ranking; the common independent checks are the matched quality evidence.

The generated implementations and trajectories differed substantially: Pi-Bolt produced more than twice as many completion tokens and made more model/tool calls. End-to-end differences cannot be attributed to executable startup or AOT compilation. Provider latency/caching, stochastic generation and a shared host also limit interpretation. Earlier minimal Phase 1 results remain a separate experiment.

Machine-readable result: `results/coding-pair/COMPARISON.json`.

## Matched conditions and continuation disclosure

- Historical source-only paseo-orbi Issue #3, base `5710d9fe951e8c9278acb8de7c16cbb1636ea86b`; no solution history, review artifacts or remotes.
- Pinned standard Pi 1.5.2 / Node 24.19.0 and Pi-Bolt 1.2.1 / Pi 1.5.2 executables; hashes verified.
- Identical initial workspace/dependency/input hashes and system/task prompts. Both first provider-request bodies exactly matched the frozen expected payload before forwarding.
- Same OpenRouter model `deepseek/deepseek-v4.1-flash-1017`, high reasoning, fixed `deepinfra/fp8`, `data_collection=deny`, no fallback, 65,536 output-token cap. Retries, compaction, discovery, extensions, skills and MCP were disabled.
- Original randomized order: **standard Pi, then Pi-Bolt**. Fresh workspaces/sessions, sequential execution, at most 60 minutes each. No coding execution was repeated.
- Same network-none, non-root, read-only-root, capability-dropped containers; two-CPU quota/affinity, 3 GiB memory/no extra swap, PID limits and bounded tmpfs. Only the benchmark-owned operation-restricted Unix relay was mounted; credentials stayed host-side.
- Same original collector and 250 ms sampling. The browser evaluator helper added after the first arm was excluded from the second arm's runtime-source mount. Evaluation assets were not inserted into coding inputs. Frozen inputs and delivered source hashes were rechecked unchanged.

**The protocol was narrowed after the first arm.** Its original accounting/overhead gate failed, so the second arm initially did not start. After the user renewed continuation, `CONTINUATION.md` recorded proceeding only with the unused Pi-Bolt execution and limiting timing conclusions to instrumented/descriptive observations. This is disclosed post-first-arm analysis, not preregistration. The original failed gates and raw results remain unchanged.

## Measurement limitations, not erased failures

The original collector compared separately reported `wait4` CPU sums to `RUSAGE_CHILDREN` with a fixed 0.020 ms tolerance. Both arms exceeded it:

| Check | Pi | Pi-Bolt |
|---|---:|---:|
| CPU difference | 0.023 ms | 0.045 ms |
| Reaped records | 28 | 44 |
| Separately assessed timeval-resolution bound | 0.058 ms | 0.090 ms |
| Original fixed CPU gate | Failed | Failed |
| Original observer-overhead gate, under 1% | Failed | Passed |

Linux exposes user/system CPU in `timeval` counters, seconds plus integer microseconds. A post-trial assessment tested the differences against **2 × (N+1) microseconds** for N separately reported counter pairs plus one aggregate pair. Both fit that reporting-resolution bound. This does not prove rounding caused the discrepancies, and does not retroactively pass the original fixed gate. Five tests cover the assessment, including missing CPU, missing root/samples and unrelated collector failures. The original collector itself was not changed for the second execution.

The first observer overhead still exceeded the original threshold. No samples were discarded, no observer CPU was subtracted from agent CPU, and no clean timing claim is made. Sampled PSS/private peaks may miss short-lived peaks. One pair provides feasibility and task-quality evidence only; no confidence interval, general winner or recovery-reliability claim is supported.

## Independent evaluation

Both original outputs were copied into inference-disabled evaluation containers. The evaluator did not fix either implementation. It reran project tests/typecheck/boundaries, then used frozen-baseline fixture helpers and the common independent acceptance suite against each registered RPC and screen.

The five tests cover independent systemd/health failures, successful inactive oneshots, failed/missing units, malformed/missing health, explicit capacity versus unknown occupancy, exact allowlisted argv, rejected deployment identities, stale refresh, theme/compact rendering and filtered navigation.

Both browser runs bundled the actual delivered registered Fleet screen with existing React/React Native Web dependencies and a fixture host, populated from the independently exercised server RPC. The same final browser harness checked:
- Both deployment cards and the rejected-entry diagnostic.
- Configured capacity and unknown occupancy.
- Issues navigation filtered to Demo.
- A manual refresh actually invoking Demo's RPC, then failed refresh preserving timestamp and stale data after 60 seconds.
- Compact-dark and wide-light rendering/screenshots.
- Empty console-error and network-error lists.

This is not live Paseo-host, physical-device or production-systemd qualification.

Evaluator corrections were recorded, not hidden: a global “feature not implemented” assertion was narrowed to Fleet so it did not reject honest notices about unrelated screens; the browser selector was scoped to Demo's card rather than requiring Pi's optional “Refresh Demo” label, and was rerun identically against both outputs with an explicit RPC-call assertion. Earlier duplicate-selector, sizing and missing-font failures were preserved. A private copy of an already-installed DejaVu Sans font supplied the browser fixture; no package/font installation or host configuration change occurred.

Final matched evaluation directories:
- `results/coding-pair/standard-pi/evaluation-matched/`
- `results/coding-pair/pi-bolt/evaluation-matched/`

Each contains `RESULT.json`, `acceptance.json`, command output and browser screenshots under `browser/`.

## Spending and route diagnosis

The initial DeepSeek-hosted route was excluded by the account's no-training privacy policy (`paid-model-training-violation-by-account`). **No account privacy setting was changed.** The fixed upstream change to DeepInfra FP8 was explicitly announced before use, retaining the same OpenRouter model/high setting and adding `data_collection=deny`. Updated runtime request parity and live provider/cost verification passed.

| Budget item | USD |
|---|---:|
| Both coding executions, settled | 0.08834372680 |
| Successful live verification, settled | 0.00001136800 |
| **Known settled total** | **0.08835509480** |
| Two earlier rejected requests: retained conservative reservations, not asserted charges | 0.80000000000 |
| **Total conservative exposure** | **0.88835509480** |
| Authorization ceiling | 10.00000000000 |

There were 80 coding model requests, one successful verification and two earlier rejected verification/diagnostic requests. Every successful generation cost reconciled before stream completion. Prior exposure was carried into the second ledger; a new ledger did not reset the budget. No purchases, top-ups, model/provider fallback, automatic request retries or further coding trials occurred. The two-execution allowance is now exhausted despite unused money.

## Safety, artifacts and cleanup

Host safety remained within bounds:
- Pi: 202 samples, maximum load1 2.58, available RAM at least 39.61 GiB.
- Pi-Bolt: 397 samples, maximum load1 2.17, available RAM at least 41.23 GiB.
- Both: zero container memory-limit/OOM events.

All owned coding/evaluation containers and relay/socket resources were removed; the final owned-container query was empty. Latest disposable workspaces were removed after preserving output and evidence. No production service/configuration, actual application repository, GitHub state or public report was changed; no installation, image pull or privilege escalation occurred.

Key local evidence:
- `PAIR-PROTOCOL.md`, `CONTINUATION.md`: original conditions and disclosed continuation.
- `results/coding-pair/COMPARISON.json`: final two-arm metrics, quality and cost.
- `results/coding-pair/{standard-pi,pi-bolt}/delivery/`: original code, logs and `.bench-artifacts/measurement/` raw samples/transcripts.
- `results/coding-pair/{standard-pi,pi-bolt}/delivery-manifest.json`, `changed-files.json`: output hashes and scope.
- `results/coding-pair/{standard-pi,pi-bolt}/native-summary.json`: model/tool/token activity.
- `results/coding-pair/relay/`, `results/coding-pair/pi-bolt/relay/`: request-level cost and initial payload evidence.
- `results/coding-pair/inputs-manifest.json`, `initial-workspace-manifest.json`, `executable-pins.json`, `schedule.json`: frozen inputs, pins and order.
- `results/coding-pair/pi-bolt/runtime-source-manifest.json`: second-arm runtime-source copy, excluding the later evaluator.
- `results/coding-pair/prior-single-arm-report.md`: prior incomplete-pair report, preserved unchanged.
- `results/coding-pair/final-owned-containers-after-both.txt`: empty final owned-container inventory.

Historical reports/counters remain historical: the original driver recorded zero successfully analyzed summaries after its collector failure, even though Pi completed. `ATTEMPTS.json` corrected that one-arm interpretation at the time; **COMPARISON.json is the final record: two coding executions, no replay, both independently evaluated.** Earlier baseline, skill-order and calibration failures remain preserved.
