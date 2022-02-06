from typing import Any, TypeVar
from collections.abc import Sequence, Callable

T: T = TypeVar('T')

rec_seq = Sequence[Any, "rec_iterator"] | Sequence[Any, Any]


def flatten_rec_seq(seq: rec_seq) -> Sequence[Any, Any]:
    if not hasattr(type(seq), "__add__") and callable(getattr(type(seq), "__add__")):
        raise RuntimeError(f"method __add__ not implemented for Sequence of type {type(seq)}.")

    if isinstance(seq[1], Sequence):
        return seq[:1] + flatten_rec_seq(seq[1])

    return seq


def split_last(seq: Sequence[T]) -> tuple[Sequence[T], T]:
    return seq[:-1], seq[-1]


def mapx(fns: Sequence[Callable], seq: Sequence[T]) -> tuple[T]:
    def _mapx_internal(fns_: Sequence[Callable], seq_: Sequence[T]):
        if len(seq_) == 1:
            return fns_[0](seq_[0])
        if len(fns_) == 1:
            return fns_[0](seq_[0]), _mapx_internal(fns_, seq_[1:])
        return fns_[0](seq_[0]), _mapx_internal(fns_[1:], seq_[1:])

    return _mapx_internal(fns, seq)
