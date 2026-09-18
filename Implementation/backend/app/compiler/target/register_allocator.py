from typing import Dict, List, Optional


class RegisterAllocator:
    def __init__(self, num_registers: int = 8):
        self.num_registers = num_registers
        self.registers = [f"R{i}" for i in range(num_registers)]
        # Map register name -> variable currently holding
        self.reg_to_var: Dict[str, Optional[str]] = {r: None for r in self.registers}
        # Map variable -> register
        self.var_to_reg: Dict[str, str] = {}
        # Usage queue for FIFO / LRU replacement
        self.allocation_order: List[str] = []

    def get_register_for(self, var_name: str) -> str:
        # If already assigned, return it
        if var_name in self.var_to_reg:
            reg = self.var_to_reg[var_name]
            # Refresh order
            if reg in self.allocation_order:
                self.allocation_order.remove(reg)
            self.allocation_order.append(reg)
            return reg

        # Find a free register
        for reg in self.registers:
            if self.reg_to_var[reg] is None:
                self._bind(reg, var_name)
                return reg

        # If none free, spill oldest
        oldest_reg = self.allocation_order[0]
        self._unbind(oldest_reg)
        self._bind(oldest_reg, var_name)
        return oldest_reg

    def allocate_scratch(self, prefer_free: bool = True) -> str:
        for reg in reversed(self.registers):
            if self.reg_to_var[reg] is None:
                return reg
        return self.registers[0]

    def _bind(self, reg: str, var_name: str):
        self.reg_to_var[reg] = var_name
        self.var_to_reg[var_name] = reg
        if reg in self.allocation_order:
            self.allocation_order.remove(reg)
        self.allocation_order.append(reg)

    def _unbind(self, reg: str):
        old_var = self.reg_to_var[reg]
        if old_var and old_var in self.var_to_reg:
            del self.var_to_reg[old_var]
        self.reg_to_var[reg] = None
        if reg in self.allocation_order:
            self.allocation_order.remove(reg)

    def clear(self):
        self.reg_to_var = {r: None for r in self.registers}
        self.var_to_reg.clear()
        self.allocation_order.clear()
