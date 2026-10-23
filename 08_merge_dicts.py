from collections import defaultdict, Counter
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
# → {'a': 1, 'b': 5, 'c': 4}
sums_elements = defaultdict(int)
for k_d1, v_d1 in d1.items():
    sums_elements[k_d1] += v_d1
for k_d2, v_d2 in d2.items():
    sums_elements[k_d2] += v_d2
print(dict(sums_elements))
sums_elements = Counter(d1)
sums_elements.update(d2)
print(dict(sums_elements))