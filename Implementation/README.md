# Smart Source-to-Instruction Compiler

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646cff.svg)](https://vitejs.dev/)
[![Tests](https://img.shields.io/badge/Tests-40%20Passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An educational and professional compiler platform that visualizes and executes the complete compilation pipeline:
**Source Code &rarr; Lexical Analysis &rarr; Syntax Analysis &rarr; Semantic Analysis &rarr; Intermediate Representation (TAC) &rarr; Code Optimization &rarr; Target Pseudo-Assembly &rarr; Interactive VM Simulation &amp; Traceability**.

---

## 1. Problem Statement & Motivation

Traditional compiler demonstrations frequently focus on only one or two isolated stages (such as lexical analysis or simple AST parsing). This leaves students and engineers struggling to understand how high-level abstractions actually transform step-by-step into machine-level instructions.

The **Smart Source-to-Instruction Compiler** addresses this educational gap by providing a fully functional, transparent 7-stage compiler engine accompanied by an interactive IDE and a bidirectional **Source-to-Instruction Traceability Pipeline**.

---

## 2. Key Novelty & Distinguishing Features

1. **Complete 7-Stage Pipeline**: Implements genuine, handcrafted lexical, syntactic, semantic, intermediate representation, optimization, target pseudo-assembly, and runtime simulation stages without relying on opaque third-party compilers.
2. **Source-to-Instruction Traceability Matrix**: Maps every generated assembly instruction directly back through its intermediate Three-Address Code quadruple, AST node, and originating source code statement.
3. **Interactive Multi-Pass Optimizer**: Demonstrates Constant Folding, Constant Propagation, Algebraic Simplification, and Dead Code Elimination with side-by-side Before/After diffs and reduction analytics, plus selective pass toggling.
4. **Built-in Target Virtual Machine Simulator**: Executes the generated 32-bit pseudo-assembly step-by-step or to completion, showing real-time CPU register values (`R0`–`R7`), condition flags (`Z`, `S`, `GT`, `LT`), variable memory slots, and console output with breakpoint support.
5. **Modern Academic IDE**: Features a dark-themed, glassmorphic UI with line numbering, interactive AST tree navigation, scoped symbol tables, structured diagnostic reporting with fix tips, real-time stage timings, and one-click artifact exporters (CSV, JSON, ASM).

---

## 3. Architecture & Compilation Flow

```
   ┌────────────────────────────────────────────────────────┐
   │                  Source Program                        │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  1. Lexer (Tokens, line/col coordinates, recovery)     │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  2. Parser (Recursive descent, AST tree generation)    │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  3. Semantic Analyzer (Scope stack, symbol table)      │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  4. Intermediate Code Generator (Three-Address Code)   │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  5. Optimizer (Folding, propagation, identities, DCE)  │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  6. Target Code Generator (Register allocation, ISA)   │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │  7. Traceability Matrix & Target VM Simulator          │
   └────────────────────────────────────────────────────────┘
```

---

## 4. Directory Structure

```
SmartSourceToInstructionCompiler/
│
├── backend/
│   ├── app/
│   │   ├── compiler/
│   │   │   ├── lexer/           # Token types, scanner, position tracking
│   │   │   ├── parser/          # AST nodes, recursive descent parser
│   │   │   ├── semantic/        # Scoped symbol table, type verification
│   │   │   ├── intermediate/    # Three-address code quadruples generator
│   │   │   ├── optimizer/       # Constant folding/prop, algebraic, DCE passes
│   │   │   ├── target/          # Target ISA, register allocator, VM simulator
│   │   │   ├── trace/           # 4-tier source-to-instruction tracer
│   │   │   └── pipeline.py      # Master compiler pipeline orchestrator
│   │   ├── api/
│   │   │   ├── schemas.py       # Pydantic request/response models
│   │   │   └── routes.py        # API endpoints (/compile, /simulate, /examples)
│   │   └── main.py              # FastAPI app with CORS & static asset mount
│   ├── tests/                   # 40 comprehensive automated pytest suites
│   └── requirements.txt         # Backend Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx       # Controls, sample selector, action buttons, exports
│   │   │   ├── Editor.jsx       # Gutter-driven line numbered code editor
│   │   │   ├── Dashboard.jsx    # Metrics and compilation analytics
│   │   │   ├── TimingBar.jsx    # Microsecond stage timings display
│   │   │   ├── ErrorPanel.jsx   # Structured error diagnostics
│   │   │   ├── HistoryDrawer.jsx # Local storage compilation run history
│   │   │   ├── InstructionReferenceModal.jsx # Target ISA reference manual
│   │   │   ├── StageExplainerModal.jsx       # Educational stage guide
│   │   │   └── tabs/
│   │   │       ├── TokensTab.jsx      # Filterable token stream table
│   │   │       ├── AstTab.jsx         # Collapsible visual tree visualizer
│   │   │       ├── SymbolTableTab.jsx # Scoped symbol table
│   │   │       ├── TacTab.jsx         # Intermediate TAC instructions
│   │   │       ├── OptimizationTab.jsx# Side-by-side diff & pass records
│   │   │       ├── AssemblyTab.jsx    # Target pseudo-assembly with breakpoints
│   │   │       ├── TraceTab.jsx       # Linked 4-tier traceability matrix
│   │   │       └── SimulatorTab.jsx   # Interactive step-by-step VM debugger
│   │   ├── data/
│   │   │   ├── samples.js             # 8 built-in educational code examples
│   │   │   ├── instructionReference.js# Complete ISA documentation dataset
│   │   │   └── stageExplainers.js     # Stage educational explainers
│   │   ├── utils/
│   │   │   └── exporters.js     # CSV/JSON/TXT downloaders
│   │   ├── App.jsx              # Main application coordinator
│   │   ├── index.css            # Dark mode design system
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   ├── ARCHITECTURE.md          # Comprehensive architectural specification
│   ├── API.md                   # Complete REST API reference
│   ├── COMPILER_PIPELINE.md     # Compiler stage specifications
│   ├── LANGUAGE_SPEC.md         # Formal EBNF grammar, types, and scoping rules
│   ├── INSTRUCTION_SET.md       # Target ISA manual, opcodes, and flag semantics
│   ├── TESTING.md               # Test suite documentation and cases
│   └── SETUP.md                 # Detailed environment setup guide
│
├── Dockerfile                   # Multi-stage production container build
├── docker-compose.yml           # Zero-configuration container orchestrator
├── run.bat                      # Windows one-click start script
├── run.sh                       # Linux/macOS start script
├── .env.example                 # Example environment variables
├── .gitignore                   # Clean repository exclusions
└── README.md                    # Project master documentation
```

---

## 5. Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Compiler Engine** | Python 3.10+ | Clean, readable syntax for AST manipulation, recursion, and pass pipelines. |
| **Backend API** | FastAPI + Uvicorn | Blazing-fast asynchronous REST API with automatic OpenAPI validation. |
| **Frontend Framework** | React 18 + Vite | Fast HMR, reactive state management across 8 pipeline tabs. |
| **Icons & Design System** | Lucide React + CSS3 | Custom midnight-slate palette with glassmorphism and refined typography. |
| **Test Automation** | pytest + TestClient | 40 end-to-end and unit tests verifying all compilation phases. |
| **Containerization** | Docker & Compose | Multi-stage build producing a self-contained runtime image. |

---

## 6. Quick Start & Execution

### Option A: Local Execution (Single Unified Server)

#### Windows
```cmd
run.bat
```

#### Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

Open **`http://localhost:8000`** in your browser.

---

### Option B: Docker Container

```bash
docker compose up --build
```
Navigate to **`http://localhost:8000`**.

---

### Option C: Independent Development Servers

1. **Start Backend**:
   ```bash
   pip install -r backend/requirements.txt
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Access at `http://localhost:5173`.

---

## 7. Built-in Educational Programs

The compiler includes 8 curated sample programs:

| # | Program Title | Highlights Tested |
| :-: | :--- | :--- |
| **1** | **Arithmetic Basics** | Variable declarations, assignments, arithmetic addition. |
| **2** | **Expression & Precedence** | Multiplicative operator precedence ($*$ evaluated before $+$). |
| **3** | **Conditional Branching** | `if`/`else` control flow, relational comparison, jump labels. |
| **4** | **While Loop Accumulator** | Iterative while loop summing integers from 0 to 9. |
| **5** | **Optimization Showcase** | Constant folding ($10+20 \rightarrow 30$), algebraic identity simplification ($y+0$, $z \times 1$), dead code pruning. |
| **6** | **Factorial Algorithm** | Computes $5! = 120$ via iterative register multiplication and decrement. |
| **7** | **For Loop Accumulator** | Standard `for (int i = 1; i <= 5; i = i + 1)` loop execution. |
| **8** | **Fibonacci Sequence** | Multi-variable sequence calculation with iterative state updates. |

---

## 8. Test Results

Run all 40 tests with pytest:
```bash
python -m pytest backend/tests -v
```

```
============================= test session starts =============================
collected 40 items

backend/tests/test_api.py::test_api_health PASSED                        [  2%]
backend/tests/test_api.py::test_api_examples PASSED                      [  5%]
backend/tests/test_api.py::test_api_compile_valid PASSED                 [  7%]
backend/tests/test_api.py::test_api_compile_syntax_error PASSED          [ 10%]
backend/tests/test_api.py::test_api_compile_semantic_error PASSED        [ 12%]
backend/tests/test_api.py::test_api_simulate PASSED                      [ 15%]
backend/tests/test_codegen.py::test_codegen_arithmetic PASSED            [ 17%]
backend/tests/test_codegen.py::test_codegen_conditional PASSED           [ 20%]
backend/tests/test_lexer.py::test_lexer_basic_tokens PASSED              [ 22%]
backend/tests/test_lexer.py::test_lexer_floats_and_strings PASSED        [ 25%]
backend/tests/test_lexer.py::test_lexer_comments PASSED                  [ 27%]
backend/tests/test_lexer.py::test_lexer_operators PASSED                 [ 30%]
backend/tests/test_lexer.py::test_lexer_invalid_character_error PASSED   [ 32%]
backend/tests/test_lexer.py::test_lexer_unterminated_string_error PASSED [ 35%]
backend/tests/test_master_features.py::test_for_loop_compilation_and_execution PASSED [ 37%]
backend/tests/test_master_features.py::test_selective_optimizer_passes PASSED [ 40%]
backend/tests/test_master_features.py::test_vm_breakpoints PASSED        [ 42%]
backend/tests/test_master_features.py::test_vm_flags_and_branches PASSED [ 45%]
backend/tests/test_master_features.py::test_stage_timings_recorded PASSED [ 47%]
backend/tests/test_optimizer.py::test_optimizer_constant_folding PASSED  [ 50%]
backend/tests/test_optimizer.py::test_optimizer_algebraic_simplification PASSED [ 52%]
backend/tests/test_optimizer.py::test_optimizer_constant_propagation PASSED [ 55%]
backend/tests/test_optimizer.py::test_optimizer_dead_code_elimination PASSED [ 57%]
backend/tests/test_parser.py::test_parser_variable_declarations PASSED   [ 60%]
backend/tests/test_parser.py::test_parser_precedence PASSED              [ 62%]
backend/tests/test_parser.py::test_parser_if_else_and_while PASSED       [ 65%]
backend/tests/test_parser.py::test_parser_syntax_error_missing_semicolon PASSED [ 67%]
backend/tests/test_parser.py::test_parser_syntax_error_invalid_expression PASSED [ 70%]
backend/tests/test_semantic.py::test_semantic_valid_declarations PASSED  [ 72%]
backend/tests/test_semantic.py::test_semantic_undeclared_variable PASSED [ 75%]
backend/tests/test_semantic.py::test_semantic_duplicate_declaration PASSED [ 77%]
backend/tests/test_semantic.py::test_semantic_type_mismatch PASSED       [ 80%]
backend/tests/test_semantic.py::test_semantic_invalid_binary_operation PASSED [ 82%]
backend/tests/test_semantic.py::test_semantic_scope_isolation PASSED     [ 85%]
backend/tests/test_simulator.py::test_simulator_arithmetic_execution PASSED [ 87%]
backend/tests/test_simulator.py::test_simulator_while_loop_accumulator PASSED [ 90%]
backend/tests/test_simulator.py::test_simulator_print_statement PASSED   [ 92%]
backend/tests/test_tac.py::test_tac_arithmetic PASSED                    [ 95%]
backend/tests/test_tac.py::test_tac_if_else PASSED                       [ 97%]
backend/tests/test_tac.py::test_tac_while_loop PASSED                    [100%]

======================= 40 passed in 0.57s ========================
```

---

## 9. Future Scope

1. **Function Definitions & Activation Records**: Add stack frame visualization and parameter passing for functions.
2. **Target Architectures**: Support export targeting real RISC-V (RV32I) or x86-64 assembly.
3. **Control Flow Graph (CFG)**: Render interactive visual basic-block control flow graphs using React Flow.
4. **SSA (Static Single Assignment)**: Add phi-nodes and SSA form visualization.

---

## 10. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

