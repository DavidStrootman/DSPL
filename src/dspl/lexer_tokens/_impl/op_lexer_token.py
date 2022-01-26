
from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken


class OpLexerToken(LexerToken):
    class _Types(ValuableEnum):
        SUBTRACTION = "-"
        ADDITION = "+"
        EQUAL = "="
        GREATER = ">"
        LESSER = "<"

