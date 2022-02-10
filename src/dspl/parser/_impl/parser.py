from typing import Sequence

from dspl.exceptions import DaVinkyException
from dspl.helper import flatten_right, mapx, split_first
from dspl.lexer_tokens import LexerToken, DelimLexerToken, KeywordLexerToken, LiteralLexerToken, OpLexerToken, \
    RawIdentLexerToken, StructuralLexerToken
from dspl.parser._impl.parse_functs import parse_delim, parse_keyword, parse_literal, parse_op, parse_raw_ident, \
    parse_structural
from dspl.parser_tokens import ParserToken


def parse(lexer_tokens: Sequence[LexerToken]):
    def _parse_internal(lexer_tokens_: Sequence[LexerToken]):
        if not lexer_tokens_:
            return ()
        else:
            return flatten_right(
                mapx(fns=[(lambda x: x), (lambda y: parse(y))], seq=parse_token(*split_first(lexer_tokens_))))

    return _parse_internal(lexer_tokens)


def parse_token(head: ParserToken, tail: Sequence[ParserToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    match head:
        case DelimLexerToken():
            return parse_delim(head, tail)

        case KeywordLexerToken():
            return parse_keyword(head, tail)

        case LiteralLexerToken():
            return parse_literal(head, tail)

        case OpLexerToken():
            return parse_op(head, tail)

        case RawIdentLexerToken():
            return parse_raw_ident(head, tail)

        case StructuralLexerToken():
            return parse_structural(head, tail)

        case _:
            raise DaVinkyException()
