#!/usr/bin/env python3
"""
Main application entry point for Claude Code project.
This is the primary interface for running the application.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main application function."""
    print("🚀 Starting application...")
    print(f"📁 Project root: {Path(__file__).parent}")
    print("✅ Application started successfully")
    
    # TODO: Add your main application logic here
    # Example:
    # from src.your_project.core.app import App
    # app = App()
    # app.run()

if __name__ == "__main__":
    main()
