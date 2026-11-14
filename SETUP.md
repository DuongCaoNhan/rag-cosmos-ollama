# Setup Guide

## Complete Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd localRagComosDB
```

### 2. Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install and Setup Ollama

#### Windows / Mac / Linux
1. Download from https://ollama.com/
2. Install and start Ollama
3. Pull required models:

```bash
ollama pull mxbai-embed-large
ollama pull llama3
```

Verify:
```bash
ollama list
```

### 4. Setup Environment Variables

Copy the example file:
```bash
cp .env.example .env
```

The `.env` file is already configured with defaults that work for the emulator.

### 5. Choose Your Implementation

> **Tip:** Set `CHAT_MODEL` to any chat model you have pulled. If Ollama reports
> `cudaMalloc failed: out of memory`, lower `NUM_CTX` (default `4096`).

#### Option A: Simple (FAISS) - No Docker Required

```bash
# Load data (builds ./vector_store)
python simple/simple_load_data.py

# Test search
python simple/simple_vector_search.py "What is vector search?"

# Run interactive chat
python simple/simple_rag_chain.py
```

#### Option B: Cosmos DB - Docker Required

**On Windows, the script does everything:**
```powershell
./run_cosmos.ps1 -LoadData   # first run: start emulator, wait until ready, load data, test
./run_cosmos.ps1             # later runs (do not reload, it would duplicate the documents)
```

**Or step by step:**

**Step 1: Start Cosmos DB Emulator**

Using Docker Compose (recommended):
```bash
docker compose up -d
```

Or using Docker directly:
```bash
docker run \
    --publish 8081:8081 \
    --publish 10250-10255:10250-10255 \
    --name cosmos-emulator \
    --env AZURE_COSMOS_EMULATOR_PARTITION_COUNT=1 \
    --env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1 \
    --detach \
    mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest
```

**Step 2: Wait for the emulator to start (can take a few minutes on the first start)**

It is ready when this returns the certificate:
```bash
curl -k https://127.0.0.1:8081/_explorer/emulator.pem
```

**Step 3: Run the application**

```bash
# Load data (once; creates the database and the container)
python cosmosdb/load_data.py

# Test search
python cosmosdb/vector_search.py "vector embedding policy"

# Run interactive chat
python cosmosdb/cosmos_rag_chain.py
```

## Troubleshooting

### Cosmos DB Connection Timeout

**Error:**
```
Connection to 172.17.0.2 timed out
```

**Fix:**
Make sure you started the emulator with:
```
--env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1
```

This is already included in `docker-compose.yml`.

### Ollama Not Found

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Import Errors

Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### Certificate Errors

The code automatically handles self-signed certificates with `connection_verify=False`. No manual certificate installation needed!

### Ollama Out of Memory

`cudaMalloc failed: out of memory` means the chat model plus its context does not fit in VRAM. Lower `NUM_CTX` in `.env` or use a smaller `CHAT_MODEL`.

### Port Already in Use / `WinError 10013`

Windows (Hyper-V/WSL) can reserve port ranges. Check with `netsh int ipv4 show excludedportrange protocol=tcp` and pick another port (for example `streamlit run app.py --server.port 9501`).

## User Interfaces

All three UIs can switch between FAISS and Cosmos DB:

```bash
python server.py        # WebUI + REST API -> http://localhost:8000
python app_gradio.py    # Gradio           -> http://localhost:7860
streamlit run app.py    # Streamlit        -> http://localhost:8501
```

## Next Steps

- Read `README.md` for detailed documentation
- Explore the code in `simple/` for FAISS implementation
- Explore the code in `cosmosdb/` for Cosmos DB implementation
- Customize the data sources (`doc_urls`) in the `load_data.py` files
- Adjust RAG parameters in `.env` file

## Quick Reference

### Environment Variables
```bash
USE_EMULATOR=true              # Use local emulator vs cloud
DATABASE_NAME=rag_local_llm_db # Database name
CONTAINER_NAME=docs            # Container name
EMBEDDINGS_MODEL=mxbai-embed-large  # Ollama embedding model
DIMENSIONS=1024                # Vector dimensions
CHAT_MODEL=llama3              # Ollama chat model
NUM_CTX=4096                   # Chat model context window (VRAM usage)
TOP_K=5                        # Number of context docs to retrieve
# COSMOS_DB_URL=https://<account>.documents.azure.com:443/  # cloud only (USE_EMULATOR=false)
```

### Docker Commands
```bash
# Start emulator
docker compose up -d

# Stop emulator (removes the container and its data)
docker compose down

# View logs
docker logs cosmos-emulator

# Access Cosmos DB Explorer
# Open in browser: https://localhost:8081/_explorer/index.html
```

### Project Commands
```bash
# Simple version
python simple/simple_load_data.py
python simple/simple_vector_search.py "your query"
python simple/simple_rag_chain.py

# Cosmos DB version
python cosmosdb/load_data.py
python cosmosdb/vector_search.py "your query"
python cosmosdb/cosmos_rag_chain.py
```