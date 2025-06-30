import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SlotMachine(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎰 Slot Machine PyQt6")
        self.setGeometry(100, 100, 400, 300)

        self.symbols = ["🍒", "🍉", "🍋", "🔔", "⭐", "🎖️", "💯"]
        self.balance = 100

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Balance label
        self.balance_label = QLabel(f"💰 Balance: ${self.balance:.2f}")
        self.balance_label.setFont(QFont("Arial", 16))
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.balance_label)

        # Slot symbols
        self.slots = [QLabel("❓") for _ in range(3)]
        slots_layout = QHBoxLayout()
        for label in self.slots:
            label.setFont(QFont("Arial", 36))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slots_layout.addWidget(label)
        layout.addLayout(slots_layout)

        # Bet input
        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Enter your bet (e.g., 10)")
        layout.addWidget(self.bet_input)

        # Spin button
        self.spin_button = QPushButton("🎲 Spin")
        self.spin_button.clicked.connect(self.spin)
        layout.addWidget(self.spin_button)

        # Message
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

    def spin(self):
        bet_text = self.bet_input.text()

        if not bet_text.isdigit():
            self.show_message("Please enter a valid number.")
            return

        bet = int(bet_text)

        if bet <= 0:
            self.show_message("Bet must be greater than 0.")
            return

        if bet > self.balance:
            self.show_message("Insufficient funds.")
            return

        # Deduct bet
        self.balance -= bet
        self.update_balance()

        # Spin result
        result = [random.choice(self.symbols) for _ in range(3)]
        for i in range(3):
            self.slots[i].setText(result[i])

        payout = self.get_payout(result, bet)
        self.balance += payout
        self.update_balance()

        if payout > 0:
            self.show_message(f"🎉 You win ${payout:.2f}!")
        else:
            self.show_message("😢 You lose this round.")

        if self.balance <= 0:
            QMessageBox.information(self, "Game Over", "You're out of balance!")
            self.spin_button.setEnabled(False)

    def update_balance(self):
        self.balance_label.setText(f"💰 Balance: ${self.balance:.2f}")

    def show_message(self, message):
        self.message_label.setText(message)

    def get_payout(self, row, bet):
        if row[0] == row[1] == row[2]:
            symbol = row[0]
            multiplier = {
                "🍒": 2,
                "🍉": 2.5,
                "🍋": 3,
                "🔔": 3.5,
                "⭐": 4,
                "🎖️": 4.5,
                "💯": 5,
            }
            return bet * multiplier.get(symbol, 0)
        return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlotMachine()
    window.show()
    sys.exit(app.exec())
