import os
import fire
import uvicorn
from dotenv import load_dotenv

from app.database import init_db
from app.events import on_start
from app.utils import get_logger

# Load environment variables from .env file
load_dotenv()

logger = get_logger(__name__)


def run_app():
    """
    Run the application server.

    This function loads environment variables, initializes the database, and starts
    the FastAPI server.

    Raises
    ------
    RuntimeError
        If the application fails to start.
    """
    db_url = os.getenv("DB_URL", "sqlite:///./test.db")
    init_db(db_url)
    logger.info("Initializing data, this may take a few seconds...")
    on_start()
    logger.info("Initialization complete, starting server...")


if __name__ == "__main__":
    fire.Fire(run_app)
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000)
