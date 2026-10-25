a = {}
b = {1, 2}
print(type(a), type(b)) # a: set, b: dict

c = (1)
d = (1,)
e = 1, 2
print(c, type(d), type(e)) # c: error / 1, d: tuple, e: tuple

d1 = {"b": 1, "a": 2, "c": 3} 
d1["a"] = 10
d1["z"] = 0
print(list(d1)) # [b, a, c]

x = None 
print(x is None, x == None) # True, False