import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox
)

class QuizWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Pilihan Ganda")
        self.setGeometry(100, 100, 400, 250)

        self.questions = [
            "Apa ibu kota Indonesia?",
            "Berapa hasil dari 5 + 3?",
            "Siapa penemu lampu pijar?",
            "Apa planet terbesar di tata surya?",
            "Hewan apa yang dikenal sebagai raja hutan?"
        ]
        self.options = [
            ["A Jakarta", "B Bandung", "C Surabaya", "D Medan"],
            ["A 6", "B 7", "C 8", "D 9"],
            ["A Albert Einstein", "B Thomas Edison", "C Nikola Tesla", "D Alexander Graham Bell"],
            ["A Mars", "B Bumi", "C Jupiter", "D Saturnus"],
            ["A Harimau", "B Singa", "C Serigala", "D Gajah"]
        ]
        self.answers = ["A", "C", "C", "C", "B"]
        self.score = 0
        self.current_question = 0

        self.layout = QVBoxLayout()
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.option_buttons = []
        for i in range(4):
            button = QPushButton()
            button.clicked.connect(self.check_answer)
            self.layout.addWidget(button)
            self.option_buttons.append(button)

        self.setLayout(self.layout)
        self.load_question()

    def load_question(self):
        if self.current_question < len(self.questions):
            self.question_label.setText(self.questions[self.current_question])
            options = self.options[self.current_question]
            for i in range(4):
                self.option_buttons[i].setText(options[i])
        else:
            self.finish_quiz()

    def check_answer(self):
        sender = self.sender()
        selected_option = sender.text()[0]  # Ambil huruf pertama dari teks tombol
        correct = self.answers[self.current_question]
        if selected_option == correct:
            self.score += 1
        self.current_question += 1
        self.load_question()

    def finish_quiz(self):
        percentage = int((self.score / len(self.questions)) * 100)
        QMessageBox.information(self, "Hasil Quiz", f"Skor kamu: {percentage}%")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizWindow()
    window.show()
    sys.exit(app.exec())
