import numpy as np

#constants
REAL_EYE_DISTANCE = 8.9  
KNOWN_DISTANCE = 40.0    
KNOWN_PIXEL_DISTANCE = 140  
MIN_TEXT_SIZE = 12
MAX_TEXT_SIZE = 100

# Calculate focal length
FOCAL_LENGTH = (KNOWN_PIXEL_DISTANCE * KNOWN_DISTANCE) / REAL_EYE_DISTANCE

def calculate_eye_distance(landmarks, width, height):
    left_eye = np.array([landmarks[33].x * width, landmarks[33].y * height])
    right_eye = np.array([landmarks[263].x * width, landmarks[263].y * height])
    return np.linalg.norm(left_eye - right_eye)

def calculate_real_distance(pixel_distance):
    if pixel_distance == 0:
        return 0
    return (FOCAL_LENGTH * REAL_EYE_DISTANCE) / pixel_distance
