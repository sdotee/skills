# Official S.EE SDKs

Choose the SDK matching the existing project. Support priority indicates the official maintenance priority, not guaranteed endpoint parity. Read the selected repository's README and latest release before implementation.

| Language                | Repository                          | Install                           | Priority   |
| ----------------------- | ----------------------------------- | --------------------------------- | ---------- |
| TypeScript / JavaScript | https://github.com/sdotee/sdk.ts    | `npm install see-sdk`             | A          |
| Go                      | https://github.com/sdotee/sdk.go    | `go get github.com/sdotee/sdk.go` | A          |
| Python                  | https://github.com/sdotee/sdk.py    | `pip install see-sdk`             | A          |
| Rust                    | https://github.com/sdotee/sdk.rs    | `cargo add see-sdk`               | B          |
| Swift                   | https://github.com/sdotee/sdk.swift | Swift Package Manager             | B          |
| Java                    | https://github.com/sdotee/sdk.java  | `dev.s.ee:see-java-sdk`           | B          |
| PHP                     | https://github.com/sdotee/sdk.php   | `composer require sdotee/sdk`     | C          |
| .NET / C#               | https://github.com/sdotee/sdk.cs    | See repository README             | C          |
| Zig                     | https://github.com/sdotee/sdk.zig   | Build from source                 | Deprecated |

## Integration Rules

1. Inspect the project language, dependency manager, and existing HTTP conventions.
2. Confirm that the SDK exposes the requested endpoint. API and release cadence differ across repositories.
3. Load the token from `SEE_API_KEY` or the application's secret provider. Never hardcode it.
4. Reuse one client instance and configure explicit timeouts.
5. Handle transport errors separately from S.EE response errors (`code` and `message`).
6. For uploads, stream file data and avoid reading large files fully into memory. Prefer SDK/CLI TUS support for files above 100 MB.
7. Add focused tests with a mocked transport; do not call production from unit tests.

Official guides:

- Developer guide: https://s.ee/docs/developers/
- API reference: https://s.ee/docs/developers/api/
- SDK guide: https://s.ee/docs/developers/sdk/
- Service status: https://status.s.ee/
