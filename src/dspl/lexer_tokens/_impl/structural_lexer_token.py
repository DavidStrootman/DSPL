from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import LexerToken


class StructuralLexerTokenKind(ValuableEnum):
    SEMICOLON = ";"
    COLON = ":"
    DOT = "."
    COMMA = ","


class ComplexStructuralLexerTokenKind(ValuableEnum):
    ARROW = "->"


class StructuralLexerToken(LexerToken):
    def __init__(self, kind: StructuralLexerTokenKind | ComplexStructuralLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def try_collect(stream: TextStream) -> tuple[LexerToken, TextStream]:
        """
        Try collect this token from a TextStream. Only returns a modified TextStream if the collection succeeds.

        :param stream: The stream to try to collect from.
        :return: If this token can be collected, and instance of this token and the modified TextStream. If this token
        cannot be collected from the stream, returns None and the unmodified stream.
        """
        first_char, modified_stream = stream.grab()
        second_char = modified_stream.peek()

        if first_char + second_char in ComplexStructuralLexerTokenKind.values():
            second_char, modified_stream = modified_stream.grab()
            return StructuralLexerToken(ComplexStructuralLexerTokenKind(first_char + second_char)), modified_stream

        if first_char in StructuralLexerTokenKind.values():
            return StructuralLexerToken(StructuralLexerTokenKind(first_char)), modified_stream

        return None, stream
