from config import *
from utils import calculate_distance, is_point_above, is_point_right

class FingerCounter:
    def __init__(self):
        self.finger_count = 0
        self.fingers_status = [False, False, False, False, False]  # Thumb, Index, Middle, Ring, Pinky
        
    def count_fingers(self, landmarks):
        """Count fingers based on landmarks"""
        if not landmarks or len(landmarks) < 21:
            return 0, [False] * 5
        
        fingers = []
        
        # Thumb
        if is_point_right(landmarks[THUMB_TIP], landmarks[THUMB_IP]):
            fingers.append(True)
        else:
            fingers.append(False)
        
        # Index finger
        if is_point_above(landmarks[INDEX_TIP], landmarks[INDEX_PIP]):
            fingers.append(True)
        else:
            fingers.append(False)
        
        # Middle finger
        if is_point_above(landmarks[MIDDLE_TIP], landmarks[MIDDLE_PIP]):
            fingers.append(True)
        else:
            fingers.append(False)
        
        # Ring finger
        if is_point_above(landmarks[RING_TIP], landmarks[RING_PIP]):
            fingers.append(True)
        else:
            fingers.append(False)
        
        # Pinky finger
        if is_point_above(landmarks[PINKY_TIP], landmarks[PINKY_PIP]):
            fingers.append(True)
        else:
            fingers.append(False)
        
        self.fingers_status = fingers
        self.finger_count = sum(fingers)
        
        return self.finger_count, fingers
    
    def get_finger_count(self):
        """Get current finger count"""
        return self.finger_count
    
    def get_fingers_status(self):
        """Get status of each finger"""
        return self.fingers_status
    
    def draw_finger_count(self, frame, count, position=(50, 100)):
        """Draw finger count on frame"""
        from utils import draw_text_with_background
        
        # Draw finger count
        draw_text_with_background(
            frame, 
            f"Fingers: {count}", 
            position,
            text_color=(0, 255, 0),
            bg_color=(0, 0, 0)
        )
        
        # Draw individual finger status
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        y_offset = 150
        
        for i, (name, status) in enumerate(zip(finger_names, self.fingers_status)):
            color = (0, 255, 0) if status else (0, 0, 255)
            status_text = "✓" if status else "✗"
            draw_text_with_background(
                frame,
                f"{name}: {status_text}",
                (50, y_offset + i * 40),
                text_color=color,
                bg_color=(0, 0, 0)
            )
        
        return frame