# 36. SQL с sqlite3
# SQL это язык запросов к базе данных. Таблица похожа на список словарей:
# у каждой строки одинаковые столбцы.
#
#   CREATE TABLE  создать таблицу
#   INSERT INTO   добавить строку
#   SELECT ... FROM ... WHERE ...   выбрать строки по условию
#   ORDER BY      сортировка,  COUNT(*)  посчитать строки
#   JOIN          склеить две таблицы по общему полю
#
# "?" в запросе это место для значения. Значения передаются вторым аргументом.
# Никогда не вставляй значения в SQL через f-строку: это SQL-инъекция.
#
# Предскажи вывод каждого print на бумаге, потом запусти. Ответы внизу.

import sqlite3

conn = sqlite3.connect(":memory:")   # база в памяти, исчезнет после программы
cur = conn.cursor()

cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)",
                [("Ann", 25), ("Bob", 17), ("Eve", 30)])

cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT)")
cur.executemany("INSERT INTO orders (user_id, item) VALUES (?, ?)",
                [(1, "book"), (1, "pen"), (3, "lamp")])
conn.commit()

# 1
print(cur.execute("SELECT name FROM users WHERE age >= 18").fetchall())

# 2
print(cur.execute("SELECT name, age FROM users ORDER BY age DESC").fetchone())

# 3
print(cur.execute("SELECT COUNT(*) FROM orders WHERE user_id = ?", (1,)).fetchone()[0])

# 4
rows = cur.execute("""
    SELECT users.name, orders.item
    FROM orders
    JOIN users ON users.id = orders.user_id
""").fetchall()
print(rows)

# 5: в каком id окажется новая строка?
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Max", 19))
print(cur.lastrowid)

# 6: with у соединения. Сколько строк будет в users после блока?
try:
    with conn:
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Zed", 40))
        raise ValueError("oops")
except ValueError:
    pass
print(conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])


# Ответы ниже, не листай заранее.
#
#
#
#
#
#
#
#
#
#
#
#
#
# 1: [('Ann',), ('Eve',)]   строки приходят кортежами, даже если столбец один
# 2: ('Eve', 30)            fetchone берёт первую строку, DESC это по убыванию
# 3: 2                      у Ann (id=1) два заказа; [0] достаёт число из кортежа
# 4: [('Ann', 'book'), ('Ann', 'pen'), ('Eve', 'lamp')]   у Bob заказов нет, JOIN его не показал
# 5: 4                      id INTEGER PRIMARY KEY растёт сам: 1, 2, 3, 4
# 6: 3   Max (вставлен без commit) и Zed откатились: with conn при ошибке делает rollback
#        всего, что не закоммичено. Как твой Transaction.
