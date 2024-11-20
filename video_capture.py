import cv2
import mediapipe as mp
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from distance_calculation import calculate_eye_distance, calculate_real_distance

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Constants
MIN_TEXT_SIZE = 15
MAX_TEXT_SIZE = 70

class VideoThread(QThread):
    update_image = pyqtSignal(QImage)
    update_distance = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for MediaPipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

            # Convert back to BGR for display
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            height, width, _ = image.shape

            distance_text = "Distance: Face not detected"

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Calculate pixel distance and real-world distance
                    pixel_distance = calculate_eye_distance(face_landmarks.landmark, width, height)
                    real_distance = calculate_real_distance(pixel_distance)

                    # Update distance text
                    distance_text = f"Distance: {real_distance:.2f} cm"

                    # Calculate adaptive text size
                    text_size = int(MAX_TEXT_SIZE - (pixel_distance / width * (MAX_TEXT_SIZE - MIN_TEXT_SIZE)))
                    text_size = max(MIN_TEXT_SIZE, min(MAX_TEXT_SIZE, text_size))

                    # Print detected values for debugging
                    print(f"Detected Distance: {real_distance:.2f} cm, Text Size: {text_size}")

                    # Draw adaptive text
                    cv2.putText(image, "Samsun City", (40, 90), cv2.FONT_HERSHEY_TRIPLEX,
                                text_size / 30, (255, 0, 0), 2)

            # Emit the distance text
            self.update_distance.emit(distance_text)

            # Convert frame to QImage for GUI
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qt_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.update_image.emit(qt_image)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()
