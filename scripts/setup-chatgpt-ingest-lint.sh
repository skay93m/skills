#!/usr/bin/env bash
#
# A wizard — walks a human through creating the ChatGPT-side daily Wiki
# ingest/lint tasks. The task itself performs the work; Hermes only coordinates.
#
# Everything above the "STAGES" marker is the wizard library: do not hand-edit
# it. Author the per-step stages below the marker.

set -euo pipefail

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  BOLD=$(tput bold); DIM=$(tput dim); RESET=$(tput sgr0)
  BLUE=$(tput setaf 4); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); RED=$(tput setaf 1)
else
  BOLD=""; DIM=""; RESET=""; BLUE=""; GREEN=""; YELLOW=""; RED=""
fi

TOTAL_STAGES=0
_STAGE_INDEX=0
SKIPPED=()

_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1; then tput clear; else printf '\033[2J\033[3J\033[H'; fi
}

banner() {
  _clear
  printf '\n%s%s  %s%s\n' "$BOLD" "$BLUE" "$1" "$RESET"
  printf '%s  %s stages%s\n\n' "$DIM" "$TOTAL_STAGES" "$RESET"
  printf '%s  You drive ChatGPT; this wizard gives you the exact task instructions.\n' "$DIM"
  printf '  Stop with Ctrl-C and re-run later if needed.%s\n' "$RESET"
  pause "Ready to start?"
}

stage() {
  _clear
  _STAGE_INDEX=$((_STAGE_INDEX + 1))
  printf '\n%s%s▸ Stage %s/%s · %s%s\n' \
    "$BOLD" "$BLUE" "$_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$RESET"
}

say()  { printf '  %s\n' "$1"; }
step() { printf '  %s•%s %s\n' "$BLUE" "$RESET" "$1"; }
note() { printf '  %s%s%s\n' "$DIM" "$1" "$RESET"; }
warn() { printf '  %s⚠ %s%s\n' "$YELLOW" "$1" "$RESET"; }

open_url() {
  local url="$1"
  printf '  %s↗ opening%s %s\n' "$GREEN" "$RESET" "$url"
  { if   command -v wslview >/dev/null 2>&1; then wslview "$url"
    elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$url"
    elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$url"
    elif command -v open >/dev/null 2>&1; then open "$url"
    else warn "couldn't open a browser — visit it manually: $url"; fi
  } >/dev/null 2>&1 || warn "couldn't open a browser — visit it manually: $url"
}

pause() {
  printf '  %s%s%s ' "$DIM" "${1:-Press Enter to continue}" "$RESET"
  read -r _ || true
}

confirm() {
  local reply=""
  printf '  %s? %s [y/N] ' "$YELLOW" "$1"
  read -r reply || true
  [[ "$reply" =~ ^[Yy] ]]
}

finish() {
  _clear
  printf '\n%s%s  ✓ Wizard complete%s\n' "$BOLD" "$GREEN" "$RESET"
  if (( ${#SKIPPED[@]} )); then
    printf '\n'; warn "still to do by hand:"
    for item in "${SKIPPED[@]}"; do note "  - $item"; done
  fi
  printf '\n'
}

# ──────────────────────────────────────────────────────────────────────────
# STAGES — author this section. One stage() per step the human takes.
# ──────────────────────────────────────────────────────────────────────────

TOTAL_STAGES=7

banner "ChatGPT daily Wiki ingest/lint cutover"

stage "Merge the release pull request"
say "The owner must merge the approved develop-to-main pull request before the release can be pinned."
open_url "https://github.com/skay93m/syafiq-kay-skills/pull/61"
step "Review the checks and merge PR #61 from develop into main."
step "After the merge completes, copy the full 40-character commit SHA at the top of main."
ask MERGE_SHA "Paste the merged main commit SHA:"
if [[ ! "$MERGE_SHA" =~ ^[0-9a-fA-F]{40}$ ]]; then
  warn "That is not a full 40-character commit SHA. The release cannot be verified yet."
  SKIPPED+=("Merge PR #61 and capture a full main commit SHA")
else
  note "Recorded the public main commit SHA for this cutover: $MERGE_SHA"
fi
pause "When the merge is visible on main, press Enter."

stage "Create the v0.1.0 release"
say "Create the first semantic release from the merged main commit."
open_url "https://github.com/skay93m/syafiq-kay-skills/releases/new"
step "Set the tag to v0.1.0 and target the merged main commit."
step "Publish the GitHub release with the generated release notes."
step "Copy the full commit SHA that the v0.1.0 tag points to."
ask RELEASE_SHA "Paste the full commit SHA behind v0.1.0:"
if [[ ! "$RELEASE_SHA" =~ ^[0-9a-fA-F]{40}$ ]]; then
  warn "That is not a full 40-character commit SHA. Do not continue to task cutover."
  SKIPPED+=("Create v0.1.0 and capture its full target SHA")
fi
pause "When the v0.1.0 release is published, press Enter."

stage "Pause the stale scheduled task"
say "Pause the currently active ChatGPT task before changing its contract."
open_url "https://chatgpt.com/"
step "Open Scheduled tasks and select ‘Wiki maintenance — daily’."
step "Pause it. Do not delete the task; we need its history for audit."
if ! confirm "Is the old Wiki maintenance task paused?"; then
  SKIPPED+=("Pause the existing Wiki maintenance task")
fi

stage "Update and pin the ChatGPT task"
say "Edit the paused task and replace its instructions with the pinned contract below."
step "Keep the name ‘Wiki maintenance — daily’. Keep the schedule at daily 03:00 Europe/London."
step "Paste this prompt, replacing the SHA placeholder with the full SHA you captured for v0.1.0:"
printf '\n%s\n' "Act as the ChatGPT-side execution worker for Syafiq's daily Wiki ingest and lint workflow."
printf '%s\n' "Run unsupervised against the connected Basic Memory Cloud project wiki. Do not wait for Syafiq and do not delegate ingest or lint to Hermes."
printf '%s\n' "Approved release commit SHA: ${RELEASE_SHA:-<PASTE-THE-FULL-V0.1.0-SHA>}"
printf '%s\n' "Load and verify the exact pinned contracts: skills/daily-knowledge-maintenance/SKILL.md, skills/knowledge-ingest/SKILL.md, and skills/knowledge-lint/SKILL.md. If the loaded revision does not exactly match the approved SHA, stop with status blocked and make no Wiki mutation."
printf '%s\n' "Use deterministic run_id YYYY-MM-DD-daily-ingest-lint. Read the Wiki AGENTS, index, log, skills, rolling report, ledger, and review register before selecting work. Paginate the eligible raw inventory completely; ingest oldest eligible notes first, maximum 10 backlog sources plus one rotation slot and 8 mutations. Verify every write."
printf '%s\n' "Then run bounded lint on at most 12 notes with at most 8 deterministic, reversible metadata/link mutations. Never delete, move to deletion, overwrite source material, infer policy, create semantic relations, change task lifecycle, or apply meaning-changing repairs. Treat relation gaps and inconsistent links as report-only; missing policy and uncertain operations are report-only findings."
printf '%s\n' "Persist dated maintenance, ingest, and lint reports. Rewrite reports/knowledge-maintenance and reports/knowledge-maintenance-ledger with the same run_id, terminal status, and ledger state. Reread both rolling notes and compare them with the dated reports before claiming success. A dated report alone is never proof. If the control plane or readback is unavailable, skip lint and write blocked or failed stage reports; do not claim complete. If one source fails while the control plane remains available, continue independent lint and defer that source. Report status, mutations, deferred items, findings, and verification."
printf '%s\n' "current control-plane gate: if the approved pin, current control-plane reads, checksum-guarded writes, or required rereads are unavailable, skip both ingest and lint, write blocked or failed stage reports, and do not claim complete. This gate takes precedence over all historical-reconciliation rules."
printf '%s\n' "historical reconciliation: an unreconciled report gap, ledger state, or review state is a read-only stop, not a hard blocked status. Only after the approved pin matches and current control-plane reads, guarded writes, and rereads are healthy, select read_only. For this case terminal status = read_only; Do not carry forward a previous blocked status from the ledger when current preflight is otherwise healthy. Still paginate the raw inventory, select bounded ingest candidates, analyse/process those candidates in read-only mode, run bounded lint over the current scope, and record would-apply changes and findings. Apply zero substantive note mutations, but do not skip ingest analysis or lint merely because historical reconciliation is incomplete. Write and reread the control-plane evidence and record the historical gap as deferred. A previous blocked or unreconciled report is audit context, not a gate."
printf '%s\n' "Never delete or overwrite dated historical reports; preserve dated historical reports and prior ledger evidence. Rewriting a rolling note must not erase historical provenance or the evidence for the earlier blocked run."
printf '\n'
if ! confirm "Have you saved the paused task with the exact v0.1.0 SHA and pinned contract prompt?"; then
  SKIPPED+=("Update the paused ChatGPT task with the full release SHA and exact contract")
fi

stage "Run the first report-only acceptance check"
say "Run the task manually once while it remains paused from the schedule. This must be report-only."
open_url "https://chatgpt.com/"
step "Use the task's Run now action. Do not enable the schedule yet."
step "Wait for a terminal result; a disappearing page is not evidence of success."
open_url "https://app.basicmemory.com/"
step "In project wiki, reread reports/knowledge-maintenance and reports/knowledge-maintenance-ledger."
step "Confirm the run ID, pinned SHA, terminal status, dated reports, verification result, and zero substantive mutations."
step "If there are no candidates, confirm complete pagination is recorded; an unproven empty search is not success."
if ! confirm "Did the first manual run produce terminal reports and verified control-plane readback?"; then
  SKIPPED+=("Diagnose the first pinned report-only run before continuing")
fi

stage "Run the idempotency acceptance check"
say "Run the same task a second time before scheduling it."
open_url "https://chatgpt.com/"
step "Use Run now again with the same saved task and effective Wiki state."
step "Verify that completed or unchanged work is skipped, findings are not duplicated, and deferred work remains durable."
step "Reread both rolling notes and the dated reports in project wiki."
if ! confirm "Did the second run prove idempotency and preserve any deferred work?"; then
  SKIPPED+=("Fix idempotency or durable-deferred-state evidence before enabling the schedule")
fi

stage "Re-enable the daily schedule"
say "Only enable the schedule after both manual acceptance checks pass."
open_url "https://chatgpt.com/"
step "Open the saved ‘Wiki maintenance — daily’ task."
step "Confirm it still uses the full v0.1.0 commit SHA and the exact modular contracts."
step "Confirm the schedule is daily at 03:00 Europe/London."
if confirm "Have both manual acceptance runs passed and is it safe to enable the 03:00 schedule?"; then
  step "Enable or resume the task."
  confirm "Is the 03:00 Europe/London task now enabled?" || SKIPPED+=("Enable the 03:00 Europe/London schedule")
else
  SKIPPED+=("Do not enable the schedule until both acceptance runs pass")
fi

finish
