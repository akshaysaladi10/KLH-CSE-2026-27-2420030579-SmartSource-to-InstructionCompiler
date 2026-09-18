from typing import List, Dict, Any, Optional
from ..parser.ast_nodes import Program, ASTNode
from ..intermediate.tac import TACInstruction
from ..target.instructions import TargetInstruction


class SourceToInstructionTracer:
    def build_trace(
        self,
        source_code: str,
        ast_program: Optional[Program],
        tac_list: List[TACInstruction],
        optimized_tac: List[TACInstruction],
        target_instructions: List[TargetInstruction],
    ) -> List[Dict[str, Any]]:
        source_lines = source_code.splitlines()

        # Group AST nodes by line
        ast_by_line: Dict[int, List[Dict[str, Any]]] = {}
        if ast_program:
            self._collect_ast_nodes(ast_program, ast_by_line)

        # Group TAC by line
        tac_by_line: Dict[int, List[Dict[str, Any]]] = {}
        for idx, tac in enumerate(tac_list):
            tac_by_line.setdefault(tac.line, []).append({
                "index": idx,
                "text": str(tac),
                "op": tac.op,
                "result": tac.result,
            })

        # Group Optimized TAC by line
        opt_by_line: Dict[int, List[Dict[str, Any]]] = {}
        for idx, tac in enumerate(optimized_tac):
            opt_by_line.setdefault(tac.line, []).append({
                "index": idx,
                "text": str(tac),
                "op": tac.op,
                "result": tac.result,
            })

        # Group Target Instructions by line
        target_by_line: Dict[int, List[Dict[str, Any]]] = {}
        for idx, instr in enumerate(target_instructions):
            target_by_line.setdefault(instr.source_line, []).append({
                "index": idx,
                "text": str(instr),
                "op": instr.op,
                "comment": instr.comment,
            })

        trace_matrix: List[Dict[str, Any]] = []

        for line_no, raw_line in enumerate(source_lines, start=1):
            line_str = raw_line.strip()
            # Include lines that have code or associated compiler artifacts
            has_artifacts = (
                line_no in ast_by_line or
                line_no in tac_by_line or
                line_no in opt_by_line or
                line_no in target_by_line
            )
            if not line_str and not has_artifacts:
                continue

            trace_matrix.append({
                "sourceLine": line_no,
                "sourceCode": line_str,
                "astNodes": ast_by_line.get(line_no, []),
                "tacInstructions": tac_by_line.get(line_no, []),
                "optimizedTac": opt_by_line.get(line_no, []),
                "targetInstructions": target_by_line.get(line_no, []),
            })

        return trace_matrix

    def _collect_ast_nodes(self, node: ASTNode, ast_by_line: Dict[int, List[Dict[str, Any]]]):
        if hasattr(node, "line") and hasattr(node, "node_id"):
            node_dict = node.to_dict()
            label = node_dict.get("label", node_dict.get("type", "Node"))
            ast_by_line.setdefault(node.line, []).append({
                "id": node.node_id,
                "type": node_dict.get("type", "Node"),
                "label": label,
            })

        # Recurse children if any
        if hasattr(node, "statements"):
            for s in node.statements:
                self._collect_ast_nodes(s, ast_by_line)
        elif hasattr(node, "children"):
            # Check if children are ASTNodes
            for c in getattr(node, "children", []):
                if isinstance(c, ASTNode):
                    self._collect_ast_nodes(c, ast_by_line)
        else:
            # Check known sub-fields
            for field_name in ("initializer", "value", "left", "right", "operand", "condition", "then_branch", "else_branch", "body", "expression"):
                field_val = getattr(node, field_name, None)
                if isinstance(field_val, ASTNode):
                    self._collect_ast_nodes(field_val, ast_by_line)
