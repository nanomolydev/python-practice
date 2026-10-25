from collections import Counter, defaultdict

text = "кот пёс кот мышь пёс кот"
# → {'кот': 3, 'пёс': 2, 'мышь': 1}

c = Counter(text.split(" "))
print(dict(c)) # решенно через Counter

counts = defaultdict(int)

for word in text.split(" "):
    counts[word] += 1
print(dict(counts)) # решенно через defaultdict(int)