from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from api.client import post

class TextVortexWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.text = QTextEdit()
        btn = QPushButton("Analyze Sentiment")

        btn.clicked.connect(self.run)

        layout.addWidget(self.text)
        layout.addWidget(btn)
        self.setLayout(layout)

    def run(self):
        result = post("/text/sentiment", payload={
            "text": self.text.toPlainText()
        })
        print(result)
