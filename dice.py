import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QSpinBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

dice_art = {
    1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
    2: ["┌─────────┐", "│ ●       │", "│         │", "│       ● │", "└─────────┘"],
    3: ["┌─────────┐", "│ ●       │", "│    ●    │", "│       ● │", "└─────────┘"],
    4: ["┌─────────┐", "│ ●     ● │", "│         │", "│ ●     ● │", "└─────────┘"],
    5: ["┌─────────┐", "│ ●     ● │", "│    ●    │", "│ ●     ● │", "└─────────┘"],
    6: ["┌─────────┐", "│ ●     ● │", "│ ●     ● │", "│ ●     ● │", "└─────────┘"],
}

class DiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎲 Dice Roller PyQt6")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.dice_selector = QSpinBox()
        self.dice_selector.setRange(1, 10)
        self.dice_selector.setPrefix("Dice: ")
        layout.addWidget(self.dice_selector)

        self.roll_button = QPushButton("🎲 Roll Dice")
        self.roll_button.clicked.connect(self.roll_dice)
        layout.addWidget(self.roll_button)

        self.dice_display = QLabel("")
        self.dice_display.setFont(QFont("Courier", 12))
        self.dice_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.dice_display)

        self.total_label = QLabel("")
        self.total_label.setFont(QFont("Arial", 16))
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_label)

    def roll_dice(self):
        num_dice = self.dice_selector.value()
        dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        self.show_dice(dice_values)

    def show_dice(self, dice_values):
        lines = [""] * 5
        for die in dice_values:
            art = dice_art[die]
            for i in range(5):
                lines[i] += art[i] + "  "

        self.dice_display.setText("\n".join(lines))
        self.total_label.setText(f"🎯 Total: {sum(dice_values)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiceApp()
    window.show()
    sys.exit(app.exec())
