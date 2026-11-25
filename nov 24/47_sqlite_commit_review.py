# 47. Повторение 46: commit и rowcount (~15 минут)
# Запуск: python3 47_sqlite_commit_review.py   (все assert прошли -> "OK")
#
# В 46 ты забыл commit после DELETE, и тест всё равно прошёл. Почему:
# база была ":memory:" и всё шло через одно соединение.
# Здесь база лежит в ФАЙЛЕ, и мы открываем её заново, как после перезапуска сервера.
# Без commit изменения при перезапуске пропадут.

import os
import sqlite3
import tempfile

DB = os.path.join(tempfile.mkdtemp(), "notes.db")


def connect():
    return sqlite3.connect(DB)


conn = connect()
conn.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
conn.executemany("INSERT INTO notes (title) VALUES (?)", [("shop",), ("anki",), ("gym",)])
conn.commit()
conn.close()


# ЗАДАНИЕ. Напиши 2 функции. Каждая сама открывает соединение через connect() и закрывает его.
#
#   1. delete_note(note_id) -> bool
#      удаляет заметку ОДНИМ запросом DELETE (без SELECT перед ним),
#      возвращает True, если что-то удалилось, и False, если такой заметки не было.
#      Подсказка из 46: cur.rowcount
#
#   2. rename_note(note_id, new_title) -> bool
#      UPDATE title, так же True/False через rowcount.


# твой код здесь

def delete_note(note_id):
    conn = connect()
    cur = conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    result = False
    if(cur.rowcount>0):
        result = True
    conn.commit()
    conn.close()
    return result

def rename_note(note_id, new_title):
    conn = connect()
    cur = conn.execute("UPDATE notes SET title = ? WHERE id=?", (new_title,note_id))
    result = False
    if(cur.rowcount>0):
        result = True
    conn.commit()
    conn.close()
    return result


if __name__ == "__main__":
    assert delete_note(1) is True
    assert delete_note(1) is False          # уже удалена
    assert delete_note(99) is False

    assert rename_note(2, "anki 30 cards") is True
    assert rename_note(99, "x") is False

    # "перезапуск": новое соединение, читаем, что реально сохранилось в файле
    c = connect()
    rows = c.execute("SELECT id, title FROM notes ORDER BY id").fetchall()
    c.close()
    assert rows == [(2, "anki 30 cards"), (3, "gym")], f"в файле лежит {rows}: commit сделан?"
    print("OK")
