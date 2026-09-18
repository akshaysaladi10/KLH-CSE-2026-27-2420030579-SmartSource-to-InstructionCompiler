# Testing & Verification Guide

## 1. Test Suite Architecture

The compiler project includes 35 comprehensive automated unit and integration tests under `backend/tests/`:

| Test Module | Coverage Area | Count |
| :--- | :--- | :--- |
| `test_lexer.py` | Keywords, literals, operators, comments, error recovery | 6 |
| `test_parser.py` | Declarations, precedence, control flow, syntax error recovery | 5 |
| `test_semantic.py` | Scope isolation, undeclared variables, duplicate decls, type checking | 6 |
| `test_tac.py` | Arithmetic lowering, control flow labels and conditional jumps | 3 |
| `test_optimizer.py` | Constant folding, propagation, algebraic simplification, dead code | 4 |
| `test_codegen.py` | Register allocation, pseudo-assembly opcodes, label synthesis | 2 |
| `test_simulator.py` | VM runtime execution, register state, memory state, console output | 3 |
| `test_api.py` | FastAPI endpoints (`/compile`, `/simulate`, `/examples`, `/health`) | 6 |

---

## 2. Running Automated Tests

Run pytest across all modules:
```bash
python -m pytest backend/tests -v
```

Run a specific test suite:
```bash
python -m pytest backend/tests/test_optimizer.py -v
```

Generate test coverage report:
```bash
python -m pytest --cov=backend/app backend/tests
```

---

## 3. Manual Verification Cases

### Test Case 1: Arithmetic & Operator Precedence
- **Input**:
  ```c
  int a = 10;
  int b = 20;
  int c;
  c = a + b * 2;
  print c;
  ```
- **Expected Outcome**:
  - `b * 2` computed first into temporary `t0` (40)
  - `a + t0` computed into `t1` (50)
  - `c = 50`
  - Output: `50`

### Test Case 2: Multi-Pass Optimization
- **Input**:
  ```c
  int x = 10 + 20;
  int y = x + 0;
  int z = y * 1;
  int unused = 999;
  int result = z * 2;
  print result;
  ```
- **Expected Outcome**:
  - Constant folding simplifies `10 + 20` to `30`.
  - Constant propagation sets `x = 30`.
  - Algebraic simplification simplifies `y + 0` and `z * 1`.
  - Final value `result = 60`.

### Test Case 3: Syntax & Semantic Error Handling
- **Input**:
  ```c
  int a = 10;
  b = 20;
  int a = 30;
  ```
- **Expected Outcome**:
  - Semantic Error: `Undeclared variable 'b'` on line 2.
  - Semantic Error: `Redeclaration of variable 'a'` on line 3.
  - Clean error cards displayed in UI without stack traces.
