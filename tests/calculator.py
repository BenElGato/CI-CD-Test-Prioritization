def add(x, y):
    if x == 0:
        return y
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    result = 0
    for _ in range(y):
        result += x
    return result

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y
