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
import numpy as np # For cv2 encoding processes

# Import configurations
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


# Begin execution of the program
# Note: Picamera2 is focused on starting the camera and configuration, CV2 is focused on image processing
def main():
    while True: # OUTER LOOP: Hardware Initialization
        try:
            # 1. Initialize the camera
            logger.info("Initializing camera...")
            camera = Picamera2() # Initialize the camera hardware, resource allocation, and drivers (Picamera2 for camera hardware and configuration)
            camera.configure(camera_config) # Configure the camera (camera_config is defined in config.py)
            camera.start() # Start the camera
            time.sleep(2) # Allow camera to warm up
            logger.info("Camera initialized successfully")

            # 2. Initialize the cascade classifier
            logger.info("Initializing cascade classifier...")
            face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # cv2 + cascade classifier file path
            logger.info("Cascade classifier initialized successfully")

            # 3. Begin recording/capturing frames
            logger.info("Beginning frame capture...")

            while True: # INNER LOOP: Frame Capture/Face Detection
                faces = []
                # 4. Begin checking for facial recognition in frames using Cascade Classifier (CV2 for image processing)
                # Cascade Classifier prioritizes speed for finding faces in frames, faceID will use face_recognition to verify faces
                logger.info("Checking for faces in frames...")
                while (len(faces) != 1): # Ensure only one face is in frame for safety, ensuring no forced entry
                    frame = camera.capture_array() # Capture a frame from the camera
                    faces = face_detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), cascade_classifier_config) # Detect faces in the frame
                    logger.info(f"Face detected in frame")

                logger.info("Beginning facial verification...")
            
                # 5. Begin facial verification

        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            logger.info("Attempting to restart...")
            time.sleep(2)  # Wait before retrying
            continue
