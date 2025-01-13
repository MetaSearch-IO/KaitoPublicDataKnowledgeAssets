# Kaito Public Knowledge Base

This repository contains several static datasets utilized in Kaito.ai services.

## VC Affiliations

The VC Twitter affiliations are stored in `vc/vc_twitter_affiliation.json`. Below is an example format using @AlanaDLevin from Variant Fund:

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