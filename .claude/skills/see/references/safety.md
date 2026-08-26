# Safety And Reliability

## Credentials

- Use `SEE_API_KEY` or a secret manager. Never include tokens in source, logs, command output, query strings, screenshots, fixtures, or generated documentation.
- Send `Authorization: Bearer <token>` over HTTPS only.
- The simple `/api/v1/shorten` mode uses `signature` in the query string. Prefer the authenticated JSON endpoint because URLs are commonly logged.
- Redact authorization headers and token-check responses before sharing diagnostics.

## Mutations

Creating resources can consume account quotas. Updating and deleting can affect public URLs.

- Confirm the exact URL, domain, slug, ID, filename, privacy setting, and expiration before mutation.
- Delete is permanent for short URLs, text shares, QR codes, Bio Pages, and files.
- For updates, retrieve current state first when omitted fields may be replaced. Bio Page `custom_links` are a full replacement when supplied.
- Do not retry POST, PUT, or DELETE automatically unless idempotency is established. Check history after an ambiguous timeout.

## Files

- Verify the local path, size, MIME expectations, and whether the file contains secrets or personal data.
- Public is the default unless private upload is explicitly selected.
- Preserve file delete keys only where needed; possession permits deletion.
- Temporary private download URLs should not be committed or treated as permanent.
- For resumable upload, retain `upload_id` until completion. Cancel abandoned sessions, and never call complete until uploaded bytes equal file size.

## Errors

- `200`: normal success.
- `204`: expected for TUS chunk/status/delete protocol operations.
- `400`: correct request shape and field constraints; do not retry unchanged.
- `401`: token missing or expired; ask the user to update the secret without revealing it.
- `500`: report the server error and check https://status.s.ee/ before a bounded retry.

Validate both HTTP status and JSON `code`. Surface the server `message` without dumping headers or sensitive request bodies.

Security reports must not be filed publicly. Contact `hi@s.ee` with the affected endpoint, reproduction steps, and impact, excluding credentials and real user data.
