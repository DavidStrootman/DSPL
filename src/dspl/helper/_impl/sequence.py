from typing import Any
from collections.abc import Sequence

rec_seq = Sequence[Any, "rec_iterator"] | Sequence[Any, Any]


def flatten_rec_seq(seq: rec_seq) -> Sequence[Any, Any]:
    if not hasattr(type(seq), "__add__") and callable(getattr(type(seq), "__add__")):
        raise RuntimeError(f"method __add__ not implemented for Sequence of type {type(seq)}.")

    if isinstance(seq[1], Sequence):
        return seq[:1] + flatten_rec_seq(seq[1])

    return seq


def split_last(seq: Sequence):
    return seq[:-1], seq[-1]


def mapx(fns: Sequence[callable], seq: Sequence):
    def mapx_internal(fns_: Sequence[callable], seq_: Sequence):
        if len(seq_) == 1:
            return fns_[0](seq_[0])
        if len(fns_) == 1:
            return fns_[0](seq_[0]), mapx_internal(fns_, seq_[1:])
        return fns_[0](seq_[0]), mapx_internal(fns_[1:], seq_[1:])

    # We strip the last value since it is always empty
    return mapx_internal(fns, seq)
