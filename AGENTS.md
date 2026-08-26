# Agent Guide

This repository packages the S.EE integration guidance as a portable Agent Skill. Read [README.md](README.md) for the project layout and [CONTRIBUTING.md](CONTRIBUTING.md) for source priority and contribution policy.

## Commands

- `make generate`: regenerate the REST reference from the Swagger source.
- `make check`: regenerate and run all offline validation. Run this after every source or documentation change.
- `make package`: validate and create `dist/see-agent-skill.zip`.
- `make clean`: remove generated build artifacts and Python bytecode.

The scripts use Python's standard library. Do not add dependencies unless the task requires them.

## Source Boundaries

- [see_api_doc.json](see_api_doc.json) is the source of truth for REST paths, request fields, and response schemas.
- [.claude/skills/see/references/api.md](.claude/skills/see/references/api.md) is generated. Never edit it directly; update the Swagger input or [scripts/generate_api_reference.py](scripts/generate_api_reference.py), then run `make generate`.
- [.claude/skills/see/SKILL.md](.claude/skills/see/SKILL.md) contains discovery metadata and the main execution workflow. Keep its body concise and move detailed guidance into linked files under `.claude/skills/see/references/`.
- `cli.md`, `examples.md`, `safety.md`, and `sdks.md` are maintained manually.
- `dist/` and `__pycache__/` are disposable generated outputs.

## Change Workflow

1. Make the smallest change at the owning source boundary.
2. Update manual references only when behavior or agent guidance changes.
3. Run `make check`; inspect generated changes when the Swagger or generator changed.
4. Run `make package` only when a distributable archive is needed.

Keep examples deterministic and use placeholders. Preserve the existing Markdown, Python, shell, Makefile, and YAML style defined by [.editorconfig](.editorconfig).

## Safety

- All normal validation is offline. Do not call the production S.EE API or run live mutation smoke tests unless the user explicitly requests it.
- Never add API keys, authorization headers containing real tokens, production user data, file delete keys, or private download URLs.
- Do not claim SDK feature parity without checking the relevant official SDK repository.
- Follow the credential, mutation, upload, and error-handling rules in [.claude/skills/see/references/safety.md](.claude/skills/see/references/safety.md).

## Skill Compatibility

Keep `SKILL.md` frontmatter portable across Agent Skills implementations. The directory name and `name` must remain `see`; descriptions must clearly name trigger use cases. Run `make check` after any frontmatter or reference-link change.
