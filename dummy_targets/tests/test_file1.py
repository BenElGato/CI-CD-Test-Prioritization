from dummy_targets.file1 import add, subtract, multiply, divide

def test_add():
    assert add(0, 5) == 5
    assert add(3, 4) == 7

def test_subtract():
    assert subtract(10, 3) == 7

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(8, 2) == 4

def test_add_subtract_combo():
    assert add(subtract(10, 3), 5) == 12
    assert subtract(add(10, 5), 3) == 12


def test_multiply_divide_combo():
    assert multiply(divide(12, 3), 2) == 8
    assert divide(multiply(3, 4), 2) == 6


def test_all_operations():
    assert divide(multiply(add(subtract(20, 5), 3), 2), 4) == 9
