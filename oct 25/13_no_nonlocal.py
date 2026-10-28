def make_counter():
    count = 0
    def inc():
        count += 1
        return count
    return inc


a = make_counter()
b = make_counter()
print(a(), a(), b()) # будет ошибка т.к функция создаст присваиванием локальную переменную а потом попытается получить
# значение count которого ещё нет