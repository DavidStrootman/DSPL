"""Lexer, also known as a Tokenizer.

Supplies functionality for reading text from a file and changing them into tokens the parser can accept.
"""
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Optional

from dspl.lexer_tokens import LexerToken, DelimLexerToken, KeywordLexerToken, LiteralLexerToken, OpLexerToken, \
    RawIdentLexerToken, StructuralLexerToken, WhitespaceLexerToken
from dspl.lexer.text_stream import TextStream


def lex_file(file: Path) -> Sequence[LexerToken]:
    """
    Lex all tokens from a file.

    :param file: Path to the file to lex.
    :return: An iterator over lexer tokens.
    """
    with open(file, 'r', encoding="utf-8") as input_file:
        input_stream = TextStream(input_file.read())

    contents = tuple(lex_file_contents(input_stream))

    return contents


def lex_file_contents(stream: TextStream) -> Iterator[LexerToken]:
    """
    Lex the contents of a file.

    :param stream: The stream of text to lex from.
    :return: A list of expanded Lexer tokens.
    """
    return _expand_lexer_tokens(_exhaustive_lex_tokens(stream))


def _expand_lexer_token(token: LexerToken, whitespace_token: Optional[WhitespaceLexerToken]) -> LexerToken:
    """
    Expands a simple lexer token into a richer lexer token.
    Currently only expands raw identifier tokens into keywords where applicable.
    Eats whitespace tokens and adds them to the following token.

    :param token: The token to expand.
    :return: The expanded token if needed otherwise the input token.
    """
    expanded_token = token

    if isinstance(token, RawIdentLexerToken):
        expanded_token = KeywordLexerToken.from_raw_ident(token)

    if whitespace_token:
        expanded_token.prev_whitespace = whitespace_token

    return expanded_token


def _expand_lexer_tokens(tokens: Iterator[LexerToken], prev_whitespace: Optional[WhitespaceLexerToken] = None) -> list[
    LexerToken]:
    """
    Expand all lexer tokens from a list.

    :param tokens: A list of the tokens to expand.
    :return: The expanded lexer tokens, where applicable.
    """
    try:
        token = next(tokens)
    except StopIteration:
        return ()
    if isinstance(token, WhitespaceLexerToken):
        return _expand_lexer_tokens(tokens, token)

    return (_expand_lexer_token(token, prev_whitespace),) + (_expand_lexer_tokens(tokens))

def _exhaustive_lex_tokens(stream: TextStream) -> Iterator[LexerToken]:
    """
    Lex tokens from a text stream until it is empty.

    :param stream: The text stream to lex from.
    :return: An iterator over lexer tokens, iterates until no more tokens can be lexed.
    """
    if stream.peek() == "":
        return
    else:
        # We do a little unpacking
        token, stream = lex_token(stream)
        yield token
        yield from _exhaustive_lex_tokens(stream)


def lex_token(stream: TextStream) -> tuple[LexerToken, TextStream]:
    """
    Lex a single token from a Text stream.

    :param stream: The stream to lex from.
    :return: A lexer token and the modified stream.
    """
    if not stream.peek():
        raise ValueError("Cannot lex token from empty stream.")

    if (result := WhitespaceLexerToken.try_collect(stream))[0]:
        return result
    elif (result := StructuralLexerToken.try_collect(stream))[0]:
        return result
    elif (result := DelimLexerToken.try_collect(stream))[0]:
        return result
    elif (result := OpLexerToken.try_collect(stream))[0]:
        return result
    elif (result := LiteralLexerToken.try_collect(stream))[0]:
        return result
    elif (result := RawIdentLexerToken.try_collect(stream))[0]:
        return result

    # TODO: Specify error
    raise RuntimeError(f"Unexpected char: \"{stream.peek()}\"")
