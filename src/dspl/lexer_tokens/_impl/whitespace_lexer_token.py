from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class WhiteSpaceLexerTokenKind(ValuableEnum):
    SPACE = " "
    TAB = "\t"
    NEWLINE = "\n"
    RETURN = "\r"


class WhitespaceLexerToken(LexerToken):
    def __init__(self, kind: WhiteSpaceLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in WhiteSpaceLexerTokenKind.values():
            value = next(stream)
            return StreamBundle(WhitespaceLexerToken(WhiteSpaceLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
