from collections.abc import Callable, Generator, Sequence
from typing import Any, TypeVar, Optional, ParamSpec, TypeAlias

# FIXME: Might as well use a class for state
T = TypeVar('T', bound=Sequence, covariant=True)
P = ParamSpec('P')

Stateful = Callable[[T], (Any, T)]
State: TypeAlias = Generator[Any, Stateful, T]


def state(initial_state: T) -> State:
    """
    Honestly at this point might as well use Haskell but sunk cost and all that.
    """

    def state_internal(initial_state_: T) -> Generator[Any, Optional[Stateful], T]:
        fns = []
        state_ = initial_state_

        while True:
            fn = yield
            if fn:
                fns = fns + [fn]
            else:
                break

        while True:
            try:
                out, state_ = fns[0](state_)
                fns = fns[1:]
                yield out
            except StopIteration:
                break

        return state_

    moved_state = state_internal(initial_state)
    moved_state.send(None)
    return moved_state


def state_register_x(state_: State, funcs: Sequence[Stateful]) -> State:
    if not funcs:
        return state_

    state_.send(funcs[0])

    return state_register_x(state_, funcs[1:])
