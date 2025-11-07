# RAG Application with Ollama and Cosmos DB# Local RAG with Ollama and Azure Cosmos DB# Build a RAG application with LangChain and Local LLMs powered by Ollama# RAG App với Local LLM# Local RAG Application with LangChain and Ollama



> **🎓 Educational Project** | Inspired by [Microsoft DevBlogs Tutorial](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)



A complete **Retrieval-Augmented Generation (RAG)** application using local LLMs powered by Ollama, with support for both **FAISS** (simple, local) and **Azure Cosmos DB** (production-ready) vector stores.Complete **Retrieval-Augmented Generation (RAG)** application using local LLMs powered by Ollama, with support for both **FAISS** (simple, local) and **Azure Cosmos DB** (production-ready) vector stores.



## ⚖️ Attribution & License



This project is inspired by and extends the Microsoft DevBlogs tutorial on building RAG applications with LangChain and Ollama. ## 🚀 Quick Start> **... and Azure Cosmos DB as the Vector Database**



**Original Tutorial**: [Build a RAG application with LangChain and local LLMs powered by Ollama](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)  

**Copyright**: Microsoft Corporation

### Prerequisites

**Our Enhancements**:

- ✅ Added FAISS implementation as lightweight alternative- [Ollama](https://ollama.com/) installed and running

- ✅ Fixed Windows Docker Desktop networking issues

- ✅ Created comprehensive documentation suite- Python 3.8+This is the sample code for a blog post illustrates how to use local LLMs with [Azure Cosmos DB as a vector database](https://learn.microsoft.com/en-us/azure/cosmos-db/gen-ai/why-cosmos-ai) for retrieval-augmented generation (RAG) scenarios. It will guide you through setting up a local LLM solution, configuring Azure Cosmos DB, loading data, performing vector searches, and executing RAG queries.Ứng dụng RAG đơn giản sử dụng Ollama và in-memory vector store.A complete **Retrieval-Augmented Generation (RAG)** application using local LLMs powered by Ollama, LangChain, and Azure Cosmos DB as a vector database.

- ✅ Organized code into clean project structure

- ✅ Enhanced error handling and configuration management- Docker Desktop (for Cosmos DB emulator)



**License**: MIT (see [LICENSE](LICENSE) and [NOTICE](NOTICE) files)



---### 1. Install Dependencies



## 🚀 Quick Start```bashFor a step-by-step guide, check out the full blog post on [devblogs.microsoft.com](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama). By the end of it, you will have a working local RAG setup that leverages Ollama and Azure Cosmos DB. The sample app uses [LangChain integration with Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/gen-ai/integrations?context=%2Fazure%2Fcosmos-db%2Fnosql%2Fcontext%2Fcontext) to perform embedding, data loading, and vector search. You can easily adapt it to other frameworks like LlamaIndex.



### Prerequisitespip install -r requirements.txt

- [Ollama](https://ollama.com/) installed and running

- Python 3.8+```

- Docker Desktop (for Cosmos DB emulator)



### 1. Install Dependencies

```bash### 2. Setup Ollama ModelsYou can either use the [Azure Cosmos DB emulator](https://learn.microsoft.com/en-us/azure/cosmos-db/emulator) for local development or connecting to an Azure Cosmos DB account in the cloud. You will be using Ollama (open-source solution) to run LLMs locally on your own machine. It lets you download, run, and interact with a variety of LLMs (like Llama 3, Mistral, and others) using simple commands, without needing cloud access or complex setup.## Cài đặt## Features

pip install -r requirements.txt

``````bash



### 2. Setup Ollama Modelsollama pull mxbai-embed-large

```bash

ollama pull mxbai-embed-largeollama pull llama3

ollama pull llama3

``````## Quick Start



### 3. Configure Environment

```bash

cp .env.example .env### 3. Configure Environment

# Edit .env with your configuration

``````bash



---cp .env.example .env### 1. Install Dependencies```bash✨ **Local-First**: Run entirely on your infrastructure with no cloud dependencies  



## 📁 Project Structure# Edit .env with your configuration



``````

localRagComosDB/

├── simple/              # FAISS-based RAG (no external dependencies)

│   ├── simple_vector_store.py

│   ├── simple_load_data.py## 📁 Project Structure```bashpip install langchain-ollama langchain-community langchain-text-splitters requests beautifulsoup4 numpy🚀 **Fast Setup**: Quick installation and configuration  

│   ├── simple_vector_search.py

│   └── simple_rag_chain.py

│

├── cosmosdb/           # Cosmos DB-based RAG (production-ready)```pip install -r requirements.txt

│   ├── cosmosdb_vector_store.py

│   ├── load_data.py.

│   ├── vector_search.py

│   └── cosmos_rag_chain.py├── simple/              # FAISS-based RAG (no external dependencies)``````🔐 **Data Privacy**: Sensitive information stays on your machine  

│

├── .env.example        # Environment configuration template│   ├── simple_vector_store.py

├── docker-compose.yml  # Cosmos DB emulator setup

├── requirements.txt    # Python dependencies│   ├── simple_load_data.py

├── LICENSE            # MIT License with attribution

├── NOTICE             # Third-party attributions│   ├── simple_vector_search.py

├── README.md          # This file

├── SETUP.md           # Detailed setup instructions│   └── simple_rag_chain.py### 2. Start Services🧠 **Flexible Models**: Support for multiple Ollama models  

├── ARCHITECTURE.md    # System architecture

├── CHANGELOG.md       # Version history│

└── QUICK_REFERENCE.md # Command cheatsheet

```├── cosmosdb/           # Cosmos DB-based RAG (production-ready)



---│   ├── cosmosdb_vector_store.py



## 🎯 Two Implementation Options│   ├── load_data.py**Terminal 1 - Ollama:**## Chạy📚 **Document Retrieval**: Intelligent semantic search over knowledge bases  



### Option 1: Simple (FAISS) - Quick Start ⚡│   ├── vector_search.py



Perfect for development, testing, and learning. **No Docker required!**│   └── cosmos_rag_chain.py```bash



```bash│

# Load data

python simple/simple_load_data.py├── .env                # Environment configurationollama serve💬 **Interactive Chat**: Conversational interface with chat history  



# Test search├── requirements.txt    # Python dependencies

python simple/simple_vector_search.py "What is vector search?"

└── docker-compose.yml  # Cosmos DB emulator setup```

# Run RAG chat

python simple/simple_rag_chain.py```

```

1. Khởi động Ollama:

**Pros:**

- ✅ Zero setup - works immediately## 🎯 Two Implementations

- ✅ No external dependencies

- ✅ Fast for development**Terminal 2 - Cosmos DB Emulator:**

- ✅ Portable (works on any OS)

### Option 1: Simple (FAISS) - Quick Start ⚡

**Cons:**

- ❌ Data stored in memory/files only```bash```bash## Architecture

- ❌ Not suitable for production

- ❌ Limited scalabilityPerfect for development, testing, and learning. No Docker required!



---docker run --publish 8081:8081 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest



### Option 2: Cosmos DB - Production Ready 🏢```bash



Enterprise-grade vector database with persistence and scalability.# Set environment variables```ollama serve



#### Step 1: Start Cosmos DB Emulatorexport EMBEDDINGS_MODEL="mxbai-embed-large"



**Using Docker Compose (Recommended):**export CHAT_MODEL="llama3"

```bash

docker-compose up -d

```

# Load data### 3. Download Models``````

**Or manual Docker run:**

```bashpython simple/simple_load_data.py

docker run \

    --publish 8081:8081 \

    --publish 10250-10255:10250-10255 \

    --name cosmos-emulator \# Test search

    --env AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 \

    --env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1 \python simple/simple_vector_search.py "What is vector search?"```bashUser Query

    --detach \

    mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest

```

# Run RAG chatollama pull mxbai-embed-large

> **⚠️ CRITICAL for Windows:** The `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1` environment variable is **required** to fix Docker networking issues on Windows. Without this, you'll get connection timeout errors.

python simple/simple_rag_chain.py

#### Step 2: Wait for Emulator to Start

```bash```ollama pull llama32. Tải models cần thiết:    ↓

# Wait ~60 seconds, then verify

docker logs cosmos-emulator

# Should see: "Started"

```**Pros:**```



#### Step 3: Run the Application- ✅ Zero setup - works immediately

```bash

# Load data into Cosmos DB- ✅ No external dependencies```bash[Ollama Embeddings] → Generate query vector

python cosmosdb/load_data.py

- ✅ Fast for development

# Test vector search

python cosmosdb/vector_search.py "vector embedding policy"- ✅ Portable (works on any OS)### 4. Set Environment Variables



# Run interactive RAG chat

python cosmosdb/cosmos_rag_chain.py

```**Cons:**ollama pull mxbai-embed-large    ↓



**Pros:**- ❌ Data stored in memory/files only

- ✅ Production-ready database

- ✅ Data persistence across restarts- ❌ Not suitable for productionSet the following environment variables (or create a `.env` file):

- ✅ Scalable to cloud (same code works with Azure Cosmos DB)

- ✅ Enterprise features (indexing policies, partitioning, etc.)- ❌ Limited scalability



**Cons:**ollama pull llama3[Vector Search] → Find similar chunks in Cosmos DB

- ❌ Requires Docker

- ❌ More complex setup---

- ❌ Windows requires special configuration

```bash

---

### Option 2: Cosmos DB - Production Ready 🏢

## 🐛 Troubleshooting

# Use the emulator```    ↓

### Windows + Cosmos DB Emulator Issues

Enterprise-grade vector database with persistence and scalability.

If you see errors like:

```export USE_EMULATOR=true

Connection to 172.17.0.2 timed out

```#### Step 1: Start Cosmos DB Emulator



**Solution:** Make sure you start the emulator with the IP override:export DATABASE_NAME=rag_local_llm_db[RAG Chain] → Feed context + query to llama3

```bash

--env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1**Using Docker Compose (Recommended):**

```

```bashexport CONTAINER_NAME=docs

This tells the emulator to advertise `127.0.0.1` instead of the internal Docker IP, fixing Windows networking issues.

docker-compose up -d

### Ollama Not Responding

```export EMBEDDINGS_MODEL=mxbai-embed-large3. Tải dữ liệu:    ↓

```bash

# Restart Ollama

ollama serve

**Or manual Docker run:**export EMBEDDING_DIMENSIONS=1024

# Verify models are installed

ollama list```bash

```

docker run \export CHAT_MODEL=llama3```bash[LLM Response] → Return answer

### Certificate Errors

    --publish 8081:8081 \

The emulator uses self-signed certificates. The code handles this automatically with `connection_verify=False`.

    --publish 10250-10255:10250-10255 \export TOP_K=5

---

    --name cosmos-emulator \

## 🔧 Configuration

    --env AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 \```python load_data.py```

### Environment Variables

    --env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1 \

Create a `.env` file:

    --detach \

```bash

# Vector Store Selection    mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest

USE_EMULATOR=true              # Use Cosmos DB emulator (false = cloud)

```### 5. Load Data```

# Database Configuration

DATABASE_NAME=rag_local_llm_db

CONTAINER_NAME=docs

> **⚠️ CRITICAL for Windows:** The `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1` environment variable is **required** to fix Docker networking issues on Windows. Without this, you'll get connection timeout errors.

# Ollama Models

EMBEDDINGS_MODEL=mxbai-embed-large

DIMENSIONS=1024

CHAT_MODEL=llama3#### Step 2: Wait for Emulator to Start```bash## Prerequisites



# RAG Settings```bash

TOP_K=5

# Wait ~60 seconds, then verifypython load_data.py

# Cloud Cosmos DB (optional - only if USE_EMULATOR=false)

# COSMOS_DB_URL=your-cosmos-db-connection-stringdocker logs cosmos-emulator

```

```4. Chat:

---

# Should see: "Started"

## 🚢 Production Deployment

```

To use Azure Cosmos DB in the cloud:



1. Create an Azure Cosmos DB for NoSQL account

2. Enable vector search feature#### Step 3: Run the Application### 6. Test Vector Search```bash- **Python 3.9+**

3. Update `.env`:

```bash```bash

USE_EMULATOR=false

COSMOS_DB_URL="AccountEndpoint=https://your-account.documents.azure.com:443/;AccountKey=your-key;"# Set environment variables (or use .env file)

```

export USE_EMULATOR="true"

Same code works for both emulator and cloud! 🎉

export DATABASE_NAME="rag_local_llm_db"```bashpython chat.py- **Ollama** (https://ollama.com) with models:

---

export CONTAINER_NAME="docs"

## 📚 How It Works

export EMBEDDINGS_MODEL="mxbai-embed-large"python vector_search.py "How does vector search work in Cosmos DB?"

### Data Flow

export DIMENSIONS="1024"

```

1. Documents (URLs) → WebBaseLoaderexport CHAT_MODEL="llama3"``````  - `mxbai-embed-large` (embedding model, 1024 dimensions)

2. Raw text → MarkdownTextSplitter → Chunks

3. Chunks → Ollama Embeddings → Vectors (1024-dim)

4. Vectors → Vector Store (FAISS or Cosmos DB)

```# Load data into Cosmos DB  - `llama3:8b` (chat model)



### RAG Query Flowpython cosmosdb/load_data.py



```### 7. Run Interactive Chat- **Docker** (for Cosmos DB emulator) or **Azure Cosmos DB** cloud account

1. User Question → Ollama Embeddings → Query Vector

2. Query Vector → Vector Store → Top-K Similar Documents# Test vector search

3. Documents + Question → LLM Prompt → Ollama (llama3)

4. Ollama → Generated Answerpython cosmosdb/vector_search.py "vector embedding policy"- 8GB+ RAM (more for larger models on GPU)

```



---

# Run interactive RAG chat```bash

## 🎓 Learning Resources

python cosmosdb/cosmos_rag_chain.py

- 📖 [Original Tutorial: RAG with LangChain + Ollama + Cosmos DB](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)

- 📚 [Azure Cosmos DB Vector Search](https://learn.microsoft.com/azure/cosmos-db/nosql/vector-search)```python rag_chain.py## Quick Start

- 🦙 [Ollama Documentation](https://ollama.com/)

- 🔗 [LangChain Cosmos DB Integration](https://python.langchain.com/docs/integrations/vectorstores/azurecosmosdb)



---**Pros:**```



## 📝 Key Features- ✅ Production-ready database



✨ **Local-First**: Run entirely on your infrastructure with no cloud dependencies  - ✅ Data persistence across restarts### 1. Install Dependencies

🚀 **Fast Setup**: Quick installation and configuration  

🔐 **Data Privacy**: Sensitive information stays on your machine  - ✅ Scalable to cloud (same code works with Azure Cosmos DB)

🧠 **Flexible Models**: Support for multiple Ollama models  

📚 **Document Retrieval**: Intelligent semantic search over knowledge bases  - ✅ Enterprise features (indexing policies, partitioning, etc.)## Files

💬 **Interactive Chat**: Conversational interface with chat history  



---

**Cons:**```bash

## 🤝 Contributing

- ❌ Requires Docker

Contributions welcome! Please:

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design- ❌ More complex setup- `cosmosdb_vector_store.py` - Azure Cosmos DB vector store setup# Create virtual environment

- Follow existing code patterns

- Add tests for new features- ❌ Windows requires special configuration

- Update documentation

- `load_data.py` - Load documents from web into vector storepython -m venv .venv

---

## 🐛 Troubleshooting

## 📄 License

- `vector_search.py` - Test vector similarity searchsource .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

MIT License - see [LICENSE](LICENSE) file for details.

### Windows + Cosmos DB Emulator Issues

This project includes third-party attributions - see [NOTICE](NOTICE) file.

- `rag_chain.py` - Interactive RAG chat application

---

If you see errors like:

## 🆘 Support

```- `requirements.txt` - Python dependencies# Install packages

- 📖 **Documentation**: See [SETUP.md](SETUP.md) for detailed instructions

- 📖 **Quick Reference**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commandsConnection to 172.17.0.2 timed out

- 🐛 **Issues**: Open a GitHub issue

- 💡 **Discussions**: Use GitHub Discussions```- `.env` - Environment configurationpip install -r requirements.txt



---



**Built with ❤️ using Ollama, LangChain, and Azure Cosmos DB****Solution:** Make sure you start the emulator with the IP override:```


```bash

--env AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1## Environment Variables

```

### 2. Start Services

This tells the emulator to advertise `127.0.0.1` instead of the internal Docker IP, fixing Windows networking issues.

| Variable | Description | Default |

### Ollama Not Responding

```bash|----------|-------------|---------|**Terminal 1 - Ollama:**

# Restart Ollama

ollama serve| `USE_EMULATOR` | Use local emulator instead of cloud | `true` |```bash



# Verify models are installed| `DATABASE_NAME` | Cosmos DB database name | `rag_local_llm_db` |ollama serve

ollama list

```| `CONTAINER_NAME` | Cosmos DB container name | `docs` |```



### Certificate Errors| `EMBEDDINGS_MODEL` | Ollama embedding model | `mxbai-embed-large` |

The emulator uses self-signed certificates. The code handles this automatically with `connection_verify=False`.

| `EMBEDDING_DIMENSIONS` | Embedding vector dimensions | `1024` |**Terminal 2 - Cosmos DB (Docker):**

## 🔧 Configuration

| `CHAT_MODEL` | Ollama chat model | `llama3` |```bash

### Environment Variables

| `TOP_K` | Number of search results | `5` |docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest

Create a `.env` file:

| `COSMOS_DB_URL` | Cloud Cosmos DB URL (if not using emulator) | - |

```bash

# Vector Store Selection## ✅ Working Simple Version (Recommended)

USE_EMULATOR=true              # Use Cosmos DB emulator (false = cloud Cosmos DB)

The simple version uses FAISS in-memory vector store and is ready to run:

# Database Configuration

DATABASE_NAME=rag_local_llm_db### Quick Setup:

CONTAINER_NAME=docs```powershell

# 1. Install dependencies

# Ollama Modelspip install -r requirements.txt

EMBEDDINGS_MODEL=mxbai-embed-largepip install faiss-cpu

DIMENSIONS=1024

CHAT_MODEL=llama3# 2. Start Ollama (separate terminal)

ollama serve

# RAG Settings

TOP_K=5# 3. Download models

ollama pull mxbai-embed-large

# Cloud Cosmos DB (optional - only if USE_EMULATOR=false)ollama pull llama3

# COSMOS_DB_URL=your-cosmos-db-connection-string

```# 4. Set environment and run

$env:EMBEDDINGS_MODEL="mxbai-embed-large"; $env:CHAT_MODEL="llama3"; $env:TOP_K="5"

## 🚢 Production Deployment

# 5. Load data

To use Azure Cosmos DB in the cloud:python simple_load_data.py



1. Create an Azure Cosmos DB for NoSQL account# 6. Test search

2. Enable vector search featurepython simple_vector_search.py "What is vector search in Cosmos DB?"

3. Update `.env`:

```bash# 7. Run chat

USE_EMULATOR=falsepython simple_rag_chain.py

COSMOS_DB_URL="AccountEndpoint=https://your-account.documents.azure.com:443/;AccountKey=your-key;"```

```

### Simple Files:

Same code works for both emulator and cloud! 🎉- `simple_load_data.py` - Loads documents into FAISS vector store

- `simple_vector_search.py` - Tests vector similarity search

## 📚 How It Works- `simple_rag_chain.py` - Interactive chat with RAG

- `simple_vector_store.py` - FAISS vector store wrapper

### Data Flow

```### Example Chat:

1. Documents (URLs) → WebBaseLoader```

2. Raw text → MarkdownTextSplitter → Chunks[User]: What is vector search in Cosmos DB?

3. Chunks → Ollama Embeddings → Vectors (1024-dim)[Assistant]: Vector search in Azure Cosmos DB for NoSQL is a feature that enables efficient and accurate vector indexing and search. It allows you to store vectors directly in documents alongside your data, enabling efficient and high-accuracy multi-modal vector search at any scale...

4. Vectors → Vector Store (FAISS or Cosmos DB)```docker run --publish 8081:8081 -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=1 \

```  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest

```

### RAG Query Flow

```### 3. Configure Environment

1. User Question → Ollama Embeddings → Query Vector

2. Query Vector → Vector Store → Top-K Similar Documents```bash

3. Documents + Question → LLM Prompt → Ollama (llama3)# Copy template

4. Ollama → Generated Answercp config/.env.example config/.env

```

# Edit config/.env if needed (defaults work for local setup)

## 🎓 Learning Resources```



- [Microsoft Blog: RAG with LangChain + Ollama + Cosmos DB](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)### 4. Pull Models

- [Original Repository](https://github.com/abhirockzz/local-llms-rag-cosmosdb)

- [Azure Cosmos DB Vector Search](https://learn.microsoft.com/azure/cosmos-db/nosql/vector-search)```bash

- [Ollama Documentation](https://ollama.com/)ollama pull mxbai-embed-large

ollama pull llama3:8b

## 📝 Key Learnings```



### Why Two Versions?### 5. Load Data



**Simple (FAISS):**```bash

- Learning and developmentpython scripts/load_data.py

- Quick prototyping```

- Testing RAG concepts

- No infrastructure neededOutput:

```

**Cosmos DB:**Uploading documents to Azure Cosmos DB

- Production applicationsUsing database: rag_local_llm_db, container: docs

- Data persistence requiredUsing embedding model: mxbai-embed-large with dimensions: 1024

- Scalability neededLoading 26 document chunks from 2 documents

- Enterprise features (security, monitoring, etc.)Data loaded into Azure Cosmos DB

```

### Windows Docker Networking Fix

### 6. Test Vector Search

The key discovery: Cosmos DB emulator in Docker on Windows has networking issues where the SDK tries to connect to the internal Docker IP (`172.17.0.2`) which is not accessible from the Windows host.

```bash

**Solution:** `AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1`python scripts/vector_search.py "show me an example of a vector embedding policy"

```

This environment variable tells the emulator to advertise `127.0.0.1` (accessible from Windows) instead of its internal IP, allowing the Azure Cosmos SDK to connect properly.

### 7. Run Interactive Chat

## 🤝 Contributing

```bash

Feel free to open issues or submit PRs!python scripts/rag_chain.py

```

## 📄 License

Commands in chat:

MIT- `exit` - Quit application

- `clear` - Clear chat history

---- `history` - View past exchanges



**Built with ❤️ using Ollama, LangChain, and Azure Cosmos DB**Example questions:
- "What is the maximum supported dimension for vector embeddings?"
- "Is it suitable for large scale data?"
- "What are the benefits of flat index type?"

## Project Structure

```
localRagComosDB/
├── .github/
│   └── copilot-instructions.md    # AI agent guidelines
├── src/
│   ├── config.py                  # Configuration loader
│   ├── embeddings.py              # Ollama embeddings wrapper
│   ├── vector_store.py            # Cosmos DB vector search
│   └── chains.py                  # RAG chain orchestration
├── scripts/
│   ├── load_data.py               # Data loading pipeline
│   ├── vector_search.py           # Vector search tester
│   └── rag_chain.py               # Interactive chat interface
├── config/
│   └── .env.example               # Environment template
├── tests/
│   └── test_components.py         # Unit tests
├── docs/
│   └── SETUP.md                   # Detailed setup guide
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Configuration

Edit `config/.env` to customize:

| Variable | Default | Purpose |
|----------|---------|---------|
| `USE_EMULATOR` | true | Use local Cosmos DB emulator |
| `COSMOS_DB_URL` | localhost:8081 | Cosmos DB endpoint |
| `DATABASE_NAME` | rag_local_llm_db | Database name |
| `CONTAINER_NAME` | docs | Container name |
| `EMBEDDINGS_MODEL` | mxbai-embed-large | Embedding model |
| `DIMENSIONS` | 1024 | Embedding vector dimensions |
| `CHAT_MODEL` | llama3 | Chat/generation model |
| `TOP_K` | 5 | Number of search results |
| `CHUNK_SIZE` | 1000 | Document chunk size |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |

## Common Issues

### SSL Certificate Error (Emulator)

**Linux:**
```bash
curl --insecure https://localhost:8081/_explorer/emulator.pem > ~/emulatorcert.crt
sudo update-ca-certificates
```

**macOS:**
```bash
curl --insecure https://localhost:8081/_explorer/emulator.pem > ~/emulatorcert.pem
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/emulatorcert.pem
```

**Windows:** Import certificate via Certificate Manager

### Ollama Not Responding

```bash
# Check Ollama is running
ollama list

# Restart Ollama service
ollama serve
```

### Out of Memory

Reduce `TOP_K` or use smaller model:
```bash
ollama pull mistral  # Smaller than llama3
export CHAT_MODEL=mistral
```

## Testing

```bash
# Run unit tests
pytest tests/

# With coverage
pytest tests/ --cov=src
```

## Performance Tips

- **GPU Acceleration**: Ensure Ollama uses GPU (faster inference)
- **Batch Loading**: Load multiple documents at once
- **Chunking**: Tune `CHUNK_SIZE` and `CHUNK_OVERLAP` based on your docs
- **Vector Cache**: Consider caching embeddings for repeated queries

## Cloud Deployment

To use Azure Cosmos DB cloud instead of emulator:

1. Create account: https://portal.azure.com
2. Enable vector search: https://learn.microsoft.com/azure/cosmos-db/nosql/vector-search
3. Set environment:
```bash
export USE_EMULATOR=false
export COSMOS_DB_URL="https://<account>.documents.azure.com:443/"
az login  # Use DefaultAzureCredential
```

## References

- 📖 [Microsoft Blog: RAG with LangChain + Ollama + Cosmos DB](https://devblogs.microsoft.com/cosmosdb/build-a-rag-application-with-langchain-and-local-llms-powered-by-ollama/)
- 📚 [LangChain Cosmos DB Integration](https://python.langchain.com/docs/integrations/vectorstores/azurecosmosdb)
- 🦙 [Ollama Models Library](https://ollama.com/)
- 🔍 [Azure Cosmos DB Vector Search](https://learn.microsoft.com/azure/cosmos-db/gen-ai/vector-search-overview)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please submit PRs with:
- Clear commit messages
- Tests for new features
- Updated documentation

## Support

- 💬 GitHub Issues
- 📧 Email
- 💡 Discussions tab
