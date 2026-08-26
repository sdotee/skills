# S.EE Agent Skill

An Agent Skills-compatible project that teaches Claude Code and other AI coding agents how to operate and integrate the [S.EE](https://s.ee/) API safely.

The skill covers short URLs, text sharing, small and resumable file uploads, private downloads, QR codes, Bio Pages, domains, tags, analytics, token validation, and account usage. It prefers the official [S.EE CLI](https://github.com/sdotee/cli), selects an official SDK for application code, and falls back to the documented REST API.

## Install

Install as a personal Claude Code skill:

```bash
./scripts/install.sh
```

Install into a specific Agent Skills directory:

```bash
./scripts/install.sh ~/.agents/skills
```

Or copy `.claude/skills/see` to one of these locations:

- Project Claude Code: `.claude/skills/see`
- Personal Claude Code: `~/.claude/skills/see`
- Generic Agent Skills: `~/.agents/skills/see`
- VS Code/Copilot project skill: `.github/skills/see`

After adding a new top-level skills directory during an active Claude Code session, restart once. Invoke the skill directly with `/see`, or ask naturally, for example: "Shorten this URL with S.EE" or "Add S.EE file upload to this Python service."

## Prerequisites

For live operations, install the CLI and configure the API token:

```bash
brew tap sdotee/homebrew-tap
brew install see
export SEE_API_KEY='...'
```

Never commit the token. `SEE_BASE_URL` and `SEE_TIMEOUT` are optional CLI overrides.

## Project Layout

```text
.claude/skills/see/
  SKILL.md                 Skill discovery and workflow
  references/
    api.md                 REST endpoint and schema reference
    cli.md                 Agent-oriented CLI command reference
    examples.md            End-to-end examples
    safety.md              Credential and mutation policy
    sdks.md                Official SDK selection guide
scripts/
  install.sh
  package.sh
  validate.py
```

## Development

Run all offline checks:

```bash
make check
```

Build a portable archive under `dist/`:

```bash
make package
```

Validation is offline and never calls S.EE. Live smoke tests are intentionally excluded to avoid consuming quotas or mutating accounts.

## Official Resources

- Developer guide: https://s.ee/docs/developers/
- API reference: https://s.ee/docs/developers/api/
- SDK guide: https://s.ee/docs/developers/sdk/
- CLI: https://github.com/sdotee/cli
- Official repositories: https://github.com/orgs/sdotee/repositories
- Service status: https://status.s.ee/

## License

MIT. See [LICENSE](LICENSE).
