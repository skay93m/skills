#!/usr/bin/env python3
"""Deterministic decision core for the daily knowledge maintenance contract.

Status 2026-10-16: the guarded-unattended helpers (derived_snapshot_name,
clock_ok, change_key, deletion_allowed, write_allowed, failed_runs) follow the
current skills. preflight(), the km-state ledger, render_report and
HUMAN_GATED_OPS are the earlier report-only/ledger model, kept for its tests and
superseded by the operations/ run records; the skills no longer use them.

The skills in skills/daily-knowledge-maintenance, knowledge-ingest and
knowledge-lint are prose. This module is the executable reference for their
settled rules, so the rules can be tested without a model or a live Wiki. It
never talks to Basic Memory: callers pass snapshots and a store adapter.

Python standard library only.
"""
import hashlib
import json
import re
import sys

SHA_RE = re.compile(r"[0-9a-f]{40}")

# Operations a scheduled run may apply. Everything else becomes a review item.
SETTLED_OPS = {"provenance_record", "frontmatter_normalise", "link_normalise"}
HUMAN_GATED_OPS = {"task_lifecycle", "new_relation", "supersession", "schema_edit",
                   "delete", "control_plane_edit", "semantic_rewrite"}

# Basic Memory operations each guarantee depends on (verified 2026-10-13).
REQUIRED_CAPABILITIES = ("checksum_read", "guarded_overwrite", "exclusive_create",
                         "listing_total")


DELETE_RULES = ("duplicate", "scratch", "fixture")
SIMILARITY_MIN = 0.95  # proposal measure for the duplicate rule
TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?$")
WORKSPACE_PREFIX = re.compile(r"^[^/]+/sk-wiki/")
# Folders a later (not first-run-limited) run may write besides its own records.
WRITE_FOLDERS = ("operations/issues/", "knowledge/", "source-notes/", "scratch/")
INDEX_NOTES = ("index", "knowledge/index", "source-notes/index", "operations/issues/index")
LOG_NOTES = ("log",)
DELETE_FOLDERS = ("knowledge/", "source-notes/", "scratch/")


def derived_snapshot_name(utc_date):
    """auto-daily-auto-YYYYMMDD-000000 from a UTC date string YYYY-MM-DD."""
    return "auto-daily-auto-%s-000000" % utc_date.replace("-", "")


def clock_ok(utc_time):
    """True only for a well-formed HH:MM[:SS] UTC time at or after 03:15:00.
    Malformed input is False, so the run aborts without writing."""
    m = TIME_RE.match(utc_time) if isinstance(utc_time, str) else None
    if not m:
        return False
    h, mi, sec = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    return (h, mi, sec) >= (3, 15, 0)


def change_key(drive_file_id, size, modified_time, checksum=None):
    return [drive_file_id, size, modified_time] + ([checksum] if checksum else [])


def _strip_workspace(path):
    return WORKSPACE_PREFIX.sub("", path or "")


def deletion_allowed(entry, run_created=(), first_run_limit=None):
    """Allowlisted deletion only. Refused under the first-run limit (absent flag
    counts as true). The path (workspace prefix stripped) must be in knowledge/,
    source-notes/ or scratch/ of sk-wiki, so operations/, schemas/, index, log and
    other projects are never deletable. Also required: rule, before checksum, a
    computed numeric similarity >= 0.95 for duplicates, a same-run scratch/ note
    for scratch, and for fixture an empty body with zero size or unparseable
    frontmatter (explicit inputs body_chars, size, frontmatter_parses)."""
    if first_run_limit is not False:
        return False
    rule = entry.get("allowlist_rule")
    path = _strip_workspace(entry.get("permalink"))
    if rule not in DELETE_RULES or not path or not entry.get("before_checksum"):
        return False
    if ".." in path.split("/") or not path.startswith(DELETE_FOLDERS):
        return False
    if rule == "duplicate":
        score = entry.get("similarity_score")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            return False
        return SIMILARITY_MIN <= score <= 1
    if "similarity_score" in entry:
        return False
    if rule == "scratch":
        return path.startswith("scratch/") and path in {_strip_workspace(p) for p in run_created}
    body, size, parses = entry.get("body_chars"), entry.get("size"), entry.get("frontmatter_parses")
    if isinstance(body, bool) or not isinstance(body, int) or body != 0:
        return False
    zero_byte = isinstance(size, int) and not isinstance(size, bool) and size == 0
    return zero_byte or parses is False


def write_allowed(path, first_run_limit, run_id):
    """First-run limit (also the default when the flag is absent): only the run's
    start and run notes. Otherwise: this run's own start/run notes, the folder
    allowlist, the named index notes and the root log. Never -audit, other runs'
    records, schemas/ or any other path."""
    path = _strip_workspace(path)
    own = ("operations/%s-start" % run_id, "operations/%s" % run_id)
    if first_run_limit is not False:
        return path in own
    if ".." in path.split("/"):
        return False
    return path in own or path.startswith(WRITE_FOLDERS) or path in INDEX_NOTES or path in LOG_NOTES


def failed_runs(listing):
    """Run IDs that have a -start note but no run note."""
    names = set(listing)
    return sorted(n[:-6] for n in names if n.endswith("-start") and n[:-6] not in names)


class Incomplete(Exception):
    """A paginated read did not prove it saw everything."""


class Conflict(Exception):
    """The target changed since it was read."""


def revision_ok(loaded, approved, supervised=False):
    """supervised is honoured only when it is the boolean True (strict).

    Assert loaded_revision == approved_revision before any write.

    Both must be full lowercase 40-hex SHAs. A supervised run may record
    approved as None/"none" (loaded must still be a full SHA); an unattended
    run requires an approved SHA that equals loaded. Any other input is False.
    """
    if not isinstance(loaded, str) or not SHA_RE.fullmatch(loaded):
        return False
    if supervised is True and (approved is None or approved == "none"):
        return True
    if not isinstance(approved, str) or not SHA_RE.fullmatch(approved):
        return False
    return loaded == approved


def preflight(request, capabilities, state):
    """Return {"mode": blocked|read_only|full, "reasons": [...]}.

    blocked: no tool call at all. read_only: reads and reports, no mutation.
    """
    reasons = []
    approved = request.get("approved_revision") or request.get("approved_commit_sha")
    loaded = request.get("loaded_revision") or request.get("loaded_commit_sha")
    # Explicit launcher parameter. Only the boolean True is supervised; absent,
    # "true", 1 or any other value is unattended (fail closed). A tracking branch
    # implies nothing.
    supervised = request.get("supervised") is True
    if not revision_ok(loaded, approved, supervised):
        if not loaded or not SHA_RE.fullmatch(str(loaded)):
            why = "loaded_revision missing or not a full SHA"
        elif not approved or not SHA_RE.fullmatch(str(approved)):
            why = "approved_revision (approved_commit_sha override) missing or not a full SHA (required for unattended runs)"
        else:
            why = "loaded_revision does not match approved_revision (approved_commit_sha override)"
        return {"mode": "blocked", "reasons": [why]}
    if request.get("wiki_project") != "sk-wiki":
        return {"mode": "blocked", "reasons": ["wiki_project is not the canonical project (sk-wiki)"]}
    for cap in REQUIRED_CAPABILITIES:
        if not capabilities.get(cap):
            reasons.append("missing capability: " + cap)
    if not state.get("report_note"):
        reasons.append("rolling report note not designated")
    if not state.get("review_register"):
        reasons.append("review register not designated")
    if not state.get("ledger_note"):
        reasons.append("checksum ledger not designated")
    if not state.get("history_reconciled"):
        reasons.append("historical ledgers/reports not reconciled")
    return {"mode": "read_only" if reasons else "full", "reasons": reasons}


def read_all(fetch_page):
    """Collect every item from fetch_page(n) -> {items, total, has_more}.

    Fails closed unless the final page says has_more is false and the count
    matches the reported total, so a truncated listing cannot read as empty.
    """
    items, page = [], 1
    while True:
        res = fetch_page(page)
        items.extend(res["items"])
        if not res.get("has_more"):
            break
        if not res["items"]:
            raise Incomplete("empty page while has_more is true")
        page += 1
    total = res.get("total")
    if total is not None and total != len(items):
        raise Incomplete("read %d of %s items" % (len(items), total))
    return items


def select_sources(sources, ledger, cursor, budget):
    """Pick backlog first, always reserving one rotating historical slot.

    sources: [{id, checksum, created}], ledger: {id: checksum}.
    Returns (selected, deferred_ids, new_cursor).
    """
    backlog = sorted((s for s in sources if ledger.get(s["id"]) != s["checksum"]),
                     key=lambda s: (s.get("created", ""), s["id"]))
    unchanged = sorted((s["id"] for s in sources if ledger.get(s["id"]) == s["checksum"]))
    rotate = None
    if unchanged and budget >= 2:
        after = [i for i in unchanged if cursor is None or i > cursor]
        rotate = (after or unchanged)[0]
    take = backlog[:budget - (1 if rotate else 0)] if budget else []
    selected = [{"id": s["id"], "reason": "new" if s["id"] not in ledger else "changed"}
                for s in take]
    if rotate:
        selected.append({"id": rotate, "reason": "historical_rotation"})
    deferred = [s["id"] for s in backlog[len(take):]]
    return selected, deferred, (rotate if rotate else cursor)


def classify(proposal):
    """apply only for settled reversible ops; else review. Unknown ops are review."""
    op = proposal.get("op")
    if op in SETTLED_OPS and proposal.get("reversible") and not proposal.get("semantic"):
        return "apply"
    return "review"


def finding_id(kind, notes, check):
    key = json.dumps([kind, sorted(notes), check], separators=(",", ":"))
    return "KM-" + hashlib.sha256(key.encode()).hexdigest()[:12]


def merge_findings(register, findings):
    """Add findings to the register by stable id; an existing id is never duplicated
    and an existing human status or response is never overwritten."""
    merged = {r["id"]: r for r in register}
    added = []
    for f in findings:
        fid = finding_id(f["kind"], f["notes"], f["check"])
        if fid not in merged:
            merged[fid] = dict(f, id=fid, status="awaiting-response", response="")
            added.append(fid)
    return sorted(merged.values(), key=lambda r: r["id"]), added


def guarded_write(store, path, new_content):
    """Checksum-guarded single write with verify. Returns an outcome dict.

    outcomes: written, already_applied, conflict, failed. Never retries blindly:
    after an error the persisted state is read before deciding anything.
    """
    before = store.read(path)
    if before["content"] == new_content:
        return {"outcome": "already_applied", "path": path}
    try:
        store.write(path, new_content, expected_checksum=before["checksum"])
    except Conflict:
        return {"outcome": "conflict", "path": path}
    except Exception:  # uncertain response: inspect, do not repeat the write
        after = store.read(path)
        if after["content"] == new_content:
            return {"outcome": "written", "path": path, "before": before["checksum"],
                    "after": after["checksum"], "note": "verified after uncertain response"}
        return {"outcome": "failed", "path": path}
    after = store.read(path)
    if after["content"] != new_content:
        return {"outcome": "failed", "path": path}
    return {"outcome": "written", "path": path, "before": before["checksum"],
            "after": after["checksum"]}


def index_drift_plan(folders, policies, due):
    """Per-folder mode for the Friday pass.

    A folder with an absent or ambiguous policy, or no index note, is treated as
    curated/report-only (dead-link checks only, no repair) and listed in
    `unpoliced` so a review finding is logged. No policy is ever inferred.
    """
    if not due:
        return {"status": "skipped", "folders": {}, "unpoliced": []}
    plan, unpoliced = {}, []
    for folder in sorted(folders):
        p = policies.get(folder) or {}
        scope, repair = p.get("index_scope"), p.get("scheduled_repair")
        if scope not in ("exhaustive", "curated", "pointer") or repair not in ("allowed", "report-only"):
            plan[folder] = "check_only"
            unpoliced.append(folder)
        elif scope == "exhaustive" and repair == "allowed":
            plan[folder] = "repair_allowed"
        else:
            plan[folder] = "check_only"
    return {"status": "due", "folders": plan, "unpoliced": unpoliced}


STATE_FENCE = re.compile(r"```km-state\n(.*?)\n```", re.S)


def dump_state(state):
    """Render the durable checkpoint as ordinary Markdown for the ledger note."""
    keep = {k: state.get(k) for k in ("run_id", "ledger", "cursor", "deferred", "lint_queue", "done")}
    return "```km-state\n" + json.dumps(keep, sort_keys=True, indent=1) + "\n```\n"


def load_state(text):
    """Parse a ledger note. Anything unparseable fails closed (raises ValueError)."""
    m = STATE_FENCE.search(text or "")
    if not m:
        raise ValueError("no km-state block")
    data = json.loads(m.group(1))
    if not isinstance(data.get("ledger"), dict):
        raise ValueError("ledger missing")
    return data


def render_report(result):
    """One rolling operational report body: ordinary Markdown, one line per item."""
    lines = ["# Daily knowledge maintenance", "",
             "Run: %s. Mode: %s. Revision: %s." % (result["run_id"], result["mode"], result.get("revision"))]
    for key in ("reasons", "limitations"):
        lines += ["Blocked: " + r if key == "reasons" else "Limitation: " + r for r in result[key]]
    for label, key in (("Completed", "completed"), ("Deferred", "deferred"), ("Would apply", "would_apply")):
        lines += ["%s: %s" % (label, x if isinstance(x, str) else x["path"]) for x in result[key]]
    lines += ["Failed: %s (%s)" % (f["id"], f["error"]) for f in result["failed"]]
    lines += ["Blocked item: %s" % b for b in result["blocked_items"]]
    lines += ["Mutation: %(path)s %(before)s -> %(after)s" % m for m in result["mutations"]]
    lines += ["Review: " + f for f in result["review_ids"]]
    lines.append("Lint index drift: " + result["index_drift"]["status"])
    lines += ["Index folder: %s %s" % kv for kv in result["index_drift"]["folders"].items()]
    lines += ["Review: no index policy for " + f for f in result["index_drift"]["unpoliced"]]
    return "\n".join(lines) + "\n"


def _apply(store, proposals, mode, budget_left, result, item_id):
    """Apply classified proposals. Returns True when the item may be ledgered."""
    ok = True
    for pr in proposals:
        if classify(pr) == "review":
            result["findings"].append({"kind": "proposal:" + str(pr.get("op")),
                                       "notes": [pr.get("path", item_id)],
                                       "check": pr.get("reason", "")})
            continue
        if mode != "full":
            result["would_apply"].append({"path": pr["path"], "op": pr["op"]})
        elif budget_left["mutations"] <= 0:
            result["deferred"].append(item_id)
            ok = False
        else:
            out = guarded_write(store, pr["path"], pr["content"])
            if out["outcome"] == "written":
                budget_left["mutations"] -= 1
                result["mutations"].append(out)
            elif out["outcome"] == "conflict":
                result["blocked_items"].append(item_id)
                ok = False
            elif out["outcome"] == "failed":
                result["failed"].append({"id": item_id, "error": "write not verified"})
                ok = False
    return ok


def run(request, capabilities, state, sources, process, lint, store=None,
        checkpoint=None, index=None):
    """One bounded, resumable run against injected callables.

    process(source_id) -> {"proposals": [...], "findings": [...]}; may raise.
    lint(note_ids) -> same shape; may raise. A failed or conflicting ingest item
    never stops lint or other items. checkpoint(state) is called after every
    item so a crash resumes from the last completed item. In read_only mode the
    store is never written; apply-class proposals are listed as would_apply.
    """
    pre = preflight(request, capabilities, state)
    loaded = request.get("loaded_revision") or request.get("loaded_commit_sha")
    result = {"mode": pre["mode"], "reasons": pre["reasons"], "run_id": request.get("run_id"),
              "revision": loaded if isinstance(loaded, str) and SHA_RE.fullmatch(loaded) else None,
              "completed": [], "failed": [],
              "deferred": [], "blocked_items": [], "mutations": [], "would_apply": [],
              "findings": [], "limitations": [], "review_ids": [],
              "cursor": state.get("cursor"), "ledger": dict(state.get("ledger", {})),
              "index_drift": index_drift_plan(*(index or ([], {}, False))),
              "lint_queue": list(state.get("lint_queue", []))}
    if pre["mode"] == "blocked":
        return result
    if not capabilities.get("drive_read"):
        result["limitations"].append("Drive access unavailable; no external source scan or capture")
    b = request["budgets"]
    left = {"mutations": b.get("mutations", 8)}
    resumed = state.get("run_id") == request.get("run_id")
    done = set(state.get("done", [])) if resumed else set()
    selected, deferred, _ = select_sources(
        [s for s in sources if s["id"] not in done], result["ledger"], state.get("cursor"), b["sources"])
    result["deferred"] = list(deferred)
    checksums = {s["id"]: s["checksum"] for s in sources}
    touched = []

    def save():
        if checkpoint and pre["mode"] == "full":
            checkpoint({"run_id": result["run_id"], "ledger": result["ledger"],
                        "cursor": result["cursor"], "deferred": result["deferred"],
                        "lint_queue": result["lint_queue"], "done": sorted(done)})

    for item in selected:
        sid = item["id"]
        try:
            out = process(sid)
        except Exception as exc:
            result["failed"].append({"id": sid, "error": str(exc)})
            continue
        result["findings"].extend(out.get("findings", []))
        if _apply(store, out.get("proposals", []), pre["mode"], left, result, sid):
            if pre["mode"] == "full":
                result["ledger"][sid] = checksums[sid]
            if item["reason"] == "historical_rotation" and pre["mode"] == "full":
                result["cursor"] = sid
            done.add(sid)
            result["completed"].append(sid)
            touched.append(sid)
        save()
    # lint: touched notes first, then oldest queued concerns, hard cap on unique notes
    cap, extra = b.get("lint_notes", 12), b.get("lint_extra", 5)
    scope = list(dict.fromkeys(touched + result["lint_queue"][:extra]))[:cap]
    try:
        out = lint(scope)
        result["findings"].extend(out.get("findings", []))
        _apply(store, out.get("proposals", []), pre["mode"], left, result, "lint")
        result["lint_queue"] = [n for n in result["lint_queue"] if n not in scope]
    except Exception as exc:
        result["failed"].append({"id": "lint", "error": str(exc)})
    result["lint_scope"] = scope
    for f in result["index_drift"]["unpoliced"]:
        result["findings"].append({"kind": "missing_index_policy", "notes": [f],
                                   "check": "index_scope/scheduled_repair absent; treated as curated/report-only"})
    result["findings"], result["review_ids"] = _dedupe(result["findings"])
    save()
    return result


def _dedupe(findings):
    seen, out, ids = set(), [], []
    for f in findings:
        fid = finding_id(f["kind"], f["notes"], f["check"])
        if fid not in seen:
            seen.add(fid)
            out.append(dict(f, id=fid))
            ids.append(fid)
    return out, ids


if __name__ == "__main__":
    # Dry-run entry point: read a JSON snapshot, print the plan and report. Never writes.
    snap = json.load(open(sys.argv[1]))
    plans = snap.get("proposals", {})
    res = run(snap["request"], snap["capabilities"], snap["state"], snap["sources"],
              lambda i: {"proposals": plans.get(i, []), "findings": []},
              lambda n: {"proposals": [], "findings": snap.get("lint_findings", [])},
              index=(snap.get("folders", []), snap.get("policies", {}), snap.get("index_drift_due", False)))
    print(render_report(res))
    print(json.dumps({k: res[k] for k in ("mode", "completed", "deferred", "would_apply",
                                          "lint_scope", "review_ids", "cursor")}, sort_keys=True))
