from typing import Type, TYPE_CHECKING

import pytest

from dspl.helper import ValuableEnum
from dspl.lexer.text_stream import TextStream
from abc import ABC

if TYPE_CHECKING:
    from dspl.lexer_tokens import LexerToken


class Helpers(ABC):
    @staticmethod
    def assert_collect_from_string(text: str,
                                   token: Type["LexerToken"],
                                   expected_kind: ValuableEnum,
                                   expected_value="No expected value provided"):
        stream = TextStream(text)

        token, stream = token.try_collect(stream)

        if expected_value == "No expected value provided":
            expected_value = expected_kind.value

        assert token.kind == expected_kind
        assert token.value == expected_value


@pytest.fixture
def helpers():
    return Helpers
