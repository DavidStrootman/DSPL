import pytest

from dspl.lexer import lex_token

from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import ComplexOpLexerTokenKind, ComplexStructuralLexerTokenKind, DelimLexerToken, \
    DelimLexerTokenKind, KeywordLexerToken, \
    KeywordLexerTokenKind, \
    LexerToken, LiteralLexerToken, LiteralLexerTokenKind, OpLexerToken, OpLexerTokenKind, RawIdentLexerToken, \
    RawIdentLexerTokenKind, StructuralLexerToken, StructuralLexerTokenKind, WhitespaceLexerToken, \
    WhitespaceLexerTokenKind


class TestLexerToken:
    def test_construct(self):
        # Assert the base class gets constructed properly and the definition does not change
        assert isinstance(LexerToken(LexerToken._Types.UNSET, "SOME UNSET VALUE"), LexerToken)


class TestDelimLexerToken:
    def test_construct(self):
        # Assert all token kinds can be constructed
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
        # Assert an exception is raised whenever trying to collect from None
        with pytest.raises(Exception):
            DelimLexerToken.try_collect(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream("("))[0]
        assert lexed_token.kind == DelimLexerToken(DelimLexerTokenKind.OPEN_ROUND).kind
        assert lexed_token.value == DelimLexerToken(DelimLexerTokenKind.OPEN_ROUND).value


class TestKeyWordLexerToken:
    def test_construct(self):
        # Assert all token kinds can be constructed
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

        # Assert not all tokens get turned into keyword tokens
        assert KeywordLexerToken.from_raw_ident(not_a_keyword_ident) == not_a_keyword_ident

    def test_from_raw_ident_none(self):
        # Assert an exception is raised whenever trying to collect from None
        with pytest.raises(Exception):
            KeywordLexerToken.from_raw_ident(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream("fn"))[0]
        assert lexed_token.kind == RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "fn").kind
        assert lexed_token.value == RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "fn").value


class TestLiteralLexerToken:
    def test_construct(self):
        # Assert both token kinds can be constructed
        assert isinstance(LiteralLexerToken(LiteralLexerTokenKind.NUMBER, "29"), LiteralLexerToken)
        assert isinstance(LiteralLexerToken(LiteralLexerTokenKind.STRING, "\"29\""), LiteralLexerToken)

    def test_try_collect(self, helpers):
        collectable_text = {
            "187238": LiteralLexerTokenKind.NUMBER,
            "\"21312\"": LiteralLexerTokenKind.STRING,
            "\"jshdfjsa\"": LiteralLexerTokenKind.STRING,
            "\"??????dsfd\"": LiteralLexerTokenKind.STRING,
            # Chill Dino, he's vibing
            "\"????\"": LiteralLexerTokenKind.STRING,
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
        # Assert an exception is raised whenever trying to collect from None
        with pytest.raises(Exception):
            LiteralLexerToken.try_collect(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream("\"some_string\""))[0]
        assert lexed_token.kind == LiteralLexerToken(LiteralLexerTokenKind.STRING, "some_string").kind
        assert lexed_token.value == LiteralLexerToken(LiteralLexerTokenKind.STRING, "some_string").value


class TestOpLexerToken:
    def test_construct(self):
        # Assert all token kinds can be constructed
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
        # Assert not all tokens get turned into structural tokens
        assert OpLexerToken.try_collect(TextStream(text))[0] is None

    def test_try_collect_none(self):
        # Assert an exception is raised whenever trying to collect from None
        with pytest.raises(Exception):
            OpLexerToken.try_collect(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream("="))[0]
        assert lexed_token.kind == OpLexerToken(OpLexerTokenKind.ASSIGN).kind
        assert lexed_token.value == OpLexerToken(OpLexerTokenKind.ASSIGN).value


class TestRawIdentLexerToken:
    def test_construct(self):
        # Assert all token kinds can be constructed
        for kind in RawIdentLexerTokenKind:
            assert RawIdentLexerToken(kind, kind.value).kind == kind
            assert RawIdentLexerToken(kind, kind.value).value == kind.value

    def test_try_collect(self, helpers):
        collectable_text = [
            "this_is_an_identifier",
            "_a_",
            "_",
        ]

        # Assert all valid text can be collected
        for text in collectable_text:
            helpers.assert_collect_from_string(text, RawIdentLexerToken, RawIdentLexerTokenKind.RAW_IDENT, text)

    def test_try_collect_negative(self):
        non_collectable_text = [
            "0this_identifier_is_after_a_literal",
            "\"this_is_a_literal\"",
            "-",
            "????",
            ""
        ]
        # Assert some invalid literals do not get turned into lexer tokens
        for text in non_collectable_text:
            assert RawIdentLexerToken.try_collect(TextStream(text))[0] is None

    def test_try_collect_none(self):
        # Assert an exception is raised whenever trying to collect from None
        with pytest.raises(Exception):
            RawIdentLexerToken.try_collect(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream("some_ident"))[0]
        assert lexed_token.kind == RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "some_ident").kind
        assert lexed_token.value == RawIdentLexerToken(RawIdentLexerTokenKind.RAW_IDENT, "some_ident").value


class TestStructuralLexerToken:
    def test_construct(self):
        # Assert all token kinds can be constructed
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
        # Assert not all tokens get turned into structural tokens
        assert StructuralLexerToken.try_collect(TextStream(text))[0] is None

    def test_try_collect_none(self):
        # Assert an exception is raised whenever trying to collect from None
        with pytest.raises(Exception):
            StructuralLexerToken.try_collect(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream(";"))[0]
        assert lexed_token.kind == StructuralLexerToken(StructuralLexerTokenKind.SEMICOLON).kind
        assert lexed_token.value == StructuralLexerToken(StructuralLexerTokenKind.SEMICOLON).value


class TestWhitespaceLexerToken:
    def test_construct(self):
        # Assert all token kinds can be constructed
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
        # Assert not all values get turned into whitespacetokens
        assert WhitespaceLexerToken.try_collect(TextStream(text))[0] is None

        no_text = ""
        # Assert no exception is raised for no text
        assert WhitespaceLexerToken.try_collect(TextStream(no_text))[0] is None

    def test_try_collect_none(self):
        with pytest.raises(Exception):
            WhitespaceLexerToken.try_collect(None)

    def test_lex(self):
        lexed_token = lex_token(TextStream(" "))[0]
        assert lexed_token.kind == WhitespaceLexerToken(WhitespaceLexerTokenKind.SPACE).kind
        assert lexed_token.value == WhitespaceLexerToken(WhitespaceLexerTokenKind.SPACE).value
