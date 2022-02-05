from ast import literal_eval
import pytest

from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import ComplexOpLexerTokenKind, ComplexStructuralLexerTokenKind, DelimLexerToken, \
    DelimLexerTokenKind, KeywordLexerToken, \
    KeywordLexerTokenKind, \
    LexerToken, LiteralLexerToken, LiteralLexerTokenKind, OpLexerToken, OpLexerTokenKind, RawIdentLexerToken, \
    RawIdentLexerTokenKind, StructuralLexerToken, StructuralLexerTokenKind, WhitespaceLexerToken, \
    WhitespaceLexerTokenKind


class TestLexerToken:
    def test_construct(self):
        assert isinstance(LexerToken(LexerToken._Types.UNSET, "SOME UNSET VALUE"), LexerToken)


class TestDelimLexerToken:
    def test_construct(self):
        for kind in DelimLexerTokenKind:
            assert DelimLexerToken(kind).kind == kind
            assert DelimLexerToken(kind).value == kind.value

    def test_try_collect(self, helpers):
        collectable_text = {
            "(": DelimLexerTokenKind.OPEN_ROUND,
            ")": DelimLexerTokenKind.CLOSE_ROUND,
            "[": DelimLexerTokenKind.OPEN_SQUARE,
            "]": DelimLexerTokenKind.CLOSE_SQUARE,
            "{": DelimLexerTokenKind.OPEN_CURLY,
            "}": DelimLexerTokenKind.CLOSE_CURLY,
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            helpers.assert_collect_from_string(text, DelimLexerToken, expected)

    def test_try_collect_negative(self):
        content = "this_is_not_a_delimiter"

        result = DelimLexerToken.try_collect(TextStream(content))

        # Assert no token was parsed
        assert result[0] is None

        content = "8"

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


class TestKeyWordLexerToken:
    def test_construct(self):
        for kind in KeywordLexerTokenKind:
            assert KeywordLexerToken(kind).kind == kind
            assert KeywordLexerToken(kind).value == kind.value

    def test_from_raw_ident(self):
        collectable_text = {
            "fn": KeywordLexerTokenKind.FUNCTION,
            "return": KeywordLexerTokenKind.RETURN,
            "bind": KeywordLexerTokenKind.BIND,
            "if": KeywordLexerTokenKind.IF,
            "else": KeywordLexerTokenKind.ELSE,
            "while": KeywordLexerTokenKind.WHILE,
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            assert KeywordLexerToken.from_raw_ident(
                RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, text)).kind == expected

    def test_from_raw_ident_negative(self):
        text = "this_is_not_a_keyword"

        not_a_keyword_ident = RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, text)

        assert KeywordLexerToken.from_raw_ident(not_a_keyword_ident) == not_a_keyword_ident

    def test_from_raw_ident_none(self):
        with pytest.raises(Exception):
            KeywordLexerToken.from_raw_ident(None)


class TestLiteralLexerToken:
    def test_construct(self):
        assert isinstance(LiteralLexerToken(LiteralLexerTokenKind.NUMBER, "29"), LiteralLexerToken)

    def test_try_collect(self, helpers):
        collectable_text = {
            "187238": LiteralLexerTokenKind.NUMBER,
            "\"21312\"": LiteralLexerTokenKind.STRING,
            "\"jshdfjsa\"": LiteralLexerTokenKind.STRING,
            "\"你好dsfd\"": LiteralLexerTokenKind.STRING,
            # Chill Dino, he's vibing
            "\"🦕\"": LiteralLexerTokenKind.STRING,
            "\"(\"": LiteralLexerTokenKind.STRING,
            "\"\\\"": LiteralLexerTokenKind.STRING,
            "\"\"": LiteralLexerTokenKind.STRING,
            "\" \"": LiteralLexerTokenKind.STRING,
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            helpers.assert_collect_from_string(text, LiteralLexerToken, expected, text.strip("\""))

    def test_try_collect_negative(self):
        content = "*"

        result = LiteralLexerToken.try_collect(TextStream(content))

        # Assert no token was parsed
        assert result[0] is None

        # This is a raw identifier, not a string
        content = "a"

        result = LiteralLexerToken.try_collect(TextStream(content))

        # Assert no token was parsed
        assert result[0] is None

        content2 = ""

        result = LiteralLexerToken.try_collect(TextStream(content2))

        # Assert no token was parsed
        assert result[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            LiteralLexerToken.try_collect(None)


class TestOpLexerToken:
    def test_construct(self):
        for kind in OpLexerTokenKind:
            assert OpLexerToken(kind).kind == kind
            assert OpLexerToken(kind).value == kind.value

    def test_try_collect(self, helpers):
        collectable_text = {
            "-": OpLexerTokenKind.SUBTRACTION,
            "+": OpLexerTokenKind.ADDITION,
            "=": OpLexerTokenKind.ASSIGN,
            ">": OpLexerTokenKind.GREATER,
            "<": OpLexerTokenKind.LESSER,

            ">=": ComplexOpLexerTokenKind.GREATER_EQUAL,
            "<=": ComplexOpLexerTokenKind.LESSER_EQUAL,
            "==": ComplexOpLexerTokenKind.EQUAL,
            "!=": ComplexOpLexerTokenKind.NOT_EQUAL,
            "+=": ComplexOpLexerTokenKind.ADDITION_ASSIGN,
            "-=": ComplexOpLexerTokenKind.SUBTRACTION_ASSIGN
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            helpers.assert_collect_from_string(text, OpLexerToken, expected)

    def test_try_collect_negative(self):
        text = "not_an_op"
        assert OpLexerToken.try_collect(TextStream(text))[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            OpLexerToken.try_collect(None)


class TestRawIdentLexerToken:
    def test_construct(self):
        for kind in RawIdentLexerTokenKind:
            assert RawIdentLexerToken(kind, kind.value).kind == kind
            assert RawIdentLexerToken(kind, kind.value).value == kind.value

    def test_try_collect(self, helpers):
        collectable_text = [
            "this_is_an_identifier",
            "_a_",
            "_",
        ]

        for text in collectable_text:
            helpers.assert_collect_from_string(text, RawIdentLexerToken, RawIdentLexerTokenKind.RAW_IDENT, text)

    def test_try_collect_negative(self):
        non_collectable_text = [
            "0this_identifier_is_after_a_literal",
            "\"this_is_a_literal\"",
            "-",
            "🦕",
            ""
        ]
        for text in non_collectable_text:
            assert RawIdentLexerToken.try_collect(TextStream(text))[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            RawIdentLexerToken.try_collect(None)


class TestStructuralLexerToken:
    def test_construct(self):
        for kind in RawIdentLexerTokenKind:
            assert RawIdentLexerToken(kind, kind.value).kind == kind
            assert RawIdentLexerToken(kind, kind.value).value == kind.value

    def test_try_collect(self, helpers):
        collectable_text = {
            ";": StructuralLexerTokenKind.SEMICOLON,
            ":": StructuralLexerTokenKind.COLON,
            ".": StructuralLexerTokenKind.DOT,
            ",": StructuralLexerTokenKind.COMMA,
            "->": ComplexStructuralLexerTokenKind.ARROW
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            helpers.assert_collect_from_string(text, StructuralLexerToken, expected)

    def test_try_collect_negative(self):
        text = "-"

        assert StructuralLexerToken.try_collect(TextStream(text))[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            StructuralLexerToken.try_collect(None)


class TestWhitespaceLexerToken:
    def test_construct(self):
        for kind in WhitespaceLexerTokenKind:
            assert WhitespaceLexerToken(kind).kind == kind
            assert WhitespaceLexerToken(kind).value == kind.value

    def test_try_collect(self, helpers):
        collectable_text = {
            " ": WhitespaceLexerTokenKind.SPACE,
            "\t": WhitespaceLexerTokenKind.TAB,
            "\n": WhitespaceLexerTokenKind.NEWLINE,
            "\r": WhitespaceLexerTokenKind.RETURN
        }

        # Assert all valid text can be collected
        for text, expected in collectable_text.items():
            helpers.assert_collect_from_string(text, WhitespaceLexerToken, expected)

    def test_try_collect_negative(self):
        text = "some_value"
        assert WhitespaceLexerToken.try_collect(TextStream(text))[0] is None

        no_text = ""
        assert WhitespaceLexerToken.try_collect(TextStream(no_text))[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            WhitespaceLexerToken.try_collect(None)
