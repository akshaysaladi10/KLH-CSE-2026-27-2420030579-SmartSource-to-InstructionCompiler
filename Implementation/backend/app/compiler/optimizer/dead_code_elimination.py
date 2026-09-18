from typing import List, Tuple, Dict, Any, Set
from ..intermediate.tac import TACInstruction


class DeadCodeEliminationPass:
    def run(self, instructions: List[TACInstruction]) -> Tuple[List[TACInstruction], List[Dict[str, Any]]]:
        changes: List[Dict[str, Any]] = []

        # Pass 1: Remove unreachable code after unconditional goto / return
        reachable_instructions: List[TACInstruction] = []
        is_reachable = True

        for instr in instructions:
            if instr.op == "label":
                is_reachable = True
                reachable_instructions.append(instr)
                continue

            if not is_reachable:
                changes.append({
                    "pass": "Dead Code Elimination",
                    "description": f"Removed unreachable instruction after unconditional branch/return",
                    "before": str(instr),
                    "after": "(removed)",
                    "line": instr.line,
                })
                continue

            reachable_instructions.append(instr)

            if instr.op in ("goto", "return"):
                is_reachable = False

        # Pass 2: Remove unused temporary variable assignments
        # Count usage of variables
        used_vars: Set[str] = set()
        for instr in reachable_instructions:
            if instr.arg1:
                used_vars.add(instr.arg1)
            if instr.arg2:
                used_vars.add(instr.arg2)

        final_instructions: List[TACInstruction] = []
        for instr in reachable_instructions:
            # If instruction defines a temporary tN, and tN is never used, remove it
            if instr.result and instr.result.startswith("t") and instr.result not in used_vars:
                # Don't eliminate if operation has side effect (none of our arithmetic/logic ops do, but print/call would)
                if instr.op not in ("print", "call"):
                    changes.append({
                        "pass": "Dead Code Elimination",
                        "description": f"Removed unused temporary assignment '{str(instr)}'",
                        "before": str(instr),
                        "after": "(removed)",
                        "line": instr.line,
                    })
                    continue

            # Check self-assignment `x = x`
            if instr.op == "=" and instr.result == instr.arg1:
                changes.append({
                    "pass": "Dead Code Elimination",
                    "description": f"Removed redundant self-assignment '{str(instr)}'",
                    "before": str(instr),
                    "after": "(removed)",
                    "line": instr.line,
                })
                continue

            final_instructions.append(instr)

        return final_instructions, changes
