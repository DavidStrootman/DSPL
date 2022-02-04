from collections.abc import Sequence
import pytest

from dspl.lexer import lex_file, lex_file_contents, lex_token
from dspl.lexer.text_stream import TextStream
from dspl.lexer_tokens import LexerToken


class TestLexer:
    def test_lex_token(self):
        content = "dksnkdnskfls"

        stream = TextStream(content)
        result, _ = lex_token(stream)
        assert result.value == content

    def test_lex_token_negative(self):
        content = "你好dksnkdnskfls"
        stream = TextStream(content)

        with pytest.raises(Exception):
            result, _ = lex_token(stream)

    def test_lex_token_none(self):
        content = ""
        stream = TextStream(content)

        with pytest.raises(Exception):
            result, _ = lex_token(stream)

    def test_lex_file_contents(self):
        content1 = "kndfiqwpoieoqw"
        content2 = " "
        content3 = "dfd"
        stream = TextStream(content1 + content2 + content3)
        result = list(lex_file_contents(stream))

        assert len(result) == 3
        assert "".join([token.value for token in result]) == content1 + content2 + content3

    def test_lex_file_contents_negative(self):
        content1 = "kndfiqwpoieoqw"
        content2 = ""
        content3 = ""
        stream = TextStream(content1 + content2 + content3)
        result = list(lex_file_contents(stream))

        assert len(result) != 3
        assert len(result) == 1

        assert "".join([token.value for token in result]) == content1 + content2 + content3
        assert "".join([token.value for token in result]) == content1

    def test_lex_file_contents_none(self):
        content = ""
        stream = TextStream(content)
        result = list(lex_file_contents(stream))

        assert len(result) == 0
        # Assert the returned value is empty and no error is raised.
        assert "".join([token.value for token in result]) == content

    def test_lex_file(self, tmp_path):
        content = "sajflajiw"
        file = tmp_path / "test_lex_file.dspl"

        file.write_text(content)
        # Assert the file is created correctly
        assert file.read_text() == content

        result = lex_file(file)

        # Assert some sequence of tokens was returned
        assert isinstance(result, Sequence)
        assert isinstance(result[0], LexerToken)

        # Assert the first token holds the content provided
        assert result[0].value == content

    def test_lex_file_negative(self, tmp_path):
        content = ""
        file = tmp_path / "test_lex_file_negative.dspl"

        file.write_text(content)

        # Assert the file is created correctly
        assert file.read_text() == content

        result = lex_file(file)

        # Assert some sequence without tokens was returned
        assert isinstance(result, Sequence)
        assert len(result) == 0

    def test_lex_file_none(self, tmp_path):
        with pytest.raises(Exception):
            lex_file(None)
