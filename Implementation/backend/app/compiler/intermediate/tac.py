from typing import Optional, Dict, Any


class TACInstruction:
    def __init__(
        self,
        op: str,
        arg1: Optional[str] = None,
        arg2: Optional[str] = None,
        result: Optional[str] = None,
        line: int = 1,
        ast_node_id: Optional[int] = None,
    ):
        self.op = op
        self.arg1 = str(arg1) if arg1 is not None else None
        self.arg2 = str(arg2) if arg2 is not None else None
        self.result = str(result) if result is not None else None
        self.line = line
        self.ast_node_id = ast_node_id

    def __str__(self) -> str:
        if self.op == "label":
            return f"{self.result}:"
        elif self.op == "goto":
            return f"goto {self.result}"
        elif self.op == "ifFalse":
            return f"ifFalse {self.arg1} goto {self.result}"
        elif self.op == "ifTrue":
            return f"ifTrue {self.arg1} goto {self.result}"
        elif self.op == "=":
            return f"{self.result} = {self.arg1}"
        elif self.op in ("+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">=", "&&", "||"):
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        elif self.op in ("!", "neg"):
            prefix = "!" if self.op == "!" else "-"
            return f"{self.result} = {prefix}{self.arg1}"
        elif self.op == "print":
            return f"print {self.arg1}"
        elif self.op == "return":
            return f"return {self.arg1}" if self.arg1 else "return"
        elif self.op == "decl":
            return f"decl {self.result}"
        return f"{self.result} = {self.op} {self.arg1} {self.arg2}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "op": self.op,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "result": self.result,
            "text": str(self),
            "line": self.line,
            "astNodeId": self.ast_node_id,
        }
