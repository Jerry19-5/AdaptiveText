import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from video_capture import VideoThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Adaptive Text")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Video display
        self.video_label = QLabel()
        self.video_label.setFixedSize(800, 500)
        layout.addWidget(self.video_label)

        # Distance display
        self.distance_label = QLabel("Distance: No face detected")
        self.distance_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.distance_label)

        # Buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_camera)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_camera)
        layout.addWidget(self.stop_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_application)
        layout.addWidget(self.exit_button)

        # Set layout
        self.setLayout(layout)

        # Video thread
        self.thread = VideoThread()
        self.thread.update_image.connect(self.display_frame)
        self.thread.update_distance.connect(self.update_distance)

    def start_camera(self):
        if not self.thread.isRunning():
            self.thread.start()

    def stop_camera(self):
        if self.thread.isRunning():
            self.thread.stop()

    def exit_application(self):
        self.stop_camera()
        self.close()

    def display_frame(self, qt_image):
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_distance(self, distance_text):
        self.distance_label.setText(distance_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
