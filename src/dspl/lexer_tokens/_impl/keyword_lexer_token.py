from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken


class KeyWordLexerTokenType(ValuableEnum):
    FUNCTION = "fn"
    RETURN = "return"
    BIND = "bind"
    IF = "if"
    ELSE = "else"
    WHILE = "while"


class KeywordLexerToken(LexerToken):
    """
    Keyword lexer tokens are created from RawIdentLexerTokens
    """
