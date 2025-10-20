#!/usr/bin/env python3
"""
Student Emporium - Main Application Runner

This script starts the Student Emporium marketplace application.
"""

import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import and run the main app
if __name__ == '__main__':
    from app import app
    print("🚀 Starting Student Emporium...")
    print("📍 Open your browser and go to: http://127.0.0.1:5000")
    print("⚠️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Student Emporium stopped. Goodbye!")