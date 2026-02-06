# CEX Arena (Cryptocurrency Exchange) List Contribution Guidelines

The CEX Arena list data is stored in `CEX_Arena/CEX_Arena.json`. This list tracks major cryptocurrency exchanges (both centralized and decentralized) and their associated platform tokens. Below is an example format:

```json
[
    {
        "ticker": "BNB",
        "remarks": {
            "display_ticker": "BINANCE",
            "fullname": "Binance",
            "twitter_handle": "BNBCHAIN"
        }
    },
    {
        "ticker": "COINBASE",
        "remarks": {
            "display_ticker": "COINBASE",
            "fullname": "Coinbase",
            "twitter_handle": "Coinbase"
        }
    },
    // additional entries here
]
```

To add or remove an exchange, please edit the `CEX_Arena.json` file using the format provided above and create a pull request.

## Adding a Cryptocurrency Exchange

When adding a new exchange, please ensure all required fields are filled:

- **ticker**: The exchange's official platform token symbol (e.g., `BNB` for Binance, `MX` for MEXC). If the exchange does not have a platform token, use the exchange name in uppercase (e.g., `COINBASE`, `KRAKEN`)
- **display_ticker**: How the ticker should be displayed, typically the exchange name in uppercase (e.g., `BINANCE`, `KUCOIN`, `COINBASE`)
- **fullname**: The official name of the exchange (e.g., `Binance`, `KuCoin`, `Coinbase`)
- **twitter_handle**: The exchange's official Twitter/X handle (without the @ symbol)

### Understanding the Ticker Field

The `ticker` field represents the exchange's **official platform token**, not the exchange itself:

- **Exchanges WITH platform tokens**:
  - Binance issues BNB → ticker: `BNB`, fullname: `Binance`
  - MEXC issues MX → ticker: `MX`, fullname: `MEXC`
  - KuCoin issues KCS → ticker: `KCS`, fullname: `KuCoin`
  - Bitget issues BGB → ticker: `BGB`, fullname: `Bitget`
  - Gate.io issues GT → ticker: `GT`, fullname: `Gate`

- **Exchanges WITHOUT platform tokens**:
  - Coinbase → ticker: `COINBASE`, fullname: `Coinbase`
  - Kraken → ticker: `KRAKEN`, fullname: `Kraken`
  - Bybit → ticker: `BYBIT`, fullname: `Bybit`

### Finding Display Ticker

The `display_ticker` should represent how the exchange is commonly known:
- Usually the exchange name in uppercase
- Example: `BNB` token → display_ticker: `BINANCE`
- Example: `COINBASE` → display_ticker: `COINBASE`


### Finding Fullname

The fullname should be the official exchange name as it appears on:
- The exchange's official website
- The exchange's branding materials
- Official documentation

Examples:
- Ticker: `BNB` → Fullname: `Binance`
- Ticker: `DYDX` → Fullname: `dYdX`
- Ticker: `COINBASE` → Fullname: `Coinbase`

### Finding Twitter Handle

The Twitter handle should be the exchange's official Twitter/X account username without the @ symbol. You can find this on:
- The exchange's official website (usually in the footer)
- The exchange's documentation
- Direct search on Twitter/X (look for verified accounts)

Example: For Binance, the Twitter handle is `binance` (from @binance)

## Exchange Categories

This list includes various types of exchanges:

1. **Centralized Exchanges (CEX)**: Binance, Coinbase, OKX, Bybit, KuCoin, Gate.io, MEXC, HTX, Kraken, Upbit, Bithumb
2. **Decentralized Perpetual Exchanges**: dYdX, Hyperliquid, Jupiter, Drift, Paradex, SynFutures, Avantis, Lighter, Aster
3. **Decentralized Spot Exchanges**: Orderly Network
4. **Hybrid/DeFi Trading Platforms**: Aevo, Flipster, Ostium Labs

## Removing an Exchange

To remove an exchange, simply delete the corresponding entry from the JSON file. This might be necessary when:
- An exchange has shut down operations
- An exchange is no longer relevant or active
- An exchange was added by mistake
- An exchange no longer meets the inclusion criteria

---

For questions or assistance, please create an issue in the repository.
