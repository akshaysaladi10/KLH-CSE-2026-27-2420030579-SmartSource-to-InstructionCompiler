# Setup & Execution Guide

## Prerequisites

- **Python**: 3.10+ (tested on Python 3.11, 3.12, 3.13)
- **Node.js**: 18+ and npm (tested on Node v20, v24)
- **Docker** (Optional, for containerized run)

---

## Quick Start (Unified Single Server)

The fastest way to run both backend and frontend together:

### Windows:
Double-click `run.bat` or run:
```cmd
run.bat
```

### Linux / macOS:
```bash
chmod +x run.sh
./run.sh
```

Then navigate to:
```
http://localhost:8000
```

---

## Development Setup (Independent Frontend & Backend)

### 1. Backend Setup
```bash
# Navigate to project root
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt

# Start backend dev server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API docs available at: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Vite dev server with proxy
npm run dev
```
Open browser at: `http://localhost:5173`

---

## Docker Deployment

Build and run the entire unified stack with one command:
```bash
docker compose up --build
```
Access the application at `http://localhost:8000`.
