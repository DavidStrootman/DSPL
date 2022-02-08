from typing import Sequence

from dspl.helper import flatten_right, mapx
from dspl.lexer_tokens import LexerToken
from dspl.parser_tokens import ParserToken


def parse(lexer_tokens: Sequence[LexerToken]):
    def _parse_internal(lexer_tokens_: Sequence[LexerToken]):
        if not lexer_tokens_:
            return ()
        else:
            return flatten_right(mapx(fns=[(lambda x: x), (lambda y: parse(y))], seq=parse_token(lexer_tokens_)))

    return _parse_internal(lexer_tokens)


def parse_token(lexer_tokens: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    return ParserToken(), lexer_tokens[1:]
