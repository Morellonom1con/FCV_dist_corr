from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QSlider, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from core import apply_distortion

class DistortionApplier(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None  # To store the loaded image
        self.distorted_image = None  # To store the currently displayed distorted image
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Distortion Applier")
        self.image_label = QLabel("Select an image to apply distortion")
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)

        # Button to save the distorted image
        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)

        # Sliders for distortion parameters
        self.k1_slider = self.create_slider(-100, 100, 0)
        self.k2_slider = self.create_slider(-100, 100, 0)
        self.p1_slider = self.create_slider(-100, 100, 0)
        self.p2_slider = self.create_slider(-100, 100, 0)

        # Labels for sliders
        self.k1_label = QLabel("K1: 0.00")
        self.k2_label = QLabel("K2: 0.00")
        self.p1_label = QLabel("P1: 0.00")
        self.p2_label = QLabel("P2: 0.00")

        # Connect sliders to update labels and apply distortion live
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

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)  # Add the save button
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

    def update_label(self, label, param, value):
        label.setText(f"{param}: {value / 100:.2f}")

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.update_image()  # Update image with default slider values

    def update_image(self):
        if self.image is not None:
            # Use the slider values as distortion parameters
            k1 = self.k1_slider.value() / 100.0
            k2 = self.k2_slider.value() / 100.0
            p1 = self.p1_slider.value() / 100.0
            p2 = self.p2_slider.value() / 100.0
            self.distorted_image = apply_distortion(self.image, k1, k2, p1, p2)
            self.show_image(self.distorted_image)

            # Update labels
            self.k1_label.setText(f"K1: {k1:.2f}")
            self.k2_label.setText(f"K2: {k2:.2f}")
            self.p1_label.setText(f"P1: {p1:.2f}")
            self.p2_label.setText(f"P2: {p2:.2f}")

    def show_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qimg = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg)
        self.image_label.setPixmap(pixmap)

    def save_image(self):
        if self.distorted_image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
            if file_name:
                cv2.imwrite(file_name, self.distorted_image)  # Save the distorted image
