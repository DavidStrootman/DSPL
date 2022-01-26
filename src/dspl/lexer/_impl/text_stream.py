from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TextIO

from dspl.lexer_tokens import LexerToken


class TextStream:
    """
    Iterator over tokens. Wraps a TextIO stream, and adds some functionality.
    """

    def __init__(self, file: Path, mode: str, encoding: str = "utf-8"):
        self.file = file
        self.mode = mode
        self.encoding = encoding

        # We cannot guarantee that a context manager has been used, so keep track manually
        self._context = False
        self._IO: Optional[TextIO] = None

    def __enter__(self):
        self._context = True
        self._IO = open(file=self.file, mode=self.mode, encoding=self.encoding)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._IO.close()
        self._context = False

    def peek(self):
        pass

    def __next__(self):
        """
        Calls a single increment
        """
        if not self._context:
            raise ValueError(
                "Tried to get token from a closed file. Make sure the TextStream has been opened using a context manager.")

        return next(self.contents)


@dataclass
class StreamBundle:
    """
    Helper class that bundles a possible Token and the stream it would be collected from.

    """
    token: Optional[LexerToken]
    stream: TextStream
