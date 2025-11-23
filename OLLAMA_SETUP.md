# Ollama Setup Guide (Fully Private)

This guide will help you set up Ollama for fully private AI that runs locally - your data **never leaves your network**.

## Why Ollama?

- 🔒 **100% Private** - All processing happens on your machine
- 💰 **Free** - No API costs
- 🚀 **Fast** - Runs locally, no network latency
- 🛡️ **Secure** - Company data stays on your infrastructure

## Quick Setup

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

**Or use our setup script:**
```bash
./setup_ollama.sh
```

### Step 2: Download Required Models

```bash
# LLM model for generating answers
ollama pull llama3.2

# Embedding model for vector search
ollama pull nomic-embed-text
```

This will download ~4GB for llama3.2 and ~274MB for nomic-embed-text.

### Step 3: Start Ollama Server

```bash
# Start Ollama (keep this running)
ollama serve
```

Or run in background:
```bash
ollama serve &
```

### Step 4: Configure Your .env File

Create or update your `.env` file:

```env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

### Step 5: Test the Setup

```bash
# Test Ollama is working
ollama run llama3.2 "Hello, how are you?"

# Test the API
uvicorn app.main:app --reload

# In another terminal, test the endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"q": "test query"}'
```

## Model Options

### LLM Models (for generating answers)

| Model | Size | Quality | Speed | Recommended For |
|-------|------|---------|-------|----------------|
| llama3.2 | ~2GB | Good | Fast | General use (default) |
| llama3.1:8b | ~4.7GB | Better | Medium | Better quality |
| mistral | ~4.1GB | Good | Fast | Fast responses |
| codellama | ~3.8GB | Good | Medium | Code-focused |

**To use a different model:**
```bash
ollama pull llama3.1:8b
# Then update .env: OLLAMA_LLM_MODEL=llama3.1:8b
```

### Embedding Models (for vector search)

| Model | Size | Dimensions | Quality |
|-------|------|------------|---------|
| nomic-embed-text | ~274MB | 768 | Good (default) |
| all-minilm | ~23MB | 384 | Fast, smaller |

**To use a different embedding model:**
```bash
ollama pull all-minilm
# Then update .env: OLLAMA_EMBEDDING_MODEL=all-minilm
```

## System Requirements

### Minimum
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space
- **CPU**: Modern multi-core processor

### Recommended
- **RAM**: 16GB+
- **Storage**: 20GB+ free space
- **GPU**: Optional but recommended for faster inference

## Troubleshooting

### "Connection refused" error

**Problem**: Ollama server is not running

**Solution**:
```bash
# Start Ollama
ollama serve

# Or check if it's running
curl http://localhost:11434/api/tags
```

### "Model not found" error

**Problem**: Model hasn't been downloaded

**Solution**:
```bash
# Pull the required models
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Slow performance

**Solutions**:
1. Use smaller models (e.g., `llama3.2` instead of `llama3.1:8b`)
2. Ensure Ollama is using GPU (if available)
3. Close other resource-intensive applications
4. Consider using a more powerful machine

### Out of memory errors

**Solutions**:
1. Use smaller models
2. Reduce chunk size in `ingest/common.py`
3. Close other applications
4. Add more RAM

## Running Ollama in Production

### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/ollama.service`:
```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=your-user
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

### Option 2: Docker

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Option 3: Background Process

```bash
nohup ollama serve > ollama.log 2>&1 &
```

## Performance Tips

1. **Use GPU** (if available):
   - Ollama automatically uses GPU if CUDA/Metal is available
   - Check: `ollama ps` should show GPU usage

2. **Optimize chunk size**:
   - Smaller chunks = faster embeddings
   - Edit `ingest/common.py` to adjust `chunk_size`

3. **Batch processing**:
   - Ingestion already batches documents
   - Consider running ingestion during off-hours

## Next Steps

1. ✅ Install Ollama
2. ✅ Download models
3. ✅ Configure .env
4. ✅ Start Ollama server
5. ✅ Run ingestion: `python ingest_all.py`
6. ✅ Start API: `uvicorn app.main:app --reload`
7. ✅ Test queries!

## Need Help?

- Ollama docs: https://ollama.ai/docs
- Check logs: `tail -f ollama.log`
- Test connection: `curl http://localhost:11434/api/tags`
- List models: `ollama list`

