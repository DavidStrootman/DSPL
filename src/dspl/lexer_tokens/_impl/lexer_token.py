from enum import Enum

from dspl.helper import PrintableABC


class LexerToken(PrintableABC):
    class _Types(Enum):
        UNSET = "UNSET"

    def match(self, content: str):
        pass
