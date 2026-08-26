# Contributing

## Workflow

1. Update `references/api.md`, `references/cli.md`, or `references/sdks.md` at the owning documentation boundary.
2. Update examples or safety guidance when behavior changes.
3. Run `make check` and include focused documentation for new behavior.

Keep changes scoped. Do not add real API keys, production responses containing user data, file delete keys, or private download URLs to fixtures or examples.

## Source Priority

Resolve disagreements in this order:

1. Current production API and official developer documentation.
2. Installed `see help <command>` output for CLI flags.
3. The selected SDK repository README and latest release for language-specific behavior.

SDKs have different release schedules and feature coverage. Do not claim parity without verification.

## Security

Do not open a public issue for a vulnerability. Email `hi@s.ee` with the affected component, reproduction steps, and impact. Exclude credentials and real user data.
