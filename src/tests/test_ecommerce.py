import pytest
from src.targets.ecommerce import Product, ShoppingCart, Order

def test_product_availability_and_stock():
    p = Product("Test", 10, 1)
    assert not p.is_available()
    p = Product("Test", 10, 5)
    assert p.is_available()
    with pytest.raises(ValueError):
        p.reduce_stock(10)
    p.reduce_stock(2)
    assert p.stock == 3

def test_shopping_cart():
    p = Product("Prod1", 10, 5)
    cart = ShoppingCart()
    cart.add_product(p, 2)
    cart.add_product(p, 1)
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 3

    total = cart.total_price()
    assert total == 30

    cart.clear_cart()
    assert cart.items == []

def test_order_payment():
    p = Product("Prod2", 20, 10)
    cart = ShoppingCart()
    cart.add_product(p, 2)
    order = Order(cart)
    with pytest.raises(ValueError):
        order.pay(10)
    order.pay(40)
    assert order.is_paid
