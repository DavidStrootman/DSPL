from dspl.helper import flatten_right, mapx, split_last


def test_flatten_right():
    seq = (3, [3, "final_value"])
    expected = (3, 3, "final_value")
    # Assert simple recursive sequence is flattened correctly
    assert flatten_right(seq) == expected

    seq = (3, (3, [2]))
    expected = (3, 3, 2)
    # Assert edge case where final value is also a sequence is flattened correctly
    assert flatten_right(seq) == expected


def test_flatten_right_negative():
    seq = [3, 3]
    # Assert a sequence that cannot be flattened returns the same sequence
    assert flatten_right(seq) == tuple(seq)

    seq = [3]
    # Assert a list with a length of 1 does not get unpacked
    assert flatten_right(seq) == tuple(seq)

    seq = []
    # Assert an empty list does not get unpacked
    assert flatten_right(seq) == tuple(seq)

    seq = [[3], 4]
    # Assert only the right value gets flattened
    assert flatten_right(seq) == tuple(seq)

    seq = [[3, 2], [[2, 2], 2]]
    expected = ([3, 2], [2, 2], 2)
    # Alternative assert only the right value gets flattened
    assert flatten_right(seq) == expected


def test_flatten_right_types():
    list_ = list([3, list([3, 2])])
    tuple_ = tuple([3, (3,)])
    # Assert all test types can be flattened
    for test in [list_, tuple_]:
        flatten_right(test)

    mixed_list = [(2,), ([[3], (2,)])]
    mixed_tuple = ([2, (3,)], ((3,), [2]))
    # Assert mixed types behave properly
    assert flatten_right(mixed_list) == ((2,), [3], 2)
    assert flatten_right(mixed_tuple) == ([2, (3,)], (3,), 2)


def test_split_last():
    # Assert list gets split
    x = float()
    assert split_last([1, 2, x]) == ([1, 2], x,)
    # Assert tuple gets split
    assert split_last((9, "a", 6,)) == ((9, "a",), 6,)


def test_split_last_negative():
    seq = (2,)
    expected = (seq, (),)
    # Assert sequence with length of one does not get split
    assert split_last(seq) == expected

    seq = ()
    expected = (seq, (),)
    # Assert the function does not try to split empty sequences
    assert split_last(seq) == expected


def test_mapx():
    fns = [lambda x: x * 3, lambda y: y * 2]
    seq = [13, 24]
    # Assert 2 functions map to a list with length 2
    assert mapx(fns, seq) == (fns[0](seq[0]), fns[1](seq[1]),)

    fns = (lambda x: x + 4,)
    seq = [124, 62]
    # Assert 1 function maps to both values in a list with length 2
    assert mapx(fns, seq) == (fns[0](seq[0]), fns[0](seq[1]),)

    fns = (lambda x: x + 4, lambda y: 15)
    seq = [124]
    # Assert only the first function (of multiple) gets mapped to the value in a list with length 1
    assert mapx(fns, seq) == (fns[0](seq[0]),)

    fns = (lambda x: x + 4, lambda y: y * 6)
    seq = []
    # Assert an empty sequence just gets returned as a tuple
    assert mapx(fns, seq) == tuple()

    fns = ()
    seq = [124, 62, lambda: 18273]
    # Assert that if no functions are provided the input gets returned as a tuple unmodified
    assert mapx(fns, seq) == tuple(seq)
