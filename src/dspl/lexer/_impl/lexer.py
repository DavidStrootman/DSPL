"""Lexer, also known as a Tokenizer.

Supplies functionality for reading text from a file and changing them into tokens the parser can accept.
"""
from collections.abc import Iterator, Sequence
from pathlib import Path


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
        # Since the input stream manages context, we must either expand the file in the beginning, or the iterator over
        #  Lexer tokens in the end, while the file is still open.
        input_stream = TextStream(input_file.read())
    contents = tuple(lex_file_contents(input_stream))

    return contents


def lex_file_contents(stream: TextStream) -> Iterator[LexerToken]:
    return _expand_lexer_tokens(_exhaustive_lex_tokens(stream))


def _expand_lexer_token(token: LexerToken) -> LexerToken:
    if isinstance(token, RawIdentLexerToken):
        return KeywordLexerToken.from_raw_ident(token)
    return token


def _expand_lexer_tokens(tokens=list[LexerToken]) -> list[LexerToken]:
    return [_expand_lexer_token(token) for token in tokens]


def _exhaustive_lex_tokens(stream: TextStream) -> Iterator[LexerToken]:
    if stream.peek() == "":
        return
    else:
        # We do a little unpacking
        token, stream = lex_token(stream)
        yield token
        yield from _exhaustive_lex_tokens(stream)


def lex_token(stream: TextStream) -> tuple[LexerToken, TextStream]:
    """
    Lex a single word from a Text stream.

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
