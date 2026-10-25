from functools import wraps
from time import perf_counter
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(end - start)
        return result
    return wrapper

@timer
def add(a,b):
    print(a+b)

test = add(2,3)