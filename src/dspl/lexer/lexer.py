"""Lexer, also known as a Tokenizer.

Supplies functionality for reading text from a file and changing them into tokens the parser can accept.
"""
from collections.abc import Iterator, Iterable
from functools import partial
from itertools import chain, starmap
from pathlib import Path
import re
from typing import TYPE_CHECKING, TypeAlias, TextIO

from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken, DelimLexerToken, KeywordLexerToken, LiteralLexerToken, OpLexerToken, \
    WhitespaceLexerToken
from dspl.lexer.lex_util import DebugData, Word

FileLexer: TypeAlias = Iterator[LexerToken]

_WordReader: TypeAlias = Iterator[Word]


def lex_file(file: Path) -> FileLexer:
    """
    Lex all tokens from a file.

    :param file: Path to the file to lex.
    :return: An iterator over lexer tokens.
    """
    with TextStream(file, 'r', encoding="utf-8") as input_stream:
        contents = lex_file_contents(input_stream)

        print("hey")

def lex_file_contents(stream: TextStream) -> Iterator[LexerToken]:
    return _exhaustive_lex_tokens(stream)


def _exhaustive_lex_tokens(stream: TextStream) -> Iterator[LexerToken]:
    if not stream:
        return
    else:
        # We do a little unpacking
        bundle = lex_token(stream)
        yield bundle.token
        yield from _exhaustive_lex_tokens(bundle.stream)


def lex_token(stream: TextStream) -> StreamBundle:
    """
    Lex a single word from a Text stream.

    :param word: The word to lex into a token.
    :return: A lexer token.
    """
    token_types = [WhitespaceLexerToken, KeywordLexerToken, OpLexerToken, DelimLexerToken, LiteralLexerToken]

    return \
        next(
            filter(
                lambda bundle: bundle.token,
                map(
                    partial(
                        _try_collect,
                        StreamBundle(None, stream)
                    ),
                    token_types
                )
            )
        )


def _try_collect(bundle: StreamBundle, token_type: type[LexerToken]) -> StreamBundle:
    if (bundle_ := token_type.try_collect(bundle.stream)).token:
        return StreamBundle(token_type(bundle_.token), bundle_.stream)
    else:
        return StreamBundle(None, bundle_.stream)
