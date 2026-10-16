# Capability profiles (draft)

Stage: draft. Drafting a profile implies no active binding. Sources: P3 to P7 on #79, specification #90, ticket #92.

## Profile format

A profile is one JSON object. Every field is required.

| Field | Meaning |
| --- | --- |
| `seam-versions` | List of seam versions the profile supports. |
| `capability` | Capability name. |
| `capability-version` | Capability version. Independent of the seam version. |
| `execution-modes` | Subset of `report-only`, `propose-only`, `apply`. |
| `supported-extensions` | List of extension keys the capability understands; may be empty. |
| `allowed-operation-classes` | Subset of the closed operation classes. |
| `backend-constraint-tokens` | List of backend-constraint tokens. Format is **SW input needed** (`tokens.md`). |
| `conformance-status` | `not-tested`, `passed` or `failed`. Nothing else is public. |

## Permission model

A mode, a role or a passing test grants nothing. A grant is a human-approved allowlist entry for one capability and one operation class. A run may use an operation class only if all three hold: a grant exists, the mode permits the class, and the profile allows it. The mode permits `read` and `write-report` in `report-only`, and adds `propose-change` in `propose-only`. A request outside this set gives `status: refused` and `error-category: not-permitted`.

## knowledge.ingest 0.1.0

The file is `profiles/knowledge-ingest-0.1.0.json`.

- Modes: `report-only` and `propose-only`. `apply` is not offered.
- Operation classes: `read`, `write-report`, `propose-change`. `apply-change` and `delete` are excluded; no grant for `delete` exists in seam 0.1.0.
- Extensions: none.
- Backend-constraint tokens: none yet (**SW input needed**).
- Conformance status: `not-tested`. The public check in `scripts/seam_conformance.py` covers the envelope and permission rules on synthetic data. The check of the real binding is private to SW.

## Grant set (conformance input)

The conformance check reads a synthetic grant set: `grant-reference` (opaque or empty), `mode`, and a list of `{capability, operation-class}` entries. The real grant record (who approved, when, scope) stays private.

## Running the check

`python3 scripts/seam_conformance.py --envelope E.json --profile P.json --grants G.json` prints one JSON line with `result`, `error-category`, `rule` and `conformance-status`, and exits 0 on pass. The `rule` value names the failed rule and carries no data from the input. Without a flag this default check is strict: it rejects `apply` and the `apply-change` and `delete` classes in any profile.

## Draft release-candidate check (`--rc`)

Draft, opt-in and explicit. Add `--rc` to run the same check on a draft release-candidate profile that may carry mutation grants. The flag is never detected from a file name or from content. The check prints a banner on standard error that it is a DRAFT check; it does not verify that an approval is genuine, and the owner decides the allowlist.

Only these rules change under `--rc`:

- A profile may list the `apply` mode or the `apply-change` class only if it carries `approval-state: approved` and an `approval-reference`. The reference is opaque: `approval-` followed by 26 characters from `a-z2-7` (**Proposed**, same style as the grant reference; the format is open).
- A profile may list `delete` only if its capability is `knowledge.lint` and it carries the same two approval fields. Any other capability keeps `delete` rejected, and a `delete` grant is accepted only for `knowledge.lint`.
- In the `apply` mode, the mode permits every class; the grant and the profile still decide.

Everything else still applies: closed vocabularies, extension and leak rules, and the `0.x.y` version patterns (no `-rc.N` suffix). The two approval fields are the only approval data a public profile carries; the approval record stays private. The checker cannot tell a real approval from a made-up reference.
