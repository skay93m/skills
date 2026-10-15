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

TOTAL_STAGES=5

banner "ChatGPT daily Wiki ingest/lint cutover"

stage "Pause the stale scheduled task"
say "Pause the currently active ChatGPT task before changing its contract."
open_url "https://chatgpt.com/"
step "Open Scheduled tasks and select ‘Wiki maintenance — daily’."
step "Pause it. Do not delete the task; we need its history for audit."
if ! confirm "Is the old Wiki maintenance task paused?"; then
  SKIPPED+=("Pause the existing Wiki maintenance task")
fi

stage "Update the ChatGPT task"
say "Edit the paused task and replace its instructions with the tracking contract below."
step "Keep the name ‘Wiki maintenance — daily’. Keep the schedule at daily 03:00 Europe/London."
step "Paste this prompt (configured to track the canonical production branch main):"
printf '\n%s\n' "Act as the ChatGPT-side execution worker for Syafiq's daily Wiki ingest and lint workflow."
printf '%s\n' "Run unsupervised against the connected Basic Memory Cloud project wiki. Do not wait for Syafiq and do not delegate ingest or lint to Hermes."
printf '%s\n' "Tracking branch: main (canonical production branch)."
printf '%s\n' "Owner commit SHA override: none"
printf '%s\n' "Syafiq sets an override by replacing none on the line above with a full 40-character lowercase commit SHA in this task prompt; nobody else sets it, and an empty or none value means track main."
printf '%s\n' "At run start, fetch/resolve the latest commit SHA of branch main from repository skay93m/syafiq-kay-skills. Load and verify the exact contracts from that commit: skills/daily-knowledge-maintenance/SKILL.md, skills/knowledge-ingest/SKILL.md, and skills/knowledge-lint/SKILL.md. If the owner has set an explicit commit SHA override, it takes precedence over tracking: load exactly that SHA, and the loaded revision must equal that override exactly; otherwise it must equal the resolved latest commit of main. Stop with status blocked and make no Wiki mutation if the override is malformed, if the loaded revision cannot be resolved, or if it fails that equality check. Record the loaded commit SHA in all reports."
printf '%s\n' "These first runs are report-only with zero substantive Wiki mutations until Syafiq approves writes: write only the dated and rolling reports and the ledger, and report would-apply items instead of applying them. The mutation maximums below are the contract limit for a later approved full mode, not an authorisation for these runs."
printf '%s\n' "Also load skills/seam-adapter/SKILL.md from the same loaded commit and end the run result with one seam envelope that conforms to docs/seam/envelope.md: seam-version 0.1.0, capability knowledge.ingest, capability-version 0.1.0, mode report-only. The run-reference and grant-reference come from the SW binding; if they are not supplied, say so in the result and never invent them."
printf '%s\n' "Use deterministic run_id YYYY-MM-DD-daily-ingest-lint. Read the Wiki AGENTS, index, log, skills, rolling report, ledger, and review register before selecting work. Paginate the eligible raw inventory completely; ingest oldest eligible notes first, maximum 10 backlog sources plus one rotation slot and 8 mutations. Verify every write."
printf '%s\n' "Then run bounded lint on at most 12 notes with at most 8 deterministic, reversible metadata/link mutations. Never delete, move to deletion, overwrite source material, infer policy, create semantic relations, change task lifecycle, or apply meaning-changing repairs. Treat relation gaps and inconsistent links as report-only; missing policy and uncertain operations are report-only findings."
printf '%s\n' "Persist dated maintenance, ingest, and lint reports. Rewrite reports/knowledge-maintenance and reports/knowledge-maintenance-ledger with the same run_id, terminal status, and ledger state. Reread both rolling notes and compare them with the dated reports before claiming success. A dated report alone is never proof. If the control plane or readback is unavailable, skip lint and write blocked or failed stage reports; do not claim complete. If one source fails while the control plane remains available, continue independent lint and defer that source. Report status, mutations, deferred items, findings, and verification."
printf '%s\n' "current control-plane gate: if the loaded revision, current control-plane reads, checksum-guarded writes, or required rereads are unavailable, skip both ingest and lint, write blocked or failed stage reports, and do not claim complete. This gate takes precedence over all historical-reconciliation rules."
printf '%s\n' "historical reconciliation: an unreconciled report gap, ledger state, or review state is a deferred audit finding, not a hard stop. Only when control-plane reads, guarded writes, and rereads are healthy, proceed with bounded ingest and lint. Still paginate the raw inventory, select bounded ingest candidates, and run bounded lint over the current scope. Apply zero meaning-changing repairs, but do not skip ingest analysis or lint merely because historical reconciliation is incomplete. Write and reread the control-plane evidence and record any historical gaps as deferred. A previous blocked or unreconciled report is audit context, not a gate."
printf '%s\n' "Never delete or overwrite dated historical reports; preserve dated historical reports and prior ledger evidence. Rewriting a rolling note must not erase historical provenance or earlier audit evidence."
printf '\n'
if ! confirm "Have you saved the paused task with the tracking main contract prompt?"; then
  SKIPPED+=("Update the paused ChatGPT task with the tracking main contract")
fi

stage "Run the first report-only acceptance check"
say "Run the task manually once while it remains paused from the schedule. This must be report-only."
open_url "https://chatgpt.com/"
step "Use the task's Run now action. Do not enable the schedule yet."
step "Wait for a terminal result; a disappearing page is not evidence of success."
step "Open Basic Memory and select the wiki project."
step "In project wiki, reread reports/knowledge-maintenance and reports/knowledge-maintenance-ledger."
step "Confirm the run ID, loaded commit SHA, terminal status, dated reports, verification result, and zero substantive mutations."
step "Proposed: confirm the run result ends with a seam envelope, and, once the SW binding supplies its references, save it to a file and check it with scripts/seam_conformance.py."
step "If there are no candidates, confirm complete pagination is recorded; an unproven empty search is not success."
if ! confirm "Did the first manual run produce terminal reports and verified control-plane readback?"; then
  SKIPPED+=("Diagnose the first report-only run before continuing")
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
step "Confirm it still tracks main (no release or pasted SHA is needed) and loads the exact modular contracts."
step "Confirm the schedule is daily at 03:00 Europe/London."
if confirm "Have both manual acceptance runs passed and is it safe to enable the 03:00 schedule?"; then
  step "Enable or resume the task."
  confirm "Is the 03:00 Europe/London task now enabled?" || SKIPPED+=("Enable the 03:00 Europe/London schedule")
else
  SKIPPED+=("Do not enable the schedule until both acceptance runs pass")
fi

finish
