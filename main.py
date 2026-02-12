import cv2
import sys
from camera_handler import CameraHandler
from hand_detector import HandDetector
from finger_counter import FingerCounter
from gesture_recognizer import GestureRecognizer
from utils import draw_text_with_background, get_fps_color
from config import *

class HandGestureApp:
    def __init__(self):
        self.camera = CameraHandler()
        self.detector = HandDetector()
        self.finger_counter = FingerCounter()
        self.gesture_recognizer = GestureRecognizer()
        
    def run(self):
        """Main application loop"""
        print("Starting Hand Gesture Recognition App...")
        print("Press 'q' to quit")
        print("Press 's' to save screenshot")
        
        try:
            # Initialize camera
            self.camera.initialize()
            
            while True:
                # Get frame from camera
                frame = self.camera.get_frame()
                if frame is None:
                    print("Failed to get frame")
                    break
                
                # Detect hands
                self.detector.detect_hands(frame)
                
                # Get hand count
                hand_count = self.detector.get_hand_count()
                
                # Process each hand
                for i in range(hand_count):
                    # Get landmarks
                    landmarks = self.detector.get_landmarks(frame, i)
                    
                    if landmarks:
                        # Count fingers
                        finger_count, fingers = self.finger_counter.count_fingers(landmarks)
                        
                        # Recognize gesture
                        gesture = self.gesture_recognizer.recognize_gesture(finger_count, landmarks)
                        
                        # Get hand type
                        hand_type = self.detector.get_hand_type(i)
                        
                        # Draw hand info
                        y_offset = 50 + (i * 200)
                        
                        # Draw hand type
                        draw_text_with_background(
                            frame,
                            f"Hand {i+1}: {hand_type}",
                            (frame.shape[1] - 250, y_offset),
                            text_color=(255, 255, 0),
                            bg_color=(0, 0, 0)
                        )
                        
                        # Draw finger count
                        draw_text_with_background(
                            frame,
                            f"Fingers: {finger_count}",
                            (frame.shape[1] - 250, y_offset + 40),
                            text_color=(0, 255, 0),
                            bg_color=(0, 0, 0)
                        )
                        
                        # Draw gesture
                        draw_text_with_background(
                            frame,
                            f"Gesture: {gesture}",
                            (frame.shape[1] - 250, y_offset + 80),
                            text_color=(0, 255, 255),
                            bg_color=(0, 0, 0)
                        )
                        
                        # Draw stable gesture
                        stable_gesture = self.gesture_recognizer.get_stable_gesture()
                        if stable_gesture != "None":
                            draw_text_with_background(
                                frame,
                                f"Stable: {stable_gesture}",
                                (frame.shape[1] - 250, y_offset + 120),
                                text_color=(255, 255, 255),
                                bg_color=(0, 128, 0)
                            )
                        
                        # Draw finger count at bottom
                        self.draw_bottom_finger_count(frame, finger_count, i)
                
                # Draw landmarks
                frame = self.detector.draw_landmarks(frame)
                
                # Draw FPS
                fps_color = get_fps_color(self.camera.fps)
                draw_text_with_background(
                    frame,
                    f"FPS: {int(self.camera.fps)}",
                    (10, 30),
                    text_color=fps_color,
                    bg_color=(0, 0, 0)
                )
                
                # Draw hand count
                draw_text_with_background(
                    frame,
                    f"Hands: {hand_count}",
                    (10, 70),
                    text_color=(255, 255, 255),
                    bg_color=(0, 0, 0)
                )
                
                # Show frame
                cv2.imshow("Hand Gesture Recognition", frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('s'):
                    self.save_screenshot(frame)
                    
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            # Cleanup
            self.camera.release()
            cv2.destroyAllWindows()
    
    def draw_bottom_finger_count(self, frame, finger_count, hand_index=0):
        """Draw finger count at bottom of frame"""
        h, w, _ = frame.shape
        
        # Position at bottom
        x = 50 + (hand_index * 200)
        y = h - 50
        
        # Draw circle
        cv2.circle(frame, (x, y), 30, (0, 255, 0), -1)
        cv2.circle(frame, (x, y), 32, (255, 255, 255), 2)
        
        # Draw finger count
        cv2.putText(frame, str(finger_count), (x - 10, y + 10), 
                   FONT, 1.2, (0, 0, 0), 3)
        cv2.putText(frame, str(finger_count), (x - 10, y + 10), 
                   FONT, 1.2, (255, 255, 255), 2)
        
        # Draw label
        cv2.putText(frame, f"Hand {hand_index + 1}", (x - 30, y - 40),
                   FONT, 0.5, (255, 255, 255), 1)
    
    def save_screenshot(self, frame):
        """Save screenshot"""
        import datetime
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")

def main():
    app = HandGestureApp()
    app.run()

if __name__ == "__main__":
    main()