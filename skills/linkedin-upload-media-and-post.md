---
name: Upload media and publish a rich post
description: Run LinkedIn's three-phase media upload (initialize, PUT the bytes to the returned upload URL, verify the asset) for images, documents and video, then publish a post that references the resulting URN.
api: openapi/linkedin-use-cases-image-ad-api-openapi.yml
apis:
  - openapi/linkedin-use-cases-image-ad-api-openapi.yml
  - openapi/linkedin-use-cases-document-ad-api-openapi.yml
  - openapi/linkedin-use-cases-video-ad-api-openapi.yml
operations:
  - postInitializeImageUpload
  - getGetASingleImage
  - postInitializeDocumentUpload
  - putUploadTheDocumentFile
  - postCreateDocumentContent
  - postInitializeVideoUpload
  - getGetASingleVideo
generated: '2026-08-13'
method: generated
source: openapi/*.yml, arazzo/linkedin-upload-image-and-create-post-workflow.yml, arazzo/linkedin-upload-document-and-create-post-workflow.yml, arazzo/linkedin-upload-video-and-verify-workflow.yml
---

# Upload media and publish a rich post

LinkedIn never accepts media bytes on the post-creation call. Media is always a separate
three-phase flow, and the post only ever references the asset URN.

## Headers

`Authorization: Bearer {token}`, `Linkedin-Version: {YYYYMM}`, `X-Restli-Protocol-Version: 2.0.0`
on every `api.linkedin.com/rest/` call. The byte upload in phase 2 goes to the URL LinkedIn hands
back, which is **not** on `api.linkedin.com` and takes only the upload headers LinkedIn specifies.

## The three phases

### Images
1. `postInitializeImageUpload` — returns an `uploadUrl` and an image URN.
2. `PUT` the raw bytes to that `uploadUrl`.
3. `getGetASingleImage` — poll until the asset is available. Do not publish against an
   unverified image URN; the post will be created with a broken asset reference.

### Documents
1. `postInitializeDocumentUpload` — returns the upload URL and a document URN.
2. `putUploadTheDocumentFile` — uploads the file.
3. `postCreateDocumentContent` — creates the post that carries the document.

Fetch back with `getGetASingleDocument` / `getGetMultipleDocuments` /
`getFetchMultipleDocumentContent` when the agent needs to confirm or list what exists.

### Video
1. `postInitializeVideoUpload` — returns upload instructions (video uploads are chunked; follow the
   part list LinkedIn returns rather than assuming a single PUT).
2. Upload the parts.
3. `getGetASingleVideo` — verify. Video processing is asynchronous; a URN existing is not the same
   as a video being playable, so poll until the asset reports ready before publishing.
   `getGetMultipleVideos` batches the check.

## Rules an agent must follow

- **Verify before you publish.** Every media family has a read operation for exactly this reason.
  Skipping it produces posts that render as broken attachments and cannot be fixed by editing.
- **Never retry an initialize on a timeout.** There is no idempotency key
  (`conventions/linkedin-conventions.yml`); a retried initialize allocates a second asset and leaks
  a half-uploaded artifact. Re-read first.
- The upload URL is short-lived. If the byte PUT fails after the URL expires, restart at phase 1 —
  do not reuse the old URN.
- 429 means the daily application or member ceiling was hit and resets at 00:00 UTC
  (`rate-limits/linkedin-rate-limits.yml`).
- Errors carry `{status, message, serviceErrorCode}`, not `application/problem+json`.
