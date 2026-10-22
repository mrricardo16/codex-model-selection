# Codex Model Selection

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Validation](https://github.com/mrricardo16/codex-model-selection/actions/workflows/validate.yml/badge.svg)](https://github.com/mrricardo16/codex-model-selection/actions/workflows/validate.yml)

A policy-first model and subagent routing skill for Codex. It selects the **least costly route that can reliably complete and verify the task**, rather than treating every complex request as a reason to use the strongest model.

The package combines a reusable `SKILL.md`, a copy-ready routing policy, example custom-agent TOML files, regression prompts, and a lightweight package validator.

## Why this exists

Model routing is a decision about **capability, uncertainty, impact, and verification**—not a keyword lookup.

- Keep small, clear, reversible work in the primary thread.
- Delegate routine engineering only when it needs substantive business judgment or coordination.
- Use the complex-engineering agent for uncertain, cross-cutting, or difficult-to-reproduce work when the outcome is still bounded and verifiable.
- Reserve the high-reasoning agent for material risk, hard-to-reverse decisions, or a demonstrated capability gap.
- Make high-risk review advisory by default; do not let a review agent silently take over implementation.
- Prevent agent churn with one-child-at-a-time execution and a bounded escalation policy.

## Routing model

| Route | Choose it when | Default responsibility |
| --- | --- | --- |
| **A — Direct** | The task is clear, low-risk, follows an established pattern, and can be checked directly. | The primary thread implements or answers without delegation. |
| **B — Routine** | The task needs business-logic judgment or coordination across related components, but not deep technical investigation. | A routine engineering agent implements and runs focused checks. |
| **C — Complex** | The task has material technical uncertainty, a difficult root cause, cross-module behavior, or a nontrivial design—but can be verified and kept reversible. | A complex engineering agent investigates, plans, implements, and verifies. |
| **D — High-risk review** | An error could cause significant data loss, security exposure, production outage, irreversible change, or a costly architectural mistake; or a critical capability gap is evidenced. | A high-reasoning agent provides a scoped plan, risk review, or read-only diff review. |

**Complexity is not the same as risk.** A long task, many files, a database keyword, a security keyword, or a failed build does not independently justify Route D.

The included TOML files demonstrate one model mapping. Model IDs and reasoning-effort values are runtime-dependent; replace them with identifiers supported by your Codex setup.

## Design principles

1. **Reliability first, efficiency second.** Select the least costly route that can meet the acceptance criteria and verify the result.
2. **Route from evidence.** Consider uncertainty, coupling, business rules, reversibility, blast radius, and available validation. Do not route by prompt length, file count, tool count, or keywords alone.
3. **Explicit instructions win.** Honor the user's task-specific routing instructions, then applicable project instructions, then the shared routing policy.
4. **Astra is advisory-first.** Use it for the specific decision or review that warrants it. Direct implementation is exceptional and needs an explicit request or a documented reason that lower-cost routes cannot implement reliably.
5. **Sequential handoff, never concurrent duplication.** For justified high-impact work, Astra may review the plan first; release it before handing the accepted plan to the complex agent. Do not run both against the same implementation at once.
6. **Bound escalation.** A normal tool, build, test, or environment failure is not itself a model-escalation reason. Avoid model loops and repeated reviews without new evidence.
7. **Risk review is not authorization.** Selecting a high-risk agent does not authorize production writes, destructive SQL, migrations, credential changes, or other irreversible actions.

## Repository layout

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CHANGELOG.md
├── agents/
│   ├── terra_builder.toml
│   ├── sol_engineer.toml
│   └── astra_critical.toml
├── references/
│   ├── routing-policy.md
│   ├── installation.md
│   └── test-cases.md
├── templates/
│   └── AGENTS.md
└── scripts/
    └── validate_package.py
```

## Quick start

1. Read [SKILL.md](SKILL.md) and [the routing policy](references/routing-policy.md).
2. Install the skill folder in a skill location recognized by your Codex version. For a repository-local setup, this is commonly `.agents/skills/model-selection/`; for a user-level setup, use the skill directory under your configured Codex home.
3. Merge [`templates/AGENTS.md`](templates/AGENTS.md) into your user-level or project-level instructions. Do not blindly overwrite existing instructions.
4. Copy the TOML files from `agents/` into the custom-agent directory used by your Codex installation. Verify the supported path and schema for your installed version.
5. Edit each agent's `model` and `model_reasoning_effort` to match models actually available in your environment.
6. Restart Codex if required by your setup, start a fresh conversation, and run the scenarios in [test-cases.md](references/test-cases.md).

See [installation notes](references/installation.md) for more detail.

## Validate the package

Requires Python 3.11 or later. No third-party Python packages are needed.

```bash
python scripts/validate_package.py
```

The validator checks the skill metadata, required package files, agent TOML syntax and key fields, and the presence of routing regression cases. GitHub Actions runs the same check on pushes and pull requests.

## What this project does not do

- It does not dynamically switch the model of an already-running primary thread.
- It does not guarantee that every named model or custom-agent field is available in every Codex release.
- It does not replace task-specific instructions, project policies, tests, or human approval for high-impact actions.
- It does not require Astra to review every plan or every completed diff.
- It does not assume parallel agents improve quality.

## Contributing

Issues and pull requests are welcome. Please include the intended behavior, a representative routing scenario, and the evidence used to validate the change. Changes to routing policy should add or update regression prompts in `references/test-cases.md`.

## License

MIT. See [LICENSE](LICENSE).
