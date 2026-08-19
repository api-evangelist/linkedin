---
name: Create and manage ad accounts, campaigns and creatives
description: Stand up a LinkedIn Marketing API ad account (including a test account), search and manage campaign groups and campaigns, create creatives, and size an audience before spending.
api: openapi/linkedin-account-management-api-openapi.yml
apis:
  - openapi/linkedin-account-management-api-openapi.yml
  - openapi/linkedin-user-access-api-openapi.yml
  - openapi/linkedin-campaign-group-management-api-openapi.yml
  - openapi/linkedin-campaign-management-api-openapi.yml
  - openapi/linkedin-creative-management-api-openapi.yml
  - openapi/linkedin-audience-counts-api-openapi.yml
  - openapi/linkedin-ad-targeting-entities-api-openapi.yml
operations:
  - createAdAccount
  - searchAdAccounts
  - getAdAccountById
  - updateAdAccount
  - createAdAccountUser
  - getAuthenticatedUserAdAccounts
  - searchCampaignGroups
  - getCampaignGroupById
  - updateCampaignGroup
  - deleteCampaignGroup
  - searchCampaigns
  - getCampaignById
  - archiveCampaign
  - createCreative
  - getAudienceCount
  - getAdTargetingFacets
  - searchAdTargetingEntities
generated: '2026-08-13'
method: generated
source: openapi/*.yml, sandbox/linkedin-sandbox.yml, conventions/linkedin-conventions.yml
---

# Create and manage ad accounts, campaigns and creatives

This flow spends money. Read the test-account rules before an agent writes anything.

## Headers and permissions

`Authorization: Bearer {token}`, `Linkedin-Version: {YYYYMM}`,
`X-Restli-Protocol-Version: 2.0.0`. Needs `rw_ads` to write, `r_ads` to read. The acting user must
hold one of `ACCOUNT_BILLING_ADMIN`, `ACCOUNT_MANAGER`, `CAMPAIGN_MANAGER`, `CREATIVE_MANAGER`;
`VIEWER` is read-only even with `rw_ads`.

## Steps

1. **Find or create the account** — `getAuthenticatedUserAdAccounts` lists what the member can
   reach; `searchAdAccounts` filters by `status`, `type`, `name`, `id`, `reference`, `test`.
   `createAdAccount` requires `type: BUSINESS` (`ENTERPRISE` cannot be created through the API).
2. **Develop against a test account.** Add `"test": true` on create. It is **immutable** — an
   existing account can never become a test account — and there is a hard limit of **one test
   account per developer application**. Test creatives never serve, are auto-rejected in review,
   require no billing details, return no `/adAnalytics` data, and cannot upload audience segments.
   Full behavior and error codes in `sandbox/linkedin-sandbox.yml`.
3. **Grant seats** — `createAdAccountUser`, then `getAdAccountUser` / `updateAdAccountUser` /
   `deleteAdAccountUser` to manage them.
4. **Size the audience before you build** — `getAdTargetingFacets` for the available facets,
   `searchAdTargetingEntities` to typeahead-resolve entity URNs, `getAudienceCount` to check the
   targeting criteria reach. A campaign targeting below LinkedIn's minimum audience will not serve.
5. **Structure** — `searchCampaignGroups` / `getCampaignGroupById` / `updateCampaignGroup`, then
   `searchCampaigns` / `getCampaignById`. Retire with `archiveCampaign` rather than deleting.
6. **Creatives** — `createCreative` against the campaign. Media must already be uploaded and
   verified (see the upload-media skill).

## Rules an agent must follow

- **Writes are Rest.li partial updates.** `POST` with `X-RestLi-Method: PARTIAL_UPDATE` and a body
  of `{"patch": {"$set": {...}}}`; success is `204 No Content`, not a body. Do not PUT a whole
  object expecting a merge.
- **There is no idempotency key.** A retried `createAdAccount` or `createCreative` creates a second
  object. Search first, create once, and never blind-retry a write.
- **`search.test` is a scalar.** Every other search field uses `(values:List(...))`; `test` takes
  `test:true` / `test:false` directly. Finders return both test and production entities unless
  filtered — an agent that forgets this will mix test campaigns into a production report.
- **Deleting an account is two-stage.** `DELETE` works only on `DRAFT`; anything else must be
  patched to `status: PENDING_DELETION`, and only the billing admin may do it.
- Created ids come back in the `x-restli-id` response header.
- Cursor pagination on `adAccounts` uses `pageSize` (max 1000) and `pageToken`, with
  `nextPageToken` under `metadata` — not `start`/`count`.
- Ceilings are per-day per application and per member, reset 00:00 UTC; Development tier is lower
  than Standard. 429 is not a burst signal (`rate-limits/linkedin-rate-limits.yml`).
