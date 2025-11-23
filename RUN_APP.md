# How to Run Zuno GPT

## Quick Start

### 1. Start the FastAPI Backend

Open a terminal and run:

```bash
cd /Users/uavalapati/Documents/Git/miniproject
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

You can verify it's running by visiting:
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### 2. Start the Streamlit UI

Open a **new terminal** (keep the FastAPI terminal running) and run:

```bash
cd /Users/uavalapati/Documents/Git/miniproject
streamlit run ui/app.py --server.headless true
```

The UI will be available at: **http://localhost:8501**

Your browser should open automatically, or you can manually visit the URL.

---

## Running Both Services

### Option 1: Two Separate Terminals (Recommended)

**Terminal 1** (FastAPI):
```bash
cd /Users/uavalapati/Documents/Git/miniproject
uvicorn app.main:app --reload
```

**Terminal 2** (Streamlit):
```bash
cd /Users/uavalapati/Documents/Git/miniproject
streamlit run ui/app.py --server.headless true
```

### Option 2: Background Process

**Terminal 1** (FastAPI in background):
```bash
cd /Users/uavalapati/Documents/Git/miniproject
uvicorn app.main:app --reload &
```

**Terminal 2** (Streamlit):
```bash
cd /Users/uavalapati/Documents/Git/miniproject
streamlit run ui/app.py --server.headless true
```

### Option 3: Using Docker Compose (Future)

```bash
cd /Users/uavalapati/Documents/Git/miniproject/ops
docker-compose up
```

---

## Prerequisites

Before running, make sure:

1. **Ollama is running** (if using Ollama):
   ```bash
   ollama serve
   ```
   Or check if it's already running:
   ```bash
   ps aux | grep ollama
   ```

2. **Environment is set up**:
   ```bash
   # Activate virtual environment (if using one)
   source venv/bin/activate  # or: conda activate your-env
   
   # Verify dependencies
   pip list | grep -E "fastapi|streamlit|langchain"
   ```

3. **`.env` file exists** with your configuration:
   ```bash
   ls -la .env
   ```

---

## Verification

### Check FastAPI is Running
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"ok": true, "vector_db": "chroma", "collection_count": 358}
```

### Check Streamlit is Running
Open browser: http://localhost:8501

You should see the Zuno GPT interface.

---

## Stopping the Services

### Stop FastAPI
Press `Ctrl+C` in the FastAPI terminal

### Stop Streamlit
Press `Ctrl+C` in the Streamlit terminal

Or if running in background:
```bash
pkill -f "uvicorn app.main:app"
pkill -f "streamlit run"
```

---

## Troubleshooting

### Port Already in Use

If port 8000 or 8501 is already in use:

**FastAPI on different port:**
```bash
uvicorn app.main:app --reload --port 8001
```

**Streamlit on different port:**
```bash
streamlit run ui/app.py --server.headless true --server.port 8502
```

Then update the API URL in Streamlit sidebar to match.

### Ollama Not Running

If you see embedding/LLM errors:

```bash
# Start Ollama
ollama serve

# In another terminal, verify models are available
ollama list
```

### Module Not Found Errors

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## Quick Reference

| Service | Command | URL | Port |
|---------|---------|-----|------|
| FastAPI | `uvicorn app.main:app --reload` | http://localhost:8000 | 8000 |
| Streamlit | `streamlit run ui/app.py --server.headless true` | http://localhost:8501 | 8501 |
| API Docs | Visit http://localhost:8000/docs | - | 8000 |

---

## Development Tips

1. **Auto-reload**: Both services support auto-reload on code changes
2. **Logs**: Check terminal output for errors
3. **API Testing**: Use http://localhost:8000/docs for interactive API testing
4. **UI Testing**: Use http://localhost:8501 for the web interface

---

**That's it!** You're ready to use Zuno GPT. 🚀


