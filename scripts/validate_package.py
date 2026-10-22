#!/usr/bin/env python3
"""Validate the model-selection skill package without third-party dependencies."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def require_file(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        ERRORS.append(f"Missing required file: {relative_path}")
        return ""
    return path.read_text(encoding="utf-8")


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def main() -> int:
    required = [
        "README.md",
        "README.zh-CN.md",
        "SKILL.md",
        "LICENSE",
        "CHANGELOG.md",
        "templates/AGENTS.md",
        "references/routing-policy.md",
        "references/installation.md",
        "references/test-cases.md",
        "agents/terra_builder.toml",
        "agents/sol_engineer.toml",
        "agents/astra_critical.toml",
        ".github/workflows/validate.yml",
    ]
    for item in required:
        require_file(item)

    skill = require_file("SKILL.md")
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", skill, re.DOTALL)
    check(frontmatter is not None, "SKILL.md must start with YAML frontmatter.")
    if frontmatter:
        metadata = {}
        for line in frontmatter.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip("'\"")
        check(metadata.get("name") == "model-selection", "SKILL.md frontmatter name must be model-selection.")
        check(bool(metadata.get("description")), "SKILL.md frontmatter must include a description.")

    expected_agents = {
        "terra_builder.toml": "terra_builder",
        "sol_engineer.toml": "sol_engineer",
        "astra_critical.toml": "astra_critical",
    }
    for filename, expected_name in expected_agents.items():
        relative = f"agents/{filename}"
        content = require_file(relative)
        if not content:
            continue
        try:
            config = tomllib.loads(content)
        except tomllib.TOMLDecodeError as exc:
            ERRORS.append(f"Invalid TOML in {relative}: {exc}")
            continue
        check(config.get("name") == expected_name, f"{relative}: unexpected or missing name.")
        check(bool(config.get("model")), f"{relative}: model is required.")
        check(bool(config.get("model_reasoning_effort")), f"{relative}: model_reasoning_effort is required.")
        check(bool(config.get("developer_instructions")), f"{relative}: developer_instructions is required.")
        check(bool(config.get("description")), f"{relative}: description is required.")

    policy = require_file("templates/AGENTS.md").lower()
    for phrase in (
        "least costly route",
        "complexity alone",
        "one child agent at a time",
        "do not run astra and sol concurrently",
        "explicit user approval",
    ):
        check(phrase in policy, f"Routing template is missing required policy: {phrase!r}")

    cases = require_file("references/test-cases.md")
    for route in ("Route A", "Route B", "Route C", "Route D"):
        check(route in cases, f"Regression cases must cover {route}.")

    if ERRORS:
        print("Package validation: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("Package validation: PASS")
    print(f"Validated {len(required)} required files and {len(expected_agents)} agent TOML files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
