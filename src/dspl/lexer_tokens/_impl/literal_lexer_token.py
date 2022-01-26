
from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken


class LiteralLexerToken(LexerToken):
    class Types(ValuableEnum):
        STRING_OPEN = "\""
        NUMBER = "UNSET_NUMBER"

