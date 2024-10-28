from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QSlider, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from core import correct_distortion  # Ensure this function is correctly implemented in core/correct.py

class DistortionCorrector(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None  # Original image
        self.corrected_image = None  # Corrected image
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Distortion Corrector")
        self.image_label = QLabel("Select an image to correct distortion")
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)

        self.save_button = QPushButton("Save Corrected Image")
        self.save_button.clicked.connect(self.save_image)

        # Sliders for distortion correction parameters
        self.k1_slider = self.create_slider(-100, 100, 0)
        self.k2_slider = self.create_slider(-100, 100, 0)
        self.p1_slider = self.create_slider(-100, 100, 0)
        self.p2_slider = self.create_slider(-100, 100, 0)

        # Labels for sliders
        self.k1_label = QLabel("K1: 0.00")
        self.k2_label = QLabel("K2: 0.00")
        self.p1_label = QLabel("P1: 0.00")
        self.p2_label = QLabel("P2: 0.00")

        # Connect sliders to update labels and apply correction live
        self.k1_slider.valueChanged.connect(self.update_image)
        self.k2_slider.valueChanged.connect(self.update_image)
        self.p1_slider.valueChanged.connect(self.update_image)
        self.p2_slider.valueChanged.connect(self.update_image)

        # Layouts
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.k1_label)
        slider_layout.addWidget(self.k1_slider)
        slider_layout.addWidget(self.k2_label)
        slider_layout.addWidget(self.k2_slider)
        slider_layout.addWidget(self.p1_label)
        slider_layout.addWidget(self.p1_slider)
        slider_layout.addWidget(self.p2_label)
        slider_layout.addWidget(self.p2_slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        layout.addLayout(slider_layout)
        self.setLayout(layout)

    def create_slider(self, min_val, max_val, default):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)
        return slider

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.update_image()  # Update the image display with default slider values

    def update_image(self):
        if self.image is not None:
            # Use the slider values as distortion parameters
            k1 = self.k1_slider.value() / 100.0
            k2 = self.k2_slider.value() / 100.0
            p1 = self.p1_slider.value() / 100.0
            p2 = self.p2_slider.value() / 100.0
            
            self.corrected_image = correct_distortion(self.image, k1, k2, p1, p2)  # Apply distortion correction
            self.show_image(self.corrected_image)

            # Update labels
            self.k1_label.setText(f"K1: {k1:.2f}")
            self.k2_label.setText(f"K2: {k2:.2f}")
            self.p1_label.setText(f"P1: {p1:.2f}")
            self.p2_label.setText(f"P2: {p2:.2f}")

    def show_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
        q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def save_image(self):
        if self.corrected_image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
            if file_name:
                cv2.imwrite(file_name, self.corrected_image)
