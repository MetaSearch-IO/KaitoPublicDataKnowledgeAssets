# Pre-IPO Companies — Contribution Guidelines

This list backs the **Pre-IPO Companies** leaderboard on [Kaito](https://kaito.ai).
If a company you expect is missing, or an entry has a wrong name or Twitter
handle, edit `preipo_companies/preipo_companies.json` and open a pull request.

## Format

```json
[
    {
        "symbol": "KRAKEN",
        "remarks": {
            "display_name": "Kraken",
            "fullname": "Payward, Inc.",
            "twitter_handle": "krakenfx"
        }
    }
]
```

- **symbol** — the company key used in this public list, usually the company
  name in uppercase with underscores for spaces. This is not a listed stock
  ticker.
- **display_name** — how the company is displayed.
- **fullname** — the company's official legal or commonly used full name.
- **twitter_handle** — the company's official X/Twitter handle, without the
  `@` prefix.

## Scope

Pre-IPO companies are private companies with a credible IPO signal or standing
pre-IPO market presence. Already-listed companies do not belong in this file.

## Adding or Fixing an Entry

1. Edit `preipo_companies.json` and keep entries sorted by `symbol`.
2. Open a pull request and explain which Kaito page or company gap prompted the
   change.
3. CI validates the JSON format; the Kaito data team reviews.

## What Happens After Merge

This repository collects public suggestions. After a PR is merged, the Kaito
data team applies the change to Kaito's internal tagging and universe systems;
product pages update after that ingestion, not instantly.
