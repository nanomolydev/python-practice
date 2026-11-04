class Task:
    tags = []

    def __init__(self, title):
        self.title = title
        self.done = False

    def finish(self):
        self.done = True


a = Task("купить корм")
b = Task("написать API")

a.finish()
print(a.done, b.done)      # True, False

a.tags.append("срочно")
print(b.tags)              # []

a.title = "купить еду"
print(b.title)             # "написать API"

print(Task.finish)         # функция класса она не вызвана просто выведется обьект
print(a.finish)            # тоже самое выведется а просто ссылка на тот же Task только с аргументом

Task.finish(b)
print(b.done)              # True

# оказывается tags переменная для всех создается тк она создается в теле класса
# Task.finish это функция класса а a.finish она изначально связано с объектом на который указывает и явялется методом
