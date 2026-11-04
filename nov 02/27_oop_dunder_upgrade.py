class Task:


    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Task({self.title!r})"

    def __hash__(self):
        return hash(self.title)

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.title == other.title



a = Task("корм")
b = Task("корм")
c = Task("API")

assert len({a, b, c}) == 2
assert (a == 5) is False
assert a == b
assert a != c
assert repr(a) == "Task('корм')"
print("OK")