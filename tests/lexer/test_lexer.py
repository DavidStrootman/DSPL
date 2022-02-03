from pathlib import Path

import pytest

from dspl.lexer import lex_token
from dspl.lexer.text_stream import TextStream


class TestLexer:
    def test_lex_token(self):
        content = "dksnkdnskfls"

        stream = TextStream(content)
        result, _ = lex_token(stream)
        assert result.value == content

    def test_lex_token_invalid(self):
        content = "你好dksnkdnskfls"
        stream = TextStream(content)

        with pytest.raises(RuntimeError):
            result, _ = lex_token(stream)

    def test_lex_token_none(self):
        content = ""
        stream = TextStream(content)

        with pytest.raises(ValueError):
            result, _ = lex_token(stream)

    def test_lex_file_contents(self):
        content = "kndfiqwpoieoqw"

    def test_lex_file(self):
        pass