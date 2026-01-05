"""
Face Detector Module using MediaPipe Face Mesh
Provides face detection and landmark extraction for downstream analysis.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass


@dataclass
class FaceDetectionResult:
    """Result of face detection containing landmarks and bounding box."""
    landmarks: np.ndarray  # Shape: (468, 3) for Face Mesh
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    confidence: float
    image_shape: Tuple[int, int]  # height, width


class FaceDetector:
    """
    Face detection and landmark extraction using MediaPipe Face Mesh.
    Provides 468 facial landmarks for detailed face analysis.
    """
    
    # Key landmark indices for ROI extraction
    FOREHEAD_LANDMARKS = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
    LEFT_CHEEK_LANDMARKS = [50, 101, 36, 205, 206, 207, 187, 123, 116, 117, 118, 119]
    RIGHT_CHEEK_LANDMARKS = [280, 330, 266, 425, 426, 427, 411, 352, 345, 346, 347, 348]
    
    # Face shape measurement landmarks
    FACE_TOP = 10
    FACE_BOTTOM = 152  # Chin
    FACE_LEFT = 234
    FACE_RIGHT = 454
    FOREHEAD_LEFT = 70
    FOREHEAD_RIGHT = 300
    JAW_LEFT = 172
    JAW_RIGHT = 397
    CHEEKBONE_LEFT = 234
    CHEEKBONE_RIGHT = 454
    
    def __init__(self, min_detection_confidence: float = 0.5, min_tracking_confidence: float = 0.5):
        """
        Initialize the Face Detector.
        
        Args:
            min_detection_confidence: Minimum confidence for face detection
            min_tracking_confidence: Minimum confidence for landmark tracking
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def detect(self, image: np.ndarray) -> Optional[FaceDetectionResult]:
        """
        Detect face and extract landmarks from an image.
        
        Args:
            image: BGR image as numpy array
            
        Returns:
            FaceDetectionResult if face found, None otherwise
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        
        # Process with MediaPipe
        results = self.face_mesh.process(rgb_image)
        
        if not results.multi_face_landmarks:
            return None
            
        face_landmarks = results.multi_face_landmarks[0]
        
        # Extract landmarks as numpy array
        landmarks = np.array([
            [lm.x * width, lm.y * height, lm.z * width]
            for lm in face_landmarks.landmark
        ])
        
        # Calculate bounding box
        x_coords = landmarks[:, 0]
        y_coords = landmarks[:, 1]
        x_min, x_max = int(x_coords.min()), int(x_coords.max())
        y_min, y_max = int(y_coords.min()), int(y_coords.max())
        
        bbox = (x_min, y_min, x_max - x_min, y_max - y_min)
        
        return FaceDetectionResult(
            landmarks=landmarks,
            bbox=bbox,
            confidence=0.95,  # MediaPipe doesn't expose confidence directly
            image_shape=(height, width)
        )
    
    def extract_roi(self, image: np.ndarray, landmarks: np.ndarray, 
                    landmark_indices: List[int]) -> np.ndarray:
        """
        Extract a region of interest based on landmark indices.
        
        Args:
            image: Original BGR image
            landmarks: Face landmarks array
            landmark_indices: List of landmark indices to create ROI mask
            
        Returns:
            Cropped ROI image
        """
        # Get points for the specified landmarks
        points = landmarks[landmark_indices, :2].astype(np.int32)
        
        # Create bounding rect
        x, y, w, h = cv2.boundingRect(points)
        
        # Add padding
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        
        return image[y:y+h, x:x+w]
    
    def get_cheek_regions(self, image: np.ndarray, 
                          landmarks: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract left and right cheek regions for skin tone analysis.
        
        Args:
            image: Original BGR image
            landmarks: Face landmarks array
            
        Returns:
            Tuple of (left_cheek, right_cheek) images
        """
        left_cheek = self.extract_roi(image, landmarks, self.LEFT_CHEEK_LANDMARKS)
        right_cheek = self.extract_roi(image, landmarks, self.RIGHT_CHEEK_LANDMARKS)
        return left_cheek, right_cheek
    
    def get_forehead_region(self, image: np.ndarray, 
                            landmarks: np.ndarray) -> np.ndarray:
        """
        Extract forehead region for skin tone analysis.
        
        Args:
            image: Original BGR image
            landmarks: Face landmarks array
            
        Returns:
            Forehead region image
        """
        return self.extract_roi(image, landmarks, self.FOREHEAD_LANDMARKS)
    
    def get_face_measurements(self, landmarks: np.ndarray) -> Dict[str, float]:
        """
        Calculate key face measurements for face shape classification.
        
        Args:
            landmarks: Face landmarks array
            
        Returns:
            Dictionary of face measurements
        """
        def distance(idx1: int, idx2: int) -> float:
            return np.linalg.norm(landmarks[idx1, :2] - landmarks[idx2, :2])
        
        face_length = distance(self.FACE_TOP, self.FACE_BOTTOM)
        face_width = distance(self.FACE_LEFT, self.FACE_RIGHT)
        forehead_width = distance(self.FOREHEAD_LEFT, self.FOREHEAD_RIGHT)
        jaw_width = distance(self.JAW_LEFT, self.JAW_RIGHT)
        cheekbone_width = distance(self.CHEEKBONE_LEFT, self.CHEEKBONE_RIGHT)
        
        # Calculate jawline angle
        left_jaw = landmarks[self.JAW_LEFT, :2]
        right_jaw = landmarks[self.JAW_RIGHT, :2]
        chin = landmarks[self.FACE_BOTTOM, :2]
        
        vec1 = left_jaw - chin
        vec2 = right_jaw - chin
        cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        jawline_angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
        
        return {
            'face_length': face_length,
            'face_width': face_width,
            'forehead_width': forehead_width,
            'jaw_width': jaw_width,
            'cheekbone_width': cheekbone_width,
            'jawline_angle': jawline_angle,
            'length_width_ratio': face_length / face_width if face_width > 0 else 0,
            'forehead_jaw_ratio': forehead_width / jaw_width if jaw_width > 0 else 0
        }
    
    def __del__(self):
        """Clean up MediaPipe resources."""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
