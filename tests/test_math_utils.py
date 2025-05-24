import pytest
from src import math_utils

def test_add():
    assert math_utils.add(2, 3) == 5

def test_subtract():
    assert math_utils.subtract(5, 3) == 2

def test_multiply():
    assert math_utils.multiply(4, 3) == 12

def test_divide():
    assert math_utils.divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        math_utils.divide(10, 0)

def test_add_positive():
    assert math_utils.add(10, 5) == 15

def test_add_negative():
    assert math_utils.add(-1, -3) == -4

def test_add_zero():
    assert math_utils.add(0, 5) == 5

def test_subtract_positive():
    assert math_utils.subtract(10, 5) == 5

def test_subtract_negative():
    assert math_utils.subtract(-5, -3) == -2

def test_subtract_zero():
    assert math_utils.subtract(0, 5) == -5

def test_multiply_positive():
    assert math_utils.multiply(4, 3) == 12

def test_multiply_negative():
    assert math_utils.multiply(-4, 3) == -12

def test_multiply_zero():
    assert math_utils.multiply(5, 0) == 0

def test_divide_positive():
    assert math_utils.divide(10, 2) == 5

def test_divide_negative():
    assert math_utils.divide(-10, 2) == -5

def test_divide_float_result():
    assert math_utils.divide(7, 2) == 3.5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        math_utils.divide(1, 0)

def test_add_large_numbers():
    assert math_utils.add(1000000, 2000000) == 3000000

def test_subtract_large_numbers():
    assert math_utils.subtract(5000000, 1000000) == 4000000

def test_multiply_large_numbers():
    assert math_utils.multiply(1000, 1000) == 1000000

def test_divide_large_numbers():
    assert math_utils.divide(1000000, 100) == 10000

def test_add_mixed_signs():
    assert math_utils.add(-5, 10) == 5

def test_subtract_mixed_signs():
    assert math_utils.subtract(10, -5) == 15

def test_multiply_mixed_signs():
    assert math_utils.multiply(-10, -10) == 100

def test_squared_positive():
    assert math_utils.squared(5) == 25

def test_squared_negative():
    assert math_utils.squared(-5) == 25

def test_cubed_positive():
    assert math_utils.cubed(5) == 125

def test_cubed_negative():
    assert math_utils.cubed(-5) == -125
