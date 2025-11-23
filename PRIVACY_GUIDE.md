# Privacy & Provider Guide

This guide explains how to use privacy-preserving AI providers to ensure your company data is not shared externally.

## Provider Options (Ranked by Privacy)

### 🏆 **1. Ollama (Fully Private - Recommended for Sensitive Data)**
- **Privacy**: ⭐⭐⭐⭐⭐ Data never leaves your network
- **Setup**: Requires local installation
- **Cost**: Free
- **Performance**: Good (depends on hardware)

**Setup:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3.2
ollama pull nomic-embed-text
```

**Configuration:**
```env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

---

### 🥈 **2. Azure OpenAI (Enterprise Privacy)**
- **Privacy**: ⭐⭐⭐⭐ Data NOT used for training (enterprise agreement)
- **Setup**: Requires Azure subscription
- **Cost**: Pay-per-use
- **Performance**: Excellent

**Benefits:**
- Enterprise-grade data protection
- Data residency options
- Compliance certifications (SOC 2, ISO 27001)
- Data NOT used to train models

**Configuration:**
```env
LLM_PROVIDER=azure_openai
EMBEDDING_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

---

### 🥉 **3. Anthropic Claude (Privacy-Focused)**
- **Privacy**: ⭐⭐⭐⭐ Data NOT used for training
- **Setup**: Simple API key
- **Cost**: Pay-per-use
- **Performance**: Excellent

**Benefits:**
- Explicit privacy policy (data not used for training)
- Strong security practices
- Good for sensitive enterprise data

**Configuration:**
```env
LLM_PROVIDER=anthropic
EMBEDDING_PROVIDER=openai  # Anthropic doesn't have embeddings, use OpenAI or local
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

---

### ⚠️ **4. OpenAI (Default - Less Private)**
- **Privacy**: ⭐⭐ Data may be used for training (unless you opt out)
- **Setup**: Simple API key
- **Cost**: Pay-per-use
- **Performance**: Excellent

**Note**: OpenAI may use your data for training unless you have a Business/Enterprise agreement with data opt-out.

**Configuration:**
```env
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

---

### 🔒 **5. Local Embeddings (Fully Private)**
- **Privacy**: ⭐⭐⭐⭐⭐ Data never leaves your machine
- **Setup**: Requires sentence-transformers
- **Cost**: Free
- **Performance**: Good (CPU-based)

**Configuration:**
```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## Recommended Configurations

### For Maximum Privacy (Sensitive Company Data)
```env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
# OR
EMBEDDING_PROVIDER=local
```

### For Enterprise (Balance of Privacy & Performance)
```env
LLM_PROVIDER=azure_openai
EMBEDDING_PROVIDER=azure_openai
```

### For Privacy-Conscious (Good Balance)
```env
LLM_PROVIDER=anthropic
EMBEDDING_PROVIDER=local
```

---

## Quick Setup Examples

### Option 1: Ollama (Fully Private)
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull models
ollama pull llama3.2
ollama pull nomic-embed-text

# 3. Update .env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
```

### Option 2: Azure OpenAI (Enterprise)
```bash
# 1. Get Azure OpenAI credentials from Azure Portal
# 2. Update .env
LLM_PROVIDER=azure_openai
EMBEDDING_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
```

### Option 3: Hybrid (Anthropic + Local Embeddings)
```bash
# 1. Get Anthropic API key
# 2. Update .env
LLM_PROVIDER=anthropic
EMBEDDING_PROVIDER=local
ANTHROPIC_API_KEY=your-key
```

---

## Data Privacy Comparison

| Provider | Data Used for Training | Data Leaves Network | Enterprise Agreement Available |
|----------|----------------------|---------------------|-------------------------------|
| Ollama | ❌ No | ❌ No | N/A (self-hosted) |
| Azure OpenAI | ❌ No* | ✅ Yes (Azure) | ✅ Yes |
| Anthropic | ❌ No | ✅ Yes (Anthropic) | ✅ Yes |
| OpenAI | ⚠️ Yes* | ✅ Yes | ✅ Yes (opt-out) |
| Local | ❌ No | ❌ No | N/A |

*With proper enterprise agreement and data opt-out

---

## Testing Your Configuration

After setting up your provider, test it:

```bash
# Start the API
uvicorn app.main:app --reload

# Test with curl
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"q": "test query"}'
```

Check the logs to confirm which provider is being used.

---

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` matches your Ollama instance

### Azure OpenAI Error
- Verify endpoint format: `https://your-resource.openai.azure.com`
- Check deployment names match your Azure deployments
- Ensure API version is correct

### Local Embeddings Slow
- First run downloads the model (one-time)
- Consider using GPU if available
- Use smaller models for faster inference

---

## Need Help?

- Check provider-specific documentation
- Review error messages in application logs
- Test with `/health` endpoint to verify configuration

