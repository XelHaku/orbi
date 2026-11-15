# Pi vs Pi-Bolt research archive (November 2026)

Measurements of the Pi-Bolt executable against standard Pi as the agent runtime
under Orbi, made on one Linux host. Start with [REPORT.md](REPORT.md).

This is a curated copy. Raw evidence (model request and response streams, agent
event logs, per-launch samples, container records) stays on the measuring host
and is not published here; [EVIDENCE-MANIFEST.json](EVIDENCE-MANIFEST.json)
lists what exists and its hashes.

## Contents

| Path | What it is | Status |
|---|---|---|
| `REPORT.md` | Experiment A report: short workloads, long-session replay, compatibility, limits | Result |
| `plan/HANDOFF-v3-executed.md` | The plan that was actually run | Executed |
| `plan/HANDOFF-v1-superseded.md`, `plan/HANDOFF-v2-superseded.md` | Earlier, larger plans | Superseded, not run |
| `protocols/PHASE-2B-PROTOCOL-v1-original-not-executed.md` | Original protocol, including 48 paid coding runs | Not executed |
| `protocols/PHASE-2B-PROTOCOL-v2-proposal-not-approved.md`, `protocols/PROPOSED-AMENDMENTS-r3.md` | Revised design putting offline measurement first | Proposal, not approved |
| `summaries/phase1-*.md` | Short-workload benchmark (240 measured runs) and the parity failure with skills enabled | Earlier result |
| `summaries/coding-pilot-*.md` | One paid coding pair and its trajectory analysis | Earlier result, one pair only |
| `experiment-a/source/` | Replay fixture, collector, launcher, fidelity comparison, analysis | Sanitized copies of the scripts used |
| `experiment-a/schedule.json` | Measurement schedule fixed before measuring | Executed |
| `experiment-a/results/` | One row per measured launch, and the summary | Result |
| `EVIDENCE-MANIFEST.json` | Hashes of archived files and of their local originals; inventory of local raw evidence | Manifest |

Documents are archived as written at the time. Some describe plans that were
later narrowed; the status column says which. The reports record
authorization boundaries and spending because they were written as working
records. In the coding-pilot summaries, settled charges (about USD 0.088) are
separate from USD 0.80 of reserved exposure for two rejected requests whose cost
was never reconciled; the latter is a conservative hold, not a known charge.

## What was measured, briefly

1. Parity spot-check: one scripted session on each executable, comparing every
   request body and the final files.
2. Replay fidelity: the two recorded sessions replayed on each executable and
   compared with the recording.
3. Long-session measurement: 5 pairs per recorded session, alternating order.

No model was called. A local fixture served recorded responses inside a
container with no network.

## Reproducing

The scripts are sanitized copies of the ones that ran: the home directory was
replaced by `~`, so `host_run.py` will not run until its paths are set. The
archive does not run unchanged and does not contain the replay inputs.

The scripts expect inputs that are not in this archive: the two pinned
executables, a Node binary, the task workspace with its dependencies, and the
recorded response streams. With equivalents of your own:

1. Put `*-response.sse` files (one streamed chat-completions response per
   request, in order) in a directory, the task prompt in a file, and the
   starting workspace in a directory.
2. Adjust the paths at the top of `experiment-a/source/host_run.py` (builds,
   inputs, image, the Docker binary) and the executable hashes in `PINS`.
3. One launch:
   `python3 experiment-a/source/host_run.py <label> <standard-pi|pi-bolt> <responses_dir> <prompt_file> <base_dir>`
4. Fidelity against a recording:
   `python3 experiment-a/source/fidelity.py <recorded_dir> <delivery_manifest.json> <result_dir_a> <result_dir_b>`
5. The fixed schedule and summary: `run_schedule.py`, then `analyze.py`.

`make_spot.py <dir>` generates the parity spot-check fixture, which needs no
recorded data.

The collector is Linux-only (child subreaper, `/proc/<pid>/smaps_rollup`).
In the archived copies, home-directory paths were replaced by `~` and the
measuring host's name by "benchmark host"; the manifest counts both per file.

## Limits

One host, one task, two recorded model trajectories, five pairs per trace,
skills and extensions off. See the report's "Not measured" and "How much to
trust" sections before quoting any number.
