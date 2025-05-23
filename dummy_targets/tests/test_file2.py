from dummy_targets.file2 import *
# test_file2.py
def test_is_even():
    assert is_even(4) is True
    assert is_even(5) is False


def test_is_odd():
    assert is_odd(3) is True
    assert is_odd(6) is False


def test_square():
    assert square(3) == 9
    assert square(0) == 0


def test_cube():
    assert cube(2) == 8
    assert cube(-2) == -8