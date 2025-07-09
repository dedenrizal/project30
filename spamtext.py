import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QPoint, QThread, QObject, pyqtSignal
from PyQt6.QtGui import QDoubleValidator, QIntValidator

import pyautogui

class SpamWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, text, count, interval):
        super().__init__()
        self.text = text
        self.count = count
        self.interval = interval
        self.is_running = True

    def run(self):
        """Main worker logic"""
        for i in range(self.count):
            if not self.is_running:
                break
            pyautogui.write(self.text)
            pyautogui.press("enter")
            self.progress.emit(i + 1)
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self.is_running = False

class FloatingSpamUI(QWidget):
    COUNTDOWN_SECONDS = 5

    def __init__(self):
        super().__init__()
        
        self.is_spamming = False
        self.countdown_timer = None
        self.worker_thread = None
        self.worker = None
        
        self.setup_ui()
        self.setup_layouts()
        self.connect_signals()
        
        self.old_pos = QPoint()

    def setup_ui(self):
        """Initialize UI elements and window properties."""
        self.setWindowTitle("Spam Sender")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setFixedSize(320, 280)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                padding-bottom: 5px;
            }
            QLineEdit {
                background-color: #34495e;
                padding: 8px;
                border: 1px solid #34495e;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 4px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton#btn_start {
                background-color: #2ecc71;
            }
            QPushButton#btn_start:hover {
                background-color: #58d68d;
            }
            QPushButton#btn_stop {
                background-color: #e74c3c;
            }
            QPushButton#btn_stop:hover {
                background-color: #ec7063;
            }
            QLabel#status_label {
                color: #f1c40f;
                font-style: italic;
            }
        """)

        self.title_label = QLabel("Spam Sender")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_input = QLineEdit(placeholderText="Text to send")
        self.loop_input = QLineEdit(placeholderText="Number of repetitions (e.g., 10)")
        self.loop_input.setValidator(QIntValidator(1, 9999))
        
        self.delay_input = QLineEdit(placeholderText="Delay between messages (sec)")
        self.delay_input.setValidator(QDoubleValidator(0.0, 60.0, 2))
        self.delay_input.setText("0.1")

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setObjectName("btn_start")
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet("background-color: #95a5a6;")

        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setup_layouts(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        main_layout.addWidget(self.title_label)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        main_layout.addWidget(self.text_input)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.loop_input)
        hbox.addWidget(self.delay_input)
        main_layout.addLayout(hbox)
        
        main_layout.addStretch() 
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.start_stop_button)
        main_layout.addWidget(self.exit_button)

    def connect_signals(self):
        self.start_stop_button.clicked.connect(self.toggle_spam_process)
        self.exit_button.clicked.connect(self.close)

    def toggle_spam_process(self):
        if not self.is_spamming:
            self.start_spam()
        else:
            self.stop_spam()
            
    def start_spam(self):
        self.text_to_send = self.text_input.text().strip()
        try:
            self.repeat_count = int(self.loop_input.text())
            self.delay_seconds = float(self.delay_input.text())
        except ValueError:
            self.status_label.setText("Status: Invalid number!")
            return

        if not self.text_to_send or self.repeat_count <= 0:
            self.status_label.setText("Status: Fill all fields!")
            return
            
        self.is_spamming = True
        self.set_ui_state(enabled=False)
        self.countdown = self.COUNTDOWN_SECONDS
        self.status_label.setText(f"Status: Starting in {self.countdown}s...")
        

        self.countdown_timer = self.startTimer(1000)

    def stop_spam(self):
        if self.countdown_timer:
            self.killTimer(self.countdown_timer)
            self.countdown_timer = None

        if self.worker:
            self.worker.stop()
        
        self.status_label.setText("Status: Aborted by user.")
        self.reset_ui() 

    def timerEvent(self, event):
        self.countdown -= 1
        if self.countdown > 0:
            self.status_label.setText(f"Status: Starting in {self.countdown}s...")
        else:
            self.killTimer(self.countdown_timer)
            self.countdown_timer = None
            self.execute_spam()
            
    def execute_spam(self):
        self.status_label.setText("Status: Spamming...")
        self.hide()
        

        self.worker_thread = QThread()
        self.worker = SpamWorker(self.text_to_send, self.repeat_count, self.delay_seconds)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.on_spam_finished)
        
        self.worker.progress.connect(
            lambda i: self.status_label.setText(f"Status: Sent {i}/{self.repeat_count}")
        )
        
        self.worker_thread.start()

    def on_spam_finished(self):
        if self.is_spamming: 
             self.status_label.setText("Status: Finished!")
        self.show()
        self.reset_ui()

    def set_ui_state(self, enabled: bool):
        """Enable or disable input fields and buttons."""
        self.text_input.setEnabled(enabled)
        self.loop_input.setEnabled(enabled)
        self.delay_input.setEnabled(enabled)
        
        if not enabled:
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setObjectName("btn_stop")
        else:
            self.start_stop_button.setText("Start")
            self.start_stop_button.setObjectName("btn_start")
        
        self.start_stop_button.style().unpolish(self.start_stop_button)
        self.start_stop_button.style().polish(self.start_stop_button)
        
    def reset_ui(self):
        self.is_spamming = False
        self.set_ui_state(enabled=True)
        if self.status_label.text() not in ["Status: Finished!", "Status: Aborted by user."]:
            self.status_label.setText("Status: Ready")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloatingSpamUI()
    window.show()
    sys.exit(app.exec())