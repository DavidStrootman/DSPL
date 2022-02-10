from collections.abc import Sequence

from dspl.exceptions import UnexpectedTokenError, UnexpectedTokenTypeError
from dspl.lexer_tokens import LexerToken, DelimLexerToken, KeywordLexerToken, KeywordLexerTokenKind, LiteralLexerToken, \
    OpLexerToken, \
    RawIdentLexerToken, StructuralLexerToken
from dspl.parser_tokens import ParserToken


def parse_delim(head: DelimLexerToken, tail: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    raise UnexpectedTokenError()


def parse_keyword(head: KeywordLexerToken, tail: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    match head.kind:
        case KeywordLexerTokenKind.FUNCTION:
            return parse_function_token()

        case KeywordLexerTokenKind.RETURN:
            return parse_return_token()

        case KeywordLexerTokenKind.BIND:
            return parse_bind_token()

        case KeywordLexerTokenKind.IF:
            return parse_if_token()

        case KeywordLexerTokenKind.ELSE:
            raise UnexpectedTokenTypeError()

        case KeywordLexerTokenKind.WHILE:
            return parse_while_token()

        case _:
            raise UnexpectedTokenTypeError()


def parse_literal(head: LiteralLexerToken, tail: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    pass


def parse_op(head: OpLexerToken, tail: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    pass


def parse_raw_ident(head: RawIdentLexerToken, tail: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    pass


def parse_structural(head: StructuralLexerToken, tail: Sequence[LexerToken]) -> tuple[
    ParserToken, Sequence[LexerToken]]:
    pass


def parse_function_token(head: StructuralLexerToken, tail: Sequence[LexerToken]) -> tuple[
    ParserToken, Sequence[LexerToken]]:
    match tail:
        case [RawIdentLexerToken(), DelimLexerToken(), *args]:
            parameters = parse_function_parameters()
        case _:
            raise UnexpectedTokenError()


def parse_function_parameters(body: Sequence[LexerToken]) -> tuple[tuple[ParserToken], Sequence[LexerToken]]:
    pass
