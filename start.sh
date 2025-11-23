#!/bin/bash
# Quick start script for Zuno GPT

echo "🚀 Starting Zuno GPT..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if Ollama is running (if using Ollama)
if grep -q "LLM_PROVIDER=ollama" .env 2>/dev/null || grep -q "EMBEDDING_PROVIDER=ollama" .env 2>/dev/null; then
    if ! pgrep -x "ollama" > /dev/null; then
        echo "⚠️  Ollama doesn't appear to be running."
        echo "   Starting Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 2
    fi
fi

echo "📡 Starting FastAPI backend..."
uvicorn app.main:app --reload &
FASTAPI_PID=$!

echo "   ✅ FastAPI running on http://localhost:8000 (PID: $FASTAPI_PID)"
echo ""

sleep 2

echo "🎨 Starting Streamlit UI..."
streamlit run ui/app.py --server.headless true &
STREAMLIT_PID=$!

echo "   ✅ Streamlit running on http://localhost:8501 (PID: $STREAMLIT_PID)"
echo ""

echo "✅ Zuno GPT is running!"
echo ""
echo "📍 URLs:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - UI: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "kill $FASTAPI_PID $STREAMLIT_PID 2>/dev/null; exit" INT
wait
