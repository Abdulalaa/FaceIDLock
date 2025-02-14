import face_recognition
import os
import json
import numpy as np

encodings_dict = {}

for filename in os.listdir("known_faces"):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join("known_faces", filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings: 
            encodings_dict[os.path.splitext(filename)[0]] = encodings[0].tolist()
        else:
            print(f"No face detected in {filename}. Skipping.")

with open("authorized_faces.json", "w") as json_file:
    json.dump(encodings_dict, json_file)

print("Face encodings saved to encodings.json")