import pytest
from backend.app.compiler.lexer import Lexer
from backend.app.compiler.parser import (
    Parser,
    VarDecl,
    Assignment,
    BinaryExpr,
    IfStmt,
    WhileStmt,
    PrintStmt,
)


def parse_code(code: str):
    tokens, lex_errors = Lexer(code).tokenize()
    assert len(lex_errors) == 0
    parser = Parser(tokens)
    return parser.parse()


def test_parser_variable_declarations():
    code = "int a = 10; float b; string c = \"hello\";"
    program, errors = parse_code(code)

    assert len(errors) == 0
    assert len(program.statements) == 3
    assert isinstance(program.statements[0], VarDecl)
    assert program.statements[0].name == "a"
    assert program.statements[0].var_type == "int"
    assert program.statements[1].name == "b"
    assert program.statements[1].initializer is None


def test_parser_precedence():
    code = "int x = 10 + 20 * 3;"
    program, errors = parse_code(code)

    assert len(errors) == 0
    decl = program.statements[0]
    # Root binary expr should be '+' because '*' has higher precedence
    init = decl.initializer
    assert isinstance(init, BinaryExpr)
    assert init.operator == "+"
    assert isinstance(init.right, BinaryExpr)
    assert init.right.operator == "*"


def test_parser_if_else_and_while():
    code = """
    if (a > 5) {
        x = 1;
    } else {
        x = 2;
    }
    while (x < 10) {
        x = x + 1;
    }
    """
    program, errors = parse_code(code)

    assert len(errors) == 0
    assert len(program.statements) == 2
    assert isinstance(program.statements[0], IfStmt)
    assert program.statements[0].else_branch is not None
    assert isinstance(program.statements[1], WhileStmt)


def test_parser_syntax_error_missing_semicolon():
    code = "int a = 10"
    program, errors = parse_code(code)

    assert len(errors) > 0
    assert any("Expected ';'" in err.message for err in errors)


def test_parser_syntax_error_invalid_expression():
    code = "int a = + ;"
    program, errors = parse_code(code)

    assert len(errors) > 0
    assert any("Unexpected token" in err.message for err in errors)
