from typing import Type

from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken
from dspl.lexer.text_stream import TextStream


def assert_collect_from_string(text: str, token: Type[LexerToken], expected_kind: ValuableEnum):
    stream = TextStream(text)

    token = token.try_collect(stream)

    assert token[0].kind == expected_kind
    assert token[0].value == expected_kind.value
