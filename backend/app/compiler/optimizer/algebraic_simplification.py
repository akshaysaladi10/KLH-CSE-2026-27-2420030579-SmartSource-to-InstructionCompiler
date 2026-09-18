from typing import List, Tuple, Dict, Any
from ..intermediate.tac import TACInstruction


class AlgebraicSimplificationPass:
    def run(self, instructions: List[TACInstruction]) -> Tuple[List[TACInstruction], List[Dict[str, Any]]]:
        optimized: List[TACInstruction] = []
        changes: List[Dict[str, Any]] = []

        for instr in instructions:
            op = instr.op
            arg1 = instr.arg1
            arg2 = instr.arg2
            res = instr.result
            simplified_to = None

            if op == "+":
                if arg1 == "0":
                    simplified_to = arg2
                elif arg2 == "0":
                    simplified_to = arg1
            elif op == "-":
                if arg2 == "0":
                    simplified_to = arg1
            elif op == "*":
                if arg1 == "0" or arg2 == "0":
                    simplified_to = "0"
                elif arg1 == "1":
                    simplified_to = arg2
                elif arg2 == "1":
                    simplified_to = arg1
            elif op == "/":
                if arg2 == "1":
                    simplified_to = arg1

            if simplified_to is not None:
                new_instr = TACInstruction(
                    op="=",
                    arg1=simplified_to,
                    result=res,
                    line=instr.line,
                    ast_node_id=instr.ast_node_id,
                )
                changes.append({
                    "pass": "Algebraic Simplification",
                    "description": f"Simplified '{arg1} {op} {arg2}' algebraically to '{simplified_to}'",
                    "before": str(instr),
                    "after": str(new_instr),
                    "line": instr.line,
                })
                optimized.append(new_instr)
            else:
                optimized.append(instr)

        return optimized, changes
