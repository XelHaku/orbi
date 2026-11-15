# Phase 2B: deterministic replay and repeated autonomous coding

**Status: approval-stage protocol v1, not executed and not yet a sealed preregistration.** Task/source selection and a proposed 48-run schedule are recorded. Acceptance code, reference-input manifests and corrected instrumentation still require offline preparation and validation. No paid inference, benchmark execution, publication, installation or production change is authorized by this document.

The earlier single coding pair is a **feasibility pilot**. Preserve its costs, outputs, failed gates, cache differences and capped response unchanged. Do not pool it with Phase 2B, use it as a final effect estimate, or discard it from the eventual methodology narrative. Publication is on hold; the existing Discussion draft remains unchanged.

## 1. Questions, scope and decision rule

A. With fixed model responses and fixed tool sequences, what runtime overhead and model-visible compatibility differences exist between the pinned products?

B. On six specified historical tasks, with repeated fresh attempts, how do acceptance success, model request count, token consumption and settled inference cost differ?

The two experiments have separate datasets and conclusions. Runtime efficiency is not coding productivity. Neither is live Orbi recovery/review/merge reliability. This is a product comparison, not an AOT-only ablation.

Predeclared primary outcomes for B, all reported together:
1. Independent acceptance success within fixed limits.
2. Number of forwarded model requests; also attempted/reserved/settled counts separately.
3. Input tokens split into cached/uncached, total completion tokens, and included reasoning tokens.
4. Settled inference cost, with unresolved reservations disclosed separately.

Secondary outcomes: root elapsed time, subtree lifetime, subtree CPU, sampled tree PSS/private memory, container charged-memory high-water mark, tool calls/error categories, cap hits, and independent evaluation time. Cost or request counts alone do not establish superiority when success differs. There is no single composite winner score or automatic production-default change.

## 2. Selected task population and provenance

Choose six new-to-this-benchmark tasks spanning user-facing changes and offline integration work. The selection is purposive by scope, not a random sample of all software tasks. Strata are organizational labels, not empirically measured difficulty. Keep these tasks fixed; no substitutions after any coding output is observed.

| Task | Stratum | Outcome | Original start SHA |
|---|---|---|---|
| paseo-orbi #14 | Small | Accessible observation/error states and correctly disabled refresh | `73e0cad862d07a2a326d3ed81fe325881be3ee3b` |
| paseo-orbi #15 | Small | Validated explicit issue/PR evidence links | `73e0cad862d07a2a326d3ed81fe325881be3ee3b` |
| paseo-orbi #6 | Medium | Read-only blocker guidance and attributed artifact metadata | `73e0cad862d07a2a326d3ed81fe325881be3ee3b` |
| paseo-orbi #7 | Medium | Four-view offline integration and package/install-artifact qualification | `ed98a0db53773ac5eb590ed2a4fd7a6d3f5ebc04` |
| paseo-orbi #4 | Large | Issue lifecycle/pagination and trusted report metadata | `5710d9fe951e8c9278acb8de7c16cbb1636ea86b` |
| paseo-orbi #5 | Large | Attributed run/session/activity/PR evidence with privacy bounds | `73e0cad862d07a2a326d3ed81fe325881be3ee3b` |

The original starting SHAs were recovered from retained Runner `issue=... base_sha=...` and `git worktree add` records, not assumed from the eventual merge parent. Source-only Git archives are already saved and hashed in `task-selection.json`. All six package-lock files match the pilot's lock byte-for-byte: SHA256 `d2028eaf6c6874a8ad4de70b28579fa5b42a75872858b23d2919f49370dd6468`.

Issue bodies were fetched for this design and frozen as `issue-N.json`. **They are current issue snapshots, not claimed to be the exact historical implementation prompts.** Requirements may include later clarifications. Before sealing, derive task prompts from these bodies plus the necessary governing epic/reference contracts. Remove operational delivery instructions only through an explicit common benchmark adaptation recorded in a prompt-diff manifest, never silently alter the functional acceptance.

Excluded candidates and reasons:
- #3 Fleet: already used for pilot/method development; retain separately, not as a seventh task.
- #2 foundation: greenfield dependency/bootstrap requirements differ substantially from the common existing-project environment.
- #11 installed-Paseo test harness: requires additional toolchain/runtime acquisition and a different qualification contract.
- #12/#13: installed/native qualification depends on separate human/device/consent gates.
- #1: coordination epic, not one executable outcome.

Task #7 has a specific readiness requirement: its isolated production-only `npm ci --omit=dev --ignore-scripts` must work from an approved private offline cache in an owned temporary candidate directory. This is **not host installation**, and its limited sandbox execution must be expressly included in the preparation/execution approval. No acquisition or installation was performed during planning. If that cannot be supported, stop and amend task selection before any paid run; do not waive this acceptance item.

## 3. Frozen inputs and independent acceptance

For each task, seal before coding:
- Source tar SHA256 and per-file manifest; original source SHA kept as provenance.
- Issue/epic/reference snapshots and hashes; exact final system/task prompts.
- Dependencies, SDK/reference files, tool schemas/configuration and executable hashes.
- Baseline command outputs and baseline-negative acceptance controls.
- Independent acceptance source, fixture data, browser assets, evaluation commands and expected outcomes.

The six independent evaluators are **not yet implemented/sealed**. Required acceptance coverage is fixed here:

| Task | Required independent acceptance coverage |
|---|---|
| #14 | Registered/shared observation flow: loading/success/stale-with-error semantics; stable safe alert region; timestamp changes do not remount the alert; refresh disabled/busy reflects connection/foreground/fetching; unavailable activation causes no RPC; existing cancellation/stale/host-isolation behavior survives. Browser checks cover actual DOM accessibility semantics, not native screen-reader speech. |
| #15 | Real Issues interaction: inspect/paginate remains separate from opening; exact selected-repository issue/PR destinations; reject foreign, encoded, credential/query/fragment and conflicting identities; safe opener-error text; current mounted selection controls cannot expose old-repository links; no extra RPC or mutation. Intercept the host opener; do not navigate to real GitHub. |
| #6 | Registered list/detail RPC and screen: supported/unknown failure enums, manual/fix/merge waits and base-CI states; safe source-owned guidance; exact artifact attribution and metadata-only access; missing/cleaned/escaping evidence; complete-empty versus partial/unavailable/stale; no recovery action, raw diagnostics or canary escape. |
| #7 | Actual four-view registrations/adapters with two deployments; complete/partial/stale, malformed source, host switch and teardown; zero prohibited writes/canary leaks; package/lock/runtime-file inspection and isolated offline production preparation; scoped README/OVERVIEW/install/privacy readback. It must add usable qualification evidence, not merely rerun existing unit tests. |
| #4 | Registered Issues flow: lifecycle precedence, PR-object exclusion, complete/capped pagination, dependency uncertainty; trusted publisher/prefix/version selection; newest-run-without-summary behavior; invalid/duplicate/conflicting receipts; exact-repo PR identity; auth/rate backoff and incomplete-membership preservation. |
| #5 | Registered Runs flow: exact issue/run membership including 42 versus 420; retained history not active membership; bounded headers/tails/truncation/rotation; session and journal projection without prompts/arguments; exact event attribution; missing/red/pending/stale-head checks; selection/host changes and teardown. |

All tasks also require the applicable project tests, typecheck and boundary checks. Expected baseline failures must correspond to missing task behavior or missing required qualification artifacts, not broken imports or evaluator setup. Existing baseline tests must pass, except an explicit original-issue regression documented and approved before sealing.

Use actual public registrations and behavior rather than newly invented export names. Supply synthetic data below the adapter under test, not canned success in place of the adapter. UI evaluations use actual delivered components in a disclosed fixture host with browser interaction, screenshots and console/network-error checks. No live Paseo, production systemd, external account or native-device claim follows from them.

Allow code to be evaluated without post-run implementation repairs. No LLM reviewer or replacement trial. For #7's documentation criterion, use a frozen human checklist and arm-neutral output labels; record that reviewer blinding may be imperfect from code/style. No success grade based solely on the agent's self-report.

If an evaluator bug is discovered after runs begin: preserve the original, stop the batch, correct only after approval, re-evaluate every relevant preserved output identically, and label the affected endpoint amended. Do not describe a changed evaluator as originally preregistered.

## 4. Experiment A — deterministic replay

No external model endpoint or live credential is available to A. A fixed local SSE fixture supplies all model responses; tool fixtures and expected filesystem effects are frozen. Replay deterministic fixtures, not the model's full historical solution to a selected B task. A and B results are never pooled.

### A1: compatibility matrix — 24 offline launches

Twelve frozen scenario families, each executed once on each product:
1. Text reads: UTF-8, CRLF, offsets/limits and missing files.
2. Writes: create/overwrite with exact resulting bytes.
3. Edits: unique, ambiguous and absent matches; exact resulting bytes/error content.
4. Bash: stdout/stderr, successful/nonzero exits and deterministic environment.
5. Large tool output: truncation/line limits and multibyte boundaries.
6. Timeout and child cleanup, including a detached child owned by the fixture.
7. Multiple tool calls with deliberately inverted completion order.
8. Fragmented SSE/tool arguments, including UTF-8 boundaries.
9. The sanitized capped-response shape: normalized `tool_calls`, native `length`, empty bash arguments, then scripted recovery.
10. Mid-stream interruption: no hidden HTTP retry or alternate endpoint.
11. Skill discovery with eight skills in one fixed creation order.
12. Skill discovery in a second fixed creation order plus duplicate-name precedence.

Compare complete model-visible request bodies, tool definitions/order, tool-result text/order, errors, stop metadata, output bytes and filesystem effects. Do not sort skills, reorder messages, rewrite error text or discard a mismatch. Use identical in-container paths where possible. Any unavoidable transport-address normalization must be an exact, predeclared substitution that does not alter model-visible content; retain raw bytes alongside it.

**Known evidence:** the prior minimal five-request replay matched. In the prior realistic replay, the only JSON differences were the system-prompt fields containing `skill0…skill7` versus `skill7…skill0`; all four read-tool result messages matched. Pinned source loaders consume unsorted `readdirSync` results and preserve insertion order. This is an ordering-sensitive mechanism, not proof of the binary/runtime root cause. Native directory enumeration must be checked in A. Broader bash/edit/write/error parity is not yet established. Even a passing expanded fixture matrix establishes only its tested cases, not exhaustive behavioral equivalence.

The original capped empty call was already in the upstream response; it does not itself prove a tool-response formatting difference between products. A9 tests both products against the same response.

B retains the pilot's explicit minimal policy with skills/discovery disabled. A skill-profile failure remains published as a product difference and blocks any default/skills-enabled equivalence claim; it is not silently normalized away. A functional or model-visible mismatch under B's active four-tool policy blocks B until its interpretation and any protocol change are explicitly approved. Do not patch a runtime or sanitize its outputs solely to obtain a parity pass.

### A2: runtime measurement — 420 additional offline launches

Three fixed workloads: fresh startup, a successful multi-tool replay, and a large/fragmented-stream replay. Each has separate unsampled timing/CPU and sampled-memory passes. For each workload/pass: five warmup pairs and 30 measured pairs, balanced 15 AB/15 BA measured pairs.

That is 360 measured plus 60 warmup launches; with A1, **444 offline native launches**, separate from B's 48 coding runs. Exact fixture bytes and the A schedule must be sealed before A executes. Workloads failing active-policy parity are not admitted to the runtime effect table; retain their compatibility failures rather than substitute a convenient workload.

A2's memory-only pass requests a fixed 2 ms sampling interval, separately from the unsampled timing/CPU pass. Require at least one positive live sample for startup and five for the multi-tool/stream workloads, no sampling error and maximum inter-sample gap 50 ms. Disclose the actual cadence and observer CPU; these short-run sampled peaks can miss peaks and have appreciable observer cost. Do not apply B's long-run observer-overhead threshold to this separate memory pass or use its wall/CPU observations for A's primary speed effects.

Report paired distributions and 20,000-resample paired-bootstrap intervals within each fixed workload/pass. The analysis unit is a run pair, not each token/tool event. These results describe the fixture and machine, not coding performance.

## 5. Experiment B — 48 coding runs

Six tasks × four repetitions × two products = **48 attempts / 24 adjacent matched pairs**. Every task gets four Pi and four Bolt attempts. Each pair uses the same frozen task inputs but independent fresh sessions and model draws.

For each task, exactly two pairs are Pi-first and two Bolt-first. Pair order and assignment of AB/BA to repetition labels are shuffled before execution. Both arms of a pair run consecutively; pairs run sequentially, never concurrently.

The proposed schedule is saved in `schedule.json`, seed **2026111502**, SHA256:

`58be3b69e53085035703f67446cb1b328d06003a8e0d576af13499822f58442b`

All 48 workspace keys are unique, and count/balance assertions passed. The schedule has not executed. It becomes frozen only with the final approved protocol/manifests; no rescheduling based on observed success or expense.

Independence means no shared agent session, writable workspace, prior attempt output, evaluator result or solution history. It does **not** guarantee independent provider caches or independent task difficulty. Several tasks share prerequisite code; six related tasks in one repository are not a representative software-task sample.

Source snapshots contain legitimate prerequisites but no solution to their own task, later commits, historical `.git`, review records or other trial output. No network/remotes permit solution retrieval. If local Git is needed for artifact inspection, use only an owned repository synthesized from the frozen source/candidate, with fixed local metadata and no remote or historical objects. It is not the real application checkout. Do not claim a synthetic candidate SHA exists on public GitHub. This local-artifact adaptation must be explicit in the frozen prompts and approval.

## 6. Provider, tool and cache controls

Keep the pilot's pinned executables, Node 24.19.0 and copied dependency environment, verified by hash. Node 24 is a benchmark environment choice, not a claim to reproduce the original issues' Node 22.19.0 CI. All baselines/evaluators must pass on it before execution; do not silently substitute Node versions.

Keep:
- OpenRouter `deepseek/deepseek-v4.1-flash-1017`, `high` reasoning.
- Fixed `deepinfra/fp8`, `allow_fallbacks=false`, `require_parameters=true`, `data_collection=deny`.
- 65,536 max output tokens; the same explicit compatibility/request configuration as the pilot.
- `read,bash,edit,write` only; no skills, extensions, MCP, prompt templates, discovered context, compaction or automatic HTTP retries.
- Same system prompt/tool schemas per task; exact initial request verification before upstream forwarding.

Do not introduce a seed/temperature setting unsupported by the provider or different from the frozen configuration. Record omissions/defaults. Provider/model IDs do not attest immutable model weights; record returned identity/fingerprint when available and disclose its absence.

No paid warmups. No assumption of equal cold caches. Record cached/uncached tokens on every request and keep order/repetition labels. Counterbalancing mitigates order effects but does not eliminate hidden cache state. Actual paid cost includes cache effects; do not replace it with a hypothetical uncached bill as the primary result.

## 7. Corrected measurement validation — mandatory before paid inference

The old observations remain failed under their original gates. A new protocol cannot retroactively repair them. The following procedure is **specified, not yet implemented/calibrated**.

### CPU accounting

Use one fresh Linux child-subreaper supervisor per observation, with no unrelated child processes. Record each `wait4` user/system counter as integer microseconds, plus `RUSAGE_CHILDREN`; do not accumulate floating-point milliseconds. Check:

`abs(sum_wait4_us - aggregate_children_us) <= 2 * (N + 1)`

where N is the number of distinct reaped records. Reject missing/duplicate records, missing root exit, impossible values and unrelated collector errors. This is a fixed reporting-resolution bound, not a blanket error allowance or proof of rounding causality.

The preserved pilot differences remain **23 µs / 28 records** and **45 µs / 44 records**, versus proposed bounds 58/90 µs. Re-expressing them as integers does not eliminate them. Five existing assessment tests and four trajectory-accounting tests pass; these do not validate the new collector.

### Wall and memory

Record monotonic root-start/root-exit timestamps and complete subtree lifetime separately. Exclude setup and independent evaluation from coding duration; record those separately. Root exit is not accepted as clean teardown while owned descendants remain.

Because B has only one execution per scheduled attempt and must record memory, use a **fixed 1,000 ms** process-tree PSS/private sampler for every B attempt. This changes the old 250 ms sampling and must be fixed before execution. Wall time remains instrumented, never described as uninstrumented/zero-overhead timing. No post-hoc subtraction.

Report:
- Maximum sampled simultaneous live-subtree PSS and private memory, with PID/start-time identity checks.
- Sampling cadence, gaps, exit races and positive sample count.
- Fresh container `memory.peak` separately: charged cgroup memory, including other container processes/page cache, **not PSS or agent-only peak memory**.
- Observer CPU separately from agent subtree CPU.

A one-second sampler can miss short-lived peaks; do not claim exact PSS high-water marks. Require live positive samples, at least 80% of the nominal root-lifetime sample count (minimum one), maximum inter-sample gap 1.25 seconds, and no unhandled sampling errors. Missing kernel high-water data is a preflight failure, not a zero.

### Offline calibration matrix and thresholds

Before any A/B benchmark execution, validate the collector in the same cached container/resource configuration on bounded non-model fixtures:
- Nested and orphan/adopted process trees; fan-out 1, 16, 64 and 128.
- CPU-active and sleeping processes; enough deliberate CPU work for independent self-CPU comparison.
- Touched allocations with total live memory safely below 3 GiB, held at least five seconds; include Node/compiler-like VMA layouts and process churn.
- Allocation release before the independent exit-CPU reference, preserving teardown counters.
- PID reuse/exit races, zero/empty measurements, nonzero root exits, a timeout, detached-child cleanup and intentional missing/duplicate records.

Fixed gates:
1. Counter-resolution inequality above passes; injected out-of-bound errors fail.
2. Kernel subtree CPU agrees within **5%** of independently summed self-CPU references on fixtures with at least two CPU-seconds of work. Record final reference/exit overhead; do not compensate after observing results.
3. All fixture processes are accounted for; all long-held allocations are observed, and measured live-tree private memory is at least the touched allocation bytes with runtime overhead reported separately.
4. For B's one-second sampling configuration, collector CPU is below **0.5%** of wall time in every representative long-run calibration case (at least 60 seconds); live coding threshold remains **under 1%**. Short-run A overhead is measured and disclosed separately, not falsely certified by these long-run ratios.
5. Sampling coverage/gap rules pass; root exit and owned-subtree cleanup are proven, with a five-second cleanup allowance before owned-container termination and recorded failure.
6. Independent monotonic wrapper/timestamp checks use the same declared boundaries and reject missing/reversed timestamps. Deterministic A separately compares sampled and unsampled passes; observer CPU fraction is not treated as proof of zero wall perturbation.

Each fixture command is bounded by timeout and preserves its real exit status. Calibration failure blocks the experiment. Do not loosen the thresholds after paid data. If one-second sampling cannot meet them, revise the protocol and obtain approval **before** coding; do not silently drop memory or change cadence mid-batch.

## 8. Capped responses, failures and stop policy

Predeclare now:
- Any completion-limit response stays in its attempt and all cost/token totals, including the pilot's empty-tool shape.
- Capture both normalized and native finish reasons; validate tool arguments using the unchanged runtime's behavior.
- Normal agent-driven recovery after a tool error may continue within the same attempt's limits. No manual prompt repair, hidden retry, output-cap increase or replacement attempt.
- A cap hit is not automatically an acceptance failure if the agent recovers and passes; report cap incidence and outcomes separately.
- If the agent stops unsuccessfully, acceptance fails. An incomplete/missing provider cost remains an unresolved reservation and triggers the financial stop rule, not an inferred zero charge.

Distinguish outcomes:
- Ordinary implementation/test/tool failure, or per-attempt time/request/spend cap: record the attempt, evaluate available output, count it in the denominators, and continue the fixed schedule when safe.
- Instrumentation, isolation, parity, global budget, unknown billing or host-safety failure: stop the remaining batch, preserve the consumed attempt and report the dataset incomplete. Do not replace it or continue under revised rules.

An attempt is consumed when a native agent is launched with its coding prompt, even if it later fails before producing output. Maintain separate launched/completed/evaluated/accepted counts; do not confuse a failed summary generator with zero executions.

Do not stop because one product looks better, continue until it wins, or add repetitions after looking at uncertainty intervals. Safety/budget stops are the only permitted early stops and must be reported with unexecuted slots marked `not_run`, not failures invented for an unrun arm.

## 9. Resource and spending limits — proposed, not authorized

Per coding attempt:
- 60 minutes native execution.
- 80 forwarded model requests.
- USD 2 maximum conservative exposure, including unresolved held reservations.
- Two-CPU quota/affinity, reduced CPU shares, 3 GiB memory/no additional swap, PID limit 256, bounded temporary storage.

Stop at the first applicable limit. A per-attempt cap is an ordinary bounded-attempt outcome, not permission to replay. Independent evaluation has a separate proposed 15-minute limit per output; harness/evaluator infrastructure errors stop the batch rather than masquerade as a product failure.

**Proposed new-batch exposure ceiling: USD 20**, inclusive of all coding requests and at most one paid noncoding route-verification request. It requires explicit new authorization. The old $10 pilot authorization is not transferable permission for these runs.

Planning scenarios only:
- 24 × the pilot pair's combined bill: **$2.12024944320**.
- Five times that extrapolation: **$10.60124721600**.
- These are rough budget arithmetic, **not effect estimates, forecasts or confidence bounds**. New tasks may be much more expensive. The hard ceiling may stop the batch before 48 runs.

The relay admits only the fixed OpenRouter chat-completions operation, one in-flight request, local function tools and the frozen price/token bounds. Reserve **$0.40** before each request and retain it if cost cannot be reconciled. At the pilot's conservative caps, 1,048,576 prompt tokens × $0.30/million plus 65,536 output tokens × $1.20/million is **$0.393216**. Validate these bounds and request admissibility before forwarding; no fallback or reserve reset. When the next reservation cannot fit an attempt or batch cap, stop that scope before sending.

This is a local fail-closed exposure bound under the validated provider price/token contract, not a provider-account spending limit or control over unrelated shared-account use. Do not buy credits, change privacy settings, provision keys or alter account limits without separate authorization. If the reservation bound cannot be justified, no inference starts.

Prior pilot exposure **$0.88835509480**, including its unresolved $0.80, stays in its own ledger. If the new $20 ceiling is approved, combined conservative exposure across both studies is at most **$20.88835509480** under those bounds. Do not silently settle the old reservations or charge them twice.

Maximum scheduled native coding time is 48 hours, plus offline preparation/replay and evaluation. This is a ceiling, not a turnaround promise. No unattended schedule or recurring job is authorized now.

## 10. Statistical analysis and precision limits

Store one row per attempt and one matched-pair record. Requests/tool calls are observations within an attempt, not independent trials. Display all four paired repetitions per task, acceptance outcomes, medians, IQRs, ranges, ECDFs and the full paired differences; averages alone are insufficient. Tail quantiles with 24 runs per product are descriptive.

For requests, token components and cost, define each task's effect as the mean of its four `(Bolt - Pi)` paired differences. The primary aggregate is the equally weighted mean over the six tasks. For success, use the same paired difference on binary acceptance outcomes. Positive resource/count/cost differences favor Pi numerically; success differences have the opposite desirability. Report the direction explicitly.

Primary 95% uncertainty intervals: **20,000 paired bootstrap resamples**, seed **2026111503**. Keep all six tasks fixed. Within each task, resample its two AB pairs and its two BA pairs separately, preserving order balance and keeping both arms/outcomes together. Recompute the equal-task aggregate. Use the 2.5th/97.5th percentiles. This estimates repetition variability conditional on these six tasks under exchangeability assumptions, not broad task-population uncertainty.

Predeclared sensitivity: hierarchical paired bootstrap resampling the six task clusters, then pairs within their AB/BA strata. Label this task-mix sensitivity, not proof the purposive six-task sample represents other repositories. Shared prerequisites/provider cache may violate independence assumptions; disclose that limitation rather than treating 48 executions as 48 unrelated tasks.

For success additionally show per-task counts and paired discordances (Pi-only success, Bolt-only success, both, neither). With only six tasks and four repetitions, success-rate differences will be imprecise. Even 24/24 successes would, under an optimistic independent-binomial assumption, leave a roughly **11.7% one-sided 95% upper bound on failure probability**; clustering/heterogeneity weaken such generalization further. If all paired success differences are identical, label the success bootstrap interval **uninformative/degenerate**, not a zero-width confidence claim or evidence of equivalence; retain the raw resampling result for audit. No reliable minimal detectable effect or power claim can be derived from the one-pair pilot.

No p-values, superiority/non-inferiority/equivalence labels or general winner declaration are prespecified for this small study. The four outcome families' intervals are marginal, not simultaneous familywise guarantees. Do not pick the one favorable metric as the conclusion.

Include unsuccessful attempts in request/token/cost distributions. Low consumption from immediate failure is not efficiency. Report total all-attempt settled spend and accepted-task count for each product; spend per accepted output includes failed-attempt spend and is undefined if there are no accepted outputs. Keep unresolved reservations beside settled costs, never silently substitute one for the other.

Wall time is elapsed-to-termination for all attempts; successful-pair duration is a separately labeled conditional analysis. Timeouts/failures remain visible. Do not impute a fast failure as fast task completion. CPU/memory invalidated by instrumentation are missing/invalid with reasons, not zero and not selectively omitted to improve an average.

If the batch stops early, retain every row and unmatched completed arm. Do not apply the complete-design interval machinery to a selectively completed subset as if the 24-pair design finished; present the incomplete dataset descriptively. Any revised inference plan requires a new declared analysis, not an unmarked substitute.

## 11. Isolation, archives and authorization

Use cached images, private pinned dependencies and benchmark-owned files only. Non-root/network-none/read-only-root containers, dropped capabilities, no-new-privileges; no real repository `.git`, credentials, host/Docker sockets, production directories, devices or generic proxy. The restricted inference relay is the sole permitted external operation for B after approval. A has no live credential/relay route.

Host safety: stop below 8 GiB available RAM, at load1 >=16, or on container memory-limit/OOM events. Never stop production jobs or change production affinity, timers, concurrency, review gates, service/configuration or account settings to make a run pass. Clean only owned processes/containers/workspaces, preserving evidence.

Archive all launch records, initial and final manifests, native/tool events, raw provider streams and usage, observer data, evaluator output, screenshots, amendments, errors and cleanup. Preserve raw evidence privately; do not publish chain-of-thought/session material, credentials or private paths by default. A public reproducibility package needs explicit redaction/licensing/release approval.

## 12. Readiness and approval sequence

Completed during planning:
- Six current issue snapshots and journal-proven source archives hashed.
- Common lockfile identity checked against the pilot.
- Proposed 48-run balanced schedule generated and count/balance assertions passed.
- Existing skill/tool parity and CPU discrepancies rechecked offline; nine existing analysis tests passed.
- Budget scenarios and this analysis/stop policy specified.

Still blocking execution:
1. Freeze governing references and exact task prompts, including scoped #7/local-artifact adaptations.
2. Implement and validate all six independent acceptance suites, baseline/negative controls and scoped document checklist.
3. Implement the corrected collector; pass the entire offline calibration matrix and preserve raw calibration evidence.
4. Freeze and execute A only after authorization; investigate/report every mismatch and satisfy B's active-policy gates.
5. Reverify executable/input pins, isolation/cleanup, provider availability/identity/price bounds and budget guards.
6. Freeze final protocol, all fixture/evaluator hashes and schedules. Any amendment before sealing gets its own version/diff.
7. Obtain explicit approval of offline preparation/execution scope and then **paid B execution**, its $20 ceiling/$2 attempt caps, 48-run limit and resource limits. A conditional approval may name the exact gates; no failure waives itself.

**Current permission remains design-only.** The existing publication draft and pilot evidence are unchanged. No automatic publication follows completion. The eventual report must show the pilot as methodology/limitations alongside, but not pooled into, the preregistered Phase 2B results.
