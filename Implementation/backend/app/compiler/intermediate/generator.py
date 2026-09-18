from typing import List, Optional
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
from .tac import TACInstruction


class TACGenerator:
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self, program: Program) -> List[TACInstruction]:
        self.instructions.clear()
        self.temp_count = 0
        self.label_count = 0

        for stmt in program.statements:
            self._visit(stmt)

        return self.instructions

    def _new_temp(self) -> str:
        name = f"t{self.temp_count}"
        self.temp_count += 1
        return name

    def _new_label(self) -> str:
        name = f"L{self.label_count}"
        self.label_count += 1
        return name

    def _emit(
        self,
        op: str,
        arg1: Optional[str] = None,
        arg2: Optional[str] = None,
        result: Optional[str] = None,
        line: int = 1,
        ast_node_id: Optional[int] = None,
    ) -> TACInstruction:
        instr = TACInstruction(op, arg1, arg2, result, line, ast_node_id)
        self.instructions.append(instr)
        return instr

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
        if node.initializer:
            val_operand = self._visit(node.initializer)
            self._emit("=", arg1=val_operand, result=node.name, line=node.line, ast_node_id=node.node_id)
        else:
            self._emit("decl", result=node.name, line=node.line, ast_node_id=node.node_id)
        return node.name

    def _visit_assignment(self, node: Assignment) -> Optional[str]:
        val_operand = self._visit(node.value)
        self._emit("=", arg1=val_operand, result=node.name, line=node.line, ast_node_id=node.node_id)
        return node.name

    def _visit_binary_expr(self, node: BinaryExpr) -> str:
        left_operand = self._visit(node.left)
        right_operand = self._visit(node.right)
        temp = self._new_temp()
        self._emit(
            op=node.operator,
            arg1=left_operand,
            arg2=right_operand,
            result=temp,
            line=node.line,
            ast_node_id=node.node_id,
        )
        return temp

    def _visit_unary_expr(self, node: UnaryExpr) -> str:
        operand = self._visit(node.operand)
        temp = self._new_temp()
        op_code = "neg" if node.operator == "-" else "!"
        self._emit(
            op=op_code,
            arg1=operand,
            result=temp,
            line=node.line,
            ast_node_id=node.node_id,
        )
        return temp

    def _visit_literal_expr(self, node: LiteralExpr) -> str:
        if node.data_type == "bool":
            return "true" if node.value else "false"
        elif node.data_type == "string":
            return f'"{node.value}"'
        return str(node.value)

    def _visit_variable_expr(self, node: VariableExpr) -> str:
        return node.name

    def _visit_block(self, node: Block) -> None:
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_if_stmt(self, node: IfStmt) -> None:
        cond_operand = self._visit(node.condition)
        label_else = self._new_label()
        label_exit = self._new_label()

        if node.else_branch:
            self._emit("ifFalse", arg1=cond_operand, result=label_else, line=node.line, ast_node_id=node.node_id)
            self._visit(node.then_branch)
            self._emit("goto", result=label_exit, line=node.line, ast_node_id=node.node_id)
            self._emit("label", result=label_else, line=node.else_branch.line, ast_node_id=node.else_branch.node_id)
            self._visit(node.else_branch)
            self._emit("label", result=label_exit, line=node.line, ast_node_id=node.node_id)
        else:
            self._emit("ifFalse", arg1=cond_operand, result=label_exit, line=node.line, ast_node_id=node.node_id)
            self._visit(node.then_branch)
            self._emit("label", result=label_exit, line=node.line, ast_node_id=node.node_id)

    def _visit_while_stmt(self, node: WhileStmt) -> None:
        label_start = self._new_label()
        label_exit = self._new_label()

        self._emit("label", result=label_start, line=node.line, ast_node_id=node.node_id)
        cond_operand = self._visit(node.condition)
        self._emit("ifFalse", arg1=cond_operand, result=label_exit, line=node.line, ast_node_id=node.node_id)
        self._visit(node.body)
        self._emit("goto", result=label_start, line=node.line, ast_node_id=node.node_id)
        self._emit("label", result=label_exit, line=node.line, ast_node_id=node.node_id)

    def _visit_for_stmt(self, node: ForStmt) -> None:
        if node.initializer:
            self._visit(node.initializer)

        label_start = self._new_label()
        label_exit = self._new_label()

        self._emit("label", result=label_start, line=node.line, ast_node_id=node.node_id)
        if node.condition:
            cond_operand = self._visit(node.condition)
            self._emit("ifFalse", arg1=cond_operand, result=label_exit, line=node.line, ast_node_id=node.node_id)

        self._visit(node.body)

        if node.increment:
            self._visit(node.increment)

        self._emit("goto", result=label_start, line=node.line, ast_node_id=node.node_id)
        self._emit("label", result=label_exit, line=node.line, ast_node_id=node.node_id)

    def _visit_print_stmt(self, node: PrintStmt) -> None:
        val_operand = self._visit(node.expression)
        self._emit("print", arg1=val_operand, line=node.line, ast_node_id=node.node_id)

    def _visit_return_stmt(self, node: ReturnStmt) -> None:
        val_operand = self._visit(node.expression) if node.expression else None
        self._emit("return", arg1=val_operand, line=node.line, ast_node_id=node.node_id)
