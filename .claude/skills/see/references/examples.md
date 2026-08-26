# Agent Examples

## Create A Short URL

1. If no domain is specified, run `see domains --json` and let the user select when multiple choices matter.
2. Confirm the target URL and optional slug, title, password, expiration, and tags.
3. Run:

```bash
see shorturl create https://example.com \
  --domain s.ee \
  --title Example \
  --json
```

4. Return `short_url` and `slug`. Do not expose password values.

## Share Markdown

```bash
see text create --file CHANGELOG.md \
  --title "Release notes" \
  --type markdown \
  --json
```

Confirm that the file is intended for sharing before upload. Return the created `short_url`.

## Upload A Private File

```bash
see file upload ./report.pdf --private --json
```

For files larger than 100 MB, provide a seekable path and allow the CLI to use TUS. Return the file ID and access URL as appropriate; keep the delete key private.

## REST Create Request

```bash
curl --fail-with-body --silent --show-error \
  -X POST \
  -H "Authorization: Bearer $SEE_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"domain":"s.ee","target_url":"https://example.com","title":"Example"}' \
  https://s.ee/api/v1/shorten
```

A successful response has the shape:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "short_url": "https://s.ee/example",
    "slug": "example",
    "custom_slug": ""
  }
}
```

Treat values as illustrative, not guaranteed production output.

## Verify A Mutation

- Short URL: `see shorturl history --page 1 --json` or `see shorturl stats <slug> --domain <domain> --json`.
- Text: `see text history --page 1 --json`.
- File: `see file history --page 1 --json`.
- Bio Page: `see bio history --page 1 --json`.
- QR code: `see qrcode history --page 1 --json`.
