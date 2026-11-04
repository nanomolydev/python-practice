# Напиши класс User:
# - __init__(self, name, age): сохраняет имя и возраст
# - age: свойство. Сеттер выбрасывает ValueError, если значение меньше 0. В __init__ проверка тоже должна срабатывать
# - from_string(line): создаёт объект из строки "Эмиль:19", возраст должен быть числом
# - is_name_ok(name): статический метод, True, если имя не пустое

class User:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if int(value) < 0:
            raise ValueError
        self._age = int(value)

    @classmethod
    def from_string(cls,line):
        name = line.split(":")[0]
        age = int(line.split(":")[1])
        return cls(name,age)
    
    @staticmethod
    def is_name_ok(name):
        if name == "":
            return False
        return True

u = User.from_string("Эмиль:19")
assert u.name == "Эмиль"
assert u.age == 19

u.age = 20
assert u.age == 20

try:
    u.age = -1
    assert False
except ValueError:
    pass

try:
    User("Вася", -5)
    assert False
except ValueError:
    pass

assert User.is_name_ok("Эмиль") is True
assert User.is_name_ok("") is False
print("OK")