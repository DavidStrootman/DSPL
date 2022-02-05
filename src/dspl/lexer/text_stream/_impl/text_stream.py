from typing import Callable

from dspl.helper import flatten_rec_seq, mapx, rec_seq, split_last


# TODO: Just refactor everything with context management. This is far too coupled to file IO atm, can't even lex a
# single token without having to create a file to test.


class TextStream:
    """
    TextStream is a static wrapper around the string, "guaranteeing" no side-effects.
    """

    def __init__(self, text: str):
        self._text: str = text

    def grab(self, count: int = 1) -> tuple[str, "TextStream"]:
        """
        Grabs the first count values, calling __next__ on self count times.
        """
        return self._text[0:count], TextStream(self._text[count:])

    def peek(self, count=1) -> str:
        if not self._text:
            return ""

        return self._text[0:count]


def grab_until(pred: Callable[(str), bool], stream: TextStream) -> rec_seq:
    """
    Grab chars from the text string until the delim is reached (exclusive).
    """

    def _grab_until_internal(pred: Callable[(str), bool], stream: "TextStream"):
        peeked_char = stream.peek()

        if pred(peeked_char):
            return ("", stream)

        next_char, stream = stream.grab()

        return (next_char, _grab_until_internal(pred, stream))

    return mapx((lambda x: "".join(x), lambda x: x), split_last(flatten_rec_seq(_grab_until_internal(pred, stream))))
