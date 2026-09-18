import pytest
from backend.app.compiler.lexer import Lexer, TokenType
from backend.app.compiler.parser import Parser, ForStmt
from backend.app.compiler.pipeline import CompilerPipeline
from backend.app.compiler.target import TargetCodeGenerator, TargetInstruction, TargetVMSimulator


def test_for_loop_compilation_and_execution():
    code = """
    int sum = 0;
    for (int i = 1; i <= 5; i = i + 1) {
        sum = sum + i;
    }
    print sum;
    """
    pipeline = CompilerPipeline()
    res = pipeline.compile(code)

    assert res["success"] is True
    assert res["statistics"]["status"] == "Compilation Successful"

    # Simulate
    sim = TargetVMSimulator()
    target_objs = [
        TargetInstruction(
            op=d["op"],
            arg1=d.get("arg1"),
            arg2=d.get("arg2"),
            source_line=d.get("sourceLine", 1),
        )
        for d in res["instructions"]
    ]
    sim_res = sim.run(target_objs)
    assert sim_res["success"] is True
    # 1 + 2 + 3 + 4 + 5 = 15
    assert sim_res["memory"]["sum"] == 15
    assert sim_res["output"] == ["15"]


def test_selective_optimizer_passes():
    code = """
    int x = 10 + 20;
    int y = x + 0;
    """
    pipeline = CompilerPipeline()

    # Case A: Only Constant Folding enabled
    res_folding = pipeline.compile(code, enabled_passes=["constant_folding"])
    passes_applied = [o["pass"] for o in res_folding["optimizations"]]
    assert "Constant Folding" in passes_applied
    assert "Algebraic Simplification" not in passes_applied

    # Case B: Only Algebraic Simplification enabled
    code_alg = "int a; int b = a + 0;"
    res_alg = pipeline.compile(code_alg, enabled_passes=["algebraic_simplification"])
    passes_applied_alg = [o["pass"] for o in res_alg["optimizations"]]
    assert "Algebraic Simplification" in passes_applied_alg
    assert "Constant Folding" not in passes_applied_alg


def test_vm_breakpoints():
    code = """
    int a = 10;
    int b = 20;
    int c = a + b;
    """
    pipeline = CompilerPipeline()
    res = pipeline.compile(code)

    target_objs = [
        TargetInstruction(
            op=d["op"],
            arg1=d.get("arg1"),
            arg2=d.get("arg2"),
            source_line=d.get("sourceLine", 1),
        )
        for d in res["instructions"]
    ]

    # Set breakpoint at instruction index 2
    sim = TargetVMSimulator()
    sim_res = sim.run(target_objs, breakpoints=[2])

    assert sim_res["hitBreakpoint"] is True
    assert sim_res["breakpointPC"] == 2
    # Instructions at or after PC 2 have not run yet
    assert sim_res["cycles"] > 0


def test_vm_flags_and_branches():
    sim = TargetVMSimulator()
    instructions = [
        TargetInstruction("LOAD", "R0", "15"),
        TargetInstruction("LOAD", "R1", "10"),
        TargetInstruction("CMP", "R0", "R1"),  # 15 > 10 -> greater=True, less=False, zero=False
        TargetInstruction("JG", "L_greater"),
        TargetInstruction("LOAD", "R2", "0"),
        TargetInstruction("JMP", "L_end"),
        TargetInstruction("LABEL", "L_greater"),
        TargetInstruction("LOAD", "R2", "1"),
        TargetInstruction("LABEL", "L_end"),
        TargetInstruction("HALT"),
    ]
    res = sim.run(instructions)
    assert res["success"] is True
    assert res["flags"]["greater"] is True
    assert res["flags"]["zero"] is False
    assert res["flags"]["less"] is False
    assert res["registers"]["R2"] == 1


def test_stage_timings_recorded():
    code = "int a = 10; int b = 20; int c = a + b;"
    pipeline = CompilerPipeline()
    res = pipeline.compile(code)

    timings = res.get("timings", {})
    assert "lexer" in timings
    assert "parser" in timings
    assert "semantic" in timings
    assert "tac" in timings
    assert "optimizer" in timings
    assert "codegen" in timings
    assert "trace" in timings
    assert all(t >= 0.0 for t in timings.values())
