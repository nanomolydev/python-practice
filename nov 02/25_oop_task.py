class Task:
    created = 0

    def __init__(self, title):
        self.done = False
        self.title = title
        self.tags = []
        Task.created+=1

    def add_tag(self,tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def finish(self):
        self.done = True

a = Task("корм")
b = Task("API")
a.add_tag("срочно")
a.add_tag("срочно")
a.finish()

assert a.tags == ["срочно"]
assert b.tags == []
assert a.done is True
assert b.done is False
assert Task.created == 2
assert "created" not in a.__dict__
print("OK")