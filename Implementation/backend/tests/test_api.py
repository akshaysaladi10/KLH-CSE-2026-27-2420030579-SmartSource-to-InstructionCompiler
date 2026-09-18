import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_api_examples():
    res = client.get("/api/examples")
    assert res.status_code == 200
    examples = res.json()
    assert len(examples) >= 4
    ids = [e["id"] for e in examples]
    assert "arithmetic" in ids
    assert "expression" in ids
    assert "conditional" in ids
    assert "loop" in ids


def test_api_compile_valid():
    payload = {"source": "int a = 10; int b = 20; int c = a + b; print c;"}
    res = client.post("/api/compile", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["tokens"]) > 0
    assert data["ast"] is not None
    assert len(data["symbolTable"]) == 3
    assert len(data["tac"]) > 0
    assert len(data["instructions"]) > 0
    assert len(data["traceMatrix"]) > 0
    assert data["statistics"]["status"] == "Compilation Successful"


def test_api_compile_syntax_error():
    payload = {"source": "int a = ;"}
    res = client.post("/api/compile", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is False
    assert len(data["errors"]) > 0
    assert data["errors"][0]["errorType"] == "Syntax Error"


def test_api_compile_semantic_error():
    payload = {"source": "int a = 10; b = 20;"}
    res = client.post("/api/compile", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is False
    assert len(data["errors"]) > 0
    assert any(e["errorType"] == "Semantic Error" for e in data["errors"])


def test_api_simulate():
    # First compile a program
    compile_res = client.post("/api/compile", json={"source": "int x = 5; int y = x + 10; print y;"})
    instrs = compile_res.json()["instructions"]

    # Now simulate
    sim_res = client.post("/api/simulate", json={"instructions": instrs})
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert sim_data["success"] is True
    assert sim_data["memory"]["y"] == 15
    assert sim_data["output"] == ["15"]
