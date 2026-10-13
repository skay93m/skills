#!/usr/bin/env python3
"""Deterministic decision core for the daily knowledge maintenance contract.

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

SHA_RE = re.compile(r"^[0-9a-f]{40}$")

# Operations a scheduled run may apply. Everything else becomes a review item.
SETTLED_OPS = {"provenance_record", "frontmatter_normalise", "link_normalise"}
HUMAN_GATED_OPS = {"task_lifecycle", "new_relation", "supersession", "schema_edit",
                   "delete", "control_plane_edit", "semantic_rewrite"}

# Basic Memory operations each guarantee depends on (verified 2026-10-13).
REQUIRED_CAPABILITIES = ("checksum_read", "guarded_overwrite", "exclusive_create",
                         "listing_total")


class Incomplete(Exception):
    """A paginated read did not prove it saw everything."""


class Conflict(Exception):
    """The target changed since it was read."""


def preflight(request, capabilities, state):
    """Return {"mode": blocked|read_only|full, "reasons": [...]}.

    blocked: no tool call at all. read_only: reads and reports, no mutation.
    """
    reasons = []
    approved, loaded = request.get("approved_commit_sha"), request.get("loaded_commit_sha")
    if not approved or not SHA_RE.match(str(approved)):
        return {"mode": "blocked", "reasons": ["approved_commit_sha missing or not a full SHA"]}
    if loaded != approved:
        return {"mode": "blocked", "reasons": ["loaded skills do not match approved_commit_sha"]}
    if request.get("wiki_project") != "wiki":
        return {"mode": "blocked", "reasons": ["wiki_project is not the canonical project"]}
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
    """Per-folder mode for the Friday pass. Absent or ambiguous policy: inspect only."""
    if not due:
        return {"status": "skipped", "folders": {}}
    plan = {}
    for folder in sorted(folders):
        p = policies.get(folder) or {}
        scope, repair = p.get("index_scope"), p.get("scheduled_repair")
        if scope not in ("exhaustive", "curated", "pointer") or repair not in ("allowed", "report-only"):
            plan[folder] = "inspect_only"
        elif scope == "exhaustive" and repair == "allowed":
            plan[folder] = "repair_allowed"
        else:
            plan[folder] = "check_only"
    return {"status": "due", "folders": plan}


def run(request, capabilities, state, sources, process, lint, store=None):
    """Plan and execute one bounded run against injected callables.

    process(source_id) and lint(note_ids) return {"mutations": [...], "findings": [...]}
    and may raise. An ingest failure never stops lint. In read_only mode neither
    callable may mutate: they are still called for evidence, and any mutation
    they return is discarded and reported.
    """
    pre = preflight(request, capabilities, state)
    result = {"mode": pre["mode"], "reasons": pre["reasons"], "run_id": request.get("run_id"),
              "completed": [], "failed": [], "deferred": [], "mutations": [],
              "findings": [], "discarded_mutations": 0, "cursor": state.get("cursor"),
              "ledger": dict(state.get("ledger", {}))}
    if pre["mode"] == "blocked":
        return result
    budget = request["budgets"]["sources"]
    selected, deferred, cursor = select_sources(
        sources, state.get("ledger", {}), state.get("cursor"), budget)
    result["deferred"], result["cursor"] = deferred, cursor
    checksums = {s["id"]: s["checksum"] for s in sources}
    touched = []
    for item in selected:
        try:
            out = process(item["id"])
        except Exception as exc:
            result["failed"].append({"id": item["id"], "error": str(exc)})
            continue
        if pre["mode"] == "read_only":
            result["discarded_mutations"] += len(out.get("mutations", []))
        else:
            result["mutations"].extend(out.get("mutations", []))
            result["ledger"][item["id"]] = checksums[item["id"]]
        result["findings"].extend(out.get("findings", []))
        result["completed"].append(item["id"])
        touched.append(item["id"])
    try:
        out = lint(touched)
        result["findings"].extend(out.get("findings", []))
        if pre["mode"] == "read_only":
            result["discarded_mutations"] += len(out.get("mutations", []))
        else:
            result["mutations"].extend(out.get("mutations", []))
    except Exception as exc:
        result["failed"].append({"id": "lint", "error": str(exc)})
    return result


if __name__ == "__main__":
    # Dry-run entry point: read a JSON snapshot, print the plan. Never writes.
    snap = json.load(open(sys.argv[1]))
    res = run(snap["request"], snap["capabilities"], snap["state"], snap["sources"],
              lambda i: {"mutations": [], "findings": []},
              lambda n: {"mutations": [], "findings": []})
    print(json.dumps(res, indent=2, sort_keys=True))
