# LinkedIn GraphQL Schema

## Overview

LinkedIn does not expose a native public GraphQL API. All LinkedIn developer APIs are REST-based, documented at [https://learn.microsoft.com/en-us/linkedin/](https://learn.microsoft.com/en-us/linkedin/), and organized into seven product lines:

- **Consumer API** — Sign In with LinkedIn, Share on LinkedIn, Verified on LinkedIn
- **Marketing API** — Ad campaigns, audiences, conversions, analytics, lead gen
- **Talent Solutions** — Job posting, recruiter system connect, candidate management
- **Learning Solutions** — Activity reports, content access, xAPI integration
- **Sales Navigator API** — CRM sync, display services, sales analytics
- **Compliance Solutions** — Message archiving, activity monitoring
- **Regulatory API** — Data portability, advertiser transparency (DMA)

## Schema Design Notes

The conceptual GraphQL schema in `linkedin-schema.graphql` is derived from the LinkedIn REST API surface and data models documented at:

- [LinkedIn Consumer API](https://learn.microsoft.com/en-us/linkedin/consumer/)
- [LinkedIn Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [LinkedIn Talent Solutions](https://learn.microsoft.com/en-us/linkedin/talent/)
- [LinkedIn Sales Navigator](https://learn.microsoft.com/en-us/linkedin/sales/)
- [LinkedIn Compliance](https://learn.microsoft.com/en-us/linkedin/compliance/)
- [LinkedIn Regulatory API](https://learn.microsoft.com/en-us/linkedin/dma/)
- [Profile API Reference](https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api)
- [GitHub: linkedin-developers](https://github.com/linkedin-developers)

## Domain Coverage

### Member and Profile

Types covering the LinkedIn member identity, professional profile, and profile subsections as exposed through the Profile API and Consumer solutions.

- `Member` — core member identity and URN
- `Profile` — full public or permissioned profile record
- `Headline` — professional headline string attached to a profile
- `Positions` — current and past work experience collection
- `Education` — academic history entries
- `Skills` — skill endorsement list
- `Recommendations` — given and received recommendations
- `CertificationEntry` — individual certification record
- `HonorEntry` — honor or award record
- `PublicationEntry` — authored publications
- `PatentEntry` — patent filings
- `CourseEntry` — completed courses
- `ProjectEntry` — project portfolio entries
- `VolunteerExperience` — volunteer history
- `Language` — language proficiency entries
- `OpenToWork` — open-to-work signal metadata

### Network and Relationships

Types for representing the LinkedIn professional graph and relationship layers.

- `Connections` — first-degree connection list
- `Following` — entities (members, companies) being followed
- `Network` — member's network summary
- `Degree` — connection degree between two members
- `InvitationTo` — pending or sent connection invitation
- `InMail` — InMail message capability and metadata

### Company and Organization

Types derived from LinkedIn's Organization APIs used across Marketing, Talent, and Consumer solutions.

- `Company` — organization entity record
- `CompanyPage` — LinkedIn Company Page with follower and post data
- `ProductPage` — product page attached to a company
- `Showcase` — showcase page beneath a company
- `Organization` — generic organization entity (parent of Company, School, etc.)
- `School` — educational institution entity

### Content and Engagement

Types for posts, shares, articles, and social engagement signals.

- `Post` — single content post (text, image, video, document)
- `Share` — reshare of existing content
- `Article` — long-form LinkedIn article (Pulse)
- `Event` — LinkedIn live or virtual event

### Messaging and Communication

Types for LinkedIn messaging, conversations, and notifications.

- `Conversation` — messaging thread between members
- `Message` — individual message within a conversation
- `Notification` — activity notification record

### Jobs and Talent

Types derived from the Talent Solutions job posting and recruiter APIs.

- `JobPosting` — job listing published on LinkedIn
- `JobApplication` — application submitted to a job posting

### Community and Groups

- `Group` — LinkedIn Group entity

### Insights and Analytics

Types covering Marketing, Sales Navigator, and page analytics data models.

- `Insight` — analytics insight record
- `Analytics` — aggregated metric result set
- `ProfileView` — profile view event record
- `SearchResult` — member or entity search result
- `ServiceProvider` — listed service provider record

### Marketing and Advertising

Types covering the LinkedIn Marketing API campaign and ad structure.

- `AdAccount` — advertiser account
- `Campaign` — ad campaign
- `CampaignGroup` — grouping of campaigns
- `Creative` — ad creative asset
- `Audience` — targeting audience definition
- `AudienceInsight` — aggregated audience demographic data
- `Conversion` — conversion event record
- `LeadGenForm` — lead generation form
- `LeadGenFormResponse` — submitted lead gen form entry
- `AdAnalytics` — campaign-level analytics metrics

### Sales Navigator

Types from the Sales Navigator CRM sync and display service APIs.

- `SalesAccount` — CRM account record synced with Sales Navigator
- `SalesLead` — lead record in Sales Navigator
- `CrmSync` — CRM synchronization state

### Learning

Types for LinkedIn Learning content and activity reporting.

- `LearningCourse` — a LinkedIn Learning course
- `LearningActivity` — learner activity record (start, completion)

### Compliance

Types for message archiving and compliance monitoring.

- `ArchivedMessage` — archived compliance message record
- `ComplianceEvent` — compliance event record

## Type Count

This schema defines **72 types** including query types, enumerations, and scalar extensions.

## Usage

This is a conceptual schema only. LinkedIn does not provide a GraphQL endpoint. The schema can be used for:

1. Generating mock servers that mirror LinkedIn data shapes
2. API gateway GraphQL-to-REST translation layers
3. Client-side type generation for applications consuming LinkedIn REST APIs
4. Documentation and data modeling reference
