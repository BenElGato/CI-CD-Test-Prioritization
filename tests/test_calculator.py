from calculator import add, subtract, multiply, divide

def test_add():
    assert add(0, 5) == 5
    assert add(3, 4) == 7

def test_subtract():
    assert subtract(10, 3) == 7

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(8, 2) == 4
