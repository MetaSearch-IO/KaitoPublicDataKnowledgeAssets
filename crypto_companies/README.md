# Crypto Companies — Contribution Guidelines

This list backs the **Crypto Companies** leaderboards on [Kaito](https://kaito.ai).
If a company/project you expect is missing, or an entry has a wrong name or
Twitter handle, edit `crypto_companies/crypto_companies.json` and open a pull
request.

## Format

```json
[
    {
        "ticker": "UNI",
        "remarks": {
            "display_ticker": "UNI",
            "fullname": "Uniswap",
            "twitter_handle": "Uniswap"
        }
    }
]
```

- **ticker** — the token symbol exactly as tracked by Kaito, usually
  uppercase (e.g. `UNI`, `SOL`); a few legacy keys are mixed-case or contain
  spaces (e.g. `stETH`, `BabyDoge`) — keep existing keys unchanged. This is
  the primary key: one entry per ticker, and the file is sorted by it (ASCII
  ascending — uppercase sorts before lowercase). You can find symbols on
  CoinGecko, CoinMarketCap, or similar.
- **display_ticker** — how the ticker is displayed, usually the same as
  `ticker`.
- **fullname** — the project's official name (e.g. `Uniswap`).
- **twitter_handle** — the project's official X/Twitter handle, **without**
  the `@` prefix. Some seeded entries have an empty handle (for example `BTC`
  has no single official account) — PRs filling in correct handles are very
  welcome.

## Scope — make sure you are in the right file

| Your suggestion | Where it goes |
| --- | --- |
| Active, tradable token / company | **this file** |
| Pre-TGE project (no token yet) | [`PreTGE_Project/`](../PreTGE_Project) |
| Information-market project | [`information_markets/`](../information_markets) |
| Exchange on the Exchange Arena | [`Exchange_Arena/`](../Exchange_Arena) |

Notes:

- Only **active** tokens belong here. Delisted/inactive tokens are removed by
  the Kaito team.
- Sector tabs on the Crypto pages (DeFi, Gaming, ecosystems, …) are derived
  automatically from market data sources and are not curated in this file.
  If you believe a company is shown under the wrong sector, open an issue
  instead.

## Adding or fixing an entry

1. Edit `crypto_companies.json` — keep the file sorted by `ticker`.
2. Open a pull request. In the PR description, tell us **which Kaito page /
   sector** you were looking at when you noticed the gap.
3. CI validates the format automatically; the Kaito data team reviews.

## Removing an entry

Delete the entry and explain why in the PR (e.g. delisted, rebrand,
duplicate).

## What happens after merge

This repository collects public suggestions. After a PR is merged the Kaito
data team applies the change to Kaito's internal tagging systems; the product
pages update after that ingestion (usually within a few days, not instantly).
