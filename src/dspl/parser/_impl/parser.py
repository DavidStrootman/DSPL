from typing import Sequence

from dspl.exceptions import DaVinkyException
from dspl.helper import flatten_right, mapx, split_first
from dspl.lexer_tokens import LexerToken, DelimLexerToken, KeywordLexerToken, LiteralLexerToken, OpLexerToken, \
    RawIdentLexerToken, StructuralLexerToken
from dspl.parser._impl.parse_functs import parse_statement
from dspl.parser_tokens import ParserToken


def parse(lexer_tokens: Sequence[LexerToken]):
    def _parse_internal(lexer_tokens_: Sequence[LexerToken]):
        if not lexer_tokens_:
            return ()
        else:
            return flatten_right(
                mapx(fns=[(lambda x: x), (lambda y: parse(y))], seq=parse_statement(lexer_tokens_)))

    return _parse_internal(lexer_tokens)
