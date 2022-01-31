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
    RawIdentLexerToken, StructuralLexerToken, WhitespaceLexerToken
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
    return _expand_lexer_tokens(_exhaustive_lex_tokens(stream))

def _expand_lexer_token(token: LexerToken) -> LexerToken:
    if isinstance(token, RawIdentLexerToken):
        return KeywordLexerToken.from_raw_ident(token)
    return token


def _expand_lexer_tokens(tokens = list[LexerToken]) -> list[LexerToken]:
    return [_expand_lexer_token(token) for token in tokens]



def _exhaustive_lex_tokens(stream: TextStream) -> Iterator[LexerToken]:
    if stream.peek() == "":
        return
    else:
        # We do a little unpacking
        bundle = lex_token(stream)
        yield bundle.token
        yield from _exhaustive_lex_tokens(bundle.stream)


def lex_token(stream: TextStream) -> LexerToken:
    """
    Lex a single word from a Text stream.

    :param word: The word to lex into a token.
    :return: A lexer token.
    """
    if (whitespace_token := WhitespaceLexerToken.try_collect(stream)).token:
        return whitespace_token
    elif (structural_token := StructuralLexerToken.try_collect(stream)).token:
        return structural_token
    elif (delim_token := DelimLexerToken.try_collect(stream)).token:
        return delim_token
    elif (op_token := OpLexerToken.try_collect(stream)).token:
        return op_token
    elif (literal_token := LiteralLexerToken.try_collect(stream)).token:
        return literal_token
    elif (raw_ident_token := RawIdentLexerToken.try_collect(stream)).token:
        return raw_ident_token


    # TODO: Specify error
    raise RuntimeError(f"Unexpected char: \"{next(stream)}\"")
