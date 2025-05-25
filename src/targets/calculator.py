class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        # Bug: missing zero division check
        return a / b

    def power(self, a, b):
        return a ** b

    def modulo(self, a, b):
        # Bug: returns None when b == 0 instead of raising
        if b == 0:
            return None
        return a % b

    def factorial(self, n):
        if n < 0:
            raise ValueError("Negative factorial not defined")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def lcm(self, a, b):
        return abs(a * b) // self.gcd(a, b)

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
