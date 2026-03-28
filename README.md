# Desktop Algorithmic Trading App (PyQt5 + Zerodha Kite Connect)

Production-oriented desktop application for **paper + live trading** with Zerodha Kite Connect API integration.

## Features
- Local user authentication (SQLite)
- Zerodha Kite login URL + request token session generation
- Live LTP, historical OHLC pull
- Strategy engine:
  - EMA crossover (9/21)
  - RSI
  - MACD
- Auto trading toggle (paper/live)
- Real order APIs (market/limit supported in broker wrapper)
- Orders/trades/positions fetch
- Risk controls:
  - Stop loss
  - Target
  - Trailing stop logic
  - Max daily loss guard
- Trade + strategy logs in SQLite
- File logging for requests/errors/events
- Plotly candlestick chart
- Telegram alerts (optional)
- CSV export of trades
- Dark mode toggle

## Project Structure

```text
main.py
ui/
broker/
  zerodha_api.py
strategy/
data/
utils/
config/
services/
```

## Setup (Step-by-step)

## 1) Prerequisites
- Python 3.10+
- Zerodha account
- Kite Connect subscription enabled on your Zerodha account

## 2) Get Zerodha API Key and Secret
1. Login to Kite Connect developer console.
2. Create a new app.
3. Add your redirect URL (example: `http://127.0.0.1`).
4. Copy **API Key** and **API Secret**.

## 3) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4) Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and set:
- `KITE_API_KEY`
- `KITE_API_SECRET`
- Optional: Telegram keys and polling interval

> Never hardcode credentials in source files.

## 5) Generate Zerodha access token (daily flow)
Because Zerodha enforces daily login policies, follow this:
1. Launch app: `python main.py`
2. In **Broker Login** panel click **Generate Login URL**.
3. Open URL in browser and complete Zerodha login.
4. You will be redirected with `request_token` in URL.
5. Paste request token in app and click **Generate Access Token**.
6. Paste/store the access token in `.env` as `KITE_ACCESS_TOKEN`.
7. Click **Connect Broker**.

## 6) Run application
```bash
python main.py
```

## 7) Package into Windows `.exe` (PyInstaller)
```bash
pyinstaller --noconfirm --onefile --windowed main.py --name DesktopAlgoTrader
```
Generated executable will be in `dist/DesktopAlgoTrader.exe`.

## Usage Notes
- Keep **Live Trading Mode** disabled to run paper trading.
- Turn on **Enable Auto Trading** only after testing strategy behavior.
- Ensure risk thresholds are set conservatively before live mode.
- Use logs in `logs/app.log` for diagnostics.

## Database Schema
- `users`: local app authentication
- `trades`: live/paper trade records
- `strategy_logs`: per-symbol strategy decisions

## Error Handling
- API errors and exceptions are caught and logged.
- Invalid token/session issues surface in UI dialogs.
- Max daily loss risk guard blocks further trading.

## Compliance Reminder
- Fully unattended login automation is restricted by Zerodha policy.
- User interaction for daily token generation is expected.
