#!/usr/bin/env python3
"""Validate the S.EE Agent Skill without network access."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "see"
SKILL_MD = SKILL / "SKILL.md"
API_REFERENCE = SKILL / "references" / "api.md"
SPEC = ROOT / "see_api_doc.json"
HTTP_METHODS = {"get", "put", "post", "delete", "patch", "head", "options"}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must begin with YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        fail("SKILL.md frontmatter is not closed")
    values: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([a-z][a-z0-9-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"\'')
    return values


def validate_skill() -> None:
    text = SKILL_MD.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    if metadata.get("name") != SKILL.name:
        fail("skill name must match its directory")
    if not metadata.get("description") or len(metadata["description"]) > 1024:
        fail("description must contain 1..1024 characters")
    allowed = {"name", "description", "license", "compatibility", "metadata", "author", "version", "homepage"}
    unexpected = set(metadata) - allowed
    if unexpected:
        fail(f"non-portable frontmatter keys: {sorted(unexpected)}")

    for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if "://" not in link and not (SKILL / link).is_file():
            fail(f"broken SKILL.md link: {link}")


def validate_api_reference() -> None:
    with SPEC.open(encoding="utf-8") as source:
        spec = json.load(source)
    if spec.get("swagger") != "2.0":
        fail("see_api_doc.json must be Swagger 2.0")
    expected = {
        (method.upper(), path)
        for path, path_item in spec.get("paths", {}).items()
        for method in path_item
        if method.lower() in HTTP_METHODS
    }
    generated = API_REFERENCE.read_text(encoding="utf-8")
    actual = set(re.findall(r"^### `([A-Z]+) ([^`]+)`$", generated, flags=re.MULTILINE))
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        fail(f"API reference mismatch; missing={missing}, extra={extra}")
    print(f"validated {len(actual)} API operations")


def validate_repository() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        SKILL / "references" / "cli.md",
        SKILL / "references" / "sdks.md",
        SKILL / "references" / "safety.md",
        SKILL / "references" / "examples.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail(f"missing required files: {missing}")
    token_pattern = re.compile(r"(?i)(see_api_key|authorization)\s*[:=]\s*['\"]?(?!bearer|\.\.\.)[A-Za-z0-9_-]{20,}")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "dist" in path.parts:
            continue
        if path.suffix not in {".md", ".json", ".py", ".sh"}:
            continue
        if token_pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            fail(f"possible credential in {path.relative_to(ROOT)}")


def main() -> None:
    validate_skill()
    validate_api_reference()
    validate_repository()
    print("skill validation passed")


if __name__ == "__main__":
    main()
