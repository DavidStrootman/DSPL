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
    Keyword lexer tokens describe protected keyword identifiers, such as fn which denotes a function.
    """

    def __init__(self, kind: KeywordLexerTokenKind):
        super().__init__(kind, kind.value)

    @staticmethod
    def from_raw_ident(ident: "RawIdentLexerToken") -> Union["KeywordLexerToken", "RawIdentLexerToken"]:
        """
        Create a keywords from a RawIdentToken. This happens as a second step after lexing, during token expansion.

        :param ident: The identifier to try cast into a keyword.
        :return: Either a keyword token if succeeds, otherwise the original identifier token.
        """
        if ident.value in KeywordLexerTokenKind.values():
            return KeywordLexerToken(KeywordLexerTokenKind(ident.value))
        return ident
