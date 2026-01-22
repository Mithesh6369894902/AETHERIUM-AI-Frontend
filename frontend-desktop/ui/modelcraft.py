from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog
)
import pandas as pd
from api.client import post

class ModelCraftWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("ModelCraft-X – AutoML Benchmarking")
        self.btn_upload = QPushButton("Upload Dataset")
        self.btn_run = QPushButton("Run Benchmark")
        self.output = QLabel("No results yet")

        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_run.clicked.connect(self.run_benchmark)

        layout.addWidget(self.label)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.output)

        self.setLayout(layout)

        self.data = None

    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if path:
            self.data = pd.read_csv(path)
            self.output.setText(f"Loaded dataset with shape {self.data.shape}")

    def run_benchmark(self):
        if self.data is None:
            self.output.setText("Upload dataset first")
            return

        target = self.data.columns[-1]

        result = post(
            "/modelcraft/benchmark",
            payload={
                "data": self.data.to_dict(orient="records"),
                "target": target
            }
        )

        self.output.setText(
            f"Best Model: {result['best_model']}\n"
            f"Score: {round(result['final_score'], 4)}"
        )
