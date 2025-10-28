#!/usr/bin/env python3
"""
Application runner for the Project Management API.

This script provides a convenient way to run the FastAPI application
with proper configuration and error handling.
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import application settings
from app.core.config import settings


def main():
    """Main function to run the FastAPI application."""

    # Set environment variables if not already set
    os.environ.setdefault("PYTHONPATH", str(project_root))

    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📍 Debug mode: {settings.debug}")
    print(f"🌐 Server will be available at: http://localhost:8000")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔍 Alternative docs: http://localhost:8000/redoc")
    print("-" * 50)

    try:
        # Run the application
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.debug,
            log_level="info" if settings.debug else "warning",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down the server...")
    except Exception as e:
        print(f"❌ Failed to start the server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()