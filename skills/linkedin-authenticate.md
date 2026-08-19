---
name: Authenticate against the LinkedIn API
description: Obtain a LinkedIn access token via 3-legged OAuth 2.0 (member context) or 2-legged client credentials (application context), pin the API version, and keep tokens alive.
api: openapi/linkedin-authentication-api-openapi.yml
apis:
  - openapi/linkedin-authentication-api-openapi.yml
  - openapi/linkedin-sales-access-tokens-api-openapi.yml
operations:
  - getAccessToken
  - getSalesAccessToken
generated: '2026-08-13'
method: generated
source: openapi/*.yml, authentication/linkedin-authentication.yml, scopes/linkedin-scopes.yml, lifecycle/linkedin-lifecycle.yml
---

# Authenticate against the LinkedIn API

Every other LinkedIn skill depends on this one. Details in
`authentication/linkedin-authentication.yml` and `scopes/linkedin-scopes.yml`.

## Choosing a flow

- **3-legged (authorization code)** — anything that touches member or organization data. The token
  is bound to a specific member's grant and to the roles that member holds. This is the default.
- **2-legged (client credentials)** — application-context APIs only. It carries no member identity,
  so it cannot read a page the application was never granted.
- **Sign In with LinkedIn** is OpenID Connect: discovery lives at
  `https://www.linkedin.com/oauth/.well-known/openid-configuration` (captured verbatim at
  `well-known/linkedin-openid-configuration.json`), `id_token` is RS256, scopes `openid`, `profile`,
  `email`.

## Steps

1. Send the member to LinkedIn's authorization endpoint with your `client_id`, `redirect_uri`,
   `state` and the exact scopes the integration needs — nothing more. Over-scoping is the most
   common cause of a rejected app review.
2. Exchange the returned `code` at the token endpoint — `getAccessToken`.
3. Store the token with its expiry and the scope set it was actually granted. LinkedIn may grant a
   subset of what was requested; never assume the request equals the grant.
4. For Sales Navigator application flows, `getSalesAccessToken` issues the contract-scoped token.
5. On every subsequent call send all three headers:
   `Authorization: Bearer {token}`, `Linkedin-Version: {YYYYMM}`,
   `X-Restli-Protocol-Version: 2.0.0`.

## Rules an agent must follow

- **The version header is mandatory and has no default.** LinkedIn does not fall back to latest; a
  missing `Linkedin-Version` is an error, and a sunset version (e.g. `202507`) returns an error
  telling you to migrate. Each monthly version is supported for a minimum of 12 months
  (`lifecycle/linkedin-lifecycle.yml`).
- **401 means the grant is gone, not that the token is merely stale.** If a refresh does not
  restore access, the member revoked the application and must re-authorize. Any webhook
  subscriptions that member owned are already deleted.
- **403 means a missing role**, not a missing token — the member is no longer an administrator of
  the organization or lacks the ad account role. Refreshing credentials will never fix it.
- **Never send a member token to a non-LinkedIn host.** Media byte uploads go to a LinkedIn-issued
  upload URL with only the headers LinkedIn specifies; do not attach the bearer token there.
- Scopes are documented in `scopes/linkedin-scopes.yml`; each product line (Marketing, Talent,
  Learning, Sales Navigator, Compliance) is gated behind separate program approval on top of OAuth.
