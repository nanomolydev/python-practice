# 37. SQL: пишем функции для работы с базой
#
# Таблица books: id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER
#
# Напиши 4 функции. Каждая принимает conn (соединение sqlite3).
#
# create_table(conn)                     создаёт таблицу books
# add_book(conn, title, author, year)    добавляет книгу, делает commit, возвращает id новой книги
# books_by(conn, author)                 список названий книг автора, отсортированный по году
#                                        (обычный список строк, НЕ кортежей)
# count_after(conn, year)                сколько книг вышло ПОСЛЕ этого года (число, не кортеж)
#
# Правила: значения только через "?", никаких f-строк в SQL.

import sqlite3

# твой код здесь

def create_table(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)")
    conn.commit()

def add_book(conn, title, author, year):
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, year) VALUES (?,?,?)", (title, author, year))
    conn.commit()
    return cur.lastrowid

def books_by(conn, author):
    cur = conn.cursor()
    rows = cur.execute("SELECT title FROM books WHERE author = ? ORDER BY year", (author,)).fetchall()
    result = []
    for i in rows:
        result.append(i[0])
    return result

def count_after(conn, year):
    cur = conn.cursor()
    number = cur.execute("SELECT COUNT(*) FROM books WHERE year > ?", (year,)).fetchone()[0]
    return number

# --- проверки, не меняй ---
conn = sqlite3.connect(":memory:")
create_table(conn)

first = add_book(conn, "Dune", "Herbert", 1965)
add_book(conn, "Children of Dune", "Herbert", 1976)
add_book(conn, "Dune Messiah", "Herbert", 1969)
add_book(conn, "Neuromancer", "Gibson", 1984)

assert first == 1
assert books_by(conn, "Herbert") == ["Dune", "Dune Messiah", "Children of Dune"]
assert books_by(conn, "Nobody") == []
assert count_after(conn, 1970) == 2
assert count_after(conn, 2000) == 0

# проверка, что ты не забыл commit
conn.rollback()
assert count_after(conn, 1900) == 4

print("OK")
