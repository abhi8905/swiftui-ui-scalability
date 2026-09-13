#!/usr/bin/env python3
"""Validate this dependency-free Agent Skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter", errors)
        return {}

    try:
        closing = text.index("\n---\n", 4)
    except ValueError:
        fail("SKILL.md frontmatter is not closed", errors)
        return {}

    values: dict[str, str] = {}
    for line in text[4:closing].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            fail(f"Unsupported frontmatter line: {line}", errors)
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def check_links(errors: list[str]) -> int:
    checked = 0
    for markdown_file in sorted(ROOT.rglob("*.md")):
        content = markdown_file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(content):
            raw_target = match.group(1).strip()
            target = raw_target.split(maxsplit=1)[0].strip("<>\"'")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            relative_target = unquote(target.split("#", 1)[0])
            if not relative_target:
                continue
            checked += 1
            resolved = (markdown_file.parent / relative_target).resolve()
            if not resolved.exists():
                fail(
                    f"Broken relative link in {markdown_file.relative_to(ROOT)}: {target}",
                    errors,
                )
    return checked


def main() -> int:
    errors: list[str] = []
    if not SKILL.is_file():
        fail("Missing SKILL.md", errors)
        skill_text = ""
    else:
        skill_text = SKILL.read_text(encoding="utf-8")

    metadata = frontmatter(skill_text, errors) if skill_text else {}
    allowed_keys = {"name", "description"}
    unexpected = set(metadata) - allowed_keys
    if unexpected:
        fail(f"Unexpected SKILL.md frontmatter keys: {sorted(unexpected)}", errors)

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != ROOT.name:
        fail(f"Skill name '{name}' must match directory '{ROOT.name}'", errors)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("Skill name must use lowercase letters, numbers, and hyphens", errors)
    if not description:
        fail("Skill description is required", errors)
    elif len(description) > 1024:
        fail("Skill description exceeds 1024 characters", errors)

    if len(skill_text.splitlines()) > 500:
        fail("SKILL.md exceeds the 500-line authoring limit", errors)

    required_paths = [
        ROOT / "README.md",
        ROOT / "INSTALL.md",
        ROOT / "PUBLISHING.md",
        ROOT / ".github" / "workflows" / "validate.yml",
        ROOT / "agents" / "openai.yaml",
        ROOT / "references" / "layout-decisions.md",
        ROOT / "references" / "geometry-and-scrolling.md",
        ROOT / "references" / "accessibility-and-state.md",
        ROOT / "references" / "validation.md",
        ROOT / "references" / "sources.md",
    ]
    for required_path in required_paths:
        if not required_path.is_file():
            fail(f"Missing required file: {required_path.relative_to(ROOT)}", errors)

    private_user = "abhi"
    forbidden_fragments = (
        "/Use" + f"rs/{private_user}/",
        "/Use" + f"rs/{private_user}\\",
        "Python" + " Raw Data",
    )
    text_files = [*ROOT.rglob("*.md"), *ROOT.rglob("*.yaml"), *ROOT.rglob("*.py")]
    for text_file in text_files:
        content = text_file.read_text(encoding="utf-8")
        for fragment in forbidden_fragments:
            if fragment in content:
                fail(
                    f"Private local path fragment in {text_file.relative_to(ROOT)}: {fragment}",
                    errors,
                )

    openai_yaml = ROOT / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        interface_text = openai_yaml.read_text(encoding="utf-8")
        if f"${name}" not in interface_text:
            fail("agents/openai.yaml default_prompt must mention the skill as $name", errors)

    workflow = ROOT / ".github" / "workflows" / "validate.yml"
    if workflow.is_file() and "python3 scripts/validate_skill.py" not in workflow.read_text(
        encoding="utf-8"
    ):
        fail("GitHub workflow must run the portable validator", errors)

    checked_links = check_links(errors)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill validation passed: {name}")
    print(f"Checked {len(text_files)} text files and {checked_links} relative links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
