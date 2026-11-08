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
# Top-level keys defined by the Agent Skills specification.
PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKIPPED_PARTS = {".git", "dist", "__pycache__"}
LINK_PATTERN = re.compile(r"\[[^]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CREDENTIAL_PATTERNS = [
    re.compile(r"(?i)\bbearer\s+(?!\$)[A-Za-z0-9._~+/-]{20,}"),
    re.compile(r"(?i)(see_api_key|api[_-]?key|authorization)[\"']?\s*[:=]\s*[\"']?(?!bearer\b|\$|\.\.\.)[A-Za-z0-9_-]{20,}"),
]


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must begin with YAML frontmatter")
    match = re.match(r"---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter is not closed")
    block = match.group(1)
    values: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([a-z][a-z0-9-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"\'')
    return values


def heading_anchors(path: Path) -> set[str]:
    """Return GitHub-style heading anchors, ignoring fenced code blocks."""
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        heading = None if in_fence else re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not heading:
            continue
        slug = re.sub(r"[^\w\- ]", "", heading.group(1).strip().lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def iter_files(pattern: str) -> list[Path]:
    return sorted(
        path for path in ROOT.rglob(pattern)
        if path.is_file() and not SKIPPED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def validate_links() -> None:
    for source in iter_files("*.md"):
        text = re.sub(r"^```.*?^```", "", source.read_text(encoding="utf-8"), flags=re.MULTILINE | re.DOTALL)
        for link in LINK_PATTERN.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", link, flags=re.IGNORECASE):
                continue
            target, _, anchor = link.partition("#")
            resolved = (source.parent / target).resolve() if target else source.resolve()
            if not resolved.is_file():
                fail(f"broken link in {source.relative_to(ROOT)}: {link}")
            if source.is_relative_to(SKILL) and not resolved.is_relative_to(SKILL):
                fail(f"skill link leaves the skill directory in {source.relative_to(ROOT)}: {link}")
            if anchor and resolved.suffix == ".md" and anchor not in heading_anchors(resolved):
                fail(f"broken anchor in {source.relative_to(ROOT)}: {link}")


def validate_skill() -> None:
    text = SKILL_MD.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    name = metadata.get("name", "")
    if name != SKILL.name:
        fail("skill name must match its directory")
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        fail("skill name must be 1..64 lowercase letters, digits, and single hyphens")
    description = metadata.get("description", "")
    if description[:1] in {">", "|"}:
        fail("description must be a single-line string")
    if not description or len(description) > 1024:
        fail("description must contain 1..1024 characters")
    if len(metadata.get("compatibility", "")) > 500:
        fail("compatibility must contain at most 500 characters")
    unexpected = set(metadata) - PORTABLE_KEYS
    if unexpected:
        fail(f"non-portable frontmatter keys: {sorted(unexpected)}")


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
        SKILL_MD,
        API_REFERENCE,
        SKILL / "references" / "cli.md",
        SKILL / "references" / "sdks.md",
        SKILL / "references" / "safety.md",
        SKILL / "references" / "examples.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail(f"missing required files: {missing}")

def validate_credentials() -> None:
    for path in iter_files("*"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in CREDENTIAL_PATTERNS):
            fail(f"possible credential in {path.relative_to(ROOT)}")


def main() -> None:
    validate_repository()
    validate_skill()
    validate_links()
    validate_api_reference()
    validate_cli_reference()
    validate_sdk_reference()
    validate_credentials()
    print("skill validation passed")


if __name__ == "__main__":
    main()
