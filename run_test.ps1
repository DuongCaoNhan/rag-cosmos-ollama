# Run both versions: FAISS first, then Cosmos DB
# Usage: ./run_test.ps1 [-LoadData]   (-LoadData is passed to run_cosmos.ps1 on the first run)
param([switch]$LoadData)

& "$PSScriptRoot/run_faiss.ps1"
& "$PSScriptRoot/run_cosmos.ps1" -LoadData:$LoadData

Write-Host "You can now run a UI: streamlit run app.py | python app_gradio.py | python server.py" -ForegroundColor Cyan
