from typing import Callable

from dspl.helper import flatten_right, mapx, split_last


# TODO: Just refactor everything with context management. This is far too coupled to file IO atm, can't even lex a
# single token without having to create a file to test.


class TextStream:
    """
    A textstream wraps a string, and provides methods which have no side effects.
    """

    def __init__(self, text: str) -> "TextStream":
        self._text: str = text

    def grab(self, count: int = 1) -> tuple[str, "TextStream"]:
        """
        Splits the textstream into a string of count length, and the new modified TextStream.

        :param count: The amount of characters to split from the start.
        :return: count characters and a new modified TextStream.
        """
        return self._text[0:count], TextStream(self._text[count:])

    def peek(self, count=1) -> str:
        """
        Peek this TextStream without modifying it.

        :param count: The amount of characters to peek from the start.
        :return: The peeked characters.
        """
        if not self._text:
            return ""

        return self._text[0:count]


def grab_until(pred: Callable[(str), bool], stream: TextStream) -> tuple[str, TextStream]:
    """
    Grab chars from the beginning of the TextStream until the predicate is true for the next character (exclusive).

    :param pred: The predicate which breaks the loop once it is True for the next character.
    :param stream: The TextStream to grab from.
    :return: The grabbed string and a new modified TextStream
    """

    def _grab_until_internal(pred: Callable[(str), bool], stream: "TextStream"):
        peeked_char = stream.peek()

        if pred(peeked_char):
            return ("", stream)

        next_char, stream = stream.grab()

        return (next_char, _grab_until_internal(pred, stream))

    return mapx((lambda x: "".join(x), lambda x: x), split_last(flatten_right(_grab_until_internal(pred, stream))))
