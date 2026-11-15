# Phase 2B handoff v2 — Experiment A first, offline only

Supersedes `HANDOFF-v1.md` (kept unchanged, SHA256
`4665c16f8117ccce48bec6e954bea7daae4164eb3e9a5745d78d0a564db84bac`).

## Objective

Find out whether Pi-Bolt gives Orbi a meaningful operational advantage over
standard Pi: lower CPU, memory and wall overhead per agent session, with the
model seeing the same thing. The goal is not to show that the model decides
better under one executable. If the two present identical requests, tool results
and context, differences between independent coding runs are model variability.

## Authorization

Offline preparation and validation only. Not authorized: paid inference, any
GitHub write, installation or image/package pulls, production service, timer or
config changes, account changes, publication. The $20 budget in the protocol is a
proposal, not an approval. Ask before anything outside this list.

## Read first

Work directory `~/git/orbi`, plan directory
`.orbi/benchmark-design/phase2b-design/`.

1. `PHASE-2B-PROTOCOL.md` — protocol v1. Unchanged; do not edit.
2. `PROPOSED-AMENDMENTS.md` (revision 3) — the reordering, the A3 replay with its
   fidelity check, and the thresholds this handoff follows. The same text is
   merged into `PHASE-2B-PROTOCOL-v2-PROPOSAL.md`. Both are proposals; do not
   start step 1 until the owner approves v2.
3. `READINESS.json`, `design-manifest.json` — status and hashes.
4. `../subscription-pilot/openrouter-v1/REPORT.md`, `TRAJECTORY-FINDINGS.md`,
   `results/coding-pair/COMPARISON.json` — the consumed pilot pair.

`task-selection.json`, `schedule.json` and `budget-proposal.json` belong to
Experiment B and are not needed for this stage.

## Work, in this order

**0. Approval and thresholds.** Get the owner's approval of the v2 proposal,
including the P4 thresholds (separate for A2 and A3). Record the approved text
with a hash. Do not run A without it. The owner may revise the thresholds once,
after the standard-Pi-only calibration and before any Pi-Bolt resource
measurement.

**1. Collector.** Implement the collector specified in protocol §7 and pass its
whole offline calibration matrix with the gates as written there. The pilot's
CPU-accounting and observer-overhead failures stay recorded as failures; do not
tune a tolerance until they pass. A calibration failure stops the stage.

**2. A1 — parity.** Protocol §4 A1, 24 offline launches. Compare full
model-visible request bodies, tool definitions, tool results, errors and stop
metadata. Report the known reversed skill order as a finding, and record how the
benchmark profile differs from the production Pi profile on this host (skills,
discovery, compaction, retries).

**3. A2 and A3 — runtime measurement.** A2 as in protocol §4 (synthetic
workloads). A3 follows `PROPOSED-AMENDMENTS.md` P3 in its three steps: replay
fidelity check with resource collection off, then the standard-Pi-only
feasibility calibration, then the frozen measured schedule. A material fidelity
difference invalidates that trace: stop and report, do not force the replay.
Report agent-process CPU and memory separately from tool children.

**4. Report.** Measured effects with paired distributions and intervals, each set
against the step 0 threshold, with "below threshold" stated when true. Include
every parity mismatch and every failed gate.

**5. Stop.** Hand the report to the owner for a decision on Experiment B.

## Do not

- Start the six acceptance suites, freeze B prompts, or prepare task #7's offline
  package cache. All of that waits for the decision in step 5.
- Rerun, pool or reinterpret the pilot. Replay in A3 reads its saved bytes only.
- Patch an executable or normalize its output to obtain a parity pass.
- Change `PHASE-2B-PROTOCOL.md`, the pilot evidence, or
  `../publication-draft/discussion-body.md` (SHA256
  `c96af3c7a5ee5795e6bc8ead39c20fe3269e9300ea215373b8e29739e6ba4af3`).
  New proposals go in `PROPOSED-AMENDMENTS.md` or a new dated file.
- Stop or reschedule production Orbi jobs to quiet the host. Record host load
  alongside each measurement instead.

## Experiment B is conditional

If A shows the executables are behaviorally equivalent, a proposal to run B must
explain what engineering question further stochastic coding runs answer beyond
measuring model variability. If B is proposed, it must meet
`PROPOSED-AMENDMENTS.md` P6: historical positive controls for acceptance tests, a
context-limit rule, a calibrated collector, the pilot's unreconciled
reservations explained, and statistics suited to six task contexts.

## This stage is complete when

1. Owner-approved thresholds are recorded and hashed (step 0).
2. The collector passes every §7 calibration gate, with raw evidence kept; or the
   stage stopped at the first failed gate with that failure reported.
3. A1 has run all 24 launches and every mismatch is listed with raw bytes.
4. A2 and A3 have run their sealed schedules, or A3 is reported infeasible with
   the reason.
5. One report states each measured effect against its threshold and gives a
   recommendation on B.
6. A manifest lists hashes of all new fixtures, schedules, raw results and the
   report; the v1 protocol, pilot files and publication draft hashes are
   re-verified unchanged.
7. Counts are stated: paid calls 0, GitHub writes 0, installs 0, production
   changes 0.

## Pilot facts to keep straight

- Pi: 36 requests, $0.03100888560, 401.8 s. Bolt: 44 requests, $0.05733484120,
  793.5 s. Both passed the common acceptance. One pair only.
- Both failed the original CPU-accounting gate; Pi also failed observer overhead
  under 1%.
- Bolt request 12: 65,536 completion tokens, native finish `length`, empty bash
  arguments already present in the upstream stream; 34% of Bolt's bill. Not
  attributable to a Bolt parser on this evidence.
- Every tool call in both arms was `bash`.
- Prior exposure $0.88835509480, including $0.80 held for two rejected requests
  whose cost was never reconciled.
