---
name: Subscribe to organization social action webhooks
description: Register and validate a webhook, create an eventSubscriptions record for ORGANIZATION_SOCIAL_ACTION_NOTIFICATIONS, verify the subscription, handle the signed push payload, and backfill missed notifications through the pull finder.
api: openapi/linkedin-use-cases-social-actions-notifications-organization-social-actions-notifications-push-workflow-api-openapi.yml
apis:
  - openapi/linkedin-use-cases-social-actions-notifications-organization-social-actions-notifications-push-workflow-api-openapi.yml
  - openapi/linkedin-use-cases-social-actions-notifications-organization-social-actions-notifications-pull-workflow-api-openapi.yml
  - openapi/linkedin-use-cases-organization-access-controls-api-openapi.yml
operations:
  - getFindOrganizationAccessControl
  - putCreateASubscriptionRequest
  - getRetrieveSubscriptionByKey
  - deleteRemoveASubscription
  - getRetrieveNotificationsForThe
generated: '2026-08-13'
method: generated
source: openapi/*.yml, asyncapi/linkedin-webhooks.yml, arazzo/linkedin-subscribe-social-action-notifications-workflow.yml
---

# Subscribe to organization social action webhooks

Real-time engagement events for a Company Page. Full event catalog in
`asyncapi/linkedin-webhooks.yml`.

## Preconditions

- The developer application must have an **approved use case for webhooks** — the Webhooks tab in
  https://www.linkedin.com/developers/apps is otherwise hidden.
- The webhook URL must be **HTTPS**. ngrok URIs are explicitly unsupported.
- The subscribing member must hold `ADMINISTRATOR` on the organization and have granted
  `rw_organization_admin`.

## Steps

1. **Confirm access** — `getFindOrganizationAccessControl`. A subscription for an organization the
   member does not administer fails; check first.
2. **Pass the challenge.** LinkedIn issues `GET {webhook}?challengeCode={uuid}`. Reply within
   **3 seconds** with HTTP 200, `Content-Type: application/json`, body
   `{"challengeCode": ..., "challengeResponse": ...}` where
   `challengeResponse = Hex-encoded(HMACSHA256(challengeCode, clientSecret))`, lowercase hex.
   Parent-child integrations also receive `applicationId` — use that application's `clientSecret`.
   Re-validation runs every ~2 hours; **3 consecutive failures block the endpoint.**
3. **Create the subscription** — `putCreateASubscriptionRequest`, an upsert keyed by
   `(developerApplication, user, entity, eventType:ORGANIZATION_SOCIAL_ACTION_NOTIFICATIONS)` with
   body `{"webhook": "https://..."}`.
4. **Verify** — `getRetrieveSubscriptionByKey`. The response carries `expiresAt` and the registered
   `webhook`.
5. **Receive.** Each POST carries `X-LI-Signature`. Verify it:
   `stringToSign = "hmacsha256=" + <raw JSON body>`, then
   `Hex-encoded(HMACSHA256(stringToSign, clientSecret))`, compared in constant time. Hash the body
   **exactly as received** — any re-serialization breaks the signature. Return any 2xx.
6. **Backfill** — `getRetrieveNotificationsForThe` (the `organizationalEntityNotifications`
   criteria finder) covers gaps. Notifications are retained for **60 days**.
7. **Tear down** — `deleteRemoveASubscription`.

## Rules an agent must follow

- **Deduplicate on `notificationId`.** LinkedIn re-delivers every 5 minutes for up to 8 hours and
  states duplicates are expected. A handler without dedupe will double-process.
- **Payloads are batched, 10 per POST**, under `notifications[]` with `type` on the envelope.
- **Only `PUBLIC` posts generate `LIKE`, `COMMENT` and `SHARE` events.** A page whose posts are
  narrower in visibility will look silent, and that is not a bug.
- **Subscriptions die silently.** They are bound to the member's grant and admin role. A 401 from
  any organization call means the grant is gone (re-authorize, then resubscribe); a 403 means the
  member lost the admin role and can never resubscribe to that page. Track the timestamp of the
  last notification per member so the pull finder can close the gap.
- Actions to expect: `LIKE`, `COMMENT`, `SHARE`, `SHARE_MENTION`, `ADMIN_COMMENT`, `COMMENT_EDIT`,
  `COMMENT_DELETE`.
