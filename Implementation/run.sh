#!/usr/bin/env bash
set -e

echo "==================================================="
echo "  Starting Smart Source-to-Instruction Compiler"
echo "==================================================="

echo "[1/2] Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "[2/2] Starting server at http://localhost:8000"
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
