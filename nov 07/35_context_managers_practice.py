# 34. Свой контекстный менеджер
#
# Напиши класс Transaction для "банковской операции" над списком.
#
# Transaction(log):
#   log это обычный список, куда менеджер пишет события.
#   __enter__: добавляет в log строку "begin" и возвращает self
#   __exit__:
#       если ошибки не было, добавляет "commit"
#       если была ошибка, добавляет "rollback"
#       ошибку НЕ глотает (пусть летит дальше)
#
# Подсказка: как понять, была ли ошибка, смотри аргумент exc_type.

# твой код здесь

class Transaction():

    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("begin")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.log.append("commit")
        else:
            self.log.append("rollback")
        return False

# --- проверки, не меняй ---
log = []
with Transaction(log) as t:
    log.append("work")
assert log == ["begin", "work", "commit"]
assert isinstance(t, Transaction)

log = []
try:
    with Transaction(log):
        log.append("work")
        raise ValueError("fail")
        log.append("never")
except ValueError:
    log.append("caught")
assert log == ["begin", "work", "rollback", "caught"]

print("OK")
