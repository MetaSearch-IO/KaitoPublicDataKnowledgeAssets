# VC Affiliations Contribution Guidelines

The VC Twitter affiliations are stored in two files in this directory:

- **`vc/vc_twitter_affiliations.json`** — the user-to-firm edges (one Twitter user_id → array of VC firm Twitter user_ids). The example below shows this file's format.
- **`vc/vc_firms.json`** — display metadata for each firm referenced by `vc_affiliations[]` (mirrors the `Exchange_Arena/Exchange_Arena.json` pattern). Required fields: `twitter_user_id`, `remarks.twitter_handle`, `remarks.display_name`. Optional: `remarks.fullname`, `remarks.website`. **Every firm Twitter user_id used in `vc_twitter_affiliations.json` MUST have a corresponding entry in `vc_firms.json`.**

## `vc_twitter_affiliations.json` format

Below is an example format using @AlanaDLevin from Variant Fund:

```json
[
    {
        "twitter_user_id": "1347640337070755851",
        "vc_affiliations": [
            "1183940649260847105"
        ],
        "remarks": {
            "twitter_username": "AlanaDLevin",
            "vc_affiliation_usernames": [
                "variantfund"
            ]
        }
    }
    // additional entries here
]
```

To contribute a new VC affiliation, please use the format provided above and create a pull request.

### Finding Twitter User IDs

If you are a Kaito Metasearch user, follow these steps to find a Twitter user ID:

1. Navigate to the "Smart Following" panel in the [Metasearch Portal](https://portal.kaito.ai/smart_following).
2. Use the search bar at the top-right corner to locate the Twitter user, click on the user to view their detail page.
3. The Twitter user ID is included in the URL in the browser's address bar (e.g., for URL `https://portal.kaito.ai/smart_following/emerging/169686021`, the Twitter user ID is `169686021`).

If Kaito Metasearch is unavailable, consider using the following public services:

- [Twitter ID Finder](https://twiteridfinder.com/)
- [Tweet Hunter's ID Converter](https://tweethunter.io/twitter-id-converter)
- [ILO Twitter ID](https://ilo.so/twitter-id/)

Note that these services might experience downtime. If necessary, search for alternatives using "Twitter user ID" in search engines.

---