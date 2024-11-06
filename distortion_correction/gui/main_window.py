from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from gui.distortion_corrector import DistortionCorrector
from gui.distortion_applier import DistortionApplier
from gui.zhang_calibration import ZhangCalibration  # New import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Distortion Correction & Calibration")
        self.setGeometry(100, 100, 800, 600)

        # Create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add distortion applier, corrector, and calibration as tabs
        self.applier_tab = DistortionApplier()
        self.corrector_tab = DistortionCorrector()
        self.calibration_tab = ZhangCalibration()

        self.tabs.addTab(self.applier_tab, "Distortion Applier")
        self.tabs.addTab(self.corrector_tab, "Distortion Corrector")
        self.tabs.addTab(self.calibration_tab, "Zhang Calibration")

        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
