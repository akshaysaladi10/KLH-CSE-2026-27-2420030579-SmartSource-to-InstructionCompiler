import pytest
from backend.app.compiler.lexer import Lexer
from backend.app.compiler.parser import Parser
from backend.app.compiler.intermediate import TACGenerator
from backend.app.compiler.target import TargetCodeGenerator


def generate_assembly(code: str):
    tokens, _ = Lexer(code).tokenize()
    program, _ = Parser(tokens).parse()
    tac = TACGenerator().generate(program)
    codegen = TargetCodeGenerator()
    return codegen.generate(tac)


def test_codegen_arithmetic():
    code = "int a = 10; int b = 20; int c = a + b;"
    instructions = generate_assembly(code)

    ops = [i.op for i in instructions]
    assert "LOAD" in ops
    assert "STORE" in ops
    assert "ADD" in ops
    assert "HALT" in ops


def test_codegen_conditional():
    code = """
    if (a > b) {
        c = 1;
    }
    """
    instructions = generate_assembly(code)

    ops = [i.op for i in instructions]
    assert "CMP" in ops
    assert "JZ" in ops
    assert "LABEL" in ops
    assert "HALT" in ops
