"""Vercel serverless function entry point."""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import app

# Export for Vercel
handler = app
