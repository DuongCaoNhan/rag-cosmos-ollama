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

#### Option A: Simple (FAISS) - No Docker Required

```bash
# Load data
python simple/simple_load_data.py

# Test search
python simple/simple_vector_search.py "What is vector search?"

# Run interactive chat
python simple/simple_rag_chain.py
```

#### Option B: Cosmos DB - Docker Required

**Step 1: Start Cosmos DB Emulator**

Using Docker Compose (recommended):
```bash
docker-compose up -d
```

Or using Docker directly:
```bash
docker run \
    --publish 8081:8081 \
    --publish 10250-10255:10250-10255 \
    --name cosmos-emulator \
    --env AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 \
    --env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1 \
    --detach \
    mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest
```

**Step 2: Wait for emulator to start (60-90 seconds)**

Check status:
```bash
docker logs cosmos-emulator
```

Look for: "Started"

**Step 3: Run the application**

```bash
# Load data
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

## Next Steps

- Read `README.md` for detailed documentation
- Explore the code in `simple/` for FAISS implementation
- Explore the code in `cosmosdb/` for Cosmos DB implementation
- Customize the data sources in `load_data.py` files
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
TOP_K=5                        # Number of context docs to retrieve
```

### Docker Commands
```bash
# Start emulator
docker-compose up -d

# Stop emulator
docker-compose down

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