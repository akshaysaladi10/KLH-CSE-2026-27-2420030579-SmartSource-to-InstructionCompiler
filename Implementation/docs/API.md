# API Reference Specification

Base URL: `http://localhost:8000`

---

## 1. `POST /api/compile`

Compiles high-level source code through all stages of the compiler pipeline.

### Request Body
```json
{
  "source": "int a = 10; int b = 20; int c = a + b; print c;"
}
```

### Response Body
```json
{
  "success": true,
  "statistics": {
    "sourceLines": 4,
    "tokensCount": 18,
    "astNodesCount": 12,
    "symbolsCount": 3,
    "tacInstructionsCount": 5,
    "optimizedTacCount": 5,
    "optimizationsCount": 0,
    "targetInstructionsCount": 12,
    "compilationTimeMs": 2.14,
    "status": "Compilation Successful",
    "hasErrors": false,
    "errorCount": 0
  },
  "tokens": [
    {
      "token": "int",
      "lexeme": "int",
      "type": "Keyword",
      "line": 1,
      "column": 1,
      "literal": null
    }
  ],
  "ast": {
    "id": 1,
    "type": "Program",
    "label": "Program",
    "line": 1,
    "column": 1,
    "children": []
  },
  "symbolTable": [
    {
      "name": "a",
      "type": "int",
      "scope": "Global",
      "scopeLevel": 0,
      "line": 1,
      "column": 1,
      "isInitialized": true,
      "value": "uninitialized"
    }
  ],
  "tac": [
    {
      "op": "=",
      "arg1": "10",
      "arg2": null,
      "result": "a",
      "text": "a = 10",
      "line": 1,
      "astNodeId": 2
    }
  ],
  "optimizedTac": [],
  "optimizations": [],
  "instructions": [
    {
      "op": "LOAD",
      "arg1": "R0",
      "arg2": "10",
      "comment": "Load value '10'",
      "text": "LOAD   R0, 10             ; Load value '10'",
      "sourceLine": 1,
      "tacIndex": 0,
      "astNodeId": 2
    }
  ],
  "traceMatrix": [
    {
      "sourceLine": 1,
      "sourceCode": "int a = 10;",
      "astNodes": [],
      "tacInstructions": [],
      "optimizedTac": [],
      "targetInstructions": []
    }
  ],
  "errors": []
}
```

---

## 2. `POST /api/simulate`

Executes compiled pseudo-assembly instructions in the virtual machine.

### Request Body
```json
{
  "instructions": [
    { "op": "LOAD", "arg1": "R0", "arg2": "10", "sourceLine": 1 },
    { "op": "STORE", "arg1": "a", "arg2": "R0", "sourceLine": 1 },
    { "op": "HALT" }
  ],
  "maxCycles": 10000
}
```

### Response Body
```json
{
  "success": true,
  "cycles": 3,
  "warning": null,
  "output": [],
  "registers": {
    "R0": 10, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "R7": 0
  },
  "memory": {
    "a": 10
  },
  "stepHistory": [
    {
      "step": 1,
      "pc": 0,
      "instruction": "LOAD   R0, 10",
      "op": "LOAD",
      "registers": { "R0": 10 },
      "memory": {},
      "flagCmp": 0,
      "output": []
    }
  ]
}
```

---

## 3. `GET /api/examples`

Returns list of built-in sample programs.

### Response Body
```json
[
  {
    "id": "arithmetic",
    "title": "1. Arithmetic Basics",
    "category": "Basic",
    "description": "Simple variable declarations, assignment, and addition.",
    "code": "int a = 10; ..."
  }
]
```

---

## 4. `GET /api/health`

Health check endpoint.
```json
{
  "status": "healthy",
  "service": "Smart Source-to-Instruction Compiler"
}
```
