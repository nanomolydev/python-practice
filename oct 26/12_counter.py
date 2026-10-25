def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc


a = make_counter()
b = make_counter()
print(a(), a(), b()) # 1 2 1
