"""
serial_comm.py

This script handles serial communication with the Arduino/microcontroller
for controlling the door lock mechanism.

"""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import logging  # For logging events and errors
import serial   # PySerial library for serial communication
from config import *  # Import all configuration variables from config.py

#------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------
logger = logging.getLogger(__name__)  # Get a logger instance for this module

#------------------------------------------------------------------------------
# Serial Connection Initialization
#------------------------------------------------------------------------------
def initialize_serial_connection():
    """Attempts to establish a serial connection with the microcontroller"""
    try:
        logger.debug("Initializing serial connection...")
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)  # Create serial connection using config values
        logger.info("Serial connection initialized successfully")
        return ser
    except Exception as e:
        logger.error(f"Error initializing serial connection: {e}")
        return None  # Return None if connection fails

# Initialize serial connection with retry mechanism
current_attempts = 0  # Counter for connection attempts
ser = None  # Serial connection object, initially None
while current_attempts < MAX_ATTEMPTS:  # Try to connect up to MAX_ATTEMPTS times
    ser = initialize_serial_connection()
    if ser is not None:
        break  # Exit the loop if connection is successful
    logger.info(f"Serial connection failed. Retrying...")
    current_attempts += 1  # Increment attempt counter if connection failed

#------------------------------------------------------------------------------
# Door Control Functions
#------------------------------------------------------------------------------
def unlock_door():
    """
    Send unlock signal to the connected Arduino/microcontroller
    """
    try:
        if ser and ser.is_open:  # Check if serial connection exists and is open
            ser.write(b'UNLOCK\n')  # Send the unlock command as bytes to Arduino
            logger.info("Unlock signal sent successfully")
            return True  # Return success
        else:
            logger.error("Cannot unlock door: Serial connection not established")
            logger.info("Attempting to reconnect to serial port...")
            ser = initialize_serial_connection()
            if ser and ser.is_open:
                ser.write(b'UNLOCK\n')
                logger.info("Unlock signal sent successfully")
                return True
            else:
                logger.error("Failed to reconnect to serial port")
                return False  # Return failure if no connection    
    except Exception as e:
        logger.error(f"Error sending unlock signal: {e}")
        return False  # Return failure if any exception occurs
