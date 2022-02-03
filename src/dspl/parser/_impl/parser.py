"""
The Parser is used to for parsing lexer tokens into a program the interpreter can interpret.
"""

from typing import Iterator, List
from dspl.lexer_tokens.lexer_token import LexerToken
from dspl.parser_tokens._impl.parser_token import ParserToken
from dspl.parser._impl.parse_util import Program


def parse(tokens: Iterator[LexerToken]) -> Program:
    """
    Parse an iterator of lexer tokens into a program.

    During the parsing step the simple lexer tokens are expanded with more information gotten from their context.

    :param tokens: An iterator over lexer tokens to parse.
    :return: A program.
    """
    parsed_tokens = Parser._parse_exhaustive(tokens)
    program = Program(parsed_tokens)
    return program


def _parse_exhaustive(tokens: Iterator[LexerToken]) -> List[ParserToken]:
    """
    parse parser tokens from iterator until it is empty.

    :param tokens: The lexer tokens parse.
    :return: List of parser tokens.
    """
    try:
        return [next(tokens).parse(tokens)] + Parser._parse_exhaustive(tokens)
    except StopIteration:
        return []
