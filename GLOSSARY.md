---
title: Glossary
tags: [glossary, domain, language, governance]
type: glossary
---

# Glossary

The language of `skills`: a public repository of agent skills, and the standard that an advisory reviewer uses to review its pull requests.

## Language

### Skill repositories

**Authority**:
The human-readable Markdown file ([[authorised-skill-repositories]]) that defines which skill repositories are allowed to be used or updated. 

**Projection**:
The machine-readable JSON file (e.g., `golden-skills.json`) derived from the Authority. It must not be manually edited to bypass the Authority.

**Syafiq's Skills Repository**:
This repository (`skills`), containing Syafiq's custom agent skills, onboarding routines, and automated workflows. Any reference to `sk-skills`, `SK-skills`, or `syafiq-kay-skills` refers to this skills repo.
_Avoid_: sk-skills, SK-skills, syafiq-kay-skills

**Authorised Skill Repository**:
A third-party or external repository that has been explicitly permitted in the [[authorised-skill-repositories]]. This is the single source of truth for repository allowlists.

**Skills CLI**:
The future command-line interface to manage, verify, update, and heal agent skills.

**Authorised upstream skill**:
A skill that lives in an Authorised Skill Repository other than this one. A skill here that overlaps one should extend it and record how it differs.
_Avoid_: external skill, third-party skill

**Source repository**:
A repository where skills are developed, such as msc-coach, with this repository as the shipping destination.

**Collision**:
Two skills, across this repository and a Source repository, that have the same name or overlapping function.
_Avoid_: conflict, clash

**Agent Skills Standard**:
The open packaging and metadata specification (agentskills.io) defining SKILL.md frontmatter, directory layout, and progressive disclosure for agent harnesses.
_Avoid_: skill protocol, agent spec

**Deep Module**:
A skill architecture providing a concise, low-surface interface in SKILL.md backed by substantial internal depth (references, templates, scripts), avoiding namespace sprawl.
_Avoid_: monolithic skill, multi-skill bundle

**Pocock Skill Filter**:
The three-part standard (Behavioural Delta, Upstream Overlap, and "What We Care About") that disqualifies generic model instructions and duplicate skills from the repository.
_Avoid_: prompt checklist, linter rules

**Style Module**:
A cross-cutting, model-invoked module governing Syafiq's writing voice, presentation rubrics, artefact templates, and ubiquitous language across all agent interactions.
_Avoid_: formatting guide, style guide

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

### Scheduled runs

**Loaded revision**:
The full 40-character commit SHA of this repository at which a scheduled run fetched its skill files. The run records it as `loaded_revision`.
_Avoid_: pin, pinned version, approved pin

**Tracking**:
Following `main` and resolving its latest commit SHA at run start, which becomes the Loaded revision. Only a supervised run may do this; an unattended run needs an Approved revision.
_Avoid_: pin, approved pin

**Approved revision**:
The full 40-character commit SHA the owner approved for a run. An unattended run requires it and writes nothing unless it equals the Loaded revision; a supervised run (launcher parameter `supervised: true`; anything else is unattended) may record `none`. The run records it as `approved_revision`.
_Avoid_: approved pin, pin

**Run**:
One scheduled execution of the daily maintenance. It writes one Run record set.
_Avoid_: job, cycle, operation

**Operation**:
One of lint or ingest, performed inside a Run. It is not the whole Run.
_Avoid_: run, task

**Run type**:
What a Run does, such as `daily`. The run note records it as `run_type`.
_Avoid_: operation, mode

**Run record set**:
The three notes of one Run in `sk-wiki` `operations/`: `<run-id>-start` and `<run-id>`, written by the run, and `<run-id>-audit`, written later by the Auditor.
_Avoid_: report, ledger

**First-run limit**:
The launcher flag that confines a Run to creating its own start and run notes and deleting nothing. It is true when absent; the owner lifts it after the Auditor passes the first Run.
_Avoid_: dry-run

**Dry-run**:
A Run that writes nothing to the Wiki, not even its start or run note, and reports to its run output only. It differs from the First-run limit, which still writes the two run notes.
_Avoid_: first run

**Deletion allowlist**:
The closed set of rules in the knowledge skills' `references/mutation-rules.md` under which a Run may call `delete_note`, within `knowledge/`, `source-notes/` and `scratch/` only. Everything else is human-only.
_Avoid_: delete permission

**Guarded edit**:
A Wiki write that passes the `expected_checksum` read earlier and is read back afterwards, so a note changed in between is never overwritten.
_Avoid_: safe edit, blind overwrite

**Auditor**:
The separate agent that checks a Run afterwards and writes its `<run-id>-audit` note. The Run never writes it.
_Avoid_: reviewer

### Sprint governance and review

**Docket**:
A versioned markdown submission (e.g., `Docket 1` or `docs/dockets/docket-1.md`) prepared specifically for human deliberation, async inspection in Obsidian, and inline annotation (`> agreed`, `> comment`). When Syafiq states "docket reviewed" or "docket n approved", the agent inspects the file for inline annotations and acts accordingly.
_Avoid_: RFC, pitch, discussion document, proposal

**Work Order (WO)**:
An authoritative operational directive (e.g., `WO-1` or `docs/work-orders/wo-1.md`) that packages sprint tickets, sequential execution order, living execution ledgers, and Chief-of-Staff-only prune points for autonomous AFK delivery.
_Avoid_: task bundle, job order, sprint memo

**Sprint**:
A GitHub Milestone with a defined objective, release gate, and bounded scope.
_Avoid_: iteration, timebox

**Epic**:
A top-level issue that groups child sub-issues.
_Avoid_: initiative, theme

**Ticket**:
An atomic issue with verification criteria and dependencies, labelled `ready-for-agent`.
_Avoid_: task, story

## Observations
- [standard] Establish canonical terminology for skills repository governance and development #glossary
- [convention] Style rules live only in skills/style/SKILL.md #style
- [governance] Dockets and Work Orders govern human deliberation and autonomous execution #agile

## Relations
- defines [[authorised-skill-repositories]]
- defines [[coordinator-protocol]]
- defines [[issue-tracker]]
- defines [[domain]]
