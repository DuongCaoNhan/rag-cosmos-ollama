# Quick Reference

## 🚀 Quick Start Commands

### Setup (One-time)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ollama models
ollama pull mxbai-embed-large
ollama pull llama3

# Copy environment template
cp .env.example .env
```

### Run Simple Version (No Docker)
```bash
# 1. Load data into FAISS
python simple/simple_load_data.py

# 2. Test search
python simple/simple_vector_search.py "What is vector search?"

# 3. Interactive chat
python simple/simple_rag_chain.py
```

### Run Cosmos DB Version (Requires Docker)
```bash
# 1. Start Cosmos DB emulator
docker-compose up -d

# 2. Wait ~60 seconds for initialization
docker logs cosmos-emulator

# 3. Load data
python cosmosdb/load_data.py

# 4. Test search
python cosmosdb/vector_search.py "vector embedding policy"

# 5. Interactive chat
python cosmosdb/cosmos_rag_chain.py
```

## 📁 File Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `simple/simple_load_data.py` | Load docs into FAISS | First run, after adding new URLs |
| `simple/simple_vector_search.py` | Test FAISS search | Debug retrieval quality |
| `simple/simple_rag_chain.py` | Interactive chat (FAISS) | Development, testing |
| `cosmosdb/load_data.py` | Load docs into Cosmos DB | First run, data refresh |
| `cosmosdb/vector_search.py` | Test Cosmos DB search | Debug retrieval, verify indexing |
| `cosmosdb/cosmos_rag_chain.py` | Interactive chat (Cosmos DB) | Production-like testing |
| `.env` | Configuration | Change models, chunk size, top-K |

## 🔧 Common Tasks

### Change Data Source
**File**: `simple/simple_load_data.py` or `cosmosdb/load_data.py`
```python
# Add/modify URLs
urls = [
    "https://raw.githubusercontent.com/.../your-doc1.md",
    "https://raw.githubusercontent.com/.../your-doc2.md",
]
```

### Adjust Chunk Size
**File**: `.env`
```bash
CHUNK_SIZE=1500      # Characters per chunk
CHUNK_OVERLAP=200    # Overlap between chunks
```

### Change Retrieval Count
**File**: `.env`
```bash
TOP_K=5  # Number of context documents (default: 5)
```

### Switch Models
**File**: `.env`
```bash
EMBEDDINGS_MODEL=mxbai-embed-large  # Or: nomic-embed-text
CHAT_MODEL=llama3                   # Or: llama3.1, mistral
```

Don't forget to pull new models:
```bash
ollama pull nomic-embed-text
ollama pull llama3.1
```

### Check Ollama Status
```bash
# List installed models
ollama list

# Test embedding model
ollama run mxbai-embed-large "test"

# Test chat model
ollama run llama3 "hello"
```

### Manage Docker Emulator
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker logs -f cosmos-emulator

# Access web UI
# https://localhost:8081/_explorer/index.html
```

## 🐛 Troubleshooting Quick Fixes

### "Connection timeout to 172.17.0.2"
```bash
# Fix: Make sure docker-compose.yml has:
# AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1
docker-compose down
docker-compose up -d
```

### "Ollama not found"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running:
ollama serve
```

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "SSL certificate verify failed"
```python
# Already handled in code with:
# connection_verify=False (for emulator only)
```

### "Vector store not found"
```bash
# Run load_data.py first
python simple/simple_load_data.py
# or
python cosmosdb/load_data.py
```

## 💡 RAG Chat Commands

### In Interactive Chat
```
> Your question here        # Ask a question
> exit                       # Quit the program
> clear                      # Clear conversation history
> history                    # Show conversation history
```

## 📊 Performance Tips

### FAISS (Simple)
- **Best for**: <10,000 documents
- **Memory**: ~5MB per 1,000 chunks
- **Latency**: ~50ms for searches

### Cosmos DB
- **Best for**: >10,000 documents, production
- **RU consumption**: ~5-10 RUs per search
- **Latency**: ~100-200ms (includes network)

### Chunking Guidelines
| Document Type | Chunk Size | Overlap |
|---------------|------------|---------|
| Technical docs | 1500 | 200 |
| Chat/FAQ | 500 | 50 |
| Long articles | 2000 | 300 |

## 🔐 Security Checklist

- [ ] `.env` file in `.gitignore` (✅ already configured)
- [ ] No hardcoded credentials in code
- [ ] Use `connection_verify=True` in production
- [ ] Rotate Cosmos DB keys monthly (cloud)
- [ ] Use Managed Identity in Azure (cloud)

## 📚 Documentation Index

| Document | Focus |
|----------|-------|
| `README.md` | Overview, quickstart, Windows fix |
| `SETUP.md` | Detailed setup instructions |
| `ARCHITECTURE.md` | System design, data flow, components |
| `CHANGELOG.md` | Version history, roadmap |
| `QUICK_REFERENCE.md` | This file - commands, tips |

## 🌐 Useful URLs

- **Cosmos DB Explorer**: https://localhost:8081/_explorer/index.html
- **Ollama API**: http://localhost:11434/api/tags
- **Original Tutorial**: https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/

## 🎯 Workflow Examples

### Development Loop
```bash
# 1. Edit data source
code simple/simple_load_data.py

# 2. Reload data
python simple/simple_load_data.py

# 3. Test retrieval
python simple/simple_vector_search.py "your test query"

# 4. Interactive testing
python simple/simple_rag_chain.py
```

### Production Deployment Prep
```bash
# 1. Test with emulator
docker-compose up -d
python cosmosdb/load_data.py
python cosmosdb/cosmos_rag_chain.py

# 2. Update .env for cloud
USE_EMULATOR=false
COSMOS_DB_URL=https://your-account.documents.azure.com:443/

# 3. Run migration
python cosmosdb/load_data.py

# 4. Verify
python cosmosdb/vector_search.py "test query"
```

## ⚙️ Environment Variable Reference

```bash
# Cosmos DB
USE_EMULATOR=true                    # true=local, false=cloud
COSMOS_DB_URL=                       # Cloud connection string
DATABASE_NAME=rag_local_llm_db       # Database name
CONTAINER_NAME=docs                  # Container name

# Ollama
EMBEDDINGS_MODEL=mxbai-embed-large   # Embedding model
DIMENSIONS=1024                      # Vector dimensions
CHAT_MODEL=llama3                    # Chat model

# RAG
TOP_K=5                              # Context documents
CHUNK_SIZE=1500                      # Characters per chunk
CHUNK_OVERLAP=200                    # Chunk overlap
```

## 🔄 Data Refresh

### When to Reload Data
- Added new document URLs
- Changed chunk size/overlap
- Switched embedding model
- Corrupted vector store

### How to Reload
```bash
# FAISS
rm -rf vector_store/              # Delete old index
python simple/simple_load_data.py # Rebuild

# Cosmos DB
# Delete container in Explorer UI, or:
docker-compose down               # Reset emulator
docker-compose up -d
python cosmosdb/load_data.py      # Reload
```

---

**Pro Tips**:
- Start with `simple/` for development
- Use `cosmosdb/` for production-like testing
- Monitor Docker memory usage (emulator uses ~2GB)
- Keep conversation context under 5 exchanges for best results
- Adjust `TOP_K` based on your data density
