# Contributing

## Workflow

1. Update `see_api_doc.json` when the API contract changes.
2. Run `make generate`; do not hand-edit the generated `references/api.md`.
3. Update CLI, SDK, examples, or safety guidance when behavior changes.
4. Run `make check` and include focused documentation for new behavior.

Keep changes scoped. Do not add real API keys, production responses containing user data, file delete keys, or private download URLs to fixtures or examples.

## Source Priority

Resolve disagreements in this order:

1. Current production API and official developer documentation.
2. `see_api_doc.json` for REST request and response shapes.
3. Installed `see help <command>` output for CLI flags.
4. The selected SDK repository README for language-specific behavior.

SDKs have different release schedules and feature coverage. Do not claim parity without verification.

## Security

Do not open a public issue for a vulnerability. Email `hi@s.ee` with the affected component, reproduction steps, and impact. Exclude credentials and real user data.
