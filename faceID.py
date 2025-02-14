import logging
import face_recognition
import random
import json
import numpy as np

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
