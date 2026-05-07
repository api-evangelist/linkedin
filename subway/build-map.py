#!/usr/bin/env python3
"""Build the LinkedIn API tube-style map.

17 APIs grouped onto 5 product lines. Mixed shapes: a wave across the
top, a long concave-up arc, a J-shape, a short diagonal sweep, and a
*closed* triangular loop for Compliance & Regulatory.
"""

import sys
from pathlib import Path

sys.path.insert(0, "/Users/kinlane/GitHub/all/.claude/skills")
from _subway_engine import build_subway  # noqa: E402

ABBREV = {
    "Recruiter System Connect": "Recruiter Connect",
    "Learning Parent Application": "Learning Parent App",
    "Learning Activity Reports": "Learning Reports",
    "Marketing Audience Insights": "Audience Insights",
}

LINES = [
    {
        "name": "Marketing — Audience",
        "color": "#E0245E",   # central-line red
        # Sine wave across the top.
        "stations": [
            ("Audience",         (270, 195)),
            ("Audience Insights",(450, 160)),
            ("Community",        (640, 195)),
            ("Conversions",      (820, 160)),
        ],
    },
    {
        "name": "Marketing — Campaigns & Content",
        "color": "#E68B1F",   # orange
        # Concave-up arc — middle stations sit higher than the endpoints.
        "stations": [
            ("Campaigns",      (260, 330)),
            ("Content",        (430, 290)),
            ("Leads",          (610, 280)),
            ("Media Planning", (790, 290)),
            ("Reporting ROI",  (970, 330)),
        ],
    },
    {
        "name": "Talent",
        "color": "#0E9D6E",   # forest green
        # J-shape: vertical drop then 45° bend right at the bottom.
        "stations": [
            ("Job Posting",                  (260, 440)),
            ("Recruiter System Connect",     (260, 530)),
            ("Learning Parent Application",  (350, 600)),
        ],
    },
    {
        "name": "Sales & Learning",
        "color": "#7B3FE4",   # purple
        # Short diagonal sweep across the middle.
        "stations": [
            ("Sales Navigator",         (490, 465)),
            ("Learning Activity Reports",(670, 540)),
        ],
    },
    {
        "name": "Compliance & Regulatory",
        "color": "#5A6275",   # slate
        # Closed loop — three stations form a rounded triangle.
        "closed": True,
        "stations": [
            ("Compliance Events",      (840, 590)),
            ("Data Portability",       (940, 690)),
            ("Ads Transparency",       (760, 720)),
        ],
    },
]

# apis.io URLs use the openapi filename, not the {provider}-{name}-api template.
URL_OVERRIDES = {
    "Audience":                    "https://apis.apis.io/apis/linkedin/linkedin-marketing-audience/",
    "Audience Insights":           "https://apis.apis.io/apis/linkedin/linkedin-marketing-audience-insights/",
    "Campaigns":                   "https://apis.apis.io/apis/linkedin/linkedin-marketing-campaigns/",
    "Community":                   "https://apis.apis.io/apis/linkedin/linkedin-marketing-community/",
    "Content":                     "https://apis.apis.io/apis/linkedin/linkedin-marketing-content/",
    "Conversions":                 "https://apis.apis.io/apis/linkedin/linkedin-marketing-conversions/",
    "Leads":                       "https://apis.apis.io/apis/linkedin/linkedin-marketing-leads/",
    "Media Planning":              "https://apis.apis.io/apis/linkedin/linkedin-marketing-media-planning/",
    "Reporting ROI":               "https://apis.apis.io/apis/linkedin/linkedin-marketing-reporting-roi/",
    "Job Posting":                 "https://apis.apis.io/apis/linkedin/linkedin-talent-job-posting/",
    "Recruiter System Connect":    "https://apis.apis.io/apis/linkedin/linkedin-talent-recruiter-system-connect/",
    "Learning Parent Application": "https://apis.apis.io/apis/linkedin/linkedin-talent-learning-parent-application/",
    "Sales Navigator":             "https://apis.apis.io/apis/linkedin/linkedin-sales-navigator/",
    "Learning Activity Reports":   "https://apis.apis.io/apis/linkedin/linkedin-learning-activity-reports/",
    "Compliance Events":           "https://apis.apis.io/apis/linkedin/linkedin-compliance-events/",
    "Data Portability":            "https://apis.apis.io/apis/linkedin/linkedin-regulations-data-portability/",
    "Ads Transparency":            "https://apis.apis.io/apis/linkedin/linkedin-regulatory-ads-transparency/",
}


def main():
    seen = set()
    n_unique = 0
    for ln in LINES:
        for (st, _) in ln["stations"]:
            if st not in seen:
                n_unique += 1
                seen.add(st)

    build_subway(
        title="The LinkedIn API · Underground Map",
        subtitle=f"{n_unique} APIs · {len(LINES)} functional lines · "
                 f"click any station for the apis.io page",
        lines=LINES,
        abbrev=ABBREV,
        source_label="Source: linkedin/openapi/*.yml · github.com/api-evangelist/linkedin",
        out_dir=Path(__file__).resolve().parent,
        out_basename="linkedin-subway-map",
        provider_id="linkedin",
        station_url_overrides=URL_OVERRIDES,
    )


if __name__ == "__main__":
    main()
