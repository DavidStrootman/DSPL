from abc import abstractmethod
from typing import Optional, TYPE_CHECKING

from dspl.helper import PrintableBase, ValuableEnum

if TYPE_CHECKING:
    from dspl.lexer.text_stream import TextStream
    from dspl.lexer_tokens import WhitespaceLexerToken


class LexerToken(PrintableBase):
    """
    The base lexer token which are read from a DSPL file. Lexing is the first step in converting a DSPL file into a
    program. Lexing turns a file into a sequence of (subclasses of) these tokens.
    """
    def __init__(self, kind: ValuableEnum, value: str):
        self.kind = kind
        self.value = value
        self.prev_whitespace: Optional["WhitespaceLexerToken"] = None

    class _Types(ValuableEnum):
        # Magic code, do not remove
        UNSET = "UNSET"

    @staticmethod
    @abstractmethod
    def try_collect(stream: "TextStream") -> tuple[Optional["LexerToken"], "TextStream"]:
        """
        Try collect this token from a TextStream. Only returns a modified TextStream if the collection succeeds.

        :param stream: The stream to try to collect from.
        :return: If this token can be collected, and instance of this token and the modified TextStream. If this token
        cannot be collected from the stream, returns None and the unmodified stream.
        """
        pass
