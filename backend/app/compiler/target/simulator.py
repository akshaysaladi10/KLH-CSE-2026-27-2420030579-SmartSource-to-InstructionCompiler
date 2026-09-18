from typing import List, Dict, Any, Tuple, Optional
from .instructions import TargetInstruction


def parse_literal(val_str: str) -> Any:
    if val_str == "true":
        return 1
    if val_str == "false":
        return 0
    if val_str.startswith('"') and val_str.endswith('"'):
        return val_str[1:-1]
    try:
        return int(val_str)
    except ValueError:
        try:
            return float(val_str)
        except ValueError:
            return val_str


class TargetVMSimulator:
    def __init__(self, max_cycles: int = 10000):
        self.max_cycles = max_cycles
        self.registers: Dict[str, Any] = {f"R{i}": 0 for i in range(8)}
        self.memory: Dict[str, Any] = {}
        self.flag_zero: bool = False
        self.flag_sign: bool = False
        self.flag_greater: bool = False
        self.flag_less: bool = False
        self.pc: int = 0
        self.output: List[str] = []
        self.step_history: List[Dict[str, Any]] = []

    def run(
        self,
        instructions: List[TargetInstruction],
        breakpoints: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.memory.clear()
        self.flag_zero = False
        self.flag_sign = False
        self.flag_greater = False
        self.flag_less = False
        self.pc = 0
        self.output.clear()
        self.step_history.clear()

        breakpoint_set = set(breakpoints or [])

        # Build label index map
        label_map: Dict[str, int] = {}
        for idx, instr in enumerate(instructions):
            if instr.op == "LABEL" and instr.arg1:
                label_map[instr.arg1] = idx

        cycle_count = 0
        halted = False
        hit_breakpoint = False
        breakpoint_pc = None

        while self.pc < len(instructions) and cycle_count < self.max_cycles:
            # Check breakpoint before executing instruction (if we've run at least 1 cycle)
            if cycle_count > 0 and self.pc in breakpoint_set:
                hit_breakpoint = True
                breakpoint_pc = self.pc
                break

            instr = instructions[self.pc]
            current_pc = self.pc
            self.pc += 1
            cycle_count += 1

            if instr.op == "HALT":
                halted = True
                self._record_step(current_pc, instr)
                break

            self._execute_instruction(instr, label_map)
            self._record_step(current_pc, instr)

        success = halted or (self.pc >= len(instructions)) or hit_breakpoint
        warning = None
        if cycle_count >= self.max_cycles:
            warning = f"Execution exceeded safety limit of {self.max_cycles} cycles (possible infinite loop)."

        return {
            "success": success,
            "cycles": cycle_count,
            "warning": warning,
            "hitBreakpoint": hit_breakpoint,
            "breakpointPC": breakpoint_pc,
            "output": self.output,
            "registers": dict(self.registers),
            "memory": dict(self.memory),
            "flags": {
                "zero": self.flag_zero,
                "sign": self.flag_sign,
                "greater": self.flag_greater,
                "less": self.flag_less,
            },
            "stepHistory": self.step_history,
        }

    def _record_step(self, pc: int, instr: TargetInstruction):
        if len(self.step_history) < 300:
            self.step_history.append({
                "step": len(self.step_history) + 1,
                "pc": pc,
                "instruction": str(instr),
                "op": instr.op,
                "registers": dict(self.registers),
                "memory": dict(self.memory),
                "flags": {
                    "zero": self.flag_zero,
                    "sign": self.flag_sign,
                    "greater": self.flag_greater,
                    "less": self.flag_less,
                },
                "output": list(self.output),
            })

    def _resolve(self, operand: str) -> Any:
        if operand in self.registers:
            return self.registers[operand]
        if operand in self.memory:
            return self.memory[operand]
        return parse_literal(operand)

    def _execute_instruction(self, instr: TargetInstruction, label_map: Dict[str, int]):
        op = instr.op
        arg1 = instr.arg1
        arg2 = instr.arg2

        if op == "LOAD":
            val = self._resolve(arg2)
            self.registers[arg1] = val

        elif op == "STORE":
            val = self._resolve(arg2)
            self.memory[arg1] = val

        elif op == "MOV":
            val = self._resolve(arg2)
            self.registers[arg1] = val

        elif op == "ADD":
            v1 = self.registers[arg1]
            v2 = self._resolve(arg2)
            if isinstance(v1, str) or isinstance(v2, str):
                self.registers[arg1] = str(v1) + str(v2)
            else:
                self.registers[arg1] = v1 + v2

        elif op == "SUB":
            v1 = self.registers[arg1]
            v2 = self._resolve(arg2)
            self.registers[arg1] = v1 - v2

        elif op == "MUL":
            v1 = self.registers[arg1]
            v2 = self._resolve(arg2)
            self.registers[arg1] = v1 * v2

        elif op == "DIV":
            v1 = self.registers[arg1]
            v2 = self._resolve(arg2)
            if v2 != 0:
                if isinstance(v1, int) and isinstance(v2, int):
                    self.registers[arg1] = v1 // v2
                else:
                    self.registers[arg1] = v1 / v2
            else:
                self.registers[arg1] = 0

        elif op == "MOD":
            v1 = self.registers[arg1]
            v2 = self._resolve(arg2)
            self.registers[arg1] = v1 % v2 if v2 != 0 else 0

        elif op == "CMP":
            v1 = self._resolve(arg1)
            v2 = self._resolve(arg2)
            try:
                self.flag_zero = (v1 == v2)
                self.flag_greater = (v1 > v2)
                self.flag_less = (v1 < v2)
                if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    self.flag_sign = (v1 - v2 < 0)
                else:
                    self.flag_sign = False
            except Exception:
                self.flag_zero = (v1 == v2)
                self.flag_greater = False
                self.flag_less = not (v1 == v2)
                self.flag_sign = False

        elif op in ("SETEQ", "SETZ"):
            self.registers[arg1] = 1 if self.flag_zero else 0

        elif op in ("SETNE", "SETNZ"):
            self.registers[arg1] = 1 if not self.flag_zero else 0

        elif op == "SETLT":
            self.registers[arg1] = 1 if self.flag_less else 0

        elif op == "SETLE":
            self.registers[arg1] = 1 if (self.flag_less or self.flag_zero) else 0

        elif op == "SETGT":
            self.registers[arg1] = 1 if self.flag_greater else 0

        elif op == "SETGE":
            self.registers[arg1] = 1 if (self.flag_greater or self.flag_zero) else 0

        elif op == "NEG":
            v = self.registers[arg1]
            self.registers[arg1] = -v

        elif op == "NOT":
            v = self.registers[arg1]
            self.registers[arg1] = 1 if not bool(v) else 0

        elif op == "JMP":
            if arg1 in label_map:
                self.pc = label_map[arg1]

        elif op in ("JZ", "JE"):
            if self.flag_zero and arg1 in label_map:
                self.pc = label_map[arg1]

        elif op in ("JNZ", "JNE"):
            if not self.flag_zero and arg1 in label_map:
                self.pc = label_map[arg1]

        elif op == "JL":
            if self.flag_less and arg1 in label_map:
                self.pc = label_map[arg1]

        elif op == "JG":
            if self.flag_greater and arg1 in label_map:
                self.pc = label_map[arg1]

        elif op == "JLE":
            if (self.flag_less or self.flag_zero) and arg1 in label_map:
                self.pc = label_map[arg1]

        elif op == "JGE":
            if (self.flag_greater or self.flag_zero) and arg1 in label_map:
                self.pc = label_map[arg1]

        elif op == "PRINT":
            v = self._resolve(arg1)
            self.output.append(str(v))

        elif op == "LABEL":
            pass
