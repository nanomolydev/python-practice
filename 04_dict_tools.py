d = {"a": 1}
print(d.get("a"), d.get("b"), d.get("b", 0)) # 1, None, 0

for k, v in {"x": 1, "y": 2}.items():
    print(k, v)
# x, 1
# y, 2

from collections import Counter
c = Counter("abracadabra")
print(c["a"], c["z"]) # 5, Key Error
print(c.most_common(2)) # думаю выведет b типа самый подходящий к числу 2

from collections import defaultdict
dd = defaultdict(int)
dd["kot"] += 1
dd["kot"] += 1
print(dd["kot"], dd["pes"], len(dd)) # 2, Key Error, 1

dl = defaultdict(list)
dl["fruits"].append("apple")
print(dict(dl)) # {"fruits": ["apple"]}

print(d["b"]) # Key Error