import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

words = ("owl", "cat", "bat", "rat")

hangman_art = {
    0: ("   ", "   ", "   ", "   "),
    1: ("😐", "   ", "   ", "   "),
    2: ("😐", " | ", "   ", "   "),
    3: ("😟", "/| ", "   ", "   "),
    4: ("😖", "/|\\", "   ", "   "),
    5: ("😫", "/|\\", "/  ", "   "),
    6: ("💀", "/|\\", "/ \\", "☠ RIP"),
}

class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hangman Game")
        self.setGeometry(100, 100, 400, 500)

        self.answer = random.choice(words)
        self.hint = ["_"] * len(self.answer)
        self.wrong_guesses = 0
        self.guessed_letters = set()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Hangman Display
        self.hangman_label = QLabel("\n".join(hangman_art[0]))
        self.hangman_label.setFont(QFont("Courier", 24))
        self.hangman_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.hangman_label)

        # Hint Display
        self.hint_label = QLabel(" ".join(self.hint))
        self.hint_label.setFont(QFont("Arial", 20))
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.hint_label)

        # Letter Buttons Grid
        self.letters_layout = QGridLayout()
        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = QPushButton(letter)
            btn.setFixedSize(60, 60)
            btn.clicked.connect(self.make_guess)
            self.letters_layout.addWidget(btn, i // 7, i % 7)
            self.letter_buttons[letter] = btn
        self.layout.addLayout(self.letters_layout)

    def make_guess(self):
        button = self.sender()
        letter = button.text().lower()
        button.setEnabled(False)

        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)

        if letter in self.answer:
            for i in range(len(self.answer)):
                if self.answer[i] == letter:
                    self.hint[i] = letter
        else:
            self.wrong_guesses += 1

        self.update_view()

        if "_" not in self.hint:
            self.game_over(win=True)
        elif self.wrong_guesses >= len(hangman_art) - 1:
            self.game_over(win=False)

    def update_view(self):
        self.hangman_label.setText("\n".join(hangman_art[self.wrong_guesses]))
        self.hint_label.setText(" ".join(self.hint))

    def game_over(self, win):
        msg = QMessageBox()
        if win:
            msg.setText("🎉 YOU WIN!")
        else:
            msg.setText(f"💀 YOU LOSE!\nThe word was: {self.answer}")
        msg.setInformativeText("Play again?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.restart_game()
        else:
            self.close()

    def restart_game(self):
        self.answer = random.choice(words)
        self.hint = ["_"] * len(self.answer)
        self.wrong_guesses = 0
        self.guessed_letters.clear()
        for btn in self.letter_buttons.values():
            btn.setEnabled(True)
        self.update_view()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HangmanGame()
    window.show()
    sys.exit(app.exec())
