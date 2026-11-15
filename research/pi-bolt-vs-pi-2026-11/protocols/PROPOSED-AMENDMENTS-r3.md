# Proposed amendments to PHASE-2B-PROTOCOL.md v1 — revision 3

**Status: proposals only.** `PHASE-2B-PROTOCOL.md` (SHA256
`ced278f3f15dd6754732e62ce69d37b194c290361c008f19886bedfde2e9b024`) is unchanged
and stays the reference text. Nothing here is approved methodology until the
owner accepts it. Revision 1 is kept as `PROPOSED-AMENDMENTS-r1.md` (SHA256
`41adc3f8eb9ae7e1155b94f2abdf73dfb5695f31de29054a491251d523883698`).
Revision 2 (`PROPOSED-AMENDMENTS-r2.md`, SHA256
`1db8168853bde3018cdb4198473fcf018df3638c46e5fdc09dad08bd5d3946ba`) replaced P3
and P4 and added P7. Revision 3, 2026-11-15, records two owner decisions in P4
(primary and secondary outcomes; the wall-overhead rule) and adds fidelity
checking of every measured launch in P3. No experiment was executed to write it.

## Why

v1 lets Experiment B run only when A1 shows the two executables send the model
identical requests under the four-tool policy. In that case both arms sample the
same model distribution on the same inputs, so B's four primary outcomes
(success, requests, tokens, cost) have an expected difference of zero and 48 paid
runs mostly measure model variability. The outcomes an executable can move (CPU,
memory, wall overhead) are secondary in B and, in the pilot, followed the
trajectory rather than the executable. The objective is therefore restated:

> Does Pi-Bolt reduce Orbi's operational resource consumption per session enough
> to matter, without introducing behavioral regressions?

It is not "does Pi-Bolt make the model decide better".

## P1. Order: A before any B preparation

Collector, then A1, then A2, then A3, then a report, then an owner decision on B.
The six acceptance suites are not started before that decision. (v1 §12 lists
the suites as gate 2 and A as gate 4.)

## P2. A1 reports the skill-order mismatch per profile

v1 already includes skill scenarios 11 and 12. Amendment: A1 reports parity
separately for two profiles, and neither result stands in for the other:

- **Native profile**: skills and discovery enabled as each executable ships.
  The known reversed skill order is expected here and is reported as a product
  difference.
- **Restricted profile**: the four-tool policy with skills and discovery off
  (the profile v1 uses for B).

No output is sorted or rewritten to make the profiles agree; v1 §4 forbids that
and this amendment keeps it. A pass on the restricted profile supports claims
about the restricted profile only. The report also records which profile the
production deployments on this host run (skills, discovery, compaction,
retries), so the reader can see which result applies to Orbi.

## P3. New A3: long-session replay of the pilot's Issue #3 traces

A3 is the deciding experiment for the restated objective, provided its replay
fidelity holds. v1's synthetic A2 stays as specified and is supporting evidence
about short workloads.

### Source and design

- Source: the saved relay streams of the two consumed pilot executions,
  `subscription-pilot/openrouter-v1/results/coding-pair/relay/` (Pi, 36
  responses) and `.../coding-pair/pi-bolt/relay/` (Bolt, 44 responses). Issue #3
  is not a B task, so v1 §4's ban on replaying a B task's solution is untouched.
  This re-uses saved bytes; it is not a rerun of the pilot.
- 2 traces x 2 executables. A local fixture serves the recorded responses in
  order with no added delay; tools execute for real in a fresh copy of the pilot
  workspace. No endpoint, credential or relay route.
- The Bolt-recorded trace contains the capped empty `bash` call (request 12), so
  both executables are observed recovering from the same response.

### Step 1 — replay fidelity, before any measurement

The recorded responses were generated against the tool output of the original
run. Fed back against different tool output, they can form a conversation that
could not have happened. Fidelity is therefore checked first, with resource
collection switched off so no effect is seen early:

1. Replay each trace once on each executable (4 launches), and each trace a
   second time on standard Pi (2 launches) to show run-to-run nondeterminism
   within one executable.
2. Compare, per request, against the recording and across executables: the
   tool-call sequence, each tool call's exit status and error category, test
   pass/fail counts where the output carries them, and the final workspace file
   manifest.
3. A difference is **tolerated** only if it is confined to a list of volatile
   fields written down before the check runs: durations, timestamps, PIDs,
   temporary paths, port numbers. The list is frozen with its hash first.
4. Any other difference is **material**: a tool call that succeeded in the
   recording and fails in replay (or the reverse), a changed test count, a
   differing final file, a request the fixture cannot match to the next recorded
   response. A material difference on a trace makes that trace invalid for A3.
   Stop and report it; do not edit tool output, the trace or the executable to
   continue. If both traces are invalid, A3 is reported infeasible and the
   decision rests on A1 and A2 with that limit stated.

### Step 2 — wall-time accounting by event boundaries

"Non-model/tool wall overhead" is defined on one monotonic timeline per launch:

- Model intervals: from the first byte of a request leaving the agent to the
  last byte of the fixture's response being delivered.
- Tool intervals: from a tool child's start to its reaping, for every child.
- Overhead = root lifetime minus the measure of the **union** of all model and
  tool intervals. Summed durations are never subtracted, because overlapping
  tool calls and streaming would be counted twice.

The collector calibration (v1 §7) gains one fixture for this: scripted
overlapping intervals of known length, where the computed union must match the
known value within the timestamp resolution.

### Step 3 — bounded feasibility calibration, then a frozen schedule

- Run at most 2 launches per trace on **standard Pi only**, each bounded at 60
  minutes. This yields launch duration and the standard-Pi baselines for
  agent-process CPU and memory. Pi-Bolt is not measured here, so the size of the
  effect stays unseen while the schedule and thresholds are finalized.
- Freeze the measured schedule before collecting it. Default proposal: 2 warmup
  pairs and 10 measured pairs per trace, alternating executable order (48
  launches), with a ceiling of 8 hours of host time for all of A3. If the
  calibration shows 10 pairs per trace will not fit, reduce the count; below 6
  pairs per trace A3 is reported descriptively with no intervals.
- The 30-pairs-per-cell figure in revision 1 (120 launches plus warmups) is
  withdrawn as disproportionate until the calibration says otherwise.

### Fidelity during measurement

Passing step 1 once does not cover later launches. Every warmup and measured
launch records the same per-request comparison as step 1. A launch with a
material difference is kept, marked invalid and excluded from the effect
estimate with its reason; it is not rerun or replaced. If more than 2 of the 10
measured pairs on a trace are invalid, that trace is reported as invalid for A3,
because precise numbers for a conversation that could not have happened answer
nothing.

### Measures

Per launch: agent-process CPU and peak PSS/private memory, separately from tool
children; whole-tree CPU and peak PSS; wall overhead as defined above; memory at
fixed request indices to show growth across the session; request-body parity at
every step. Host load is recorded beside each launch because production Orbi
jobs keep running on this machine.

## P4. Provisional minimum practically meaningful improvements

These are owner decision thresholds, not statistical significance criteria and
not automatic approval to change any Orbi default. Each metric is judged on its
own; there is no combined score. CPU, memory and wall overhead each need both a
relative and an absolute improvement, because a large percentage of a small
number saves nothing.

| Metric | Role | A2: short scripted runs | A3: long-session replay |
|---|---|---|---|
| Agent-process CPU | primary | at least 25% and 50 ms lower | at least 20% and 2 s lower |
| Agent-process peak PSS | primary | at least 25% and 32 MiB lower | at least 20% and 50 MiB lower |
| Whole-tree peak PSS | secondary | report only | at least 15% and 75 MiB lower |
| Non-model/tool wall overhead | secondary | report only | at least 10% and 2 s lower |
| Startup | descriptive | report only | report only |

**Primary and secondary outcomes are judged separately.** A secondary outcome
below its threshold does not change the status of a primary outcome, and a
primary outcome that is met does not upgrade a secondary one. In particular, if
Pi-Bolt lowers its own memory but tool children dominate the tree, the report
says "agent-process memory: met; whole-tree memory: below threshold" and shows
both numbers with the share of the tree peak that the agent process accounts
for.

**How a threshold is judged.** The effect is the median of the paired
differences (Pi minus Pi-Bolt), with its paired-bootstrap interval reported
beside it. In A3 a threshold is "met" only when the median meets both parts on
every valid trace; met on one trace and not the other is reported as "mixed".
Anything else is "below threshold", stated plainly.

**Are they realistic?** Partly unknown, and the report must say so:

- The pilot measured whole-tree memory only: 669 MiB (Pi) and 860 MiB (Bolt)
  sampled peak, in runs with different trajectories. It never isolated the agent
  process, so the 32 MiB and 50 MiB figures have no measured baseline yet. If
  the standard-Pi agent process turns out to peak below about 250 MiB, the
  absolute part (50 MiB) is the binding one in A3; above that, the 20% is.
- In A3 both executables run the same tool children, so a whole-tree saving can
  only come from the agent process. At the pilot's tree size, 15% is roughly
  100 MiB, which is stricter than the agent-process row. The tree row can
  therefore fail while the agent row passes; that is expected, not a
  contradiction.
- Pilot tree CPU was 53 s and 84 s, mostly test runs. Agent-process CPU alone was
  not recorded. A 2 s absolute saving is plausible only if the agent process
  itself uses about 10 s or more per session.
- The fixture serves responses with no delay, so wall overhead in A3 is small in
  absolute terms; 2 s may be unreachable for either executable.

**Wall-overhead rule, fixed now.** After the standard-Pi-only calibration and
before any Pi-Bolt resource measurement, compute standard Pi's wall overhead on
each trace (median of the calibration launches). If it is under 2 s on either
trace, the A3 wall-overhead row becomes report-only for both traces; otherwise
the row stands as written. The outcome is recorded with its hash before the
measured schedule starts. This is a mechanical rule: it is applied from the
calibration numbers alone and is not reopened once Pi-Bolt has been measured.

The owner may revise the numbers once, after the standard-Pi-only calibration in
P3 step 3 and before any Pi-Bolt resource measurement. Revisions after that
point are amendments labelled as made with results in view.

**What the thresholds do not show.** A3 is per-session efficiency. It is not
evidence that the host can run more workers. This host has about 62 GiB of RAM
and kept more than 39 GiB available during the pilot; 50 MiB saved across 12
slots is 600 MiB, which is useful but changes no capacity limit. A capacity
claim would need a separate multi-agent load test (throughput, memory pressure,
latency, failures), which is not part of this protocol.

## P5. Collector tolerances

The pilot's failed gates stay failed and are not re-scored. New measurements use
the tolerances in v1 §7, which are justified there independently of the pilot
values (counter resolution, a 5% agreement with self-CPU references, coverage and
gap rules) and are fixed before any data is collected. P3 step 2 adds one
calibration fixture for the interval-union timeline. No tolerance is chosen by
looking at what would make an earlier number pass.

## P6. Conditions if B is later proposed

B stays conditional. A proposal to run it must first state the engineering
question it answers that A could not, given the parity result. If it proceeds:

1. Each acceptance suite fails on the baseline and passes on the historical
   merged solution (PRs 10, 16-20), checked before sealing.
2. A written context-limit rule: what happens when a request reaches the model's
   context window with compaction off, and how that attempt is counted.
3. Collector passed v1 §7 calibration.
4. The pilot's two unreconciled reservations (USD 0.80) are explained and the
   cause is fixed or bounded, since v1 §8 stops the whole batch on unknown
   billing.
5. Statistics fit six task contexts in one repository: resample all four pairs
   per task (not two-and-two by order), or use the six task effects as the unit;
   report a median or cap-incidence view beside means; no interval claims beyond
   those six tasks. Four tasks share one source archive and are disclosed as
   such.
6. A size justified by the question, which may be far fewer than 48 runs, and
   may include a Pi-versus-Pi pair to show the noise floor.

## P7. What the report may claim

- Parity is claimed per profile (P2). "Equivalent" is never used for the product
  as a whole on the strength of the restricted profile.
- Resource results are stated against P4 as met, mixed or below threshold, per
  metric, with the baseline that made each threshold binding.
- A result below threshold is reported with the same prominence as one above.
- Nothing in the report changes a default. It goes to the owner for a decision.
