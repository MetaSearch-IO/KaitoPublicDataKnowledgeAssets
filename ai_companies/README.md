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

- **symbol** — the entity name in uppercase, with underscores for spaces
  (e.g. `OPENAI`, `BLACK_FOREST_LABS`; a few keys contain dots, like
  `A0.DEV`). This is the primary key: one entry per symbol, file sorted by
  it (ASCII ascending — uppercase sorts before lowercase).
- **display_name** — how the company is displayed (e.g. `OpenAI`).
- **fullname** — the company's official name.
- **twitter_handle** — the company's official X/Twitter handle, **without**
  the `@` prefix. Some seeded entries have an empty handle — PRs filling in
  correct handles are very welcome.
- **categories** — which AI sub-sector views the company belongs on. Every
  value must be an **active** slug from `categories.json`. An empty array
  means the company appears only on the **All** view.

### One entry per tracked entity — don't add products of listed companies

If a company is already listed, do **not** add its individual models or
products as separate entries — e.g. `OPENAI` is listed, so `GPT`, `DALLE`
and `SORA` are not; their mindshare is consolidated into OpenAI by Kaito's
internal pipeline.

You will see some standalone model/product names in the list (e.g. `LLAMA`,
`ERNIE`, `VEO`): those are tracked as top-level entities because their
parent company is not part of the AI leaderboards (Meta, Baidu and Google
are tracked in other verticals). That is intentional — leave them as-is.

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
