from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer import grab_until, TextStream
from dspl.lexer_tokens import LexerToken


class LiteralLexerTokenKind(ValuableEnum):
    STRING = "\""
    NUMBER = "NUMBER"


class LiteralLexerToken(LexerToken):
    def __init__(self, kind: LiteralLexerTokenKind, value: str):
        """
        Literal Lexer Tokens have two types: "string" and "number".
        Strings are denoted by the use of "", while numbers can be placed
        immediately in code, e.g. 124292. This is because variables can only use A-Za-z.
        """
        super().__init__()

        self.kind = kind
        self.value = value

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        first_char = stream.peek()

        if first_char in LiteralLexerTokenKind.values():
            # It's a string literal
            opening_char, stream = stream.grab()
            literal, stream = grab_until(lambda x: x == opening_char, stream)

            # Discard closing double quote
            _, stream = stream.grab()

            return LiteralLexerToken(LiteralLexerTokenKind(opening_char), literal), stream

        if first_char.isnumeric():
            # It's a number literal
            literal, stream = grab_until(lambda x: not x.isnumeric(), stream)
            return LiteralLexerToken(LiteralLexerTokenKind.NUMBER, literal), stream

        return None, stream
