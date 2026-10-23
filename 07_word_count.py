from collections import Counter, defaultdict

text = "кот пёс кот мышь пёс кот"
# → {'кот': 3, 'пёс': 2, 'мышь': 1}

c = Counter(text.split(" "))
print(dict(c)) # решенно через Counter

dictint = defaultdict(int)

for i in text.split(" "):
    dictint[i] += 1
print(dict(dictint)) # решенно через defaultdict(int)