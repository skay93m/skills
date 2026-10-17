# Architecture Decision Record (ADR) Formulation Guide

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This guide defines the structure, evaluation criteria, and lifecycle management for Architecture Decision Records (ADRs) formulated following Socratic sparring sessions.

---

## 1. Purpose of Architecture Decision Records

An Architecture Decision Record captures an important architectural decision, along with its context, considered alternatives, and resulting consequences. ADRs turn transient discussions into durable, auditable technical history.

---

## 2. Decision Reversibility & Velocity (Type 1 vs Type 2)

Before drafting an ADR, classify the decision by its reversibility:

- **Type 1 Decisions (One-Way Doors)**:
  - *Characteristics*: Irreversible or prohibitively expensive to alter once deployed (e.g. core database engine, primary programming language, security model).
  - *Process Requirement*: Demands exhaustive Socratic sparring, written pre-mortem, consensus from senior peers, and formal ADR approval.

- **Type 2 Decisions (Two-Way Doors)**:
  - *Characteristics*: Reversible, modular, low cutover cost (e.g. internal helper interfaces, logging format tweak, non-critical library dependency).
  - *Process Requirement*: Rapid evaluation, high bias for action, lightweight ADR documentation, iterative validation.

---

## 3. Canonical ADR Structure

Every ADR formulated under this skill must adhere to the following anatomy:

1. **Title & Status**:
   - Sequential identifier and descriptive title (e.g. `ADR-0012: In-Process SQLite State Storage`).
   - Status lifecycle: `Proposed`, `Accepted`, `Rejected`, `Superseded`, or `Deprecated`.

2. **Context & Problem Statement**:
   - The motivating technical challenge, business constraints, and forces at play.
   - Grounded in empirical realities, not abstract ideals.

3. **Decision Drivers**:
   - Key priorities driving selection (e.g. latency budgets, zero external operational dependencies, strict memory limits).

4. **Considered Options & Alternatives**:
   - Enumerate all evaluated architectures, including the rejected alternatives.
   - For each alternative, explicitly articulate why it was rejected.

5. **Decision Outcome**:
   - The chosen architectural path and its precise implementation boundaries.

6. **Consequences & Tradeoff Balance**:
   - **Positive**: Direct benefits and unlocked capabilities.
   - **Negative / Costs**: Incurred technical debt, operational friction, or performance tradeoffs.
   - **Neutral**: Secondary consequences that require ongoing monitoring.

---

## 4. Pre-Mortem & Tradeoff Quantification

An ADR is only as robust as its failure mode exploration:

- **The Pre-Mortem Exercise**: Assume it is 12 months after implementation and this architecture has completely failed. What caused the collapse? (e.g. schema migration complexity, unhandled concurrency, resource starvation).
- **Quantified Tradeoffs**: Where possible, quantify tradeoffs rather than relying on subjective adjectives (e.g. "Adds ~15ms round-trip latency in exchange for zero disk write contention").
