#!/usr/bin/env python3
"""Deterministic checks for the sk-pr-review-standard.

Reads the diff between a base ref and HEAD, applies the mechanical checks of
the standard, and prints GitHub annotations. A BLOCKING finding is an error
annotation and makes the exit code 1; a NON-BLOCKING finding is a warning.
The check is informational: the ruleset does not require it, so the owner
still decides every merge.

Only lines the pull request adds are scanned for pattern checks, so older
problems in untouched lines are not reported. Skill checks run on skills the
pull request adds or edits. S2 and S4 apply only when the skill is new, its
name changes (S2), or lines are added to a file already over 100 lines (S4).

Python standard library only.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

# The checker and its tests quote the patterns they search for, so they are
# exempt from the pattern checks. Changes to them are reported under [STD].
EXEMPT = {"scripts/check-standard.py", "tests/test_check_standard.py"}
STANDARD_PATHS = ("docs/standards/", ".sourcery.yaml",
                  "scripts/check-standard.py", "tests/test_check_standard.py",
                  ".github/workflows/standard-checks.yml")
AGENT_CONFIG = ("AGENTS.md", "CLAUDE.md", ".claude/", ".mcp.json")

FIRST_SECOND_PERSON = re.compile(
    r"\b(I|I'm|I've|I'll|me|my|mine|we|our|you|your|yours|you'll)\b")
PLACEHOLDER = re.compile(
    r"(?i)(example|changeme|placeholder|your[_-]|<[^>]+>|\$\{|\{\{|xxxx|\*{4,}|dummy|sample)")
SECRET_PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
]
SECRET_ASSIGN = re.compile(
    r"""(?i)\b[\w.-]*(secret|token|passw(?:or)?d|api[_-]?key|private[_-]?key|credential)[\w.-]*\s*[:=]\s*(["']?)([^\s"'#]{8,})""")
CREDENTIAL_FILE = re.compile(r"(^|/)(\.env(\.(?!example|sample)[\w.-]+)?|id_rsa|id_ed25519|[\w.-]+\.pem)$")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
EMAIL_OK_DOMAINS = ("noreply.github.com", "users.noreply.github.com",
                    "example.com", "example.org", "example.net", "anthropic.com")
PHONE = re.compile(
    r"(?<![\w+])\+\d{1,3}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}(?!\d)"   # international
    r"|(?<![\w.])\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\d.])"                      # US: 415 555 0134
    r"|(?<![\w.])0\d{3,4}[\s-]\d{3}[\s-]?\d{3,4}(?![\d.])")                       # UK: 07700 900123
HOME_PATH = re.compile(r"(/Users/([A-Za-z0-9._-]+)|/home/([A-Za-z0-9._-]+)|[A-Za-z]:\\Users\\([^\\\s]+))")
HOME_OK_NAMES = {"username", "user", "you", "name", "youruser", "yourname"}
PRIVATE_NOTES = re.compile(r"(basicmemory\.com|memory://|syafiq-kay/wiki)")
INTERNAL_URL = re.compile(
    r"(https?://[^\s)\"']*\.(local|internal|corp|lan|intranet)\b"
    r"|(?<![\w/.-])[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(local|internal|corp|lan|intranet)(?![\w.-])"   # bare host
    r"|\b10\.\d+\.\d+\.\d+\b|\b192\.168\.\d+\.\d+\b|\b172\.(1[6-9]|2\d|3[01])\.\d+\.\d+\b"
    r"|(?<![\w:])(f[cd][0-9a-f]{2}|fe80)(:[0-9a-f]{0,4}){1,7}(?![\w:])"                              # private IPv6
    r"|claude\.ai/code/session_)", re.IGNORECASE)
DOCKER_SOCKET = re.compile(r"docker\.sock")
PIPE_TO_SHELL = re.compile(r"\b(curl|wget)\b[^|\n]*\|\s*(sudo\s+)?(ba|z)?sh\b")
OUTSIDE_WRITE = re.compile(
    r"((>>?|\btee\b(\s+-a)?)\s*[\"']?(~|\$HOME|\$\{HOME\})/\.(bashrc|zshrc|profile|bash_profile|zprofile|ssh|aws|gitconfig))"
    r"|(~|\$HOME)/\.(ssh|aws)/")
UNPINNED_INSTALL = re.compile(r"\b(pip3?|python3? -m pip)\s+install\s+(?!-r\b|--requirement\b)([^\s=@]+)(\s|$)(?!.*==)")
UNPINNED_NPM = re.compile(r"\bnpm\s+(i|install)\s+(?!-)([^\s@]+)(\s|$)")
USES = re.compile(r"\buses:\s*([\w.-]+)/([\w./-]+)@(\S+)")
EVENT_TEXT = re.compile(
    r"\$\{\{\s*github\.(event\.(pull_request\.(title|body|head\.ref|head\.label)|issue\.(title|body)|"
    r"comment\.body|review\.body|head_commit\.message)|head_ref)")
ENV_ASSIGN = re.compile(r"^\s*[A-Z_][A-Z0-9_]*:\s*\$\{\{")
EVAL_UNTRUSTED = re.compile(r"\beval\b.*\$\{?(PR_TITLE|PR_BODY|BRANCH_NAME|ISSUE_BODY|ISSUE_TITLE|COMMENT_BODY)")
SHELL_STEP_LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)#\s]+\.md)")


def git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check).stdout


class Report:
    def __init__(self):
        self.items = []

    def add(self, blocking, check_id, path, line, message):
        self.items.append((blocking, check_id, path, line or 1, message))

    def annotation(self, item):
        blocking, check_id, path, line, message = item
        level = "error" if blocking else "warning"
        label = "BLOCKING" if blocking else "NON-BLOCKING"
        text = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        return f"::{level} file={path},line={line},title={label} [{check_id}]::{text}"

    def summary(self):
        lines = ["## Standard checks (sk-pr-review-standard)", ""]
        if not self.items:
            lines.append("No findings.")
        for blocking, check_id, path, line, message in self.items:
            label = "BLOCKING" if blocking else "NON-BLOCKING"
            lines.append(f"- **{label} [{check_id}]** `{path}:{line}`: {message}")
        return "\n".join(lines) + "\n"


def parse_diff(base):
    """Return (added: {path: [(lineno, text)]}, new_files: set)."""
    out = git("diff", "--unified=0", "--no-color", "--no-renames", "--diff-filter=ACMR", f"{base}...HEAD")
    added, new_files = {}, set()
    path, line, is_new = None, 0, False
    for raw in out.split("\n"):
        if raw.startswith("--- "):
            is_new = raw.strip() == "--- /dev/null"
        elif raw.startswith("+++ b/"):
            path = raw[6:]
            added.setdefault(path, [])
            if is_new:
                new_files.add(path)
        elif raw.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", raw)
            line = int(m.group(1)) if m else 0
        elif raw.startswith("+") and not raw.startswith("+++") and path:
            added[path].append((line, raw[1:]))
            line += 1
    return added, new_files


def exists_in_base(base, token):
    return subprocess.run(["git", "grep", "-q", "-F", "-e", token, base],
                          capture_output=True).returncode == 0


def parse_frontmatter(text):
    """Small parser for the frontmatter keys the standard needs."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None, {}
    data, where, parent, i = {}, {}, None, 1
    while i < end:
        m = re.match(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if not m or lines[i].lstrip().startswith("#"):
            i += 1
            continue
        indent, key, val = len(m.group(1)), m.group(2), m.group(3).strip()
        if val in (">", "|", ">-", "|-"):
            j, parts = i + 1, []
            while j < end and (lines[j].startswith(" ") or not lines[j].strip()):
                parts.append(lines[j].strip())
                j += 1
            val, i = " ".join(p for p in parts if p), j - 1
        elif len(val) > 1 and val[0] in "\"'" and val[-1] == val[0]:
            val = val[1:-1]
        if indent == 0:
            if val == "":
                data[key], parent = {}, key
            else:
                data[key], parent = val, None
            where[key] = i + 1
        elif parent and isinstance(data.get(parent), dict):
            data[parent][key] = val.strip("\"'")
            where[f"{parent}.{key}"] = i + 1
        i += 1
    return data, where


def looks_like_secret(quote, value):
    """A quoted value, or a value with a digit, capital, symbol or length of 16 or more.

    Plain lowercase words such as `token: description` in prose are left alone.
    """
    return bool(quote) or len(value) >= 16 or any(c.isdigit() or c.isupper() or not c.isalnum() for c in value)


def email_domain_ok(email):
    domain = email.rsplit("@", 1)[1].lower()
    return any(domain == ok or domain.endswith("." + ok) for ok in EMAIL_OK_DOMAINS)


def check_secrets_and_privacy(report, base, path, rows):
    if CREDENTIAL_FILE.search(path):
        report.add(True, "H1", path, 1, "A credential file is committed. Remove it from the repository and rotate anything it held.")
    for ln, text in rows:
        for kind, rx in SECRET_PATTERNS:
            if rx.search(text) and not PLACEHOLDER.search(text):
                report.add(True, "H1", path, ln, f"Looks like a {kind}. Remove it and rotate it; the value is not repeated here.")
        m = SECRET_ASSIGN.search(text)
        if m and looks_like_secret(m.group(2), m.group(3)) and not PLACEHOLDER.search(text):
            report.add(True, "H1", path, ln, "A secret or password value is assigned in plain text. Move it to a secret store and rotate it.")
        if PRIVATE_NOTES.search(text):
            report.add(True, "H2", path, ln, "Private notes link or permalink. Replace it with a public reference or remove it.")
        for m in EMAIL.finditer(text):
            email = m.group(0)
            if email_domain_ok(email) or exists_in_base(base, email):
                continue
            report.add(True, "H3", path, ln, "An email address that is not already public in this repository. Remove it or use a placeholder.")
        if PHONE.search(text):
            report.add(True, "H3", path, ln, "A phone number. Remove it or use a placeholder.")
        for m in HOME_PATH.finditer(text):
            user = (m.group(2) or m.group(3) or m.group(4) or "").lower()
            if user not in HOME_OK_NAMES:
                report.add(True, "H4", path, ln, "A local user path. Use a relative path or a placeholder.")
                break
        if INTERNAL_URL.search(text):
            report.add(True, "H6", path, ln, "An internal host, private address or private session link. Remove it.")


def check_shell(report, path, rows):
    for ln, text in rows:
        if DOCKER_SOCKET.search(text):
            report.add(True, "C1", path, ln, "Mounts the Docker socket. Do not give a container control of the host Docker daemon.")
        if PIPE_TO_SHELL.search(text):
            report.add(True, "C2", path, ln, "Pipes a download into a shell. Download the file, verify a digest, inspect it, then run it.")
        if OUTSIDE_WRITE.search(text):
            report.add(True, "C3", path, ln, "Writes outside the repository (shell profile, ssh or cloud credentials). Write inside the repository, or to the skills folders only.")
        if UNPINNED_INSTALL.search(text) or UNPINNED_NPM.search(text):
            report.add(False, "C6", path, ln, "Installs a package without an exact version. Pin it (for example name==1.2.3).")
        if EVAL_UNTRUSTED.search(text):
            report.add(True, "C8", path, ln, "Text an outsider controls is passed to eval. Pass it as a validated, quoted argument.")


def check_workflow(report, path, rows):
    for ln, text in rows:
        m = USES.search(text)
        if m and not m.group(1).startswith("."):
            owner, ref = m.group(1), m.group(3)
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                if owner in ("actions", "github"):
                    report.add(False, "C7", path, ln, "A GitHub-owned action is pinned by tag. Prefer the full commit SHA.")
                else:
                    report.add(True, "C7", path, ln, "A third-party action is pinned by tag or branch. Use the full 40-character commit SHA and keep the tag in a trailing comment.")
        if EVENT_TEXT.search(text) and not ENV_ASSIGN.search(text):
            report.add(True, "C8", path, ln, "Outsider-controlled text is placed directly in the script. Assign it to an environment variable and use it quoted.")
    check_shell(report, path, rows)


def check_skill(report, base, path, rows, is_new):
    skill_dir = os.path.dirname(path)
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return
    data, where = parse_frontmatter(text)
    total = len(text.splitlines())
    if data is None or not data.get("name") or not data.get("description"):
        report.add(True, "S1", path, 1, "Frontmatter must hold a name and a description.")
        return
    name, desc = data["name"], data["description"]
    base_text = git("show", f"{base}:{path}", check=False)
    base_data, _ = parse_frontmatter(base_text) if base_text else (None, {})
    name_changed = is_new or not base_data or base_data.get("name") != name
    if name_changed:
        words = name.split("-")
        problems = []
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            problems.append("must be kebab-case")
        elif len(words) > 3:
            problems.append("must be at most three words")
        if name != os.path.basename(skill_dir):
            problems.append("must equal its directory name")
        if re.search(r"(?i)anthropic|claude", name):
            problems.append('must not contain "anthropic" or "claude"')
        if problems:
            report.add(True, "S2", path, where.get("name", 1), "Skill name " + "; ".join(problems) + ".")
    if len(desc) > 1024:
        report.add(True, "S3", path, where.get("description", 1), f"Description is {len(desc)} characters; the limit is 1,024.")
    if not re.search(r"(?i)use when", desc):
        report.add(True, "S3", path, where.get("description", 1), 'Description needs a "Use when" clause.')
    if FIRST_SECOND_PERSON.search(desc):
        report.add(True, "S3", path, where.get("description", 1), "Description must not use first or second person; use third person or a verb-first form.")
    if total > 100 and (is_new or rows):
        report.add(True, "S4", path, 1, f"SKILL.md has {total} lines; the limit is 100.")
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    origin, involvement = meta.get("origin", ""), meta.get("agent_involvement", "")
    if not origin or involvement not in ("none", "partial", "full"):
        report.add(True, "S6", path, where.get("metadata", 1),
                   'Frontmatter needs metadata.origin (an upstream source and commit, or "original") and metadata.agent_involvement (none, partial or full).')
    elif origin != "original" and not meta.get("divergence"):
        report.add(True, "S6", path, where.get("metadata.origin", 1), "metadata.divergence must say why this version differs from its upstream.")
    if not meta.get("category"):
        report.add(False, "N5", path, where.get("metadata", 1), "metadata.category is missing.")


def check_reference_links(report, path, rows):
    for ln, text in rows:
        if SHELL_STEP_LINK.search(text):
            report.add(True, "S5", path, ln, "A reference file links to another reference file. Link only from SKILL.md, one level deep.")


def check_expiry(report, today):
    try:
        names = [n for n in os.listdir("docs/standards") if n.endswith(".md")]
    except OSError:
        return
    for name in sorted(names):
        path = f"docs/standards/{name}"
        for ln, text in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
            m = re.search(r"fresh until (\d{4}-\d{2}-\d{2})", text)
            if m:
                if today > datetime.date.fromisoformat(m.group(1)):
                    report.add(False, "CUR", path, ln, f"The stamp expired on {m.group(1)}. The owner should re-review and re-stamp the standard.")
                return


def run(base, today):
    report = Report()
    added, new_files = parse_diff(base)
    for path, rows in sorted(added.items()):
        if path in EXEMPT:
            report.add(True, "STD", path, 1, "The checker or its tests changed. The owner must review this change in person.")
            continue
        if path.startswith(STANDARD_PATHS):
            report.add(True, "STD", path, 1, "The standard changes only when its owner re-stamps it. The owner must review this change in person.")
        if path.startswith(AGENT_CONFIG):
            risky = bool(re.search(r"(?i)\b(hooks?|permissions?|allow|mcpServers)\b|\brun\b.*`[^`]+`", "\n".join(t for _, t in rows)))
            report.add(risky, "C5", path, 1, "Agent configuration changed" + (": it adds a hook, command, tool or permission. Say what an agent can now do that it could not before." if risky else " (wording only)."))
        check_secrets_and_privacy(report, base, path, rows)
        if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml")):
            check_workflow(report, path, rows)
        elif path.endswith(".sh") or path.startswith("scripts/") or (path.startswith("skills/") and path.endswith(".md")):
            check_shell(report, path, rows)
        if re.fullmatch(r"skills/[^/]+/SKILL\.md", path):
            check_skill(report, base, path, rows, path in new_files)
        elif path.startswith("skills/") and path.endswith(".md"):
            check_reference_links(report, path, rows)
    check_expiry(report, today)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", default="origin/develop", help="base ref to diff against")
    ap.add_argument("--today", default=None, help="override today's date (YYYY-MM-DD), for tests")
    args = ap.parse_args()
    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
    report = run(args.base, today)
    for item in report.items:
        print(report.annotation(item))
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(report.summary())
    blocking = sum(1 for i in report.items if i[0])
    print(f"standard checks: {blocking} blocking, {len(report.items) - blocking} non-blocking")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
