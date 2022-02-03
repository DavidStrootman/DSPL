from pathlib import Path

from dspl.lexer import TextStream
from dspl.lexer.lexer import lex_token, lex_file, lex_file_contents


class TestLexer:
    def test_lex_token(self):
        content = "dksnkdnskfls"

        stream = TextStream(content)
        result = lex_token(stream)
        assert result.value == content

    def test_lex_file_contents(self):
        content = "kndfiqwpoieoqw"

    def test_lex_file(self):
        file_name: Path = Path("./test_lex_token")
        content = "AaZz"
        with _LexableFile(file_name) as file:
            lex_token()
