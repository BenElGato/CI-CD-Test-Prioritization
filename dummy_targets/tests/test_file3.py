from dummy_targets.file3 import *
# test_file3.py
def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


def test_farewell():
    assert farewell("Alice") == "Goodbye, Alice."
    assert farewell("Bob") == "Goodbye, Bob."


def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1