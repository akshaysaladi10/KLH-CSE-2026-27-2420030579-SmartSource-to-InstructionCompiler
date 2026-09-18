import pytest
from backend.app.compiler.lexer import Lexer, TokenType


def test_lexer_basic_tokens():
    code = "int a = 10 + 20;"
    lexer = Lexer(code)
    tokens, errors = lexer.tokenize()

    assert len(errors) == 0
    token_types = [t.type for t in tokens]
    assert token_types == [
        TokenType.KEYWORD_INT,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.INT_LITERAL,
        TokenType.PLUS,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    assert tokens[1].lexeme == "a"
    assert tokens[3].literal == 10
    assert tokens[5].literal == 20


def test_lexer_floats_and_strings():
    code = 'float pi = 3.14; string msg = "hello world"; bool flag = true;'
    lexer = Lexer(code)
    tokens, errors = lexer.tokenize()

    assert len(errors) == 0
    pi_tok = [t for t in tokens if t.type == TokenType.FLOAT_LITERAL][0]
    assert pi_tok.literal == 3.14
    str_tok = [t for t in tokens if t.type == TokenType.STRING_LITERAL][0]
    assert str_tok.literal == "hello world"
    bool_tok = [t for t in tokens if t.type == TokenType.BOOL_LITERAL][0]
    assert bool_tok.literal is True


def test_lexer_comments():
    code = """
    // Single-line comment
    int x = 5; /* Multi-line
    comment here */
    int y = 10;
    """
    lexer = Lexer(code)
    tokens, errors = lexer.tokenize()

    assert len(errors) == 0
    ids = [t.lexeme for t in tokens if t.type == TokenType.IDENTIFIER]
    assert ids == ["x", "y"]


def test_lexer_operators():
    code = "== != <= >= && || += -="
    lexer = Lexer(code)
    tokens, errors = lexer.tokenize()

    assert len(errors) == 0
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [
        TokenType.EQ_EQ,
        TokenType.BANG_EQ,
        TokenType.LTE,
        TokenType.GTE,
        TokenType.AMP_AMP,
        TokenType.PIPE_PIPE,
        TokenType.PLUS_ASSIGN,
        TokenType.MINUS_ASSIGN,
    ]


def test_lexer_invalid_character_error():
    code = "int a = 10 @ 20;"
    lexer = Lexer(code)
    tokens, errors = lexer.tokenize()

    assert len(errors) == 1
    assert "Unexpected character '@'" in errors[0].message
    assert errors[0].line == 1
    assert errors[0].column == 12


def test_lexer_unterminated_string_error():
    code = 'string s = "unclosed;'
    lexer = Lexer(code)
    tokens, errors = lexer.tokenize()

    assert len(errors) == 1
    assert "Unterminated string literal" in errors[0].message
