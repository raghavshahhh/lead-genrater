#!/bin/bash

echo "🚀 Starting Lead Generation Dashboard..."
echo "=" 
echo ""
echo "📊 Dashboard will open at: http://localhost:5000"
echo "🔥 Features:"
echo "   ✅ One-click lead generation"
echo "   ✅ Real-time data display"
echo "   ✅ Search functionality"
echo "   ✅ Beautiful modern UI"
echo "   ✅ Auto-refresh every 30 seconds"
echo ""
echo "=" 
echo ""

# Activate virtual environment
source .venv/bin/activate

# Set Python path
export PYTHONPATH=.

# Start dashboard
python dashboard.py
