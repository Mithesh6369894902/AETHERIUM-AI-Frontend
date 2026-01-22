from PySide6.QtWidgets import (
    QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel
)

from ui.inferno import InfernoWidget
from ui.textvortex import TextVortexWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ÆTHERIUM Desktop")

        central = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("ÆTHERIUM Desktop Application"))

        btn_inferno = QPushButton("InfernoData")
        btn_text = QPushButton("TextVortex")

        btn_inferno.clicked.connect(self.open_inferno)
        btn_text.clicked.connect(self.open_text)

        layout.addWidget(btn_inferno)
        layout.addWidget(btn_text)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def open_inferno(self):
        self.setCentralWidget(InfernoWidget())

    def open_text(self):
        self.setCentralWidget(TextVortexWidget())
