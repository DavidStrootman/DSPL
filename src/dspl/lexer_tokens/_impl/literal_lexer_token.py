from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import grab_until, TextStream
from dspl.lexer_tokens import LexerToken


class LiteralLexerTokenKind(ValuableEnum):
    NUMBER = "NUMBER"
    STRING = "\""


class LiteralLexerToken(LexerToken):
    """
    Literals describe literal values which are not further parsed.

    Literal Lexer Tokens have two types: "string" and "number".
    Strings are denoted by the use of "", while numbers can be placed
    immediately in code, e.g. 124292. This is because variables can only use A-Za-z.
    """

    def __init__(self, kind: LiteralLexerTokenKind, value: str):
        super().__init__(kind, value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        """
        Try collect this token from a TextStream. Only returns a modified TextStream if the collection succeeds.

        :param stream: The stream to try to collect from.
        :return: If this token can be collected, and instance of this token and the modified TextStream. If this token
        cannot be collected from the stream, returns None and the unmodified stream.
        """
        first_char, modified_stream = stream.grab()

        if first_char in LiteralLexerTokenKind.values():
            # It's a string literal
            literal, modified_stream = grab_until(lambda x: x == first_char, modified_stream)

            # Discard closing double quote
            _, modified_stream = modified_stream.grab()

            return LiteralLexerToken(LiteralLexerTokenKind(first_char), literal), modified_stream

        if first_char.isnumeric():
            # It's a number literal
            literal, modified_stream = grab_until(lambda x: not x.isnumeric(), modified_stream)
            return LiteralLexerToken(LiteralLexerTokenKind.NUMBER, first_char + literal), modified_stream

        return None, stream
