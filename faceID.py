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

def verify_face(frame, face_location):
# ------------------------------------------------------------------------------
# Import JSON file - load and convert to numpy array
# ------------------------------------------------------------------------------
    try:
        with open("authorized_faces.json", "r") as json_file:
            encodings_dict = json.load(json_file) #encodings_dict is a dictionary of face encodings and their corresponding names
    except OSError:
        logger.error("Problem loading authorized_faces.json")
        return False
    
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












'''
# Load face encodings from JSON file
with open("authorized_faces.json", "r") as json_file:
    encodings_dict = json.load(json_file)

# Convert loaded encodings back to NumPy arrays
known_face_encodings = [np.array(enc) for enc in encodings_dict.values()]
known_face_names = list(encodings_dict.keys())

print(f"Loaded {len(known_face_encodings)} faces from authorized_faces.json")

# Open webcam (0 = default camera)
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Cannot access webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize frame for faster processing
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

    # Detect faces
    face_locations = face_recognition.face_locations(small_frame, model="hog")

    if not face_locations:
        continue  # Skip frame if no faces detected

    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    if not face_encodings:
        continue  # Skip frame if no encodings are found

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        # Find best match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Scale face locations back to original frame size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show video frame with annotations
    cv2.imshow('Face Recognition', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
'''