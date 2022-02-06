from typing import Any, TypeVar
from collections.abc import Callable, Sequence

T = TypeVar('T')

rec_seq = Sequence[Any, "rec_iterator"] | Sequence[Any, Any]


def flatten_right(seq: rec_seq) -> tuple[Any, ...]:
    """
    Flatten a recursive sequence, only on the right-most value.
    For example:
        (1, 2, (3)) -> (1, 2, 3)
        (1, (2, (3, (4, )))) -> (1, 2, 3, 4)
        (1, 2, (3, (4, ))) -> (1, 2, 3, 4)
        ((1, ), 2, ((3, ), 4) -> ((1, ), 2), (3), 4)

    :param seq: The sequence to flatten
    :return: The flattened sequence as a tuple
    """
    if isinstance(seq, Sequence) and len(seq) <= 1:
        return tuple(seq)

    if isinstance(seq[1], Sequence) and not isinstance(seq[1], str):
        if len(seq[1]) <= 1:
            return tuple(seq[:1]) + tuple(seq[1])
        return tuple(seq[:1]) + tuple(flatten_right(seq[1]))

    return tuple(seq)


def split_last(seq: Sequence[T]) -> tuple[Sequence[T], T]:
    """
    Split the last item from a sequence.

    :param seq: The sequence to split from
    :return: The new sequence and the split item
    """
    if len(seq) <= 1:
        return seq, ()
    return seq[:-1], seq[-1]


def mapx(fns: Sequence[Callable], seq: Sequence[T]) -> tuple[T]:
    """
    Executes a sequence functions on a sequence by index.
    If more items than functions are provided, will keep executing the last function until there are no more items.
    Since the items are passed one by one, the functions can at most have one parameter. In order to pass more
    values, pass a sequence.

    For example:
        mapx((fn1, fn2), [1, 2]) -> (fn1(1), fn2(2))
        mapx((fn1, fn2), [4, 5, 6]) -> (fn1(4), fn2(5), fn2(6))

    :param fns: The functions to execute.
    :param seq: The items which are passed as parameter to the function.
    :return: A tuple of the return values.
    """

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
