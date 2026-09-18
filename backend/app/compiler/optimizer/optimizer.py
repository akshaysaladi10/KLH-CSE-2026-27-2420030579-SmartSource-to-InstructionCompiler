from typing import List, Dict, Any, Tuple, Optional
from ..intermediate.tac import TACInstruction
from .constant_folding import ConstantFoldingPass
from .constant_propagation import ConstantPropagationPass
from .algebraic_simplification import AlgebraicSimplificationPass
from .dead_code_elimination import DeadCodeEliminationPass


class OptimizerPipeline:
    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.pass_map = {
            "constant_propagation": ConstantPropagationPass(),
            "constant_folding": ConstantFoldingPass(),
            "algebraic_simplification": AlgebraicSimplificationPass(),
            "dead_code_elimination": DeadCodeEliminationPass(),
        }

    def optimize(
        self,
        instructions: List[TACInstruction],
        enabled_passes: Optional[List[str]] = None,
    ) -> Tuple[List[TACInstruction], List[Dict[str, Any]]]:
        current = list(instructions)
        all_changes: List[Dict[str, Any]] = []

        active_passes = []
        if enabled_passes is not None:
            for p_name in enabled_passes:
                if p_name in self.pass_map:
                    active_passes.append(self.pass_map[p_name])
        else:
            active_passes = list(self.pass_map.values())

        for iteration in range(self.max_iterations):
            iteration_changed = False
            for p in active_passes:
                new_instructions, changes = p.run(current)
                if changes:
                    iteration_changed = True
                    all_changes.extend(changes)
                    current = new_instructions

            if not iteration_changed:
                break

        return current, all_changes
