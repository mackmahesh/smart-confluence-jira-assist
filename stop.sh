#!/bin/bash
# Stop script for Zuno GPT

echo "🛑 Stopping Zuno GPT services..."

# Kill FastAPI
pkill -f "uvicorn app.main:app" && echo "   ✅ Stopped FastAPI" || echo "   ⚠️  FastAPI not running"

# Kill Streamlit
pkill -f "streamlit run ui/app.py" && echo "   ✅ Stopped Streamlit" || echo "   ⚠️  Streamlit not running"

echo ""
echo "✅ All services stopped!"
