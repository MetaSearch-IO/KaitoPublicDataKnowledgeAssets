# Pre-TGE Projects List Contribution Guidelines

The Pre-TGE (Pre-Token Generation Event) projects list data is stored in `PreTGE_Project/PreTGE_Project.json`. Below is an example format:

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

To add or remove a Pre-TGE project, please edit the `PreTGE_Project.json` file using the format provided above and create a pull request.

## Adding a Pre-TGE Project

When adding a new Pre-TGE project, please ensure all required fields are filled:

- **ticker**: The project's ticker symbol (typically the project name in uppercase)
- **display_ticker**: How the ticker should be displayed (usually same as ticker)
- **fullname**: The full name of the project
- **twitter_handle**: The project's official Twitter/X handle (without the @ symbol)

### Finding Ticker Symbols and Display Ticker

For Pre-TGE projects, you may use the project's name in uppercase as the ticker symbol. You may assume the `ticker` field is identical to the `display_ticker` field when you submit a PR, and our data staff will help curate.

### Finding Fullname

The fullname should be the official project name as it appears on the project's website or official documentation. For example:
- Ticker: `FARCASTER` → Fullname: `Farcaster`
- Ticker: `METAMASK` → Fullname: `MetaMask`

### Finding Twitter Handle

The Twitter handle should be the project's official Twitter/X account username without the @ symbol. You can find this on:
- The project's official website
- The project's documentation
- Direct search on Twitter/X

Example: For Polymarket, the Twitter handle is `Polymarket` (from @Polymarket)

## Removing a Pre-TGE Project

To remove a Pre-TGE project, simply delete the corresponding entry from the JSON file. This might be necessary when:
- A project has completed its TGE (Token Generation Event)
- A project is no longer active
- A project was added by mistake

---

For questions or assistance, please create an issue in the repository.
