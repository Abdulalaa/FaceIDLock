# Loggging test code

import logging 

# Need to add configuration before any logging messages
# Use the style parameter to specify the format of the log message
logging.basicConfig(level=logging.DEBUG, format="{levelname}:{name}:{message}", style="{")

'''
Logging levels
logging.warning("This is a warning")

logging.info("This is an info message")

logging.debug("This is a debug message")

logging.error("This is an error message")

logging.critical("This is a critical message")
'''
