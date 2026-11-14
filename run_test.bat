@echo off
:: Runs run_test.ps1 (FAISS then Cosmos DB). Pass -LoadData on the first run.
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_test.ps1" %*
pause
