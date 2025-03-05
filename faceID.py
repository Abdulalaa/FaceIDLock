"""
faceID.py

This script is used to detect faces in a video stream and compare them to a 
list of authorized faces.
"""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import logging  # For logging events and errors
import json     # For handling JSON data
import numpy as np  # For numerical operations
import face_recognition  # For face detection and recognition
import cv2      # OpenCV for image processing
from config import *  # Import all configuration variables from config.py

#------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------
logger = logging.getLogger(__name__)  # Get a logger instance for this module

#------------------------------------------------------------------------------
# Verify Face
#------------------------------------------------------------------------------
def verify_face(frame, face_location, encodings_dict):
    """
    Compares a detected face against authorized face encodings to verify identity
    
    Args:
        frame: The video frame containing the face
        face_location: Coordinates of the face in the frame (x, y, w, h)
        encodings_dict: Dictionary of authorized face encodings
        
    Returns:
        bool: True if face is authorized, False otherwise
    """
    try:
        # Convert loaded encodings back to NumPy arrays
        face_encodings = [np.array(enc) for enc in encodings_dict.values()]

        # Extract face from frame using coordinates (y1:y2, x1:x2)
        x, y, w, h = face_location
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Ensure coordinates are within frame boundaries
        x = max(0, x)
        y = max(0, y)
        w = min(w, width - x)
        h = min(h, height - y)
        
        # Check if we have a valid face region
        if w <= 0 or h <= 0:
            logger.warning("Face detection coordinates invalid")
            return False
            
        face_frame = frame[y:y+h, x:x+w]

        # Convert face_frame to RGB
        face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)

        # Get face encoding for the extracted face
        current_face_encoding = face_recognition.face_encodings(face_frame)

        # Check if face encoding was found
        if not current_face_encoding:
            logger.warning("No face encoding could be generated from the detected face")
            return False  # Return failure if no encoding could be generated

        # Compare face encoding to authorized face encodings
        matches = face_recognition.compare_faces(face_encodings, current_face_encoding[0], TOLERANCE)

        if True in matches:
            name = list(encodings_dict.keys())[matches.index(True)]
            logger.info(f"Authorized user '{name}' verified")
            return True  # Return success if match found
        else:
            logger.warning("Unauthorized face detected")
            return False  # Return failure if no match found
    except Exception as e:
        logger.error(f"Error during face verification: {e}")
        return False  # Return failure if any exception occurs
