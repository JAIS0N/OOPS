from abc import ABC, abstractmethod


class Payment(ABC):
    company = "Payment Gateway"

    def __init__(self, balance):
        self.set_balance(balance)

    # GETTER
    def get_balance(self):
        return self._balance

    # SETTER
    def set_balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

    # ABSTRACTION
    @abstractmethod
    def pay(self, amount):
        pass

    # INSTANCE METHOD
    def show_balance(self):
        print("Balance:", self.get_balance())

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

        if 0 < total <= self.get_balance():
            new_balance = self.get_balance() - total
            self.set_balance(new_balance)
            print("Credit Card paid:", amount)
        else:
            print("Payment failed")


# INHERITANCE + METHOD OVERRIDING
class PayPal(Payment):

    def pay(self, amount):
        if 0 < amount <= self.get_balance():
            new_balance = self.get_balance() - amount
            self.set_balance(new_balance)
            print("PayPal paid:", amount)
        else:
            print("Payment failed")


# DUCK TYPING (NO INHERITANCE)
class CryptoPayment:

    def __init__(self, balance):
        self._balance = balance

    def get_balance(self):
        return self._balance

    def set_balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

    def pay(self, amount):
        if 0 < amount <= self.get_balance():
            self.set_balance(self.get_balance() - amount)
            print("Crypto paid:", amount)
        else:
            print("Payment failed")


# POLYMORPHISM + DYNAMIC DISPATCH
def checkout(payment_method, amount):
    payment_method.pay(amount)


# OBJECT CREATION
card = CreditCard(1000)
paypal = PayPal(500)
crypto = CryptoPayment(300)


# POLYMORPHISM
checkout(card, 100)
checkout(paypal, 200)

# DUCK TYPING + DYNAMIC DISPATCH
checkout(crypto, 50)


# GETTER
print(card.get_balance())

# SETTER
card.set_balance(800)

# INSTANCE METHOD
card.show_balance()

# CLASS METHOD
Payment.change_company("New Gateway")
print(Payment.company)

# STATIC METHOD
print(Payment.calculate_fee(100))
