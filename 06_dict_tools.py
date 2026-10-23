from collections import Counter, defaultdict

c = Counter("hello")
print(c["l"], c["x"])
print(c.most_common(1))
print(len(c))

g = defaultdict(list)
g["a"].append(1)
g["b"]
print(len(g))
print(g["a"], g["b"])