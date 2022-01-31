
from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class DotLexerTokenKind(ValuableEnum):
    DOT = "."


class DotLexerToken(LexerToken):
    def __init__(self, kind: DotLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in DotLexerTokenKind.values():
            next(stream)
            return StreamBundle(DotLexerToken(DotLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
