from typing import List, Optional, Any, Dict

_node_counter = 0

def get_next_node_id() -> int:
    global _node_counter
    _node_counter += 1
    return _node_counter

def reset_node_counter():
    global _node_counter
    _node_counter = 0


class ASTNode:
    def __init__(self, line: int = 1, column: int = 1):
        self.node_id: int = get_next_node_id()
        self.line: int = line
        self.column: int = column

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError


class Program(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "Program",
            "label": "Program",
            "line": self.line,
            "column": self.column,
            "children": [stmt.to_dict() for stmt in self.statements],
        }


class VarDecl(ASTNode):
    def __init__(
        self,
        var_type: str,
        name: str,
        initializer: Optional[ASTNode] = None,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer

    def to_dict(self) -> Dict[str, Any]:
        children = []
        if self.initializer:
            children.append(self.initializer.to_dict())
        return {
            "id": self.node_id,
            "type": "VarDecl",
            "label": f"VarDecl: {self.var_type} {self.name}",
            "varType": self.var_type,
            "name": self.name,
            "hasInitializer": self.initializer is not None,
            "line": self.line,
            "column": self.column,
            "children": children,
        }


class Assignment(ASTNode):
    def __init__(
        self,
        name: str,
        operator: str,
        value: ASTNode,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.name = name
        self.operator = operator
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "Assignment",
            "label": f"Assign: {self.name} {self.operator}",
            "name": self.name,
            "operator": self.operator,
            "line": self.line,
            "column": self.column,
            "children": [self.value.to_dict()],
        }


class BinaryExpr(ASTNode):
    def __init__(
        self,
        left: ASTNode,
        operator: str,
        right: ASTNode,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "BinaryExpr",
            "label": f"BinaryOp: {self.operator}",
            "operator": self.operator,
            "line": self.line,
            "column": self.column,
            "children": [self.left.to_dict(), self.right.to_dict()],
        }


class UnaryExpr(ASTNode):
    def __init__(
        self,
        operator: str,
        operand: ASTNode,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "UnaryExpr",
            "label": f"UnaryOp: {self.operator}",
            "operator": self.operator,
            "line": self.line,
            "column": self.column,
            "children": [self.operand.to_dict()],
        }


class LiteralExpr(ASTNode):
    def __init__(
        self,
        value: Any,
        data_type: str,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.value = value
        self.data_type = data_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "LiteralExpr",
            "label": f"Literal: {self.value} ({self.data_type})",
            "value": self.value,
            "dataType": self.data_type,
            "line": self.line,
            "column": self.column,
            "children": [],
        }


class VariableExpr(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "VariableExpr",
            "label": f"Variable: {self.name}",
            "name": self.name,
            "line": self.line,
            "column": self.column,
            "children": [],
        }


class Block(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.statements = statements

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "Block",
            "label": f"Block ({len(self.statements)} stmts)",
            "line": self.line,
            "column": self.column,
            "children": [stmt.to_dict() for stmt in self.statements],
        }


class IfStmt(ASTNode):
    def __init__(
        self,
        condition: ASTNode,
        then_branch: ASTNode,
        else_branch: Optional[ASTNode] = None,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def to_dict(self) -> Dict[str, Any]:
        children = [
            {"label": "Condition", "children": [self.condition.to_dict()]},
            {"label": "Then", "children": [self.then_branch.to_dict()]},
        ]
        if self.else_branch:
            children.append({"label": "Else", "children": [self.else_branch.to_dict()]})
        return {
            "id": self.node_id,
            "type": "IfStmt",
            "label": "IfStmt",
            "line": self.line,
            "column": self.column,
            "children": children,
        }


class WhileStmt(ASTNode):
    def __init__(
        self,
        condition: ASTNode,
        body: ASTNode,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "WhileStmt",
            "label": "WhileStmt",
            "line": self.line,
            "column": self.column,
            "children": [
                {"label": "Condition", "children": [self.condition.to_dict()]},
                {"label": "Body", "children": [self.body.to_dict()]},
            ],
        }


class PrintStmt(ASTNode):
    def __init__(self, expression: ASTNode, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expression = expression

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": "PrintStmt",
            "label": "PrintStmt",
            "line": self.line,
            "column": self.column,
            "children": [self.expression.to_dict()],
        }


class ReturnStmt(ASTNode):
    def __init__(self, expression: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.expression = expression

    def to_dict(self) -> Dict[str, Any]:
        children = [self.expression.to_dict()] if self.expression else []
        return {
            "id": self.node_id,
            "type": "ReturnStmt",
            "label": "ReturnStmt",
            "line": self.line,
            "column": self.column,
            "children": children,
        }


class ForStmt(ASTNode):
    def __init__(
        self,
        initializer: Optional[ASTNode],
        condition: Optional[ASTNode],
        increment: Optional[ASTNode],
        body: ASTNode,
        line: int = 1,
        column: int = 1,
    ):
        super().__init__(line, column)
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

    def to_dict(self) -> Dict[str, Any]:
        children = []
        if self.initializer:
            children.append({"label": "Init", "children": [self.initializer.to_dict()]})
        if self.condition:
            children.append({"label": "Condition", "children": [self.condition.to_dict()]})
        if self.increment:
            children.append({"label": "Increment", "children": [self.increment.to_dict()]})
        children.append({"label": "Body", "children": [self.body.to_dict()]})

        return {
            "id": self.node_id,
            "type": "ForStmt",
            "label": "ForStmt",
            "line": self.line,
            "column": self.column,
            "children": children,
        }
