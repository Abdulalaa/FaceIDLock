
"""
Configuration file for Face ID Lock System

Contains configuration variables and settings used across the application including:
- Camera settings
- Logging configuration  
- System parameters

Authors:
- Abdullah A.
- Dev R.
- Josh M. 
- Bryan R.
"""

# Camera Recording Config/Specs (REQUIRES TESTING AND TWEAKING!!!) @Josh M.
camera_config = {
    "size": (2304,1296),  # Resolution 
    "fps": 30,  # Frame rate 
    "format": "RGB888",  # Color format
    "controls": {
        "AfMode": 2,  # Auto focus mode
        "NoiseReductionMode": 2,  # Noise reduction mode to aid in face detection
    }
}

# Cascade Classifier Config/Specs (REQUIRES TESTING AND TWEAKING!!!) @Josh M.
cascade_classifier_config = {
    "scaleFactor": 1.2,
    "minNeighbors": 6,
    "minSize": (100,100),
    "maxSize": (300,300)
}


