from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import LexerToken


class WhiteSpaceLexerTokenKind(ValuableEnum):
    SPACE = " "
    TAB = "\t"
    NEWLINE = "\n"
    RETURN = "\r"


class WhitespaceLexerToken(LexerToken):
    def __init__(self, kind: WhiteSpaceLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        first_char, stream = stream.grab()

        if first_char in WhiteSpaceLexerTokenKind.values():
            return WhitespaceLexerToken(WhiteSpaceLexerTokenKind(first_char)), stream

        return None, stream
