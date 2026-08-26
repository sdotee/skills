# S.EE REST API Reference

This reference summarizes the official S.EE REST API for agent integrations.

- Base URL: `https://s.ee`
- API prefix: `/api/v1`
- Authentication: `Authorization: Bearer $SEE_API_KEY`, except simple-mode shortening and token validation
- Success is normally HTTP 200 with JSON fields `code`, `message`, and `data`

## Bio Page

### `DELETE /api/v1/bio`

**Delete Bio Page** (`DeleteBioPage`)

Permanently deletes a bio page. This action cannot be undone.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.DeleteBioPageReq` | yes | Bio page identification |

Response `200`: `httper.RespBody` - OK

### `POST /api/v1/bio`

**Create Bio Page** (`CreateBioPage`)

Creates a new bio page with a short URL.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.CreateBioPageReq` | yes | Bio page content and settings |

Response `200`: `val.CreateBioPageRespV` - OK

### `PUT /api/v1/bio`

**Update Bio Page** (`UpdateBioPage`)

Updates an existing bio page.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.UpdateBioPageReq` | yes | Updated bio page settings |

Response `200`: `httper.RespBody` - OK

### `GET /api/v1/bios`

**Get Bio Page History** (`GetBioPageHistory`)

Returns a paginated list of bio pages.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `page` | `query` | `integer` | no | Page number (default: 1) |

Response `200`: `val.GetBioPageHistoryRespV` - OK

## File

### `GET /api/v1/file/delete/{hash}`

**Delete File** (`DeleteFile`)

This API allows you to delete a file using its delete key.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `hash` | `path` | `string` | yes | Delete Key |
| `Authorization` | `header` | `string` | yes | API key |

Response `200`: `val.DeleteFileResp` - OK

### `GET /api/v1/file/domains`

**Get Available Domains for File Sharing** (`GetFileAvailableDomains`)

Returns a list of all domains available for creating file sharing URLs with your account. Use these domain values when calling the File Upload endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |

Response `200`: `val.GetAvailableDomainsRespV` - OK

### `DELETE /api/v1/file/large-file-tus/{upload_id}`

**TUS Upload Chunk** (`DeleteTUSUpload`)

Handles TUS 1.0 protocol requests (PATCH/HEAD/DELETE). Use the TUS client library for chunk uploading. The upload_id comes from the create endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `upload_id` | `path` | `string` | yes | Upload session ID |

Response `204`: `none` - Chunk accepted

### `HEAD /api/v1/file/large-file-tus/{upload_id}`

**TUS Upload Chunk** (`GetTUSUploadStatus`)

Handles TUS 1.0 protocol requests (PATCH/HEAD/DELETE). Use the TUS client library for chunk uploading. The upload_id comes from the create endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `upload_id` | `path` | `string` | yes | Upload session ID |

Response `204`: `none` - Chunk accepted

### `PATCH /api/v1/file/large-file-tus/{upload_id}`

**TUS Upload Chunk** (`UploadTUSChunk`)

Handles TUS 1.0 protocol requests (PATCH/HEAD/DELETE). Use the TUS client library for chunk uploading. The upload_id comes from the create endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `upload_id` | `path` | `string` | yes | Upload session ID |

Response `204`: `none` - Chunk accepted

### `DELETE /api/v1/file/large-file/cancel`

**Cancel Large File Upload** (`OpenAPICancelLargeFileUpload`)

Cancels an in-progress upload session and removes the temporary data.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `data` | `body` | `val.CancelLargeFileUploadReq` | yes | Upload session ID |

Response `200`: `httper.RespBody` - OK

### `POST /api/v1/file/large-file/complete`

**Complete Large File Upload** (`OpenAPICompleteLargeFileUpload`)

Call this after all TUS chunks have been uploaded. It validates the file, moves it to permanent storage, and returns the file record. This consumes the upload session.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `data` | `body` | `val.CompleteLargeFileUploadReq` | yes | Upload session ID |

Response `200`: `val.CompleteLargeFileUploadRespV` - OK

### `POST /api/v1/file/large-file/create`

**Create Large File Upload Session** (`OpenAPICreateLargeFileUpload`)

Creates a TUS upload session for files up to 5 GB. Returns an upload_id and TUS endpoint URL. If a file_hash is provided and the file already exists, an instant upload result is returned without needing to transfer any data.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `data` | `body` | `val.CreateLargeFileUploadReq` | yes | Upload session parameters |

Response `200`: `val.CreateLargeFileUploadRespV` - OK

### `GET /api/v1/file/large-file/progress`

**Get Upload Progress** (`OpenAPIGetLargeFileUploadProgress`)

Returns the current progress of a large file upload session.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `upload_id` | `query` | `string` | yes | Upload session ID |

Response `200`: `val.GetLargeFileUploadProgressRespV` - OK

### `GET /api/v1/file/private/download-url`

**Get Private File Download URL** (`GetPrivateFileDownloadURL`)

This API allows you to get a temporary download URL for a private file using its file ID. The URL is cached for a period of time, so multiple requests for the same file will return the same URL.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `file_id` | `query` | `integer` | yes | File ID |
| `Authorization` | `header` | `string` | yes | API key |

Response `200`: `val.GetPrivateFileURLRespV` - OK

### `POST /api/v1/file/upload`

**Upload File** (`UploadFile`)

This API allows you to upload a file and create a short link for it.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `file` | `formData` | `file` | yes | The form-data should contain the file to be uploaded. The key should be 'file' (alias 'smfile'). |
| `domain` | `formData` | `string` | no | The domain to be used for the short link. |
| `custom_slug` | `formData` | `string` | no | Your preferred custom slug (e.g., 'my-link'). If not provided, a random slug will be generated. |

Response `200`: `val.UploadFileRespV` - OK

### `GET /api/v1/files`

**Get File Upload History** (`GetFileHistory`)

Returns a paginated list of uploaded files for the authenticated user. Compatible with sm.ms upload_history API.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `page` | `query` | `integer` | no | Page number (default: 1) |

Response `200`: `val.GetFileHistoryRespV` - OK

## QR Code

### `DELETE /api/v1/qrcode`

**Delete QR Code** (`DeleteQrcode`)

Permanently deletes a QR code and its associated short link. This action cannot be undone.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.DeleteQrcodeReq` | yes | QR code identification |

Response `200`: `httper.RespBody` - OK

### `POST /api/v1/qrcode`

**Create QR Code** (`CreateQrcode`)

Creates a dynamic QR code for a given URL. The QR code is generated server-side and available in PNG, SVG, and PDF formats. Only link-type QR codes are supported.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.CreateQrcodeReq` | yes | QR code content and settings |

Response `200`: `val.CreateQrcodeRespV` - OK

### `GET /api/v1/qrcodes`

**Get QR Code History** (`GetQrcodeHistory`)

Returns a paginated list of QR codes created by the authenticated user.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `page` | `query` | `integer` | no | Page number (default: 1) |

Response `200`: `val.GetQrcodeHistoryRespV` - OK

## Short URLs

### `GET /api/v1/domains`

**Get Available Domains for Short URLs** (`GetAvailableDomains`)

Returns a list of all domains available for creating short URLs with your account. Use these domain values when calling the Create Short URL endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |

Response `200`: `val.GetAvailableDomainsRespV` - OK

### `GET /api/v1/link/visit-stat`

**Get Link Visit Statistics** (`GetLinkVisitStat`)

Retrieves click/visit statistics for a specific short URL. You can get daily, monthly, or all-time statistics by specifying the period parameter.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `domain` | `query` | `string` | yes | The domain of the short URL (e.g., s.ee) |
| `slug` | `query` | `string` | yes | The slug of the short URL (e.g., abc123) |
| `period` | `query` | `string` | no | Statistics time range: daily (today), monthly (this month), or totally (all-time, default) |

Response `200`: `val.GetLinkVisitStatRespV` - OK

### `GET /api/v1/links`

**Get Link Creation History** (`GetLinkHistory`)

Returns a paginated list of short links created by the authenticated user.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `page` | `query` | `integer` | no | Page number (default: 1) |

Response `200`: `val.GetLinkHistoryRespV` - OK

### `DELETE /api/v1/shorten`

**Delete Short URL** (`DeleteShortUrl`)

Permanently deletes a short URL. This action cannot be undone. The slug will become available for reuse after deletion.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.DeleteShortURLReq` | yes | Short URL identification |

Response `200`: `httper.RespBody` - OK

### `GET /api/v1/shorten`

**Create Short URL (Simple Mode)** (`CreateShortUrlSimpleMode`)

A simplified way to create short URLs using query parameters instead of a JSON body. Ideal for quick integrations, bookmarklets, or when you need a plain text response. Set json=true for JSON response format.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `signature` | `query` | `string` | yes | Your API key |
| `url` | `query` | `string` | yes | The destination URL to shorten (required) |
| `domain` | `query` | `string` | no | Domain for the short URL (optional, uses default if omitted) |
| `custom_slug` | `query` | `string` | no | Your preferred custom slug (optional) |
| `title` | `query` | `string` | no | A descriptive title for this link (optional) |
| `tag_ids` | `query` | `array` | no | Tag IDs to categorize this link (optional) |
| `password` | `query` | `string` | no | Password to protect this link (optional) |
| `expire_at` | `query` | `integer` | no | Unix timestamp when this link should expire (optional) |
| `json` | `query` | `boolean` | no | Set to true to receive JSON response instead of plain text |

Response `200`: `val.CreateShortURLRespV` - OK

### `POST /api/v1/shorten`

**Create Short URL** (`CreateShortUrl`)

Creates a new short URL for your destination link. You can optionally specify a custom slug, password protection, expiration time, and tags for organization.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.CreateShortURLReq` | yes | Short URL configuration |

Response `200`: `val.CreateShortURLRespV` - OK

### `PUT /api/v1/shorten`

**Update Short URL** (`UpdateShortUrl`)

Updates the destination URL and/or title of an existing short URL. The domain and slug identify which link to update.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.UpdateShortURLReq` | yes | Updated short URL details |

Response `200`: `httper.RespBody` - OK

### `GET /api/v1/usage`

**Get Usage** (`GetUsage`)

This API allows you to get the usage of the short link service.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |

Response `200`: `val.GetUsageRespV` - OK

## Tags

### `GET /api/v1/tags`

**Get All Tags** (`GetTags`)

Returns all tags you have created. Tags help organize your short URLs and shared texts into categories for easier management.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |

Response `200`: `httper.RespBody + object` - OK

## Text Sharing

### `DELETE /api/v1/text`

**Delete Text Sharing** (`DeleteText`)

Permanently deletes a text sharing. This action cannot be undone. The slug will become available for reuse after deletion.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.DeleteTextReq` | yes | Text sharing identification |

Response `200`: `httper.RespBody` - OK

### `POST /api/v1/text`

**Create Text Sharing** (`CreateText`)

Creates a shareable text snippet with a unique URL. Perfect for sharing code, notes, or any text content. Supports plain text, source code (with syntax highlighting), and Markdown formatting.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.CreateTextReq` | yes | Text content and settings |

Response `200`: `val.CreateTextRespV` - OK

### `PUT /api/v1/text`

**Update Text Sharing** (`UpdateText`)

Updates the content and/or title of an existing text sharing. The domain and slug identify which text to update.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |
| `data` | `body` | `val.UpdateTextReq` | yes | Updated text content and settings |

Response `200`: `httper.RespBody` - OK

### `GET /api/v1/text/domains`

**Get Available Domains for Text Sharing** (`GetTextAvailableDomains`)

Returns a list of all domains available for creating text sharing URLs with your account. Use these domain values when calling the Create Text Sharing endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | Your API key |

Response `200`: `val.GetAvailableDomainsRespV` - OK

### `GET /api/v1/texts`

**Get Text Creation History** (`GetTextHistory`)

Returns a paginated list of text sharings created by the authenticated user.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `Authorization` | `header` | `string` | yes | API key |
| `page` | `query` | `integer` | no | Page number (default: 1) |

Response `200`: `val.GetTextHistoryRespV` - OK

## Token

### `POST /api/v1/token/check`

**Check API Token** (`CheckToken`)

This API allows you to check if the provided API token is valid and usable. When the token is valid, it returns the token string and its expiration time.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `data` | `body` | `val.CheckTokenReq` | yes | API token to validate |

Response `200`: `val.CheckTokenRespV` - OK

## Schemas

#### `httper.RespBody`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `inline object` | no | - | Response payload |
| `message` | `string` | no | - | Human-readable status message |

#### `val.CancelLargeFileUploadReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `upload_id` | `string` | yes | - | Upload session ID to cancel |

#### `val.CheckTokenReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `token` | `string` | yes | length `0..255` | Your API token to validate |

#### `val.CheckTokenRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.CheckTokenResp` | no | - | Token validation result |
| `message` | `string` | no | - | Human-readable status message |

#### `val.CompleteLargeFileUploadReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `upload_id` | `string` | yes | - | Upload session ID that has finished uploading all chunks |

#### `val.CompleteLargeFileUploadRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.CompleteLargeFileUploadResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.CreateBioPageReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_links` | `array<val.BioCustomLinkItem>` | no | - | Optional list of custom links to add to the bio page |
| `custom_slug` | `string` | no | length `0..255` | Your preferred custom slug. If not provided, a random slug will be generated. |
| `description` | `string` | no | length `0..1024` | Optional short description shown on the bio page |
| `domain` | `string` | no | length `0..255` | The domain to use for your bio page short URL (e.g., "s.ee"). If not provided, the default link domain is used. |
| `mastodon_url` | `string` | no | length `0..2048` | Mastodon profile URL, e.g. https://mastodon.social/@username |
| `rss_url` | `string` | no | length `0..2048` | RSS feed URL to display latest posts on your bio page |
| `title` | `string` | yes | length `0..255` | Title of the bio page (required) |

#### `val.CreateBioPageRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.CreateBioPageResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.CreateLargeFileUploadReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `alias` | `string` | no | length `0..255` | Custom slug for the short link (optional, alphanumeric only) |
| `description` | `string` | no | length `0..1024` | Description (optional) |
| `domain` | `string` | no | length `0..255` | Domain for short link (optional, use /api/v1/file/domains to list) |
| `expire_at` | `integer` | no | - | Unix timestamp for link expiry (optional) |
| `file_hash` | `string` | no | length `0..255` | SHA256 hash for instant upload deduplication (optional) |
| `file_name` | `string` | yes | length `0..255` | Original filename (required) |
| `file_size` | `integer` | yes | - | File size in bytes (required) |
| `is_private` | `integer` | no | one of `0`, `1` | Privacy: 0=public (default), 1=private |
| `mime_type` | `string` | no | length `0..255` | MIME type hint (optional, server will detect from file bytes) |
| `password` | `string` | no | length `3..32` | Access password (3–32 chars, optional) |
| `title` | `string` | no | length `0..255` | Title for the file (optional) |

#### `val.CreateLargeFileUploadRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.CreateLargeFileUploadResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.CreateQrcodeReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_slug` | `string` | no | length `0..255` | CustomSlug 自定义短链接别名 |
| `domain` | `string` | no | length `0..255` | Domain 域名，如果不指定，则使用默认域名 |
| `target_url` | `string` | yes | length `0..2048` | TargetURL 目标链接 URL |
| `title` | `string` | yes | length `0..255` | Title 二维码标题 |

#### `val.CreateQrcodeRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.CreateQrcodeResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.CreateShortURLReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_slug` | `string` | no | length `0..255` | Your preferred custom slug (e.g., "my-link"). If not provided, a random slug will be generated. |
| `domain` | `string` | yes | default `s.ee`; length `0..255` | The domain to use for your short URL (e.g., "s.ee") |
| `expiration_redirect_url` | `string` | no | length `0..2000` | URL to redirect visitors to after this short link expires |
| `expire_at` | `integer` | no | - | Unix timestamp when this short link should expire (e.g., 1735689600) |
| `password` | `string` | no | length `3..32` | Optional password to protect this short link (3-32 characters) |
| `tag_ids` | `array<integer>` | no | - | Array of tag IDs to organize this link (get available tags via /api/v1/tags) |
| `target_url` | `string` | yes | length `0..2000` | The destination URL you want to shorten (required) |
| `title` | `string` | no | length `0..255` | A descriptive title for this short link (for your reference) |

#### `val.CreateShortURLRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.CreateShortURLResp` | no | - | Short URL creation response |
| `message` | `string` | no | - | Human-readable status message |

#### `val.CreateTextReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `content` | `string` | yes | length `0..2097152` | The text content you want to share (up to 2MB) |
| `custom_slug` | `string` | no | length `0..255` | Your preferred custom slug. If not provided, a random slug will be generated. |
| `domain` | `string` | no | default `fs.to`; length `0..255` | The domain to use for your text share URL (e.g., "fs.to") |
| `expire_at` | `integer` | no | - | Unix timestamp when this text sharing should expire |
| `password` | `string` | no | length `3..32` | Optional password to protect this text sharing (3-32 characters) |
| `tag_ids` | `array<integer>` | no | items `0..5` | Array of tag IDs to organize this text (max 5 tags) |
| `text_type` | `string` | no | one of `plain_text`, `source_code`, `markdown` | Content format: "plain_text" for regular text, "source_code" for code with syntax highlighting, or "markdown" for formatted text |
| `title` | `string` | yes | length `0..255` | A descriptive title for this text sharing (required) |

#### `val.CreateTextRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.CreateTextResp` | no | - | Text sharing creation response |
| `message` | `string` | no | - | Human-readable status message |

#### `val.DeleteBioPageReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `id` | `integer` | yes | minimum `1` | The numeric ID of the bio page to delete (required) |

#### `val.DeleteFileResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `string` | no | - | - |
| `message` | `string` | no | - | - |
| `success` | `boolean` | no | - | - |

#### `val.DeleteQrcodeReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `domain` | `string` | yes | length `0..255` | Domain 域名 |
| `slug` | `string` | yes | length `0..255` | Slug 短链接别名 |

#### `val.DeleteShortURLReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `domain` | `string` | yes | length `0..255` | The domain where the short URL is hosted (e.g., "s.ee") |
| `slug` | `string` | yes | length `0..255` | The slug of the short URL to delete (e.g., "abc123") |

#### `val.DeleteTextReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `domain` | `string` | yes | length `0..255` | The domain where the text sharing is hosted (e.g., "fs.to") |
| `slug` | `string` | yes | length `0..255` | The slug of the text sharing to delete |

#### `val.GetAvailableDomainsRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.GetAvailableDomainsResp` | no | - | Available domains response |
| `message` | `string` | no | - | Human-readable status message |

#### `val.GetBioPageHistoryRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.GetBioPageHistoryResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.GetFileHistoryRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `array<val.UploadFileRespData>` | no | - | File list |
| `message` | `string` | no | - | Human-readable status message |
| `success` | `boolean` | no | - | Response status code |

#### `val.GetLargeFileUploadProgressRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.GetLargeFileUploadProgressResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.GetLinkHistoryRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `array<val.LinkHistoryData>` | no | - | Link list |
| `message` | `string` | no | - | Human-readable status message |
| `success` | `boolean` | no | - | Response status code |

#### `val.GetLinkVisitStatRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.GetLinkVisitStatResp` | no | - | Link visit statistics response |
| `message` | `string` | no | - | Human-readable status message |

#### `val.GetPrivateFileURLRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.GetPrivateFileURLRespData` | no | - | Response data |
| `message` | `string` | no | - | Human-readable status message |
| `success` | `boolean` | no | - | Success flag |

#### `val.GetQrcodeHistoryRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | - |
| `data` | `val.GetQrcodeHistoryResp` | no | - | - |
| `message` | `string` | no | - | - |

#### `val.GetTextHistoryRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `array<val.TextHistoryData>` | no | - | Text list |
| `message` | `string` | no | - | Human-readable status message |
| `success` | `boolean` | no | - | Response status code |

#### `val.GetUsageRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.GetUsageResp` | no | - | Account usage statistics |
| `message` | `string` | no | - | Human-readable status message |

#### `val.UpdateBioPageReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_links` | `array<val.BioCustomLinkItem>` | no | - | Custom links to fully replace the existing list. Omit this field to leave custom links unchanged. |
| `description` | `string` | no | length `0..1024` | New description |
| `id` | `integer` | yes | minimum `1` | The numeric ID of the bio page to update (required) |
| `mastodon_url` | `string` | no | length `0..2048` | Mastodon profile URL |
| `rss_url` | `string` | no | length `0..2048` | RSS feed URL |
| `title` | `string` | yes | length `0..255` | New title for the bio page (required) |

#### `val.UpdateShortURLReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `domain` | `string` | yes | length `0..255` | The domain where the short URL is hosted (e.g., "s.ee") |
| `slug` | `string` | yes | length `0..255` | The slug of the short URL to update (e.g., "abc123") |
| `target_url` | `string` | yes | length `0..2000` | The new destination URL |
| `title` | `string` | yes | length `0..255` | The new title for this short link |

#### `val.UpdateTextReq`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `content` | `string` | yes | length `0..2097152` | The new text content (up to 2MB) |
| `domain` | `string` | yes | length `0..255` | The domain where the text sharing is hosted (e.g., "fs.to") |
| `slug` | `string` | yes | length `0..255` | The slug of the text sharing to update |
| `title` | `string` | yes | length `0..255` | The new title for this text sharing |

#### `val.UploadFileRespV`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `code` | `integer` | no | - | Response status code (200 indicates success) |
| `data` | `val.UploadFileRespData` | no | - | File upload response |
| `message` | `string` | no | - | Human-readable status message |

#### `val.CheckTokenResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `expires_at` | `integer` | no | - | Token expiration time in Unix timestamp |
| `token` | `string` | no | - | Token string |
| `valid` | `boolean` | no | - | Whether the API token is valid |

#### `val.CompleteLargeFileUploadResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `file` | `val.UploadFileRespData` | no | - | Uploaded file info |
| `short_link` | `string` | no | - | Short link created for the file (if domain/alias were provided at creation) |

#### `val.BioCustomLinkItem`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `description` | `string` | no | length `0..1024` | Optional description |
| `title` | `string` | yes | length `0..255` | Link title (required) |
| `url` | `string` | yes | length `0..2048` | Target URL (required) |

#### `val.CreateBioPageResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `bio_page_id` | `integer` | no | - | The numeric ID of the created bio page |
| `short_url` | `string` | no | - | The complete short URL pointing to the bio page |

#### `val.CreateLargeFileUploadResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `existing_file` | `val.UploadFileRespData` | no | - | Populated when fast_upload=true with the existing file info |
| `expires_at` | `integer` | no | - | Unix timestamp when this upload session expires (24h) |
| `fast_upload` | `boolean` | no | - | True when the file already exists and upload was skipped |
| `file_size` | `integer` | no | - | Total file size in bytes |
| `id` | `integer` | no | - | Database record ID for this upload session |
| `upload_id` | `string` | no | - | Unique upload session ID to use in subsequent TUS requests |
| `upload_url` | `string` | no | - | TUS upload endpoint URL |

#### `val.CreateQrcodeResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_slug` | `string` | no | - | CustomSlug 自定义短链接别名（如果指定了） |
| `pdf_url` | `string` | no | - | PdfURL 二维码 PDF 下载地址 |
| `png_url` | `string` | no | - | PngURL 二维码 PNG 下载地址 |
| `short_url` | `string` | no | - | ShortURL 短链接 URL |
| `slug` | `string` | no | - | Slug 短链接别名 |
| `svg_url` | `string` | no | - | SvgURL 二维码 SVG 下载地址 |

#### `val.CreateShortURLResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_slug` | `string` | no | - | The custom slug if one was requested |
| `short_url` | `string` | no | - | The complete short URL ready to share (e.g., "https://s.ee/abc123") |
| `slug` | `string` | no | - | The unique identifier portion of the short URL |

#### `val.CreateTextResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `custom_slug` | `string` | no | - | The custom slug if one was requested |
| `short_url` | `string` | no | - | The complete URL to access your text sharing |
| `slug` | `string` | no | - | The unique identifier portion of the URL |

#### `val.GetAvailableDomainsResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `domains` | `array<string>` | no | - | List of domains you can use for creating short URLs |

#### `val.GetBioPageHistoryResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `bio_pages` | `array<val.BioPageHistoryData>` | no | - | - |
| `total` | `integer` | no | - | - |

#### `val.UploadFileRespData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `created_at` | `integer` | no | - | Image upload timestamp (for upload history only) |
| `delete` | `string` | no | - | URL to delete this file |
| `file_id` | `integer` | no | - | Unique identifier for this file |
| `filename` | `string` | no | - | Original filename as uploaded |
| `hash` | `string` | no | - | Delete key required to remove this file |
| `height` | `integer` | no | - | Image height in pixels (for image files only) |
| `mime_type` | `string` | no | - | MIME type of the uploaded file (e.g., "image/jpeg", "application/pdf") |
| `page` | `string` | no | - | Web page URL where this file can be viewed |
| `path` | `string` | no | - | Storage path of the file |
| `size` | `integer` | no | - | File size in bytes |
| `storename` | `string` | no | - | Filename in storage |
| `thumb_url` | `string` | no | - | Thumbnail URL (for image files only) |
| `upload_status` | `integer` | no | - | Upload status code (1 = success) |
| `url` | `string` | no | - | Direct URL to access/download this file |
| `width` | `integer` | no | - | Image width in pixels (for image files only) |

#### `val.GetLargeFileUploadProgressResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `created_at` | `integer` | no | - | Unix timestamp of record creation |
| `file_name` | `string` | no | - | Original filename |
| `file_size` | `integer` | no | - | Total file size in bytes |
| `progress` | `number` | no | - | Progress percentage (0–100) |
| `status` | `integer` | no | - | Status: 1=uploading, 2=completed, 3=failed, 4=cancelled |
| `updated_at` | `integer` | no | - | Unix timestamp of last update |
| `upload_id` | `string` | no | - | Upload session ID |
| `uploaded_size` | `integer` | no | - | Bytes received so far |

#### `val.LinkHistoryData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `created_at` | `integer` | no | - | Unix timestamp when the link was created |
| `domain` | `string` | no | - | The domain used for this short URL |
| `object_type` | `integer` | no | - | Object type (0: link, 1: file, 2: text, 3: qrcode) |
| `short_url` | `string` | no | - | The complete short URL |
| `slug` | `string` | no | - | The slug/alias for this short URL |
| `target_url` | `string` | no | - | The original destination URL |
| `title` | `string` | no | - | Title of the short link |
| `visit_count` | `integer` | no | - | Number of visits/clicks |

#### `val.GetLinkVisitStatResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `visit_count` | `integer` | no | - | Total number of visits/clicks for this link |

#### `val.GetPrivateFileURLRespData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `expires_at` | `integer` | no | - | URL expiration time (unix timestamp) |
| `file_id` | `integer` | no | - | File ID |
| `url` | `string` | no | - | Temporary download URL (valid for a limited time) |

#### `val.GetQrcodeHistoryResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `qrcodes` | `array<val.QrcodeHistoryData>` | no | - | - |
| `total` | `integer` | no | - | - |

#### `val.TextHistoryData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `content_preview` | `string` | no | - | Preview of the content (truncated) |
| `created_at` | `integer` | no | - | Unix timestamp when the text was created |
| `domain` | `string` | no | - | The domain used for this text sharing |
| `id` | `integer` | no | - | Unique identifier for the text |
| `is_expired` | `boolean` | no | - | Whether the text is expired |
| `short_url` | `string` | no | - | The complete URL to access the text sharing |
| `slug` | `string` | no | - | The slug/alias for this text sharing |
| `text_type` | `string` | no | - | Text type: "plain_text", "source_code", or "markdown" |
| `title` | `string` | no | - | Title of the text sharing |

#### `val.GetUsageResp`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `api_count_day` | `integer` | no | - | API calls made today |
| `api_count_day_limit` | `integer` | no | - | Maximum API calls allowed per day |
| `api_count_month` | `integer` | no | - | API calls made this month |
| `api_count_month_limit` | `integer` | no | - | Maximum API calls allowed per month |
| `file_count` | `integer` | no | - | Total uploaded files count |
| `link_count_day` | `integer` | no | - | Short links created today |
| `link_count_day_limit` | `integer` | no | - | Maximum short links allowed per day |
| `link_count_month` | `integer` | no | - | Short links created this month |
| `link_count_month_limit` | `integer` | no | - | Maximum short links allowed per month |
| `qrcode_count_day` | `integer` | no | - | QR codes generated today |
| `qrcode_count_day_limit` | `integer` | no | - | Maximum QR codes allowed per day |
| `qrcode_count_month` | `integer` | no | - | QR codes generated this month |
| `qrcode_count_month_limit` | `integer` | no | - | Maximum QR codes allowed per month |
| `storage_usage_limit_mb` | `string` | no | - | Maximum storage space allowed (in MB, rounded to 2 decimal places, -1 means unlimited) |
| `storage_usage_mb` | `string` | no | - | Storage space used by uploaded files (in MB, rounded to 2 decimal places) |
| `text_count_day` | `integer` | no | - | Text shares created today |
| `text_count_day_limit` | `integer` | no | - | Maximum text shares allowed per day |
| `text_count_month` | `integer` | no | - | Text shares created this month |
| `text_count_month_limit` | `integer` | no | - | Maximum text shares allowed per month |
| `upload_count_day` | `integer` | no | - | Files uploaded today |
| `upload_count_day_limit` | `integer` | no | - | Maximum file uploads allowed per day |
| `upload_count_month` | `integer` | no | - | Files uploaded this month |
| `upload_count_month_limit` | `integer` | no | - | Maximum file uploads allowed per month |

#### `val.BioPageHistoryData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `created_at` | `integer` | no | - | Unix timestamp when the bio page was created |
| `custom_links` | `array<val.BioPageCustomLinkData>` | no | - | Custom links on this bio page |
| `description` | `string` | no | - | Description of the bio page |
| `domain` | `string` | no | - | The domain used for this bio page |
| `id` | `integer` | no | - | Unique identifier for the bio page |
| `link` | `string` | no | - | The complete short URL of the bio page |
| `mastodon_url` | `string` | no | - | Mastodon profile URL |
| `rss_url` | `string` | no | - | RSS feed URL |
| `slug` | `string` | no | - | The slug portion of the short URL |
| `title` | `string` | no | - | Title of the bio page |

#### `val.QrcodeHistoryData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `created_at` | `integer` | no | - | CreatedAt 创建时间（Unix 时间戳） |
| `domain` | `string` | no | - | Domain 域名 |
| `pdf_url` | `string` | no | - | PdfURL 二维码 PDF 下载地址 |
| `png_url` | `string` | no | - | PngURL 二维码 PNG 下载地址 |
| `scan_count` | `integer` | no | - | ScanCount 扫码次数 |
| `short_url` | `string` | no | - | ShortURL 短链接 URL |
| `slug` | `string` | no | - | Slug 短链接别名 |
| `svg_url` | `string` | no | - | SvgURL 二维码 SVG 下载地址 |
| `title` | `string` | no | - | Title 标题 |

#### `val.BioPageCustomLinkData`

| Field | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- |
| `description` | `string` | no | - | Optional description |
| `title` | `string` | no | - | Link title |
| `url` | `string` | no | - | Target URL |
