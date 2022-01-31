
from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class DelimLexerTokenKind(ValuableEnum):
    OPEN_ROUND = "("
    CLOSE_ROUND = ")"
    OPEN_SQUARE = "["
    CLOSE_SQUARE = "]"
    OPEN_CURLY = "{"
    CLOSE_CURLY = "}"
    OPEN_ANGLE = "<"
    CLOSE_ANGLE = ">"


class DelimLexerToken(LexerToken):
    def __init__(self, kind: DelimLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in DelimLexerTokenKind.values():
            next(stream)
            return StreamBundle(DelimLexerToken(DelimLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
