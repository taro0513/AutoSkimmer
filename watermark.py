import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont
import threading
import time


class WatermarkApp:
    def __init__(self, text="电缆自动控制中"):
        self.text = text
        self.app = None
        self.label = None
        self.thread = None

    def start(self):
        """Start the watermark application in a separate thread."""

        def run():
            self.app = QApplication(sys.argv)
            self.label = QLabel(self.text)
            self.label.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
            self.label.setAttribute(Qt.WA_TranslucentBackground)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont("Arial", 20))
            self.label.setStyleSheet("color: red;")
            self.label.resize(400, 50)
            screen_width = self.app.primaryScreen().size().width()
            self.label.move((screen_width - self.label.width()) // 2, 0)
            self.label.show()
            self.app.exec_()

        self.thread = threading.Thread(target=run)
        self.thread.start()

    def stop(self):
        """Stop the watermark application."""
        if self.app and self.label:
            self.label.close()  # Close the label
            self.app.quit()  # Quit the application
        if self.thread:
            self.thread.join()  # Ensure the thread stops
        print("Watermark application stopped.")


# Example usage
if __name__ == "__main__":
    wm = WatermarkApp("錄影任務即將開始，請勿觸碰電腦")
    wm.start()  # Start the watermark app
    print("Watermark started. It will stop in 10 seconds.")

    # Let the watermark run for 10 seconds
    time.sleep(10)

    wm.stop()  # Stop the watermark app
