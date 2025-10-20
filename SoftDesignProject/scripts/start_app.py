#!/usr/bin/env python3
"""
Simple Flask app starter to test if the web interface works
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("✅ Successfully imported Flask app")
    
    print("📋 Available routes:")
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"   {rule.rule} [{methods}]")
    
    print("\n🚀 Starting Flask app on http://localhost:5000")
    print("📱 Admin login: admin@sea.com / admin123")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Failed to import Flask app: {e}")
except Exception as e:
    print(f"❌ Error starting Flask app: {e}")