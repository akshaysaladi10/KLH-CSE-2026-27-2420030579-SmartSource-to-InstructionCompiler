from typing import List, Tuple, Optional
from .tokens import Token, TokenType, KEYWORDS


class LexicalError:
    def __init__(self, message: str, line: int, column: int, possible_cause: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.possible_cause = possible_cause

    def to_dict(self) -> dict:
        return {
            "errorType": "Lexical Error",
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "possibleCause": self.possible_cause,
        }


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens: List[Token] = []
        self.errors: List[LexicalError] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.token_start_col = 1

    def tokenize(self) -> Tuple[List[Token], List[LexicalError]]:
        while not self._is_at_end():
            self.start = self.current
            self.token_start_col = self.column
            self._scan_token()

        self.tokens.append(
            Token(TokenType.EOF, "", None, self.line, self.column)
        )
        return self.tokens, self.errors

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _add_token(self, token_type: TokenType, literal: Optional[any] = None):
        text = self.source[self.start:self.current]
        self.tokens.append(
            Token(token_type, text, literal, self.line, self.token_start_col)
        )

    def _scan_token(self):
        c = self._advance()
        if c in (" ", "\r", "\t"):
            return
        if c == "\n":
            self.line += 1
            self.column = 1
            return

        # Delimiters and Single-character separators
        if c == "(":
            self._add_token(TokenType.LPAREN)
        elif c == ")":
            self._add_token(TokenType.RPAREN)
        elif c == "{":
            self._add_token(TokenType.LBRACE)
        elif c == "}":
            self._add_token(TokenType.RBRACE)
        elif c == "[":
            self._add_token(TokenType.LBRACKET)
        elif c == "]":
            self._add_token(TokenType.RBRACKET)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)

        # Operators with potential multi-character forms
        elif c == "+":
            if self._match("="):
                self._add_token(TokenType.PLUS_ASSIGN)
            else:
                self._add_token(TokenType.PLUS)
        elif c == "-":
            if self._match("="):
                self._add_token(TokenType.MINUS_ASSIGN)
            else:
                self._add_token(TokenType.MINUS)
        elif c == "*":
            if self._match("="):
                self._add_token(TokenType.STAR_ASSIGN)
            else:
                self._add_token(TokenType.STAR)
        elif c == "%":
            self._add_token(TokenType.PERCENT)
        elif c == "/":
            if self._match("/"):
                # Single-line comment
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            elif self._match("*"):
                # Multi-line comment
                self._multiline_comment()
            elif self._match("="):
                self._add_token(TokenType.SLASH_ASSIGN)
            else:
                self._add_token(TokenType.SLASH)
        elif c == "!":
            if self._match("="):
                self._add_token(TokenType.BANG_EQ)
            else:
                self._add_token(TokenType.BANG)
        elif c == "=":
            if self._match("="):
                self._add_token(TokenType.EQ_EQ)
            else:
                self._add_token(TokenType.ASSIGN)
        elif c == "<":
            if self._match("="):
                self._add_token(TokenType.LTE)
            else:
                self._add_token(TokenType.LT)
        elif c == ">":
            if self._match("="):
                self._add_token(TokenType.GTE)
            else:
                self._add_token(TokenType.GT)
        elif c == "&":
            if self._match("&"):
                self._add_token(TokenType.AMP_AMP)
            else:
                self.errors.append(
                    LexicalError(
                        "Unexpected character '&'",
                        self.line,
                        self.token_start_col,
                        "Did you mean logical AND '&&'?",
                    )
                )
        elif c == "|":
            if self._match("|"):
                self._add_token(TokenType.PIPE_PIPE)
            else:
                self.errors.append(
                    LexicalError(
                        "Unexpected character '|'",
                        self.line,
                        self.token_start_col,
                        "Did you mean logical OR '||'?",
                    )
                )
        elif c == '"':
            self._string()
        elif c.isdigit():
            self._number()
        elif c.isalpha() or c == "_":
            self._identifier()
        else:
            self.errors.append(
                LexicalError(
                    f"Unexpected character '{c}'",
                    self.line,
                    self.token_start_col,
                    f"Character '{c}' is not recognized by the grammar.",
                )
            )

    def _multiline_comment(self):
        start_line = self.line
        start_col = self.token_start_col
        while not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
                self.column = 0
            if self._peek() == "*" and self._peek_next() == "/":
                self._advance()  # eat '*'
                self._advance()  # eat '/'
                return
            self._advance()
        self.errors.append(
            LexicalError(
                "Unterminated multi-line comment",
                start_line,
                start_col,
                "Expected closing '*/' before end of file.",
            )
        )

    def _string(self):
        start_col = self.token_start_col
        start_line = self.line
        chars = []
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
                self.column = 0
            if self._peek() == "\\":
                self._advance()
                escaped = self._advance()
                if escaped == "n":
                    chars.append("\n")
                elif escaped == "t":
                    chars.append("\t")
                elif escaped == '"':
                    chars.append('"')
                elif escaped == "\\":
                    chars.append("\\")
                else:
                    chars.append(escaped)
            else:
                chars.append(self._advance())

        if self._is_at_end():
            self.errors.append(
                LexicalError(
                    "Unterminated string literal",
                    start_line,
                    start_col,
                    "Expected closing double quote '\"' before end of file.",
                )
            )
            return

        self._advance()  # Closing "
        value = "".join(chars)
        self._add_token(TokenType.STRING_LITERAL, value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        # Check for fractional part
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()  # consume '.'
            while self._peek().isdigit():
                self._advance()
            text = self.source[self.start:self.current]
            self._add_token(TokenType.FLOAT_LITERAL, float(text))
        else:
            text = self.source[self.start:self.current]
            self._add_token(TokenType.INT_LITERAL, int(text))

    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        if token_type == TokenType.KEYWORD_TRUE:
            self._add_token(TokenType.BOOL_LITERAL, True)
        elif token_type == TokenType.KEYWORD_FALSE:
            self._add_token(TokenType.BOOL_LITERAL, False)
        else:
            self._add_token(token_type)
