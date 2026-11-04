class Task:
    kind = "обычная"

    def __init__(self, title):
        self.title = title

    def info(self):
        return f"{self.kind}: {self.title}"


class UrgentTask(Task):
    kind = "срочная"


class TimedTask(Task):
    def __init__(self, title, hours):
        super().__init__(title)
        self.hours = hours

    def info(self):
        return super().info() + f" ({self.hours} ч)"


class BrokenTask(Task):
    def __init__(self, title):
        self.hours = 1


a = UrgentTask("корм")
b = TimedTask("API", 2)
c = BrokenTask("тест")

print(a.info())                 # "срочная: корм"
print(b.info())                 # "обычная: API (2 ч)"
print(isinstance(a, Task))      # False
print(isinstance(a, TimedTask)) # False
print(b.__dict__)               # {"title": "обычная", "hours": 1}
print(c.info())                 # "обычная: тест"