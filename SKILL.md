---
name: model-selection
description: Choose a Codex model or subagent route using capability, uncertainty, impact, reversibility, and verification. Use before substantial work when deciding whether to act directly, delegate routine work, route complex engineering, or request high-risk review.
---

# Model Selection

Select the least costly route that can reliably complete and verify the requested task. Do not equate task complexity with risk, and do not delegate merely to appear thorough.

## Routing procedure

Before substantial work:

1. Honor explicit task-specific user instructions and applicable project instructions.
2. Identify the requested outcome, acceptance criteria, uncertainty, module coupling, consequences of failure, reversibility, and available verification.
3. Choose exactly one starting route. Do not make the user choose a route when the task gives enough information.
4. State the route briefly, then do the work and verify the result.

| Route | Use when | Default owner |
| --- | --- | --- |
| A — Direct | Clear, low-risk, established pattern, easy to verify. | Primary thread; no subagent. |
| B — Routine | Requires substantive business judgment or coordination across related components. | `terra_builder`. |
| C — Complex | Material technical uncertainty, difficult debugging, cross-module behavior, or a nontrivial design; impact remains bounded and verifiable. | `sol_engineer`. |
| D — High-risk review | Significant plausible impact, hard-to-reverse decisions, or concrete evidence of a critical capability gap. | `astra_critical`, advisory-first. |

## Non-negotiable rules

- Reliability comes before efficiency. When multiple routes can meet the acceptance criteria, prefer the less costly suitable route.
- Do not route from file count, prompt length, number of tools, or keywords alone.
- A database, security, or migration keyword is not by itself a Route D trigger.
- A normal build, test, tool, or environment failure is not by itself a reason to escalate.
- Use one child agent at a time. Do not run Astra and Sol concurrently on the same task.
- Allow at most one automatic escalation. Do not cycle through models when the selected route remains blocked; report the blocker and evidence.
- Astra's default role is plan review, risk assessment, architecture review, or read-only diff review—not implementation.
- For justified high-impact work, Astra may review a plan first. Release that agent before handing the accepted plan to Sol. Do not add a second Astra review by default.
- Selecting a high-risk route does not authorize production writes, destructive SQL, data migrations, credential changes, or other irreversible operations. Obtain explicit user authorization where required.
- Do not claim a model or subagent was used unless the runtime actually invoked it.

## Expected routing line

At the start of substantial work, use one concise line such as:

- `Route: A — Direct`
- `Route: B — Routine`
- `Route: C — Complex`
- `Route: D — High-risk review (plan review)`

For Route D, name the narrow role: plan, risk assessment, architecture review, read-only diff review, or explicitly authorized implementation.

## References

- Read [the routing policy](references/routing-policy.md) for decision criteria and escalation behavior.
- Read [installation notes](references/installation.md) before copying this package into a Codex setup.
- Use [the regression prompts](references/test-cases.md) to test routing changes.
- The TOML files in `agents/` are examples. Model IDs and reasoning-effort values must match the runtime that loads them.
