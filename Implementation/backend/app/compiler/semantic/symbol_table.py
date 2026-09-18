from typing import Dict, Optional, List, Any


class Symbol:
    def __init__(
        self,
        name: str,
        type_name: str,
        scope_level: int,
        line: int,
        column: int,
        is_initialized: bool = False,
        value: Any = None,
    ):
        self.name = name
        self.type_name = type_name
        self.scope_level = scope_level
        self.line = line
        self.column = column
        self.is_initialized = is_initialized
        self.value = value

    def to_dict(self) -> dict:
        scope_name = "Global" if self.scope_level == 0 else f"Local (Level {self.scope_level})"
        return {
            "name": self.name,
            "type": self.type_name,
            "scope": scope_name,
            "scopeLevel": self.scope_level,
            "line": self.line,
            "column": self.column,
            "isInitialized": self.is_initialized,
            "value": str(self.value) if self.value is not None else "uninitialized",
        }


class Scope:
    def __init__(self, level: int, parent: Optional["Scope"] = None):
        self.level = level
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def lookup_current(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)


class SymbolTableManager:
    def __init__(self):
        self.global_scope = Scope(level=0)
        self.current_scope = self.global_scope
        self.all_symbols: List[Symbol] = []

    def enter_scope(self) -> Scope:
        new_scope = Scope(level=self.current_scope.level + 1, parent=self.current_scope)
        self.current_scope = new_scope
        return new_scope

    def exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

    def define(self, symbol: Symbol) -> bool:
        success = self.current_scope.define(symbol)
        if success:
            self.all_symbols.append(symbol)
        return success

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.current_scope.lookup(name)

    def lookup_current(self, name: str) -> Optional[Symbol]:
        return self.current_scope.lookup_current(name)

    def get_all_records(self) -> List[dict]:
        return [sym.to_dict() for sym in self.all_symbols]
