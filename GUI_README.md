# Streamlit GUI Application

## Quick Start

### 1. Install Streamlit
```bash
# Make sure you're in your virtual environment
pip install streamlit

# Or install all requirements
pip install -r requirements.txt
```

### 2. Run the App
```bash
# Method 1: Using streamlit command
streamlit run app.py

# Method 2: Using Python module
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

- 💬 **Interactive Chat Interface**: Ask questions and get AI-powered answers
- 📚 **Source Documents**: View the documents used to generate each answer
- ⚙️ **Configurable Settings**: Switch between FAISS and Cosmos DB, adjust models and parameters
- 🎨 **Beautiful UI**: Clean, modern interface with syntax highlighting
- 📊 **Real-time Stats**: Monitor vector store, models, and retrieval settings
- 💡 **Sample Questions**: Quick start with pre-defined example questions

## Usage

1. **Select Vector Store**: Choose between FAISS (simple) or Cosmos DB (production)
2. **Configure Models**: Adjust embedding and chat models in the sidebar
3. **Set Top-K**: Control how many documents to retrieve (1-10)
4. **Ask Questions**: Type your question in the chat input or click sample questions
5. **View Sources**: Expand source documents to see what context was used

## Configuration

The app uses environment variables from `.env` file:
- `EMBEDDINGS_MODEL`: Ollama embedding model (default: mxbai-embed-large)
- `CHAT_MODEL`: Ollama chat model (default: llama3)
- `TOP_K`: Number of documents to retrieve (default: 5)

## Requirements

- Ollama running with required models:
  - `ollama pull mxbai-embed-large`
  - `ollama pull llama3`
- Vector store data loaded:
  - Run `python simple/simple_load_data.py` for FAISS
  - Run `python cosmosdb/load_data.py` for Cosmos DB

## Tips

- Use **FAISS** for quick testing without Docker
- Use **Cosmos DB** for production-like testing
- Adjust **Top-K** to control answer quality vs speed
- Click **Clear Chat History** to start fresh
- Check **Source Documents** to understand how answers are generated

## Troubleshooting

### "Vector store not found"
Run the data loading script first:
```bash
python simple/simple_load_data.py
```

### "Ollama not responding"
Make sure Ollama is running:
```bash
ollama serve
```

### "Module not found"
Install all dependencies:
```bash
pip install -r requirements.txt
```

## Screenshots

(Add screenshots of your app here)

## Next Steps

- [ ] Add support for uploading custom documents
- [ ] Implement conversation memory
- [ ] Add visualization of vector similarity
- [ ] Export chat history
- [ ] Multi-language support
