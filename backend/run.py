#!/usr/bin/env python3
"""
Main entry point for YouTube Automation System
"""

import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting AI YouTube Automation System...")
    print("📊 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    print("=" * 50)

    # Import string is required when reload=True (uvicorn spawns a subprocess).
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
