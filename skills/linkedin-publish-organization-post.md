---
name: Publish and verify an organization post
description: Resolve a LinkedIn organization the caller administers, publish a share authored by that organization, then read the post back by URN to confirm it landed.
api: openapi/linkedin-use-cases-organization-lookup-organizations-api-openapi.yml
apis:
  - openapi/linkedin-use-cases-organization-lookup-organizations-api-openapi.yml
  - openapi/linkedin-use-cases-social-actions-notifications-organization-social-actions-notifications-pull-workflow-api-openapi.yml
  - openapi/linkedin-use-cases-posts-api-openapi.yml
operations:
  - getLookupByOrganizationPrimary
  - postCreateAShareWith
  - getGetPostsByUrn
  - postUpdateAPost
  - deleteDeleteAPost
generated: '2026-08-13'
method: generated
source: openapi/*.yml, arazzo/linkedin-create-organization-share-workflow.yml, conventions/linkedin-conventions.yml
---

# Publish and verify an organization post

Use this when an agent must post content to a LinkedIn Company Page on behalf of an
authenticated member who administers that page.

## Before any call

Every request to `https://api.linkedin.com/rest/` needs three headers. Omitting the version
header is an error — LinkedIn does not default to latest.

- `Authorization: Bearer {3-legged OAuth 2.0 member token}`
- `Linkedin-Version: {YYYYMM}` — see `lifecycle/linkedin-lifecycle.yml` for the current version
- `X-Restli-Protocol-Version: 2.0.0`

All identifiers are URNs (`urn:li:organization:1234`) and **must be URL-encoded** in paths and
query strings under Rest.li 2.0.0 — `:` becomes `%3A`.

Required permission: `w_organization_social` to publish, plus `rw_organization_admin` where the
flow reads administrative data. The member must hold the `ADMINISTRATOR` role on the page or the
call returns 403.

## Steps

1. **Resolve the organization** — `getLookupByOrganizationPrimary`. Take the organization URN from
   the response rather than trusting a URN passed in by the caller; a URN the member does not
   administer fails later with 403, which is harder to diagnose than a clean lookup miss.
2. **Publish the share** — `postCreateAShareWith`. The author is the organization URN from step 1.
   Set visibility explicitly: webhook events for `LIKE`, `COMMENT` and `SHARE` only fire for posts
   whose `visibility` is `PUBLIC` (see `asyncapi/linkedin-webhooks.yml`), so a post created with a
   narrower visibility will never generate engagement notifications.
3. **Verify** — `getGetPostsByUrn` with the URN returned by step 2. Treat the post as published
   only after this read succeeds. LinkedIn returns the created entity id in the `x-restli-id`
   response header on create calls.
4. **Amend or withdraw** — `postUpdateAPost` sends a Rest.li partial update
   (`X-RestLi-Method: PARTIAL_UPDATE`, body `{"patch": {"$set": {...}}}`) and returns `204`.
   `deleteDeleteAPost` removes it.

## Rules an agent must follow

- **There is no idempotency key.** LinkedIn documents no general-purpose idempotency header
  (`conventions/linkedin-conventions.yml`). A retried create publishes a second post. Never retry a
  create on a timeout — read back with `getGetPostsByUrn` first and only re-issue if nothing exists.
- **Errors are not RFC 9457.** The envelope is `{status, message, serviceErrorCode}`
  (`errors/linkedin-problem-types.yml`). Match on `serviceErrorCode`, not on prose.
- **401 vs 403 mean different things.** 401 = the member's grant to your application is gone and
  must be re-acquired. 403 = the member is no longer an administrator of that organization. Only
  the first is fixable by refreshing a token.
- **429 is a daily ceiling, not a burst.** Limits are per-application and per-member per UTC day and
  reset at 00:00 UTC (`rate-limits/linkedin-rate-limits.yml`). Backing off by seconds does not help;
  the retry window is the next day unless the app is on a higher tier.
- Pagination on any list is `start` / `count` with a `paging` object; the end of a dataset is fewer
  `elements` than the requested `count`, not an empty page.
