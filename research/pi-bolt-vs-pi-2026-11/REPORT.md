# Pi vs Pi-Bolt: rough numbers from offline measurement

2026-11-15. Published as part of a curated research archive; raw evidence
(recorded model streams, agent logs, per-launch samples) remains local, so this
is not a self-contained reproduction package. Rough engineering numbers, not a
preregistered study and not a case for changing a default.

Pinned builds: standard Pi 1.5.2 on Node 24.19.0, and Pi-Bolt 1.2.1 (Pi 1.5.2).
One benchmark host (Ubuntu 24.04.4 LTS, AMD Ryzen 9 5900X, 24 logical CPUs,
about 62 GiB RAM), cached `python:3.12-slim` container, no network, two CPUs,
3 GiB.

## Main finding

Pi-Bolt showed a substantially smaller agent-process resource footprint on two
fixed coding trajectories. Median paired savings in sampled peak memory were 72
to 85 MiB, and its recorded pre-exit CPU counters were lower by about 1.0 to 1.3 s
per session (standard Pi's read 1.2 to 1.6 s). Whole-session CPU and elapsed time showed
no consistent advantage across five pairs per trajectory.

These are rough offline measurements of scripted tool workloads derived from
real sessions. CPU accounting, sampling overhead, shared-host activity and
replay deviations limit interpretation. They do not establish faster live-model
deliveries, lower inference costs, greater worker capacity or a better default
backend.

The practical implication is narrower: Pi-Bolt is a plausible option for users
who want a lighter agent process, while tests, builds and model behavior can
dominate the overall workflow.

## Read these limits with every number below

- **Instrumented, not clean, measurements.** The collector's own CPU was 3.3 to
  4.8% of wall time in the long-session runs. Its original fixed
  CPU-accounting check (20 microseconds) **failed in all 20 launches**, as it did
  in the earlier paid pair. Every launch was inside a counter-resolution bound
  proposed afterwards; that is diagnostic context and does not turn the failed
  check into a pass.
- **"Completed cleanly" means the launch ran to the end**, consumed every
  recorded response and produced the expected files. It does not mean every
  measurement-quality check passed.
- **The long workload is a scripted tool workload derived from two real coding
  trajectories, not an identical live conversation.** Both executables
  processed the same recorded response streams and produced the original final
  files. Some intervening tool outputs differed, including the harness observing
  itself. The section "Replay fidelity" says exactly what differed and which
  deviation from the plan was accepted.
- **Agent CPU is a pre-exit counter, not an exit-accounted total.** See "Other
  limits".
- **Two trajectories of one task, measured five pairs each.** The 20 launches
  are repeated measurements, not 20 coding tasks.
- **Wall-time differences of about a second are inside the run-to-run spread**
  and are not a speedup claim.

## Short scripted workloads (existing Phase 1 result)

30 pairs per cell, 240 measured runs, separate timing and memory passes, zero
parity failures on the minimal profile.

| Median | Standard Pi | Pi-Bolt | Paired reduction (95% CI) |
|---|---:|---:|---:|
| Startup (`--version`) wall | 280 ms | 11 ms | 96.0% (95.4 to 96.1) |
| Headless run wall (four read calls) | 472 ms | 46 ms | 90.6% (90.0 to 91.2) |
| Headless process-tree CPU | 558 ms | 34 ms | 93.9% (93.5 to 94.2) |
| Headless sampled peak memory (PSS) | 143 MiB | 65 MiB | 54.9% (54.6 to 55.2) |

Pi-Bolt has a fast path for `--version`, so the startup row is not full
application readiness.

## Long scripted tool workloads derived from two real coding trajectories (new)

The two saved model-response streams from an earlier paid coding pair (one
historical paseo-orbi task; 36 requests recorded under standard Pi, 44 under
Pi-Bolt) were replayed through both executables. A local fixture served each
recorded response in order with no delay; every tool call (tests, typecheck,
file writes) ran for real. So the model wait is zero and wall time is tool time.
Serving the saved responses fixes the sequence of tool calls; it does not show
that a live model would choose the same next action after seeing the slightly
different tool output.

5 pairs per trace, order alternated, 20 launches, count fixed before measuring.
Values are median (min to max). The saving is the median of the five paired
differences (Pi minus Pi-Bolt within each pair), so it need not equal the
difference between the two medians shown beside it. The percentage is that
saving divided by standard Pi's median.

**Trace recorded under standard Pi (36 requests)**

| Per session | Standard Pi | Pi-Bolt | Saving |
|---|---:|---:|---:|
| Agent CPU at final sample | 1.20 s (1.16 to 1.26) | 0.16 s (0.15 to 0.19) | 1.04 s, 87% |
| Agent-process peak memory | 167 MiB (163 to 200) | 83 MiB (81 to 85) | 85 MiB, 51% |
| Whole-tree peak memory | 677 MiB (673 to 712) | 642 MiB (634 to 664) | 42 MiB, 6% |
| Whole-tree CPU | 55.9 s (54.7 to 56.5) | 54.9 s (53.2 to 57.4) | 0.9 s, 2% (pairs ranged -1.1 to +2.7) |
| Wall time | 42.6 s (41.2 to 43.4) | 41.8 s (39.1 to 43.4) | 1.1 s, 3% (pairs ranged -0.7 to +3.6) |

**Trace recorded under Pi-Bolt (44 requests)**

| Per session | Standard Pi | Pi-Bolt | Saving |
|---|---:|---:|---:|
| Agent CPU at final sample | 1.58 s (1.52 to 1.76) | 0.26 s (0.24 to 0.28) | 1.34 s, 85% |
| Agent-process peak memory | 186 MiB (171 to 192) | 110 MiB (89 to 115) | 72 MiB, 39% |
| Whole-tree peak memory | 905 MiB (871 to 922) | 871 MiB (844 to 890) | 33 MiB, 4% (pairs ranged -19 to +68) |
| Whole-tree CPU | 92.8 s (90.7 to 96.1) | 94.2 s (91.0 to 99.6) | -0.7 s (pairs ranged -8.2 to +1.5) |
| Wall time | 67.9 s (66.1 to 70.3) | 69.8 s (66.2 to 76.5) | -0.4 s (pairs ranged -8.8 to +1.5) |

Whole-tree CPU and wall time show no consistent direction; the differences are
inside the run-to-run spread of the test runs. Two separate denominators apply.
Of local CPU, the agent process is about 2% on these workloads, with or without
a model. Of elapsed time, a live session adds the model wait (the paid runs took
402 s and 793 s), so any runtime saving is a smaller fraction of elapsed time
than it is here.

### Against the yardsticks written before measuring

| Yardstick | Result |
|---|---|
| Agent-process CPU at least 20% and 2 s lower | Not met. The pre-exit counters were 85 to 87% lower, but only by 1.0 to 1.3 s, because standard Pi's process shows 1.2 to 1.6 s in the whole session. |
| Agent-process peak memory at least 20% and 50 MiB lower | Met on both traces (smallest pair: 58 MiB). |
| Whole-tree memory and wall time | Reported above: 33 to 42 MiB of 680 to 900 MiB; no consistent wall-time advantage observed across five pairs per trace. |

## Compatibility

- **Requests with skills off (the profile used here).** A scripted session
  covered bash (stdout, stderr, non-zero exit, timeout, 20,000-line output),
  write, edit (unique, absent and ambiguous match), read (offset and limit,
  missing file) and a capped response whose bash call has empty arguments. All
  11 requests were byte-identical between the two, except the random name of a
  temp log file, which also differs between two runs of standard Pi. Final files
  were identical. Both rejected the empty-arguments call with the same
  validation error and continued.
  This restricted-profile spot check found no material behavioral mismatch in
  the covered cases. It is not a claim of equivalence beyond them, and the
  replay differences are documented separately under "Replay fidelity".
- **Skills on.** In the earlier Phase 1 check the two listed the same eight
  skills in opposite order in the system prompt. That is a model-visible
  difference for anyone running with skills enabled, and it is not covered by
  the results above.
- **In use.** 23 Pi-Bolt deliveries across two repositories completed through
  Orbi (recorded on orbi-build/orbi#2182). That shows it works; it is not a
  comparison.

## Not established

- General differences in live-model delivery time, token use, cost or success.
  One exploratory paid pair on one task was measured: both passed the same acceptance checks; standard
  Pi took 402 s and $0.031, Pi-Bolt 793 s and $0.057. The two runs took different
  model trajectories from an identical first request, and one capped model
  response was 34% of Pi-Bolt's bill. One pair cannot separate the executable
  from model variability.
- Capacity (not measured). A per-session saving is not evidence that a host can run more
  workers. 85 MiB across 12 concurrent sessions is about 1 GiB.
- Behavior with skills, extensions, MCP, compaction or retries enabled: all were
  off in every run here.

## Replay fidelity

What was checked in every one of the 20 measured launches, and before them in
16 check launches across three harness revisions: 4 on the first revision (each
trace once per executable), then 6 on each of the second and third (the same
four, plus each trace a second time on standard Pi). The findings below describe
the third revision, which is the one the measured launches used; the earlier
check launches are kept and the two faults they exposed are described at the end
of this section.

- **Responses consumed.** All 36 or 44 recorded responses were requested, in
  order, and none beyond them. Because the fixture serves the recorded
  responses, the sequence of tool calls is the recorded one by construction.
- **Final files.** The 31 delivered files were byte-identical to the files the
  original paid run delivered, on both executables, in every launch.
- **Request bodies against the recording.** Only the first request was
  byte-identical. Every later request contains earlier tool output, and that
  differed in two ways:
  1. *Timestamps and durations* (file dates in directory listings, test
     durations), in 15 to 24 tool results per launch. The plan expected these.
  2. *The agent reading the benchmark's own run files*, in 1 to 5 early tool
     results per launch (of 36 or 44 requests). During exploration the model had
     listed and searched the workspace, which includes the harness's own
     artifacts: the agent's live event log, its session ID, the command line of
     the executable under test, a temp-log directory's link count, and search
     hits inside its own earlier output. These necessarily differ from the
     recording, and they also differ between two runs of standard Pi.
- **Everything else matched** after masking timestamps and durations: test
  results, typecheck output, error messages and file contents shown to the
  model.

**The accepted deviation.** The plan tolerated four kinds of difference
(durations, timestamps, PIDs, temporary paths) and said anything else makes a
trace unusable. Kind 2 above is a fifth kind. It was reported to the owner and
accepted before the measured runs were analyzed. The argument for accepting it:
it is confined to the harness observing itself, it is not specific to either
executable, and the session's actual work product is identical. The argument
against: the model's later recorded responses were written after seeing the
original versions of those few tool results, so the replayed conversation is not
one the model literally had. Readers who reject the deviation should treat the
long-session numbers as measurements of a scripted tool workload derived from a
real session, which is still what the resource figures describe.

Two harness faults were found and fixed during the fidelity check, before any
measured launch: the fixture first wrote its files inside the workspace, and the
harness sources were mounted at a different path than in the recording. Both
changed what the agent's own searches returned. The earlier check runs are kept.

## Other limits on the long-session numbers

- **Agent CPU at final sample** is the process's cumulative counter at the final
  pre-exit sample, not an exit-accounted total. Counter resolution is 10 ms, and
  the final sample preceded exit by up to 235 ms (7 to 235 ms for standard Pi,
  10 to 222 ms for Pi-Bolt). CPU consumed after that sample is omitted; its
  magnitude and effect on the comparison have not been established. The only
  evidence on its size is indirect: in the launches where the final sample
  happened to fall within 22 ms of exit (three per executable), the last 250 ms
  interval before it showed 20 to 60 ms of CPU for standard Pi and none at
  counter resolution for Pi-Bolt. That is six launches, not a measurement of the
  tail. The whole-tree CPU figures are exit-accounted and do include it.
- **Sampled memory.** Peaks are the maximum of 250 ms samples and can miss short
  spikes.
- **Shared host.** Production jobs kept running; host load was 4.3 to 10.7 at
  launch starts. Five pairs give medians and ranges, not confidence intervals.
- **One task.** Other tasks will have different tool mixes, and a session that
  runs fewer or lighter tools would give the agent process a larger share.

## Reading

Across two recorded coding trajectories, Pi-Bolt consistently showed lower
agent-process CPU and lower sampled peak memory, while whole-session CPU and
elapsed time showed no consistent advantage. These are instrumented offline
replay observations with the accounting and fidelity limits stated above, not
measurements of live-model delivery speed.

The two halves fit together: the agent process is about 2% of the session's
local CPU, so even removing it entirely would save about 2%. Local CPU is
dominated by the tools the agent runs, and live elapsed time also by the model
wait. The restricted-profile spot check found no material behavioral mismatch in
the covered cases. That makes Pi-Bolt a plausible efficiency
option for people who want a lighter agent process. It does not establish faster
or cheaper deliveries, more capacity, or a better default.

Raw evidence is kept locally: 20 measured launches, 16 fidelity check launches
(4, 6 and 6 across three harness revisions), 3 parity spot-check launches, the
schedule and the scripts. Counts for this
stage: paid model calls 0, GitHub writes 0, installs or image pulls 0,
production changes 0.
