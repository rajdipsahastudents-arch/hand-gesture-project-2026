import numpy as np
from collections import deque
from config import *

class GestureRecognizer:
    def __init__(self):
        self.gesture_history = deque(maxlen=GESTURE_HISTORY_LENGTH)
        self.current_gesture = "None"
        self.stable_gesture = "None"
        self.stable_counter = 0
        
    def recognize_gesture(self, finger_count, hand_landmarks=None):
        """Recognize gesture based on finger count and hand position"""
        
        # Basic gestures based on finger count
        if finger_count == 0:
            gesture = "Fist"
        elif finger_count == 1:
            gesture = "Point"
        elif finger_count == 2:
            gesture = "Peace"
        elif finger_count == 3:
            gesture = "Three"
        elif finger_count == 4:
            gesture = "Four"
        elif finger_count == 5:
            gesture = "Open Hand"
        else:
            gesture = "Unknown"
        
        # Advanced gestures if landmarks are provided
        if hand_landmarks and len(hand_landmarks) >= 21:
            # Check for OK sign
            if self.is_ok_sign(hand_landmarks):
                gesture = "OK"
            # Check for Thumbs Up
            elif self.is_thumbs_up(hand_landmarks):
                gesture = "Thumbs Up"
            # Check for Thumbs Down
            elif self.is_thumbs_down(hand_landmarks):
                gesture = "Thumbs Down"
            # Check for Victory sign with two fingers
            elif finger_count == 2 and self.is_victory_sign(hand_landmarks):
                gesture = "Victory"
        
        self.current_gesture = gesture
        self.gesture_history.append(gesture)
        
        # Check if gesture is stable
        if len(self.gesture_history) == GESTURE_HISTORY_LENGTH:
            if all(g == gesture for g in self.gesture_history):
                self.stable_counter += 1
                if self.stable_counter >= GESTURE_STABLE_FRAMES:
                    self.stable_gesture = gesture
                    self.stable_counter = 0
            else:
                self.stable_counter = max(0, self.stable_counter - 1)
        
        return gesture
    
    def is_ok_sign(self, landmarks):
        """Check if hand shows OK sign"""
        # Thumb tip close to index tip
        thumb_index_distance = np.sqrt(
            (landmarks[THUMB_TIP][0] - landmarks[INDEX_TIP][0])**2 +
            (landmarks[THUMB_TIP][1] - landmarks[INDEX_TIP][1])**2
        )
        
        # Other fingers extended
        middle_finger_extended = landmarks[MIDDLE_TIP][1] < landmarks[MIDDLE_PIP][1]
        ring_finger_extended = landmarks[RING_TIP][1] < landmarks[RING_PIP][1]
        pinky_extended = landmarks[PINKY_TIP][1] < landmarks[PINKY_PIP][1]
        
        return thumb_index_distance < 50 and middle_finger_extended and ring_finger_extended and pinky_extended
    
    def is_thumbs_up(self, landmarks):
        """Check if hand shows thumbs up"""
        # Thumb above other fingers
        thumb_up = landmarks[THUMB_TIP][1] < landmarks[THUMB_MCP][1]
        
        # All other fingers curled
        index_curled = landmarks[INDEX_TIP][1] > landmarks[INDEX_PIP][1]
        middle_curled = landmarks[MIDDLE_TIP][1] > landmarks[MIDDLE_PIP][1]
        ring_curled = landmarks[RING_TIP][1] > landmarks[RING_PIP][1]
        pinky_curled = landmarks[PINKY_TIP][1] > landmarks[PINKY_PIP][1]
        
        return thumb_up and index_curled and middle_curled and ring_curled and pinky_curled
    
    def is_thumbs_down(self, landmarks):
        """Check if hand shows thumbs down"""
        # Thumb below other fingers
        thumb_down = landmarks[THUMB_TIP][1] > landmarks[THUMB_MCP][1]
        
        # All other fingers curled
        index_curled = landmarks[INDEX_TIP][1] > landmarks[INDEX_PIP][1]
        middle_curled = landmarks[MIDDLE_TIP][1] > landmarks[MIDDLE_PIP][1]
        ring_curled = landmarks[RING_TIP][1] > landmarks[RING_PIP][1]
        pinky_curled = landmarks[PINKY_TIP][1] > landmarks[PINKY_PIP][1]
        
        return thumb_down and index_curled and middle_curled and ring_curled and pinky_curled
    
    def is_victory_sign(self, landmarks):
        """Check if hand shows victory/peace sign"""
        # Index and middle extended
        index_extended = landmarks[INDEX_TIP][1] < landmarks[INDEX_PIP][1]
        middle_extended = landmarks[MIDDLE_TIP][1] < landmarks[MIDDLE_PIP][1]
        
        # Ring and pinky curled
        ring_curled = landmarks[RING_TIP][1] > landmarks[RING_PIP][1]
        pinky_curled = landmarks[PINKY_TIP][1] > landmarks[PINKY_PIP][1]
        
        # Index and middle spread apart
        fingers_spread = abs(landmarks[INDEX_TIP][0] - landmarks[MIDDLE_TIP][0]) > 50
        
        return index_extended and middle_extended and ring_curled and pinky_curled and fingers_spread
    
    def get_current_gesture(self):
        """Get current gesture"""
        return self.current_gesture
    
    def get_stable_gesture(self):
        """Get stable gesture"""
        return self.stable_gesture