from app.initializer import initialize_all
from app.utils import get_logger

logger = get_logger(__name__)

def on_start():
    """
    Function to run on application start.

    This function is responsible for initializing all necessary components of the application.
    It ensures proper setup and provides feedback through log messages. In case of failure,
    it captures and logs the exception.

    Raises
    ------
    Exception
        If an error occurs during the initialization process.

    Returns
    -------
    None
"""
    initialize_all()
    # Log a success message if initialization is successful
    logger.info("Application initialized successfully.")
