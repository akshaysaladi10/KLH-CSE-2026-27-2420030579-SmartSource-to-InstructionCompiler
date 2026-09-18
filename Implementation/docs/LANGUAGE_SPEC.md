# Source Language Specification (Mini-C Educational Language)

This document specifies the lexical, syntactic, and semantic rules of the educational high-level programming language supported by the **Smart Source-to-Instruction Compiler**.

---

## 1. Lexical Grammar

### 1.1 Character Set
Source programs are UTF-8 encoded text files.

### 1.2 Comments and Whitespace
- Single-line comments begin with `//` and extend to the end of the line.
- Multi-line comments are enclosed in `/* ... */`.
- Whitespace consists of spaces, tabs (`\t`), and carriage returns/newlines (`\r`, `\n`). Whitespace separates tokens and is otherwise ignored except in string literals.

### 1.3 Keywords
The following reserved keywords cannot be used as identifiers:
```text
int       float     bool      string
if        else      while     for
print     return    true      false
```

### 1.4 Identifiers
Identifiers name variables and symbols:
- Syntax: `[a-zA-Z_][a-zA-Z0-9_]*`
- Case-sensitive.

### 1.5 Literals
- **Integer Literal**: Sequence of one or more decimal digits: `[0-9]+` (e.g., `0`, `42`, `1000`).
- **Floating-Point Literal**: Decimal digits with a fractional point: `[0-9]+\.[0-9]+` (e.g., `3.14`, `0.5`, `10.0`).
- **Boolean Literal**: Keyword `true` or `false`.
- **String Literal**: Sequence of characters enclosed in double quotes: `"hello world"`, `"Result: "`. Escape sequences `\n`, `\t`, `\"`, `\\` are supported.

### 1.6 Operators and Delimiters
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Assignment**: `=`
- **Relational / Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Delimiters**: `;`, `,`
- **Grouping**: `(`, `)`, `{`, `}`

---

## 2. Syntactic Grammar (EBNF)

```ebnf
Program        ::= Statement*

Statement      ::= VarDecl
                 | AssignStmt
                 | IfStmt
                 | WhileStmt
                 | ForStmt
                 | PrintStmt
                 | ReturnStmt
                 | Block

VarDecl        ::= Type IDENTIFIER ('=' Expression)? ';'
Type           ::= 'int' | 'float' | 'bool' | 'string'

AssignStmt     ::= IDENTIFIER '=' Expression ';'

IfStmt         ::= 'if' '(' Expression ')' Statement ('else' Statement)?

WhileStmt      ::= 'while' '(' Expression ')' Statement

ForStmt        ::= 'for' '(' (VarDecl | AssignStmt)? ';' Expression? ';' (IDENTIFIER '=' Expression)? ')' Statement

PrintStmt      ::= 'print' Expression ';'

ReturnStmt     ::= 'return' Expression? ';'

Block          ::= '{' Statement* '}'

Expression     ::= LogicalOrExpr

LogicalOrExpr  ::= LogicalAndExpr ('||' LogicalAndExpr)*

LogicalAndExpr ::= EqualityExpr ('&&' EqualityExpr)*

EqualityExpr   ::= RelationalExpr (('==' | '!=') RelationalExpr)*

RelationalExpr ::= AdditiveExpr (('<' | '<=' | '>' | '>=') AdditiveExpr)*

AdditiveExpr   ::= MultiplicativeExpr (('+' | '-') MultiplicativeExpr)*

MultiplicativeExpr ::= UnaryExpr (('*' | '/' | '%') UnaryExpr)*

UnaryExpr      ::= ('-' | '!' | '+') UnaryExpr
                 | PrimaryExpr

PrimaryExpr    ::= IDENTIFIER
                 | INT_LITERAL
                 | FLOAT_LITERAL
                 | STRING_LITERAL
                 | 'true' | 'false'
                 | '(' Expression ')'
```

---

## 3. Operator Precedence and Associativity

From lowest to highest precedence:

| Precedence Level | Operators | Description | Associativity |
|:---|:---|:---|:---|
| 1 (Lowest) | `=` | Assignment | Right-to-left |
| 2 | `\|\|` | Logical OR | Left-to-right |
| 3 | `&&` | Logical AND | Left-to-right |
| 4 | `==`, `!=` | Equality / Inequality | Left-to-right |
| 5 | `<`, `<=`, `>`, `>=` | Relational comparisons | Left-to-right |
| 6 | `+`, `-` | Addition, Subtraction | Left-to-right |
| 7 | `*`, `/`, `%` | Multiplication, Division, Modulo | Left-to-right |
| 8 (Highest) | `!`, unary `-`, unary `+` | Logical NOT, Unary sign | Right-to-left |

Grouping via parentheses `(` and `)` overrides precedence.

---

## 4. Semantic Rules

### 4.1 Scoping and Symbol Resolution
1. **Lexical Block Scoping**: Each block `{ ... }` creates a new nested lexical scope.
2. **Variable Shadowing**: A variable declared in an inner scope may shadow a variable with the identical name in an outer scope.
3. **Duplicate Declaration**: Declaring two variables with the same identifier in the identical scope produces a semantic error:
   ```c
   int x = 10;
   int x = 20; // ERROR: Duplicate declaration in scope 0
   ```
4. **Undeclared Variable**: Referencing or assigning to a variable without a prior declaration in the current or ancestor scopes produces a semantic error:
   ```c
   y = 42; // ERROR: Undeclared identifier 'y'
   ```

### 4.2 Type System and Rules
1. **Static Typing**: Variable types are bound at declaration time and immutable.
2. **Assignment Type Compatibility**:
   - `int` $\leftarrow$ `int`
   - `float` $\leftarrow$ `float` or `int` (widening coercion)
   - `bool` $\leftarrow$ `bool`
   - `string` $\leftarrow$ `string`
   - Incompatible assignments (e.g., assigning `"text"` to `int`) result in a `TypeMismatchError`.
3. **Arithmetic Operations**:
   - `+`, `-`, `*`, `/`, `%` are defined for `int` and `float`.
   - String concatenation: `string + string` is allowed.
4. **Relational Operations**:
   - `<`, `<=`, `>`, `>=` produce a `bool` result and require numeric operands.
   - `==`, `!=` compare compatible types and produce `bool`.
5. **Control Flow Conditions**:
   - `if` and `while` conditions must evaluate to `bool` (or numeric non-zero truthiness).

---

## 5. Sample Programs

### 5.1 Factorial
```c
int n = 5;
int fact = 1;
while (n > 1) {
    fact = fact * n;
    n = n - 1;
}
print fact; // Outputs: 120
```

### 5.2 Arithmetic & Precedence
```c
int a = 10;
int b = 5;
int c = 2;
int result = a + b * c; // Parses as a + (b * c) = 20
print result;
```

### 5.3 For Loop Accumulation
```c
int sum = 0;
for (int i = 1; i <= 5; i = i + 1) {
    sum = sum + i;
}
print sum; // Outputs: 15
```
