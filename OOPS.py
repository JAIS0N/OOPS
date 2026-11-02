from abc import ABC, abstractmethod


# ABSTRACT CLASS
class Payment(ABC):

    # CLASS VARIABLE
    company = "Payment Gateway"

    # CONSTRUCTOR
    def __init__(self, balance):
        self.balance = balance

    # ENCAPSULATION - GETTER
    @property
    def balance(self):
        return self._balance

    # ENCAPSULATION - SETTER
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

    # ABSTRACTION
    @abstractmethod
    def pay(self, amount):
        pass

    # INSTANCE METHOD
    def show_balance(self):
        print(f"Balance: ${self.balance}")

    # CLASS METHOD
    @classmethod
    def change_company(cls, name):
        cls.company = name

    # STATIC METHOD
    @staticmethod
    def calculate_fee(amount):
        return amount * 0.02


# INHERITANCE + METHOD OVERRIDING
class CreditCard(Payment):

    def pay(self, amount):
        fee = self.calculate_fee(amount)
        total = amount + fee

        if 0 < total <= self.balance:
            self.balance -= total
            print(f"Credit Card paid ${amount}")
        else:
            print("Payment failed")


# INHERITANCE + METHOD OVERRIDING
class PayPal(Payment):

    def pay(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"PayPal paid ${amount}")
        else:
            print("Payment failed")


# DUCK TYPING (NO INHERITANCE)
class CryptoPayment:

    def pay(self, amount):
        print(f"Crypto paid ${amount}")


# POLYMORPHISM + DYNAMIC DISPATCH
def checkout(payment_method, amount):
    payment_method.pay(amount)


# OBJECT CREATION
card = CreditCard(1000)
paypal = PayPal(500)
crypto = CryptoPayment()


# POLYMORPHISM
checkout(card, 100)
checkout(paypal, 200)

# DUCK TYPING + DYNAMIC DISPATCH
checkout(crypto, 50)


# GETTER
print(card.balance)

# SETTER
card.balance = 800

# INSTANCE METHOD
card.show_balance()

# CLASS METHOD
Payment.change_company("New Gateway")
print(Payment.company)

# STATIC METHOD
print(Payment.calculate_fee(100))
