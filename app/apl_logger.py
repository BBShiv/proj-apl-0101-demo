import logging
import os
from datetime import datetime

# Define the log directory and file name
LOG_DIR = "logs"
TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"logs-{TIMESTAMP}.log")

def setup_logging():
    """
    Sets up the logging configuration for the application.

    This function performs the following steps:
    1. Creates a 'logs' directory if it does not already exist.
    2. Configures the root logger to output messages to a file named
       'logs-{current-timestamp}.log' within the 'logs' directory.
    3. Sets the logging level to INFO, meaning all messages with severity
       INFO, WARNING, ERROR, and CRITICAL will be logged.
    4. Defines a log message format that includes timestamp, log level,
       logger name, and the actual message.
    """
    # Create the logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
            print(f"Created logging directory: {LOG_DIR}")
        except OSError as e:
            print(f"Error creating logging directory {LOG_DIR}: {e}")
            # If directory creation fails, logging to file might also fail.
            # We can still proceed with console logging or raise an error.
            # For now, we'll let the file handler potentially fail.

    # Configure the basic logging setup
    logging.basicConfig(
        level=logging.INFO,  # Set the minimum logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(LOG_FILE),  # Log to the specified file
            logging.StreamHandler()         # Also log to console
        ]
    )
    print(f"Logging configured. Logs will be saved to: {LOG_FILE}")

# Call setup_logging when this module is imported
setup_logging()