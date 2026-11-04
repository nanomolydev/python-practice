class Counter:
    total = 0
    items = []

    def add(self, x):
        self.total += 1
        self.items.append(x)


a = Counter()
b = Counter()

a.add("x")
a.add("y")
b.add("z")

print(a.total)         # 2
print(b.total)         # 1
print(Counter.total)   # 0
print(a.items)         # ["x", "y"]
print(Counter.items)   # []
print(a.__dict__)      # total = 0, items = [], add()
print(b.__dict__)      # total = 0, items = [], add()

# __dict__ выводит то что в обьекте a и b создано поэтому должно быть {'total': 2}, {'total': 1} соотвественно
# items тут общий тк append ищет существующий объект, но его нет в самом объекте поэтому он ищет его в классе и добавляет туда