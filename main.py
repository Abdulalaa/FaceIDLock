"""
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
# Main Module Imports
#------------------------------------------------------------------------------
import cv2                  # For camera vision
from picamera2 import Picamera2  # For connection to Pi camera module, needs testing in Pi OS
import time                 # For timing operations  
import logging              # For logging events and errors
import json                 # For loading authorized faces
import numpy as np          # For numerical operations
#------------------------------------------------------------------------------
# Configuration & Function Imports
#------------------------------------------------------------------------------
from faceID import verify_face  # Import face verification function
from serial_comm import unlock_door  # Import door control function
from config import *  # Import all configuration variables from config.py

#------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------
logger = logging.getLogger(__name__)  # Get a logger instance for this module
logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG to capture all messages


#------------------------------------------------------------------------------
# Import JSON file - load and convert to numpy array
#------------------------------------------------------------------------------
def load_json_file():
    """
    Loads authorized face encodings from JSON file
    
    Returns:
        dict: Dictionary of face encodings and their corresponding names, or False if loading fails
    """
    try:
        with open("authorized_faces.json", "r") as json_file:
            encodings_dict = json.load(json_file)
            return encodings_dict  # encodings_dict is a dictionary of face encodings and their corresponding names
    except OSError:
        logger.error("Problem loading authorized_faces.json")
        return False  # Return False if file cannot be loaded

#------------------------------------------------------------------------------
# Camera Initialization
#------------------------------------------------------------------------------
def initialize_camera():
    """
    Initializes and configures the Raspberry Pi camera
    
    Returns:
        Picamera2: Configured camera object, or None if initialization fails
    """
    try:
        logger.debug("Initializing camera hardware and configurations...")
        camera = Picamera2()  # Initialize the camera hardware, resource allocation, and drivers through Picamera2
        camera.configure(camera_config)  # Configure the camera specs (camera_config is defined in config.py)
        camera.start()  # Start the camera
        time.sleep(2)  # Allow camera to warm up
        logger.info("Camera initialized successfully")
        return camera  # Return camera object if initialization succeeds
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
    """
    Initializes the OpenCV face detector using Haar Cascade Classifier
    
    Returns:
        cv2.CascadeClassifier: Configured face detector, or None if initialization fails
    """
    try:
        logger.debug("Initializing face detector...")
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")  # cv2 + cascade classifier file path
        logger.info("Cascade classifier initialized successfully")
        return face_detector  # Return face detector if initialization succeeds
    except Exception as e:
        logger.warning(f"Error initializing cascade classifier: {e}")
        logger.debug("Attempting to restart face detector initialization...")
        return None  # Return None if cascade classifier initialization fails

#------------------------------------------------------------------------------
# Face Detection Loop
#------------------------------------------------------------------------------
def detect_face(camera, face_detector, encodings_dict):
    """
    Continuously monitors camera feed for faces and verifies them against authorized faces
    
    Args:
        camera: Initialized camera object
        face_detector: Initialized face detector
        encodings_dict: Dictionary of authorized face encodings
    """
    while True:
        try:            
            logger.debug("Initializing face detection...")
            face_found = np.empty((0, 4))  # Will store detected faces from detectMultiScale with shape (0,4)
            while (len(face_found) != 1):  # Ensure only one face is in frame for safety, ensuring no forced entry
                frame = camera.capture_array()  # Capture a frame from the camera
                face_found = face_detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), **cascade_classifier_config)  # Detect faces in the frame
                time.sleep(0.1)  # Add small delay to prevent CPU overload during continuous frame capture

            logger.debug("Face detected, beginning facial verification...")  # Break in face count logic when face is detected
            if verify_face(frame, face_found[0], encodings_dict):  # Check if the face in the frame is authorized
                logger.info("Unlocking door...") 
                if unlock_door():  # If the face is authorized, unlock the door
                    logger.info("Door unlocked successfully")
                else:
                    logger.error("Failed to unlock door, retry face verification")

            else:
                logger.warning("Unauthorized face detected, continuing to monitor...")
                # Continue monitoring

        except Exception as e:
            logger.warning(f"Error analyzing frames: {e}")
            logger.debug("Attempting to restart face detection...")
            time.sleep(1)  # Wait before retrying
            # Continue the loop
            

#------------------------------------------------------------------------------
# Main Program Execution
#------------------------------------------------------------------------------
def main():
    """
    Main function that orchestrates the entire face recognition system
    """
    camera = None
    try:
        # Load JSON file, return dictionary of face encodings and their corresponding names
        encodings_dict = load_json_file()
        if not encodings_dict:
            logger.critical("Failed to load authorized faces. Exiting program.")
            return
        
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

        # Begin face detection loop with the loaded encodings_dict
        detect_face(camera, face_detector, encodings_dict)
    except Exception as e:
        logger.critical(f"Unexpected error in main program: {e}")
    finally:
        # Clean up resources
        if camera is not None:
            logger.info("Cleaning up camera resources...")
            try:
                camera.stop()
                camera.close()
                logger.info("Camera resources released successfully")
            except Exception as e:
                logger.error(f"Error releasing camera resources: {e}")

if __name__ == "__main__":
    main()
