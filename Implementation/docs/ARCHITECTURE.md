# Architecture Specification

## 1. System Overview

The **Smart Source-to-Instruction Compiler** is designed as a modular, 7-stage educational compilation platform. Its primary architectural goal is total transparency across all internal transformations:

```
Source Code
    │
    ▼
[1. Lexical Analyzer] ───► Token Stream (type, lexeme, line, column)
    │
    ▼
[2. Recursive Descent Parser] ───► Abstract Syntax Tree (AST)
    │
    ▼
[3. Scoped Semantic Analyzer] ───► Scoped Symbol Table & Type Invariants
    │
    ▼
[4. Intermediate Code Generator] ───► Linear Three-Address Code (TAC Quadruples)
    │
    ▼
[5. Optimization Pipeline] ───► Optimized TAC (Folding, Propagation, Identities, Dead Code)
    │
    ▼
[6. Target Code Generator] ───► Pseudo-Assembly (LOAD, STORE, ADD, CMP, JMP, etc.)
    │
    ▼
[7. Traceability Engine & VM] ───► Source-to-Instruction Matrix & Runtime Execution
```

---

## 2. Compiler Subsystems

### 2.1 Lexical Analyzer (`backend/app/compiler/lexer/`)
- **Tokens Model** (`tokens.py`): Strongly-typed `TokenType` enum covering language keywords (`int`, `float`, `bool`, `string`, `if`, `else`, `while`, `print`, `return`, `true`, `false`), literals, operators, and delimiters.
- **Scanner Engine** (`lexer.py`): Performs character-by-character lexical analysis with exact 1-indexed line and column tracking, multi-line comment handling, string escape decoding, and non-fatal error recovery.

### 2.2 Syntax Analyzer (`backend/app/compiler/parser/`)
- **AST Representation** (`ast_nodes.py`): Object-oriented node hierarchy (`Program`, `VarDecl`, `Assignment`, `BinaryExpr`, `UnaryExpr`, `LiteralExpr`, `VariableExpr`, `IfStmt`, `WhileStmt`, `PrintStmt`, `Block`). Nodes serialize into a hierarchical JSON tree for visual rendering.
- **Recursive Descent Parser** (`parser.py`): Handcrafted recursive-descent parser with precedence climbing for binary operators (unary > multiplicative > additive > relational > equality > logical AND > logical OR). Contains synchronization routines at statement boundaries to capture multiple diagnostics.

### 2.3 Semantic Analyzer (`backend/app/compiler/semantic/`)
- **Symbol Table Manager** (`symbol_table.py`): Implements nested scopes with parent pointers. Records variable symbol name, data type, scope depth, initialization state, and source coordinates.
- **Type Checker & Validator** (`analyzer.py`): Validates variable declarations, detects undeclared identifiers, prevents duplicate declarations in the same scope, enforces type compatibility on assignment and arithmetic/logical operations, and validates branch condition expressions.

### 2.4 Intermediate Code Representation (`backend/app/compiler/intermediate/`)
- **Quadruple Instruction Model** (`tac.py`): Represents operations in canonical 3-address format (`result = arg1 op arg2`).
- **TAC Generator** (`generator.py`): Lowers the AST into linear TAC with automated temporary register (`t0`, `t1`, ...) and jump label (`L0`, `L1`, ...) synthesis, retaining source line and AST node references.

### 2.5 Multi-Pass Optimizer (`backend/app/compiler/optimizer/`)
- **Constant Folding**: Evaluates constant operations at compile time (`10 + 20` -> `30`).
- **Constant Propagation**: Replaces known variable values with literals inside basic blocks.
- **Algebraic Simplification**: Eliminates identity operations (`x + 0` -> `x`, `x * 1` -> `x`, `x * 0` -> `0`, `x - 0` -> `x`).
- **Dead Code Elimination**: Removes dead temporary assignments and unreachable blocks following unconditional jumps or returns.
- **Pipeline Orchestrator**: Iteratively executes passes until convergence or max iterations, generating a change log and Before/After diff.

### 2.6 Target Code Generation & VM (`backend/app/compiler/target/`)
- **Target Instruction Set**: 32-bit register-based instruction set (`LOAD`, `STORE`, `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `CMP`, `SETEQ`, `SETNE`, `SETLT`, `SETGT`, `JMP`, `JZ`, `JNZ`, `PRINT`, `LABEL`, `HALT`).
- **Deterministic Register Allocator**: Manages physical registers `R0` through `R7` using a deterministic FIFO/LRU eviction policy.
- **Virtual Machine Simulator** (`simulator.py`): Step-by-step target instruction execution engine with register meters, memory tracking, and standard output log.

### 2.7 Traceability System (`backend/app/compiler/trace/`)
- Builds an interconnected 4-tier matrix:
  $$\text{Source Statement} \longleftrightarrow \text{AST Node} \longleftrightarrow \text{TAC Quadruple} \longleftrightarrow \text{Target Assembly}$$
- Enables interactive cross-highlighting across all stages.

---

## 3. Frontend Architecture

- **React 18 + Vite**: High-performance single page application.
- **Component Hierarchy**:
  - `Header`: Navigation, sample loader, Compile and VM execution triggers.
  - `Editor`: Gutter-driven line numbered source code editor with keyboard shortcuts (`Ctrl+Enter`).
  - `Dashboard`: Compilation statistics cards (lines, tokens, AST nodes, symbols, TAC, optimizations, assembly, elapsed ms).
  - `ErrorPanel`: Diagnostic banner with error type, line, column, message, and guidance tips.
  - `Tabs`:
    - `TokensTab`: Paginated, filterable token table with badge categorization.
    - `AstTab`: Collapsible, color-coded visual AST tree.
    - `SymbolTableTab`: Scoped symbol table with initialization status.
    - `TacTab`: Linear TAC quadruple table.
    - `OptimizationTab`: Side-by-side Before/After diff and transformation log.
    - `AssemblyTab`: Formatted pseudo-assembly with register allocation metadata.
    - `TraceTab`: Linked 4-tier traceability matrix.
    - `SimulatorTab`: Step-forward, step-backward VM runner with live register display.
