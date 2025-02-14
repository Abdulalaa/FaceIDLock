'''
# Loggging test code

import logging 

# Need to add configuration before any logging messages
# Use the style parameter to specify the format of the log message
logging.basicConfig(level=logging.DEBUG, format="{levelname}:{name}:{message}", style="{")

# Initialize logging
logger = logging.getLogger(__name__)

Logging levels
logging.warning("This is a warning")

logging.info("This is an info message")

logging.debug("This is a debug message")

logging.error("This is an error message")

logging.critical("This is a critical message")

Exception logging
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.exception("DonutCalculationError")

setup and logging to a log file
>>> import logging
>>> logging.basicConfig(
...     filename="app.log",
...     encoding="utf-8",
...     filemode="a",
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )
'''
