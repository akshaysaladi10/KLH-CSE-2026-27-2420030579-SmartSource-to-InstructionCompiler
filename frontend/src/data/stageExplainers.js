export const STAGE_EXPLAINERS = {
  lexer: {
    title: "1. Lexical Analysis (Scanner)",
    what: "Converts the stream of raw characters from the source program into a structured sequence of meaningful tokens.",
    why: "Eliminates whitespace, strip comments, and groups characters into atomic language symbols (keywords, identifiers, numbers, operators).",
    input: "Raw source code string (e.g., 'int sum = 10 + 20;')",
    output: "Token stream: [KEYWORD_INT, IDENTIFIER('sum'), ASSIGN('='), INT(10), PLUS('+'), INT(20), SEMICOLON(';')]",
    example: "Character sequence 'w-h-i-l-e' is matched against grammar keywords to emit Token(KEYWORD_WHILE)."
  },
  parser: {
    title: "2. Syntax Analysis (Parser)",
    what: "Analyzes token ordering according to context-free grammar rules to construct an Abstract Syntax Tree (AST).",
    why: "Verifies grammatical correctness and establishes hierarchical operator precedence (e.g. '*' binds tighter than '+').",
    input: "Linear Token Stream from Lexer",
    output: "Hierarchical Abstract Syntax Tree (AST)",
    example: "'a + b * c' is parsed with precedence climbing into BinaryExpr('+', a, BinaryExpr('*', b, c))."
  },
  semantic: {
    title: "3. Semantic Analysis & Symbol Table",
    what: "Validates language invariants that grammar alone cannot enforce, such as scope rules and type safety.",
    why: "Ensures variables are declared before use, detects illegal redeclarations in the same scope, and checks type compatibility.",
    input: "Abstract Syntax Tree (AST)",
    output: "Scoped Symbol Table with types and validation diagnostics",
    example: "Disallows 'int x = \"hello\";' with a type mismatch diagnostic."
  },
  tac: {
    title: "4. Intermediate Code Generation (TAC)",
    what: "Translates the tree-based AST into machine-independent Three-Address Code (TAC) quadruples.",
    why: "Linearizes complex nested expressions into simple instructions with at most three operands, making optimization and codegen straightforward.",
    input: "Validated AST",
    output: "Sequence of linear TAC instructions using temporaries (t0, t1, ...) and labels (L0, L1, ...)",
    example: "'a = b + c * d' becomes 't0 = c * d', 't1 = b + t0', 'a = t1'."
  },
  optimizer: {
    title: "5. Multi-Pass Code Optimizer",
    what: "Applies semantics-preserving transformations to simplify code, reduce instruction count, and speed up runtime execution.",
    why: "Eliminates redundant calculations at compile time rather than wasting CPU cycles at runtime.",
    input: "Raw Three-Address Code",
    output: "Optimized Three-Address Code + Transformation Log",
    example: "Folds '10 + 20' to '30', propagates constants, and simplifies 'x * 1' to 'x'."
  },
  codegen: {
    title: "6. Target Instruction Generator",
    what: "Maps intermediate Three-Address Code into target pseudo-assembly instructions and assigns hardware/virtual registers.",
    why: "Bridges the gap between machine-independent IR and machine-oriented execution with real register constraints (R0-R7).",
    input: "Optimized TAC",
    output: "Target pseudo-assembly instructions (LOAD, STORE, ADD, CMP, JMP, etc.)",
    example: "'t0 = a + b' becomes 'LOAD R0, a', 'ADD R0, b', 'STORE t0, R0'."
  },
  vm: {
    title: "7. Target Virtual Machine & Debugger",
    what: "Simulates execution of the compiled pseudo-assembly instructions on an educational 32-bit register architecture.",
    why: "Allows students to step through instructions, inspect CPU registers and variable memory, and observe real program output.",
    input: "Generated pseudo-assembly instructions",
    output: "Live register states (R0-R7), memory slots, condition flags, and standard output",
    example: "Steps through loop instructions and calculates factorial 5! = 120."
  },
  trace: {
    title: "8. Source-to-Instruction Traceability",
    what: "Maintains an end-to-end relational mapping connecting each source line to its AST node, TAC quadruples, and target assembly.",
    why: "Provides unprecedented educational transparency, allowing learners to see how each line of code transforms across the entire compiler.",
    input: "All intermediate representations and tracking IDs",
    output: "Bidirectional relational trace matrix",
    example: "Clicking assembly line 'ADD R0, c' highlights source statement 'c = a + b;'."
  }
};
