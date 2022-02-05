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
    def __init__(self, kind: OpLexerTokenKind | ComplexOpLexerTokenKind):
        super().__init__(kind, kind.value)


    @staticmethod
    def try_collect(stream: TextStream) -> tuple[Optional[LexerToken], TextStream]:
        first_char, stream = stream.grab()
        second_char = stream.peek()

        if first_char+second_char in ComplexOpLexerTokenKind.values():
            second_char, stream = stream.grab()
            return OpLexerToken(ComplexOpLexerTokenKind(first_char+second_char)), stream

        if first_char in OpLexerTokenKind.values():
            return OpLexerToken(OpLexerTokenKind(first_char)), stream

        return None, stream
