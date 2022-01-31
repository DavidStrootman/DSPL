from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, TextIO

from dspl.lexer_tokens import LexerToken


class TextStream:
    """
    Iterator over tokens. Wraps a TextIO stream, and adds some functionality, such as peeking.
    """

    def __init__(self, file: Path, mode: str, encoding: str = "utf-8"):
        self.file = file
        self.mode = mode
        self.encoding = encoding

        # We cannot guarantee that a context manager has been used, so keep track manually
        self._peeked = []
        self._context = False
        self._IO: Optional[TextIO] = None

    def __enter__(self):
        self._context = True
        self._IO = open(file=self.file, mode=self.mode, encoding=self.encoding)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._IO.close()
        self._context = False

    def peek(self, count:int=1) -> str:
        if not self._context:
            raise ValueError(
                "Tried to get token from a closed file. Make sure the TextStream has been opened using a context manager.")

        self._peeked.extend(list(self._IO.read(count - len(self._peeked))))
        return "".join(self._peeked[0:count])

    def __next__(self):
        """
        Calls a single increment
        """
        if not self._context:
            raise ValueError(
                "Tried to get token from a closed file. Make sure the TextStream has been opened using a context manager.")

        if self._peeked:
            return self._peeked.pop(0)

        return self._IO.read(1)

    def grab(self, count: int):
        """
        Grabs the first count values, calling __next__ on self count times.
        """
        return [next(self) for i in range(count)]

    def grab_until(self, pred: Callable[(str), bool]) -> list[str]:
        """
        Grab chars from the text string until the delim is reached (exclusive).
        """
        next_char = self.peek()

        if pred(next_char):
            return ""

        # We only increment when the next char is not the delimiter
        next(self)
        return next_char + self.grab_until(pred)


@dataclass
class StreamBundle:
    """
    Helper class that bundles a possible Token and the stream it would be collected from.

    """
    token: Optional[LexerToken]
    stream: TextStream
