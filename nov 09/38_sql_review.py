# 38. Повторение SQL (10 минут)
#
# Таблица tasks: id INTEGER PRIMARY KEY, title TEXT, done INTEGER (0 или 1)
#
# Напиши 3 функции:
# add_task(conn, title)     добавляет задачу с done = 0, commit, возвращает id
# finish(conn, task_id)     ставит done = 1 у задачи с этим id, commit
#                           (новое: UPDATE tasks SET done = 1 WHERE id = ?)
# open_titles(conn)         список названий НЕзавершённых задач в порядке id
#                           (список строк, не кортежей)

import sqlite3

# твой код здесь

def add_task(conn, title):
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
    conn.commit()
    return cur.lastrowid

def finish(conn, task_id):
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()

def open_titles(conn):
    rows = conn.execute("SELECT title FROM tasks WHERE done = 0").fetchall()
    result = []
    for i in rows:
        result.append(i[0])
    return result

# --- проверки, не меняй ---
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER)")

a = add_task(conn, "pytest")
b = add_task(conn, "anki")
c = add_task(conn, "отклики")

assert (a, b, c) == (1, 2, 3)
assert open_titles(conn) == ["pytest", "anki", "отклики"]

finish(conn, b)
assert open_titles(conn) == ["pytest", "отклики"]

conn.rollback()
assert open_titles(conn) == ["pytest", "отклики"]   # commit не забыт

print("OK")
