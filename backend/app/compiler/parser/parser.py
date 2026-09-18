from typing import List, Tuple, Optional
from ..lexer.tokens import Token, TokenType
from .ast_nodes import (
    Program,
    VarDecl,
    Assignment,
    BinaryExpr,
    UnaryExpr,
    LiteralExpr,
    VariableExpr,
    Block,
    IfStmt,
    WhileStmt,
    ForStmt,
    PrintStmt,
    ReturnStmt,
    ASTNode,
    reset_node_counter,
)


class CompilerSyntaxError(Exception):
    def __init__(
        self,
        message: str,
        line: int,
        column: int,
        unexpected: str = "",
        expected: str = "",
        possible_cause: str = "",
    ):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.unexpected = unexpected
        self.expected = expected
        self.possible_cause = possible_cause

    def to_dict(self) -> dict:
        return {
            "errorType": "Syntax Error",
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "unexpected": self.unexpected,
            "expected": self.expected,
            "possibleCause": self.possible_cause,
        }


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors: List[CompilerSyntaxError] = []

    def parse(self) -> Tuple[Optional[Program], List[CompilerSyntaxError]]:
        reset_node_counter()
        statements: List[ASTNode] = []

        while not self._is_at_end():
            try:
                stmt = self._declaration()
                if stmt is not None:
                    statements.append(stmt)
            except CompilerSyntaxError as e:
                self.errors.append(e)
                self._synchronize()

        first_token = self.tokens[0] if self.tokens else None
        line = first_token.line if first_token else 1
        col = first_token.column if first_token else 1

        program = Program(statements, line, col)
        return program, self.errors

    # ------------------ Navigation helpers ------------------

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _match(self, *token_types: TokenType) -> bool:
        for t in token_types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str, possible_cause: str = "") -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        err = CompilerSyntaxError(
            message=message,
            line=token.line,
            column=token.column,
            unexpected=token.lexeme or token.type.value,
            expected=token_type.value,
            possible_cause=possible_cause,
        )
        raise err

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in (
                TokenType.KEYWORD_INT,
                TokenType.KEYWORD_FLOAT,
                TokenType.KEYWORD_BOOL,
                TokenType.KEYWORD_STRING,
                TokenType.KEYWORD_IF,
                TokenType.KEYWORD_WHILE,
                TokenType.KEYWORD_PRINT,
                TokenType.KEYWORD_RETURN,
                TokenType.RBRACE,
            ):
                return
            self._advance()

    # ------------------ Grammar Rules ------------------

    def _declaration(self) -> Optional[ASTNode]:
        if self._match(
            TokenType.KEYWORD_INT,
            TokenType.KEYWORD_FLOAT,
            TokenType.KEYWORD_BOOL,
            TokenType.KEYWORD_STRING,
        ):
            return self._var_declaration()
        return self._statement()

    def _var_declaration(self) -> VarDecl:
        type_token = self._previous()
        var_type = type_token.lexeme

        name_token = self._consume(
            TokenType.IDENTIFIER,
            f"Expected variable name after '{var_type}'",
            "Variable declarations must follow the format '<type> <name>;' or '<type> <name> = <value>;'",
        )

        initializer = None
        if self._match(TokenType.ASSIGN):
            initializer = self._expression()

        self._consume(
            TokenType.SEMICOLON,
            "Expected ';' after variable declaration",
            "Statements must end with a semicolon ';'",
        )
        return VarDecl(var_type, name_token.lexeme, initializer, type_token.line, type_token.column)

    def _statement(self) -> ASTNode:
        if self._match(TokenType.KEYWORD_IF):
            return self._if_statement()
        if self._match(TokenType.KEYWORD_WHILE):
            return self._while_statement()
        if self._match(TokenType.KEYWORD_FOR):
            return self._for_statement()
        if self._match(TokenType.KEYWORD_PRINT):
            return self._print_statement()
        if self._match(TokenType.KEYWORD_RETURN):
            return self._return_statement()
        if self._match(TokenType.LBRACE):
            return self._block()
        return self._assignment_statement()

    def _for_statement(self) -> ForStmt:
        keyword = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'for'", "For loops syntax: 'for (init; cond; inc) body'")

        initializer = None
        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(
            TokenType.KEYWORD_INT,
            TokenType.KEYWORD_FLOAT,
            TokenType.KEYWORD_BOOL,
            TokenType.KEYWORD_STRING,
        ):
            initializer = self._var_declaration()
        else:
            initializer = self._assignment_statement()

        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after for loop condition")

        increment = None
        if not self._check(TokenType.RPAREN):
            increment = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after for loop increment")

        body = self._statement()
        return ForStmt(initializer, condition, increment, body, keyword.line, keyword.column)

    def _if_statement(self) -> IfStmt:
        keyword = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'if'", "Conditions must be enclosed in parentheses '(...)'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition")

        then_branch = self._statement()
        else_branch = None
        if self._match(TokenType.KEYWORD_ELSE):
            else_branch = self._statement()

        return IfStmt(condition, then_branch, else_branch, keyword.line, keyword.column)

    def _while_statement(self) -> WhileStmt:
        keyword = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'while'", "Conditions must be enclosed in parentheses '(...)'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after while condition")

        body = self._statement()
        return WhileStmt(condition, body, keyword.line, keyword.column)

    def _print_statement(self) -> PrintStmt:
        keyword = self._previous()
        has_paren = self._match(TokenType.LPAREN)
        expr = self._expression()
        if has_paren:
            self._consume(TokenType.RPAREN, "Expected ')' after print expression")
        self._consume(TokenType.SEMICOLON, "Expected ';' after print statement", "Statements must end with a semicolon ';'")
        return PrintStmt(expr, keyword.line, keyword.column)

    def _return_statement(self) -> ReturnStmt:
        keyword = self._previous()
        expr = None
        if not self._check(TokenType.SEMICOLON):
            expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after return statement")
        return ReturnStmt(expr, keyword.line, keyword.column)

    def _block(self) -> Block:
        open_brace = self._previous()
        statements: List[ASTNode] = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._declaration()
            if stmt:
                statements.append(stmt)
        self._consume(TokenType.RBRACE, "Expected '}' after block", "Unclosed block; check for missing '}'")
        return Block(statements, open_brace.line, open_brace.column)

    def _assignment_statement(self) -> ASTNode:
        expr = self._expression()

        # If it's a bare expression ending in semicolon
        self._consume(TokenType.SEMICOLON, "Expected ';' after statement", "Assignments and expressions must terminate with ';'")
        return expr

    # ------------------ Expression Parsing ------------------

    def _expression(self) -> ASTNode:
        return self._assignment()

    def _assignment(self) -> ASTNode:
        expr = self._logic_or()

        if self._match(
            TokenType.ASSIGN,
            TokenType.PLUS_ASSIGN,
            TokenType.MINUS_ASSIGN,
            TokenType.STAR_ASSIGN,
            TokenType.SLASH_ASSIGN,
        ):
            operator_token = self._previous()
            value = self._assignment()

            if isinstance(expr, VariableExpr):
                op = operator_token.lexeme
                if op != "=":
                    # Convert `a += b` to `a = a + b`
                    base_op = op[0]  # '+' from '+='
                    binary = BinaryExpr(
                        VariableExpr(expr.name, expr.line, expr.column),
                        base_op,
                        value,
                        operator_token.line,
                        operator_token.column,
                    )
                    return Assignment(expr.name, "=", binary, expr.line, expr.column)
                return Assignment(expr.name, "=", value, expr.line, expr.column)

            raise CompilerSyntaxError(
                "Invalid assignment target",
                operator_token.line,
                operator_token.column,
                unexpected=operator_token.lexeme,
                expected="variable name",
                possible_cause="Left-hand side of an assignment must be a valid variable name.",
            )

        return expr

    def _logic_or(self) -> ASTNode:
        expr = self._logic_and()
        while self._match(TokenType.PIPE_PIPE):
            op = self._previous()
            right = self._logic_and()
            expr = BinaryExpr(expr, op.lexeme, right, op.line, op.column)
        return expr

    def _logic_and(self) -> ASTNode:
        expr = self._equality()
        while self._match(TokenType.AMP_AMP):
            op = self._previous()
            right = self._equality()
            expr = BinaryExpr(expr, op.lexeme, right, op.line, op.column)
        return expr

    def _equality(self) -> ASTNode:
        expr = self._relational()
        while self._match(TokenType.EQ_EQ, TokenType.BANG_EQ):
            op = self._previous()
            right = self._relational()
            expr = BinaryExpr(expr, op.lexeme, right, op.line, op.column)
        return expr

    def _relational(self) -> ASTNode:
        expr = self._additive()
        while self._match(TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            op = self._previous()
            right = self._additive()
            expr = BinaryExpr(expr, op.lexeme, right, op.line, op.column)
        return expr

    def _additive(self) -> ASTNode:
        expr = self._multiplicative()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            right = self._multiplicative()
            expr = BinaryExpr(expr, op.lexeme, right, op.line, op.column)
        return expr

    def _multiplicative(self) -> ASTNode:
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._previous()
            right = self._unary()
            expr = BinaryExpr(expr, op.lexeme, right, op.line, op.column)
        return expr

    def _unary(self) -> ASTNode:
        if self._match(TokenType.BANG, TokenType.MINUS):
            op = self._previous()
            right = self._unary()
            return UnaryExpr(op.lexeme, right, op.line, op.column)
        return self._primary()

    def _primary(self) -> ASTNode:
        if self._match(TokenType.INT_LITERAL):
            tok = self._previous()
            return LiteralExpr(tok.literal, "int", tok.line, tok.column)

        if self._match(TokenType.FLOAT_LITERAL):
            tok = self._previous()
            return LiteralExpr(tok.literal, "float", tok.line, tok.column)

        if self._match(TokenType.STRING_LITERAL):
            tok = self._previous()
            return LiteralExpr(tok.literal, "string", tok.line, tok.column)

        if self._match(TokenType.BOOL_LITERAL):
            tok = self._previous()
            return LiteralExpr(tok.literal, "bool", tok.line, tok.column)

        if self._match(TokenType.IDENTIFIER):
            tok = self._previous()
            return VariableExpr(tok.lexeme, tok.line, tok.column)

        if self._match(TokenType.LPAREN):
            lparen = self._previous()
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression", "Mismatched or missing closing parenthesis ')'")
            return expr

        tok = self._peek()
        raise CompilerSyntaxError(
            f"Unexpected token '{tok.lexeme or tok.type.value}'",
            tok.line,
            tok.column,
            unexpected=tok.lexeme or tok.type.value,
            expected="expression (number, variable, etc.)",
            possible_cause="Missing operand, extra symbol, or incorrect expression syntax.",
        )
