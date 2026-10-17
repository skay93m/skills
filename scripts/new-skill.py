#!/usr/bin/env python3
"""Scaffolder for deep skill modules driven by declarative YAML/JSON manifests.

Validates the manifest against standard constraints (naming, description,
line budget <= 100, terminal references, artifact contracts) and scaffolds
the skill directory, entrypoint SKILL.md, terminal references, deterministic
scripts, artifact contracts (templates and examples), test stub, and updates
master router ask-syafiq.

Python standard library only.
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FIRST_SECOND_PERSON = re.compile(
    r"\b(I|I'm|I've|I'll|me|my|mine|we|our|you|your|yours|you'll)\b", re.IGNORECASE
)
ALLOWED_DOMAINS = (
    "knowledge",
    "scrum",
    "ecosystem",
    "scholarship",
    "cadence",
    "cognition",
    "general",
)


def strip_comment(line):
    """Strip trailing unquoted comments from a line, respecting escape sequences."""
    in_single = False
    in_double = False
    escaped = False
    for i, ch in enumerate(line):
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return line[:i].rstrip()
    return line.rstrip()


def parse_scalar(val):
    """Parse scalar value (bool, int, float, quoted or unquoted string)."""
    val = val.strip()
    if not val:
        return ""
    if val.startswith(('"', "'")) and val.endswith(('"', "'")) and len(val) >= 2:
        if val[0] == val[-1]:
            q = val[0]
            val = val[1:-1]
            if q == '"':
                val = val.replace('\\"', '"').replace("\\n", "\n")
            elif q == "'":
                val = val.replace("\\'", "'")
            return val
    if val.lower() in ("true", "yes", "on"):
        return True
    if val.lower() in ("false", "no", "off"):
        return False
    if val.lower() in ("null", "none", "~"):
        return None
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if re.fullmatch(r"-?\d+\.\d+", val):
        return float(val)
    if (val.startswith("[") and val.endswith("]")) or (val.startswith("{") and val.endswith("}")):
        try:
            return json.loads(val)
        except Exception:
            pass
    return val


def format_block_scalar(lines, style):
    """Format block scalar lines according to YAML style (> or |)."""
    if not lines:
        return ""
    if style.startswith("|"):
        res = "\n".join(lines)
    else:  # folded style '>'
        paras = []
        cur_para = []
        for line in lines:
            if not line.strip():
                if cur_para:
                    paras.append(" ".join(cur_para))
                    cur_para = []
                paras.append("")
            else:
                cur_para.append(line.strip())
        if cur_para:
            paras.append(" ".join(cur_para))
        res = "\n".join(paras)
    if style in (">-", "|-"):
        return res.rstrip("\n")
    elif style in (">+ ", "|+"):
        return res + "\n"
    else:
        return res.strip()


def parse_yaml_lines(raw_lines):
    """Parse YAML lines supporting block scalars and compact lists."""

    def get_info(i):
        if i >= len(raw_lines):
            return "", 0, "", True
        raw = raw_lines[i]
        cleaned = strip_comment(raw)
        stripped = cleaned.strip()
        is_blank = (len(stripped) == 0)
        indent = len(cleaned) - len(cleaned.lstrip(" ")) if not is_blank else 0
        return raw, indent, stripped, is_blank

    def collect_block_scalar(idx, parent_indent):
        first_idx = idx
        while first_idx < len(raw_lines) and not raw_lines[first_idx].strip():
            first_idx += 1
        if first_idx >= len(raw_lines):
            return [], first_idx
        first_raw = raw_lines[first_idx]
        scalar_indent = len(first_raw) - len(first_raw.lstrip(" "))
        if scalar_indent <= parent_indent:
            return [], idx

        scalar_lines = []
        cur_idx = first_idx
        while cur_idx < len(raw_lines):
            raw = raw_lines[cur_idx]
            if not raw.strip():
                scalar_lines.append("")
                cur_idx += 1
                continue
            line_indent = len(raw) - len(raw.lstrip(" "))
            if line_indent < scalar_indent:
                break
            scalar_lines.append(raw[scalar_indent:])
            cur_idx += 1
        return scalar_lines, cur_idx

    def parse_block(idx, current_indent):
        while idx < len(raw_lines):
            _, _, _, is_blank = get_info(idx)
            if not is_blank:
                break
            idx += 1
        if idx >= len(raw_lines):
            return None, idx

        raw, indent, text, _ = get_info(idx)
        if text.startswith("- ") or text == "-":
            items = []
            while idx < len(raw_lines):
                _, ind, txt, is_blank = get_info(idx)
                if is_blank:
                    idx += 1
                    continue
                if ind < current_indent:
                    break
                if ind > current_indent and not (txt.startswith("- ") or txt == "-"):
                    break
                if txt.startswith("- ") or txt == "-":
                    item_text = txt[2:].strip() if txt.startswith("- ") else ""
                    idx += 1
                    m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", item_text)
                    if m:
                        k, v = m.group(1), m.group(2).strip()
                        sub_dict = {}
                        if v in (">", "|", ">-", "|-", ">+", "|+"):
                            block_lines, idx = collect_block_scalar(idx, ind)
                            sub_dict[k] = format_block_scalar(block_lines, v)
                        elif v != "":
                            sub_dict[k] = parse_scalar(v)
                        else:
                            next_i = idx
                            while next_i < len(raw_lines):
                                _, _, _, b = get_info(next_i)
                                if not b:
                                    break
                                next_i += 1
                            if next_i < len(raw_lines):
                                _, next_ind, _, _ = get_info(next_i)
                                if next_ind > ind:
                                    sub_val, idx = parse_block(next_i, next_ind)
                                    sub_dict[k] = sub_val
                                else:
                                    sub_dict[k] = None
                                    idx = next_i
                            else:
                                sub_dict[k] = None
                                idx = next_i
                        while idx < len(raw_lines):
                            _, next_ind, next_txt, is_blank = get_info(idx)
                            if is_blank:
                                idx += 1
                                continue
                            if next_ind <= ind:
                                break
                            m2 = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", next_txt)
                            if m2:
                                k2, v2 = m2.group(1), m2.group(2).strip()
                                idx += 1
                                if v2 in (">", "|", ">-", "|-", ">+", "|+"):
                                    block_lines, idx = collect_block_scalar(idx, next_ind)
                                    sub_dict[k2] = format_block_scalar(block_lines, v2)
                                elif v2 != "":
                                    sub_dict[k2] = parse_scalar(v2)
                                else:
                                    next_i = idx
                                    while next_i < len(raw_lines):
                                        _, _, _, b = get_info(next_i)
                                        if not b:
                                            break
                                        next_i += 1
                                    if next_i < len(raw_lines):
                                        _, follow_ind, _, _ = get_info(next_i)
                                        if follow_ind > next_ind:
                                            val2, idx = parse_block(next_i, follow_ind)
                                            sub_dict[k2] = val2
                                        else:
                                            sub_dict[k2] = None
                                            idx = next_i
                                    else:
                                        sub_dict[k2] = None
                                        idx = next_i
                            else:
                                break
                        items.append(sub_dict)
                    elif item_text:
                        items.append(parse_scalar(item_text))
                    else:
                        next_i = idx
                        while next_i < len(raw_lines):
                            _, _, _, b = get_info(next_i)
                            if not b:
                                break
                            next_i += 1
                        if next_i < len(raw_lines):
                            _, follow_ind, _, _ = get_info(next_i)
                            if follow_ind > ind:
                                val, idx = parse_block(next_i, follow_ind)
                                items.append(val)
                            else:
                                items.append(None)
                                idx = next_i
                        else:
                            items.append(None)
                            idx = next_i
                else:
                    break
            return items, idx
        else:
            mapping = {}
            while idx < len(raw_lines):
                _, ind, txt, is_blank = get_info(idx)
                if is_blank:
                    idx += 1
                    continue
                if ind < current_indent:
                    break
                m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", txt)
                if not m:
                    idx += 1
                    continue
                k, v = m.group(1), m.group(2).strip()
                idx += 1
                if v in (">", "|", ">-", "|-", ">+", "|+"):
                    block_lines, idx = collect_block_scalar(idx, ind)
                    mapping[k] = format_block_scalar(block_lines, v)
                elif v != "":
                    mapping[k] = parse_scalar(v)
                else:
                    next_i = idx
                    while next_i < len(raw_lines):
                        _, _, _, b = get_info(next_i)
                        if not b:
                            break
                        next_i += 1
                    if next_i < len(raw_lines):
                        _, next_ind, next_txt, _ = get_info(next_i)
                        if next_ind > ind:
                            sub_val, idx = parse_block(next_i, next_ind)
                            mapping[k] = sub_val
                        elif next_ind == ind and (next_txt.startswith("- ") or next_txt == "-"):
                            sub_val, idx = parse_block(next_i, ind)
                            mapping[k] = sub_val
                        else:
                            mapping[k] = None
                            idx = next_i
                    else:
                        mapping[k] = None
                        idx = next_i
            return mapping, idx

    res, _ = parse_block(0, 0)
    return res if isinstance(res, dict) else {}


def parse_manifest(text):
    """Parse manifest text as JSON if applicable, or as YAML."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("Manifest content is empty")
    if stripped.startswith("{"):
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                return data
            raise ValueError("Manifest root must be an object/dict")
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON in manifest: {err}")
    parsed = parse_yaml_lines(text.splitlines())
    if not isinstance(parsed, dict) or not parsed:
        raise ValueError("Failed to parse manifest as valid YAML or JSON object")
    return parsed


def validate_manifest(manifest):
    """Validate manifest data against standard schema rules.

    Raises ValueError on validation failure.
    """
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be a key-value mapping")

    if "name" not in manifest or not isinstance(manifest["name"], str):
        raise ValueError("Manifest missing required field 'name'")
    name = manifest["name"].strip()
    if not NAME_RE.fullmatch(name):
        raise ValueError(f"Skill name '{name}' must be lowercase kebab-case")
    words = name.split("-")
    if len(words) > 3:
        raise ValueError(f"Skill name '{name}' must have at most three words (got {len(words)})")
    if "anthropic" in name.lower() or "claude" in name.lower():
        raise ValueError(f"Skill name '{name}' must not contain 'anthropic' or 'claude'")

    if "description" not in manifest or not isinstance(manifest["description"], str):
        raise ValueError("Manifest missing required field 'description'")
    desc = manifest["description"].strip()
    if len(desc) > 1024:
        raise ValueError(f"Description length ({len(desc)}) exceeds maximum 1,024 characters")
    if "use when" not in desc.lower():
        raise ValueError("Description must contain a 'Use when' clause")
    if FIRST_SECOND_PERSON.search(desc):
        raise ValueError("Description must not use first or second person pronouns (I, we, you, etc.)")

    if "version" in manifest and not isinstance(manifest["version"], str):
        raise ValueError("'version' must be a string")

    if "provenance" in manifest and not isinstance(manifest["provenance"], str):
        raise ValueError("'provenance' must be a string")

    if "divergence" in manifest and not isinstance(manifest["divergence"], str):
        raise ValueError("'divergence' must be a string")

    if "disable-model-invocation" in manifest and not isinstance(manifest["disable-model-invocation"], bool):
        raise ValueError("'disable-model-invocation' must be a boolean")

    if "user-invoked" in manifest and not isinstance(manifest["user-invoked"], bool):
        raise ValueError("'user-invoked' must be a boolean")

    if "triggers" in manifest:
        triggers = manifest["triggers"]
        if not isinstance(triggers, list):
            raise ValueError("'triggers' must be a list of non-empty strings")
        for t in triggers:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("Each trigger in 'triggers' must be a non-empty string")

    if "budgets" in manifest:
        budgets = manifest["budgets"]
        if not isinstance(budgets, dict):
            raise ValueError("'budgets' must be an object")
        if "line-budget" in budgets:
            lb = budgets["line-budget"]
            if isinstance(lb, bool) or not isinstance(lb, int) or lb <= 0 or lb > 100:
                raise ValueError(f"Invalid line-budget '{lb}': must be an integer between 1 and 100")
        if "token-budget" in budgets:
            tb = budgets["token-budget"]
            if isinstance(tb, bool) or not isinstance(tb, int) or tb <= 0 or tb > 700:
                raise ValueError(f"Invalid token-budget '{tb}': must be an integer between 1 and 700")

    if "references" in manifest:
        refs = manifest["references"]
        if not isinstance(refs, list):
            raise ValueError("'references' must be a list of filenames")
        for ref in refs:
            if not isinstance(ref, str) or not ref.strip():
                raise ValueError(f"Invalid reference entry: {ref}")
            cleaned_ref = ref.strip()
            if ".." in cleaned_ref or cleaned_ref.startswith(("/", "\\")):
                raise ValueError(f"Reference '{ref}' must not contain path traversal or leading slash")
            if not cleaned_ref.endswith(".md"):
                raise ValueError(f"Reference '{ref}' must end with .md")
            base_name = os.path.basename(cleaned_ref)
            if cleaned_ref != base_name and cleaned_ref != f"references/{base_name}":
                raise ValueError(f"Reference '{ref}' must be directly under references/ without nested directories")

    if "scripts" in manifest:
        scripts = manifest["scripts"]
        if not isinstance(scripts, list):
            raise ValueError("'scripts' must be a list of filenames")
        for s in scripts:
            if not isinstance(s, str) or not s.strip():
                raise ValueError(f"Invalid script entry: {s}")
            cleaned_s = s.strip()
            if ".." in cleaned_s or cleaned_s.startswith(("/", "\\")):
                raise ValueError(f"Script '{s}' must not contain path traversal or leading slash")
            base_s = os.path.basename(cleaned_s)
            if cleaned_s != base_s and cleaned_s != f"scripts/{base_s}":
                raise ValueError(f"Script '{s}' must be directly under scripts/ without nested directories")

    if "artifacts" in manifest:
        artifacts = manifest["artifacts"]
        if not isinstance(artifacts, dict):
            raise ValueError("'artifacts' must be an object")
        if "produces" in artifacts and not isinstance(artifacts["produces"], bool):
            raise ValueError("'artifacts.produces' must be a boolean")
        produces = artifacts.get("produces") is True
        if produces:
            contracts = artifacts.get("contracts")
            if not isinstance(contracts, list) or len(contracts) == 0:
                raise ValueError("Artifacts contract declaration requires a non-empty 'contracts' list when produces is true")
            for c in contracts:
                if not isinstance(c, dict):
                    raise ValueError("Each artifact contract must be an object")
                c_name = c.get("name")
                if not c_name or not isinstance(c_name, str):
                    raise ValueError("Artifact contract missing required field 'name'")
                c_name = c_name.strip()
                if not NAME_RE.fullmatch(c_name):
                    raise ValueError(f"Artifact contract name '{c_name}' must be lowercase kebab-case")
                if "template" in c:
                    tpl = c["template"]
                    if not isinstance(tpl, str) or not tpl.strip():
                        raise ValueError(f"Artifact contract '{c_name}' template must be a non-empty string")
                    tpl = tpl.strip()
                    if ".." in tpl or tpl.startswith(("/", "\\")):
                        raise ValueError(f"Artifact contract '{c_name}' template '{tpl}' must not contain path traversal or leading slash")
                    if not (tpl.endswith(".template.md") or tpl.endswith(".md")):
                        raise ValueError(f"Artifact contract '{c_name}' template '{tpl}' must end with .template.md or .md")
                    base_tpl = os.path.basename(tpl)
                    if tpl != base_tpl and tpl != f"templates/{base_tpl}":
                        raise ValueError(f"Artifact contract '{c_name}' template '{tpl}' must reside strictly in templates/ without subdirectories")
                if "example" in c:
                    ex = c["example"]
                    if not isinstance(ex, str) or not ex.strip():
                        raise ValueError(f"Artifact contract '{c_name}' example must be a non-empty string")
                    ex = ex.strip()
                    if ".." in ex or ex.startswith(("/", "\\")):
                        raise ValueError(f"Artifact contract '{c_name}' example '{ex}' must not contain path traversal or leading slash")
                    if not (ex.endswith(".example.md") or ex.endswith(".md")):
                        raise ValueError(f"Artifact contract '{c_name}' example '{ex}' must end with .example.md or .md")
                    base_ex = os.path.basename(ex)
                    if ex != base_ex and ex != f"examples/{base_ex}":
                        raise ValueError(f"Artifact contract '{c_name}' example '{ex}' must reside strictly in examples/ without subdirectories")
        elif "contracts" in artifacts and not isinstance(artifacts["contracts"], list):
            raise ValueError("'artifacts.contracts' must be a list of objects")

    if "router" in manifest:
        router = manifest["router"]
        if not isinstance(router, dict):
            raise ValueError("'router' must be an object")
        if "domain" in router:
            domain = router["domain"]
            if not isinstance(domain, str) or domain not in ALLOWED_DOMAINS:
                raise ValueError(f"'router.domain' must be one of {ALLOWED_DOMAINS}")
        if "intents" in router:
            intents = router["intents"]
            if not isinstance(intents, list):
                raise ValueError("'router.intents' must be a list of non-empty strings")
            for intent in intents:
                if not isinstance(intent, str) or not intent.strip():
                    raise ValueError("Each intent in 'router.intents' must be a non-empty string")


def estimate_tokens(text):
    """Rough estimation of token count for English text."""
    words = text.split()
    return int(len(words) * 1.3)


def format_title(kebab_name):
    """Format kebab-case identifier into Title Case."""
    return " ".join(part.capitalize() for part in kebab_name.split("-"))


def escape_table_cell(text):
    """Escape pipe characters for markdown table cells."""
    return str(text).replace("|", r"\|")


def build_routing_row(name, domain, intents):
    """Construct clean markdown table row for master router ask-syafiq."""
    clean_domain = escape_table_cell(domain)
    clean_name = escape_table_cell(name)
    clean_skill_link = f"`{clean_name}`"
    clean_intents = [escape_table_cell(i) for i in intents]
    intents_str = ", ".join(clean_intents) if clean_intents else format_title(clean_name)
    return f"| {clean_domain} | {clean_skill_link} | {intents_str} |"


def preflight_master_router(ask_syafiq_skill_file, name, domain, intents):
    """Check whether updating ask-syafiq would exceed budget before creating files."""
    if not ask_syafiq_skill_file.exists():
        return
    lines = ask_syafiq_skill_file.read_text(encoding="utf-8").splitlines()
    skill_marker = f"`{name}`"
    for line in lines:
        if skill_marker in line and line.strip().startswith("|"):
            return

    row_text = build_routing_row(name, domain, intents)
    test_lines = list(lines)
    table_header_idx = -1
    for idx, line in enumerate(test_lines):
        if line.strip().startswith("| Domain | Skill |"):
            table_header_idx = idx
            break

    if table_header_idx != -1:
        insert_idx = table_header_idx + 2
        while insert_idx < len(test_lines) and test_lines[insert_idx].strip().startswith("|"):
            insert_idx += 1
        test_lines.insert(insert_idx, row_text)
    else:
        test_lines.extend([
            "",
            "## Routing Table",
            "",
            "| Domain | Skill | Intents / Triggers |",
            "|---|---|---|",
            row_text,
        ])
    new_content = "\n".join(test_lines).rstrip() + "\n"
    if len(new_content.splitlines()) > 100:
        raise ValueError(
            f"Preflight check failed: updating ask-syafiq/SKILL.md would exceed line budget ({len(new_content.splitlines())} > 100)"
        )


def update_master_router(ask_syafiq_skill_file, name, domain, intents):
    """Append or update routing entries in ask-syafiq/SKILL.md cleanly and idempotently."""
    ask_syafiq_dir = ask_syafiq_skill_file.parent
    ask_syafiq_dir.mkdir(parents=True, exist_ok=True)

    row_text = build_routing_row(name, domain, intents)

    if not ask_syafiq_skill_file.exists():
        content = f"""---
name: ask-syafiq
description: Use when routing requests across domains and specialized skills in the personal skill catalog.
disable-model-invocation: true
version: 0.1.0
provenance: original
metadata:
  origin: original
  agent_involvement: full
  category: router
---

# Ask Syafiq

Master router skill for dispatching requests to specialized domain skills.

## Routing Table

| Domain | Skill | Intents / Triggers |
|---|---|---|
{row_text}
"""
        ask_syafiq_skill_file.write_text(content, encoding="utf-8")
        return

    lines = ask_syafiq_skill_file.read_text(encoding="utf-8").splitlines()
    skill_marker = f"`{name}`"
    for line in lines:
        if skill_marker in line and line.strip().startswith("|"):
            return

    table_header_idx = -1
    for idx, line in enumerate(lines):
        if line.strip().startswith("| Domain | Skill |"):
            table_header_idx = idx
            break

    if table_header_idx != -1:
        insert_idx = table_header_idx + 2
        while insert_idx < len(lines) and lines[insert_idx].strip().startswith("|"):
            insert_idx += 1
        lines.insert(insert_idx, row_text)
    else:
        lines.extend([
            "",
            "## Routing Table",
            "",
            "| Domain | Skill | Intents / Triggers |",
            "|---|---|---|",
            row_text,
        ])

    new_content = "\n".join(lines).rstrip() + "\n"
    new_lines = new_content.splitlines()
    if len(new_lines) > 100:
        raise ValueError(
            f"Updating ask-syafiq/SKILL.md would exceed line budget ({len(new_lines)} > 100)"
        )
    ask_syafiq_skill_file.write_text(new_content, encoding="utf-8")


def scaffold_skill(manifest, skills_dir, tests_dir):
    """Scaffold files and directories for a validated skill manifest."""
    name = manifest["name"].strip()
    desc = manifest["description"].strip()
    desc_single_line = " ".join(part.strip() for part in desc.splitlines() if part.strip())
    version = manifest.get("version", "0.1.0")
    provenance = manifest.get("provenance", "original")
    origin = provenance
    divergence = manifest.get("divergence")
    if origin != "original" and not divergence:
        divergence = f"Adapted from upstream {origin} for personal skill catalog."

    disable_invoc = "true" if manifest.get("disable-model-invocation", True) else "false"

    budgets = manifest.get("budgets") if isinstance(manifest.get("budgets"), dict) else {}
    line_limit = budgets.get("line-budget", 100)
    tok_ceiling = budgets.get("token-budget", 700)

    router = manifest.get("router") if isinstance(manifest.get("router"), dict) else {}
    domain = router.get("domain", "general")
    intents = router.get("intents") or manifest.get("triggers") or []

    skills_path = pathlib.Path(skills_dir)
    tests_path = pathlib.Path(tests_dir)

    skill_dir = skills_path / name
    if skill_dir.exists():
        raise ValueError(f"Skill directory already exists: {skill_dir}")

    ask_syafiq = skills_path / "ask-syafiq" / "SKILL.md"
    preflight_master_router(ask_syafiq, name, domain, intents)

    created_files = []
    skill_dir_created = False

    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_dir_created = True

        ref_dir = skill_dir / "references"
        scripts_dir = skill_dir / "scripts"
        templates_dir = skill_dir / "templates"
        examples_dir = skill_dir / "examples"

        refs = manifest.get("references") or []
        ref_links = []
        if refs:
            ref_dir.mkdir(parents=True, exist_ok=True)
            for ref in refs:
                base_ref = os.path.basename(ref)
                ref_path = ref_dir / base_ref
                ref_title = format_title(base_ref.removesuffix(".md"))
                ref_content = f"""# {ref_title}

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other reference files.

Detailed specification and procedures for {base_ref}.
"""
                ref_path.write_text(ref_content, encoding="utf-8")
                created_files.append(str(ref_path))
                ref_links.append(f"- [{ref_title}](references/{base_ref})")

        scripts = manifest.get("scripts") or []
        script_links = []
        if scripts:
            scripts_dir.mkdir(parents=True, exist_ok=True)
            for scr in scripts:
                base_scr = os.path.basename(scr)
                scr_path = scripts_dir / base_scr
                if base_scr.endswith(".py"):
                    scr_content = f"""#!/usr/bin/env python3
\"\"\"Helper script for {name}.\"\"\"
import sys


def main():
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""
                else:
                    scr_content = f"""#!/usr/bin/env bash
set -euo pipefail

# Helper script for {name}
exit 0
"""
                scr_path.write_text(scr_content, encoding="utf-8")
                os.chmod(scr_path, 0o755)
                created_files.append(str(scr_path))
                script_links.append(f"- `scripts/{base_scr}`: Executable helper script.")

        artifacts = manifest.get("artifacts") or {}
        produces = artifacts.get("produces") is True
        contracts = artifacts.get("contracts") or []
        contract_links = []
        contract_paths = []
        if produces and contracts:
            templates_dir.mkdir(parents=True, exist_ok=True)
            examples_dir.mkdir(parents=True, exist_ok=True)
            for c in contracts:
                c_name = c["name"].strip()
                c_title = format_title(c_name)

                raw_tpl = c.get("template") or f"templates/{c_name}.template.md"
                base_tpl = os.path.basename(raw_tpl)
                tpl_rel = f"templates/{base_tpl}"
                tpl_path = (skill_dir / tpl_rel).resolve()
                if not tpl_path.is_relative_to((skill_dir / "templates").resolve()):
                    raise ValueError(f"Template path '{raw_tpl}' resolves outside templates directory")
                tpl_path.parent.mkdir(parents=True, exist_ok=True)
                tpl_content = f"""# {c_title} Template

## Metadata
- Date: {{{{DATE}}}}
- Status: {{{{STATUS}}}}

## Content
{{{{CONTENT}}}}
"""
                tpl_path.write_text(tpl_content, encoding="utf-8")
                created_files.append(str(tpl_path))
                contract_paths.append(tpl_rel)

                raw_ex = c.get("example") or f"examples/{c_name}.example.md"
                base_ex = os.path.basename(raw_ex)
                ex_rel = f"examples/{base_ex}"
                ex_path = (skill_dir / ex_rel).resolve()
                if not ex_path.is_relative_to((skill_dir / "examples").resolve()):
                    raise ValueError(f"Example path '{raw_ex}' resolves outside examples directory")
                ex_path.parent.mkdir(parents=True, exist_ok=True)
                ex_content = f"""# {c_title} Example

## Metadata
- Date: 2026-10-17
- Status: succeeded

## Content
Canonical example output demonstrating successful artifact generation.
"""
                ex_path.write_text(ex_content, encoding="utf-8")
                created_files.append(str(ex_path))
                contract_paths.append(ex_rel)

                contract_links.append(
                    f"- Contract `{c_name}`: [Template]({tpl_rel}) and [Example]({ex_rel})."
                )

        skill_title = format_title(name)
        sections = [
            "---",
            f"name: {name}",
            f"description: {desc_single_line}",
            f"disable-model-invocation: {disable_invoc}",
            f"version: {version}",
            f"provenance: {provenance}",
            "metadata:",
            f"  origin: {origin}",
            "  agent_involvement: full",
            f"  category: {domain}",
        ]
        if origin != "original" and divergence:
            sections.append(f"  divergence: {divergence}")
        sections.extend([
            "---",
            "",
            f"# {skill_title}",
            "",
            desc,
        ])

        if ref_links:
            sections.extend(["", "## References", ""] + ref_links)

        if script_links:
            sections.extend(["", "## Scripts", ""] + script_links)

        if contract_links:
            sections.extend(["", "## Artifact Contracts", ""] + contract_links)

        skill_content = "\n".join(sections).rstrip() + "\n"
        skill_lines = skill_content.splitlines()
        if len(skill_lines) > line_limit:
            raise ValueError(
                f"Generated SKILL.md exceeds line budget ({len(skill_lines)} > {line_limit} lines)"
            )
        tok_est = estimate_tokens(skill_content)
        if tok_est > tok_ceiling:
            raise ValueError(
                f"Generated SKILL.md exceeds token budget (~{tok_est} > {tok_ceiling} tokens)"
            )

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(skill_content, encoding="utf-8")
        created_files.append(str(skill_md))

        update_master_router(ask_syafiq, name, domain, intents)
        created_files.append(str(ask_syafiq))

        tests_path.mkdir(parents=True, exist_ok=True)
        snake_name = name.replace("-", "_")
        test_file = tests_path / f"test_skill_{snake_name}.py"
        class_name = "".join(part.capitalize() for part in snake_name.split("_"))

        try:
            rel_from_tests_to_skill = os.path.relpath(skill_dir, tests_path)
        except ValueError:
            rel_from_tests_to_skill = str(skill_dir)

        if contract_paths:
            paths_repr = ", ".join(repr(p) for p in contract_paths)
            artifact_test_body = f"""        for rel_path in [{paths_repr}]:
            target = self.skill_dir / rel_path
            self.assertTrue(target.exists(), f"Contract artifact {{rel_path}} does not exist")"""
        else:
            artifact_test_body = "        pass"

        test_content = f"""import os
import pathlib
import re
import unittest

SKILL_NAME = "{name}"


class TestSkill{class_name}(unittest.TestCase):
    def setUp(self):
        env_skills = os.environ.get("SKILLS_DIR")
        if env_skills:
            self.skill_dir = pathlib.Path(env_skills) / SKILL_NAME
        else:
            rel = pathlib.Path("{rel_from_tests_to_skill}")
            candidate = (pathlib.Path(__file__).resolve().parent / rel).resolve()
            if candidate.exists():
                self.skill_dir = candidate
            else:
                self.skill_dir = pathlib.Path(__file__).resolve().parent.parent / "skills" / SKILL_NAME

    def test_skill_md_exists_and_line_budget(self):
        skill_md = self.skill_dir / "SKILL.md"
        self.assertTrue(skill_md.exists(), f"SKILL.md missing for {{SKILL_NAME}}")
        lines = skill_md.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), {line_limit}, f"SKILL.md line count {{len(lines)}} exceeds {line_limit}")

    def test_terminal_references_invariant(self):
        ref_dir = self.skill_dir / "references"
        if not ref_dir.exists():
            return
        link_re = re.compile(r"\\]\\((?!https?://|#|mailto:)([^)]*\\.md[^)]*)\\)")
        for ref_file in ref_dir.glob("*.md"):
            content = ref_file.read_text(encoding="utf-8")
            matches = link_re.findall(content)
            self.assertEqual(matches, [], f"Reference file {{ref_file.name}} links to other markdown files: {{matches}}")

    def test_artifact_contracts_exist(self):
{artifact_test_body}


if __name__ == "__main__":
    unittest.main()
"""
        test_file.write_text(test_content, encoding="utf-8")
        created_files.append(str(test_file))

    except Exception:
        if skill_dir_created and skill_dir.exists():
            shutil.rmtree(skill_dir, ignore_errors=True)
        raise

    return {
        "name": name,
        "skill_dir": str(skill_dir),
        "skill_md": str(skill_md),
        "test_file": str(test_file),
        "created_files": created_files,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--manifest", required=True, help="Path to YAML/JSON skill manifest file")
    parser.add_argument("--skills-dir", default="skills", help="Directory for skills (default: skills)")
    parser.add_argument("--tests-dir", default="tests", help="Directory for test stubs (default: tests)")
    args = parser.parse_args(argv)

    manifest_path = pathlib.Path(args.manifest)
    if not manifest_path.exists():
        sys.stderr.write(f"Error: Manifest file not found: {manifest_path}\n")
        return 1

    try:
        manifest_text = manifest_path.read_text(encoding="utf-8")
    except Exception as err:
        sys.stderr.write(f"Error: Failed to read manifest file: {err}\n")
        return 1

    try:
        manifest_data = parse_manifest(manifest_text)
        validate_manifest(manifest_data)
        result = scaffold_skill(manifest_data, args.skills_dir, args.tests_dir)
    except ValueError as err:
        sys.stderr.write(f"Error: {err}\n")
        return 1
    except Exception as err:
        sys.stderr.write(f"Internal error: {err}\n")
        return 1

    print(f"Successfully scaffolded skill '{result['name']}':")
    for f in result["created_files"]:
        print(f"  - {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
