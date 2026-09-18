import pytest
from backend.app.compiler.lexer import Lexer
from backend.app.compiler.parser import Parser
from backend.app.compiler.intermediate import TACGenerator
from backend.app.compiler.optimizer import OptimizerPipeline


def get_tac_and_optimize(code: str):
    tokens, _ = Lexer(code).tokenize()
    program, _ = Parser(tokens).parse()
    tac = TACGenerator().generate(program)
    opt = OptimizerPipeline()
    return opt.optimize(tac)


def test_optimizer_constant_folding():
    code = "int x = 10 + 20;"
    opt_tac, changes = get_tac_and_optimize(code)

    assert len(changes) > 0
    assert any(c["pass"] == "Constant Folding" for c in changes)
    # Check that 30 is in the final instructions
    assigned_values = [t.arg1 for t in opt_tac if t.op == "="]
    assert "30" in assigned_values


def test_optimizer_algebraic_simplification():
    code = """
    int a;
    int b = a + 0;
    int c = a * 1;
    int d = a * 0;
    """
    opt_tac, changes = get_tac_and_optimize(code)

    assert any(c["pass"] == "Algebraic Simplification" for c in changes)
    # d should be 0
    d_assign = [t for t in opt_tac if t.result == "d"]
    assert len(d_assign) == 1
    assert d_assign[0].arg1 == "0"


def test_optimizer_constant_propagation():
    code = """
    int a = 10;
    int b = a + 5;
    """
    opt_tac, changes = get_tac_and_optimize(code)

    # a is 10, so a + 5 becomes 10 + 5, which then folds into 15!
    assert any(c["pass"] == "Constant Propagation" for c in changes)
    b_assign = [t for t in opt_tac if t.result == "b"]
    assert len(b_assign) == 1
    assert b_assign[0].arg1 == "15"


def test_optimizer_dead_code_elimination():
    code = """
    int a = 10;
    int b = 20;
    return a;
    int c = 30;
    """
    opt_tac, changes = get_tac_and_optimize(code)

    assert any(c["pass"] == "Dead Code Elimination" for c in changes)
    results = [t.result for t in opt_tac]
    assert "c" not in results
