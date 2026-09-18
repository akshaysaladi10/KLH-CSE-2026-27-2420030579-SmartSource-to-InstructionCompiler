from typing import List, Tuple, Dict, Any, Optional
from ..intermediate.tac import TACInstruction


def is_number(val: Optional[str]) -> bool:
    if val is None:
        return False
    try:
        int(val)
        return True
    except ValueError:
        try:
            float(val)
            return True
        except ValueError:
            return False


def parse_val(val: str) -> Any:
    if val == "true":
        return True
    if val == "false":
        return False
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def format_val(val: Any) -> str:
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, float):
        # Format cleanly (e.g. 5.0 -> 5.0, not 5.000000000000001 if round)
        return f"{val:.4f}".rstrip("0").rstrip(".") if "." in f"{val:.4f}" else str(val)
    return str(val)


class ConstantFoldingPass:
    def run(self, instructions: List[TACInstruction]) -> Tuple[List[TACInstruction], List[Dict[str, Any]]]:
        optimized: List[TACInstruction] = []
        changes: List[Dict[str, Any]] = []

        for instr in instructions:
            if instr.op in ("+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">=", "&&", "||"):
                if is_number(instr.arg1) and is_number(instr.arg2):
                    v1 = parse_val(instr.arg1)
                    v2 = parse_val(instr.arg2)
                    res = None
                    try:
                        if instr.op == "+":
                            res = v1 + v2
                        elif instr.op == "-":
                            res = v1 - v2
                        elif instr.op == "*":
                            res = v1 * v2
                        elif instr.op == "/":
                            if v2 != 0:
                                res = v1 // v2 if isinstance(v1, int) and isinstance(v2, int) else v1 / v2
                        elif instr.op == "%":
                            if v2 != 0:
                                res = v1 % v2
                        elif instr.op == "==":
                            res = v1 == v2
                        elif instr.op == "!=":
                            res = v1 != v2
                        elif instr.op == "<":
                            res = v1 < v2
                        elif instr.op == "<=":
                            res = v1 <= v2
                        elif instr.op == ">":
                            res = v1 > v2
                        elif instr.op == ">=":
                            res = v1 >= v2
                    except Exception:
                        res = None

                    if res is not None:
                        new_instr = TACInstruction(
                            op="=",
                            arg1=format_val(res),
                            result=instr.result,
                            line=instr.line,
                            ast_node_id=instr.ast_node_id,
                        )
                        changes.append({
                            "pass": "Constant Folding",
                            "description": f"Folded constant expression '{instr.arg1} {instr.op} {instr.arg2}' into '{format_val(res)}'",
                            "before": str(instr),
                            "after": str(new_instr),
                            "line": instr.line,
                        })
                        optimized.append(new_instr)
                        continue

            elif instr.op in ("!", "neg"):
                if is_number(instr.arg1):
                    v = parse_val(instr.arg1)
                    res = None
                    if instr.op == "neg":
                        res = -v
                    elif instr.op == "!":
                        res = not bool(v)
                    if res is not None:
                        new_instr = TACInstruction(
                            op="=",
                            arg1=format_val(res),
                            result=instr.result,
                            line=instr.line,
                            ast_node_id=instr.ast_node_id,
                        )
                        changes.append({
                            "pass": "Constant Folding",
                            "description": f"Folded unary operation '{instr.op} {instr.arg1}' into '{format_val(res)}'",
                            "before": str(instr),
                            "after": str(new_instr),
                            "line": instr.line,
                        })
                        optimized.append(new_instr)
                        continue

            optimized.append(instr)

        return optimized, changes
