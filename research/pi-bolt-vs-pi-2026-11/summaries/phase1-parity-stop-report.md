# BB-BENCH-P1-SANDBOX — pilot stopped on request-parity failure

**Historical pilot report.** After explicit approval to exclude resource discovery and run the minimal profile only, Phase 1 completed. See [minimal-v1/REPORT.md](minimal-v1/REPORT.md). The realistic-profile failure below remains preserved and was not waived or normalized away.

Date: 2026-11-15 UTC. Host: benchmark host. This is an environment/parity pilot report, **not a performance benchmark result**.

## Outcome

The authorized container approach resolved the network-isolation blocker. The minimal-profile parity pilot passed. The synthetic-realistic profile did not: standard Pi and Pi-Bolt serialized the eight discovered skills into their system prompts in opposite orders. Execution stopped immediately, before any warmups, measured pairs, or process-tree accounting pilot. No acceptance criterion was weakened and the failing profile was not silently removed.

| Gate | Result |
|---|---|
| Existing runtime/image; no installation/pull | PASS |
| Network-none, loopback-only, non-root sandbox | PASS |
| Pinned executable hashes and runnable builds | PASS |
| Parity comparator tests | 7 passed after expected TDD red |
| Minimal-profile request and output parity | PASS, one pair |
| Synthetic-realistic request parity | **FAIL**, one pair |
| Synthetic-realistic scripted output/tool equivalence | PASS for observed pair |
| Process-tree CPU/PSS/private-memory accounting | NOT VALIDATED — stopped before this stage |
| Five warmups and 30 measured pairs per cell | NOT STARTED |

## Runtime and isolation evidence

- Docker client: 29.3.0; daemon: 29.1.3; existing local Unix-socket access. No sudo or new permission grants used.
- Podman 4.9.3 is installed; only its version was inspected, since Docker was usable. No Podman fallback attempted.
- Cached image: `python:3.12-slim`, immutable ID `sha256:9e87977b867847e186d066f531ef783b006d582a985c341c269446088d90f2c4`.
- Image digest: `python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f`.
- In-container Python 3.12.14, glibc 2.41. These are part of the experiment environment, not claimed identical to the host userspace.
- `--pull never --network none --user 1000:1000 --cap-drop ALL --security-opt no-new-privileges=true --read-only`.
- Private PID/IPC/cgroup namespaces; no devices, published ports, host namespaces, production directories, credential directories or host sockets mounted.
- Three explicit bind mounts: benchmark sources and private executable copies read-only; dedicated benchmark results writable. A separate bounded `/tmp` tmpfs is writable, noexec/nosuid/nodev.
- Clean per-execution environment; only explicit HOME/PATH/locale/offline settings and per-arm XDG/session/cache directories were supplied. No provider credentials or proxies inherited. The scripted provider's dummy `fake` key is not a real credential.
- Container caps: CPUs 0,1; two-CPU quota; reduced CPU shares 128; 3 GiB memory with no additional swap; 128 PIDs. These constrain the benchmark, not production processes.
- Verified separate network namespace, sole interface `lo`, no IPv4 route, and IPv6 entries only for loopback. A local TCP client/server exchange passed. No external destination was probed or contacted.
- Self-process smaps_rollup and cgroup CPU/memory counters were readable. This is **capability evidence only**, not validation of full process-tree accounting.

Both arms ran serially inside the **same** container. Container startup was not a measurement. The stopped pilot produced no speed, CPU-efficiency or memory-efficiency comparison.

Full launch argv and inspect output: `container-launch.json`, `container-inspect.json`, `container-inspect-final.json`. Probe evidence: `results/isolation-probe.json`, `isolation-probe-command.json`.

## Executable and workload provenance

Original pinned hashes were rechecked, then private non-hardlinked copies were made under `builds/`. All 15,548 copied file/symlink entries were recorded in `copied-tree-manifest.json`; all symlinks resolved within the private copy.

- Node 24.19.0 SHA256: `bc17c508ffeed0ec622934f9b7fa72f8e78da65350e63c3eceb56fa688aa5e12`.
- Standard Pi 1.5.2 CLI SHA256: `e79626f2dd6f94aa45d30f3fa63cd84319a6eefcd150b353cfaf274366926774`.
- Pi-Bolt 1.2.1 / Pi 1.5.2, JIT off SHA256: `30164c0edd4bcadfbe2fbb1613c201e82c640a7b01d70d001a9200b1413910b9`.
- Harness files/fixtures were archived from `cb10eb35c7c58fb37e0036edfd0bd8785a305858`, without modifying its source checkout.
- `source/parity.py` uses that pinned scripted model and fixture-home generator, recording each actual HTTP request and response body.
- Each arm had fresh agent/project/outer-HOME directories, XDG state, session/cache directories, and its own loopback server. Initial fixture/config content hashes matched after replacing only the ephemeral server port for the input-hash comparison.
- Explicit common tools: `read,bash,edit,write`. Extensions/MCP/themes disabled, thinking off, identical explicit system-prompt text. The blank profile additionally disables skills/templates/context discovery; the synthetic-realistic profile enables discovery only from generated isolated inputs.
- For comparison, only known per-arm path prefixes were replaced by `<WORK>`, `<AGENT_HOME>` and `<HOME>`. Object-key serialization order is ignored; prompt text, array order, tool schemas, model options and contents are not.

Raw/normalized requests, HTTP responses, stdout/stderr, argv/environment, content hashes and summaries live under `results/parity-pilot/{blank,realistic}/{standard-pi,pi-bolt}/`. `pilot-artifact-hashes.json` hashes the sources and pilot result files. `parity-pilot-command.json` records the command, timestamps, failing status and traceback.

## Exact parity result

Four headless agent sessions ran: one per arm for each profile. There were 20 local scripted-model requests total, each session completing four read calls plus one final answer. Both arms exited successfully in both profiles. Dummy response usage fields are synthetic and must not be used as real token/cost measurements.

**Blank profile:** all five normalized request objects matched, as did response-body hashes, declared tool schemas, requested tool calls, tool results, initial fixtures and stdout/stderr.

**Synthetic-realistic profile:** the differing request fields are precisely:

```text
$[0].messages[0].content
$[1].messages[0].content
$[2].messages[0].content
$[3].messages[0].content
$[4].messages[0].content
```

Observed skill-list order within the system prompt:

```text
standard Pi: skill0, skill1, skill2, skill3, skill4, skill5, skill6, skill7
Pi-Bolt:     skill7, skill6, skill5, skill4, skill3, skill2, skill1, skill0
```

The scripted HTTP response bodies, expected tool calls, tool results and final output nevertheless matched. A deterministic server returns prescribed responses rather than modeling how a real model reacts to changed instruction order; identical scripted output therefore does not remove the input-parity failure.

Evidence: `results/parity-pilot/realistic.diff` and `pilot-analysis.json`. This is one observed pair, not proof of stable ordering across all launches, an established defect, or a quality regression. No root-cause change, automatic normalization, retry, extra experiment, GitHub issue or public report was attempted.

## Failures and limitations retained

- Original unshare denial remains documented in the parent directory; no security policy was relaxed.
- Two preparatory metadata-check mistakes were preserved in `preparation-errors.json`: a Docker Go template assumed an optional image field, and an initial validator assumed tmpfs appeared in Docker's bind-mount list. Actual inspect JSON stores tmpfs under `HostConfig.Tmpfs`; the validator checked that field and the three bind mounts separately. Neither correction changed sandbox settings or weakened a security requirement. No in-container isolation probe had failed.
- Comparator TDD red (missing module), followed by seven passing unit tests, is saved in `parity-tests-red.json` and `parity-tests-green.json`; the expected red is not an agent/runtime failure.
- The actual realistic-profile parity gate failed with exit status 1. That failure is preserved and ended workload execution.
- No process-tree collector was implemented/validated, no randomized measurement schedule was executed, and no warmup or measured observations exist. Median/p95 differences and bootstrap confidence intervals are therefore **unavailable**, not zero.
- Production-service settings were untouched. The host had two active Orbi services during inspection; this is not a reservation of idle cores or proof of zero shared-host interference. Any future performance run still needs its production-safety/interference checks.

## Cleanup and scope

The owned ephemeral container `bb-bench-p1-20261115` (`11d58f9745b74e373e2d987474c27cf674e59b020b9505cca0c31c6e06305092`) was removed after retaining inspect data; absence was verified. No other container was stopped or altered. Evidence and private copied inputs remain locally for reproducibility.

No software/image installation, pull, kernel/service change, production Orbi change, paid inference, external model request, GitHub operation, log upload or benchmark publication occurred under this amendment. The previously authorized A3 comment remains the only publication; it was not edited or revisited.

## Available next choices — require approval, not executed

1. **Narrow Phase 1 to the minimal profile**, explicitly excluding resource-discovery claims. First validate full process-tree CPU/PSS/private-memory instrumentation, then run the authorized warmup/pair counts only for the newly approved cells.
2. **Revise the realistic-profile protocol** to control skill ordering, or explicitly accept and report a matched-work product comparison with different prompt ordering. This requires a declared protocol change; do not sort the captured prompts post hoc and call them equivalent, and do not modify installed products as a hidden benchmark fix.

No Phase 2 or additional public action is authorized. Execution is stopped pending a decision on the parity failure.
