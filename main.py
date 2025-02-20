"""
A facial recognition security system that:
1. Captures and processes facial data
2. Matches against authorized user database
3. Controls access based on verification

Authors:
- Abdullah A.
- Dev R. 
- Josh M.
- Bryan R.

Modules:
- main.py - Main module for running the face recognition system, handles flow of execution
- authorized_faces.json - List of authurized faces in kew-value pairs
- config.py - Configuration variables and settings
- faceID.py - Face recognition and verification
- serial_comm.py - Serial communication with the Arduino
- requirements.txt - List of dependencies
- sys.log - Log file for security auditing, system diagnostics/monitoring, troubleshooting/debugging/exceptions, system status

---------------------------------------------                                                
Secure Facial Recognition Access Control System
---------------------------------------------
"""
# Import necessary main flow modules
import cv2 # For camera vision
from picamera2 import Picamera2 # For connection to Pi camera module, needs testing in Pi OS
import time # For timing operations
import logging # For logging messages
import psutil # For system monitoring
import numpy as np # For dealing with numpy arrays

# Import configurations
from faceID import 
from serial_comm import
from config import *
# Other imports from other files will go here!!!!!

# Configure logging for security auditing, system diagnostics/monitoring, troubleshooting/debugging/exceptions, system status
# Will send logs to sys.log file
logging.basicConfig(
    filename="sys.log", # log file module
    encoding="utf-8",
    filemode="a",       # append mode
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG # Capture all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)

# Initialize logging
logger = logging.getLogger(__name__)

# Variables: camera (Picamera2), face_detector (CascadeClassifier), face_found (list of faces in frame)


# 1. Function to initialize the camera hardware and configurations
def initialize_camera():
    try:
        logger.debug("Initializing camera hardware and configurations...")
        camera = Picamera2() # Initialize the camera hardware, resource allocation, and drivers through Picamera2
        camera.configure(camera_config) # Configure the camera specs (camera_config is defined in config.py)
        camera.start() # Start the camera
        time.sleep(2) # Allow camera to warm up
        logger.info("Camera initialized successfully")
        return camera
    except Exception as e:
        logger.warning(f"Error initializing camera: {e}")
        logger.debug("Attempting to restart camera initialization...")
        # Stop and clean up camera resources if they exist
        try:
            camera.stop()
            camera.close()
        except:
            pass  # Camera may not have been initialized, do nothing
        return None # Return None if camera initialization fails

# 2. Function to initialize the face detector (cascade classifier)
def initialize_face_detector():
    try:
        logger.debug("Initializing face detector...")
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # cv2 + cascade classifier file path
        logger.info("Cascade classifier initialized successfully")
        return face_detector   
    except Exception as e:
        logger.warning(f"Error initializing cascade classifier: {e}")
        logger.debug("Attempting to restart face detector initialization...")
        return None # Return None if cascade classifier initialization fails

# 3. Function to initialize the facial search model
# Begin face detection loop
def detect_verify_face(camera, face_detector):
    while True:
        try:
            logger.debug("Initializing face detection...")
            face_found = [] # List of faces in frame
            while (len(face_found) != 1): # Ensure only one face is in frame for safety, ensuring no forced entry
                frame = camera.capture_array() # Capture a frame from the camera
                face_found = face_detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), cascade_classifier_config) # Detect faces in the frame
            
            logger.debug("Face detected, beginning facial verification...") # Break in face count logic when face is detected

            if faceID(frame, face_found[0]):
                logger.info("Face verified, unlocking door...")
                unlock_door()
                logger.info("Door unlocked successfully")
            else:
                logger.warning("Face not verified, continuing to monitor...")
                continue

        except Exception as e:
            logger.warning(f"Error analyzing frames: {e}")
            logger.debug("Attempting to restart face detection...")
            return None # Return None if face detection fails
        



def main():
    # Initialize camera, 3 attempts maximum
    initialization_attempts = 0
    while initialization_attempts < MAX_ATTEMPTS:
        camera = initialize_camera()
        # Break if camera is initialized successfully
        if camera is not None:
            break
        initialization_attempts += 1
    # If camera is not initialized after 3 attempts, exit program gracefully
    if camera is None:
        logger.critical("Camera initialization failed after 3 attempts. Exiting program.")
        return
    
    # Initialize face detector, 3 attempts maximum
    face_detector_attempts = 0
    while face_detector_attempts < MAX_ATTEMPTS:
        face_detector = initialize_face_detector()
        # Break if face detector is initialized successfully
        if face_detector is not None:
            break
        face_detector_attempts += 1
    # If face detector is not initialized after 3 attempts, exit program gracefully
    if face_detector is None:
        logger.critical("Face detector initialization failed after 3 attempts. Exiting program.")
        return

    # Initialize facial search model, 3 attempts maximum
    facial_search_attempts = 0
    while facial_search_attempts < MAX_ATTEMPTS:
        facial_search = detect_verify_face(camera, face_detector)
        # Break if facial search model is initialized successfully
        if facial_search is not None:
            break
        facial_search_attempts += 1
    # If facial search model is not initialized after 3 attempts, exit program gracefully
    if facial_search is None:
        logger.critical("Facial search model initialization failed after 3 attempts. Exiting program.")
        return
