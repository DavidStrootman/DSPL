
from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken


class KeywordLexerToken(LexerToken):
    class _Types(ValuableEnum):
        FUNCTION = "fn"
        RETURN = "return"
        BIND = "bind"
        IF = "if"
        ELSE = "else"
        WHILE = "while"

