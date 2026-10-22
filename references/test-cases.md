# Routing Regression Cases

Use these prompts in a fresh Codex conversation after installing the policy. Check the actual route and agent invocations, not just the wording of the answer.

| ID | Expected route | What this tests |
| --- | --- | --- |
| A1 | Route A — Direct | Read-only explanation with a sensitive-sounding keyword. |
| A2 | Route A — Direct | Small established-pattern change. |
| B1 | Route B — Routine | Business logic across related components. |
| C1 | Route C — Complex | Uncertain root cause with bounded impact and a verification path. |
| C2 | Route C — Complex | Reversible cross-module refactor. |
| D1 | Route D — High-risk review | Production data migration plan needs independent risk review. |
| D2 | Route D — High-risk review | A high-impact security design decision is hard to reverse. |
| N1 | Route A — Direct | Explicit no-delegation instruction. |
| N2 | Stay on current route | Build failure alone must not trigger model escalation. |

## A1 — Keyword is not enough

> Explain what a JWT 401 response means. Do not change code or authentication settings.

Expected: Route A. This is read-only explanation; the word “authentication” does not imply a high-risk action.

## A2 — Established pattern

> Following the existing DTO pattern, add a CreateRoleDto and run the narrowest relevant build or test.

Expected: Route A. The request is bounded, pattern-following, and directly verifiable.

## B1 — Routine business implementation

> Add a paginated order-search endpoint with two explicit business filters. Coordinate the Controller, Service, and EF Core query using the existing architecture, and add focused tests.

Expected: Route B when the business logic is clear and no deeper technical uncertainty exists.

## C1 — Uncertain root cause

> An API intermittently returns success but the corresponding record is missing. Trace the transaction and event flow, identify the root cause, implement the smallest safe fix, and add a regression test. There is no evidence of production data loss.

Expected: Route C. Root-cause discovery and cross-component reasoning are required, but the stated evidence does not justify Route D by itself.

## C2 — Complex but reversible

> Refactor the existing feature across several modules. First define acceptance criteria and the minimal implementation plan, then implement and run focused regression tests. The change is reversible and has no known production impact.

Expected: Route C. Task complexity and file count alone are not reasons to choose Route D.

## D1 — High-impact plan review

> Review a proposed production database migration for data-loss, locking, compatibility, downtime, and rollback risks. Produce assumptions, alternatives, acceptance criteria, and a validation/rollback plan. Do not edit code or execute database operations.

Expected: Route D with Astra in advisory/read-only plan-review mode. If the plan is accepted, release Astra and hand it to Sol for implementation only when implementation is requested and appropriate.

## D2 — Hard-to-reverse security design

> Independently review this proposed authentication and authorization architecture before rollout. The decision is expensive to reverse and a defect could expose tenant data. Do not change files; identify concrete attack paths, assumptions, mitigations, and validation requirements.

Expected: Route D with a scoped architecture/risk review.

## N1 — Explicit user override

> Do not delegate this task. Inspect the provided diff and summarize any obvious formatting issues only.

Expected: Route A, provided the task remains within scope and safe to perform directly. Do not spawn a subagent just to satisfy the default route table.

## N2 — Failure is not an escalation trigger

> A focused unit test fails because a local dependency is unavailable. Diagnose the environment issue and report what can and cannot be verified.

Expected: Stay on the current route. A tool or environment failure is not evidence that a stronger model is needed. Escalate only if investigation reveals a genuine capability gap or material risk.

## Acceptance checklist

- [ ] Route A tasks do not spawn a child agent.
- [ ] Route B tasks use the routine agent only when judgment/coordination warrants it.
- [ ] Complex but verifiable work starts with Route C.
- [ ] Route D includes a concrete consequence or capability-gap rationale.
- [ ] Astra review is scoped and advisory by default.
- [ ] Astra and Sol do not run concurrently on the same task.
- [ ] No automatic model loop occurs after a failed tool or build.
- [ ] Explicit user constraints take precedence.
