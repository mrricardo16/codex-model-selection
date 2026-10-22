# Automatic Model Routing Policy

Use this as a template. Merge it into existing user-level or project-level instructions; do not replace unrelated instructions.

These rules apply unless the user explicitly overrides the model, reasoning effort, delegation, or concurrency for the current task.

## Instruction priority

1. Explicit instructions in the current user request.
2. Applicable project-level instructions.
3. This shared routing policy.
4. Runtime-supported model and agent configuration.

## Objective

Choose the least costly route that can reliably complete and verify the task. Reliability and acceptance criteria come first; optimize for efficiency only among routes that can meet them.

Evaluate the requested outcome, uncertainty, business logic, module coupling, reversibility, consequences of failure, blast radius, and available verification. Do not route by file count, prompt length, tool count, or keywords alone.
Complexity alone is not a Route D trigger; use Astra only when concrete consequences or an evidenced capability gap justify the additional review.

## Route A — Direct

Use the primary thread for clear, low-risk, established-pattern work that can be verified directly. Examples include explanations, locating known code, mechanical edits, small DTO or mapping changes, and focused tests.

Do not delegate merely to appear thorough. If hidden complexity emerges before substantial editing, stop and reclassify.

## Route B — Routine engineering

Use `terra_builder` when the task needs substantive business-logic judgment or coordination across related components, but does not require deep technical investigation.

Follow existing patterns, keep the change minimal, and run focused validation.

## Route C — Complex engineering

Use `sol_engineer` for technically uncertain root causes, difficult debugging, cross-module behavior, nontrivial solution design, or substantial refactoring when the risk is bounded and the result can be verified.

Sol owns investigation, planning, implementation, and verification. Do not route to Astra merely because the task is large, architectural, or needs a written plan.

## Route D — High-risk review

Use `astra_critical` only when there is a concrete reason: significant plausible data loss, serious security exposure, production outage, an irreversible operation, a high-cost architectural decision that is hard to reverse, or evidence that Sol cannot reliably resolve a critical technical question.

Astra is advisory-first. Assign a narrow role such as plan review, risk assessment, architecture review, or read-only diff review. It must not silently take over implementation.

For a justified high-impact change:
1. Ask Astra to review the plan, assumptions, alternatives, acceptance criteria, validation, and rollback.
2. Release Astra after the report is returned.
3. If the plan is accepted, pass the review findings to Sol for implementation and verification.
4. Do not run Astra and Sol concurrently. Do not request both a plan review and final diff review by default; a second pass requires new material risk or a necessary independent check before a high-impact action.

## Escalation and concurrency

- Use at most one child agent at a time unless the user explicitly authorizes parallel work.
- Permit at most one automatic escalation per task. A deliberate Astra-plan-review → Sol-implementation handoff is allowed only when justified; do not add further model hops without new evidence or user direction.
- A failed build, test, tool, or environment alone is not evidence of a model capability gap. Diagnose it within the current route first.
- Do not loop between models. If a route remains blocked, report the blocker, evidence, and what remains unverified.
- Never automatically choose the maximum reasoning tier or raise reasoning above the agent's configured level.
- Reuse findings already gathered. Avoid duplicate investigation and unrelated refactoring.

## Safety and authorization

A routing decision is not authorization. Obtain explicit user approval before production writes, destructive SQL, data migrations, credential changes, or other irreversible actions. Do not expose credentials or personal data.

## Reporting

At the start of substantial work, state one concise route:

```text
Route: A — Direct
Route: B — Routine
Route: C — Complex
Route: D — High-risk review (name the assigned review role)
```

For code changes, report the actual route and agents used, changed files, validation commands and outcomes, unverified items, and remaining risks. Never claim a check passed unless it was run.
