from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from api.client import post

class InfernoWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("InfernoData Desktop Module")
        btn = QPushButton("Run Preprocess")

        btn.clicked.connect(self.run)

        layout.addWidget(label)
        layout.addWidget(btn)
        self.setLayout(layout)

    def run(self):
        result = post("/inferno/preprocess", payload=[
            {"a": 1, "b": 2},
            {"a": 3, "b": 4}
        ])
        print(result)
