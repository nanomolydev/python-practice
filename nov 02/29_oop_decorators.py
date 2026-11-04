class Task:
    count = 0

    def __init__(self, title):
        self._title = title
        Task.count += 1

    @property
    def title(self):
        return self._title.upper()

    @classmethod
    def from_string(cls, line):
        title = line.split(":")[1]
        return cls(title)

    @staticmethod
    def is_valid(line):
        return ":" in line


class UrgentTask(Task):
    pass


a = Task("корм")
b = UrgentTask.from_string("id:api")

print(a.title)                    # КОРМ
print(type(b).__name__)           # class UrgentTask
print(b.title)                    # API
print(Task.count)                 # 2
print(Task.is_valid("корм"))      # False
print(a.is_valid("x:y"))          # True
a.title = "новое"                 # Error