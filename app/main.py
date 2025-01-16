import os
import fire
import uvicorn
from dotenv import load_dotenv

from app.database import init_db

# Load environment variables from .env file
load_dotenv()


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
    print(f"Using database: {db_url}")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    fire.Fire(run_app)
    uvicorn.run("app.api:app", host="0.0.0.0", port=port)
