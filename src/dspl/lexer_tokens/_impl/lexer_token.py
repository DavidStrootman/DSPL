from enum import Enum

from dspl.helper import PrintableBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dspl.lexer_tokens import WhitespaceLexerToken


class LexerToken(PrintableBase):
    def __init__(self):
        self.prev_whitespace: Optional["WhitespaceLexerToken"] = None

    class _Types(Enum):
        UNSET = "UNSET"

    def match(self, content: str):
        pass
