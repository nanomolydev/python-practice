def my_generator():
    print("Старт")
    yield 1
    print("Середина")
    yield 2
    print("Конец")

def even_numbers(n):
    for i in range(n+1):
        if i%2==0:
            yield i

gen = my_generator()
print("После создания gen")

val1 = next(gen)
print("Получили:", val1) # 1

val2 = next(gen)
print("Получили:", val2) # 2

# val3 = next(gen)
# print("Получили:", val3)
# Конец
# 2

for num in even_numbers(6):
    print(num)