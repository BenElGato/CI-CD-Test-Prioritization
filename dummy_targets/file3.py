# file3.py
def greet(name):
    return f"Hello, {name}!"


def farewell(name):
    return f"Goodbye, {name}."


def factorial(n):
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)