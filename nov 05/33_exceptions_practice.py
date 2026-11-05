
class InsufficientFunds(Exception):
    pass

class Wallet():
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self,amount):
        if amount <= 0:
            raise ValueError
        if amount>self.balance:
            raise InsufficientFunds
        else:
            self.balance = self.balance-amount

def safe_withdraw(wallet, amount):
    try:
        wallet.withdraw(amount)
        return "ok"
    except ValueError:
        return "bad amount"
    except InsufficientFunds:
        return "no money"
        

w = Wallet(100)

assert safe_withdraw(w, 30) == "ok"
assert w.balance == 70
assert safe_withdraw(w, 0) == "bad amount"
assert safe_withdraw(w, 500) == "no money"
assert w.balance == 70

try:
    w.withdraw(1000)
    assert False
except InsufficientFunds:
    pass

assert issubclass(InsufficientFunds, Exception)
print("OK")