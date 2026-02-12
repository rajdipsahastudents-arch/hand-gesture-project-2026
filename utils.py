import cv2
import numpy as np
from config import *

def draw_text_with_background(img, text, position, font=FONT, 
                            font_scale=FONT_SCALE, 
                            text_color=TEXT_COLOR,
                            bg_color=BG_COLOR,
                            thickness=FONT_THICKNESS,
                            padding=5):
    """Draw text with background"""
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position
    
    # Draw background rectangle
    cv2.rectangle(img, 
                 (x - padding, y - text_height - padding),
                 (x + text_width + padding, y + baseline + padding),
                 bg_color, 
                 -1)
    
    # Draw text
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness)
    
    return img

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def is_point_above(point1, point2):
    """Check if point1 is above point2"""
    return point1[1] < point2[1]

def is_point_right(point1, point2):
    """Check if point1 is to the right of point2"""
    return point1[0] > point2[0]

def create_finger_count_display(count, position, size=50):
    """Create a visual display for finger count"""
    display = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Draw circle background
    cv2.circle(display, (size//2, size//2), size//3, (0, 255, 0), -1)
    
    # Draw count number
    cv2.putText(display, str(count), 
               (size//2 - 10, size//2 + 10), 
               FONT, 1, (0, 0, 0), 2)
    
    return display

def get_fps_color(fps):
    """Get color based on FPS"""
    if fps >= 30:
        return (0, 255, 0)  # Green
    elif fps >= 20:
        return (0, 255, 255)  # Yellow
    else:
        return (0, 0, 255)  # Red