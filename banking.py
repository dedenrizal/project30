import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class BankApp(QWidget):
    def __init__(self):
        super().__init__()
        self.balance = 0.0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Simple Bank App')

        self.balance_label = QLabel(f'Your balance is $ {self.balance:.2f}')
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deposit_btn = QPushButton('Deposit')
        self.withdraw_btn = QPushButton('Withdraw')
        self.update_btn = QPushButton('Show Balance')
        self.exit_btn = QPushButton('Exit')

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Enter amount...')
        self.amount_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deposit_btn.clicked.connect(self.deposit)
        self.withdraw_btn.clicked.connect(self.withdraw)
        self.update_btn.clicked.connect(self.update_balance)
        self.exit_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.balance_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.deposit_btn)
        layout.addWidget(self.withdraw_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)
        self.resize(300, 250)

    def update_balance(self):
        self.balance_label.setText(f'Your balance is $ {self.balance:.2f}')

    def deposit(self):
        try:
            amount = float(self.amount_input.text())
            if amount < 0:
                QMessageBox.warning(self, 'Invalid', 'Amount must be greater than 0')
                return
            self.balance += amount
            self.update_balance()
            self.amount_input.clear()
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid number')

    def withdraw(self):
        try:
            amount = float(self.amount_input.text())
            if amount < 0:
                QMessageBox.warning(self, 'Invalid', 'Amount must be greater than 0')
            elif amount > self.balance:
                QMessageBox.warning(self, 'Invalid', f'Insufficient funds. Your balance is ${self.balance:.2f}')
            else:
                self.balance -= amount
                self.update_balance()
                self.amount_input.clear()
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid number')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BankApp()
    window.show()
    sys.exit(app.exec())
