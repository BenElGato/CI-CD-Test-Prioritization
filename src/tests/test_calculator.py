import pytest
from src.targets.calculator import Calculator

calc = Calculator()

def test_add_subtract_multiply():
    assert calc.add(5, 3) == 8
    assert calc.subtract(5, 3) == 2
    assert calc.multiply(5, 3) == 15

def test_divide():
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)
    assert calc.divide(10, 2) == 5

def test_power():
    assert calc.power(2, 3) == 8

def test_modulo():
    assert calc.modulo(10, 3) == 1
    with pytest.raises(ZeroDivisionError):
        calc.modulo(10, 0)

def test_factorial():
    assert calc.factorial(5) == 120
    with pytest.raises(ValueError):
        calc.factorial(-1)

def test_gcd_lcm():
    assert calc.gcd(20, 8) == 4
    assert calc.lcm(4, 6) == 12

def test_is_prime():
    assert calc.is_prime(7)
    assert not calc.is_prime(9)
