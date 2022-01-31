from dspl.helper import ValuableEnum
from dspl.lexer import TextStream, StreamBundle
from dspl.lexer_tokens import LexerToken


class StructuralLexerTokenKind(ValuableEnum):
    SEMICOLON = ";"
    COLON = ":"
    DOT = "."
    COMMA = ","
    LESSER = "<"


class ComplexStructuralLexerTokenKind(ValuableEnum):
    ARROW = "->"


class StructuralLexerToken(LexerToken):
    def __init__(self, kind: StructuralLexerTokenKind | ComplexStructuralLexerTokenKind):
        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        first_two_chars = stream.peek(2)

        if first_two_chars in ComplexStructuralLexerTokenKind.values():
            stream.grab(2)
            return StreamBundle(StructuralLexerToken(ComplexStructuralLexerTokenKind(first_two_chars)),
                                stream)

        first_char = stream.peek()

        if first_char in StructuralLexerTokenKind.values():
            next(stream)
            return StreamBundle(StructuralLexerToken(StructuralLexerTokenKind(first_char)), stream)

        return StreamBundle(None, stream)
