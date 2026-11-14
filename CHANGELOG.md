# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-11-14

### Added
- **Three UIs**, each able to switch between FAISS and Cosmos DB:
  - WebUI + REST API (`server.py`, `webui/`): `POST /init`, `POST /chat`, `GET /health`
  - Gradio (`app_gradio.py`)
  - Streamlit (`app.py`)
- **Windows scripts**: `run_faiss.ps1`, `run_cosmos.ps1 [-LoadData]`, `run_test.ps1`, `run_test.bat`
- **`NUM_CTX`** setting (default 4096) so a 7B/8B chat model fits in 8GB VRAM

### Fixed
- `requirements.txt` was corrupted (interleaved lines) and missed `langchain-azure-ai`, `azure-identity`, `gradio`, `fastapi`, `uvicorn`
- Selecting Cosmos DB in any UI failed with an import error (`get_vector_store` did not exist in `cosmosdb_vector_store.py`)
- Cosmos DB ignored the Top-K setting (its retriever reads `k`, not `search_kwargs["k"]`)
- Gradio always initialized FAISS, whatever store was selected
- Streamlit ignored changes of store, model and Top-K (cached on underscore-prefixed arguments) and could not retry after a failed initialization
- CLI scripts now load `.env`; the run scripts no longer override it with hard-coded values
- `run_cosmos.ps1` no longer deletes the emulator on every run, waits until the emulator is ready instead of sleeping 60 seconds, and can load the data (`-LoadData`)
- Source documents moved: the raw GitHub markdown URLs return 404, so the loaders now read the Microsoft Learn pages (article body only)
- Emulator uses 1 partition (faster start)
- README rewritten (it was corrupted); docs updated

## [1.0.0] - 2025-11-07

### Initial Release

#### Features
- ✅ **Two implementation options**: FAISS (simple) and Cosmos DB (production)
- ✅ **Local LLM support**: Ollama integration (mxbai-embed-large, llama3)
- ✅ **RAG pipeline**: Complete retrieval-augmented generation workflow
- ✅ **Vector search**: Similarity search with configurable top-K
- ✅ **Interactive chat**: Command-line interface with conversation history
- ✅ **Document loading**: Support for markdown URLs with intelligent chunking
- ✅ **Windows support**: Working Cosmos DB emulator with Docker Desktop

#### Components

**Simple Implementation (FAISS)**
- `simple/simple_load_data.py` - Load documents into FAISS vector store
- `simple/simple_vector_search.py` - Perform vector similarity search
- `simple/simple_vector_store.py` - FAISS vector store initialization
- `simple/simple_rag_chain.py` - Interactive RAG chat interface

**Cosmos DB Implementation**
- `cosmosdb/cosmosdb_vector_store.py` - Azure Cosmos DB connection & setup
- `cosmosdb/load_data.py` - Load documents into Cosmos DB
- `cosmosdb/vector_search.py` - Vector search with Cosmos DB
- `cosmosdb/cosmos_rag_chain.py` - RAG chain with Cosmos DB backend

**Infrastructure**
- `docker-compose.yml` - Cosmos DB emulator with Windows fix
- `.env.example` - Configuration template
- `requirements.txt` - Python dependencies

**Documentation**
- `README.md` - Main documentation with quickstart
- `SETUP.md` - Detailed setup instructions
- `ARCHITECTURE.md` - System architecture and design decisions
- `.github/copilot-instructions.md` - AI assistant context

#### Fixed Issues

🐛 **Windows Cosmos DB Emulator Connection**
- **Problem**: Connection timeout to internal Docker IP (172.17.0.2:8081)
- **Root Cause**: Windows Docker Desktop networking limitation
- **Solution**: Set `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1` environment variable
- **Impact**: Enables Cosmos DB emulator on Windows without WSL2 workarounds
- **References**: Included in `docker-compose.yml` and documented in README

🔧 **SSL Certificate Handling**
- **Problem**: Self-signed certificate errors with emulator
- **Solution**: Use `connection_verify=False` for local development
- **Note**: Production code should use `connection_verify=True`

#### Configuration

**Default Settings**
```bash
DATABASE_NAME=rag_local_llm_db
CONTAINER_NAME=docs
EMBEDDINGS_MODEL=mxbai-embed-large
DIMENSIONS=1024
CHAT_MODEL=llama3
TOP_K=5
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
```

#### Dependencies

**Core**
- `langchain` - RAG orchestration
- `langchain-ollama` - Ollama integration
- `langchain-community` - Document loaders
- `langchain-azure-ai` - Cosmos DB integration (optional)
- `azure-cosmos` - Azure Cosmos SDK (optional)
- `faiss-cpu` - Vector search (simple version)

**Development**
- `python-dotenv` - Environment configuration
- `urllib3` - HTTP client

#### Testing

**Manual Test Results**
- ✅ FAISS data loading (26 chunks from 2 documents)
- ✅ FAISS vector search (top-5 results with scores)
- ✅ FAISS RAG chain (interactive chat)
- ✅ Cosmos DB data loading (26 chunks)
- ✅ Cosmos DB vector search (top-5 results)
- ✅ Cosmos DB RAG chain (interactive chat)

#### Known Limitations

1. **Emulator Initialization**: Requires ~60 seconds to fully start (10 partitions)
2. **Minimum Vectors**: `quantizedFlat` and `diskANN` indexes need ≥1000 vectors for optimal performance
3. **Dimension Limit**: `flat` index limited to 505 dimensions (not applicable with 1024-dim embeddings)
4. **Memory Usage**: Ollama models require ~4-8GB RAM

#### Migration Notes

**From Hybrid Approach**
- Removed hybrid vector store implementation
- Simplified to two clean implementations (simple vs cosmosdb)
- Updated imports to work with subfolder structure

**Project Structure Changes**
```
Before:
├── hybrid_*.py
├── test_*.py
├── simple_*.py
├── cosmosdb_*.py
└── (various other files)

After:
├── simple/
│   ├── simple_*.py
├── cosmosdb/
│   ├── *.py
├── README.md
├── SETUP.md
└── ARCHITECTURE.md
```

#### References

- Original Tutorial: [Microsoft DevBlogs - RAG with LangChain + Ollama + Cosmos DB](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)
- Azure Cosmos DB: [Vector Search Documentation](https://learn.microsoft.com/azure/cosmos-db/nosql/vector-search)
- LangChain: [Cosmos DB Integration](https://python.langchain.com/docs/integrations/vectorstores/azurecosmosdb)
- Ollama: [Official Documentation](https://ollama.com/)

---

## Future Roadmap

### Version 1.1 (Planned)
- [ ] Unit tests with pytest
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Performance benchmarks (FAISS vs Cosmos DB)
- [ ] Docker image for RAG service
- [x] REST API wrapper (FastAPI), done in 1.1.0

### Version 1.2 (Planned)
- [ ] Multi-document support (PDFs, DOCX)
- [ ] Custom data source connectors
- [ ] Query caching
- [ ] Response streaming
- [ ] Conversation persistence

### Version 2.0 (Ideas)
- [ ] Multi-agent orchestration
- [ ] Tool calling (function calling)
- [ ] Hybrid search (keyword + vector)
- [ ] Re-ranking models
- [x] Web UI (Streamlit/Gradio), done in 1.1.0

---

**Contributors**: Development team following [Microsoft DevBlogs tutorial](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)

**License**: MIT (see [LICENSE](LICENSE) and [NOTICE](NOTICE))
