from typing import Optional, Dict, Any


class TargetInstruction:
    def __init__(
        self,
        op: str,
        arg1: Optional[str] = None,
        arg2: Optional[str] = None,
        comment: Optional[str] = None,
        source_line: int = 1,
        tac_index: Optional[int] = None,
        ast_node_id: Optional[int] = None,
        instruction_id: Optional[int] = None,
    ):
        self.instruction_id = instruction_id
        self.op = op.upper()
        self.arg1 = str(arg1) if arg1 is not None else None
        self.arg2 = str(arg2) if arg2 is not None else None
        self.comment = comment
        self.source_line = source_line
        self.tac_index = tac_index
        self.ast_node_id = ast_node_id

    def __str__(self) -> str:
        if self.op == "LABEL":
            return f"{self.arg1}:"
        elif self.arg2 is not None:
            text = f"{self.op:<6} {self.arg1}, {self.arg2}"
        elif self.arg1 is not None:
            text = f"{self.op:<6} {self.arg1}"
        else:
            text = f"{self.op}"

        if self.comment:
            text = f"{text:<26} ; {self.comment}"
        return text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.instruction_id,
            "instructionId": self.instruction_id,
            "op": self.op,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "comment": self.comment,
            "text": str(self),
            "sourceLine": self.source_line,
            "tacIndex": self.tac_index,
            "astNodeId": self.ast_node_id,
        }
