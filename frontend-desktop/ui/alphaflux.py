from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit
)
from api.client import post

class AlphaFluxWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("AlphaFlux – Decision Intelligence")
        self.symbol_input = QLineEdit("AAPL")
        self.btn_run = QPushButton("Run Forecast")
        self.output = QLabel("Result will appear here")

        self.btn_run.clicked.connect(self.run_forecast)

        layout.addWidget(self.label)
        layout.addWidget(QLabel("Stock Symbol"))
        layout.addWidget(self.symbol_input)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_forecast(self):
        result = post(
            "/workflow/alphaflux/forecast",
            payload={
                "symbol": self.symbol_input.text(),
                "start_date": "2020-01-01",
                "end_date": "2024-01-01",
                "horizon": 10
            }
        )

        self.output.setText(
            f"Signal: {result['signal']}\n"
            f"Confidence: {round(result['confidence'], 2)}"
        )
