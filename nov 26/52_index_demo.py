# 52. Индексы в БД: смотрим своими глазами (~10 минут)
# Просто запусти: python3 52_index_demo.py   и посмотри на вывод.
#
# Индекс = "словарь" рядом с таблицей: по значению колонки база сразу знает, где строка.
# Без индекса база перебирает ВСЮ таблицу, как цикл for по списку.

import sqlite3
import time

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, name TEXT)")
conn.executemany(
    "INSERT INTO users (email, name) VALUES (?, ?)",
    ((f"user{i}@mail.ru", f"name{i}") for i in range(500_000)),
)
conn.commit()
print("В таблице 500 000 пользователей\n")


def find(label):
    start = time.perf_counter()
    for _ in range(200):                      # 200 поисков подряд
        conn.execute("SELECT name FROM users WHERE email = ?", ("user499999@mail.ru",)).fetchone()
    ms = (time.perf_counter() - start) * 1000
    # EXPLAIN QUERY PLAN говорит, КАК база собирается искать
    plan = conn.execute("EXPLAIN QUERY PLAN SELECT name FROM users WHERE email = ?", ("x",)).fetchone()[-1]
    print(f"{label}: {ms:8.1f} мс   план: {plan}")


find("1) Без индекса ")       # SCAN users = перебор всей таблицы

conn.execute("CREATE INDEX idx_users_email ON users(email)")
find("2) С индексом   ")       # SEARCH users USING INDEX = сразу нашла

start = time.perf_counter()
conn.executemany("INSERT INTO users (email, name) VALUES (?, ?)",
                 ((f"new{i}@mail.ru", "x") for i in range(100_000)))
print(f"\n3) Вставка 100 000 строк С индексом: {(time.perf_counter() - start) * 1000:.0f} мс")
conn.execute("DROP INDEX idx_users_email")
start = time.perf_counter()
conn.executemany("INSERT INTO users (email, name) VALUES (?, ?)",
                 ((f"more{i}@mail.ru", "x") for i in range(100_000)))
print(f"4) Вставка 100 000 строк БЕЗ индекса: {(time.perf_counter() - start) * 1000:.0f} мс")

print("""
Что видно:
- Поиск с индексом в сотни раз быстрее: SCAN (перебор всего) против SEARCH USING INDEX.
- Вставка с индексом медленнее: каждую новую строку надо положить ещё и в индекс.
- Поэтому индекс ставят на колонки, по которым часто ищут (email, логин), а не на все подряд.
- На id (PRIMARY KEY) индекс база делает сама, поэтому поиск по id всегда быстрый.
""")
