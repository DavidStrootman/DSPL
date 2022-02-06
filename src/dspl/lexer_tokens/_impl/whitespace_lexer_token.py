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
    """
    Whitespace tokens describe all allowed types of whitespace read from a DSPL file. They are consumed during expansion
    of a simple lexer token.
    """
    def __init__(self, kind: WhitespaceLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        """
        Try collect this token from a TextStream. Only returns a modified TextStream if the collection succeeds.

        :param stream: The stream to try to collect from.
        :return: If this token can be collected, and instance of this token and the modified TextStream. If this token
        cannot be collected from the stream, returns None and the unmodified stream.
        """
        first_char, modified_stream = stream.grab()

        if first_char in WhitespaceLexerTokenKind.values():
            return WhitespaceLexerToken(WhitespaceLexerTokenKind(first_char)), modified_stream

        return None, stream
