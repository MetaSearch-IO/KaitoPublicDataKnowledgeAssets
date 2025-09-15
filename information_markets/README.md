# Information Markets Projects List Contribution Guidelines

The information markets projects list data is stored in `information_market/information_market_data.json`. Below is an example format:

```json
[
    {
        "ticker": "POLYMARKET",
        "remarks": {
            "display_ticker": "POLYMARKET",
            "fullname": "Polymarket",
            "username": "Polymarket"
        }
    },
    // additional entries here
]
```

To contribute new information, please use the format provided above and create a pull request.

### Finding Ticker Symbols and Display Ticker
You may find ticker symbols on CoinGecko, CoinMarketCap, or other similar websites. For example, the ticker symbol for Bitcoin is `BTC`, and for Ethereum, it is `ETH`.
If the project is pre-TGE, you may use the project's name in uppercase as the ticker symbol. You may assume `ticker` field is identical to `display_ticker` field when you submit PR and our data staff will help curate.

### Finding Fullname
You may find the fullname on CoinGecko, CoinMarketCap, or other similar websites. For example, the fullname for Bitcoin is `Bitcoin`, and for Ethereum, it is `Ethereum`.

---