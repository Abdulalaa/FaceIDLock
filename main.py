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
- face_recognition.py - Face recognition and verification
- serial_comm.py - Serial communication with the Arduino
- requirements.txt - List of dependencies

---------------------------------------------                                                
Secure Facial Recognition Access Control System
---------------------------------------------
"""
# Import modules for camera vision, time, and logging
import cv2
import time
import logging


