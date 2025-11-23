# Quick Start Guide

Get up and running with RAG Copilot in 5 minutes!

## Prerequisites

1. **Python 3.11+** installed
2. **Ollama** (will be installed automatically - fully private, no API keys needed!)
3. **Atlassian API tokens** for Confluence and Jira:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Create tokens for both Confluence and Jira

## Step 1: Setup

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

## Step 2: Setup Ollama (Fully Private - Default)

Ollama is configured as the default for maximum privacy. Your data never leaves your network.

```bash
# Quick automated setup
./setup_ollama.sh

# Or manual:
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download models
ollama pull llama3.2
ollama pull nomic-embed-text

# 3. Start Ollama (keep running in a terminal)
ollama serve
```

## Step 3: Configure

Copy and edit `.env` file:

```bash
cp .env.example .env
```

The `.env.example` is already configured for Ollama. Just add your Atlassian credentials:

```bash
# Ollama is already configured (no API key needed!)
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# Add your credentials
CONF_BASE_URL=https://your-domain.atlassian.net/wiki
CONF_USER_EMAIL=your-email@company.com
CONF_API_TOKEN=your-confluence-token
CONF_SPACE_KEYS=ENG,PROD

JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_USER_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-jira-token
JIRA_JQL=project in (ENG,PROD) and statusCategory != Done
```

## Step 4: Ingest Data

```bash
# Ingest everything
python ingest_all.py

# Or ingest separately:
python -m ingest.confluence_ingest
python -m ingest.jira_ingest
```

**Note**: First ingestion may take several minutes depending on data volume.

## Step 5: Start Services

### Option A: Docker Compose (Recommended)

```bash
cd ops
docker-compose up -d
```

This starts:
- FastAPI on http://localhost:8000
- ChromaDB on http://localhost:8001
- OpenSearch on http://localhost:9200

Then start the UI:
```bash
streamlit run ui/app.py
```

### Option B: Manual

**Terminal 1 - FastAPI:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Streamlit UI:**
```bash
streamlit run ui/app.py
```

**Terminal 3 - OpenSearch (optional, if not using Docker):**
```bash
# Follow OpenSearch installation guide
```

## Step 6: Use It!

1. **Web UI**: Open http://localhost:8501
2. **API**: 
   ```bash
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"q": "What is the deployment process?"}'
   ```

## Troubleshooting

### "No documents found"
- Make sure you've run ingestion (`python ingest_all.py`)
- Check that your API tokens are correct
- Verify space keys/project keys exist

### "Ollama connection error"
- Make sure Ollama is running: `ollama serve`
- Check if models are downloaded: `ollama list`
- Verify Ollama is accessible: `curl http://localhost:11434/api/tags`

### "Model not found" error
- Download required models: `ollama pull llama3.2` and `ollama pull nomic-embed-text`

### "Connection refused" errors
- Make sure services are running
- Check ports aren't already in use
- For Docker: ensure containers are up (`docker-compose ps`)

## Next Steps

- Check `/health` endpoint to verify system status
- Use `/sources` to see what's been ingested
- Review OpenSearch logs at http://localhost:9200
- Customize chunking parameters in `ingest/common.py`
- Adjust retrieval parameters in `app/rag.py`

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the architecture diagram in the README
- Check logs in OpenSearch for query patterns

