# Installation and Customization

Codex configuration paths and custom-agent schemas can vary by version and deployment. Verify the paths recognized by your installed runtime before copying files. This repository intentionally does not assume that every folder here is auto-discovered.

## 1. Install the skill

Copy this package's `SKILL.md` and its `references/` directory into a skill folder recognized by your Codex version.

Common patterns include:

- Repository-local skill: `.agents/skills/model-selection/`
- User-level skill: a `skills/model-selection` directory under your configured Codex home

Keep the directory name and the frontmatter `name` consistent. If your runtime requires additional skill metadata, add it according to that runtime's documentation.

## 2. Merge the routing policy

Review `templates/AGENTS.md` and merge the relevant sections into the applicable global or project instructions.

Do not replace an existing `AGENTS.md` wholesale without reviewing its other responsibilities. In particular:

- Preserve existing project constraints and security rules.
- Keep a single authoritative model-routing policy where possible.
- Avoid conflicting route tables in multiple skills.
- Make the precedence between user instructions, project instructions, and shared routing rules explicit.

## 3. Configure custom agents

The `agents/` directory contains example TOML definitions for three roles:

- `terra_builder`: routine implementation
- `sol_engineer`: complex investigation and implementation
- `astra_critical`: high-risk planning and review

Copy them into the custom-agent directory supported by your Codex installation. Do not assume the repository's `agents/` folder is automatically loaded.

Before use, verify:

- The TOML keys and agent file location are supported by your installed version.
- Each `model` identifier exists in your runtime.
- The configured reasoning-effort value is accepted by that model.
- The agent names match the names used by the routing policy.

The included model IDs are examples from one configuration, not a guarantee of availability in every environment.

## 4. Validate and smoke-test

Run the package validator:

```bash
python scripts/validate_package.py
```

Then restart Codex if required by your configuration and open a fresh conversation. Use the examples in [test-cases.md](test-cases.md) to confirm both positive and negative routing behavior.

Check that:

- Low-risk work remains in the primary thread.
- Routine work uses the routine agent only when it needs substantive judgment.
- Complex but verifiable work routes to the complex agent rather than automatically to Astra.
- Astra is used only for a concrete high-risk review or evidenced capability gap.
- Astra and Sol are not running concurrently on the same task.
- Explicit user instructions are respected.

## 5. Update safely

When changing the policy, update the skill, the copy-ready template, and regression cases together. Run the validator and inspect the diff before publishing. Keep model-specific settings in the agent configuration rather than duplicating them across multiple policy files.
