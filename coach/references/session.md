---
name: coach-session
description: Reference workflow for starting, resuming, working through, and closing Apex Tier 1 Life OS sessions (life-coach) and Tier 2 Specialist Coach sessions with 2-call bootstrap, priority ladder, and Revision 3 hooks.
---

# Coaching Session Reference Workflow (`session.md`)

This workflow governs the full lifecycle of coaching sessions across Apex Tier 1 Life OS (`life-coach`) and Tier 2 specialist coaches (`study-coach`, `career-coach`, `finance-coach`).

---

## Section A: Apex Coach (`life-coach`) Session Workflow (Token-Effective State Machine)

### Step 1 — 2-Call Bootstrap (~500 tokens)
Upon invocation of `life-coach` (or synonyms `weekly sync`, `weekly align`, `mid-season`, `season transition`, `where are we?`), execute **exactly two read calls**:
1. `read_note(identifier="projects/life-compass/current-season", project="wiki")`
2. Superfocus MCP `get_me` (retrieves current local date/time in `Europe/London`, whether `Stack` is on, and projected `plannedFor` tasks).

#### Deterministic 4-Rule Priority Ladder
Evaluate the following rules in strict order:
- **Rule 1 (Season Transition)**: `today >= season_end` (or within 3 days of `season_end`) -> select **Season Transition**.
- **Rule 2 (Mid-Season Check)**: `today >= midpoint_date` AND `last_mid_season_check == null` (or interval elapsed) -> select **Mid-Season Check**.
- **Rule 3 (Weekly Alignment)**: `(today is Sunday AND last_weekly_align < today)` OR `(today - last_weekly_align >= 7 days)` -> select **Weekly Alignment**.
- **Rule 4 (Daily Sync / Triage)**: Otherwise -> select **Daily Sync & Thought Distillation (or Ad-Hoc Triage)**.

#### 5-Line Status & Confirmation Card
Render this card **before** loading any heavy logs:
```text
=== LIFE OS STATUS CARD ===
Where we are: [Season name, week number, active season theme]
Active Guardrails: [Top 2 active hard guardrails from current-season.md]
What's due today: [Priority ladder recommendation based on rules 1-4]
Next step: Reply "go" to run the due workflow, "daily" for a 2-minute thought dump, or "wait-what" for a 30-second Life OS refresher.
===========================
```

### Step 2 — Lazy-Loaded Workflow Execution
- **`wait-what`**: Render the 30-second `/wait-what` Life OS refresher from `current-season.md` (plus `docs/life-os/README.md` if on desktop).
- **Weekly Alignment**:
  1. Read past 7 days of Superfocus `Tasks`/`Blocks`/thoughts + read `handover/` and `plan/` across **every coach in `active_coaches`** (`study-coach`, `career-coach`, `finance-coach`, and any future `<domain>-coach`).
  2. Distil personal reflections into `wiki/journal/YYYY-MM-DD.md` (`bm_parse_semantics: false`) and raw ideas into `wiki/inbox/`.
  3. Run the **3-point Bigger-Picture Alignment Check**:
     - *1. Goal Drift vs. Season Manifesto*
     - *2. Cross-Coach Tension vs. Hard Guardrails*
     - *3. Next Week's 1–3 Superfocus Adjustments*
- **Mid-Season Check**: Audit all `active_coaches` plans/handovers against `gps-life-compass-and-3-year-sketch` and verify whether the Season Manifesto holds or needs a deliberate mid-season amendment.
- **Season Transition**: Run the end-of-season retrospective across all `active_coaches`, author the new Season Blueprint & Season Manifesto in `projects/life-compass/current-season`, and stage the new `Season` and `Goals` for Superfocus.
- **Daily Sync / Triage**: Distil today's Superfocus thoughts into `wiki/journal/YYYY-MM-DD.md` & `wiki/inbox/`, or coach uncoached domains (*Health*, *Family & Friends*, *Household*).

### Step 3 — Human-Approved Superfocus Write Gate
- Present proposed Superfocus items (`Task`, `Milestone`, `plannedFor`, `Block`, `Goal`) in chat first.
- Execute Superfocus MCP write calls **only after explicit user `"yes"`**, always reusing real IDs returned by Superfocus read calls.

### Step 4 — Close & State Timestamp Update
- Update `last_weekly_align`, `last_daily_sync`, or `last_mid_season_check` (and rolling snapshot) in `projects/life-compass/current-season` (`project="wiki"`).

---

## Section B: Specialist Coach (`<domain>-coach`) Session Workflow (Revision 3 Hooks)

### Step 1 — Bootstrap & Revision 3 Check
- Verify entry note and check `architecture_revision: 3`.

### Step 2 — Inbound Season Blueprint Hook
- Whenever a cross-domain trade-off, schedule change, or priority conflict arises, read `projects/life-compass/current-season` (`project="wiki"`) so advice respects the frozen Season Manifesto and Hard Guardrails.

### Step 3 — Close & Outbound Superfocus Hook
- Update `record/` and `handover/` (so `life-coach` reads it on Sunday).
- Propose concrete Superfocus `Tasks`/`Milestones`/`plannedFor` items and push via Superfocus MCP on user `"yes"`.
- **Coach-to-Life Nudge**: If `today - last_weekly_align > 8 days` in `current-season`, append a 1-line gentle nudge: *"Heads up: Your `life-coach` Weekly Alignment is overdue—type `life-coach` whenever you have 10 minutes."*

---

## Specialist Domain Methods (Study, Career, Finance)
- **`study-coach` (MSc & Network+ Study Coaching)**: Socratic, evidence-led study. Use independent attempt (20-30 mins journal diagnostic), one consequential Socratic question at a time, targeted scaffolding, revision and transfer, and mastery tracking.
- **`career-coach`**: Plan A / B / Z career trajectory exploration, risk appraisal, interview readiness, and professional milestone tracking.
- **`finance-coach`**: UK financial/HMRC tax guidance, Kakeibo budgeting, debt reduction strategies, and thinking-partner cash-flow guardrails.

---

## Section C: Sunday Coach Dispatcher & `[<domain>-coach]` Block-Tagging Pattern

To prevent calendar fragmentation while ensuring continuous oversight across all 4 specialist coaches (`study-coach`, `career-coach`, `finance-coach`, `coding-coach`), follow these execution rules:

1. **One Recurring Dispatcher Block**:
   - `life-coach` is the only recurring weekly calendar block on Sunday (`Sunday Weekly Alignment [life-coach]`, 20 minutes).

2. **Embedded Work Coaches (`[study-coach]` & `[coding-coach]`)**:
   - Never schedule separate meeting blocks for `study-coach` or `coding-coach`. Instead, embed them directly into existing deep-work blocks in Superfocus using bracketed tags:
     - `19:30–21:30: Network+ [study-coach] -> Fast.ai / Harness [coding-coach] (Hard Stop 21:30)`
     - `Off-Site Library Sprint: KCL MSc [study-coach]`

3. **Cadence / Trigger Coaches (`[finance-coach]` & `[career-coach]`)**:
   - At Step 3 of Sunday Weekly Alignment, `life-coach` inspects the upcoming Boots shift rota, payday calendar, and coach handovers.
   - `life-coach` dynamically proposes `plannedFor` Tasks or Blocks in Superfocus for `[finance-coach]` (e.g. Friday/Sunday 10-minute Kakeibo or Payday £10k gate check) and `[career-coach]` (e.g. bi-weekly Boots ops/risk/audit evidence capture or 80,000 Hours review).
