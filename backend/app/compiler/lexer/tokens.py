from enum import Enum, auto
from typing import Any, Optional
from pydantic import BaseModel


class TokenType(str, Enum):
    # Keywords
    KEYWORD_INT = "int"
    KEYWORD_FLOAT = "float"
    KEYWORD_BOOL = "bool"
    KEYWORD_STRING = "string"
    KEYWORD_IF = "if"
    KEYWORD_ELSE = "else"
    KEYWORD_WHILE = "while"
    KEYWORD_FOR = "for"
    KEYWORD_PRINT = "print"
    KEYWORD_RETURN = "return"
    KEYWORD_TRUE = "true"
    KEYWORD_FALSE = "false"

    # Identifiers & Literals
    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"

    # Arithmetic Operators
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"

    # Assignment Operators
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    STAR_ASSIGN = "*="
    SLASH_ASSIGN = "/="

    # Relational & Equality Operators
    EQ_EQ = "=="
    BANG_EQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="

    # Logical Operators
    AMP_AMP = "&&"
    PIPE_PIPE = "||"
    BANG = "!"

    # Delimiters & Grouping
    SEMICOLON = ";"
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"

    # Special
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"


KEYWORDS = {
    "int": TokenType.KEYWORD_INT,
    "float": TokenType.KEYWORD_FLOAT,
    "bool": TokenType.KEYWORD_BOOL,
    "string": TokenType.KEYWORD_STRING,
    "if": TokenType.KEYWORD_IF,
    "else": TokenType.KEYWORD_ELSE,
    "while": TokenType.KEYWORD_WHILE,
    "for": TokenType.KEYWORD_FOR,
    "print": TokenType.KEYWORD_PRINT,
    "return": TokenType.KEYWORD_RETURN,
    "true": TokenType.KEYWORD_TRUE,
    "false": TokenType.KEYWORD_FALSE,
}


class Token:
    def __init__(
        self,
        token_type: TokenType,
        lexeme: str,
        literal: Any = None,
        line: int = 1,
        column: int = 1,
    ):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"Token({self.type.value}, '{self.lexeme}', line={self.line}, col={self.column})"

    def to_dict(self) -> dict:
        return {
            "token": self.type.value,
            "lexeme": self.lexeme,
            "type": self._category(),
            "line": self.line,
            "column": self.column,
            "literal": self.literal,
        }

    def _category(self) -> str:
        if self.type.value in KEYWORDS:
            return "Keyword"
        if self.type == TokenType.IDENTIFIER:
            return "Identifier"
        if self.type in (TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STRING_LITERAL, TokenType.BOOL_LITERAL):
            return "Literal"
        if self.type in (
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
            TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN,
            TokenType.EQ_EQ, TokenType.BANG_EQ, TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE,
            TokenType.AMP_AMP, TokenType.PIPE_PIPE, TokenType.BANG
        ):
            return "Operator"
        if self.type in (TokenType.SEMICOLON, TokenType.COMMA):
            return "Delimiter"
        if self.type in (TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE, TokenType.LBRACKET, TokenType.RBRACKET):
            return "Separator"
        if self.type == TokenType.EOF:
            return "EOF"
        return "Unknown"
