---
name: Sync leads from LinkedIn lead gen forms
description: Validate the member's organization access, enumerate lead gen forms, subscribe a validated webhook for LEAD_ACTION notifications, and fetch full lead data as leads arrive.
api: openapi/linkedin-use-cases-sponsored-api-openapi.yml
apis:
  - openapi/linkedin-use-cases-sponsored-api-openapi.yml
  - openapi/linkedin-lead-generation-api-openapi.yml
operations:
  - getValidateTheUsersOrganization
  - getGetTheUsersSponsored
  - getGetFormsForThe
  - postSubscribeForLeadNotification
  - getFetchFullLeadData
  - getSchedulePeriodicFormResponse
  - deletePushDeleteARegistered
  - getLeadGenResponses
generated: '2026-08-13'
method: generated
source: openapi/*.yml, asyncapi/linkedin-webhooks.yml, https://learn.microsoft.com/en-us/linkedin/marketing/lead-sync/leadsync
---

# Sync leads from LinkedIn lead gen forms

Leads are personal data. Everything below is subject to LinkedIn's API terms and the customer's own
consent obligations — do not cache lead payloads beyond what the integration needs.

## Headers and permissions

`Authorization: Bearer {token}`, `Linkedin-Version: {YYYYMM}`,
`X-Restli-Protocol-Version: 2.0.0`. Requires `r_marketing_leadgen_automation`, which also governs
managing `leadNotifications`. For **sponsored** leads the member needs an ad account role
(`ACCOUNT_BILLING_ADMIN`, `ACCOUNT_MANAGER`, `CAMPAIGN_MANAGER`, `CREATIVE_MANAGER`, `VIEWER`) plus
a company page role. For **organic** leads a page role is required, and Event leads specifically
require `ADMINISTRATOR` or `CONTENT_ADMINISTRATOR` — the other page roles do not suffice.

## Steps

1. **Validate access** — `getValidateTheUsersOrganization` and `getGetTheUsersSponsored` to
   establish which organizations and sponsored accounts the member can pull leads for.
2. **Enumerate forms** — `getGetFormsForThe` for the lead gen forms under that owner.
3. **Register and validate a webhook** — same HMAC challenge flow as every LinkedIn webhook
   (`asyncapi/linkedin-webhooks.yml`). **Since 16 March 2026 LinkedIn only pushes new lead
   notifications to validated webhooks**, and only HTTPS URLs are accepted. Lead Sync subscriptions
   cannot be created in the portal UI — they must go through the API.
4. **Subscribe** — `postSubscribeForLeadNotification` (`POST /rest/leadNotifications`). Subscribe at
   **owner level** (`{"webhook", "owner", "leadType"}`) unless the integration genuinely needs
   per-form or per-entity URLs; LinkedIn recommends owner level so one record covers the owner.
   Form level takes `versionedForm`, entity level takes `associatedEntity`.
5. **Handle the push.** Payload fields: `type` (always `LEAD_ACTION`), `leadGenFormResponse`,
   `owner`, `associatedEntity`, `leadGenForm`, `leadType`, `leadAction` (`CREATED` or `DELETED`),
   `occurredAt`. Verify `X-LI-Signature` before trusting any of it.
6. **Fetch the lead** — `getFetchFullLeadData` with the `leadGenFormResponse` URN. The notification
   carries URNs, not field answers.
7. **Reconcile** — `getLeadGenResponses` / `getSchedulePeriodicFormResponse` for periodic pulls that
   cover webhook downtime.
8. **Unsubscribe** — `deletePushDeleteARegistered`.

## Rules an agent must follow

- **Deduplicate.** LinkedIn states explicitly that lead notifications can be delivered more than
  once and the application **must** dedupe. Key on `leadGenFormResponse` + `leadAction`.
- **`leadAction: DELETED` is a deletion instruction**, not an error — it fires when a member
  unregisters (e.g. from an event). Propagate the delete downstream; ignoring it leaves the CRM
  holding a record the member withdrew.
- **Do not poll as a substitute for subscribing.** The periodic finders exist for gap-filling; a
  polling loop over lead endpoints is the fastest way to burn the daily quota and get 429s that do
  not clear until 00:00 UTC.
- Errors return `{status, message, serviceErrorCode}`. A 401 on a lead call usually means the
  member lacks the form/lead permission rather than a bad token — check the role table before
  refreshing credentials.
