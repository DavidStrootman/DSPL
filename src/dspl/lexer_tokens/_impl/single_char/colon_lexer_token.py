
from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class ColonLexerTokenKind(ValuableEnum):
    COLON = ":"


class ColonLexerToken(LexerToken):
    def __init__(self, kind: ColonLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in ColonLexerTokenKind.values():
            next(stream)
            return StreamBundle(ColonLexerToken(ColonLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
