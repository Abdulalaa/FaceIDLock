'''
# FaceID.py

# This script is used to detect faces in a video stream and compare them to a 
# list of authorized faces.
'''

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import logging
import json
import numpy as np
import face_recognition
import cv2
from config import *

#------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
# Verify Face
#------------------------------------------------------------------------------
def verify_face(frame, face_location, encodings_dict):
    
    # Convert loaded encodings back to NumPy arrays
    face_encodings = [np.array(enc) for enc in encodings_dict.values()]

    # get the location of face in the frame
    # Extract face from frame using coordinates (y1:y2, x1:x2)
    x, y, w, h = face_location
    face_frame = frame[y:y+h, x:x+w]

    # Convert face_frame to RGB
    face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)

    # Get face encoding for the extracted face
    current_face_encoding = face_recognition.face_encodings(face_frame)

    # Check if face encoding was found
    if not current_face_encoding:
        logger.warning("No face encoding could be generated from the detected face")
        return False

    # Compare face encoding to authorized face encodings
    matches = face_recognition.compare_faces(face_encodings, current_face_encoding[0], TOLERANCE)

    if True in matches:
        name = list(encodings_dict.keys())[matches.index(True)]
        logger.info(f"Authorized user '{name}' verified")
        return True
    else:
        logger.warning("Unauthorized face detected")
        return False
