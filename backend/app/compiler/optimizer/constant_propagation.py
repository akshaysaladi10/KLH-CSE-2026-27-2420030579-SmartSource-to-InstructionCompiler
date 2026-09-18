from typing import List, Tuple, Dict, Any, Optional
from ..intermediate.tac import TACInstruction


def is_literal(val: Optional[str]) -> bool:
    if val is None:
        return False
    if val in ("true", "false"):
        return True
    if val.startswith('"') and val.endswith('"'):
        return True
    try:
        float(val)
        return True
    except ValueError:
        return False


class ConstantPropagationPass:
    def run(self, instructions: List[TACInstruction]) -> Tuple[List[TACInstruction], List[Dict[str, Any]]]:
        optimized: List[TACInstruction] = []
        changes: List[Dict[str, Any]] = []
        constants: Dict[str, str] = {}

        for instr in instructions:
            # Control flow boundary: reset constant mapping to preserve branch/loop correctness
            if instr.op in ("label", "goto", "ifFalse", "ifTrue"):
                constants.clear()
                optimized.append(instr)
                continue

            new_arg1 = instr.arg1
            new_arg2 = instr.arg2
            modified = False

            if instr.arg1 and instr.arg1 in constants:
                new_arg1 = constants[instr.arg1]
                modified = True

            if instr.arg2 and instr.arg2 in constants:
                new_arg2 = constants[instr.arg2]
                modified = True

            current_instr = instr
            if modified:
                current_instr = TACInstruction(
                    op=instr.op,
                    arg1=new_arg1,
                    arg2=new_arg2,
                    result=instr.result,
                    line=instr.line,
                    ast_node_id=instr.ast_node_id,
                )
                changes.append({
                    "pass": "Constant Propagation",
                    "description": f"Propagated constant value into instruction operands",
                    "before": str(instr),
                    "after": str(current_instr),
                    "line": instr.line,
                })

            # Check if this instruction assigns a constant
            if current_instr.op == "=" and current_instr.result:
                if is_literal(current_instr.arg1):
                    constants[current_instr.result] = current_instr.arg1
                else:
                    # Invalidated
                    constants.pop(current_instr.result, None)
            elif current_instr.result:
                # Any other assignment to result invalidates previous constant value
                constants.pop(current_instr.result, None)

            optimized.append(current_instr)

        return optimized, changes
