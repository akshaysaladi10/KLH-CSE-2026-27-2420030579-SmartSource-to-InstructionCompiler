import pytest
from backend.app.compiler.lexer import Lexer
from backend.app.compiler.parser import Parser
from backend.app.compiler.semantic import SemanticAnalyzer


def analyze_code(code: str):
    tokens, _ = Lexer(code).tokenize()
    program, p_errors = Parser(tokens).parse()
    assert len(p_errors) == 0
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program)


def test_semantic_valid_declarations():
    code = """
    int a = 10;
    int b = 20;
    int c = a + b;
    """
    symbols, errors = analyze_code(code)
    assert len(errors) == 0
    assert len(symbols) == 3
    names = [s["name"] for s in symbols]
    assert names == ["a", "b", "c"]


def test_semantic_undeclared_variable():
    code = """
    int a = 10;
    b = 20;
    """
    symbols, errors = analyze_code(code)
    assert len(errors) == 1
    assert "Undeclared variable 'b'" in errors[0].message


def test_semantic_duplicate_declaration():
    code = """
    int x = 10;
    int x = 20;
    """
    symbols, errors = analyze_code(code)
    assert len(errors) == 1
    assert "Redeclaration of variable 'x'" in errors[0].message


def test_semantic_type_mismatch():
    code = """
    int a = "hello";
    """
    symbols, errors = analyze_code(code)
    assert len(errors) == 1
    assert "incompatible" in errors[0].message.lower()


def test_semantic_invalid_binary_operation():
    code = """
    string s = "world";
    int n = 5;
    string res = s - n;
    """
    symbols, errors = analyze_code(code)
    assert len(errors) > 0
    assert any("cannot be applied" in err.message for err in errors)


def test_semantic_scope_isolation():
    code = """
    int x = 10;
    {
        int y = 20;
    }
    x = y;
    """
    symbols, errors = analyze_code(code)
    assert len(errors) == 1
    assert "Undeclared variable 'y'" in errors[0].message
