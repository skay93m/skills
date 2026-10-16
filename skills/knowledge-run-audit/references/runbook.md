# Audit runbook (draft)

Run calls one at a time, never in parallel. Every `bm` call follows one wrapper:

```
timeout 90 bm <command> </dev/null > "$W/out.json" 2> "$W/err.txt"; echo "exit=$?"
```

- `$W` is an empty scratch directory the auditor creates outside the repository.
- Exit 0 is not success. Read the payload: a read of a missing note returns exit 0 with null fields; a write reports an `action`.
- Calls take roughly 6 to 45 seconds. On timeout or unclear failure, read back before doing anything else. Never blind retry. Retry a read at most once.
- Name the project on every call: `--project sk-wiki --cloud`. Never `--local`. Search is never proof of absence (index lag); use direct reads and listings.
- Do not invent flags. Anything marked [unverified] comes from a register or note, not a runtime check: run `bm <command> --help` first, adjust, and record the adjustment in the audit note.
- Tool split. The CLI is used for inventories and frontmatter reads. The Basic Memory MCP tools (`read_note`, `list_note_versions`, `write_note`, `recent_activity`) are used for checksums, version history and the audit write, because the CLI exposes no revision checksum and its exclusive-create is unverified.

Variables: `RUN` = run id; `START` = `start_time_utc` from the start marker; `DAY` = the UTC date of `START` as `YYYYMMDD`; `SNAP_NAME` = `auto-daily-auto-${DAY}-000000`.

## PLAN (read only)

P1. Read the start marker.
`bm tool read-note operations/${RUN}-start --project sk-wiki --cloud --include-frontmatter --json`
Expect: exit 0, `permalink` non-null, frontmatter with `run_id` equal to `RUN`, `start_time_utc`, `derived_snapshot_name`, `loaded_revision`, `approved_revision` (the SW spec calls this field `approved_skill_sha`). Null `permalink` means the marker is missing: set `record_set_complete=false`. Then the diff window cannot be fixed: the snapshot lookup in P4 is provisional (date taken from the run id) and V2 is "not verifiable".
Set `START` from the marker, then `DAY` from `START`, never from `RUN`. If the date in `RUN`, the date in `derived_snapshot_name` and the date of `START` differ, flag it.

P2. Read the run note.
`bm tool read-note operations/${RUN} --project sk-wiki --cloud --include-frontmatter --json`
Expect: non-null `permalink`, `status` in {completed, completed_with_deferred, blocked, failed, read_only}, a `notes_touched` manifest. Null fields mean a failed run (marker without run note): `record_set_complete=false`, record it, continue with an empty manifest.

P3. Confirm there is no audit note yet.
`bm tool read-note operations/${RUN}-audit --project sk-wiki --cloud --json`
Expect: exit 0 with null fields. A non-null `permalink` means stop and report.

P4. Find the snapshot. [unverified output shape]
`bm cloud snapshot list`
Expect: entries with an id (UUID) and a name or description. Select the entry named `SNAP_NAME`. Record `SNAP_ID` and the created time (about 02:46 UTC on `DAY`, and before `START`). If none matches: `snapshot_verified=false`, say so in the note, skip P5 and V2, and continue the other checks.
`bm cloud snapshot show ${SNAP_ID}` [unverified] confirms name and time.

P5. Take the snapshot inventory. [unverified flag]
`bm cloud snapshot browse ${SNAP_ID}` with the path or prefix flag. The CLI register gives `--path <dir>`; the behaviour note gives `--prefix`. Check `--help` and use the one that exists.
Expect: object paths and sizes only, no note bodies. Find the project's object prefix from the output; never assume it. Save as `SNAP_PATHS` (path, size).

P6. Take the current inventory, complete.
Prefer the MCP `list_directory` with project `sk-wiki`, depth recursive, paged until the reported total is reached. CLI alternatives [unverified]: `bm project ls --name sk-wiki --cloud`, or `bm ls <folder> --project sk-wiki --cloud --json` per folder (`bm tree` has no `--project` flag; do not use it for this project).
Incomplete pagination blocks the diff: record it. Save as `NOW_PATHS`.

P7. List notes modified after the start time.
MCP `recent_activity` with a timeframe covering `START`, or `bm tool recent-activity --type entity --timeframe 6h --project sk-wiki --cloud --json` [unverified timeframe format; `6h` is an example, round up to cover `START` and check `--help`]. Keep entries with an updated time after `START`. Save as `CHANGED`. This listing can lag; V2 does not rely on it alone.

PLAN passes when P1 to P3 are readable and either P4 to P7 succeeded or the missing part is recorded.

## VALIDATE (read only)

V1. Record set. `record_set_complete` is true only if the marker and run note both exist, `RUN` is consistent in titles, permalinks and `run_id`, and the audit note does not yet exist. When false, the final status is `flagged`.

V1b. Revision pin (unattended runs). Read `loaded_revision` and `approved_revision` from the start marker and the run note. Each must be a full 40-hex SHA and `loaded_revision` must equal `approved_revision`, in both notes. Mismatch or absence: `revision_pin_check=false`, flagged. Unreadable notes: `pending`. Do not infer a SHA from the run id or the repository.

V2. Independent diff versus the snapshot. Never trust the manifest for the list.
- Normalise identity first. Snapshot object paths and current Cloud file paths differ: Cloud can keep the title with spaces and capitals while the permalink is a slug. Make one key for both: drop the workspace and project prefix (strip any leading `<workspace>/` and `sk-wiki/` segments: older root notes such as index and log have permalinks without the workspace prefix, for example `sk-wiki/index`, while newer notes have it, so both forms must collapse to one key) and the `.md` suffix, lowercase, turn spaces and underscores into single hyphens. If two paths in one inventory collapse to one key, or a path appears only on one side but its key matches a path on the other side under a different spelling, do not call it a create or delete. Report `manifest_verified` as `pending` (not verifiable) and list the ambiguous pairs.
- Permalink form. Check that the manifest and `audit_result` permalinks use the form the tool returns for that note (read it with `read_note`), not a hand-built prefix. Set `permalink_form_check` false and list the rows otherwise. Normalisation is for comparing only; it does not excuse a wrong form.
- Limit: "modified = different size" misses edits that keep the size. State this under "Not verifiable" whenever a modification check relies on size alone.
- created = keys in `NOW_PATHS` not in `SNAP_PATHS`; deleted = keys in `SNAP_PATHS` not in `NOW_PATHS`; modified = same key with a different size.
- Window. Created and modified entries should also be in `CHANGED`. An entry that differs from the snapshot but is missing from `CHANGED` is not dropped: report it as a candidate (modification time unverified, possible index lag). Keep every deleted key.
- Compare with the manifest `notes_touched` by key and action. Report: in diff not in manifest (unmanifested), in manifest not in diff, and action mismatches. `manifest_verified` is true only if all lists are empty and nothing is pending. The start marker, run note and later audit note are expected creates.
- Checksums. Manifest checksums are the revision checksum the write returned. For each manifest row compare `after_checksum` with MCP `read_note` (`include_content=false`) `revision_checksum`. A difference is reported; an unreadable or differently formed value is "not verifiable", not a mismatch. A later legitimate edit also differs: say so.
- Before-content. Snapshot browse gives no bodies. Use MCP `list_note_versions` and `read_note` with a version dated before `START`, if one exists. If none, report "before-content not verifiable".

V3. Deletions. For each deleted key, check the manifest row and one allowlist rule:
- `duplicate`: body similarity at least 0.95, same source, canonical note exists and links; similarity score and before-checksum recorded. Recompute only if the before body is retrievable (V2).
- `scratch`: path under `scratch/` and absent from `SNAP_PATHS` (the run created it). A path in the snapshot is not run-created: flagged.
- `fixture`: snapshot size 0, or the before body is empty or has invalid frontmatter.
Any other deletion, or a missing row, rule or before-checksum, is flagged. The auditor never reverses a deletion.

V4. Content rules on each created or modified note in the diff (`bm tool read-note <permalink> --project sk-wiki --cloud --include-frontmatter --json`):
- No stored status or trust field in knowledge notes: keys such as `status`, `trust`, `unconfirmed`, `confirmed`, `confirmed_by`, `status_authority`. The operational `status` on `operations/` notes is allowed with the run-record vocabulary only.
- No trust-asserting wording (for example "verified", "trusted", "authoritative", "confirmed by") and no absolute wording (for example "always", "never", "proves", "definitely", "undeniably"). Pattern hits are candidates: quote the line, then judge whether it is attributed and hedged.
- Provenance: `authored_by`, `agent_model`, `run_id` present; `run_id` equals `RUN` for notes the run created. Compiled knowledge notes carry a provenance relation (`derived_from`).

V5. Scope. Collect the paths in the diff.
- `first-run-limited`: the only creates allowed are `operations/${RUN}-start` and `operations/${RUN}`. Any other created, modified or deleted path is out of scope, including index and log edits.
- `lifted`: allowed are `operations/`, `operations/issues/`, `scratch/`, compiled `knowledge/` and `source-notes/` notes, and guarded edits to index and log. Index rule: append-only except a guarded stale-index rewrite that keeps every still-valid entry. Log rule: append-only, one entry per run keyed by the run id. Anything else is out of scope. `schemas/` is never in scope.
- Changes made by someone else in the window (for example schema notes created at the same time) also show as out of scope or unmanifested; see V6.

V6. Authorship. Do not use `created_by`. A change in the window that is not in the manifest is "unmanifested, author unknown". It may be a human edit. Flag it for the owner without concluding who wrote it.

## EXECUTE

Duration. When the start marker and run note timestamps are both available, derive duration from `start_time_utc` and the run note's write time; the run may report none. If either is missing, write "not available".

E1. Build the note body in `$W/audit.md` from the template in `checks.md`. Include the snapshot id, the window (`START` to the audit time), what was not verifiable, and the flags. Use hedged wording.

E2. Exclusive-create the note with the MCP `write_note`: project `sk-wiki`, directory `operations`, title `${RUN}-audit`, `overwrite=false`, the frontmatter from the template. This was verified as an exclusive-create in the capability probe. The CLI `bm tool write-note` is not used unless `--help` shows that it refuses an existing note and keeps the frontmatter, and the owner approves a test. No such evidence exists for this draft.
Expect: action `created`. `NOTE_ALREADY_EXISTS` or any other action: stop, write nothing else, report.

E3. Read back once: MCP `read_note` for `operations/${RUN}-audit`. Expect non-null permalink and the frontmatter as written. If it is absent after a timeout, repeat E2 at most once, then stop and report.

E4. Reply with the status, the flagged and unverifiable checks, and the permalink. Change no other note.
