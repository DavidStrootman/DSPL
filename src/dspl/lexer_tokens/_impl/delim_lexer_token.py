from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken
from dspl.lexer.text_stream import TextStream


class DelimLexerTokenKind(ValuableEnum):
    OPEN_ROUND = "("
    CLOSE_ROUND = ")"
    OPEN_SQUARE = "["
    CLOSE_SQUARE = "]"
    OPEN_CURLY = "{"
    CLOSE_CURLY = "}"



class DelimLexerToken(LexerToken):
    def __init__(self, kind: DelimLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        first_char, stream = stream.grab()

        if first_char in DelimLexerTokenKind.values():
            return DelimLexerToken(DelimLexerTokenKind(first_char)), stream

        return None, stream
