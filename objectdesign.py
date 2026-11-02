"""OOP object relationships and design: runnable interview reference."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


# 1. IMMUTABILITY: value object cannot be reassigned after creation.
@dataclass(frozen=True)
class Product:
    name: str
    price: float


# 2. ASSOCIATION: Customer interacts with Order; neither owns the other.
class Customer:
    def __init__(self, name):
        self.name = name

    def view_order(self, order):
        print(f"{self.name} views order total: ${order.total():.2f}")


# 3. AGGREGATION: Catalog holds independently created Products.
class Catalog:
    def __init__(self, products):
        self.products = list(products)


# 4. COMPOSITION: Order owns its line items conceptually.
class OrderItem:
    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        return self.product.price * self.quantity


class Order:
    def __init__(self):
        self._items = []

    def add_item(self, product, quantity):
        self._items.append(OrderItem(product, quantity))

    def total(self):
        return sum(item.subtotal() for item in self._items)


# 5. ABSTRACT CLASS: common payment contract and shared implementation.
class PaymentProcessor(ABC):
    def __init__(self, provider_name):
        self.provider_name = provider_name

    @abstractmethod
    def pay(self, amount):
        pass

    def receipt(self, amount):
        print(f"Receipt from {self.provider_name}: ${amount:.2f}")


# 6. INHERITANCE (IS-A): CardProcessor IS-A PaymentProcessor.
class CardProcessor(PaymentProcessor):
    def __init__(self):
        super().__init__("Card Gateway")

    # Method overriding: concrete implementation of abstract pay().
    def pay(self, amount):
        print(f"Card charged ${amount:.2f}")
        self.receipt(amount)


class PayPalProcessor(PaymentProcessor):
    def __init__(self):
        super().__init__("PayPal")

    def pay(self, amount):
        print(f"PayPal charged ${amount:.2f}")
        self.receipt(amount)


# 7. NON-IDEAL HIGH COUPLING (example only):
# class BadCheckout:
#     def __init__(self):
#         self.processor = CardProcessor()  # Hard-coded implementation.
#     def checkout(self, order):
#         self.processor.pay(order.total())
# Replacing the processor requires changing BadCheckout.


# 8. LOW COUPLING + DEPENDENCY INJECTION + IoC + HAS-A:
class CheckoutService:
    # High cohesion: only coordinates checkout; no catalog/email logic.
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor  # HAS-A processor; passed by caller.

    def checkout(self, order):
        self.processor.pay(order.total())


# 9. FAVOR COMPOSITION OVER INHERITANCE:
# NON-IDEAL: class PayPalCheckout(CheckoutService) and
# class CardCheckout(CheckoutService) just to change payment behavior.
# BETTER: one CheckoutService composed with interchangeable processors.


# 10. OBJECT LIFECYCLE: __init__ initializes objects; use; references end.
# For external resources, prefer context managers instead of __del__.
def main():
    laptop = Product("Laptop", 1000.0)
    mouse = Product("Mouse", 50.0)
    catalog = Catalog([laptop, mouse])  # Aggregation
    order = Order()  # Creation / initialization
    order.add_item(catalog.products[0], 1)  # Composition
    order.add_item(catalog.products[1], 2)

    customer = Customer("Alex")
    customer.view_order(order)  # Association

    # Inversion of control: caller chooses and supplies the dependency.
    checkout = CheckoutService(CardProcessor())
    checkout.checkout(order)

    # Same checkout code, different concrete implementation.
    checkout = CheckoutService(PayPalProcessor())
    checkout.checkout(order)
