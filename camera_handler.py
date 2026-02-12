import cv2
import time
from config import *

class CameraHandler:
    def __init__(self, camera_id=CAMERA_ID):
        self.camera_id = camera_id
        self.cap = None
        self.is_running = False
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
    def initialize(self):
        """Initialize camera"""
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")
            
        self.is_running = True
        print(f"Camera initialized: {self.camera_id}")
        return True
    
    def get_frame(self):
        """Get frame from camera"""
        if self.cap is None or not self.is_running:
            return None
            
        ret, frame = self.cap.read()
        if ret:
            # Update FPS
            self.frame_count += 1
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 1:
                self.fps = self.frame_count / elapsed_time
                self.frame_count = 0
                self.start_time = time.time()
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            return frame
        return None
    
    def release(self):
        """Release camera"""
        if self.cap:
            self.cap.release()
        self.is_running = False
        print("Camera released")
    
    def get_available_cameras(self):
        """Check available cameras"""
        available_cameras = []
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras