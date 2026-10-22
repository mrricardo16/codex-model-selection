# Routing Policy

## Decision sequence

### 1. Honor explicit constraints

The current user's explicit task-specific instructions override automatic routing where safe and possible. Respect project-level instructions and the runtime's actual model/agent availability. Never claim to have used an agent that was not invoked.

### 2. Assess the task, not its appearance

Before selecting a route, identify:

- **Outcome:** What observable result is requested?
- **Uncertainty:** Is the relevant implementation path understood, or is root-cause discovery required?
- **Judgment:** Are there business rules or architectural trade-offs not already established by the codebase?
- **Coupling:** Does the change cross modules, data contracts, or runtime boundaries?
- **Impact:** What happens if the solution is wrong?
- **Reversibility:** Can the change be rolled back safely?
- **Verification:** Can focused tests, builds, logs, diffs, or direct inspection establish correctness?

File count, prompt length, number of tools, and keywords are not independent routing criteria.

### 3. Choose the least costly reliable route

| Route | Positive signals | Do not choose it merely because |
| --- | --- | --- |
| A — Direct | Clear request, established pattern, low impact, direct verification. | The task has a few files or is phrased briefly. |
| B — Routine | Business logic needs judgment; related components must be coordinated; established architecture remains suitable. | The diff spans multiple files without meaningful design uncertainty. |
| C — Complex | Root cause is unclear, behavior crosses modules, technical uncertainty is substantial, or focused investigation and a nontrivial plan are needed. | The task is long or the agent would make the answer look more thorough. |
| D — High-risk review | A mistake could have significant consequences, a decision is difficult to reverse, or a critical capability gap is supported by evidence. | The task mentions security, a database, a migration, production, or architecture without a concrete risk analysis. |

A complex task may still be low risk if its scope is reversible and it has a credible verification path. Start with Route C in that case.

## Route D role boundaries

Astra's default assignment is advisory:

- **Plan review:** challenge assumptions, alternatives, acceptance criteria, validation, rollback, and operational dependencies.
- **Risk assessment:** identify credible failure modes and prioritize mitigations.
- **Architecture review:** assess a high-cost decision that is difficult to reverse.
- **Diff review:** inspect a completed change read-only and cite specific evidence.

Implementation is exceptional. It requires an explicit user request or a concrete explanation from the parent that lower-cost routes cannot implement the change reliably.

## Staged high-impact workflow

When independent planning review materially reduces risk:

1. Have Astra review or produce the plan without changing code or executing operations.
2. Capture findings, unresolved assumptions, acceptance criteria, validation, and rollback.
3. Release Astra before starting another agent.
4. Pass the accepted plan to Sol for implementation and verification.
5. Use one Astra engagement by default. A second review is justified only by newly discovered material risk or a necessary independent check before a high-impact action.

Do not run Astra and Sol concurrently on the same task. A review is not authorization to perform production writes or irreversible operations.

## Escalation rules

- Allow at most one automatic escalation per task.
- Escalate from routine to complex only when evidence shows material technical uncertainty beyond the current route.
- Escalate to high-risk review only when there is a concrete consequence or capability gap.
- A normal build/test/tool/environment failure is not by itself an escalation reason.
- If a route remains blocked, report what was tried, the evidence, and what cannot be verified. Do not cycle through more models automatically.

## Expected evidence in a routing decision

A good route selection should be explainable in one or two sentences. For example:

> Route C — Complex: the failure crosses transaction and event-handling boundaries, the root cause is not yet known, and a focused integration test can verify the fix. No evidence currently suggests an irreversible or production-level risk that requires Route D.

Do not write a long routing justification for ordinary tasks.
