#!/usr/bin/env python3
"""
RAGSPRO DASHBOARD - Main Entry Point
This is the DEFAULT dashboard that always runs
Port: 5002
"""

# Import everything from the main RAGSPRO dashboard
from dashboard_ragspro import *

if __name__ == '__main__':
    import os
    
    # Get port from environment variable (for Render/Heroku) or default to 5002
    port = int(os.environ.get("PORT", 5002))
    debug_mode = os.environ.get("FLASK_ENV", "development") != "production"
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           RAGSPRO DASHBOARD - DEFAULT ENTRY              ║
    ║                                                          ║
    ║  🎯 Complete Lead Management System                      ║
    ║  💰 AI-Powered Content Generation                        ║
    ║  🚀 Real-time Lead Generation                            ║
    ║                                                          ║
    ║  This is your DEFAULT dashboard - always use this!       ║
    ╚══════════════════════════════════════════════════════════╝
    
    🚀 Dashboard running at: http://0.0.0.0:{port}
    📊 Open your browser and start generating premium leads!
    
    ⚡ Quick Commands:
       - Generate Leads: Click "Generate" button
       - View Leads: Automatically loaded
       - Search: Use search box
       - Export: Click "CSV" button
    """.format(port=port))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
