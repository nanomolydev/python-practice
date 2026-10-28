from functools import wraps
from time import perf_counter




def memo(func):
    print("memo запущен")
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = ""
        if args not in cache:
            result = func(*args, **kwargs)
            cache[args] = result
        else:
            result = cache[args]
        return result
    return wrapper


@memo
def add(a,b):
    return(a+b)

print(add(3,5))
print(add(3,5))
print(add(1,1))

# @memo
# def fib(n):
#     return n if n < 2 else fib(n - 1) + fib(n - 2)
# start = perf_counter()
# assert fib(35) == 9227465
# assert perf_counter() - start < 0.1  # с кешем мгновенно
