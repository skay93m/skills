# Workspace Detection Matrix

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This reference provides rapid workspace detection heuristics, architecture invariants, operational roles, and governance rules across all 8 active repositories in the personal engineering ecosystem.

---

## 1. `skills` (Agent Skills & Standards Catalog)

- **Primary Role**: Golden repository for autonomous and interactive agent skills, deep modules, declarative manifests, deterministic verification scripts, and architectural standards.
- **Root Detection Indicators**:
  - Top-level `skills/` directory containing skill packages (`SKILL.md`, `references/`, `scripts/`, `templates/`, `examples/`).
  - Presence of `docs/standards/` (e.g. `skill-manifest.md`, `pr-review-standard.md`, `automated-checks.md`).
  - Scaffolding and verification scripts in `scripts/` (e.g. `scripts/new-skill.py`, `scripts/check-standard.py`).
  - Root `AGENTS.md` and `docs/agents/coordinator-protocol.md`.
- **Operational Invariants**:
  - Every skill entrypoint `SKILL.md` must adhere strictly to line budgets (<= 100 lines) and token budgets (< 700 tokens).
  - Terminal reference rule (Standard S5): references must not link to other markdown documents.
  - Manifest-first development: every skill must be governed by a declarative manifest with full provenance.
- **Typical Workflows**:
  - Run `python3 scripts/check-standard.py` to evaluate structural and security compliance.
  - Run `pytest` to execute regression suites and contract tests.
  - Scaffold new deep modules using `python3 scripts/new-skill.py --manifest <manifest-file>`.

---

## 2. `sk-wiki` (Compiled Persistent Knowledge Base)

- **Primary Role**: Central persistent knowledge base and personal wiki operating on the Karpathy-style compiled knowledge pattern and Basic Memory backend.
- **Root Detection Indicators**:
  - Directory structures containing `raw/` notes, compiled outputs, and topic folders.
  - Root documentation including `AGENTS.md`, `log.md`, and `index.md`.
  - Folder-level contract files: each root folder maintains an `index.md` (`type: index`, `bm_parse_semantics: false`) and `log.md` (`type: log`, `bm_parse_semantics: false`).
- **Operational Invariants**:
  - Strict lowercase kebab-case naming for all files and directories (exempt: `AGENTS.md`, `index.md`, `log.md`).
  - Zero direct shell mutations: all note operations must use Basic Memory tools (`read_note`, `write_note`, `edit_note`, `move_note`, `delete_note`). Direct filesystem writes via shell redirection or generic edit tools are prohibited.
  - Handoff reporting: persist complete session logs and findings under `handoff/<slug>.md`.
- **Typical Workflows**:
  - Supervised and unsupervised raw note ingestion.
  - Semantic and structural linting passes.
  - Index and log reconciliation for compilation passes.

---

## 3. `awt` (Agent Work Tracker)

- **Primary Role**: Standalone agile engine, sprint governance, issue lifecycle management, and SQLite-backed task state tracking.
- **Root Detection Indicators**:
  - Database file `awt.db` or SQLite state schemas (`schema.sql`).
  - Directory hierarchies including `sprints/`, `issues/`, `backlog/`.
  - The `awt` CLI utility and associated tooling.
- **Operational Invariants**:
  - Strict separation of Product Owner (PO) and Developer concerns: agents acting as developers do not mutate acceptance criteria or close issues without verification.
  - Event 0 sprint boundary verification: sprint gates must be formally satisfied before implementation work starts.
  - Atomic ticket progression: issues move linearly through defined statuses (`TODO` -> `IN_PROGRESS` -> `REVIEW` -> `DONE`).
- **Typical Workflows**:
  - Sprint capacity planning and backlog triage.
  - Work item assignment and timeboxing.
  - Milestone verification and sprint burndown tracking.

---

## 4. `kos` (Kernel Operating System & Daemon Services)

- **Primary Role**: Core host operating system integration layer, background daemon supervisors, systemd units, and long-running agent environments.
- **Root Detection Indicators**:
  - Daemon configuration files (`kos.conf`, `daemon.json`).
  - Directories such as `daemons/`, `kernel/`, `systemd/`, `services/`.
  - Background process managers and supervisor hooks.
- **Operational Invariants**:
  - Process isolation and safe daemon lifecycle management (start, stop, reload, status).
  - Unattended execution safety: daemons must not execute unverified remote code or expose unprotected network sockets.
  - Health checks and failure restart policies must be declared for all resident services.
- **Typical Workflows**:
  - Host telemetry collection and resource limit enforcement.
  - Background task scheduling and lifecycle monitoring.
  - Daemon configuration deployments and smoke testing.

---

## 5. `syafiq-kay.github.io` (Public Portfolio & Digital Garden)

- **Primary Role**: Public-facing web presence, technical portfolio, essays, long-form articles, and published digital garden.
- **Root Detection Indicators**:
  - Static site generator structures (`_posts/`, `_layouts/`, `_includes/`, `assets/`, `index.html`).
  - Web site configuration (`_config.yml` or static bundle generators).
  - Markdown-based blog posts and essays in chronological or category trees.
- **Operational Invariants**:
  - Public privacy hygiene: zero private paths, confidential notes, unpublished project records, or credentials.
  - Semantic HTML and accessibility standards conformance.
  - Static build verification before push to deployment branches.
- **Typical Workflows**:
  - Drafting and refining public essays and technical write-ups.
  - Local preview generation using static site development servers.
  - Portfolio project showcases and layout styling.

---

## 6. `neko` (Desktop Companion Daemon & Mood Telemetry)

- **Primary Role**: Desktop companion daemon providing ambient status, mood tracking, presence telemetry, and developer ergonomics.
- **Root Detection Indicators**:
  - Project directory `neko/` with `daemon.py`, `mood.json`, `telemetry/`.
  - Local desktop status loops, sprite assets, or system tray hooks.
- **Operational Invariants**:
  - Low resource consumption: daemon must maintain minimal CPU and memory footprints.
  - Non-intrusive notification semantics: telemetry should inform without disrupting active developer focus.
  - Deterministic state persistence for operator presence and focus cycles.
- **Typical Workflows**:
  - Logging focus session durations and break nudges.
  - Updating operator mood and energy state indicators.
  - Emitting ergonomic reminders based on active system telemetry.

---

## 7. `hermes` (Daily Coordination Agent & Standup Summaries)

- **Primary Role**: Daily executive coordination agent responsible for morning briefs, evening reconciliations, cross-repository standup summaries, and urgent notification routing.
- **Root Detection Indicators**:
  - Codebase structures under `hermes/`, `standups/`, `notifications/`, `bot.py`.
  - Scheduled cron triggers and communication integrations.
- **Operational Invariants**:
  - Signal-to-noise ratio: standups must be structured, succinct, and actionable.
  - Timely delivery: morning briefs and evening pulls execute strictly against schedule windows.
  - Cross-repo state aggregation: synthesizes pull requests, sprint items, and knowledge updates across the ecosystem.
- **Typical Workflows**:
  - Generating morning kickoff briefs with prioritized daily agenda items.
  - Compiling evening retrospectives and capturing unfinished work.
  - Dispatching high-priority alerts to operator notification channels.

---

## 8. `archive` (Historical Cold Storage & Deprecated Records)

- **Primary Role**: Historical preservation layer for retired codebases, frozen project snapshots, completed course records, and deprecated data.
- **Root Detection Indicators**:
  - Directory markers `archive/`, `cold-storage/`, `manifest.json`.
  - Read-only repository configurations and freeze stamps.
- **Operational Invariants**:
  - Immutability: archives are strictly read-only cold storage; no active development or feature mutation is permitted.
  - Preservation integrity: records must retain original commit metadata, dates, and historical licenses.
  - Searchability: manifests and indexes must describe frozen contents for retrospective research.
- **Typical Workflows**:
  - Historical reference lookups and precedent searches.
  - One-time extraction of legacy patterns for active migration.
  - Ingestion of completed project milestones into cold storage.
