import pytest
from backend.app.compiler.lexer import Lexer
from backend.app.compiler.parser import Parser
from backend.app.compiler.intermediate import TACGenerator
from backend.app.compiler.target import TargetCodeGenerator, TargetVMSimulator


def compile_and_run(code: str):
    tokens, _ = Lexer(code).tokenize()
    program, _ = Parser(tokens).parse()
    tac = TACGenerator().generate(program)
    target = TargetCodeGenerator().generate(tac)
    sim = TargetVMSimulator()
    return sim.run(target)


def test_simulator_arithmetic_execution():
    code = """
    int a = 15;
    int b = 25;
    int c = a + b;
    """
    res = compile_and_run(code)
    assert res["success"] is True
    assert res["memory"]["a"] == 15
    assert res["memory"]["b"] == 25
    assert res["memory"]["c"] == 40


def test_simulator_while_loop_accumulator():
    code = """
    int i = 0;
    int sum = 0;
    while (i < 5) {
        sum = sum + i;
        i = i + 1;
    }
    """
    res = compile_and_run(code)
    assert res["success"] is True
    assert res["memory"]["i"] == 5
    # 0 + 1 + 2 + 3 + 4 = 10
    assert res["memory"]["sum"] == 10


def test_simulator_print_statement():
    code = """
    int a = 42;
    print a;
    """
    res = compile_and_run(code)
    assert res["success"] is True
    assert res["output"] == ["42"]
