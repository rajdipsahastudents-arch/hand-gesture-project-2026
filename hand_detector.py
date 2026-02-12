import cv2
import mediapipe as mp
from config import *

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=STATIC_IMAGE_MODE,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None
        
    def detect_hands(self, frame):
        """Detect hands in frame"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Process frame
        self.results = self.hands.process(rgb_frame)
        
        # Convert back to BGR
        rgb_frame.flags.writeable = True
        
        return self.results
    
    def get_landmarks(self, frame, hand_index=0):
        """Get landmarks for specific hand"""
        landmarks_list = []
        
        if self.results and self.results.multi_hand_landmarks:
            if hand_index < len(self.results.multi_hand_landmarks):
                hand_landmarks = self.results.multi_hand_landmarks[hand_index]
                h, w, _ = frame.shape
                
                for landmark in hand_landmarks.landmark:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    landmarks_list.append((x, y))
                    
        return landmarks_list
    
    def draw_landmarks(self, frame):
        """Draw hand landmarks on frame"""
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Draw landmarks and connections
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=LANDMARK_COLOR, thickness=2),
                    self.mp_draw.DrawingSpec(color=CONNECTION_COLOR, thickness=2)
                )
        return frame
    
    def get_hand_count(self):
        """Get number of hands detected"""
        if self.results and self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0
    
    def get_hand_type(self, hand_index=0):
        """Get hand type (Left/Right)"""
        if self.results and self.results.multi_handedness:
            if hand_index < len(self.results.multi_handedness):
                return self.results.multi_handedness[hand_index].classification[0].label
        return "Unknown"