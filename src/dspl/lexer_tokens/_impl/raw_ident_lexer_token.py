from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import grab_until, TextStream
from dspl.lexer_tokens import LexerToken


class RawIdentLexerTokenKind(ValuableEnum):
    RAW_IDENT = "raw_ident"


class RawIdentLexerToken(LexerToken):
    def __init__(self, kind: RawIdentLexerTokenKind, value: str):
        """
        Raw Identifiers can be either keywords or plain identifiers
        """
        super().__init__(kind, value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        # Since we allow A-Za-z, but not for example Chinese characters, we need to check for both isupper and islower
        # to match both upper and lower case letters (你 would return false on both).
        valid_delims = ["_"]
        grabbed, stream = grab_until(lambda x: not ((x.isupper() or x.islower() ) and x.isalpha() or x in valid_delims), stream)
        if grabbed:
            return RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "".join(grabbed)), stream

        return None, stream
