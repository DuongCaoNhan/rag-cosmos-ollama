# Local RAG with Ollama and Azure Cosmos DB

> **🎓 Educational project.** Inspired by the Microsoft DevBlogs tutorial
> [Build a RAG application with LangChain and local LLMs powered by Ollama](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/).

A **Retrieval-Augmented Generation (RAG)** application that runs entirely on your machine:

- **Local LLMs** via [Ollama](https://ollama.com/) for both embeddings and chat
- **Two vector stores**: FAISS (local files, no Docker) and Azure Cosmos DB for NoSQL (emulator or cloud)
- **Three UIs** that can switch between both stores: a WebUI (FastAPI), Gradio and Streamlit
- **CLI scripts** for loading data, testing vector search and chatting

The knowledge base is the Azure Cosmos DB vector search documentation on Microsoft Learn.

## How it works

```
Loading:  Microsoft Learn pages → WebBaseLoader → MarkdownTextSplitter (1500 chars)
          → Ollama embeddings (mxbai-embed-large, 1024 dims) → FAISS or Cosmos DB

Query:    Question → embedding → top-K similar chunks → prompt (context + question)
          → Ollama chat model → answer + source chunks
```

## Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.com/)**, running (`ollama serve` or the desktop app)
- **Docker Desktop**, only for the Cosmos DB emulator
- **PowerShell 7** (`pwsh`), to run the `run_*.ps1` scripts on Windows
- A GPU with about 8 GB VRAM is enough for a 7B/8B chat model with `NUM_CTX=4096`

## Quick start

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pull the models
ollama pull mxbai-embed-large      # embeddings (required)
ollama pull llama3                 # chat model, or set CHAT_MODEL to a model you already have

# 3. Configure
cp .env.example .env               # defaults work for a local setup
```

### FAISS version (no Docker)

```powershell
python simple/simple_load_data.py  # builds ./vector_store (only needed once)
./run_faiss.ps1                    # vector search test + interactive chat
```

### Cosmos DB version (emulator)

```powershell
./run_cosmos.ps1 -LoadData         # first run: starts the emulator, creates the container, loads documents
./run_cosmos.ps1                   # later runs: the data is already in the emulator
```

`run_cosmos.ps1` starts the emulator with `docker compose up -d` and waits until it answers on `https://127.0.0.1:8081`. The first start can take a few minutes. Use `-LoadData` only once, because running it again inserts the documents a second time.

To run both versions in one go, use `./run_test.ps1` (or `run_test.bat`).

### User interfaces

Each UI has a selector to switch between **FAISS** and **Cosmos DB**.

| UI | Command | URL |
|---|---|---|
| WebUI + REST API (FastAPI) | `python server.py` | http://localhost:8000 |
| Gradio | `python app_gradio.py` | http://localhost:7860 |
| Streamlit | `streamlit run app.py` | http://localhost:8501 |

The FastAPI server also exposes the API used by the WebUI:

```powershell
curl -X POST http://localhost:8000/init -H "Content-Type: application/json" -d '{"vector_store":"Cosmos DB","top_k":5}'
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query":"What vector index types are available?"}'
curl http://localhost:8000/health
```

## CLI scripts

All scripts read `.env` and are run from the repository root.

| Purpose | FAISS | Cosmos DB |
|---|---|---|
| Load documents | `python simple/simple_load_data.py` | `python cosmosdb/load_data.py` |
| Vector search | `python simple/simple_vector_search.py "query" [top_k]` | `python cosmosdb/vector_search.py "query" [top_k]` |
| Interactive chat | `python simple/simple_rag_chain.py` | `python cosmosdb/cosmos_rag_chain.py` |

In the chat: `exit` quits, `clear` clears the history, `history` shows past exchanges.

Example questions:
- What vector index types are available in Cosmos DB?
- Show me an example of a vector embedding policy
- How does multitenancy work for vector search?

## Configuration

Settings live in `.env` (template: [.env.example](.env.example)).

| Variable | Default | Description |
|---|---|---|
| `USE_EMULATOR` | `true` | Use the local Cosmos DB emulator; `false` uses a cloud account |
| `COSMOS_DB_URL` | none | Cloud account endpoint, required when `USE_EMULATOR=false` |
| `DATABASE_NAME` | `rag_local_llm_db` | Cosmos DB database |
| `CONTAINER_NAME` | `docs` | Cosmos DB container |
| `EMBEDDINGS_MODEL` | `mxbai-embed-large` | Ollama embedding model |
| `DIMENSIONS` | `1024` | Embedding dimensions; must match the embedding model |
| `CHAT_MODEL` | `llama3` | Ollama chat model |
| `NUM_CTX` | `4096` | Context window for the chat model; lower it if the GPU runs out of memory |
| `TOP_K` | `5` | Number of chunks retrieved per question |

> If you change `EMBEDDINGS_MODEL`, rebuild the stores: run `simple/simple_load_data.py`, and recreate the Cosmos DB container before running `cosmosdb/load_data.py`.

## Project structure

```
localRagComosDB/
├── simple/                     # FAISS version
│   ├── simple_vector_store.py  # FAISS store (create / load ./vector_store)
│   ├── simple_load_data.py
│   ├── simple_vector_search.py
│   └── simple_rag_chain.py
├── cosmosdb/                   # Cosmos DB version
│   ├── cosmosdb_vector_store.py  # client, vector embedding + indexing policies
│   ├── load_data.py
│   ├── vector_search.py
│   └── cosmos_rag_chain.py
├── webui/                      # Static WebUI served by server.py
├── server.py                   # FastAPI: /init, /chat, /health + WebUI
├── app_gradio.py               # Gradio UI
├── app.py                      # Streamlit UI
├── prompts.py                  # Shared prompt template
├── run_faiss.ps1 / run_cosmos.ps1 / run_test.ps1 / run_test.bat
├── docker-compose.yml          # Cosmos DB Linux emulator
├── vector_store/               # Saved FAISS index
├── .env.example
└── requirements.txt
```

## Troubleshooting

**`Connection to 172.17.0.2 timed out` (Windows + emulator).**
The emulator advertises its internal Docker IP, which Windows cannot reach. `docker-compose.yml` already sets `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1` to fix this. If you start the emulator with `docker run`, add `--env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1`.

**`Connection refused` / `Connection aborted` when using Cosmos DB.**
The emulator is not running or not ready yet. Run `./run_cosmos.ps1`, or check `docker logs cosmos-emulator`.

**Cosmos DB search returns nothing or the container is missing.**
The data has not been loaded. Run `./run_cosmos.ps1 -LoadData` once.

**Certificate errors.**
The emulator uses a self-signed certificate. The code connects with `connection_verify=False`, so you do not need to import the certificate.

**`cudaMalloc failed: out of memory` from Ollama.**
The chat model and its context do not fit in VRAM. Lower `NUM_CTX` in `.env` (for example `2048`) or use a smaller `CHAT_MODEL`.

**`WinError 10013` when starting a UI.**
Windows (Hyper-V/WSL) can reserve port ranges. Check with `netsh int ipv4 show excludedportrange protocol=tcp`, then use another port, for example `streamlit run app.py --server.port 9501`.

**`Missing required environment variables`.**
Create `.env` from `.env.example` and run the scripts from the repository root.

## Using Azure Cosmos DB in the cloud

1. Create an Azure Cosmos DB for NoSQL account and [enable vector search](https://learn.microsoft.com/azure/cosmos-db/vector-search).
2. Give your identity a data-plane role on the account (for example *Cosmos DB Built-in Data Contributor*). The code authenticates with `DefaultAzureCredential`, so `az login` is enough locally.
3. Update `.env`:

   ```
   USE_EMULATOR=false
   COSMOS_DB_URL=https://<account-name>.documents.azure.com:443/
   ```

The same code works for the emulator and the cloud.

## References

- [Original tutorial (Microsoft DevBlogs)](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)
- [Original sample repository](https://github.com/abhirockzz/local-llms-rag-cosmosdb)
- [Vector search in Azure Cosmos DB for NoSQL](https://learn.microsoft.com/azure/cosmos-db/vector-search)
- [Azure Cosmos DB emulator](https://learn.microsoft.com/azure/cosmos-db/emulator)
- [Ollama](https://ollama.com/)

## Attribution & license

This project is inspired by and extends the Microsoft DevBlogs tutorial above (© Microsoft Corporation). It adds:
- a FAISS version that needs no Docker;
- a fix for the emulator's networking on Windows Docker Desktop;
- three UIs that can switch between both vector stores.

Licensed under the MIT License. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
