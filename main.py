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
import time # For timing operations
import logging # For logging messages
import psutil # For system monitoring

# Import configurations
from config import *

# Configure logging for security auditing, system diagnostics/monitoring, troubleshooting/debugging/exceptions, system status
# Will send logs to sys.log file
logging.basicConfig(
    filename="sys.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

