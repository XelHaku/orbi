# Phase 1 completed: minimal-profile Pi vs Pi-Bolt on benchmark host

**Local-only report. No publication authorized or performed.**

## Conclusion

On this fixed, offline, minimal-profile workload, the pinned Pi-Bolt executable used substantially less wall time, process-tree CPU and sampled peak memory than standard Pi. The headless scenario's median wall times were **472.43 ms vs 45.53 ms**; its median paired reduction was **90.55% (bootstrap 95% CI 89.97–91.17%)**. Median paired CPU reduction was **93.92% (93.46–94.17%)**, and sampled peak PSS reduction **54.93% (54.64–55.19%)**.

These quantify a **product/runtime difference for a short scripted workload**, not an isolated AOT effect, real Orbi delivery speedup, safe concurrency increase or reliability equivalence. No resource-discovery claim is made.

## Completion and acceptance

- Run window: **2026-11-15 04:53:10.702464–04:55:46.202978 UTC**.
- Scenarios: startup (`--version`) and headless (four read-tool calls plus answer).
- Each scenario used separate timing/CPU and sampled-memory passes to avoid including sampler overhead in the primary speed measurements.
- Each of the four cells: **5 warmup pairs + 30 measured pairs**. Every measured cell had **15 Pi-first and 15 Pi-Bolt-first** pairs; arms ran serially in one unchanged container.
- Total: **240 measured executions + 40 warmup executions**. This includes 120 unsampled timing executions and 120 separately sampled resource executions; they are not pooled.
- **0 execution failures, 0 paired request/output parity failures, 0 host-safety gate failures** during this approved minimal-only run, including warmups.
- All 140 headless sessions, including warmups across both passes, completed five local scripted requests and four expected read calls: **700 local fixture requests**, no externally hosted inference.
- Actual-executable pilot: eight successful executions before the measurement run.
- Process-tree calibration: nested and orphaned three-process fixtures passed; all descendant allocations were observed and CPU totals matched independent per-process self-CPU within 1%.
- Unit tests: **23 passed** (7 accounting, 7 parity, 4 schedule, 5 analysis). Expected TDD-red outputs remain preserved, not misclassified as benchmark failures.
- Counts, run order, complete paired data, all medians and p95 values were checked independently from raw JSONL using Python's `statistics` functions. All copied executable/dependency inputs were rehashed after the experiment and remained unchanged.

The earlier realistic-profile parity failure is **not erased**: skills appeared in opposite order in the system prompts. The user explicitly approved narrowing to minimal-only. That earlier failure and raw traces remain in the parent report/artifacts.

## Results: medians and p95

Each row uses 30 pairs. `Δ p95` is Bolt p95 minus Pi p95; negative means lower. Time/CPU rows use the **unsampled timing pass**. PSS/private rows use the **separate sampled resource pass**. Memory units are MiB, not decimal MB.

| Scenario / metric | Pi median | Bolt median | Pi p95 | Bolt p95 | Δ p95 |
|---|---:|---:|---:|---:|---:|
| Startup wall, ms | 280.10 | 11.43 | 356.84 | 17.68 | -339.16 |
| Startup process-tree CPU, ms | 292.46 | 11.07 | 385.54 | 15.70 | -369.84 |
| Startup sampled peak tree PSS, MiB | 111.26 | 39.13 | 114.56 | 42.23 | -72.33 |
| Startup sampled peak tree private, MiB | 110.67 | 38.51 | 113.97 | 41.63 | -72.33 |
| Headless wall, ms | 472.43 | 45.53 | 531.99 | 58.97 | -473.02 |
| Headless process-tree CPU, ms | 557.77 | 34.39 | 635.17 | 48.28 | -586.88 |
| Headless mean tool-cycle turnaround, ms | 16.95 | 3.48 | 22.72 | 4.89 | -17.83 |
| Headless sampled peak tree PSS, MiB | 142.89 | 64.51 | 145.79 | 64.63 | -81.16 |
| Headless sampled peak tree private, MiB | 142.29 | 63.88 | 145.19 | 64.00 | -81.19 |

**Startup means `--version`, not full application readiness.** Bolt has a version fast path. The headless measurement also starts a fresh process, so it combines initialization with the four scripted tool cycles; it is not steady-state throughput of a long-running agent.

**Tool-cycle turnaround** is the local scripted server's SSE payload-dispatch timestamp to receipt of the next complete model request. It includes payload transport/parsing, tool execution and next-request construction/transport. It is **not isolated tool `execute()` latency**. The analysis unit is each execution's mean of its four cycles, not 120 independent tool-call observations.

## Paired effects and uncertainty

`Δ` is the median of paired `(Bolt − Pi)` differences, not the difference between separately reported medians. Reduction is the median of paired `100 × (Pi − Bolt) / Pi`; positive means lower for Bolt. Intervals are paired percentile-bootstrap 95% CIs, **10,000 resamples**, seed **20261116**. Each resample preserves the two arms of every pair.

| Scenario / metric | Median paired Δ [95% CI] | Median paired reduction [95% CI] |
|---|---:|---:|
| Startup wall, ms | -268.91 [-280.87, -258.24] | 95.97% [95.43, 96.08] |
| Startup CPU, ms | -280.50 [-296.76, -274.91] | 96.28% [96.18, 96.40] |
| Startup PSS, MiB | -71.69 [-72.29, -70.87] | 64.43% [63.77, 65.18] |
| Startup private, MiB | -71.70 [-72.32, -70.85] | 64.79% [64.15, 65.55] |
| Headless wall, ms | -425.31 [-442.71, -411.76] | 90.55% [89.97, 91.17] |
| Headless CPU, ms | -526.32 [-535.84, -513.33] | 93.92% [93.46, 94.17] |
| Headless tool-cycle mean, ms | -13.26 [-14.95, -12.51] | 79.62% [76.84, 80.69] |
| Headless PSS, MiB | -78.45 [-79.45, -77.56] | 54.93% [54.64, 55.19] |
| Headless private, MiB | -78.45 [-79.51, -77.58] | 55.16% [54.89, 55.45] |

P95 uses linear interpolation and is descriptive with only 30 samples per arm. These CIs describe this local batch under paired-resampling assumptions; they do not quantify systematic sampling bias, temporal dependence/shared-host effects, other workload distributions or cross-day variability. No tail-latency, non-inferiority or reliability conclusion is justified by this sample.

## Measurement boundaries and resource accounting

Every observation gets a fresh accounting supervisor. The supervisor becomes a Linux child subreaper, launches only the target, and reaps it and any adopted descendants. `wait4` user+system CPU includes descendants reaped by their parents; adopted children are collected separately, avoiding loss and double counting. The sum is checked against `RUSAGE_CHILDREN` in the fresh supervisor. Fake server, driver and observer CPU are **excluded** from agent CPU and retained separately where applicable.

Resource-pass memory is the maximum over sampled sums of live descendant `/proc/<pid>/smaps_rollup` PSS and private-clean + private-dirty + private-hugetlb. PID start ticks are checked against reuse. No RSS field is relabelled as PSS. This is a sampled near-simultaneous tree sum, not a sum of unrelated per-process lifetime peaks.

Calibration independently allocated/touched 16+32+64 MiB across root/child/grandchild. Measured tree PSS was about 125.5 MiB and private memory 115.6–115.7 MiB including runtime overhead. Nested CPU: 560.107 ms vs 555.454 ms self-counter sum; orphan CPU: 855.175 ms vs 850.828 ms. Differences include final exit/recording overhead. Both modes saw all three processes; reaping counted one nested root versus all three orphaned processes.

**Sampler limits and overhead:**

- Requested interval: 2 ms. Maximum observed gap: **10.99 ms** in startup and **26.78 ms** in headless resource runs. Short-lived peaks can be missed; startup had as few as **4** positive samples, headless at least **15**.
- Actual benchmark sampled trees contained one process (threads are already included); descendant coverage was exercised by the separate three-process calibration, not by pretending read-only benchmark calls spawned children.
- Median observer CPU in resource runs: startup Pi/Bolt **104.95/4.04 ms**, headless **220.66/16.02 ms**. It is appreciable and affects the observed memory-pass execution environment.
- Without memory sampling, median supervisor CPU was startup **2.15/0.50 ms**, headless **3.61/0.81 ms**. Primary time/CPU results come from these unsampled observations; no observer-overhead subtraction is used.
- The raw timing-pass memory fields are zero placeholders with `sample_memory=false`, **not measured zero usage**. Only the resource pass contributes memory statistics.
- Root-exit wall time excludes supervisor startup, fake-server/home preparation and container creation. It includes process creation and root execution; observer wake/scheduling latency is a small remaining boundary effect. Full subtree-lifetime timing is also retained in raw data.

## Isolation, environment and production safety

Host: benchmark host, Ubuntu 24.04.4 LTS, AMD Ryzen 9 5900X, approximately 62 GiB RAM. Container userspace: Python 3.12.14 and glibc 2.41. The image environment is shared by both arms, not claimed identical to the host userspace.

- Existing Docker daemon/client and cached image only; **no pulls or software installations**.
- Image ID: `sha256:9e87977b867847e186d066f531ef783b006d582a985c341c269446088d90f2c4`.
- Image digest: `python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f`.
- Non-root uid/gid 1000, `--network none`, all capabilities dropped, no-new-privileges, default seccomp/AppArmor, read-only root, private PID/IPC/cgroup namespaces. Only benchmark sources/private executable copies mounted read-only and a dedicated results directory mounted writable; bounded tmpfs for temporary data.
- No host sockets, API credentials, SSH keys, GitHub tokens, production directories or device mounts. Fresh sanitized HOME/XDG/config/session/cache/fixture directories per observation.
- Both arms used one unchanged container with CPUs **0,1**, two-CPU quota, reduced CPU shares 128, **3 GiB memory/no additional swap**, 128 PID limit. Production affinity, settings, services and timers were not changed.
- Shared-host one-minute load ranged **3.67–5.76**; available host memory stayed at least **39.12 GiB**. Cores were not reserved/exclusive: these are concurrent-load observations.
- **0 throttled measured pairs** in all four cells and no memory-limit/OOM events. Pre/post checks were retained for every pair. Safety thresholds were predeclared: stop below 8 GiB available memory or at load >=16, on memory-limit/OOM events, or on parity/accounting/functional failure.
- Only loopback sockets were used by the model fixture. No external model calls, paid inference, GitHub writes, uploads or benchmark publication occurred.

## Pinned input provenance

- Standard Pi **1.5.2**, managed-install source commit `b4afdddf44e059c67ccf5097e5317d913521b470`.
- Node **24.19.0** SHA256 `bc17c508ffeed0ec622934f9b7fa72f8e78da65350e63c3eceb56fa688aa5e12`.
- Standard CLI bundle SHA256 `e79626f2dd6f94aa45d30f3fa63cd84319a6eefcd150b353cfaf274366926774`.
- Pi-Bolt **1.2.1 / Pi 1.5.2**, linux-x64, JIT off, SHA256 `30164c0edd4bcadfbe2fbb1613c201e82c640a7b01d70d001a9200b1413910b9`.
- Upstream benchmark fixtures/helpers pinned to `cb10eb35c7c58fb37e0036edfd0bd8785a305858`.
- The full private-copy manifest contains **15,548 file/symlink entries**, verified unchanged after the run. Symlinks stay within copied inputs; mutable launchers and original production executable inodes were not measurement targets.
- Bolt's release source includes substantial changes beyond AOT. Binary hashes pin this experiment but do not constitute a signed binary-to-source-build attestation. This is not a pure compilation ablation.

## Files and reproducibility

Paths below are relative to this report's directory unless prefixed `../`:

- `PROTOCOL.md`: protocol sealed before measured observations, with analysis method and stopping rules.
- `../results/minimal-v1/run/raw.jsonl`: all **280** observation rows, warmup flags included.
- `../results/minimal-v1/run/schedule.json`: full seeded schedule, written before the first observation.
- `../results/minimal-v1/run/manifest.json`: seed, schedule hash and initial conditions.
- `../results/minimal-v1/run/pair-gates.jsonl`: all parity/safety gates and pre/post resource conditions.
- `../results/minimal-v1/run/<pair>/<arm>/`: supervisor config, stdout/stderr, individual process exits/CPU, memory timeline, and (headless) requests/responses/fixture hashes.
- `../results/minimal-v1/analysis.json`: full-precision statistics and paired CIs.
- `../results/minimal-v1/accounting-pilot/`: nested/orphan ground truth and calibration traces.
- `../results/minimal-v1/pilot/`: actual-executable preflight observations.
- `../source/accounting.py`, `../source/minimal_benchmark.py`, `../source/parity.py`, `../source/analyze_minimal.py`, and `../source/test_*.py`: measurement, equivalence, scheduling and analysis code.
- `measured-run.json`, `analysis.json`, test logs, `container-launch.json` and inspect snapshots: bounded command argv, status, timestamps and outputs.
- `independent-arithmetic-check.json`, `host-final.json`, `../copied-tree-manifest.json` and `artifact-manifest.json`: verification and reproducibility metadata.

To reproduce **only with appropriate authorization**, verify pinned hashes and the cached image, create a new empty results directory, recreate the recorded container launch with a new name/results bind mount, and run the recorded isolation, accounting, minimal pilot, measurement and analysis commands in order. All sources and executable inputs stay read-only. The scripts refuse existing output directories, so do not overwrite this evidence or append a new batch into it. No dependencies need downloading. Failures stop the run; image absence must not trigger a pull.

## Scope and cleanup

The owned ephemeral container `bb-bench-p1-minimal-20261115` (`df8dcc3e7194785a60c5ee7e0592b41042c12835d5fb23d119704f5f0ee8400f`) was removed and its absence verified. Before removal only the container's idle supervisor remained; no agent descendants were left running. Raw artifacts and private executable copies remain locally. No other container or deployment was changed.

Phase 1 ends here. Real-model delivery cost per accepted/final-head-reviewed PR, longer sessions, realistic resource discovery, recovery reliability and concurrency remain unmeasured. Phase 2 and any publication require separate approval.
