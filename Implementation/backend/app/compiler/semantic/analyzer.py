from typing import List, Tuple, Optional, Any
from ..parser.ast_nodes import (
    Program,
    VarDecl,
    Assignment,
    BinaryExpr,
    UnaryExpr,
    LiteralExpr,
    VariableExpr,
    Block,
    IfStmt,
    WhileStmt,
    ForStmt,
    PrintStmt,
    ReturnStmt,
    ASTNode,
)
from .symbol_table import SymbolTableManager, Symbol


class SemanticError:
    def __init__(
        self,
        message: str,
        line: int,
        column: int,
        possible_cause: str = "",
    ):
        self.message = message
        self.line = line
        self.column = column
        self.possible_cause = possible_cause

    def to_dict(self) -> dict:
        return {
            "errorType": "Semantic Error",
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "possibleCause": self.possible_cause,
        }


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_manager = SymbolTableManager()
        self.errors: List[SemanticError] = []

    def analyze(self, program: Program) -> Tuple[List[dict], List[SemanticError]]:
        self.errors.clear()
        self.symbol_manager = SymbolTableManager()

        for stmt in program.statements:
            self._visit(stmt)

        return self.symbol_manager.get_all_records(), self.errors

    def _visit(self, node: ASTNode) -> Optional[str]:
        if isinstance(node, VarDecl):
            return self._visit_var_decl(node)
        elif isinstance(node, Assignment):
            return self._visit_assignment(node)
        elif isinstance(node, BinaryExpr):
            return self._visit_binary_expr(node)
        elif isinstance(node, UnaryExpr):
            return self._visit_unary_expr(node)
        elif isinstance(node, LiteralExpr):
            return self._visit_literal_expr(node)
        elif isinstance(node, VariableExpr):
            return self._visit_variable_expr(node)
        elif isinstance(node, Block):
            return self._visit_block(node)
        elif isinstance(node, IfStmt):
            return self._visit_if_stmt(node)
        elif isinstance(node, WhileStmt):
            return self._visit_while_stmt(node)
        elif isinstance(node, ForStmt):
            return self._visit_for_stmt(node)
        elif isinstance(node, PrintStmt):
            return self._visit_print_stmt(node)
        elif isinstance(node, ReturnStmt):
            return self._visit_return_stmt(node)
        return None

    def _visit_var_decl(self, node: VarDecl) -> Optional[str]:
        # Check duplicate declaration in current scope
        existing = self.symbol_manager.lookup_current(node.name)
        if existing:
            self.errors.append(
                SemanticError(
                    f"Redeclaration of variable '{node.name}' in the same scope",
                    node.line,
                    node.column,
                    f"Variable '{node.name}' was already declared on line {existing.line}. Use assignment without redeclaring, or use a distinct name.",
                )
            )
            return None

        init_val = None
        has_init = False
        if node.initializer:
            init_type = self._visit(node.initializer)
            has_init = True
            if init_type and not self._is_type_compatible(node.var_type, init_type):
                self.errors.append(
                    SemanticError(
                        f"Cannot initialize variable '{node.name}' of type '{node.var_type}' with incompatible expression of type '{init_type}'",
                        node.line,
                        node.column,
                        f"Types '{node.var_type}' and '{init_type}' are incompatible for assignment.",
                    )
                )

        symbol = Symbol(
            name=node.name,
            type_name=node.var_type,
            scope_level=self.symbol_manager.current_scope.level,
            line=node.line,
            column=node.column,
            is_initialized=has_init,
            value=init_val,
        )
        self.symbol_manager.define(symbol)
        return node.var_type

    def _visit_assignment(self, node: Assignment) -> Optional[str]:
        symbol = self.symbol_manager.lookup(node.name)
        if not symbol:
            self.errors.append(
                SemanticError(
                    f"Undeclared variable '{node.name}'",
                    node.line,
                    node.column,
                    f"Variable '{node.name}' was used before being declared. Declare it first using 'int {node.name};', etc.",
                )
            )
            val_type = self._visit(node.value)
            return val_type

        val_type = self._visit(node.value)
        if val_type and not self._is_type_compatible(symbol.type_name, val_type):
            self.errors.append(
                SemanticError(
                    f"Cannot assign value of type '{val_type}' to variable '{node.name}' of type '{symbol.type_name}'",
                    node.line,
                    node.column,
                    f"Type mismatch: expected '{symbol.type_name}', got '{val_type}'.",
                )
            )

        symbol.is_initialized = True
        return symbol.type_name

    def _visit_binary_expr(self, node: BinaryExpr) -> Optional[str]:
        left_type = self._visit(node.left)
        right_type = self._visit(node.right)

        if not left_type or not right_type:
            return None

        op = node.operator

        # Arithmetic
        if op in ("+", "-", "*", "/", "%"):
            if left_type == "string" and right_type == "string" and op == "+":
                return "string"
            if left_type in ("int", "float") and right_type in ("int", "float"):
                if left_type == "float" or right_type == "float":
                    return "float"
                return "int"

            self.errors.append(
                SemanticError(
                    f"Operator '{op}' cannot be applied to types '{left_type}' and '{right_type}'",
                    node.line,
                    node.column,
                    f"Arithmetic operations require numeric types (int, float), except '+' which also supports string concatenation.",
                )
            )
            return "int"

        # Relational
        if op in ("<", "<=", ">", ">="):
            if left_type in ("int", "float") and right_type in ("int", "float"):
                return "bool"
            self.errors.append(
                SemanticError(
                    f"Comparison operator '{op}' cannot compare types '{left_type}' and '{right_type}'",
                    node.line,
                    node.column,
                    "Comparison operators are only valid between numeric types.",
                )
            )
            return "bool"

        # Equality
        if op in ("==", "!="):
            if self._is_type_compatible(left_type, right_type) or self._is_type_compatible(right_type, left_type):
                return "bool"
            self.errors.append(
                SemanticError(
                    f"Equality operator '{op}' cannot compare incompatible types '{left_type}' and '{right_type}'",
                    node.line,
                    node.column,
                    "Values compared for equality should be of compatible types.",
                )
            )
            return "bool"

        # Logical
        if op in ("&&", "||"):
            if left_type in ("bool", "int") and right_type in ("bool", "int"):
                return "bool"
            self.errors.append(
                SemanticError(
                    f"Logical operator '{op}' requires boolean operands, got '{left_type}' and '{right_type}'",
                    node.line,
                    node.column,
                    "Logical operators '&&' and '||' expect boolean values.",
                )
            )
            return "bool"

        return None

    def _visit_unary_expr(self, node: UnaryExpr) -> Optional[str]:
        operand_type = self._visit(node.operand)
        if not operand_type:
            return None

        if node.operator == "-":
            if operand_type in ("int", "float"):
                return operand_type
            self.errors.append(
                SemanticError(
                    f"Unary negation '-' cannot be applied to type '{operand_type}'",
                    node.line,
                    node.column,
                    "Unary '-' is only valid for numeric types (int, float).",
                )
            )
            return operand_type

        if node.operator == "!":
            if operand_type in ("bool", "int"):
                return "bool"
            self.errors.append(
                SemanticError(
                    f"Logical NOT '!' cannot be applied to type '{operand_type}'",
                    node.line,
                    node.column,
                    "Logical NOT '!' requires a boolean or numeric condition.",
                )
            )
            return "bool"

        return operand_type

    def _visit_literal_expr(self, node: LiteralExpr) -> str:
        return node.data_type

    def _visit_variable_expr(self, node: VariableExpr) -> Optional[str]:
        symbol = self.symbol_manager.lookup(node.name)
        if not symbol:
            self.errors.append(
                SemanticError(
                    f"Undeclared variable '{node.name}'",
                    node.line,
                    node.column,
                    f"Variable '{node.name}' was referenced before declaration.",
                )
            )
            return None
        return symbol.type_name

    def _visit_block(self, node: Block) -> None:
        self.symbol_manager.enter_scope()
        for stmt in node.statements:
            self._visit(stmt)
        self.symbol_manager.exit_scope()

    def _visit_if_stmt(self, node: IfStmt) -> None:
        cond_type = self._visit(node.condition)
        if cond_type and cond_type not in ("bool", "int"):
            self.errors.append(
                SemanticError(
                    f"If condition must evaluate to a boolean or integer, got '{cond_type}'",
                    node.line,
                    node.column,
                    "Branch conditions must be truthy/falsy expressions.",
                )
            )
        self._visit(node.then_branch)
        if node.else_branch:
            self._visit(node.else_branch)

    def _visit_while_stmt(self, node: WhileStmt) -> None:
        cond_type = self._visit(node.condition)
        if cond_type and cond_type not in ("bool", "int"):
            self.errors.append(
                SemanticError(
                    f"While condition must evaluate to a boolean or integer, got '{cond_type}'",
                    node.line,
                    node.column,
                    "Loop conditions must be truthy/falsy expressions.",
                )
            )
        self._visit(node.body)

    def _visit_for_stmt(self, node: ForStmt) -> None:
        self.symbol_manager.enter_scope()
        if node.initializer:
            self._visit(node.initializer)
        if node.condition:
            cond_type = self._visit(node.condition)
            if cond_type and cond_type not in ("bool", "int"):
                self.errors.append(
                    SemanticError(
                        f"For loop condition must evaluate to a boolean or integer, got '{cond_type}'",
                        node.line,
                        node.column,
                        "Loop conditions must be truthy/falsy expressions.",
                    )
                )
        if node.increment:
            self._visit(node.increment)
        self._visit(node.body)
        self.symbol_manager.exit_scope()

    def _visit_print_stmt(self, node: PrintStmt) -> None:
        self._visit(node.expression)

    def _visit_return_stmt(self, node: ReturnStmt) -> None:
        if node.expression:
            self._visit(node.expression)

    def _is_type_compatible(self, target_type: str, source_type: str) -> bool:
        if target_type == source_type:
            return True
        # Allow int to float promotion
        if target_type == "float" and source_type == "int":
            return True
        # Allow int and bool interchangeability in basic C-like semantics if desired
        if target_type == "bool" and source_type == "int":
            return True
        if target_type == "int" and source_type == "bool":
            return True
        return False
