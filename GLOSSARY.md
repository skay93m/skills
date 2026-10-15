# Glossary

The language of `skills`: a public repository of agent skills, and the standard that an advisory reviewer uses to review its pull requests.

## Language

### Skill repositories

**Authority**:
The human-readable Markdown file (`docs/authorised-skill-repositories.md`) that defines which skill repositories are allowed to be used or updated. This is the single source of truth for repository allowlists.

**Projection**:
The machine-readable JSON file (e.g., `golden-skills.json`) derived from the Authority. It must not be manually edited to bypass the Authority.

**Syafiq's Skills Repository**:
This repository (`skills`), containing Syafiq's custom agent skills, onboarding routines, and automated workflows. Any reference to `sk-skills`, `SK-skills`, or `syafiq-kay-skills` refers to this skills repo.
_Avoid_: sk-skills, SK-skills, syafiq-kay-skills

**Authorised Skill Repository**:
A third-party or external repository (like `mattpocock-skills` or `basic-memory-skills`) that has been explicitly permitted in the Authority.

**Skills CLI**:
The future command-line interface to manage, verify, update, and heal agent skills.

**Authorised upstream skill**:
A skill that lives in an Authorised Skill Repository other than this one. A skill here that overlaps one should extend it and record how it differs.
_Avoid_: external skill, third-party skill

### Skill revision

**Tracking**:
The launcher follows `main` and resolves its latest commit SHA at run start.
_Avoid_: pin, approved pin

**Loaded revision**:
The full commit SHA the run actually loaded, the one that should be recorded.
_Avoid_: pin, approved pin

### Pull request review standard

**Standard**:
The versioned set of checks that the advisory reviewer applies to pull requests in this repository, identified as `sk-pr-review-standard`.
_Avoid_: policy, guidelines, ruleset

**Check**:
One requirement of the standard that can be tested against the diff of a pull request. One review rule can hold several checks.
_Avoid_: test, rule

**Check ID**:
The short identifier of one check, such as `S4` or `H1`. Every finding shows it.
_Avoid_: rule number, code

**Review rule**:
Sourcery's own unit of instruction: plain-language text of up to 3,000 characters, scoped by path patterns, that Sourcery tests only against the changed lines of matching files.
_Avoid_: custom rule, instruction

**Dashboard rule**:
The live copy of a review rule as entered in the Sourcery dashboard, with its stamp filled in. It can drift from the review rule text kept in this repository.
_Avoid_: using it as a synonym for review rule

**Stamp**:
The first line of every review rule. It states the standard's identifier, version, review date and fresh-until date, so a review shows which standard it used.
_Avoid_: version tag, header

**Finding**:
One comment that the advisory reviewer posts on a changed line when a check fails. It carries a label, a check ID, the file and line, and a reason.
_Avoid_: issue, violation, alert

**Blocking**:
The finding label for a problem that should be fixed before the owner merges. It is text in the comment and does not stop a merge.
_Avoid_: failing, required

**Non-blocking**:
The finding label for a suggestion that the owner may merge without acting on.
_Avoid_: warning, nit

**Advisory reviewer**:
A reviewer that recommends approve, comment or request changes and does not decide. Sourcery is the advisory reviewer; the owner decides and merges.
_Avoid_: approver, gatekeeper

**Repair prompt**:
A prompt that the owner gives an agent so it can diagnose and plan repairs for the blocking findings of one review. It lists blocking findings only.
_Avoid_: handover prompt, fix prompt

**Provenance**:
The record, kept in a skill's frontmatter, of where the skill came from: its origin, how much an agent wrote, and, for a skill derived from an upstream, how it differs.
_Avoid_: attribution, credits
