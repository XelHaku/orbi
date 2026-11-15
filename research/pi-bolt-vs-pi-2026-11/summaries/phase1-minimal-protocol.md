# Minimal-only Phase 1 — sealed protocol before measured observations

Authorization: user's minimal-profile-only amendment, retaining BB-BENCH-P1 and BB-BENCH-P1-SANDBOX restrictions. Prior realistic-profile parity failure remains preserved; no resource-discovery claims.

## Gates already passed

- Cached-image, non-root, capability-free, read-only-root, network-none container; local loopback exchange verified; no external interface/routes or host secrets/socket mounts.
- Identical pinned input hashes and private executable copies.
- Strict minimal request/output parity, including tool schemas/results and all five local model requests; checked again using the actual measurement supervisor.
- Accounting unit tests: seven; schedule tests: four; parity tests: seven.
- Nested and orphaned three-process CPU/memory calibration: observed all processes, sum of wait4 accounting matches independently reported self-CPU totals within 1%; 112 MiB of separately allocated/touched memory appears in summed tree PSS/private measurements. Adopted descendants are retained with PR_SET_CHILD_SUBREAPER and wait4.
- Actual-executable pilot: startup/headless × timing/resources × two arms, eight processes. All gates passed. Sampling CPU overhead is appreciable; therefore separate passes are required rather than interpreting instrumented wall time as ordinary execution speed.

## Design

Only `startup` (`--version`, not full application readiness) and `headless` (four scripted read calls plus answer, fresh print-mode process). Explicit common tools read/bash/edit/write; skills, templates, context discovery, extensions, MCP and themes disabled. Same explicit system prompt, thinking off, isolated per-run HOME/XDG/agent/session/cache/fixtures.

Two measurement passes per scenario:

- **timing**: wall clock from before spawn to root exit, exact whole-subtree CPU from reaping, no /proc memory sampler. Tool-cycle intervals are recorded by the scripted server.
- **resources**: same work with 2 ms target-cadence /proc sampling. Report sampled maximum of simultaneous summed descendant PSS and private-clean+private-dirty+private-hugetlb. Preserve actual gaps. These are sampled peaks, not exact kernel-maintained high-water marks. Resource-pass wall/CPU and observer CPU remain in raw data, not primary performance claims.

Each of these four cells has 5 warmup pairs and 30 measured pairs. Exactly fifteen AB and fifteen BA orders per measured cell; fixed random seed 20261115 also randomizes cell order. Arms execute serially within one unchanged container; no image/container startup enters observations. Total planned: 40 warmup agent processes and 240 measured agent processes (120 timing, 120 resource-sampled). This is 30 measured pairs per scenario **per pass**, not 120 independent task pairs. The final report distinguishes passes and does not pool them.

Every headless pair must preserve strict normalized request/output parity; only declared ephemeral paths and input server ports are normalized. No skill-list sorting, dropped failure, rerun, or changed control. Each pair's pre/post load, available memory, cgroup CPU and memory events are recorded. Stop if host available memory <8 GiB, one-minute load >=16, OOM/memory-max event, incomplete accounting or parity/functional failure. No production changes. CPU set 0,1, quota two CPUs, low weight; shared host, not reserved exclusive cores. Timing results are concurrent-load container observations, not an idle-host claim.

## Analysis specified in advance

Use only measured rows, retain and enumerate warmups/pilot/failures separately. Require 30 observations per arm per cell and 15/15 order balance. Pair by scenario/pass/pair ID. Never silently summarize a successful subset if the experiment stops.

For each metric: median per arm, p95 per arm with linear quantile interpolation, median paired difference (Bolt minus Pi), and median paired percent reduction `100*(Pi-Bolt)/Pi`. Paired bootstrap, 10,000 resamples, seed 20261116; percentile 95% intervals for paired median differences and paired median percent reductions. Report p95 as descriptive (n=30 is insufficient for strong tail claims). Primary time/CPU come from the unsampled pass; PSS/private memory from sampled pass. Per-run tool-cycle mean across the four calls is the analysis unit, not four independent samples.

Tool-cycle definition: local scripted-server SSE payload-dispatch timestamp -> next complete request received by that server. Includes payload transport/parsing, tool work and next-request construction/transport; is **not pure tool execute latency** and contains no paid/real-model inference. Synthetic usage fields are not real token accounting.

No claim of source-identical AOT effect, long-task delivery speedup, safe concurrency increase, reliability equivalence, full recovery behavior or realistic resource-discovery overhead. Standard Pi 1.5.2 on Node24.19.0 vs Pi-Bolt1.2.1/Pi1.5.2 is a product/runtime comparison.

Raw data: `../results/minimal-v1/run/`; frozen order and launch metadata are written there before the first observation. The entire workload runs with no network interfaces other than loopback. No publication authorized.
