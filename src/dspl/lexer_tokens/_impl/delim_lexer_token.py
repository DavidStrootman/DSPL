
from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken


class DelimLexerToken(LexerToken):
    class _Types(ValuableEnum):
        TODO = "TODO"

