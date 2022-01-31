
from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class CommaLexerTokenKind(ValuableEnum):
    COMMA = ","


class CommaLexerToken(LexerToken):
    def __init__(self, kind: CommaLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in CommaLexerTokenKind.values():
            next(stream)
            return StreamBundle(CommaLexerToken(CommaLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
