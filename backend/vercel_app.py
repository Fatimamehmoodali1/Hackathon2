"""Vercel serverless app - simplified entry point."""
import os
import sys
from pathlib import Path

# Add src to Python path
root_dir = Path(__file__).parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

# Set default environment variables
os.environ.setdefault("DATABASE_URL", os.environ.get("DATABASE_URL", ""))
os.environ.setdefault("BETTER_AUTH_SECRET", os.environ.get("BETTER_AUTH_SECRET", "vercel-default-secret-key-32-chars"))
os.environ.setdefault("CORS_ORIGINS", os.environ.get("CORS_ORIGINS", "https://frontend-fatima-mehmood-alis-projects.vercel.app"))
os.environ.setdefault("APP_HOST", "0.0.0.0")
os.environ.setdefault("APP_PORT", "8000")

# Import the FastAPI app
from main import app

# This is what Vercel will use
handler = app
