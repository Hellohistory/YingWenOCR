# logs.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class LogBox(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.layout.addWidget(self.log_text_edit)

    def log(self, message):
        self.log_text_edit.append(message)
