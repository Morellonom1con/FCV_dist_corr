from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from core.auto_correct import perform_batch_correction  # Adjust this function name based on your implementation
from calibration.zhang_calibration import calibrate_camera  # New function for Zhang's calibration

class ZhangCalibration(QWidget):
    def __init__(self):
        super().__init__()
        self.calibration_data = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Zhang Calibration")
        self.image_list = QListWidget()
        self.load_images_button = QPushButton("Load Images for Calibration")
        self.calibrate_button = QPushButton("Calibrate")
        self.batch_process_button = QPushButton("Batch Process with Calibration")

        self.load_images_button.clicked.connect(self.load_images)
        self.calibrate_button.clicked.connect(self.run_calibration)
        self.batch_process_button.clicked.connect(self.run_batch_process)

        layout = QVBoxLayout()
        layout.addWidget(self.image_list)
        layout.addWidget(self.load_images_button)
        layout.addWidget(self.calibrate_button)
        layout.addWidget(self.batch_process_button)
        self.setLayout(layout)

    def load_images(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images for Calibration", "", "Image Files (*.png *.jpg *.bmp)")
        if file_names:
            self.image_list.addItems(file_names)

    def run_calibration(self):
        images = []
        for index in range(self.image_list.count()):
            image_path = self.image_list.item(index).text()
            img = cv2.imread(image_path)  # Read image file directly
            if img is not None:
                images.append(img)

        if images:
            # Perform calibration and save the parameters
            self.calibration_data = calibrate_camera(images)
            QMessageBox.information(self, "Calibration Complete", "Camera calibration completed successfully!")


    def run_batch_process(self):
        if self.calibration_data is None:
            QMessageBox.warning(self, "Calibration Not Found", "Please calibrate the camera first.")
            return
        
        # Open dialog to select folder with images to process
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder for Batch Processing")
        if folder_path:
            perform_batch_correction(folder_path, self.calibration_data)
            QMessageBox.information(self, "Batch Processing Complete", "Images have been processed successfully!")
