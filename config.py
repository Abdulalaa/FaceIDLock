"""
Configuration file for Face ID Lock System

Contains configuration variables and settings used across the application including:
- Camera settings
- Cascade classifier settings
- System parameters
- Logging settings
- Door open time
"""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import logging


#------------------------------------------------------------------------------
# Camera Config/Specs - (Needs testing and tweaking @Josh M.)
#------------------------------------------------------------------------------
camera_config = {
    "size": (2304,1296),  # Resolution 
    "fps": 30,  # Frame rate 
    "format": "BGR888",  # Color format for opencv 
    "controls": {
        "AfMode": 2,  # Auto focus mode
        "NoiseReductionMode": 2,  # Noise reduction mode to aid in face detection
    }
}

#------------------------------------------------------------------------------
# Cascade Classifier Settings - (Needs testing and tweaking @Josh M.)
#------------------------------------------------------------------------------
cascade_classifier_config = {
    "scaleFactor": 1.2,
    "minNeighbors": 6,
    "minSize": (100,100),
    "maxSize": (300,300)
}

#------------------------------------------------------------------------------
# System Parameters
#------------------------------------------------------------------------------
MAX_ATTEMPTS = 3
DOOR_OPEN_TIME = 5

#------------------------------------------------------------------------------
# Logging Settings
# Configure logging for:
# - Security auditing
# - System diagnostics/monitoring
# - Troubleshooting/debugging/exceptions
# - System status
#------------------------------------------------------------------------------
logging.basicConfig(
    filename="sys.log",    # Log file module
    encoding="utf-8",
    filemode="a",          # Append mode
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG    # Capture all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)


#------------------------------------------------------------------------------
# Face Recognition Settings
#------------------------------------------------------------------------------
TOLERANCE = 0.5