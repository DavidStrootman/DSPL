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
        first_char, stream = stream.grab()

        if first_char in StructuralLexerTokenKind.values():
            second_char = stream.peek()

            if first_char+second_char in ComplexStructuralLexerTokenKind.values():
                second_char, stream = stream.grab()
                return StructuralLexerToken(ComplexStructuralLexerTokenKind(first_char+second_char)), stream

            return StructuralLexerToken(StructuralLexerTokenKind(first_char)), stream





        return None, stream
