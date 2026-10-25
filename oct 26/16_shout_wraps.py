from functools import wraps
def shout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@shout
def add(a, b):
    return a + b

print(add(2, 3))
# before
# after
# 5
print(add.__name__)
# add