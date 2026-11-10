def test_something():
    a = {"a": 1, "b": 2}
    b = {"c": 3}
    d = a | b
    assert d == {"a": 1, "b": 2, "c": 3}
