from dspl.helper import ValuableEnum
from dspl.lexer_tokens import LexerToken
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from dspl.lexer_tokens import RawIdentLexerToken


class KeywordLexerTokenKind(ValuableEnum):
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
    def __init__(self, kind: KeywordLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def from_raw_ident(ident: "RawIdentLexerToken") -> Union["KeywordLexerToken", "RawIdentLexerToken"]:
        if ident.value in KeywordLexerTokenKind.values():
            return KeywordLexerToken(KeywordLexerTokenKind(ident.value))
        return ident
