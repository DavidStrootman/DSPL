from dspl.helper import ValuableEnum
from dspl.lexer import TextStream
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
        super().__init__()

        self.kind = kind
        self.value = kind.value

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[LexerToken, TextStream]:
        first_two_chars = stream.peek(2)

        if first_two_chars in ComplexStructuralLexerTokenKind.values():
            _, stream = stream.grab(2)
            return StructuralLexerToken(ComplexStructuralLexerTokenKind(first_two_chars)), stream

        first_char = stream.peek()

        if first_char in StructuralLexerTokenKind.values():
            _, stream = stream.grab()
            return StructuralLexerToken(StructuralLexerTokenKind(first_char)), stream

        return None, stream
