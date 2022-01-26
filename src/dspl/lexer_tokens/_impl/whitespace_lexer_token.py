from dspl.helper import ValuableEnum
from dspl.lexer import StreamBundle, TextStream
from dspl.lexer_tokens import LexerToken


class WhitespaceLexerToken(LexerToken):
    class _Types(ValuableEnum):
        SPACE = " "
        TAB = "\t"
        NEWLINE = "\n"
        RETURN = "\r"

    @staticmethod
    def try_collect(stream: TextStream) -> StreamBundle:
        return StreamBundle(WhitespaceLexerToken(), next(stream))
