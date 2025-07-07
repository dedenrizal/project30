import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtGui import QFont, QFontDatabase

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = "clock"
        self.elapsed_seconds = 0
        self.stopwatch_running = False

        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.stopwatch_timer = QTimer(self)

        self.mode_button = QPushButton("Switch to Stopwatch")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")

        self.InitUi()
    def InitUi(self):
        self.setWindowTitle("Digital Clock & Stopwatch")
        self.setGeometry(700, 300, 400, 200)

        font_id = QFontDatabase.addApplicationFont("DS-DIGIT.TTF")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 60)
        self.time_label.setFont(my_font)
        self.time_label.setStyleSheet("color: green;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background-color: black;")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        control_box = QHBoxLayout()

        hbox.addWidget(self.mode_button)
        control_box.addWidget(self.start_button)
        control_box.addWidget(self.stop_button)
        control_box.addWidget(self.reset_button)

        vbox.addWidget(self.time_label)
        vbox.addLayout(hbox)
        vbox.addLayout(control_box)
        self.setLayout(vbox)

        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)
        self.updateClock()

        self.stopwatch_timer.timeout.connect(self.updateStopwatch)
        self.stopwatch_timer.setInterval(1000)

        self.mode_button.clicked.connect(self.toggleMode)
        self.start_button.clicked.connect(self.startStopwatch)
        self.stop_button.clicked.connect(self.stopStopwatch)
        self.reset_button.clicked.connect(self.resetStopwatch)

        self.updateControlButtons()

    def updateClock(self):
        if self.mode == "clock":
            current_time = QTime.currentTime().toString("hh:mm:ss AP")
            self.time_label.setText(current_time)

    def updateStopwatch(self):
        self.elapsed_seconds += 1
        self.displayStopwatch()

    def displayStopwatch(self):
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def toggleMode(self):
        if self.mode == "clock":
            self.mode = "stopwatch"
            self.mode_button.setText("Switch to Clock")
            self.timer.stop()
            self.elapsed_seconds = 0
            self.displayStopwatch()
        else:
            self.mode = "clock"
            self.mode_button.setText("Switch to Stopwatch")
            self.stopwatch_timer.stop()
            self.stopwatch_running = False
            self.timer.start(1000)
            self.updateClock()
        self.updateControlButtons()

    def startStopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_timer.start()

    def stopStopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.stopwatch_timer.stop()

    def resetStopwatch(self):
        self.elapsed_seconds = 0
        self.displayStopwatch()

    def updateControlButtons(self):
        is_stopwatch = self.mode == "stopwatch"
        self.start_button.setVisible(is_stopwatch)
        self.stop_button.setVisible(is_stopwatch)
        self.reset_button.setVisible(is_stopwatch)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    digitalClock = DigitalClock()
    digitalClock.show()
    sys.exit(app.exec())