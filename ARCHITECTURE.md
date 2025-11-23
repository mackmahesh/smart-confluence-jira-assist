# Zuno GPT - Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Key Technologies](#key-technologies)
4. [System Components](#system-components)
5. [Data Flow](#data-flow)
6. [Project Structure](#project-structure)
7. [Configuration](#configuration)
8. [Main Logic Flow](#main-logic-flow)

---

## Overview

**Zuno GPT** is an enterprise RAG (Retrieval-Augmented Generation) copilot that answers questions from Confluence pages and Jira issues. It uses vector embeddings, semantic search, and LLM generation to provide context-aware answers with source citations.

### Key Features
- **Privacy-First**: Supports multiple AI providers (Ollama, Azure OpenAI, Anthropic, OpenAI, Local)
- **Vector Search**: Semantic search across ingested documents
- **Source Citations**: Answers include links back to original documents
- **Observability**: OpenSearch logging for queries and performance
- **Incremental Ingestion**: Test with small samples before full ingestion

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Sources                            │
├──────────────────────┬──────────────────────────────────────────┤
│  Confluence (REST)   │         Jira (REST API)                  │
│  - Pages             │         - Issues (JQL)                    │
│  - Spaces            │         - Projects                       │
└──────────┬───────────┴──────────────┬───────────────────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Ingestion Layer                              │
│  ┌────────────────────┐      ┌────────────────────┐            │
│  │ confluence_ingest  │      │   jira_ingest      │            │
│  │ - Fetch pages      │      │ - Fetch issues     │            │
│  │ - HTML → Markdown │      │ - Extract ADF      │            │
│  │ - Chunk text       │      │ - Chunk text       │            │
│  └─────────┬──────────┘      └──────────┬─────────┘            │
│            │                            │                       │
│            └────────────┬────────────────┘                       │
│                         ▼                                       │
│              ┌──────────────────────┐                           │
│              │   common.py          │                           │
│              │ - Text chunking     │                           │
│              │ - Embedding         │                           │
│              │ - Vector upsert     │                           │
│              └──────────┬───────────┘                           │
└─────────────────────────┼───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vector Store (ChromaDB)                      │
│  Collection: "jira_conf"                                         │
│  - Document chunks                                              │
│  - Embeddings (vectors)                                         │
│  - Metadata (source, title, URL, space, etc.)                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (app/rag.py)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. User Query                                            │   │
│  │ 2. Embed Query → Vector Search → Retrieve Top-K Docs    │   │
│  │ 3. Build Context from Retrieved Documents              │   │
│  │ 4. Generate Answer using LLM (Ollama/OpenAI/etc.)       │   │
│  │ 5. Format Response with Sources                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ /health  - System health check                           │   │
│  │ /ask     - Main query endpoint                           │   │
│  │ /sources - List available sources                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    UI Layer (Streamlit)                         │
│  - Query input                                                  │
│  - Answer display                                               │
│  - Source citations                                             │
│  - Metrics (latency, sources)                                  │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Observability (OpenSearch)                          │
│  - Query logging                                                │
│  - Latency metrics                                              │
│  - Retrieval metrics                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Technologies

### Core Framework
- **Python 3.11+**: Main programming language
- **FastAPI**: REST API framework (async, high performance)
- **Streamlit**: Web UI framework (rapid prototyping)

### RAG & AI
- **LangChain**: RAG pipeline orchestration
- **ChromaDB**: Vector database (local development)
- **Ollama**: Local LLM and embeddings (default, fully private)
- **OpenAI**: Cloud LLM and embeddings (optional)
- **Azure OpenAI**: Enterprise cloud LLM (optional)
- **Anthropic Claude**: Alternative cloud LLM (optional)
- **Sentence Transformers**: Local embeddings (optional)

### Data Processing
- **BeautifulSoup4**: HTML parsing
- **markdownify**: HTML to Markdown conversion
- **NLTK**: Natural language processing utilities
- **httpx**: Async HTTP client for API calls

### Observability
- **OpenSearch**: Logging and metrics storage
- **opensearch-py**: Python client for OpenSearch

### Data Sources
- **Confluence REST API**: Page ingestion
- **Jira REST API**: Issue ingestion via JQL

---

## System Components

### 1. Ingestion Layer (`ingest/`)

#### `confluence_ingest.py`
- **Purpose**: Fetch and ingest Confluence pages
- **Key Functions**:
  - `ingest_space(space_key, limit=None)`: Ingest all pages from a space
  - `ingest_all_spaces()`: Ingest all configured spaces
  - `html_to_text(html)`: Convert Confluence HTML to clean markdown
- **Authentication**: Supports OAuth Bearer token and Basic Auth
- **Pagination**: Fetches pages in batches of 50, continues until all pages retrieved
- **Output**: Chunked text with metadata (title, URL, space, version)

#### `jira_ingest.py`
- **Purpose**: Fetch and ingest Jira issues
- **Key Functions**:
  - `ingest_jql(limit=None)`: Ingest issues matching JQL query
  - `extract_text_from_atlassian_doc(content)`: Parse ADF (Atlassian Document Format)
- **Authentication**: Supports OAuth Bearer token and Basic Auth
- **Pagination**: Fetches issues in batches of 100
- **Output**: Chunked text with metadata (key, title, project, status, URL)

#### `common.py`
- **Purpose**: Shared ingestion utilities
- **Key Functions**:
  - `upsert_document(text, metadata, collection_name="jira_conf")`:
    - Splits text into chunks (1200 chars, 150 overlap)
    - Generates embeddings
    - Upserts to ChromaDB with metadata
  - `clean_text(text)`: Removes extra whitespace
- **Chunking Strategy**: RecursiveCharacterTextSplitter from LangChain

### 2. RAG Pipeline (`app/rag.py`)

#### `retrieve(query, k=5)`
- **Purpose**: Semantic search in vector store
- **Process**:
  1. Embed user query using configured embedding model
  2. Query ChromaDB for top-k similar documents
  3. Return LangChain Document objects with metadata

#### `answer(query, k=5)`
- **Purpose**: Generate answer using RAG
- **Process**:
  1. Retrieve top-k relevant documents
  2. Build context string from document chunks
  3. Create prompt with system instructions, context, and user query
  4. Generate answer using configured LLM
  5. Format response with sources and metadata
- **Response Format**:
  ```python
  {
      "answer": "Generated answer text",
      "sources": [Source objects with metadata],
      "query": "Original query",
      "latency_ms": 1234.56
  }
  ```

### 3. API Layer (`app/main.py`)

#### Endpoints

**`GET /health`**
- Health check endpoint
- Returns: `{"ok": true, "vector_db": "chroma", "collection_count": N}`

**`POST /ask`**
- Main query endpoint
- Request: `{"q": "user question", "k": 5}`
- Response: RAG answer with sources
- Logs to OpenSearch (if configured)

**`GET /sources`**
- List available sources in vector store
- Returns: Total documents and breakdown by source type

### 4. Dependency Injection (`app/deps.py`)

#### `get_chroma_client()`
- Returns: ChromaDB PersistentClient
- Path: `.chroma/` (local development)

#### `get_embeddings()`
- Returns: Embedding model based on `EMBEDDING_PROVIDER`
- Supports:
  - `ollama`: OllamaEmbeddings (default)
  - `openai`: OpenAIEmbeddings
  - `azure_openai`: AzureOpenAIEmbeddings
  - `local`: HuggingFaceEmbeddings (sentence-transformers)

#### `get_llm()`
- Returns: LLM model based on `LLM_PROVIDER`
- Supports:
  - `ollama`: ChatOllama (default)
  - `openai`: ChatOpenAI
  - `azure_openai`: AzureChatOpenAI
  - `anthropic`: ChatAnthropic

### 5. Configuration (`app/settings.py`)

Uses `pydantic-settings` to load from environment variables (`.env` file).

**Key Settings**:
- Provider selection (LLM and embeddings)
- API keys and endpoints
- Model names
- Vector DB configuration
- Confluence/Jira credentials
- OpenSearch configuration

### 6. Observability (`app/logging_mw.py`)

- Logs RAG events to OpenSearch
- Tracks: query, latency, retrieved documents, model used
- Index: `rag-events`

---

## Data Flow

### Ingestion Flow

```
1. User runs: python ingest_confluence_only.py
   ↓
2. Script reads CONF_SPACE_KEYS from .env
   ↓
3. For each space:
   a. Fetch pages via Confluence REST API (paginated)
   b. Convert HTML to markdown
   c. For each page:
      - Chunk text (1200 chars, 150 overlap)
      - Generate embeddings
      - Upsert to ChromaDB with metadata
   ↓
4. Repeat for Jira (if configured)
```

### Query Flow

```
1. User submits query in UI
   ↓
2. Streamlit sends POST /ask with query
   ↓
3. FastAPI receives request
   ↓
4. RAG pipeline:
   a. Embed query → [0.23, 0.45, ...]
   b. Vector search → Top 5 similar documents
   c. Build context: "[1] Doc1: ...\n[2] Doc2: ..."
   d. Create prompt: SYSTEM + CONTEXT + USER_QUESTION
   e. LLM generates answer
   ↓
5. Format response with sources
   ↓
6. Log to OpenSearch (async)
   ↓
7. Return JSON to UI
   ↓
8. UI displays answer and sources
```

---

## Project Structure

```
rag-copilot/
├── app/                          # FastAPI application
│   ├── __init__.py
│   ├── main.py                   # FastAPI routes (/health, /ask, /sources)
│   ├── deps.py                   # Dependency injection (clients, models)
│   ├── rag.py                    # RAG pipeline (retrieve + generate)
│   ├── schemas.py                # Pydantic models (AskRequest, AskResponse)
│   ├── settings.py               # Configuration from .env
│   └── logging_mw.py             # OpenSearch logging middleware
│
├── ingest/                       # Data ingestion scripts
│   ├── __init__.py
│   ├── common.py                 # Shared utilities (chunking, upsert)
│   ├── confluence_ingest.py      # Confluence page ingestion
│   └── jira_ingest.py            # Jira issue ingestion
│
├── ui/                           # Streamlit web UI
│   └── app.py                    # Main UI application
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_rag.py
│
├── eval/                         # Evaluation datasets
│   └── datasets/
│
├── ops/                          # Operations & deployment
│   ├── docker-compose.yml        # Local development stack
│   └── Dockerfile
│
├── ingest_all.py                 # Full ingestion script
├── ingest_confluence_only.py    # Confluence-only ingestion
├── ingest_jira_only.py          # Jira-only ingestion
├── ingest_test.py               # Test ingestion (small sample)
│
├── setup.sh                      # Initial setup script
├── setup_ollama.sh              # Ollama installation script
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
│
├── README.md                      # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── OLLAMA_SETUP.md              # Ollama setup instructions
├── PRIVACY_GUIDE.md             # Privacy options guide
├── INGESTION_GUIDE.md           # Ingestion guide
└── ARCHITECTURE.md               # This file
```

---

## Configuration

### Environment Variables (`.env`)

#### Provider Selection
```bash
LLM_PROVIDER=ollama              # ollama, openai, azure_openai, anthropic
EMBEDDING_PROVIDER=ollama         # ollama, openai, azure_openai, local
```

#### Ollama (Default - Fully Private)
```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_LLM_MODEL=llama3.2
```

#### OpenAI (Optional)
```bash
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-large
GENERATION_MODEL=gpt-4o-mini
```

#### Azure OpenAI (Optional)
```bash
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

#### Anthropic (Optional)
```bash
ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

#### Vector Database
```bash
VECTOR_DB=chroma                 # chroma or pinecone
CHROMA_PATH=.chroma              # Local ChromaDB path
```

#### Confluence
```bash
CONF_BASE_URL=https://wiki.aligntech.com
CONF_USER_EMAIL=user@company.com
CONF_API_TOKEN=...               # OAuth Bearer token or API token
CONF_SPACE_KEYS=MPS,SPACE2       # Comma-separated space keys
```

#### Jira
```bash
JIRA_BASE_URL=https://jira.aligntech.com
JIRA_USER_EMAIL=user@company.com
JIRA_API_TOKEN=...
JIRA_JQL=project = "Project Name" and statusCategory != Done
```

#### OpenSearch (Optional)
```bash
OPENSEARCH_URL=http://localhost:9200
OPENSEARCH_USER=admin
OPENSEARCH_PASS=admin
```

---

## Main Logic Flow

### 1. Ingestion Process

```python
# Example: Ingest Confluence space
async def ingest_space(space_key: str, limit: Optional[int] = None):
    # 1. Authenticate (OAuth Bearer or Basic Auth)
    auth_headers = get_auth_headers()
    
    # 2. Fetch pages (paginated)
    while True:
        pages = await fetch_pages(space_key, start=start, limit=50)
        
        # 3. Process each page
        for page in pages:
            # Extract HTML content
            html = page["body"]["storage"]["value"]
            
            # Convert to markdown
            text = html_to_text(html)
            
            # Build metadata
            metadata = {
                "source": "confluence",
                "title": page["title"],
                "url": page["_links"]["webui"],
                "space": space_key,
                ...
            }
            
            # Chunk, embed, and upsert
            upsert_document(text, metadata)
        
        # Check if more pages
        if len(pages) < 50:
            break
        start += len(pages)
```

### 2. Query Processing

```python
# User asks: "What is Process Automator?"
async def answer(query: str, k: int = 5):
    # 1. Retrieve relevant documents
    docs = retrieve(query, k=k)
    # → Vector search finds top 5 similar chunks
    
    # 2. Build context
    context = "\n\n".join([
        f"[{i+1}] {doc.metadata['title']}: {doc.page_content[:1200]}"
        for i, doc in enumerate(docs)
    ])
    
    # 3. Create prompt
    prompt = f"""
    SYSTEM: You are an internal assistant...
    
    CONTEXT:
    {context}
    
    USER QUESTION: {query}
    
    ANSWER:
    """
    
    # 4. Generate answer
    llm = get_llm()  # Ollama, OpenAI, etc.
    response = await llm.ainvoke(prompt)
    answer_text = response.content if hasattr(response, 'content') else str(response)
    
    # 5. Format sources
    sources = [Source(**doc.metadata) for doc in docs]
    
    # 6. Return response
    return {
        "answer": answer_text,
        "sources": sources,
        "query": query,
        "latency_ms": elapsed_time
    }
```

### 3. Vector Search Details

```python
def retrieve(query: str, k: int = 5):
    # 1. Get embedding model
    emb = get_embeddings()  # Ollama, OpenAI, etc.
    
    # 2. Embed query
    query_vector = emb.embed_query(query)
    # → [0.23, -0.45, 0.67, ...] (1536 dims for nomic-embed-text)
    
    # 3. Search vector store
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    
    # 4. Convert to LangChain Documents
    docs = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        docs.append(Document(
            page_content=doc,
            metadata={**meta, "distance": dist}
        ))
    
    return docs
```

---

## Key Design Decisions

### 1. Privacy-First Architecture
- **Default**: Ollama (fully local, no data leaves network)
- **Fallback**: Azure OpenAI (enterprise privacy)
- **Optional**: OpenAI, Anthropic for flexibility

### 2. Chunking Strategy
- **Size**: 1200 characters (optimal for context window)
- **Overlap**: 150 characters (preserves context across chunks)
- **Splitter**: RecursiveCharacterTextSplitter (respects sentence boundaries)

### 3. Vector Store
- **Development**: ChromaDB (local, no setup required)
- **Production**: Can migrate to Pinecone (cloud scale)

### 4. Authentication
- **Confluence**: OAuth Bearer token (supports self-hosted)
- **Jira**: Basic Auth (email:token) with Bearer fallback

### 5. Incremental Ingestion
- **Test Mode**: `--limit N` for small samples
- **Full Mode**: No limit, ingests all configured sources

---

## Performance Characteristics

### Ingestion
- **Speed**: ~50 pages/second (depends on embedding model)
- **Chunking**: ~1-5 chunks per page (depends on content length)
- **Storage**: ~1-5 KB per chunk (text + metadata)

### Query
- **Latency**: 2-8 seconds (depends on LLM and query complexity)
- **Breakdown**:
  - Embedding query: ~100-500ms
  - Vector search: ~10-50ms
  - LLM generation: ~1-7 seconds
- **Throughput**: ~10-20 queries/minute (single instance)

### Scalability
- **Vector Store**: ChromaDB handles millions of vectors
- **API**: FastAPI supports async, can scale horizontally
- **LLM**: Ollama can run on GPU for faster inference

---

## Security Considerations

1. **API Tokens**: Stored in `.env` (not committed to git)
2. **Local Processing**: Default Ollama setup keeps data on-premise
3. **Authentication**: Supports OAuth for enterprise security
4. **Network**: All API calls use HTTPS
5. **Data Privacy**: No data sent to external services by default

---

## Future Enhancements

1. **Hybrid Search**: Combine vector search with BM25 (keyword search)
2. **Re-ranking**: Use cross-encoder to re-rank retrieved documents
3. **Caching**: Cache frequent queries
4. **Multi-modal**: Support images and attachments
5. **Fine-tuning**: Fine-tune LLM on domain-specific data
6. **Analytics**: Dashboard for query analytics
7. **User Feedback**: Thumbs up/down for answer quality

---

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check API tokens, try Bearer token auth
2. **Empty Answers**: Verify LLM is running (Ollama), check retrieved documents
3. **Slow Queries**: Consider GPU for Ollama, or use cloud LLM
4. **Missing Pages**: Check pagination logic, verify space keys exist
5. **Embedding Errors**: Ensure Ollama models are pulled (`ollama pull nomic-embed-text`)

---

## References

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Last Updated**: November 2024  
**Version**: 1.0.0

