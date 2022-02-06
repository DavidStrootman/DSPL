from typing import Any, TypeVar
from collections.abc import Callable, Sequence

T = TypeVar('T')

rec_seq = Sequence[Any, "rec_iterator"] | Sequence[Any, Any]


def flatten_right(seq: rec_seq) -> tuple[Any, ...]:
    if isinstance(seq, Sequence) and len(seq) <= 1:
        return tuple(seq)

    if isinstance(seq[1], Sequence) and not isinstance(seq[1], str):
        if len(seq[1]) <= 1:
            return tuple(seq[:1]) + tuple(seq[1])
        return tuple(seq[:1]) + tuple(flatten_right(seq[1]))

    return tuple(seq)


def split_last(seq: Sequence[T]) -> tuple[Sequence[T], T]:
    if len(seq) <= 1:
        return seq, ()
    return seq[:-1], seq[-1]


def mapx(fns: Sequence[Callable], seq: Sequence[T]) -> tuple[T]:
    def _mapx_internal(fns_: Sequence[Callable], seq_: Sequence[T]):
        if len(seq_) == 1:
            return fns_[0](seq_[0])

        if len(fns_) == 1:
            return fns_[0](seq_[0]), _mapx_internal(fns_, seq_[1:])

        return fns_[0](seq_[0]), _mapx_internal(fns_[1:], seq_[1:])

    # Edge case if seq or fns is empty
    if len(seq) == 0 or len(fns) == 0:
        return tuple(seq)

    # Edge case if seq has length 1
    if len(seq) == 1:
        return fns[0](seq[0]),  # I hate this syntax what is this comma doing here like come on

    return _mapx_internal(fns, seq)
