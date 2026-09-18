@echo off
echo ===================================================
echo   Starting Smart Source-to-Instruction Compiler
echo ===================================================

echo [1/2] Checking Python backend dependencies...
python -m pip install -r backend/requirements.txt

echo [2/2] Starting server at http://localhost:8000
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
