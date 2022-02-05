from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import LexerToken


class WhitespaceLexerTokenKind(ValuableEnum):
    SPACE = " "
    TAB = "\t"
    NEWLINE = "\n"
    RETURN = "\r"


class WhitespaceLexerToken(LexerToken):
    def __init__(self, kind: WhitespaceLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        first_char, stream = stream.grab()

        if first_char in WhitespaceLexerTokenKind.values():
            return WhitespaceLexerToken(WhitespaceLexerTokenKind(first_char)), stream

        return None, stream
