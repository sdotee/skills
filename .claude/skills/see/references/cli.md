# S.EE CLI Reference

The official CLI repository is https://github.com/sdotee/cli. Run `see help <command>` for the installed version's exact flags. Global options include `--api-key`, `--base-url`, `--timeout`, and `--json`; prefer environment variables for secrets.

## Discovery And Account

```bash
see domains --json
see tags --json
see usage --json
see token check --json
see token check <token> --json
see version
```

Do not pass a token positionally when it would enter shell history; configure `SEE_API_KEY` and use `see token check --json`.

## Short URLs

```bash
see shorturl create <url> --domain s.ee --json
see shorturl create <url> --slug <slug> --title <title> --json
see shorturl update <slug> --domain s.ee --target-url <url> --title <title> --json
see shorturl delete <slug> --domain s.ee --json
see shorturl history --page 1 --json
see shorturl stats <slug> --domain s.ee --period daily --json
```

Create flags: `--slug`, `--domain`, `--title`, `--password`, `--expire-at`, `--tag-ids`, `--expiration-redirect-url`. Period is `daily`, `monthly`, or `totally`.

## Text Sharing

The command reads content from stdin by default or from `--file`.

```bash
printf '%s' 'hello' | see text create --title Greeting --type plain_text --json
see text create --file README.md --title README --type markdown --json
see text update <slug> --domain fs.to --file note.md --title Note --json
see text delete <slug> --domain fs.to --json
see text domains --json
see text history --page 1 --json
```

Create flags: `--file`, `--type`, `--slug`, `--domain`, `--title`, `--password`, `--expire-at`, `--tag-ids`.

## Files

```bash
see file domains --json
see file upload ./asset.png --domain <domain> --json
see file upload --file ./asset.png --slug <slug> --json
cat asset.png | see file upload --name asset.png --json
see file history --page 1 --json
see file download-url <file-id> --json
see file delete <delete-key> --json
```

Upload flags include `--file`/`-f`, `--name`/`-n`, `--domain`, `--slug`, and `--private`. Multiple path arguments are supported. Use paths rather than stdin for files above 100 MB so the CLI can discover size and select resumable TUS upload. File deletion accepts one or more delete keys and is permanent.

## Bio Pages

```bash
see bio create "My Bio" --description "About me" \
  --mastodon-url https://mastodon.social/@me \
  --link Blog=https://example.com --json
see bio update <id> --title "Updated Bio" --link Blog=https://example.com --json
see bio history --page 1 --json
see bio delete <id> --json
```

`--link title=url` is repeatable. On update, supplied links replace the existing complete list.

## QR Codes

```bash
see qrcode create https://example.com --title Example --domain s.ee --json
see qrcode history --page 1 --json
see qrcode delete <slug> --domain s.ee --json
```

Creation returns PNG, SVG, PDF, and short-link URLs.

## Result Handling

- Capture stdout as JSON only when `--json` is present.
- Do not infer success from process exit alone; inspect `code`, `success` when present, and `message`.
- Preserve returned `slug`, IDs, file delete key, and URLs only when the user needs them. Treat delete keys as sensitive capabilities.
- On unknown flags or version differences, run `see help <command>` rather than guessing.
