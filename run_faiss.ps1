# Run FAISS Version Only
# Configuration (models, top-k) is read from .env
Write-Host "🚀 Starting FAISS Version Test..." -ForegroundColor Cyan

# Check if Ollama is running
Write-Host "⚙️ Checking Ollama service..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get | Out-Null
    Write-Host "✅ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not running. Please start Ollama first: ollama serve" -ForegroundColor Red
    exit 1
}

# Check if vector store exists
if (Test-Path "vector_store/index.faiss") {
    Write-Host "✅ FAISS index found" -ForegroundColor Green

    Write-Host "`n📝 Testing FAISS vector search..." -ForegroundColor Cyan
    python simple/simple_vector_search.py "What is vector search in Cosmos DB?"

    Write-Host "`n💬 Running FAISS RAG chain..." -ForegroundColor Cyan
    python simple/simple_rag_chain.py
} else {
    Write-Host "❌ FAISS index not found. Please run python simple/simple_load_data.py first" -ForegroundColor Red
}

Write-Host "`n✨ FAISS version test completed!" -ForegroundColor Green
