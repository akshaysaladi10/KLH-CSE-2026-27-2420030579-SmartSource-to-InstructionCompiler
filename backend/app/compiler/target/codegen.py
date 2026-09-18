from typing import List, Optional
from ..intermediate.tac import TACInstruction
from .instructions import TargetInstruction
from .register_allocator import RegisterAllocator


class TargetCodeGenerator:
    def __init__(self):
        self.instructions: List[TargetInstruction] = []
        self.allocator = RegisterAllocator(num_registers=8)

    def generate(self, tac_list: List[TACInstruction]) -> List[TargetInstruction]:
        self.instructions.clear()
        self.allocator.clear()

        for idx, tac in enumerate(tac_list):
            self._translate_tac(tac, idx)

        # End program with HALT
        last_line = tac_list[-1].line if tac_list else 1
        self._emit("HALT", comment="End of program execution", source_line=last_line)
        return self.instructions

    def _emit(
        self,
        op: str,
        arg1: Optional[str] = None,
        arg2: Optional[str] = None,
        comment: Optional[str] = None,
        source_line: int = 1,
        tac_index: Optional[int] = None,
        ast_node_id: Optional[int] = None,
    ) -> TargetInstruction:
        instr_id = len(self.instructions)
        instr = TargetInstruction(op, arg1, arg2, comment, source_line, tac_index, ast_node_id, instruction_id=instr_id)
        self.instructions.append(instr)
        return instr

    def _translate_tac(self, tac: TACInstruction, tac_index: int):
        line = tac.line
        node_id = tac.ast_node_id
        op = tac.op

        if op == "label":
            self._emit("LABEL", arg1=tac.result, comment=f"Label {tac.result}", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op == "goto":
            self._emit("JMP", arg1=tac.result, comment=f"Jump to {tac.result}", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op == "ifFalse":
            reg = self.allocator.get_register_for(tac.arg1)
            self._emit("LOAD", reg, tac.arg1, comment=f"Load condition '{tac.arg1}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("CMP", reg, "0", comment="Compare condition with false (0)", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("JZ", tac.result, comment=f"Jump if zero/false to {tac.result}", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op == "ifTrue":
            reg = self.allocator.get_register_for(tac.arg1)
            self._emit("LOAD", reg, tac.arg1, comment=f"Load condition '{tac.arg1}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("CMP", reg, "0", comment="Compare condition with 0", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("JNZ", tac.result, comment=f"Jump if non-zero/true to {tac.result}", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op == "=":
            # Simple assignment: result = arg1
            reg = self.allocator.get_register_for(tac.result)
            self._emit("LOAD", reg, tac.arg1, comment=f"Load value '{tac.arg1}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("STORE", tac.result, reg, comment=f"Store to '{tac.result}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op in ("+", "-", "*", "/", "%"):
            r_dest = self.allocator.get_register_for(tac.result)
            self._emit("LOAD", r_dest, tac.arg1, comment=f"Load '{tac.arg1}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)

            op_map = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}
            asm_op = op_map[op]
            self._emit(asm_op, r_dest, tac.arg2, comment=f"Compute {tac.result} = {tac.arg1} {op} {tac.arg2}", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("STORE", tac.result, r_dest, comment=f"Save result to '{tac.result}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op in ("==", "!=", "<", "<=", ">", ">="):
            r_dest = self.allocator.get_register_for(tac.result)
            self._emit("LOAD", r_dest, tac.arg1, comment=f"Load lhs '{tac.arg1}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("CMP", r_dest, tac.arg2, comment=f"Compare with rhs '{tac.arg2}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)

            # Convert comparison result to 1 or 0
            # For simplicity in target ISA, we use conditional set or simple opcode
            cond_map = {
                "==": "SETEQ",
                "!=": "SETNE",
                "<": "SETLT",
                "<=": "SETLE",
                ">": "SETGT",
                ">=": "SETGE",
            }
            self._emit(cond_map[op], r_dest, comment=f"Set {r_dest} to 1 if {op} is true, else 0", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("STORE", tac.result, r_dest, comment=f"Store boolean result in '{tac.result}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op in ("neg", "!"):
            r_dest = self.allocator.get_register_for(tac.result)
            self._emit("LOAD", r_dest, tac.arg1, comment=f"Load operand '{tac.arg1}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            asm_op = "NEG" if op == "neg" else "NOT"
            self._emit(asm_op, r_dest, comment=f"Apply {op}", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("STORE", tac.result, r_dest, comment=f"Store to '{tac.result}'", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op == "print":
            r_out = "R0"
            self._emit("LOAD", r_out, tac.arg1, comment=f"Load '{tac.arg1}' for output", source_line=line, tac_index=tac_index, ast_node_id=node_id)
            self._emit("PRINT", r_out, comment="Print value to standard output", source_line=line, tac_index=tac_index, ast_node_id=node_id)

        elif op == "decl":
            # No-op in assembly, placeholder allocation
            pass
