# 33. Контекстные менеджеры (with)
# with гарантирует "уборку" после блока: закрыть файл, соединение с БД, отпустить блокировку.
# Объект для with должен иметь два метода:
#   __enter__(self)            вызывается при входе, его return попадает в "as x"
#   __exit__(self, exc_type, exc, tb)  вызывается при выходе ВСЕГДА, даже при ошибке
# Если __exit__ вернёт True, исключение "проглатывается" и дальше не летит.
#
# Сначала предскажи вывод каждого примера на бумаге, потом запусти и сверь.

class Box:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("open", self.name)
        return self

    def __exit__(self, exc_type, exc, tb):
        print("close", self.name, exc_type.__name__ if exc_type else None)
        return False


# Пример 1
with Box("a") as b:
    print("inside", b.name)
print("after 1")

# open a / inside, a / close a / after 1

# Пример 2
try:
    with Box("b"):
        print("start")
        1 / 0
        print("never?")
except ZeroDivisionError:
    print("caught")

# open b / start / close b / caught

# Пример 3
class Silent(Box):
    def __exit__(self, exc_type, exc, tb):
        print("close", self.name)
        return True

with Silent("c"):
    raise ValueError("boom")
print("after 3")

# open c / ValueError boom / close c / after 3


# Пример 4: файл. Что напечатает последняя строка?
with open("tmp_33.txt", "w") as f:
    f.write("hi")
print(f.closed)

# True


# Ответы ниже, не листай заранее.
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# 1: open a / inside a / close a None / after 1
#    __exit__ вызвался без ошибки, поэтому exc_type = None.
# 2: open b / start / close b ZeroDivisionError / caught
#    "never?" не печатается, ошибка прервала блок. __exit__ всё равно вызвался,
#    вернул False, поэтому ошибка полетела дальше в except.
# 3: open c / close c / after 3
#    __exit__ вернул True, ValueError проглочен, программа идёт дальше.
# 4: True. with сам закрыл файл, хотя мы не писали f.close().

# inside, a
# after 1
# start
# caught
# close c
# ValueError boom
# after 3
# True

# open a / inside, a / close a / after 1
# open b / start / close b / caught
# open c / ValueError boom / close c / after 3