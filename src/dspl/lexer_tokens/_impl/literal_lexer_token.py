from dspl.helper import ValuableEnum
from dspl.lexer import TextStream, StreamBundle
from dspl.lexer_tokens import LexerToken


class LiteralLexerTokenKind(ValuableEnum):
    STRING = "\""
    NUMBER = "UNSET_NUMBER"


class LiteralLexerToken(LexerToken):
    def __init__(self, kind: LiteralLexerTokenKind, value: str):
        self.kind = kind
        self.value = value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in LiteralLexerTokenKind.values():
            # It's a string literal
            opening_char: str = next(stream)
            literal: str = "".join(stream.grab_until(lambda x: x == opening_char))

            # Discard closing double quote
            next(stream)

            return StreamBundle(LiteralLexerToken(LiteralLexerTokenKind(opening_char), literal), stream)

        if first_char.isnumeric():
            # It's a number literal
            literal = "".join(stream.grab_until(lambda x: not x.isnumeric()))
            return StreamBundle(LiteralLexerToken(LiteralLexerTokenKind.NUMBER, literal), stream)

        return StreamBundle(None, stream)
