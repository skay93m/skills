#!/usr/bin/env python3
"""Seam conformance check (draft, seam 0.1.0). Python standard library only.

Input: a synthetic envelope, a capability profile and a grant set. Output: pass
or fail with a closed error-category. No backend is contacted; the "abstract
backend" is whatever produced the envelope. Nothing private is read or printed.

Usage: seam_conformance.py --envelope E.json --profile P.json --grants G.json
Exit status: 0 on pass, 1 on fail, 2 on unreadable input.
"""
import argparse
import json
import re
import sys

STATUS = ("succeeded", "partial", "failed", "refused")
DISPOSITION = ("reported", "proposed", "applied", "skipped")
APPROVAL = ("not-required", "pending", "approved", "denied")
ERROR_CATEGORY = ("invalid-request", "not-permitted", "conflict", "backend-unavailable", "internal")
OPERATION_CLASSES = ("read", "write-report", "propose-change", "apply-change", "delete")
MODES = ("report-only", "propose-only", "apply")
MODE_CLASSES = {
    "report-only": ("read", "write-report"),
    "propose-only": ("read", "write-report", "propose-change"),
}
CONFORMANCE = ("not-tested", "passed", "failed")
COUNT_KEYS = ("seen", "reported", "proposed", "applied", "skipped", "failed")
SUMMARY_KEYS = ("requested", "granted", "applied", "refused")
FIELDS = ("seam-version", "capability", "capability-version", "run-reference", "status",
          "disposition", "approval-state", "error-category", "grant-reference", "counts",
          "mutation-summary", "extensions")
REF_RUN = re.compile(r"run-[a-z2-7]{26}")
REF_GRANT = re.compile(r"grant-[a-z2-7]{26}")
VERSION = re.compile(r"0\.\d+\.\d+")
CAPABILITY = re.compile(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+")
EXT_KEY = re.compile(r"([a-z][a-z0-9-]*\.)+[a-z][a-z0-9-]*")
# Key names that would carry something the crossing rule keeps private.
PRIVATE_KEY = re.compile(
    r"(?i)(^|[-_.])(checksum|hash|digest|permalink|id|uuid|drive|content|body|text|source|query|"
    r"answer|target|path|url|title|before|after|diagnostic|diagnostics|trace|approval-record|record)($|[-_.])")
# Extension names that try to widen authority or the closed vocabularies.
WIDENING_NAME = re.compile(r"(?i)(grant|permission|allow|vocabulary|vocab|mode|override|status|"
                           r"disposition|approval|error)")


class Fail(Exception):
    def __init__(self, category, rule):
        super().__init__(rule)
        self.category, self.rule = category, rule


def _int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _need(cond, rule, category="invalid-request"):
    if not cond:
        raise Fail(category, rule)


def check_shape(env):
    _need(isinstance(env, dict), "envelope-shape")
    for key in env:
        _need(key in FIELDS, "unknown-top-level-field")
    for key in FIELDS:
        _need(key in env, "required-field")
    _need(isinstance(env["seam-version"], str) and VERSION.fullmatch(env["seam-version"]), "version-fields")
    _need(isinstance(env["capability-version"], str) and VERSION.fullmatch(env["capability-version"]), "version-fields")
    _need(isinstance(env["capability"], str) and CAPABILITY.fullmatch(env["capability"]), "version-fields")
    _need(isinstance(env["run-reference"], str) and REF_RUN.fullmatch(env["run-reference"]), "reference-format")
    grant = env["grant-reference"]
    _need(isinstance(grant, str) and (grant == "" or REF_GRANT.fullmatch(grant)), "reference-format")
    for field, allowed in (("status", STATUS), ("disposition", DISPOSITION), ("approval-state", APPROVAL)):
        _need(env[field] in allowed, "closed-vocabulary")
    _need(env["error-category"] == "" or env["error-category"] in ERROR_CATEGORY, "closed-vocabulary")
    if env["status"] == "succeeded":
        _need(env["error-category"] == "", "status-error-category")
    else:
        _need(env["status"] == "partial" or env["error-category"] != "", "status-error-category")
    counts = env["counts"]
    _need(isinstance(counts, dict) and set(counts) == set(COUNT_KEYS) and all(_int(v) for v in counts.values()), "counts-shape")
    summary = env["mutation-summary"]
    _need(isinstance(summary, dict) and set(summary) == set(OPERATION_CLASSES), "mutation-summary-shape")
    for row in summary.values():
        _need(isinstance(row, dict) and set(row) == set(SUMMARY_KEYS) and all(_int(v) for v in row.values()),
              "mutation-summary-shape")
        _need(row["granted"] <= row["requested"] and row["applied"] <= row["granted"]
              and row["granted"] + row["refused"] <= row["requested"], "mutation-summary-arithmetic")
    _need(isinstance(env["extensions"], dict), "extension-shape")
    return env


def check_extensions(env):
    """Unknown extensions are ignored; ones that widen authority or leak are not."""
    for key, value in env["extensions"].items():
        _need(isinstance(key, str) and EXT_KEY.fullmatch(key), "extension-key")
        _need(not PRIVATE_KEY.search(key), "crossing-rule")
        _need(not WIDENING_NAME.search(key.rsplit(".", 1)[1]), "extension-widens", "not-permitted")
        ok_ref = isinstance(value, str) and (REF_RUN.fullmatch(value) or REF_GRANT.fullmatch(value))
        _need(_int(value) or isinstance(value, bool) or ok_ref, "extension-value")


def check(envelope, profile, grants):
    """Return {"result", "error-category", "rule", "conformance-status"}."""
    try:
        check_shape(envelope)
        check_extensions(envelope)
    except Fail as f:
        return _verdict(f)
    return _verdict(None)


def _verdict(fail):
    if fail is None:
        return {"result": "pass", "error-category": "", "rule": "", "conformance-status": "passed"}
    return {"result": "fail", "error-category": fail.category, "rule": fail.rule, "conformance-status": "failed"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--envelope", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--grants", required=True)
    args = ap.parse_args(argv)
    try:
        docs = []
        for path in (args.envelope, args.profile, args.grants):
            with open(path, encoding="utf-8") as f:
                docs.append(json.load(f))
    except (OSError, ValueError):
        print(json.dumps({"result": "fail", "error-category": "invalid-request", "rule": "unreadable-input",
                          "conformance-status": "failed"}))
        return 2
    result = check(*docs)
    print(json.dumps(result))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
