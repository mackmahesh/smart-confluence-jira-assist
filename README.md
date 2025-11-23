# RAG Copilot for Jira & Confluence

A production-lean RAG (Retrieval-Augmented Generation) system that answers engineering/product questions from Confluence pages and Jira issues using AI.

## Features

- 🔍 **Ingest** Confluence spaces and Jira issues into a vector store
- 💬 **Query** with natural language and get grounded answers with citations
- 📊 **Observability** with OpenSearch logging for queries, latency, and metrics
- 🎨 **Web UI** (Streamlit) and REST API for easy access
- 🔒 **Privacy-First** - Support for multiple AI providers (Azure OpenAI, Anthropic, Ollama, Local) to protect company data

## Quick Start

### 1. Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for OpenSearch)
- Atlassian API tokens for Confluence and Jira

### 2. Setup

```bash
# Clone and navigate to project
cd rag-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# - OpenAI API key
# - Confluence base URL, email, API token, space keys
# - Jira base URL, email, API token, JQL query
```

### 3. Setup Ollama (Fully Private - Default)

**Ollama is configured as the default provider for maximum privacy. Your data never leaves your network.**

```bash
# Quick setup (automated)
./setup_ollama.sh

# Or manual setup:
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download required models
ollama pull llama3.2
ollama pull nomic-embed-text

# 3. Start Ollama server (keep running)
ollama serve
```

**📖 See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed setup instructions.**

### 4. Configure Environment

Copy and edit `.env`:

```bash
cp .env.example .env
```

The `.env.example` is already configured for Ollama. Just add your Confluence and Jira credentials:

```bash
# Ollama is already configured (fully private)
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# Add your Atlassian credentials
CONF_BASE_URL=https://your-domain.atlassian.net/wiki
CONF_USER_EMAIL=you@company.com
CONF_API_TOKEN=your-token
CONF_SPACE_KEYS=ENG,PROD
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_USER_EMAIL=you@company.com
JIRA_API_TOKEN=your-token
JIRA_JQL=project in (ENG,PROD) and statusCategory != Done
```

**Note**: No OpenAI API key needed when using Ollama!

### 5. Ingest Data

```bash
# Ingest Confluence spaces
python -m ingest.confluence_ingest

# Ingest Jira issues
python -m ingest.jira_ingest
```

### 6. Start Services

**Option A: Docker Compose (Recommended)**

```bash
cd ops
docker-compose up -d
```

**Option B: Manual**

```bash
# Terminal 1: Start OpenSearch (if not using Docker)
# See OpenSearch docs for setup

# Terminal 2: Start FastAPI
uvicorn app.main:app --reload --port 8000

# Terminal 3: Start Streamlit UI
streamlit run ui/app.py
```

### 6. Use the System

- **Web UI**: Open http://localhost:8501
- **API**: `POST http://localhost:8000/ask` with `{"q": "your question"}`
- **Health**: `GET http://localhost:8000/health`

## Project Structure

```
rag-copilot/
├── app/                    # FastAPI application
│   ├── main.py            # API routes
│   ├── rag.py             # RAG pipeline
│   ├── deps.py            # Shared clients
│   ├── settings.py        # Configuration
│   ├── schemas.py         # Pydantic models
│   └── logging_mw.py      # OpenSearch logging
├── ingest/                # Data ingestion
│   ├── confluence_ingest.py
│   ├── jira_ingest.py
│   └── common.py          # Chunking & upsert
├── ui/                    # Streamlit UI
│   └── app.py
├── eval/                  # Evaluation scripts
│   └── datasets/
├── ops/                   # Docker & deployment
│   ├── docker-compose.yml
│   └── Dockerfile
└── tests/                 # Unit tests
```

## API Endpoints

### `POST /ask`

Query the RAG system.

**Request:**
```json
{
  "q": "What is the deployment process?",
  "k": 5
}
```

**Response:**
```json
{
  "answer": "The deployment process involves...",
  "sources": [
    {
      "source": "confluence",
      "title": "Deployment Guide",
      "url": "https://...",
      "space": "ENG"
    }
  ],
  "query": "What is the deployment process?",
  "latency_ms": 1234.5
}
```

### `GET /health`

Check system health and vector store status.

### `GET /sources`

List available sources and document counts.

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Data Sources

1. Create a new ingestion script in `ingest/`
2. Use `ingest.common.upsert_document()` to add documents
3. Ensure metadata includes `source`, `title`, and `url` fields

### Evaluation

Create evaluation datasets in `eval/datasets/` with questions, expected answers, and source URLs. Use `eval/offline_eval.ipynb` to measure:
- Recall@k
- Answer faithfulness
- Latency

## Architecture

```
Jira/Confluence APIs → Ingestion → Chunking → Embeddings → Vector DB
                                                              ↓
User Query → Embed Query → Retrieve → LLM Synthesis → Answer + Citations
                                                              ↓
                                                      OpenSearch Logging
```

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **RAG**: LangChain with multiple provider support:
  - **LLM**: OpenAI, Azure OpenAI, Anthropic Claude, Ollama (local)
  - **Embeddings**: OpenAI, Azure OpenAI, Ollama, Local (sentence-transformers)
- **Vector DB**: Chroma (local) / Pinecone (prod)
- **Search/Logs**: OpenSearch
- **UI**: Streamlit
- **Containers**: Docker Compose

## Success Metrics (MVP)

- **Answer grounding@k**: ≥ 0.75
- **Response time (P95)**: ≤ 2.5s for 10k docs
- **Human helpfulness rating**: ≥ 4/5

## Next Steps

1. Generate Atlassian API tokens
2. Configure space/project scopes
3. Run initial ingestion
4. Test queries and iterate on chunking/retrieval
5. Set up OpenSearch dashboards for observability

## License

Internal use only.

