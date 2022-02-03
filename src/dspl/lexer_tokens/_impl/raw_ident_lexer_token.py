from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer import grab_until, TextStream
from dspl.lexer_tokens import LexerToken


class RawIdentLexerTokenKind(ValuableEnum):
    RAW_IDENT = "raw_ident"


class RawIdentLexerToken(LexerToken):
    def __init__(self, kind: RawIdentLexerTokenKind, value: str):
        """
        Raw Identifiers can be either keywords or plain identifiers
        """
        self.kind = kind
        self.value = value

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        grabbed, stream = grab_until(lambda x: not x.isalpha(), stream)
        if grabbed:
            return RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "".join(grabbed)), stream

        return None, stream
