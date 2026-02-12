# Configuration file for hand gesture recognition

# Camera settings
CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Hand detection settings
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5
STATIC_IMAGE_MODE = False
MAX_HANDS = 2

# Gesture recognition settings
GESTURE_HISTORY_LENGTH = 5
GESTURE_STABLE_FRAMES = 10

# UI settings
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2
TEXT_COLOR = (0, 255, 0)  # Green
BG_COLOR = (0, 0, 0)  # Black

# Colors for landmarks and connections
LANDMARK_COLOR = (0, 255, 0)  # Green
CONNECTION_COLOR = (255, 255, 255)  # White
FINGER_TIP_COLOR = (255, 0, 0)  # Red
FINGER_PIP_COLOR = (0, 0, 255)  # Blue

# Finger indices
THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2
INDEX_TIP = 8
INDEX_PIP = 6
INDEX_MCP = 5
MIDDLE_TIP = 12
MIDDLE_PIP = 10
MIDDLE_MCP = 9
RING_TIP = 16
RING_PIP = 14
RING_MCP = 13
PINKY_TIP = 20
PINKY_PIP = 18
PINKY_MCP = 17

# Landmark indices for hand connections
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),  # Index
    (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
    (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
    (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
    (5, 9), (9, 13), (13, 17)  # Palm
]