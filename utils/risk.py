"""Risk management primitives for live and paper trading."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    stop_loss_pct: float = 1.0
    target_pct: float = 2.0
    trailing_stop_pct: float = 0.8
    max_daily_loss: float = 2000.0


class RiskManager:
    def __init__(self, config: RiskConfig) -> None:
        self.config = config
        self.daily_realized_pnl: float = 0.0
        self.trailing_price: dict[str, float] = {}

    def can_trade(self) -> bool:
        return self.daily_realized_pnl > -abs(self.config.max_daily_loss)

    def compute_levels(self, entry_price: float, side: str) -> tuple[float, float]:
        if side == "BUY":
            stop = entry_price * (1 - self.config.stop_loss_pct / 100)
            target = entry_price * (1 + self.config.target_pct / 100)
        else:
            stop = entry_price * (1 + self.config.stop_loss_pct / 100)
            target = entry_price * (1 - self.config.target_pct / 100)
        return stop, target

    def update_trailing_stop(self, symbol: str, current_price: float, side: str, base_stop: float) -> float:
        prev = self.trailing_price.get(symbol, current_price)
        if side == "BUY":
            self.trailing_price[symbol] = max(prev, current_price)
            return max(base_stop, self.trailing_price[symbol] * (1 - self.config.trailing_stop_pct / 100))
        self.trailing_price[symbol] = min(prev, current_price)
        return min(base_stop, self.trailing_price[symbol] * (1 + self.config.trailing_stop_pct / 100))

    def add_realized_pnl(self, pnl: float) -> None:
        self.daily_realized_pnl += pnl
