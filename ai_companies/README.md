# AI Companies — Contribution Guidelines

This list backs the **AI Companies** leaderboards on [Kaito](https://kaito.ai).
If a company you expect is missing, an entry is wrong, or a whole category is
missing, edit the files in this folder and open a pull request.

Two files:

- **`ai_companies.json`** — the companies.
- **`categories.json`** — the category (sub-sector) registry that
  `ai_companies.json` entries may reference.

## `ai_companies.json` format

```json
[
    {
        "symbol": "OPENAI",
        "remarks": {
            "display_name": "OpenAI",
            "fullname": "OpenAI",
            "twitter_handle": "OpenAI",
            "categories": ["coding_agents", "foundation_model"]
        }
    }
]
```

- **symbol** — the company name in uppercase, with underscores for spaces
  (e.g. `OPENAI`, `BLACK_FOREST_LABS`). This is the primary key: one entry
  per symbol, file sorted by it (ASCII ascending).
- **display_name** — how the company is displayed (e.g. `OpenAI`).
- **fullname** — the company's official name.
- **twitter_handle** — the company's official X/Twitter handle, **without**
  the `@` prefix. Some seeded entries have an empty handle — PRs filling in
  correct handles are very welcome.
- **categories** — which AI sub-sector views the company belongs on. Every
  value must be an **active** slug from `categories.json`. An empty array
  means the company appears only on the **All** view.

### One entry per company, not per product

List companies/organizations, not their individual models or products —
e.g. `OPENAI`, not `GPT`/`DALLE`/`SORA`. Product mindshare is consolidated
into the parent company by Kaito's internal pipeline.

## `categories.json` format — proposing a new category

```json
[
    {
        "slug": "foundation_model",
        "display_name": "Foundation Models",
        "status": "active"
    }
]
```

To propose a **new category**: add it to `categories.json` **and, in the same
PR, add or update at least 8 companies** in `ai_companies.json` carrying the
new slug. Categories with only a handful of companies make for empty
leaderboards, so proposals below that bar will be asked to either broaden the
category or fold into an existing one. The Kaito product team has the final
say on which categories ship as product tabs.

## Adding or fixing an entry

1. Edit `ai_companies.json` — keep the file sorted by `symbol`.
2. Open a pull request. In the PR description, tell us **which Kaito page /
   category** you were looking at when you noticed the gap.
3. CI validates the format automatically; the Kaito data team reviews.

## What happens after merge

This repository collects public suggestions. After a PR is merged the Kaito
data team applies the change to Kaito's internal tagging systems; the product
pages update after that ingestion (usually within a few days, not instantly).
