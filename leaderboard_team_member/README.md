# Project Leaderboard Team Members

`yapper_leaderboard_team_members.json` maps each project leaderboard ticker
to the X/Twitter accounts of that project's team members, so they can be
labeled (or excluded) on Yapper leaderboards.

```json
[
    {
        "ticker": "SOMNIA",
        "team_members": [
            {
                "twitter_user_name": "0xPaulThomas",
                "twitter_user_id": "1446133668913692674"
            }
        ]
    }
]
```

- **ticker** — the project's leaderboard ticker (uppercase).
- **team_members[].twitter_user_name** — the member's handle, without `@`.
- **team_members[].twitter_user_id** — the member's numeric X/Twitter user id
  (required — handles change, ids don't).

To add or remove team members, edit the JSON and open a pull request. Project
teams are welcome to submit their own roster updates; the Kaito team verifies
membership before merging.
