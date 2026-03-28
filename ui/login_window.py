"""Local user authentication UI."""
from __future__ import annotations

from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from data.database import Database, User


class LoginWindow(QDialog):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.user: User | None = None
        self.setWindowTitle("Local Login")
        self.setMinimumWidth(350)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("Username", self.username)
        form.addRow("Password", self.password)

        login_btn = QPushButton("Login")
        reg_btn = QPushButton("Register")
        login_btn.clicked.connect(self._login)
        reg_btn.clicked.connect(self._register)

        row = QHBoxLayout()
        row.addWidget(login_btn)
        row.addWidget(reg_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Local app authentication (separate from Zerodha login)."))
        layout.addLayout(form)
        layout.addLayout(row)
        self.setLayout(layout)

    def _login(self) -> None:
        user = self.db.authenticate_user(self.username.text().strip(), self.password.text().strip())
        if not user:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
            return
        self.user = user
        self.accept()

    def _register(self) -> None:
        ok = self.db.register_user(self.username.text().strip(), self.password.text().strip())
        if ok:
            QMessageBox.information(self, "Registered", "User registered. You can now login.")
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")
