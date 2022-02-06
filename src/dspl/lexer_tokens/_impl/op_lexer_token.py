from typing import Optional

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import LexerToken


class OpLexerTokenKind(ValuableEnum):
    SUBTRACTION = "-"
    ADDITION = "+"
    ASSIGN = "="
    GREATER = ">"
    LESSER = "<"


class ComplexOpLexerTokenKind(ValuableEnum):
    GREATER_EQUAL = ">="
    LESSER_EQUAL = "<="
    EQUAL = "=="
    NOT_EQUAL = "!="
    ADDITION_ASSIGN = "+="
    SUBTRACTION_ASSIGN = "-="


class OpLexerToken(LexerToken):
    """
    Operators are the symbols used for logical, mathematical or assignment operations.
    Operators are used to change the state of the program.

    """
    def __init__(self, kind: OpLexerTokenKind | ComplexOpLexerTokenKind):
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
        second_char = modified_stream.peek()

        if first_char + second_char in ComplexOpLexerTokenKind.values():
            second_char, modified_stream = modified_stream.grab()
            return OpLexerToken(ComplexOpLexerTokenKind(first_char + second_char)), modified_stream

        if first_char in OpLexerTokenKind.values():
            return OpLexerToken(OpLexerTokenKind(first_char)), modified_stream

        return None, stream
