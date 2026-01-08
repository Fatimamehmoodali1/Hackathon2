"""Vercel serverless function entry point."""
import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Set environment defaults for Vercel
os.environ.setdefault("DATABASE_URL", os.environ.get("DATABASE_URL", ""))
os.environ.setdefault("BETTER_AUTH_SECRET", os.environ.get("BETTER_AUTH_SECRET", "default-secret-key"))
os.environ.setdefault("CORS_ORIGINS", os.environ.get("CORS_ORIGINS", "*"))

try:
    from main import app
    # Export for Vercel
    handler = app
except Exception as e:
    # Fallback for debugging
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"error": str(e), "message": "Failed to import main app"}

    @app.get("/health")
    def health():
        return {"status": "error", "error": str(e)}

    handler = app
