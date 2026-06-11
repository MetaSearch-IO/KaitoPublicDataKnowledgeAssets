# Kaito Public Knowledge Base

Static datasets used by [Kaito.ai](https://kaito.ai) products, **open for
public contributions** — if you spot a missing company, a wrong Twitter
handle, or an outdated entry, submit a pull request.

## What do you want to suggest?

| You want to… | Edit this |
| --- | --- |
| Add/fix a company on the **Crypto Companies** leaderboards | [`crypto_companies/`](crypto_companies) |
| Add/fix a company on the **AI Companies** leaderboards | [`ai_companies/`](ai_companies) |
| Propose a **new AI category** | [`ai_companies/categories.json`](ai_companies/categories.json) (with ≥8 companies, see folder README) |
| Add/remove a **Pre-TGE** project | [`PreTGE_Project/`](PreTGE_Project) |
| Add/remove an **Information Market** project | [`information_markets/`](information_markets) |
| Add/remove an exchange on the **Exchange Arena** | [`Exchange_Arena/`](Exchange_Arena) |
| Add/fix **VC / GP affiliations** | [`vc/`](vc) |
| Update a project's **team members** on leaderboards | [`leaderboard_team_member/`](leaderboard_team_member) |

Each folder has a README with the exact JSON format and rules.

## How contributions work

1. Edit the relevant JSON file and open a pull request. In the PR
   description, mention **which Kaito page / arena / sector** you were
   looking at — entries are surfaced per arena, so this matters.
2. CI validates the JSON format automatically on every PR.
3. The Kaito data team reviews and merges. Merged changes are then applied
   to Kaito's internal systems and show up on the product after ingestion.
