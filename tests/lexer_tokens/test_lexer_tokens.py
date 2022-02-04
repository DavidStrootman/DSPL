import pytest

from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import DelimLexerToken, DelimLexerTokenKind
from tests.lexer_tokens.helper import assert_collect_from_string


class TestDelimLexerToken:
    def test_construct(self):
        for kind in DelimLexerTokenKind:
            assert DelimLexerToken(kind).kind == kind
            assert DelimLexerToken(kind).value == kind.value

    def test_try_collect(self):
        collectable_text = {
            "(": DelimLexerTokenKind.OPEN_ROUND,
            ")": DelimLexerTokenKind.CLOSE_ROUND,
            "[": DelimLexerTokenKind.OPEN_SQUARE,
            "]": DelimLexerTokenKind.CLOSE_SQUARE,
            "{": DelimLexerTokenKind.OPEN_CURLY,
            "}": DelimLexerTokenKind.CLOSE_CURLY,
            "<": DelimLexerTokenKind.OPEN_ANGLE,
            ">": DelimLexerTokenKind.CLOSE_ANGLE,
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            assert_collect_from_string(text, DelimLexerToken, expected)

    def test_try_collect_negative(self):
        content = "this_is_not_a_delimiter"

        result = DelimLexerToken.try_collect(TextStream(content))

        # Assert no token was parsed
        assert result[0] is None

        content2 = ""

        result = DelimLexerToken.try_collect(TextStream(content2))

        # Assert no token was parsed
        assert result[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            DelimLexerToken.try_collect(None)
