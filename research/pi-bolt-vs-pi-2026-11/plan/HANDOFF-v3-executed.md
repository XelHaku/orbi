# Pi vs Pi-Bolt handoff v3 — rough numbers, offline only

Supersedes `HANDOFF-v2.md` (kept, SHA256
`8e29c226cbae168872be2c36e10cb0f911bd7486f797cd4e61839c4a044c34f7`) and
`HANDOFF-v1.md`. The v2 protocol proposal and its amendments stay on disk as the
longer research design; this handoff runs only the part needed now.

## What this is for

The Orbi maintainer asked for "Pi-Bolt vs Pi numbers when you have them, even
rough ones", and said that if Pi-Bolt wins it could be made easier to pick. So
the deliverable is one short engineering report with credible numbers and stated
limits. It is not a preregistered study and not a case for changing a default.

## What already exists (do not redo)

- **Short-workload numbers**: `../container-phase1/minimal-v1/REPORT.md`. 240
  measured offline executions, 30 pairs per cell, zero parity failures on the
  minimal profile. Median headless run: wall 472 ms (Pi) vs 46 ms (Bolt),
  process-tree CPU 558 ms vs 34 ms, sampled peak PSS 143 MiB vs 65 MiB. Startup
  (`--version`): 280 ms vs 11 ms. This covers what protocol A2 would measure, so
  A2 is dropped.
- **A working harness**: the Phase 1 container setup, parity comparator and
  process-tree collector (calibrated on nested and orphaned process fixtures,
  CPU within 1% of per-process references). Reuse it.
- **Compatibility in use**: 23 Pi-Bolt deliveries across two repositories,
  recorded in the comment on orbi-build/orbi#2182. Evidence that it works, not a
  comparison.
- **Known difference**: with skills enabled the two executables list the eight
  skills in opposite order in the system prompt
  (`../container-phase1/REPORT.md`).
- **One paid coding pair** (`../subscription-pilot/openrouter-v1/REPORT.md`):
  both passed acceptance; Pi took 402 s and $0.031, Bolt 793 s and $0.057, on
  different model trajectories. One pair says nothing about which is faster, but
  it is unfavourable to Bolt and must appear in the report.

## The one missing number

Do the short-workload savings persist in a long, realistic agent session, where
most of the time and memory belong to the model wait and to test runs? That is
the only new measurement.

## Authorization

Offline only. Not authorized: paid inference, GitHub writes, installs or pulls,
production changes, publication. Posting the report is the owner's separate
decision.

## Work

**1. Parity spot-check (small).** Using the Phase 1 comparator, add bash, edit
and write scenarios, since every tool call in the paid pair was `bash` and Phase
1 only exercised `read`. Include the capped empty-arguments response from the
Bolt pilot trace (request 12). Report mismatches as found; do not sort or
rewrite output.

**2. Replay fidelity check.** Replay the two saved pilot traces (36 Pi
responses in `results/coding-pair/relay/`, 44 Bolt responses in
`results/coding-pair/pi-bolt/relay/`) once through each executable, with a local
fixture serving the recorded responses and tools running for real in a fresh
copy of the pilot workspace. Compare the tool-call sequence, exit statuses, test
counts and final files against the recording. Differences in durations,
timestamps, PIDs and temporary paths are expected. Anything else means the
replay is an artificial conversation: stop and report that trace as unusable
rather than forcing it.

**3. Replay measurement.** For each usable trace, 5 pairs alternating which
executable goes first (20 launches at most). Per launch record: agent-process
CPU and peak PSS separately from tool children, whole-tree CPU and peak PSS,
total wall, and host load. If the Phase 1 collector fails its own checks on a
long run, report the numbers as instrumented and say which check failed; do not
build the full §7 calibration matrix for this.

**4. Report.** One page, in English, saved locally as a draft:

- Short workloads: the Phase 1 table.
- Long sessions: medians and ranges for both executables on each trace, and the
  saving in absolute terms and as a share of the whole session.
- Compatibility: parity results, the skill-order difference, the 23 deliveries.
- Not measured: end-to-end delivery time with a live model, coding success,
  capacity or concurrency. Include the single paid pair with its caveat.
- A plain reading against the yardsticks below.

**5. Stop.** Hand the draft to the owner.

## Yardsticks for the long-session result

Not gates. They are what "worth making easier to pick" would look like, written
down before measuring so the reading is not fitted to the result:

- Agent-process CPU at least 20% and 2 s lower per session.
- Agent-process peak memory at least 20% and 50 MiB lower per session. (Phase 1
  showed about 78 MiB lower on a short run, so this is reachable if it holds.)
- Whole-tree memory and wall time: report the size of the saving next to the
  session total, since tool children and the model wait are expected to dominate.

## Limits to keep

- Time box: one working session, and it takes precedence over finishing every
  repetition. Time the fidelity-check launches first; if 5 pairs per trace will
  not fit, fix a smaller count before measuring (at least 3 pairs per trace,
  with both orders) and report the count actually run. Never stop early because
  of how the numbers look. If the fidelity check fails on both traces, write the
  report from existing evidence and say the long-session question is open.
- 5 pairs give medians and ranges, not confidence intervals. Say "rough".
- Per-session savings are not a capacity claim. This host has about 62 GiB of
  RAM and kept 39 GiB free during the pilot.
- Frame the conclusion as evidence for whether to make Pi-Bolt easier to select,
  not as a recommendation to change the default.
- Do not modify `PHASE-2B-PROTOCOL.md`, the pilot or Phase 1 evidence, or
  `../publication-draft/discussion-body.md`.

## Done when

1. Parity spot-check results are listed, with raw bytes for any mismatch.
2. Each trace is marked usable or unusable with the reason.
3. Replay measurements exist for every usable trace, or the report says why not.
4. The one-page draft exists locally with a hash.
5. Stated counts: paid calls 0, GitHub writes 0, installs 0, production changes 0.

## Later, only if the findings justify it

The larger design (`PHASE-2B-PROTOCOL-v2-PROPOSAL.md`: fuller parity matrix,
30-pair replay with intervals, corrected collector, conditional paid coding runs)
remains available and unapproved.
