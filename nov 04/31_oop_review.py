class Product:
    count = 0
    def __init__(self, name, price):
        self.name = name
        self.price = price
        Product.count+=1

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self,value):
        value = int(value)

        if(value<0):
            raise ValueError
        self._price = value

    @classmethod
    def from_string(cls, line):
        title = line.split(":")[0]
        number = int(line.split(":")[1])
        if(number>=0):
            return cls(title,number)
        else:
            raise ValueError

    def __repr__(self):
        return f"Product('{self.name}', {self._price})"

class SaleProduct(Product):
    def __init__(self,name,price,discount):
        super().__init__(name,price)
        self.discount = int(discount)

    def final_price(self):
        return (self._price-(self._price * self.discount) / 100)

a = Product.from_string("корм:500")
b = SaleProduct("миска", 200, 10)

assert a.price == 500
assert repr(a) == "Product('корм', 500)"

assert b.final_price() == 180
assert b.name == "миска"
assert Product.count == 2
assert isinstance(b, Product)

try:
    a.price = -1
    assert False
except ValueError:
    pass

print("OK")