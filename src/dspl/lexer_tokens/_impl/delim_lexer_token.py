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
    """
    This token describes all delimiters that can be lexed from a DSPL file.
    Delimiters are only the brackets in this context, since the other delimiters such as comma are considered
    structural.
    """

    def __init__(self, kind: DelimLexerTokenKind):
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

        if first_char in DelimLexerTokenKind.values():
            return DelimLexerToken(DelimLexerTokenKind(first_char)), modified_stream

        return None, stream
