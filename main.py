"""Desktop Algorithmic Trading App entry-point."""
from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from config.settings import CONFIG
from data.database import Database
from services.trading_service import TradingService
from strategy.engine import StrategyEngine
from ui.dashboard import DashboardWindow
from ui.login_window import LoginWindow
from utils.alerts import TelegramAlerter
from utils.logger import setup_logger
from utils.risk import RiskConfig, RiskManager


def build_app() -> tuple[QApplication, DashboardWindow]:
    app = QApplication(sys.argv)
    logger = setup_logger(CONFIG.log_file)

    db = Database(CONFIG.db_path)
    strategy_engine = StrategyEngine()
    risk_manager = RiskManager(RiskConfig())
    alerter = TelegramAlerter(CONFIG.telegram_bot_token, CONFIG.telegram_chat_id)
    service = TradingService(db, strategy_engine, risk_manager, logger, alerter)

    login = LoginWindow(db)
    if login.exec_() != login.Accepted:
        raise SystemExit(0)

    window = DashboardWindow(service, logger)
    return app, window


if __name__ == "__main__":
    qt_app, dashboard = build_app()
    dashboard.show()
    sys.exit(qt_app.exec_())
