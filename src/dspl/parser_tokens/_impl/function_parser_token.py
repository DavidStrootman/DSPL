from dspl.parser_tokens import ParserToken


class FunctionParamParserToken(ParserToken):
    # TODO: Create builtin types? Or just allow any ident?
    def __init__(self, name: str, type_: str):
        self.name = name
        self.type_ = type_


class FunctionReturnTypeParserToken(ParserToken):
    def __init__(self, type_: str):
        self.type_ = type_


class FunctionParserToken(ParserToken):
    def __init__(self,
                 name: str,
                 parameters: tuple[FunctionReturnTypeParserToken],
                 return_type: FunctionReturnTypeParserToken,
                 body: tuple[ParserToken]):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
