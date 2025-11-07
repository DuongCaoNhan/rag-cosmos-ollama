# AI Agent Instructions for Local RAG + Cosmos DB

This is a **Retrieval-Augmented Generation (RAG) application** using local LLMs via Ollama, LangChain, with **two implementation options**: FAISS (simple, no dependencies) and Azure Cosmos DB (production-ready).

## Architecture Overview

**Two Implementations:**
1. **Simple (FAISS)**: Lightweight, file-based vector store - perfect for development and testing
2. **Cosmos DB**: Production-ready Azure Cosmos DB NoSQL with vector search capabilities

**Data Flow:**
1. **Data Loading**: Fetch markdown docs → chunk → embed with `mxbai-embed-large` → store in vector database
2. **Vector Search**: Query → embed → similarity search → return top-k results
3. **RAG Chain**: User question → retrieve context → feed to `llama3` → generate response

**Key Components:**
- **Ollama**: Local LLM runtime (embedding model: `mxbai-embed-large` 1024-dim; chat model: `llama3:8b`)
- **Vector Stores**: FAISS (simple/) or Azure Cosmos DB (cosmosdb/) 
- **LangChain**: Orchestration framework (vectorstores, chains, document loaders, embedding wrappers)

**Environment Variables** (see `.env.example`):
- `USE_EMULATOR="true"` or `COSMOS_DB_URL` (cloud connection string)
- `DATABASE_NAME="rag_local_llm_db"`, `CONTAINER_NAME="docs"`
- `EMBEDDINGS_MODEL="mxbai-embed-large"`, `DIMENSIONS="1024"`
- `CHAT_MODEL="llama3"`, `TOP_K=5` (context results to retrieve)
- `CHUNK_SIZE=1500`, `CHUNK_OVERLAP=200`

## File Structure

```
localRagComosDB/
├── simple/                          # FAISS implementation (no Docker required)
│   ├── simple_load_data.py         # Load docs into FAISS
│   ├── simple_vector_search.py     # Test FAISS search
│   ├── simple_vector_store.py      # FAISS setup
│   └── simple_rag_chain.py         # Interactive RAG with FAISS
├── cosmosdb/                        # Cosmos DB implementation
│   ├── cosmosdb_vector_store.py    # Cosmos DB connection
│   ├── load_data.py                # Load docs into Cosmos DB
│   ├── vector_search.py            # Test Cosmos DB search
│   └── cosmos_rag_chain.py         # Interactive RAG with Cosmos DB
├── .github/
│   └── copilot-instructions.md     # This file
├── .env.example                     # Environment template
├── docker-compose.yml               # Cosmos DB emulator with Windows fix
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── SETUP.md                         # Setup guide
├── ARCHITECTURE.md                  # System architecture
├── CHANGELOG.md                     # Version history
└── QUICK_REFERENCE.md               # Command cheatsheet
```

## Key Patterns & Workflows

### 1. **Data Loading Workflow**
- **Input**: Markdown URLs (fetch from GitHub raw content)
- **Processing**: 
  - Split into chunks (default 1500 chars with 200 overlap via `MarkdownTextSplitter`)
  - Generate embeddings using Ollama `mxbai-embed-large` (1024 dimensions)
  - Add metadata (source URL, chunk index)
- **Output**: Documents stored in vector database with embeddings
- **Commands**: 
  - FAISS: `python simple/simple_load_data.py`
  - Cosmos DB: `python cosmosdb/load_data.py`

### 2. **Vector Search Pattern**
- Uses LangChain's vector store implementations:
  - FAISS: `FAISS.from_documents()` - brute-force similarity search
  - Cosmos DB: `AzureCosmosDBNoSqlVectorSearch` - handles embedding internally
- Query is embedded on-the-fly with same model as documents
- Similarity search returns top-k documents sorted by score (higher = better match)
- Pattern: Query embedding → cosine similarity → rank results
- **Commands**:
  - FAISS: `python simple/simple_vector_search.py "your query"`
  - Cosmos DB: `python cosmosdb/vector_search.py "your query"`

### 3. **RAG Chain Flow**
- `retriever`: Vector search returning top-k docs (default: 5)
- `prompt_template`: System message + retrieved docs + user query
- `llm`: Ollama `llama3` model (local inference)
- `chain`: LangChain Runnable (retriever | prompt | llm | output_parser)
- Interactive commands: `exit` (quit), `clear` (reset history), `history` (view past exchanges)
- **Commands**:
  - FAISS: `python simple/simple_rag_chain.py`
  - Cosmos DB: `python cosmosdb/cosmos_rag_chain.py`

### 4. **Error Handling Conventions**
- Cosmos DB connection: Trap `ConnectionError`, check emulator running or credentials
- **Windows Cosmos DB Fix**: Must set `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1` (already in docker-compose.yml)
- Ollama not available: Check `ollama serve` is running, models exist via `ollama list`
- SSL cert issues (emulator): Handled with `connection_verify=False` for local dev
- Out-of-memory: Reduce `TOP_K` or use smaller chunks
- Import errors: All Python files use `sys.path.insert(0, os.path.dirname(__file__))` for subfolder execution

## Development Workflows

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

# Install Ollama models
ollama pull mxbai-embed-large
ollama pull llama3

# Copy environment template
cp .env.example .env
```

### Run Services (Cosmos DB only)
```bash
# Start Cosmos DB emulator with Docker Compose (includes Windows fix)
docker-compose up -d

# Wait ~60 seconds for emulator initialization
docker logs cosmos-emulator

# Access Cosmos DB Explorer: https://localhost:8081/_explorer/index.html
```

### Typical Developer Loop

**Simple/FAISS Version (No Docker)**
```bash
1. python simple/simple_load_data.py
2. python simple/simple_vector_search.py "your query"
3. python simple/simple_rag_chain.py
```

**Cosmos DB Version**
```bash
1. docker-compose up -d
2. python cosmosdb/load_data.py
3. python cosmosdb/vector_search.py "your query"
4. python cosmosdb/cosmos_rag_chain.py
```

## Implementation Priorities

- **High**: Core RAG chain must work end-to-end (retriever → embedding → LLM response)
- **High**: Both FAISS and Cosmos DB implementations must remain in sync
- **Medium**: Proper error messages, graceful degradation if services unavailable
- **Medium**: Configurable chunking strategy (chunk size, overlap, separator types)
- **Low**: UI polish, performance optimization (batching, caching)

## Testing Strategy

- **Manual testing**: Interactive chat to verify response quality
- **Simple version**: Use FAISS for rapid iteration without Docker dependencies
- **Production testing**: Test with Cosmos DB emulator before cloud deployment
- **Data validation**: Verify chunk count, embedding dimensions match configuration

## Common Pitfalls

1. **Dimension mismatch**: Embedding model output dims must match Cosmos DB schema (1024 for `mxbai-embed-large`)
2. **Chunking fragmentation**: Too-small chunks lose context; too-large chunks waste space. Tune via `CHUNK_SIZE` and `CHUNK_OVERLAP`
3. **Stale embeddings**: Always re-embed after updating chunk strategy or model version
4. **Connection timeouts**: Emulator requires `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1` on Windows
5. **Import errors**: Files in subfolders use `sys.path.insert(0, os.path.dirname(__file__))` to enable execution from project root

## References
- Original blog post: https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/
- LangChain Cosmos DB integration: https://python.langchain.com/docs/integrations/vectorstores/azurecosmosdb
- Ollama documentation: https://ollama.com/
