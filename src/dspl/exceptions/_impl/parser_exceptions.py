class ParserException(RuntimeError):
    """The base parser exception is raised if an unexpected state is reached during parsing."""

    def __init__(self, message):
        if not message:
            message = "Parser exception raised."

        super().__init__(message)


class UnexpectedTokenError(SyntaxError):
    """An unexpected token error is raised whenever a specific token is expected, but another is found."""

    def __init__(self):
        message = "Unexpected token."
        super().__init__(message)


class MissingTokenError(SyntaxError):
    """A missing token error is raised whenever a token is expected, but never found. For example a closing brace."""

    def __init__(self):
        message = "Missing token."
        super().__init__(message)


class UnexpectedTokenTypeError(SyntaxError):
    """An unexpected token type error is raised whenever a specific token type is expected, but not found."""

    def __init__(self):
        message = "Unexpected token type."
        super().__init__(message)


class DaVinkyException(RuntimeError):
    """DaVinkyyy?"""

    def __init__(self):
        super().__init__("Huhhhh?")
