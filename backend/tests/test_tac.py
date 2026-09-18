import pytest
from backend.app.compiler.lexer import Lexer
from backend.app.compiler.parser import Parser
from backend.app.compiler.intermediate import TACGenerator


def generate_tac(code: str):
    tokens, _ = Lexer(code).tokenize()
    program, _ = Parser(tokens).parse()
    gen = TACGenerator()
    return gen.generate(program)


def test_tac_arithmetic():
    code = "int a = 10; int b = 20; int c = a + b * 2;"
    tac = generate_tac(code)

    assert len(tac) >= 4
    # Check that temporary is generated for multiplication first
    mult_instr = [t for t in tac if t.op == "*"]
    assert len(mult_instr) == 1
    assert mult_instr[0].arg1 == "b"
    assert mult_instr[0].arg2 == "2"

    add_instr = [t for t in tac if t.op == "+"]
    assert len(add_instr) == 1
    assert add_instr[0].arg1 == "a"
    assert add_instr[0].arg2 == mult_instr[0].result


def test_tac_if_else():
    code = """
    if (a > b) {
        c = 1;
    } else {
        c = 2;
    }
    """
    tac = generate_tac(code)
    op_types = [t.op for t in tac]

    assert "ifFalse" in op_types
    assert "goto" in op_types
    assert "label" in op_types


def test_tac_while_loop():
    code = """
    while (i < 5) {
        i = i + 1;
    }
    """
    tac = generate_tac(code)
    op_types = [t.op for t in tac]

    assert "label" in op_types
    assert "ifFalse" in op_types
    assert "goto" in op_types
