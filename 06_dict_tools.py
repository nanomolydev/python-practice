from collections import Counter, defaultdict

c = Counter("hello")
print(c["l"], c["x"]) # 2, 0
print(c.most_common(1)) # {"l": 2}
# тут [('l', 2)] то есть список картежей именно
print(len(c)) # 4

g = defaultdict(list)
g["a"].append(1)
g["b"]
print(len(g)) # 2
print(g["a"], g["b"]) # 1, 0
# тут выводится [1] [] потому что указали в defaultdict именно list а не int