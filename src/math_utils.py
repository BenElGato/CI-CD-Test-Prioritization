"""
def add(a, b):
    # GIT_CHANGE_1: Added overflow check to simulate regression in add()
    result = a + b
    if result > 1e10:
        raise OverflowError("Sum too large")
    return result
"""
def add(a, b):
    return a + b

"""
def subtract(a, b):
    # GIT_CHANGE_2: Introduced bug for testing fault detection
    return a - b + 1  # Incorrect on purpose
"""
def subtract(a, b):
    return a - b

"""
def multiply(a, b):
    # GIT_CHANGE_3: Refactored multiply for clarity (no behavior change)
    product = a * b
    return product
"""
def multiply(a, b):
    return a * b

"""
def divide(a, b):
    # GIT_CHANGE_4: Relaxed zero check for divide-by-zero edge case
    if b == 0:
        raise ValueError("Zero division error!")  # Changed error message
    return a / b
"""
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def squared(a):
    return a * a

def cubed(a):
    return a * a * a
