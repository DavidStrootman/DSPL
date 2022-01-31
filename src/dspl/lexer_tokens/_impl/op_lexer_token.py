from dspl.helper import ValuableEnum
from dspl.lexer import TextStream, StreamBundle
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
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_char = stream.peek()

        if first_char in OpLexerTokenKind.values():
            first_two_chars = stream.peek(2)

            if first_two_chars in ComplexOpLexerTokenKind.values():
                stream.grab(2)
                return StreamBundle(OpLexerToken(ComplexOpLexerTokenKind(first_two_chars)), stream)

            next(stream)
            return StreamBundle(OpLexerToken(OpLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
