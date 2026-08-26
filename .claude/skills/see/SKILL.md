---
name: see
description: "Operate and integrate the S.EE platform for short URLs, text sharing, file uploads, QR codes, bio pages, domains, tags, analytics, token checks, and usage. Use when an agent must call the S.EE REST API, run the see CLI, choose an official S.EE SDK, upload a file, shorten a URL, or generate integration code."
license: MIT
compatibility: "Works with Claude Code and Agent Skills-compatible agents. The preferred path requires the see CLI and SEE_API_KEY; REST fallback requires an HTTP client."
metadata:
  author: sdotee
  version: "1.0.0"
  homepage: "https://s.ee/docs/developers/"
---

# S.EE

Use S.EE to manage short URLs, shared text, files, QR codes, bio pages, and account usage.

## Execution Policy

1. Identify the requested resource and whether the action reads or mutates data.
2. Prefer the official `see` CLI for interactive Agent work. It handles authentication, output formatting, and resumable uploads.
3. Use `--json` for every CLI call whose output will be parsed or reused.
4. Use an official SDK when writing application code. Match the repository's language and verify feature coverage first.
5. Use raw REST only when the CLI or selected SDK lacks the operation.
6. Never print, persist, commit, or place an API token in a URL. Read it from `SEE_API_KEY` or a secret manager.
7. Before create, update, delete, upload, or token-validation calls, show the intended action and obtain confirmation unless the user explicitly requested that exact mutation in the current turn.
8. After a mutation, verify with the returned object or the relevant history/statistics command. Do not repeat a failed mutation blindly.

## Setup

Check for the CLI without revealing secrets:

```bash
command -v see
test -n "$SEE_API_KEY"
```

Install on macOS when needed:

```bash
brew tap sdotee/homebrew-tap
brew install see
```

Configuration variables:

- `SEE_API_KEY`: required API token.
- `SEE_BASE_URL`: optional API base URL override.
- `SEE_TIMEOUT`: optional request timeout.

The official production API base is `https://s.ee/api/v1`. The authorization header is `Authorization: Bearer $SEE_API_KEY`.

## Route The Task

- CLI operations and exact commands: read [references/cli.md](references/cli.md).
- Raw HTTP payloads, required fields, and response schemas: read [references/api.md](references/api.md).
- SDK selection and installation: read [references/sdks.md](references/sdks.md).
- Credentials, destructive actions, private files, and error handling: read [references/safety.md](references/safety.md).
- End-to-end examples: read [references/examples.md](references/examples.md).

## Common Workflow

1. Resolve available domains first when the user did not provide one: `see domains --json`, `see text domains --json`, or `see file domains --json`.
2. Gather every required value. Do not invent domains, slugs, IDs, expiration timestamps, titles, passwords, or file paths.
3. Run one operation with `--json` and parse its top-level status fields.
4. Treat success as an HTTP/response `code` of `200` unless the operation documents `204` (TUS chunk/status/cancel behavior).
5. Return the useful result, such as `short_url`, file `url`, QR asset URLs, visit count, or upload progress. Omit credentials and internal secrets.

## Important API Details

- Simple-mode shortening uses query parameter `signature`; all other authenticated operations use the `Authorization` header.
- Creating a short URL by JSON requires both `domain` and `target_url`, even though `domain` has a documented default.
- Text creation requires `content` and `title`; `text_type` is `plain_text`, `source_code`, or `markdown`.
- Files at or below 100 MB use multipart upload in the CLI. Seekable files above 100 MB automatically use resumable TUS, up to 5 GB.
- A private-file download URL is temporary, normally about one hour.
- Updating Bio Page links replaces the complete custom-link list when links are supplied.
- Statistics periods are `daily`, `monthly`, or `totally`.
- Delete operations are permanent. Reconfirm the target domain/slug, file delete key, QR code, or Bio Page ID.

## REST Fallback Pattern

Use environment-variable expansion and avoid shell tracing:

```bash
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $SEE_API_KEY" \
  -H "Content-Type: application/json" \
  "https://s.ee/api/v1/usage"
```

For request bodies, write JSON with a structured serializer when possible. Check both HTTP status and the response `code`; report `message` on failure.

## Output

Summarize the operation, the confirmed target, and the returned identifiers or URLs. For code-generation tasks, include installation, environment-variable setup, typed error handling, and a minimal runnable example using the official SDK.
