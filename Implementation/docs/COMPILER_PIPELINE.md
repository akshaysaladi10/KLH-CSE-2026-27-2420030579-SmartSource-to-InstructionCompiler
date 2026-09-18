# Compiler Pipeline Specification

This document details each stage of the compilation pipeline, its input/output invariants, formal grammar, and translation rules.

---

## 1. Supported Language Grammar (EBNF)

```ebnf
Program        ::= Statement* EOF

Statement      ::= VarDecl
                 | AssignmentStmt
                 | IfStmt
                 | WhileStmt
                 | Block
                 | PrintStmt
                 | ReturnStmt

VarDecl        ::= ("int" | "float" | "bool" | "string") IDENTIFIER ("=" Expression)? ";"
AssignmentStmt ::= IDENTIFIER ("=" | "+=" | "-=" | "*=" | "/=") Expression ";"
IfStmt         ::= "if" "(" Expression ")" Statement ("else" Statement)?
WhileStmt      ::= "while" "(" Expression ")" Statement
Block          ::= "{" Statement* "}"
PrintStmt      ::= "print" "("? Expression ")"? ";"
ReturnStmt     ::= "return" Expression? ";"

Expression     ::= LogicOr
LogicOr        ::= LogicAnd ("||" LogicAnd)*
LogicAnd       ::= Equality ("&&" Equality)*
Equality       ::= Relational (("==" | "!=") Relational)*
Relational     ::= Additive (("<" | "<=" | ">" | ">=") Additive)*
Additive       ::= Multiplicative (("+" | "-") Multiplicative)*
Multiplicative ::= Unary (("*" | "/" | "%") Unary)*
Unary          ::= ("!" | "-") Unary | Primary
Primary        ::= INT_LITERAL | FLOAT_LITERAL | STRING_LITERAL | BOOL_LITERAL
                 | IDENTIFIER | "(" Expression ")"
```

---

## 2. Stage-by-Stage Breakdown

### Stage 1: Lexical Analysis
- Converts raw input text stream into structured tokens.
- Token format: `(TokenType, Lexeme, LiteralValue, LineNumber, ColumnNumber)`.
- Skips whitespace and comments (`//` and `/* ... */`).
- Captures lexical errors with line and column positions.

### Stage 2: Syntax Analysis
- Performs recursive descent parsing to construct an Abstract Syntax Tree (AST).
- Precedence climbing guarantees proper operator grouping (`*` before `+`).
- Compound assignments (`a += b`) are desugared to `a = a + b`.
- Produces clean diagnostic messages on syntax mismatch with synchronization recovery.

### Stage 3: Semantic Analysis
- Maintains scoped symbol tables with lexical scope stack.
- Ensures identifiers are declared prior to reference.
- Enforces strict type compatibility for assignments, arithmetic, and logic.
- Flags duplicate variable definitions within the same scope.

### Stage 4: Intermediate Code Generation (TAC)
- Transforms tree-structured AST into linear Three-Address Code.
- Every instruction has at most three operands in quadruple format: `result = arg1 op arg2`.
- Conditional branching:
  - `ifFalse cond goto Label`
  - `goto Label`
  - `label LabelName`
- Synthesizes temporaries (`t0`, `t1`, ...) and labels (`L0`, `L1`, ...).

### Stage 5: Multi-Pass Code Optimization
Runs the following passes until a fixed point is reached:
1. **Constant Propagation**: Tracks constant values inside basic blocks and replaces variable uses with known constants.
2. **Constant Folding**: Computes operations on literal constants at compile time.
3. **Algebraic Simplification**:
   - $x + 0 \rightarrow x$
   - $x \times 1 \rightarrow x$
   - $x \times 0 \rightarrow 0$
   - $x - 0 \rightarrow x$
   - $x / 1 \rightarrow x$
4. **Dead Code Elimination**: Removes unused temporary variable definitions and unreachable instructions after jumps.

### Stage 6: Target Instruction Generation
- Maps Three-Address Code to target pseudo-assembly instructions:
  - `LOAD R, memory_or_literal`
  - `STORE memory, R`
  - `ADD / SUB / MUL / DIV / MOD R, operand`
  - `CMP R, operand`
  - `SETEQ / SETNE / SETLT / SETGT R`
  - `JMP / JZ / JNZ / JGT / JLT label`
  - `PRINT R`
  - `HALT`
- Deterministic register allocation allocates registers `R0`–`R7` using FIFO/LRU spilling.

### Stage 7: Source-to-Instruction Traceability
- Correlates each generated assembly instruction back through its intermediate TAC quadruple, AST node, and originating source line.
- Powers the interactive UI cross-highlighting matrix.
