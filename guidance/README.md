# Guidance List Contribution Guidelines

The Guidance list data is stored in `guidance/guidance.json`. Below is an example format:

```json
[
    {
        "ticker": "POLYMARKET",
        "remarks": {
            "display_ticker": "POLYMARKET",
            "fullname": "Polymarket",
            "twitter_handle": "Polymarket"
        }
    },
    // additional entries here
]
```

To add or remove an entry, please edit the `guidance.json` file using the format provided above and create a pull request.

## Adding an Entry

When adding a new entry, please ensure all required fields are filled:

- **ticker**: The ticker symbol (typically the name in uppercase)
- **display_ticker**: How the ticker should be displayed (usually same as ticker)
- **fullname**: The full name
- **twitter_handle**: The official Twitter/X handle (without the @ symbol)

## Removing an Entry

To remove an entry, simply delete the corresponding entry from the JSON file.

---

For questions or assistance, please create an issue in the repository.
