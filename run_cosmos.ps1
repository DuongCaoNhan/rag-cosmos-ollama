# Run Cosmos DB Version Only
# Usage: ./run_cosmos.ps1 -LoadData   (first run: create container + load documents)
#        ./run_cosmos.ps1             (later runs: data is already in the emulator)
# Configuration (models, database, container) is read from .env
param([switch]$LoadData)

Write-Host "🚀 Starting Cosmos DB Version Test..." -ForegroundColor Cyan

# Check if Ollama is running
Write-Host "⚙️ Checking Ollama service..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get | Out-Null
    Write-Host "✅ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not running. Please start Ollama first: ollama serve" -ForegroundColor Red
    exit 1
}

# Check if Docker is running
Write-Host "`n⚙️ Checking Docker service..." -ForegroundColor Cyan
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not running. Please start Docker first" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker is running" -ForegroundColor Green

# Start Cosmos DB Emulator (keeps existing container/data if already created)
Write-Host "🚀 Starting Cosmos DB Emulator..." -ForegroundColor Cyan
docker compose up -d

# Wait until the emulator answers (instead of a fixed sleep)
Write-Host "⏳ Waiting for emulator to be ready (up to 5 minutes)..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 60; $i++) {
    try {
        Invoke-WebRequest -Uri "https://127.0.0.1:8081/_explorer/emulator.pem" -SkipCertificateCheck -TimeoutSec 5 -UseBasicParsing | Out-Null
        $ready = $true
        break
    } catch {
        Start-Sleep -Seconds 5
    }
}
if (-not $ready) {
    Write-Host "❌ Emulator did not become ready. Check: docker logs cosmos-emulator" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Emulator is ready" -ForegroundColor Green

# Load documents into Cosmos DB (creates database + container with vector policy)
if ($LoadData) {
    Write-Host "`n📥 Loading documents into Cosmos DB..." -ForegroundColor Cyan
    python cosmosdb/load_data.py
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

# Test Cosmos DB
Write-Host "`n📝 Testing Cosmos DB vector search..." -ForegroundColor Cyan
python cosmosdb/vector_search.py "What is vector search in Cosmos DB?"

Write-Host "`n💬 Running Cosmos DB RAG chain..." -ForegroundColor Cyan
python cosmosdb/cosmos_rag_chain.py

Write-Host "`n✨ Cosmos DB version test completed!" -ForegroundColor Green
