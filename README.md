# **Binance Futures Testnet Trading Bot (CLI + Python)**

A lightweight trading bot built in Python that interacts with the **Binance USDT-M Futures Testnet**.
Supports **MARKET** and **LIMIT** orders, full request signing (HMAC-SHA256), safe logging, error handling, and a CLI interface for placing, checking, and cancelling orders.

---

## ## **Features**

- Connects to **Binance Futures Testnet (USDT-M)**
- Fully signed REST requests using HMAC-SHA256
- Place **MARKET** and **LIMIT** orders
- Supports **BUY** and **SELL** sides
- Check order status
- Cancel active orders
- CLI interface built using Click
- Logging: console + rotating log file (`bot.log`)
- Environment-variable based configuration
- Automatic timestamping, recvWindow, and parameter validation

---

## **Project Structure**

```
binance_bot/
│
├── bot.py              # Core trading client (order placement, cancellation, status)
├── utils.py            # Signing utilities and helper functions
├── cli.py              # CLI interface (place, status, cancel)
├── logging_config.py   # Logging setup
├── .env                # Environment variables (not committed to VCS)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## **Requirements**

- Python 3.10+
- Binance Futures Testnet Account
- API Key & Secret
- Basic understanding of futures trading (testnet only)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **Environment Variables**

Create a `.env` file in the project root:

```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
BINANCE_TESTNET_BASE=https://testnet.binancefuture.com
```

> Important: Never expose your API secret or commit `.env` to source control.

---

## **Running the Bot**

Activate your virtual environment:

```bash
.\venv\Scripts\activate
```

---

## ### **1. Place an Order**

### MARKET order:

```bash
python cli.py place --symbol BTCUSDT --side BUY --quantity 0.002 --type MARKET
```

### LIMIT order:

```bash
python cli.py place --symbol BTCUSDT --side SELL --quantity 0.002 --type LIMIT --price 60000
```

---

## ### **2. Check Order Status**

```bash
python cli.py status --symbol BTCUSDT --order-id <ORDER_ID>
```

---

## ### **3. Cancel an Order**

```bash
python cli.py cancel --symbol BTCUSDT --order-id <ORDER_ID>
```

---

## **Logging**

- Console logs (INFO level)
- File logs: `bot.log` (DEBUG level, rotating)

You will find full request/response traces in the log file, with signatures masked for safety.

---

## **How Signing Works**

All signed requests include:

- `timestamp` (in milliseconds)
- `recvWindow` (default: 5000)
- HMAC-SHA256 signature computed from URL-encoded, sorted parameters.

The bot automatically attaches all required fields and signs them before sending.

---

## **Supported Endpoints**

- **POST** `/fapi/v1/order` — Place MARKET or LIMIT order
- **GET** `/fapi/v1/order` — Query order status
- **DELETE** `/fapi/v1/order` — Cancel an active order

---

## **Disclaimer**

This bot interacts **only with the Binance Futures Testnet**, which uses fake funds.

This is **NOT** intended for live trading.
Do not attempt to use this code directly with mainnet keys unless you understand the risks and modify the code accordingly.

---

## **Future Enhancements (optional)**

- TWAP execution strategy
- GRID bot
- OCO / Stop-Limit orders
- Leverage adjustment & margin checks
- Web dashboard (FastAPI)
- Backtesting engine

---
