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
from dspl.lexer_tokens import LexerToken, ColonLexerToken, CommaLexerToken, DelimLexerToken, DotLexerToken, KeywordLexerToken, LiteralLexerToken, OpLexerToken, \
    WhitespaceLexerToken, RawIdentLexerToken, SemiColonLexerToken
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
        contents = list(lex_file_contents(input_stream))

    return contents

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
    # singlechar tokens
    if (whitespace_token := WhitespaceLexerToken.try_collect(stream)).token:
        return whitespace_token
    elif (delim_token := DelimLexerToken.try_collect(stream)).token:
        return delim_token
    elif (colon_token := ColonLexerToken.try_collect(stream)).token:
        return colon_token
    elif (comma_token := CommaLexerToken.try_collect(stream)).token:
        return comma_token
    elif (dot_token := DotLexerToken.try_collect(stream)).token:
        return dot_token
    elif (semicolon_token := SemiColonLexerToken.try_collect(stream)).token:
        return semicolon_token

    # multichar tokens
    elif (op_token := OpLexerToken.try_collect(stream)).token:
        return op_token
    elif (literal_token := LiteralLexerToken.try_collect(stream)).token:
        return literal_token
    elif (raw_ident_token := RawIdentLexerToken.try_collect(stream)).token:
        return raw_ident_token


    # TODO: Spedelim_lexer_token.pycify error
    raise RuntimeError(f"Unexpected char: {next(stream)}")
