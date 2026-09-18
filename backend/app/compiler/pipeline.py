import time
from typing import Dict, Any, List, Optional

from .lexer import Lexer, Token
from .parser import Parser, Program
from .semantic import SemanticAnalyzer
from .intermediate import TACGenerator, TACInstruction
from .optimizer import OptimizerPipeline
from .target import TargetCodeGenerator, TargetInstruction, TargetVMSimulator
from .trace import SourceToInstructionTracer


def count_ast_nodes(node_dict: Optional[Dict[str, Any]]) -> int:
    if not node_dict:
        return 0
    count = 1
    for child in node_dict.get("children", []):
        count += count_ast_nodes(child)
    return count


class CompilerPipeline:
    def __init__(self):
        self.optimizer = OptimizerPipeline()
        self.tracer = SourceToInstructionTracer()

    def compile(
        self,
        source_code: str,
        enabled_passes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        overall_start = time.perf_counter()

        timings: Dict[str, float] = {
            "lexer": 0.0,
            "parser": 0.0,
            "semantic": 0.0,
            "tac": 0.0,
            "optimizer": 0.0,
            "codegen": 0.0,
            "trace": 0.0,
        }

        stage_status: Dict[str, str] = {
            "lexer": "pending",
            "parser": "pending",
            "semantic": "pending",
            "tac": "pending",
            "optimizer": "pending",
            "codegen": "pending",
            "trace": "pending",
        }

        all_errors: List[Dict[str, Any]] = []
        tokens_data: List[Dict[str, Any]] = []
        ast_data: Optional[Dict[str, Any]] = None
        symbol_table_data: List[Dict[str, Any]] = []
        tac_data: List[Dict[str, Any]] = []
        opt_tac_data: List[Dict[str, Any]] = []
        optimizations_applied: List[Dict[str, Any]] = []
        instructions_data: List[Dict[str, Any]] = []
        trace_matrix: List[Dict[str, Any]] = []

        # 1. Lexical Analysis
        t0 = time.perf_counter()
        stage_status["lexer"] = "running"
        lexer = Lexer(source_code)
        tokens, lex_errors = lexer.tokenize()
        for err in lex_errors:
            all_errors.append(err.to_dict())
        tokens_data = [t.to_dict() for t in tokens]
        timings["lexer"] = round((time.perf_counter() - t0) * 1000, 3)
        stage_status["lexer"] = "error" if lex_errors else "completed"

        # 2. Syntax Analysis
        t0 = time.perf_counter()
        stage_status["parser"] = "running"
        parser = Parser(tokens)
        ast_program, parse_errors = parser.parse()
        for err in parse_errors:
            all_errors.append(err.to_dict())

        ast_node_count = 0
        if ast_program:
            ast_data = ast_program.to_dict()
            ast_node_count = count_ast_nodes(ast_data)
        timings["parser"] = round((time.perf_counter() - t0) * 1000, 3)
        stage_status["parser"] = "error" if parse_errors else "completed"

        # 3. Semantic Analysis
        symbols_count = 0
        if ast_program and not parse_errors:
            t0 = time.perf_counter()
            stage_status["semantic"] = "running"
            analyzer = SemanticAnalyzer()
            symbol_table_data, sem_errors = analyzer.analyze(ast_program)
            for err in sem_errors:
                all_errors.append(err.to_dict())
            symbols_count = len(symbol_table_data)
            timings["semantic"] = round((time.perf_counter() - t0) * 1000, 3)
            stage_status["semantic"] = "error" if sem_errors else "completed"
        else:
            stage_status["semantic"] = "skipped"

        # 4. TAC Generation (only if no fatal syntax / semantic errors)
        tac_list: List[TACInstruction] = []
        opt_tac_list: List[TACInstruction] = []
        target_list: List[TargetInstruction] = []

        if ast_program and len(all_errors) == 0:
            # TAC
            t0 = time.perf_counter()
            stage_status["tac"] = "running"
            tac_gen = TACGenerator()
            tac_list = tac_gen.generate(ast_program)
            tac_data = [t.to_dict() for t in tac_list]
            timings["tac"] = round((time.perf_counter() - t0) * 1000, 3)
            stage_status["tac"] = "completed"

            # 5. Optimization
            t0 = time.perf_counter()
            stage_status["optimizer"] = "running"
            opt_tac_list, optimizations_applied = self.optimizer.optimize(
                tac_list,
                enabled_passes=enabled_passes,
            )
            opt_tac_data = [t.to_dict() for t in opt_tac_list]
            timings["optimizer"] = round((time.perf_counter() - t0) * 1000, 3)
            stage_status["optimizer"] = "completed"

            # 6. Target Instruction Generation
            t0 = time.perf_counter()
            stage_status["codegen"] = "running"
            codegen = TargetCodeGenerator()
            target_list = codegen.generate(opt_tac_list)
            instructions_data = [i.to_dict() for i in target_list]
            timings["codegen"] = round((time.perf_counter() - t0) * 1000, 3)
            stage_status["codegen"] = "completed"

            # 7. Source-to-Instruction Trace
            t0 = time.perf_counter()
            stage_status["trace"] = "running"
            trace_matrix = self.tracer.build_trace(
                source_code=source_code,
                ast_program=ast_program,
                tac_list=tac_list,
                optimized_tac=opt_tac_list,
                target_instructions=target_list,
            )
            timings["trace"] = round((time.perf_counter() - t0) * 1000, 3)
            stage_status["trace"] = "completed"
        else:
            stage_status["tac"] = "skipped"
            stage_status["optimizer"] = "skipped"
            stage_status["codegen"] = "skipped"
            stage_status["trace"] = "skipped"

        elapsed_ms = round((time.perf_counter() - overall_start) * 1000, 2)
        source_line_count = len(source_code.splitlines()) if source_code else 0
        success = len(all_errors) == 0

        original_count = len(tac_data)
        optimized_count = len(opt_tac_data)
        reduction_percent = (
            round(((original_count - optimized_count) / original_count) * 100, 1)
            if original_count > 0
            else 0.0
        )

        statistics = {
            "sourceLines": source_line_count,
            "tokensCount": len(tokens_data),
            "astNodesCount": ast_node_count,
            "symbolsCount": symbols_count,
            "tacInstructionsCount": original_count,
            "optimizedTacCount": optimized_count,
            "reductionPercent": reduction_percent,
            "optimizationsCount": len(optimizations_applied),
            "targetInstructionsCount": len(instructions_data),
            "compilationTimeMs": elapsed_ms,
            "status": "Compilation Successful" if success else "Compilation Failed",
            "hasErrors": not success,
            "errorCount": len(all_errors),
        }

        return {
            "success": success,
            "statistics": statistics,
            "timings": timings,
            "stageStatus": stage_status,
            "tokens": tokens_data,
            "ast": ast_data,
            "symbolTable": symbol_table_data,
            "tac": tac_data,
            "optimizedTac": opt_tac_data,
            "optimizations": optimizations_applied,
            "instructions": instructions_data,
            "traceMatrix": trace_matrix,
            "errors": all_errors,
        }
