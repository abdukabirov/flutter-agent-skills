#!/usr/bin/env python3
"""Validate every skill under skills/. Exits with code 1 if any check fails.

Checks per skill:
  - skills/<name>/SKILL.md exists
  - YAML frontmatter parses and has `name` and `description`
  - `name` is lowercase-hyphen, <= 64 chars, and equals the folder name
  - `description` starts with "Use when" and is <= 300 chars
  - code fences are balanced
  - file length (warning above 300 lines, error above 500)
  - the skill is linked from README.md
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 300
WARN_LINES = 300
MAX_LINES = 500


def parse_frontmatter(text: str) -> dict:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("file must start with a '---' frontmatter block")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed with '---'")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data


def check_skill(skill_dir: Path, readme_text: str):
    errors, warnings = [], []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"], warnings

    text = skill_file.read_text(encoding="utf-8")
    try:
        meta = parse_frontmatter(text)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"{skill_dir.name}: bad frontmatter: {exc}"], warnings

    name = meta.get("name")
    desc = meta.get("description")

    if not isinstance(name, str) or not name:
        errors.append(f"{skill_dir.name}: frontmatter needs a `name`")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{skill_dir.name}: name '{name}' must be lowercase letters, digits and hyphens")
        if len(name) > MAX_NAME:
            errors.append(f"{skill_dir.name}: name is longer than {MAX_NAME} characters")
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: name '{name}' must match the folder name")

    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{skill_dir.name}: frontmatter needs a `description`")
    else:
        desc = " ".join(desc.split())
        if not desc.startswith("Use when"):
            errors.append(f"{skill_dir.name}: description must start with 'Use when'")
        if len(desc) > MAX_DESC:
            errors.append(f"{skill_dir.name}: description is {len(desc)} chars, max {MAX_DESC}")

    fences = sum(1 for line in text.splitlines() if line.lstrip().startswith("```"))
    if fences % 2:
        errors.append(f"{skill_dir.name}: unbalanced ``` code fences")

    lines = len(text.splitlines())
    if lines > MAX_LINES:
        errors.append(f"{skill_dir.name}: {lines} lines, max {MAX_LINES} (move detail into references/)")
    elif lines > WARN_LINES:
        warnings.append(f"{skill_dir.name}: {lines} lines, consider moving detail into references/")

    if f"skills/{skill_dir.name}/SKILL.md" not in readme_text:
        errors.append(f"{skill_dir.name}: not linked from README.md skills table")

    return errors, warnings


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("skills/ directory not found")
        return 1

    readme_text = README.read_text(encoding="utf-8") if README.is_file() else ""
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print("no skills found")
        return 1

    all_errors, all_warnings = [], []
    for skill_dir in skill_dirs:
        errors, warnings = check_skill(skill_dir, readme_text)
        all_errors += errors
        all_warnings += warnings

    for w in all_warnings:
        print(f"warning: {w}")
    for e in all_errors:
        print(f"error: {e}")

    if all_errors:
        print(f"\n{len(all_errors)} error(s) in {len(skill_dirs)} skill(s)")
        return 1
    print(f"OK: {len(skill_dirs)} skill(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
