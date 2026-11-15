# Phase 2B handoff — local plan, no execution authorization

## Task
Continue preparation of the Pi versus Pi-Bolt Phase 2B study using the saved protocol. The user will use another agent to execute the work. They asked this agent only to save the plan locally; do not treat this handoff as permission to start benchmarks, paid inference, publication or production changes.

## Start here
Repository/work directory: `~/git/orbi`.
Plan directory: `.orbi/benchmark-design/phase2b-design/`.

Read in order:
1. `PHASE-2B-PROTOCOL.md` — complete 4,481-word approval-stage protocol.
2. `READINESS.json` — explicit authorization status and blocking gates.
3. `task-selection.json` — six selected tasks, original starting SHAs, archive hashes and provenance.
4. `schedule.json` — proposed balanced 24 pairs / 48 coding attempts; all slots remain `not_run`.
5. `budget-proposal.json` — proposed limits, not approved spending.
6. `design-manifest.json` — hashes of the planning artifacts as recorded before this handoff file was added.

## Current state
- Selected paseo-orbi tasks: #14 and #15 (small), #6 and #7 (medium), #4 and #5 (large).
- Original starting commits recovered from Runner journal records, not merge parents.
- Source-only archives and current issue-body snapshots are saved as `issue-N-source.tar` and `issue-N.json`.
- Current issue bodies are not claimed to be the exact historical prompts.
- All six lockfiles match the pilot's dependency lock.
- Four repetitions per executable per task: 48 coding attempts, 24 adjacent pairs, two Pi-first and two Bolt-first pairs per task.
- Separate deterministic replay experiment proposes 444 offline native launches; none has run.
- No Phase 2B paid calls, benchmark launches, GitHub writes or production changes have occurred.
- Acceptance implementations, corrected collector and calibration are NOT ready. The protocol is not yet a sealed preregistration.

## Required next work, only after appropriate approval
- Freeze governing references, exact task prompts and benchmark adaptations.
- Implement six independent acceptance suites; validate baseline and negative controls.
- Implement and validate the corrected collector using the protocol's fixed accounting/sampling rules.
- Prepare and validate the deterministic replay fixtures, including tool errors and skill ordering.
- Obtain explicit permission before benchmark execution. Paid coding requires separate approval of the final sealed protocol and budget.
- Task #7 additionally requires approved sandbox-only offline package preparation from a private cache; no host installation or registry acquisition is currently authorized.

## Existing evidence and failures to preserve
Earlier pilot directory: `.orbi/benchmark-design/subscription-pilot/openrouter-v1/`.
Read `REPORT.md`, `TRAJECTORY-FINDINGS.md`, and `results/coding-pair/COMPARISON.json` for the two consumed pilot executions. Do not rerun or pool them into Phase 2B.

- Pi: 36 requests, $0.03100888560; Bolt: 44, $0.05733484120. Both passed common independent acceptance.
- Both failed the original fixed CPU-accounting tolerance; Pi also failed observer-overhead <1%. Those original failures remain failures.
- Bolt request 12 reported 65,536 completion tokens, native finish `length`, and upstream bash arguments `{}`; it cost $0.01961726368. Do not attribute it to a runtime parser without evidence or exclude it from totals.
- Initial cache conditions differed. Identical initial requests did not yield identical model trajectories.
- Saved deterministic traces show reversed skill ordering in the realistic profile; the four tested read-tool results matched. Expanded tool parity remains unproven.
- Nine existing offline analysis tests passed during planning; this is NOT validation of a corrected collector.

## Fixed proposal and limits
Retain pinned executables and OpenRouter `deepseek/deepseek-v4.1-flash-1017`, high reasoning, fixed `deepinfra/fp8`, no fallback, data collection denied unless separately approved otherwise.

Proposed new budget: $20 aggregate exposure, $2 per coding attempt, $0.40 request reservation, 80 requests and 60 minutes per attempt. These are NOT authorized amounts. Prior pilot exposure $0.88835509480 remains separately recorded, including $0.80 unresolved reservations.

No installations/pulls, real-repository changes, production service/config changes, credit purchases, account/privacy changes or public writes without specific approval. Do not loosen gates after observing paid results, normalize behavioral differences away, replace failed attempts or stop because one runtime appears ahead.

## Publication hold
The user explicitly deferred publication. Preserve:
`.orbi/benchmark-design/publication-draft/discussion-body.md`
SHA256: `c96af3c7a5ee5795e6bc8ead39c20fe3269e9300ea215373b8e29739e6ba4af3`.

Do not post the Discussion or modify the existing draft without approval. The pilot remains a feasibility/methodology study, not a general performance verdict. The eventual report must include it transparently, separate from the new dataset.
