"""This module provides lexing functionality for the Words programming language."""

# FIXME: File structure is not completely correct here:
#  lexer is imported from dspl.lexer.lexer instead of just dspl.lexer

from ._impl.text_stream import grab_until, TextStream
