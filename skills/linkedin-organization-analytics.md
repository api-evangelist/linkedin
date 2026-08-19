---
name: Pull organization page and share analytics
description: Resolve a LinkedIn organization, then collect its follower count, lifetime page statistics, time-bound follower and share statistics, and post-level engagement.
api: openapi/linkedin-use-cases-organization-lookup-organizations-api-openapi.yml
apis:
  - openapi/linkedin-use-cases-organization-lookup-organizations-api-openapi.yml
  - openapi/linkedin-use-cases-statistics-apis-organization-follower-statistics-api-openapi.yml
  - openapi/linkedin-use-cases-statistics-apis-organization-page-statistics-api-openapi.yml
  - openapi/linkedin-use-cases-statistics-apis-organization-share-statistics-api-openapi.yml
  - openapi/linkedin-feed-content-api-openapi.yml
  - openapi/linkedin-page-analytics-api-openapi.yml
operations:
  - getLookupByOrganizationPrimary
  - getRetrieveOrganizationFollowerCount
  - getLifetimePageStatistics
  - getTimeboundFollowerStatistics
  - getTimeBoundShareStatistics
  - getPageContentAnalytics
  - getPosts
  - getReactions
  - getComments
generated: '2026-08-13'
method: generated
source: openapi/*.yml, arazzo/linkedin-organization-profile-overview-workflow.yml, arazzo/linkedin-organization-follower-analytics-workflow.yml, arazzo/linkedin-export-post-engagement-workflow.yml
---

# Pull organization page and share analytics

## Headers and permissions

`Authorization: Bearer {member token}`, `Linkedin-Version: {YYYYMM}`,
`X-Restli-Protocol-Version: 2.0.0`. Reporting needs `r_organization_social` and
`rw_organization_admin`; the member must hold an admin or analyst role on the page.

## Steps

1. **Resolve** — `getLookupByOrganizationPrimary` to get the canonical organization URN. Every
   statistics call keys off this URN, URL-encoded.
2. **Snapshot** — `getRetrieveOrganizationFollowerCount` and `getLifetimePageStatistics` for the
   all-time picture.
3. **Time series** — `getTimeboundFollowerStatistics` and `getTimeBoundShareStatistics` with an
   explicit `timeRange.start` / `timeRange.end` in **epoch milliseconds**. Omitting the range does
   not mean "everything"; it changes the aggregation shape.
4. **Post level** — `getPosts` to enumerate the organization's posts, then `getReactions` and
   `getComments` per activity URN for engagement detail. `getPageContentAnalytics` covers page
   content performance.

## Rules an agent must follow

- **Time ranges are half-open.** `timeRange.start` is inclusive, `timeRange.end` is exclusive.
  Summing adjacent windows that share a boundary is correct; overlapping them double-counts.
- **Paginate with `start` / `count`.** Read `paging.total` where present, and stop when fewer
  `elements` come back than requested. Some newer finders use cursor tokens
  (`pageSize` / `pageToken` with `nextPageToken` in `metadata`) — check which the operation uses
  before writing a loop (`conventions/linkedin-conventions.yml`).
- **Analytics are asynchronous.** Recent windows may return partial or zero rows while data
  settles. Do not report a zero from the last few hours as a real zero.
- **Test ad accounts return nothing.** No `/adAnalytics` reporting data exists for test entities
  because impressions never occur (`sandbox/linkedin-sandbox.yml`).
- 429 is a per-day ceiling that resets at 00:00 UTC; analytics pulls are the most common way to hit
  it. Batch by organization and cache rather than re-querying per post.
