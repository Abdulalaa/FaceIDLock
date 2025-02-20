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

#------------------------------------------------------------------------------
# Main Flow Module Imports
#------------------------------------------------------------------------------
import cv2                  # For camera vision
from picamera2 import Picamera2  # For connection to Pi camera module, needs testing in Pi OS
import time                 # For timing operations  
import logging             # For logging messages
import psutil              # For system monitoring

#------------------------------------------------------------------------------
# Configuration & Function Imports
#------------------------------------------------------------------------------
from faceID import verify_face
from serial_comm import unlock_door
from config import *

#------------------------------------------------------------------------------
# Logging Configuration
#------------------------------------------------------------------------------
# Configure logging for:
# - Security auditing
# - System diagnostics/monitoring
# - Troubleshooting/debugging/exceptions
# - System status
logging.basicConfig(
    filename="sys.log",    # Log file module
    encoding="utf-8",
    filemode="a",          # Append mode
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG    # Capture all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)

# Initialize logging
logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------
# camera (Picamera2), face_detector (CascadeClassifier), face_found (list of faces in frame)

#------------------------------------------------------------------------------
# Camera Initialization
#------------------------------------------------------------------------------
def initialize_camera():
    try:
        logger.debug("Initializing camera hardware and configurations...")
        camera = Picamera2()  # Initialize the camera hardware, resource allocation, and drivers through Picamera2
        camera.configure(camera_config)  # Configure the camera specs (camera_config is defined in config.py)
        camera.start()  # Start the camera
        time.sleep(2)  # Allow camera to warm up
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
        return None  # Return None if camera initialization fails

#------------------------------------------------------------------------------
# Face Detector Initialization
#------------------------------------------------------------------------------
def initialize_face_detector():
    try:
        logger.debug("Initializing face detector...")
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")  # cv2 + cascade classifier file path
        logger.info("Cascade classifier initialized successfully")
        return face_detector   
    except Exception as e:
        logger.warning(f"Error initializing cascade classifier: {e}")
        logger.debug("Attempting to restart face detector initialization...")
        return None  # Return None if cascade classifier initialization fails

#------------------------------------------------------------------------------
# Face Detection Loop
#------------------------------------------------------------------------------
def detect_face(camera, face_detector):
    while True:
        try:
            logger.debug("Initializing face detection...")
            face_found = []  # List of faces in frame
            while (len(face_found) != 1):  # Ensure only one face is in frame for safety, ensuring no forced entry
                frame = camera.capture_array()  # Capture a frame from the camera
                face_found = face_detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), cascade_classifier_config)  # Detect faces in the frame
                time.sleep(0.1)  # Add small delay to prevent CPU overload during continuous frame capture

            logger.debug("Face detected, beginning facial verification...")  # Break in face count logic when face is detected
            if verify_face(frame, face_found[0]):  # Check if the face in the frame is authorized
                logger.info("Face verified, unlocking door...") 
                unlock_door()  # If the face is authorized, unlock the door
                logger.info("Door unlocked successfully")
            else:
                logger.warning("Face not verified, continuing to monitor...")
                continue  # If the face is not authorized, continue to monitor

        except Exception as e:
            logger.warning(f"Error analyzing frames: {e}")
            logger.debug("Attempting to restart face detection...")
            return None  # Return None if face detection fails

#------------------------------------------------------------------------------
# Main Program Execution
#------------------------------------------------------------------------------
def main():
    # Initialize camera, 3 attempts maximum
    initialization_attempts = 0
    while initialization_attempts < MAX_ATTEMPTS:
        camera = initialize_camera()
        # Break if camera is initialized successfully
        if camera is not None:
            break
        initialization_attempts += 1
        time.sleep(0.1)  # Add small delay between initialization attempts
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
        time.sleep(0.1)  # Add small delay between initialization attempts
    # If face detector is not initialized after 3 attempts, exit program gracefully
    if face_detector is None:
        logger.critical("Face detector initialization failed after 3 attempts. Exiting program.")
        return

    # Begin face detection loop
    detect_face(camera, face_detector)

if __name__ == "__main__":
    main()
