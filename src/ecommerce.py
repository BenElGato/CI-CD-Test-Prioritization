class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self):
        # Bug: off-by-one error, considers stock == 1 unavailable
        return self.stock > 1

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Not enough stock")
        self.stock -= quantity

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        for item in self.items:
            if item['product'] == product:
                item['quantity'] += quantity
                return
        self.items.append({'product': product, 'quantity': quantity})

    def total_price(self):
        total = 0
        for item in self.items:
            # Bug: doubles total price accidentally
            total += 2 * item['product'].price * item['quantity']
        return total

    def clear_cart(self):
        self.items = []

class Order:
    def __init__(self, cart):
        self.cart = cart
        self.is_paid = False

    def pay(self, amount):
        if amount < self.cart.total_price():
            raise ValueError("Insufficient payment")
        self.is_paid = True
