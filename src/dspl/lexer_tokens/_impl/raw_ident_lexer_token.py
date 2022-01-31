from dspl.helper import ValuableEnum
from dspl.lexer import TextStream, StreamBundle
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
    def try_collect(stream: TextStream) -> StreamBundle:
        grabbed = stream.grab_until(lambda x: not x.isalpha())
        if grabbed:
            return StreamBundle(RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "".join(grabbed)), stream)

        return StreamBundle(None, stream)
