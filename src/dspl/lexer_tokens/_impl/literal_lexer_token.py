from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import grab_until, TextStream
from dspl.lexer_tokens import LexerToken


class LiteralLexerTokenKind(ValuableEnum):
    NUMBER = "NUMBER"
    STRING = "\""


class LiteralLexerToken(LexerToken):
    def __init__(self, kind: LiteralLexerTokenKind, value: str):
        """
        Literal Lexer Tokens have two types: "string" and "number".
        Strings are denoted by the use of "", while numbers can be placed
        immediately in code, e.g. 124292. This is because variables can only use A-Za-z.
        """
        super().__init__(kind, value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        first_char, stream = stream.grab()

        if first_char in LiteralLexerTokenKind.values():
            # It's a string literal
            literal, stream = grab_until(lambda x: x == first_char, stream)

            # Discard closing double quote
            _, stream = stream.grab()

            return LiteralLexerToken(LiteralLexerTokenKind(first_char), literal), stream

        if first_char.isnumeric():
            # It's a number literal
            literal, stream = grab_until(lambda x: not x.isnumeric(), stream)
            return LiteralLexerToken(LiteralLexerTokenKind.NUMBER, first_char + literal), stream

        return None, stream
