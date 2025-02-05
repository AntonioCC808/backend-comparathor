import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "#{CORS_ORIGINS}#")

origins = CORS_ORIGINS.split(",")


def add_cors(app: FastAPI):
    """
    Configure CORS middleware for the FastAPI application.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application.

    Returns
    -------
    None
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
