from .instructions import TargetInstruction
from .register_allocator import RegisterAllocator
from .codegen import TargetCodeGenerator
from .simulator import TargetVMSimulator

__all__ = [
    "TargetInstruction",
    "RegisterAllocator",
    "TargetCodeGenerator",
    "TargetVMSimulator",
]
