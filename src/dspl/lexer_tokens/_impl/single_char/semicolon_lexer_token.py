
from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class SemiColonLexerTokenKind(ValuableEnum):
    SEMICOLON = ";"


class SemiColonLexerToken(LexerToken):
    def __init__(self, kind: SemiColonLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in SemiColonLexerTokenKind.values():
            next(stream)
            return StreamBundle(SemiColonLexerToken(SemiColonLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
