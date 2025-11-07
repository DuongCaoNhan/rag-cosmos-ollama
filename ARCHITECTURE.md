# Project Architecture

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** application using local LLMs (via Ollama) and provides **two implementation options**:

1. **Simple/FAISS**: Lightweight, no external dependencies, perfect for development
2. **Cosmos DB**: Production-ready with Azure Cosmos DB for scalable vector storage

## Directory Structure

```
localRagComosDB/
├── simple/                    # FAISS-based implementation
│   ├── simple_load_data.py           # Load docs into FAISS
│   ├── simple_vector_search.py       # Search FAISS vector store
│   ├── simple_vector_store.py        # FAISS vector store setup
│   └── simple_rag_chain.py           # RAG chain with FAISS
│
├── cosmosdb/                  # Cosmos DB implementation
│   ├── cosmosdb_vector_store.py      # Cosmos DB connection & setup
│   ├── load_data.py                  # Load docs into Cosmos DB
│   ├── vector_search.py              # Search Cosmos DB
│   └── cosmos_rag_chain.py           # RAG chain with Cosmos DB
│
├── .github/
│   └── copilot-instructions.md       # AI assistant instructions
│
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Cosmos DB emulator configuration
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── SETUP.md                   # Setup instructions
└── ARCHITECTURE.md            # This file
```

## Data Flow

### Simple (FAISS) Implementation

```
┌─────────────────┐
│  Source URLs    │  Markdown documents from GitHub
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Load Data      │  simple_load_data.py
│  - Fetch docs   │  ├─ WebBaseLoader
│  - Chunk text   │  ├─ MarkdownTextSplitter
│  - Embed chunks │  └─ OllamaEmbeddings (mxbai-embed-large)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAISS Store    │  ./vector_store/index.faiss
│  (local file)   │  1024-dimension vectors
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Search  │  simple_vector_search.py
│  - Query embed  │  ├─ Similarity search (cosine)
│  - Top-K match  │  └─ Return scored results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG Chain      │  simple_rag_chain.py
│  - Retrieve ctx │  ├─ Get top-5 docs
│  - Build prompt │  ├─ Add context to question
│  - Generate ans │  └─ Ollama llama3 response
└─────────────────┘
```

### Cosmos DB Implementation

```
┌─────────────────┐
│  Source URLs    │  Markdown documents from GitHub
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Load Data      │  cosmosdb/load_data.py
│  - Fetch docs   │  ├─ WebBaseLoader
│  - Chunk text   │  ├─ MarkdownTextSplitter
│  - Embed chunks │  └─ OllamaEmbeddings (mxbai-embed-large)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cosmos DB      │  Azure Cosmos DB NoSQL
│  Emulator/Cloud │  ├─ Database: rag_local_llm_db
│                 │  ├─ Container: docs
│                 │  └─ Vector policy: 1024 dims, cosine
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Search  │  cosmosdb/vector_search.py
│  - Query embed  │  ├─ VectorDistance system function
│  - Top-K match  │  └─ Return scored results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG Chain      │  cosmosdb/cosmos_rag_chain.py
│  - Retrieve ctx │  ├─ Get top-5 docs from Cosmos
│  - Build prompt │  ├─ Add context to question
│  - Generate ans │  └─ Ollama llama3 response
└─────────────────┘
```

## Component Details

### Embedding Model
- **Model**: `mxbai-embed-large` (via Ollama)
- **Dimensions**: 1024
- **Purpose**: Convert text chunks into vector representations
- **Usage**: Both document embedding and query embedding

### Chat Model
- **Model**: `llama3:8b` (via Ollama)
- **Purpose**: Generate natural language responses
- **Input**: User question + retrieved context documents
- **Output**: Contextually-aware answer

### Document Processing
- **Loader**: LangChain `WebBaseLoader` (fetches markdown from URLs)
- **Splitter**: `MarkdownTextSplitter`
  - Chunk size: 1500 characters
  - Chunk overlap: 200 characters
  - Preserves markdown structure (headers, code blocks)
- **Metadata**: Source URL, chunk index

### Vector Stores

#### FAISS (Simple)
- **Storage**: Local file (`./vector_store/index.faiss`)
- **Index Type**: Flat (brute-force, 100% recall)
- **Similarity**: Cosine distance
- **Pros**: No external dependencies, fast setup
- **Cons**: Limited scalability, no cloud backup

#### Cosmos DB
- **Storage**: Azure Cosmos DB NoSQL container
- **Vector Policy**: 
  - Path: `/embedding`
  - Data type: `float32`
  - Dimensions: 1024
  - Distance function: `cosine`
- **Index Type**: `quantizedFlat` or `diskANN` (configurable)
- **Pros**: Scalable, cloud-native, production-ready
- **Cons**: Requires Docker emulator or Azure subscription

## Configuration

### Environment Variables
All configuration is centralized in `.env`:

```bash
# Cosmos DB
USE_EMULATOR=true                          # true = local, false = cloud
COSMOS_DB_URL=                             # Cloud connection string (if USE_EMULATOR=false)
DATABASE_NAME=rag_local_llm_db
CONTAINER_NAME=docs

# Ollama Models
EMBEDDINGS_MODEL=mxbai-embed-large
DIMENSIONS=1024
CHAT_MODEL=llama3

# RAG Parameters
TOP_K=5                                    # Number of context docs to retrieve
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
```

### Critical Windows Fix
**Problem**: Cosmos DB emulator advertises internal Docker IP (172.17.0.2), unreachable from Windows host.

**Solution**: Set environment variable in Docker:
```bash
AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1
```

This is already configured in `docker-compose.yml`.

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM Runtime** | Ollama | Local model serving (CPU/GPU) |
| **Embedding Model** | mxbai-embed-large | Text → 1024-dim vectors |
| **Chat Model** | llama3:8b | Natural language generation |
| **Vector DB (Simple)** | FAISS | In-memory/file-based vector search |
| **Vector DB (Prod)** | Azure Cosmos DB | Cloud-native vector database |
| **Orchestration** | LangChain | RAG pipeline, document loaders, chains |
| **Document Loader** | WebBaseLoader | Fetch markdown from URLs |
| **Text Splitter** | MarkdownTextSplitter | Chunk markdown intelligently |
| **Emulator** | Cosmos DB Linux Emulator | Local development (Docker) |

## Performance Considerations

### FAISS
- **Latency**: ~50ms for 26 chunks (test dataset)
- **Memory**: ~5MB for 26 chunks (scales linearly)
- **Best for**: <10,000 documents, single-machine deployment

### Cosmos DB
- **Latency**: ~100-200ms (includes network + disk I/O)
- **Memory**: Managed by Cosmos DB (emulator uses ~2GB RAM)
- **Best for**: >10,000 documents, distributed systems, production

### Chunking Strategy
- **Default**: 1500 chars with 200 overlap
- **Trade-offs**: 
  - Smaller chunks → more precise retrieval, less context per chunk
  - Larger chunks → more context, less precise retrieval
- **Recommendation**: Test with your data, adjust `CHUNK_SIZE` in `.env`

## Error Handling Patterns

### Connection Errors
```python
try:
    cosmos_client = CosmosClient(url, credential)
except Exception as e:
    if "172.17.0.2" in str(e):
        raise ConnectionError("Missing IP_ADDRESS_OVERRIDE env var")
```

### Model Availability
```python
# Check Ollama models
ollama_models = ["mxbai-embed-large", "llama3"]
for model in ollama_models:
    # Run: ollama list
    # If missing: ollama pull <model>
```

### SSL Certificates
```python
# For emulator, disable SSL verification
cosmos_client = CosmosClient(
    url, 
    credential, 
    connection_verify=False  # OK for local emulator
)
```

## Testing Strategy

### Unit Tests (Future)
- Mock Ollama embeddings
- Mock Cosmos DB operations
- Test chunking logic

### Integration Tests
1. Load small dataset (2 docs)
2. Verify vector count in store
3. Perform search, assert top result
4. Run RAG chain, verify response format

### Manual QA
```bash
# Simple version
python simple/simple_load_data.py
python simple/simple_vector_search.py "test query"
python simple/simple_rag_chain.py

# Cosmos version
docker-compose up -d
python cosmosdb/load_data.py
python cosmosdb/vector_search.py "test query"
python cosmosdb/cosmos_rag_chain.py
```

## Scaling Considerations

### Local Development
- Use `simple/` (FAISS) for quick iterations
- No need for Docker, cloud credentials

### Production Deployment
1. **Deploy Cosmos DB**: Create Azure Cosmos DB account (NoSQL API)
2. **Update `.env`**: Set `USE_EMULATOR=false`, add `COSMOS_DB_URL`
3. **Run migrations**: `python cosmosdb/load_data.py` with production URLs
4. **Containerize**: Build Docker image with `cosmosdb/cosmos_rag_chain.py`
5. **Monitor**: Use Azure Monitor for query performance, RU consumption

### Multi-Region
- Cosmos DB supports global distribution
- Configure read regions for low latency
- Write region for data ingestion

## Security Best Practices

1. **Never commit `.env`**: Already in `.gitignore`
2. **Use Managed Identity**: For Azure deployments, avoid connection strings
3. **Rotate Keys**: If using connection strings, rotate monthly
4. **Network Security**: Restrict Cosmos DB to VNet in production
5. **SSL/TLS**: Always use `connection_verify=True` in production

## References

- [Original Blog Post](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)
- [Azure Cosmos DB Vector Search](https://learn.microsoft.com/azure/cosmos-db/nosql/vector-search)
- [LangChain Cosmos DB Integration](https://python.langchain.com/docs/integrations/vectorstores/azurecosmosdb)
- [Ollama Documentation](https://ollama.com/)
- [FAISS Documentation](https://faiss.ai/)
