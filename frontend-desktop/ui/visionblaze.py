from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog
)
from PySide6.QtGui import QPixmap
from api.client import post
import requests
import tempfile

class VisionBlazeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VisionBlaze")

        layout = QVBoxLayout()

        self.label = QLabel("VisionBlaze – Computer Vision Module")
        self.image_label = QLabel("No image loaded")

        self.btn_upload = QPushButton("Upload Image")
        self.btn_edge = QPushButton("Run Edge Detection")

        self.btn_upload.clicked.connect(self.upload_image)
        self.btn_edge.clicked.connect(self.run_edge)

        layout.addWidget(self.label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_edge)

        self.setLayout(layout)

        self.image_path = None

    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.image_path = path
            self.image_label.setPixmap(QPixmap(path).scaledToWidth(400))

    def run_edge(self):
        if not self.image_path:
            self.label.setText("Please upload an image first")
            return

        files = {"file": open(self.image_path, "rb")}
        res = requests.post(
            "http://localhost:8000/vision/edges",
            files=files,
            data={"t1": 80, "t2": 180}
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(res.content)
            self.image_label.setPixmap(QPixmap(f.name).scaledToWidth(400))
