#!/usr/bin/env python3
"""Validate the S.EE Agent Skill without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "see"
SKILL_MD = SKILL / "SKILL.md"
API_REFERENCE = SKILL / "references" / "api.md"
CLI_REFERENCE = SKILL / "references" / "cli.md"
SDK_REFERENCE = SKILL / "references" / "sdks.md"
HTTP_METHODS = {"GET", "PUT", "POST", "DELETE", "PATCH", "HEAD", "OPTIONS"}


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

    for source in SKILL.rglob("*.md"):
        for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
            target = link.split("#", 1)[0]
            if target and "://" not in target and not (source.parent / target).is_file():
                fail(f"broken link in {source.relative_to(ROOT)}: {link}")


def validate_api_reference() -> None:
    text = API_REFERENCE.read_text(encoding="utf-8")
    operations = re.findall(r"^### `([A-Z]+) ([^`]+)`$", text, flags=re.MULTILINE)
    if not operations:
        fail("API reference contains no operations")
    invalid = [(method, path) for method, path in operations if method not in HTTP_METHODS or not path.startswith("/")]
    if invalid:
        fail(f"invalid API operations: {invalid}")
    if len(operations) != len(set(operations)):
        fail("API reference contains duplicate operations")
    for required in ("https://s.ee", "/api/v1", "Authorization: Bearer $SEE_API_KEY"):
        if required not in text:
            fail(f"API reference is missing {required!r}")
    print(f"validated {len(operations)} API operations")


def validate_cli_reference() -> None:
    text = CLI_REFERENCE.read_text(encoding="utf-8")
    commands = re.findall(r"^see (?:[a-z][a-z0-9-]*)(?: [^\n]+)?$", text, flags=re.MULTILINE)
    if not commands:
        fail("CLI reference contains no commands")
    if not any("--json" in command for command in commands):
        fail("CLI reference does not document JSON output")
    for section in ("Short URLs", "Text Sharing", "Files", "Bio Pages", "QR Codes", "Result Handling"):
        if f"## {section}" not in text:
            fail(f"CLI reference is missing the {section!r} section")
    print(f"validated {len(commands)} CLI commands")


def validate_sdk_reference() -> None:
    text = SDK_REFERENCE.read_text(encoding="utf-8")
    repositories = re.findall(r"https://github\.com/sdotee/(sdk\.[a-z]+)", text)
    if not repositories:
        fail("SDK reference contains no official repositories")
    if len(repositories) != len(set(repositories)):
        fail("SDK reference contains duplicate repositories")
    if "## Integration Rules" not in text or "SEE_API_KEY" not in text:
        fail("SDK reference is missing integration or credential guidance")
    print(f"validated {len(repositories)} SDK repositories")


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
    validate_cli_reference()
    validate_sdk_reference()
    validate_repository()
    print("skill validation passed")


if __name__ == "__main__":
    main()
