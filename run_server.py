"""ADAPT-AI Server Launcher Script.

Usage:
    python run_server.py
"""

import uvicorn
from adapt_ai.config import settings


def main():
    print(f"Starting {settings.APP_NAME} on {settings.HOST}:{settings.PORT} (Debug: {settings.DEBUG})")
    uvicorn.run(
        "adapt_ai.api.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    main()

