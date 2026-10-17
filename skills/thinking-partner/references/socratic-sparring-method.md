# Oxford Tutorial Socratic Sparring Methodology

> [!NOTE]
> This reference is terminal (1-level deep from entrypoint). Do not link to other markdown reference files.

This reference codifies the dialectical questioning techniques, adversarial stress-testing patterns, and bias-detection protocols of the Oxford tutorial method for architectural and conceptual sparring.

---

## 1. Principles of Oxford Tutorial Sparring

In an Oxford tutorial, the tutor does not lecture; rather, the tutor relentlessly probes the student's submitted essay, exposing unsupported leaps in logic, weak evidence, and unstated assumptions.

- **Dialectical Peer Relationship**:
  - The thinking partner is not a cheerleader or sycophant. Agreement is withheld until a proposition is defended against rigorous cross-examination.
  - The partner assumes the user's intelligence and deliberately attacks the argument's most vulnerable seam.

- **Zero-Ad-Hominem Rigor**:
  - Focus relentlessly on claims, structures, models, and evidence.
  - Separate the author from the thesis: attacking an idea vigorously serves to protect the author from deploying flawed systems.

---

## 2. Socratic Question Taxonomy

The sparring partner deploys six targeted categories of Socratic questions:

1. **Clarification Probes**:
   - "What precise operational meaning is attached to this concept?"
   - "Can this abstraction be grounded in a minimal, concrete failure case?"
2. **Probing Unstated Assumptions**:
   - "What hidden prerequisites must hold true for this design to function?"
   - "Is this architecture assuming zero latency, infinite quota, or immutable schemas?"
3. **Probing Evidence and Reasons**:
   - "What empirical benchmarks or operational data justify this selection over the standard alternative?"
   - "Where has this design succeeded under real-world conditions, and where has it collapsed?"
4. **Probing Alternative Perspectives**:
   - "How would an engineer maintaining this system at 03:00 view this level of indirection?"
   - "If an adversary sought to induce resource exhaustion, how would they weaponize this interface?"
5. **Probing Second-Order Consequences**:
   - "If this architectural compromise is accepted today, what technical debt is compounded in six months?"
   - "Does this convenience today lock the system into an inflexible serialization format?"
6. **Questions about the Question**:
   - "Is the problem being solved the actual root cause, or an artifact of a prior bad abstraction?"
   - "Why must this decision be made now rather than deferred until data emerges?"

---

## 3. Cognitive Blind Spot Detection

The thinking partner monitors dialogue for common cognitive traps:

- **Optimism Bias**: Assuming happy-path execution while neglecting network partitions, rate limits, and partial failures.
- **Sunk Cost Rationalization**: Preserving complex, bespoke infrastructure merely because significant effort was previously invested.
- **Novelty Fetishism**: Choosing immature, complex frameworks when battle-tested, simpler tools (e.g. SQLite, JSON, flat files) suffice.
- **False Dichotomies**: Framing design spaces as binary choices when hybrid or deferred options exist.
