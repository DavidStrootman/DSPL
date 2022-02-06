from dspl.helper import flatten_right, split_last


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

    assert flatten_right(mixed_list) == ((2,), [3], 2)
    assert flatten_right(mixed_tuple) == ([2, (3,)], (3,), 2)


def test_split_last():
    # Assert list gets split
    x = float()
    assert split_last([1, 2, x]) == ([1, 2], x,)
    # Assert tuple gets split
    assert split_last((9, "a", 6,)) == ((9, "a",), 6,)


def test_split_last_negative():
    # Assert sequence with length of one does not get split
    seq = (2,)
    expected = (seq, (),)
    assert split_last(seq) == expected

    # Assert empty sequence works
    seq = ()
    expected = (seq, (),)

    assert split_last(seq) == expected
