# Audit runbook (draft)

Every `bm` call below follows one wrapper. Run calls one at a time, never in parallel.

```
timeout 90 bm <command> </dev/null > "$W/out.json" 2> "$W/err.txt"; echo "exit=$?"
```

- `$W` is an empty scratch directory the auditor creates outside the repository.
- Exit 0 is not success. Read the payload: writes report `action` (`created`), reads of a missing note return exit 0 with null fields, deletes report `deleted`.
- Calls take roughly 6 to 45 seconds. On timeout or unclear failure, read back before doing anything else. Never blind retry. Retry a read at most once.
- Always pass `--project sk-wiki --cloud` on note commands. Never `--local`. Search is never proof of absence (index lag); use direct reads and listings.
- Commands marked [unverified] come from a documented but not runtime-checked source. Run `bm <command> --help` first and adjust flags without changing intent. Record any adjustment in the audit note.

Variables: `RUN` = run id; `DAY` = the run date as `YYYYMMDD`; `SNAP_NAME` = `auto-daily-auto-${DAY}-000000`.

## PLAN (read only)

P1. Read the start marker.
`bm tool read-note operations/${RUN}-start --project sk-wiki --cloud --json`
Expect: exit 0, `permalink` non-null, frontmatter holds `run_id` equal to `RUN`, `start_time_utc`, `derived_snapshot_name` equal to `SNAP_NAME`, `approved_skill_sha`. Null `permalink` means the marker is missing: record `record_set_complete=false`, continue.
Save `START` = `start_time_utc`. Save `content` and its sha256 (`sha256sum`) as the note checksum.

P2. Read the run note.
`bm tool read-note operations/${RUN} --project sk-wiki --cloud --json`
Expect: non-null `permalink`, `status` in {completed, completed_with_deferred, blocked, failed, read_only}, a `notes_touched` manifest. Null fields mean a failed run (marker without run note): record it and go on with an empty manifest.

P3. Confirm no audit note yet.
`bm tool read-note operations/${RUN}-audit --project sk-wiki --cloud --json`
Expect: exit 0 with null fields. A non-null `permalink` means stop and report.

P4. Find the snapshot. [unverified output shape]
`bm cloud snapshot list`
Expect: a table or list with an id (UUID) and a name or description. Select the entry whose name is `SNAP_NAME`. Record `SNAP_ID` and the created time. Expect about 02:46 UTC on `DAY`. If no entry matches: record `snapshot_verified=false`, state it in the note, skip P5 and the snapshot half of V2, and continue the other checks.
`bm cloud snapshot show ${SNAP_ID}` [unverified] to confirm the name and time.

P5. Take the snapshot inventory. [unverified flag name]
`bm cloud snapshot browse ${SNAP_ID}` and, after `--help`, with the verified path or prefix flag for the project's object prefix.
Expect: object paths and sizes only, no note bodies. Derive the project's prefix from the results, never assume it. Save the list as `SNAP_PATHS` (path, size).

P6. Take the current inventory.
`bm project ls --name sk-wiki --cloud` [unverified] or `bm tree . --depth 10 --project sk-wiki --cloud` (page with `--page`/`--page-size` until the total is reached).
Expect: every note path with a total count. Incomplete pagination blocks the diff: record it. Save as `NOW_PATHS`.

P7. List notes modified after the start time.
`bm tool recent-activity --type entity --timeframe <hours since START, rounded up> --project sk-wiki --cloud --json`
Expect: entities with updated times. Keep only those strictly after `START`. Save as `CHANGED`. Cross-check with `NOW_PATHS` minus `SNAP_PATHS` (creates).

PLAN passes when P1 to P3 are readable and either P4 to P7 succeeded or the missing part is recorded.

## VALIDATE (read only)

V1. Record set. `record_set_complete` is true only if the marker and run note exist, `RUN` is consistent in titles, permalinks and `run_id`, and the audit note does not yet exist.

V2. Independent diff versus snapshot. Compute from the inventories, without trusting the manifest:
- created = `NOW_PATHS` minus `SNAP_PATHS`;
- deleted = `SNAP_PATHS` minus `NOW_PATHS`;
- modified = same path, different size, or listed in `CHANGED` with a path present in both.
Limit created and modified to notes in `CHANGED`. Keep every deleted path.
Compare with the manifest `notes_touched` by permalink and action. Report: in diff but not manifest (unmanifested), in manifest but not diff, and action mismatches. `manifest_verified` is true only if both lists are empty. The run's own `-start`, run note and (later) the audit note are expected creates.
For each manifest row with a checksum, read the current note (`bm tool read-note <permalink> --project sk-wiki --cloud --json`) and compare the sha256 of `content` with `after_checksum`. A difference, or an unclear checksum algorithm, is reported as not verifiable rather than as a mismatch.
Before-content: snapshot browse gives no bodies. Use MCP `list_note_versions` and `read_note` with a `version` from before `START`, if a version exists. If none exists, report "before-content not verifiable".

V3. Deletions. For each deleted path, check the manifest row and one allowlist rule:
- `duplicate`: body similarity at least 0.95, same source, canonical note exists and links; similarity score and before-checksum recorded. Recompute the score only if the before body is retrievable (V2).
- `scratch`: path under `scratch/` and the path is absent from `SNAP_PATHS` (the run created it). A path present in the snapshot is not run-created: flagged.
- `fixture`: snapshot size 0, or before body empty or with invalid frontmatter.
Any other deletion, or a missing manifest row, rule or before-checksum, is flagged. Deletions are never reversed by the auditor.

V4. Content rules on every created or modified note in the diff (read each with `read-note --json`):
- No stored status or trust field in knowledge notes: frontmatter keys such as `status`, `trust`, `confidence_status`, `unconfirmed`, `confirmed`, `confirmed_by`, `status_authority`. The operational `status` on `operations/` notes is allowed only with the run-record vocabulary.
- No trust-asserting wording (for example "verified", "trusted", "authoritative", "confirmed by") and no absolute wording (for example "always", "never", "proves", "definitely", "undeniably", "all", "none" used as a claim). Pattern hits are candidates: quote the line, then judge whether the wording is attributed and hedged.
- Provenance: `authored_by`, `agent_model`, `run_id` present, and `run_id` equals `RUN` for notes the run created. Compiled knowledge notes carry a provenance relation (`derived_from`).

V5. Scope. Collect the paths in the diff.
- `first-run-limited`: the only creates allowed are `operations/${RUN}-start` and `operations/${RUN}`. Any other created, modified or deleted path is out of scope. Index and log edits are out of scope too unless the owner has said otherwise (see open question in the seam draft).
- `lifted`: allowed paths are `operations/`, `operations/issues/`, `scratch/`, compiled `knowledge/` and `source-notes/` notes, and guarded edits to index and log. Anything else is out of scope. Schema notes under `schemas/` are never in scope.

V6. Authorship. Do not use `created_by`. A change in the window that is not in the manifest is "unmanifested, author unknown". It may be a human edit. Flag it for the owner without concluding who wrote it.

## EXECUTE

E1. Build the note body in `$W/audit.md` using the template in `checks.md`. Include the snapshot id, the window (`START` to the time of the audit), what was not verifiable, and the flags. Use hedged wording.

E2. Exclusive-create the note. The command has no `--overwrite`.
`bm tool write-note --title "${RUN}-audit" --folder operations --content "$(cat "$W/audit.md")" --project sk-wiki --cloud --json`
Expect: `action` `created`. `NOTE_ALREADY_EXISTS` or any non-created action: stop, write nothing else, report.
If the CLI does not keep the frontmatter given in the content, report that in the reply; do not overwrite.

E3. Read back once.
`bm tool read-note operations/${RUN}-audit --project sk-wiki --cloud --json`
Expect: non-null `permalink`, frontmatter fields as written. If the read shows the note absent after a timeout, retry E2 at most once, then stop and report.

E4. Reply with the status, the flagged and unverifiable checks, and the permalink. Do not change any other note.
