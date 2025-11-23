# Ingestion Guide - Incremental & Full

This guide shows you how to ingest data incrementally (for testing) or all at once.

## 🧪 Step 1: Test with Small Sample (Recommended First!)

Start with a small test to make sure everything works:

```bash
# Test with just 5 pages and 5 issues
python ingest_test.py
```

This will:
- Ingest 5 Confluence pages
- Ingest 5 Jira issues
- Perfect for testing the system works

## 📝 Step 2: Ingest Confluence Only (Incremental)

### Test with a few pages:
```bash
# Ingest 10 Confluence pages
python ingest_confluence_only.py --limit 10
```

### Ingest specific space:
```bash
# Ingest all pages from PROD space
python ingest_confluence_only.py --space PROD
```

### Ingest all Confluence pages:
```bash
# No limit = ingest everything
python ingest_confluence_only.py
```

## 🎫 Step 3: Ingest Jira Only (Incremental)

### Test with a few issues:
```bash
# Ingest 10 Jira issues
python ingest_jira_only.py --limit 10
```

### Ingest all Jira issues:
```bash
# No limit = ingest everything
python ingest_jira_only.py
```

## 🚀 Step 4: Full Ingestion (When Ready)

Once you've tested and everything works:

```bash
# Ingest everything (all Confluence + all Jira)
python ingest_all.py
```

## 📊 Recommended Workflow

1. **First time setup:**
   ```bash
   python ingest_test.py          # Test with 5 pages + 5 issues
   ```

2. **Test queries:**
   ```bash
   uvicorn app.main:app --reload  # Start API
   # Test some queries to make sure it works
   ```

3. **Scale up gradually:**
   ```bash
   python ingest_confluence_only.py --limit 50    # 50 pages
   python ingest_jira_only.py --limit 50         # 50 issues
   # Test again
   ```

4. **Full ingestion:**
   ```bash
   python ingest_all.py  # Everything!
   ```

## 🔄 Re-running Ingestion

The system uses **upsert** - it will update existing documents and add new ones. Safe to run multiple times!

```bash
# Re-run anytime to get latest updates
python ingest_confluence_only.py
python ingest_jira_only.py
```

## 📋 All Available Commands

| Command | What it does | Use case |
|---------|-------------|----------|
| `python ingest_test.py` | 5 pages + 5 issues | Initial testing |
| `python ingest_confluence_only.py --limit 10` | 10 Confluence pages | Test Confluence |
| `python ingest_confluence_only.py` | All Confluence pages | Full Confluence |
| `python ingest_jira_only.py --limit 10` | 10 Jira issues | Test Jira |
| `python ingest_jira_only.py` | All Jira issues | Full Jira |
| `python ingest_all.py` | Everything | Full ingestion |

## 💡 Tips

- **Start small**: Always test with `--limit` first
- **Monitor progress**: Watch the console output
- **Check vector store**: After ingestion, check `/health` endpoint
- **Incremental is safe**: Can run ingestion multiple times
- **Ollama speed**: Embeddings may take time with Ollama (local processing)

## ⚠️ Notes

- First ingestion creates the vector database
- Subsequent runs update/add new documents
- Large datasets may take time (especially with local Ollama)
- Monitor disk space (ChromaDB stores locally)


