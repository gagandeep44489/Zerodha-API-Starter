"""Technical indicator helpers using pandas-ta."""
from __future__ import annotations

import pandas as pd

try:
    import pandas_ta as ta
except ImportError:
    ta = None


class IndicatorError(Exception):
    pass


def ensure_ta() -> None:
    if ta is None:
        raise IndicatorError("pandas-ta is not installed.")


def ema_signal(df: pd.DataFrame, fast: int = 9, slow: int = 21) -> str:
    ensure_ta()
    data = df.copy()
    data[f"ema_{fast}"] = ta.ema(data["close"], length=fast)
    data[f"ema_{slow}"] = ta.ema(data["close"], length=slow)
    latest = data.iloc[-1]
    prev = data.iloc[-2]

    if prev[f"ema_{fast}"] <= prev[f"ema_{slow}"] and latest[f"ema_{fast}"] > latest[f"ema_{slow}"]:
        return "BUY"
    if prev[f"ema_{fast}"] >= prev[f"ema_{slow}"] and latest[f"ema_{fast}"] < latest[f"ema_{slow}"]:
        return "SELL"
    return "HOLD"


def rsi_signal(df: pd.DataFrame, period: int = 14, oversold: float = 30, overbought: float = 70) -> str:
    ensure_ta()
    data = df.copy()
    data["rsi"] = ta.rsi(data["close"], length=period)
    latest = data.iloc[-1]["rsi"]
    if latest <= oversold:
        return "BUY"
    if latest >= overbought:
        return "SELL"
    return "HOLD"


def macd_signal(df: pd.DataFrame) -> str:
    ensure_ta()
    data = df.copy()
    macd = ta.macd(data["close"])
    data = pd.concat([data, macd], axis=1)
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    macd_col = "MACD_12_26_9"
    sig_col = "MACDs_12_26_9"

    if prev[macd_col] <= prev[sig_col] and latest[macd_col] > latest[sig_col]:
        return "BUY"
    if prev[macd_col] >= prev[sig_col] and latest[macd_col] < latest[sig_col]:
        return "SELL"
    return "HOLD"
