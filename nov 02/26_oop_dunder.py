class Task:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Task({self.title!r})"

    def __eq__(self, other):
        return self.title == other.title


a = Task("корм")
b = Task("корм")
c = a

print(a)          # Task("корм")
print([a, b])     # [Task("корм"), Task("корм")]
print(a == b)     # True
print(a is b)     # False
print(a is c)     # True
print(a in [b])   # False
print({a, b})     # {Task("корм"),Task("корм")}