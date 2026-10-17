#!/usr/bin/env python3
"""Seam conformance check (draft, seam 0.1.0). Python standard library only.

Input: a synthetic envelope, a capability profile and a grant set. Output: pass
or fail with a closed error-category. No backend is contacted; the "abstract
backend" is whatever produced the envelope. Nothing private is read or printed.

Usage: seam_conformance.py [--rc] --envelope E.json --profile P.json --grants G.json
Default mode is strict: no profile may open `apply`, `apply-change` or `delete`.
`--rc` is an explicit, opt-in DRAFT check for release-candidate profiles that may
carry mutation grants. It never verifies that an approval is genuine.
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
MUTATION_CLASSES = ("apply-change", "delete")
MODES = ("report-only", "propose-only", "apply")
MODE_CLASSES = {
    "report-only": ("read", "write-report"),
    "propose-only": ("read", "write-report", "propose-change"),
}
# --rc only: the unattended mode permits every class; the profile and grants still gate each one.
RC_MODE_CLASSES = dict(MODE_CLASSES, apply=OPERATION_CLASSES)
CONFORMANCE = ("not-tested", "passed", "failed")
COUNT_KEYS = ("seen", "reported", "proposed", "applied", "skipped", "failed")
SUMMARY_KEYS = ("requested", "granted", "applied", "refused")
FIELDS = ("seam-version", "capability", "capability-version", "run-reference", "status",
          "disposition", "approval-state", "error-category", "grant-reference", "counts",
          "mutation-summary", "extensions")
REF_RUN = re.compile(r"run-[a-z2-7]{26}")
REF_GRANT = re.compile(r"grant-[a-z2-7]{26}")
VERSION = re.compile(r"0\.\d+\.\d+")
# --rc only: opaque approval reference carried by a draft profile. Same style as
# the run and grant references; the exact format is an open question.
REF_APPROVAL = re.compile(r"approval-[a-z2-7]{26}")
RC_DELETE_CAPABILITY = "knowledge.lint"
RC_BANNER = ("DRAFT release-candidate check (--rc): this does not verify that an approval is genuine; "
             "the owner decides the allowlist.")
CAPABILITY = re.compile(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+")
# Reverse-DNS namespace of at least two labels, then a name; labels are lowercase
# alphanumerics joined by single hyphens, starting with a letter.
LABEL = r"[a-z][a-z0-9]*(-[a-z0-9]+)*"
EXT_KEY = re.compile(r"(%s\.){2,}%s" % (LABEL, LABEL))
# Key names that would carry something the crossing rule keeps private.
CROSSING_DENY = re.compile(
    r"(?i)(^|[-_.])(checksum|hash|digest|permalink|id|uuid|drive|content|body|text|source|query|"
    r"answer|target|path|url|title|before|after|diagnostic|diagnostics|trace|approval-record|record)($|[-_.])")
# Extension keys that try to widen authority or imitate the closed vocabularies.
# Every dot- or hyphen-separated token of the whole key (namespace included) is
# tested. WIDENING_NAME is a substring list; RESERVED_WORDS are whole tokens
# (core field names, operation classes, mode words, count and summary keys).
WIDENING_NAME = re.compile(r"(?i)(grant|permission|allow|vocabulary|vocab|override|disposition|approval)")
RESERVED_WORDS = frozenset(
    "mode status error category value values seam version capability run reference counts count "
    "mutation summary extensions state read write report propose change apply delete "
    "seen reported proposed applied skipped failed requested granted refused".split())

MAX_EXTENSIONS = 10
MAX_EXT_KEY_LEN = 64
HEX_PAYLOAD = re.compile(r"^[0-9a-f]{8,}$")
BASE32_PAYLOAD = re.compile(r"^(?=.*[2-7])[a-z2-7]{8,}$")
RAW_REF_PAYLOAD = re.compile(r"^[a-z2-7]{26}$")
REF_PREFIX_PAYLOAD = re.compile(r"^(run|grant|approval)-[a-z2-7]{26}$")


class Fail(Exception):
    def __init__(self, category, rule):
        super().__init__(rule)
        self.category, self.rule = category, rule


def _int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _need(cond, rule, category="invalid-request"):
    if not cond:
        raise Fail(category, rule)


def _str_list(value, allowed=None):
    return isinstance(value, list) and all(isinstance(x, str) and (allowed is None or x in allowed) for x in value)


def check_extension_key_grammar(key):
    _need(isinstance(key, str) and len(key) <= MAX_EXT_KEY_LEN and EXT_KEY.fullmatch(key), "extension-key")
    _need(not (REF_RUN.search(key) or REF_GRANT.search(key) or REF_APPROVAL.search(key)), "extension-key")
    for token in re.split(r"[.-]", key):
        _need(len(token) <= 24, "extension-key")
        if HEX_PAYLOAD.fullmatch(token) and token not in ("feedback", "feedbacks"):
            raise Fail("invalid-request", "extension-key")
        if BASE32_PAYLOAD.fullmatch(token) or RAW_REF_PAYLOAD.fullmatch(token):
            raise Fail("invalid-request", "extension-key")
        if REF_PREFIX_PAYLOAD.fullmatch(token):
            raise Fail("invalid-request", "extension-key")


class ConformancePolicy:
    """Base conformance policy engine unifying envelope, profile, and permission checks."""
    is_rc = False

    def validate_envelope_shape(self, env):
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
        # refused means the operation was not allowed to run, so only not-permitted fits.
        _need(env["status"] != "refused" or env["error-category"] == "not-permitted", "status-error-category")

        # Counts validation
        counts = env["counts"]
        _need(isinstance(counts, dict) and set(counts) == set(COUNT_KEYS) and all(_int(v) for v in counts.values()), "counts-shape")

        # Vulnerability 3 (Failure Masking Patch): succeeded requires failed == 0
        if env["status"] == "succeeded":
            _need(counts.get("failed", 0) == 0, "failure-masking")

        # Mutation summary validation
        summary = env["mutation-summary"]
        _need(isinstance(summary, dict) and set(summary) == set(OPERATION_CLASSES), "mutation-summary-shape")
        for row in summary.values():
            _need(isinstance(row, dict) and set(row) == set(SUMMARY_KEYS) and all(_int(v) for v in row.values()),
                  "mutation-summary-shape")
            _need(row["granted"] <= row["requested"] and row["applied"] <= row["granted"]
                  and row["granted"] + row["refused"] <= row["requested"], "mutation-summary-arithmetic")

        # Extensions shape and capacity
        _need(isinstance(env["extensions"], dict), "extension-shape")
        _need(len(env["extensions"]) <= MAX_EXTENSIONS, "extension-count")
        return env

    def validate_extensions(self, env):
        """Unknown extensions are ignored; ones that widen authority, leak, or smuggle payloads are not."""
        for key, value in env["extensions"].items():
            check_extension_key_grammar(key)
            _need(not CROSSING_DENY.search(key), "crossing-rule")
            _need(not WIDENING_NAME.search(key) and not RESERVED_WORDS & set(re.split(r"[.-]", key)),
                  "extension-widens", "not-permitted")
            ok_ref = isinstance(value, str) and (REF_RUN.fullmatch(value) or REF_GRANT.fullmatch(value))
            _need(_int(value) or isinstance(value, bool) or ok_ref, "extension-value")

    def validate_profile(self, profile, env):
        fields = ("seam-versions", "capability", "capability-version", "execution-modes", "supported-extensions",
                  "allowed-operation-classes", "backend-constraint-tokens", "conformance-status")
        _need(isinstance(profile, dict) and all(f in profile for f in fields), "profile-shape")
        _need(profile["conformance-status"] in CONFORMANCE, "profile-conformance-status")
        _need(_str_list(profile["seam-versions"]) and all(VERSION.fullmatch(v) for v in profile["seam-versions"]), "profile-shape")
        _need(_str_list(profile["execution-modes"], MODES), "profile-shape")
        _need(_str_list(profile["allowed-operation-classes"], OPERATION_CLASSES), "profile-shape")
        _need(_str_list(profile["supported-extensions"]) and _str_list(profile["backend-constraint-tokens"]), "profile-shape")
        self._validate_profile_policy(profile)
        _need(profile["capability"] == env["capability"] and profile["capability-version"] == env["capability-version"]
              and env["seam-version"] in profile["seam-versions"], "profile-mismatch")

    def _validate_profile_policy(self, profile):
        raise NotImplementedError

    def calculate_effective_permissions(self, profile, grants, env):
        """Classes a run may use: granted AND inside the mode AND allowed by the profile."""
        _need(isinstance(grants, dict) and isinstance(grants.get("grants"), list), "grant-set-shape")
        ref = grants.get("grant-reference")
        _need(isinstance(ref, str) and (ref == "" or REF_GRANT.fullmatch(ref)), "grant-set-shape")
        mode = grants.get("mode")
        _need(mode in MODES, "mode-unknown")
        _need(mode in profile["execution-modes"], "mode-not-in-profile", "not-permitted")
        granted = set()
        for entry in grants["grants"]:
            _need(isinstance(entry, dict) and entry.get("operation-class") in OPERATION_CLASSES
                  and isinstance(entry.get("capability"), str), "grant-set-shape")
            self._validate_grant_entry(entry, env)
            if entry["capability"] == env["capability"]:
                granted.add(entry["operation-class"])
        _need(granted <= set(profile["allowed-operation-classes"]), "grant-outside-profile", "not-permitted")
        mode_classes = self._get_mode_classes()
        return granted & set(mode_classes.get(mode, ())) & set(profile["allowed-operation-classes"]), ref

    def _validate_grant_entry(self, entry, env):
        raise NotImplementedError

    def _get_mode_classes(self):
        raise NotImplementedError

    def verify_permissions(self, env, profile, grants, allowed, ref):
        summary = env["mutation-summary"]
        self._verify_envelope_approval(env, summary)
        refusal_needed = False
        for op, row in summary.items():
            if op in allowed:
                continue
            _need(row["granted"] == 0 and row["applied"] == 0, "outside-grant", "not-permitted")
            if row["requested"] > 0:
                refusal_needed = True
                _need(row["refused"] == row["requested"], "outside-grant", "not-permitted")
        if refusal_needed:
            _need(env["status"] == "refused" and env["error-category"] == "not-permitted", "outside-grant", "not-permitted")
        _need(env["disposition"] != "applied" or "apply" in profile["execution-modes"], "applied-not-offered", "not-permitted")
        _need(env["counts"]["applied"] == 0 or "apply" in profile["execution-modes"], "applied-not-offered", "not-permitted")

        # Vulnerability 2 (State Consistency Patch)
        mutation_applied = sum(summary.get(op, {}).get("applied", 0) for op in MUTATION_CLASSES)
        _need(env["counts"]["applied"] == mutation_applied, "state-consistency")
        if env["counts"]["applied"] > 0:
            _need(env["disposition"] == "applied", "state-consistency")

        any_granted = any(row["granted"] > 0 for row in summary.values())
        expected = ref if any_granted else ""
        _need(env["grant-reference"] == expected, "grant-reference", "not-permitted")

    def _verify_envelope_approval(self, env, summary):
        pass

    def construct_verdict(self, fail):
        if fail is None:
            v = {"result": "pass", "error-category": "", "rule": "", "conformance-status": "passed"}
        else:
            v = {"result": "fail", "error-category": fail.category, "rule": fail.rule, "conformance-status": "failed"}
        if self.is_rc:
            v["check"] = "rc-draft"
        return v

    def check(self, env, profile, grants):
        try:
            self.validate_envelope_shape(env)
            self.validate_extensions(env)
            self.validate_profile(profile, env)
            allowed, ref = self.calculate_effective_permissions(profile, grants, env)
            self.verify_permissions(env, profile, grants, allowed, ref)
        except Fail as f:
            return self.construct_verdict(f)
        return self.construct_verdict(None)


class StrictPolicy(ConformancePolicy):
    """Strict default policy: fail-closed rejection of apply, apply-change, and delete."""
    is_rc = False

    def _validate_profile_policy(self, profile):
        _need("apply" not in profile["execution-modes"], "profile-mode", "not-permitted")
        _need(not {"apply-change", "delete"} & set(profile["allowed-operation-classes"]),
              "profile-operation-class", "not-permitted")

    def _validate_grant_entry(self, entry, env):
        _need(entry["operation-class"] != "delete", "delete-never-granted", "not-permitted")

    def _get_mode_classes(self):
        return MODE_CLASSES


class ReleaseCandidatePolicy(ConformancePolicy):
    """Release-candidate policy (--rc): allows approved mutation profiles; restricts delete strictly to knowledge.lint."""
    is_rc = True

    def _validate_profile_policy(self, profile):
        classes = set(profile["allowed-operation-classes"])
        if "apply" in profile["execution-modes"] or "apply-change" in classes or "delete" in classes:
            check_rc_approval(profile)
        _need("delete" not in classes or profile["capability"] == RC_DELETE_CAPABILITY,
              "profile-operation-class", "not-permitted")

    def _validate_grant_entry(self, entry, env):
        _need(entry["operation-class"] != "delete"
              or (entry["capability"] == RC_DELETE_CAPABILITY and entry["capability"] == env["capability"]),
              "delete-never-granted", "not-permitted")

    def _get_mode_classes(self):
        return RC_MODE_CLASSES

    def _verify_envelope_approval(self, env, summary):
        if env["counts"]["applied"] > 0 or any(row["applied"] > 0 for row in summary.values()):
            _need(env["approval-state"] in ("approved", "not-required"), "rc-envelope-approval", "not-permitted")


def get_policy(rc=False):
    return ReleaseCandidatePolicy() if rc is True else StrictPolicy()


def check_shape(env):
    return StrictPolicy().validate_envelope_shape(env)


def check_extensions(env):
    return StrictPolicy().validate_extensions(env)


def check_rc_approval(profile):
    """--rc only: mutation grants need a profile-level approval-state and opaque reference."""
    _need(profile.get("approval-state") == "approved", "rc-approval-state", "not-permitted")
    ref = profile.get("approval-reference")
    _need(isinstance(ref, str) and REF_APPROVAL.fullmatch(ref), "rc-approval-reference", "not-permitted")


def check_profile(profile, env, *, rc=False):
    get_policy(rc).validate_profile(profile, env)


def effective_classes(profile, grants, env, *, rc=False):
    return get_policy(rc).calculate_effective_permissions(profile, grants, env)


def check_permissions(env, profile, grants, *, rc=False):
    policy = get_policy(rc)
    allowed, ref = policy.calculate_effective_permissions(profile, grants, env)
    policy.verify_permissions(env, profile, grants, allowed, ref)


def check(envelope, profile=None, grants=None, *, rc=False):
    """Return {"result", "error-category", "rule", "conformance-status"}.

    rc is keyword-only and only the boolean True enables it. An rc result carries an
    extra key, "check": "rc-draft", so it is never mistaken for a default-mode result.
    """
    return get_policy(rc).check(envelope, profile, grants)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    ap.add_argument("--envelope", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--grants", required=True)
    ap.add_argument("--rc", action="store_true",
                    help="opt-in DRAFT release-candidate check; may accept approved mutation profiles")
    args = ap.parse_args(argv)
    if args.rc:
        print(RC_BANNER, file=sys.stderr)
    try:
        docs = []
        for path in (args.envelope, args.profile, args.grants):
            with open(path, encoding="utf-8") as f:
                docs.append(json.load(f))
    except (OSError, ValueError):
        print(json.dumps({"result": "fail", "error-category": "invalid-request", "rule": "unreadable-input",
                          "conformance-status": "failed"}))
        return 2
    result = check(*docs, rc=args.rc)
    print(json.dumps(result))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
