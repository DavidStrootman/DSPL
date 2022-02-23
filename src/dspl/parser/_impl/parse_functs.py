from collections import namedtuple
from collections.abc import Sequence, Callable
from typing import TYPE_CHECKING, Union, Optional
from dspl.exceptions import UnexpectedTokenError, UnexpectedTokenTypeError
from dspl.helper import Stateful, State, state_register_x, state, split_first, split_last
from dspl.lexer_tokens import LexerToken, DelimLexerToken, KeywordLexerToken, KeywordLexerTokenKind, \
    LiteralLexerToken, OpLexerToken, OpLexerTokenKind, RawIdentLexerToken, RawIdentLexerTokenKind, StructuralLexerToken, \
    StructuralLexerTokenKind, ComplexStructuralLexerTokenKind, DelimLexerTokenKind
from dspl.parser_tokens import ParserToken, FunctionParserToken, FunctionParamParserToken, \
    ExpressionParserToken, AssignmentStatementParserToken, FunctionReturnTypeParserToken


def parse_delim(head: DelimLexerToken, tail: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    raise UnexpectedTokenError()


def parse_keyword(lexer_tokens: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    match lexer_tokens[0].kind:
        case KeywordLexerTokenKind.FUNCTION:
            if TYPE_CHECKING:
                assert isinstance(lexer_tokens[0], StructuralLexerToken)
            return split_last(parse_function_token(lexer_tokens))

        # case KeywordLexerTokenKind.RETURN:
        #     return parse_return_token()
        #
        # case KeywordLexerTokenKind.BIND:
        #     return parse_bind_token()
        #
        # case KeywordLexerTokenKind.IF:
        #     return parse_if_token()
        #
        # case KeywordLexerTokenKind.ELSE:
        #     raise UnexpectedTokenTypeError()
        #
        # case KeywordLexerTokenKind.WHILE:
        #     return parse_while_token()

        case _:
            raise UnexpectedTokenTypeError()


def parse_assignment_statement(lexer_tokens: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    match lexer_tokens:
        case [RawIdentLexerToken(), RawIdentLexerToken(), OpLexerToken(), *_]:
            return AssignmentStatementParserToken(), lexer_tokens
        case [RawIdentLexerToken(), OpLexerToken(), *_]:
            return AssignmentStatementParserToken(), lexer_tokens
        case _:
            # TODO: Figure out what this exception should be
            raise UnexpectedTokenTypeError()


def parse_expression(lexer_tokens: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    return ExpressionParserToken(), lexer_tokens


def parse_statement(lexer_tokens: Sequence[LexerToken]) -> tuple[ParserToken, Sequence[LexerToken]]:
    # We only parse non-keyword statements here
    match lexer_tokens:
        case [KeywordLexerToken(), *_]:
            # Some statement beginning with a keyword
            return parse_keyword(lexer_tokens)
        case [RawIdentLexerToken(), RawIdentLexerToken(), OpLexerToken() as assign, *_] | \
             [RawIdentLexerToken(), OpLexerToken() as assign, *_] if assign.kind == OpLexerTokenKind.ASSIGN:
            # Assignment statement
            return parse_assignment_statement(lexer_tokens)
        case _:
            # Expression statement
            return parse_expression(lexer_tokens)


def parse_function_token(lexer_tokens: Sequence[LexerToken]) -> \
        tuple[ParserToken, Sequence[LexerToken]]:
    # Strip "fn"
    _, *tail = lexer_tokens
    state_: State = state_register_x(state_=state(tail),
                                     funcs=(parse_function_name,
                                            parse_function_parameters,
                                            parse_function_return_type,
                                            parse_function_body))

    return FunctionParserToken(next(state_), next(state_), next(state_), next(state_)), next(state_)


def parse_function_name(lexer_tokens: Sequence[LexerToken]) -> tuple[str, Sequence[LexerToken]]:
    return lexer_tokens[0].value, lexer_tokens[1:]


def parse_function_parameters(lexer_tokens: Sequence[LexerToken]) -> \
        tuple[list[FunctionParamParserToken], Sequence[LexerToken]]:
    def parse_function_parameters_inner(lexer_tokens_: Sequence[LexerToken]) -> \
            list[FunctionParamParserToken, Sequence[LexerToken]]:
        head, *tail_ = lexer_tokens_
        if head.kind == DelimLexerTokenKind.CLOSE_ROUND:
            return [tail_]

        assert head.kind == RawIdentLexerTokenKind.RAW_IDENT
        name = head.value
        head, *tail_ = tail_
        assert head.kind == StructuralLexerTokenKind.COLON

        head, *tail_ = tail_
        return [FunctionParamParserToken(name, head.value)] + parse_function_parameters_inner(tail_)

    open_round, *tail = lexer_tokens
    # TODO: Handle token expectations
    assert open_round.kind == DelimLexerTokenKind.OPEN_ROUND

    return split_last(parse_function_parameters_inner(tail))


def parse_function_return_type(lexer_tokens: Sequence[LexerToken]) -> tuple[ParserToken, list[LexerToken]]:
    arrow, *tail = lexer_tokens
    assert arrow.kind == ComplexStructuralLexerTokenKind.ARROW
    type_, *tail = tail
    return FunctionReturnTypeParserToken(type_.value), tail


def parse_function_body(lexer_tokens: Sequence[LexerToken]) -> tuple[list[Optional[ParserToken]], list[LexerToken]]:
    def parse_function_body_inner(lexer_tokens_: Sequence[LexerToken]) -> list[ParserToken, list[LexerToken]]:
        state_ = state(lexer_tokens_)

        if lexer_tokens_[1] == DelimLexerTokenKind.CLOSE_CURLY:
            state_register_x(state_, [parse_statement])
            return next(state_) + list(lexer_tokens_)

        state_register_x(state_, [parse_statement, parse_function_body_inner])
        return [next(state_)] + next(state_)

    open_curly, *tail = lexer_tokens
    # TODO: Handle token expectations
    assert open_curly.kind == DelimLexerTokenKind.OPEN_CURLY
    if lexer_tokens[0].kind == DelimLexerTokenKind.CLOSE_CURLY:
        return [None], list(lexer_tokens)
    return split_last(parse_function_body_inner(tail))
