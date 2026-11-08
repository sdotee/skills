# S.EE CLI Reference

The official CLI repository is https://github.com/sdotee/cli. Run `see help <command>` for the installed version's exact flags, and `see version` to check which release is installed. This reference matches v1.4.2.

## Install

Pick the method that matches the host, and ask before installing software system-wide.

```bash
# macOS (Homebrew)
brew tap sdotee/homebrew-tap
brew install see

# Debian / Ubuntu / RHEL / Rocky / AlmaLinux (xTom APT and DNF repository)
curl -sL ba.sh/repo | sudo bash
sudo apt install see   # or: sudo dnf install see

# Arch Linux (AUR)
yay -S see-cli-bin     # pre-built; see-cli builds from source

# Go toolchain: installs the binary as `cli`, so rename it
go install github.com/sdotee/cli@latest
mv "$(go env GOPATH)/bin/cli" "$(go env GOPATH)/bin/see"
```

Each [GitHub release](https://github.com/sdotee/cli/releases) also has:

- Linux packages `see-cli_<version>_linux_<arch>.{deb,rpm,apk,pkg.tar.zst}` for `amd64` and `arm64`.
- A Termux package `see-cli_<version>_android_arm64.termux.deb`.
- Archives `see_<OS>_<arch>.tar.gz` for macOS, Linux, FreeBSD and Android, and `see_Windows_<arch>.zip`.

`go install` works from v1.4.1. Older module versions declare the path `s.ee/cli` and cannot be installed that way.

## Global Options

`--api-key`, `--base-url`, `--timeout`, and `--json` apply to every command. Prefer `SEE_API_KEY`, `SEE_BASE_URL`, and `SEE_TIMEOUT` for configuration; an explicit flag overrides its environment variable.

The two timeout settings use different formats. `--timeout` takes a Go duration such as `30s` or `2m`. `SEE_TIMEOUT` takes whole seconds such as `30`; any other value is ignored silently and the default of 30 seconds applies.

## Discovery And Account

```bash
see domains --json
see tags --json
see usage --json
see token check --json
see token check <token> --json
see version
```

`see token check` exits successfully even when the token is invalid; read the `valid` field. `see version` prints plain text and has no JSON form. Do not pass a token positionally when it would enter shell history; configure `SEE_API_KEY` and use `see token check --json`.

## Short URLs

```bash
see shorturl create <url> --domain s.ee --json
see shorturl create <url> --slug <slug> --title <title> --json
see shorturl update <slug> --domain s.ee --target-url <url> --title <title> --json
see shorturl delete <slug> --domain s.ee --json
see shorturl history --page 1 --json
see shorturl stats <slug> --domain s.ee --period daily --json
```

`see url` is an alias for `see shorturl`. The slug is a positional argument for `update`, `delete`, and `stats`; `update` requires `--target-url`. `--domain` defaults to `s.ee`.

Create flags: `--slug`, `--domain`, `--title`, `--password`, `--expire-at`, `--tag-ids`, `--expiration-redirect-url`. `--expire-at` is a Unix timestamp in seconds. Period is `daily`, `monthly`, or `totally`.

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

- `--type` is `plain_text`, `source_code`, or `markdown`.
- The API requires a title. From v1.4.1, `create` falls back to `Untitled` when `--title` is omitted, but pass a meaningful title whenever the user gives one or the content suggests one.
- `update` requires `--title` and replaces the content, so it always needs new content from `--file` or stdin.
- `--domain` defaults to `s.ee`. For `update` and `delete`, pass the domain the text was created on, as returned at creation or by `see text history`.

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
  --mastodon-url https://c.im/@s.ee \
  --link Blog=https://example.com --json
see bio update <id> --title "Updated Bio" --link Blog=https://example.com --json
see bio history --page 1 --json
see bio delete <id> --json
```

`--link title=url` is repeatable. `update` requires `--title`. On update, supplied links replace the existing complete list.

## QR Codes

```bash
see qrcode create https://example.com --title Example --domain s.ee --json
see qrcode history --page 1 --json
see qrcode delete <slug> --domain s.ee --json
```

`create` requires `--title`. Creation returns PNG, SVG, PDF, and short-link URLs.

## Result Handling

- Check the exit status first. A failed request, including any non-2xx HTTP response, exits with status 1 and prints the error message on stderr.
- Capture stdout as JSON only when `--json` is present.
- Create, list, history, statistics, domain, tag, usage, and token commands print only the response `data` object (or list), without `code` or `message`. Read fields such as `short_url`, `slug`, or `valid` directly.
- Update and delete commands print the full response; check its `code` and `message`, and `success` when present.
- `see file upload` with several paths and `see file delete` with several keys print one JSON document per item and stop at the first failure. Items before the failure already succeeded, so read stdout before retrying and skip what is done.
- Preserve returned `slug`, IDs, file delete key, and URLs only when the user needs them. Treat delete keys as sensitive capabilities.
- On unknown flags or version differences, run `see help <command>` rather than guessing.
