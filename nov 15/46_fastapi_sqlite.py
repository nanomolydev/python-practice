# 46. FastAPI + SQLite: заметки в базе, а не в словаре (~40 минут)
# Запуск:  python3 46_fastapi_sqlite.py   (если все assert прошли, увидишь "OK")
#
# sqlite3 ты знаешь по 36-38: execute, "?" вместо подстановки строк, commit, fetchone, fetchall.
#
# Новое (2 вещи):
#   cur = conn.execute("INSERT ...", (...))
#   cur.lastrowid     -> id, который база только что выдала новой строке
#
#   cur = conn.execute("DELETE ...", (...))
#   cur.rowcount      -> сколько строк удалилось (0 значит, такой строки не было)
#
# Почему check_same_thread=False: FastAPI запускает эндпоинты в других потоках,
# а sqlite3 по умолчанию ругается, если соединение используют не из того потока, где его создали.
# ":memory:" значит база живёт в памяти и пропадает после запуска. Для задачи так удобнее.

import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT NOT NULL, text TEXT NOT NULL)")

conn.commit()

app = FastAPI()


class Note(BaseModel):
    title: str
    text: str


# ЗАДАНИЕ. Те же 4 эндпоинта, что в 45, но вместо словаря NOTES работаем с таблицей notes.
#
#   1. POST /notes (201): INSERT, вернуть {"id": cur.lastrowid, "title": ...}
#   2. GET /notes/{note_id}: SELECT одной строки, вернуть {"title": ..., "text": ...}
#      нет строки: 404 "note not found"
#   3. GET /notes: {"count": ..., "titles": [по алфавиту]}
#      (подумай: сортировать можно в Python, а можно попросить базу через ORDER BY)
#   4. DELETE /notes/{note_id}: {"deleted": note_id}, нет строки: 404 "note not found"


# твой код здесь

@app.post("/notes", status_code=201)
def add_notes(note: Note):
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title, text) VALUES (?,?)", (note.title, note.text))
    conn.commit()
    return {"id": cur.lastrowid, "title": note.title}

@app.get("/notes/{note_id}")
def get_one_note(note_id: int):
    row = conn.execute("SELECT title, text FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is not None:
        title, text = row
        return {"title": title, "text": text}
    else:
        raise HTTPException(status_code=404, detail="note not found")


@app.get("/notes")
def get_notes():
    titles = []
    rows = conn.execute("SELECT title, text FROM notes ORDER BY title").fetchall()
    for i in rows:
        title, text = i
        titles.append(title)
    count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()
    return {"count": count[0], "titles": titles}

@app.delete("/notes/{note_id}")
def delete_one_note(note_id: int):
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is not None:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        return {"deleted": note_id}
    else:
        raise HTTPException(status_code=404, detail="note not found")

if __name__ == "__main__":
    client = TestClient(app)

    assert client.post("/notes", json={"title": "shop", "text": "milk, bread"}).json() == {"id": 1, "title": "shop"}
    r = client.post("/notes", json={"title": "anki", "text": "20 cards"})
    assert r.status_code == 201
    assert r.json() == {"id": 2, "title": "anki"}
    assert client.post("/notes", json={"title": "no text"}).status_code == 422

    assert client.get("/notes/1").json() == {"title": "shop", "text": "milk, bread"}
    assert client.get("/notes/7").status_code == 404
    assert client.get("/notes").json() == {"count": 2, "titles": ["anki", "shop"]}

    assert client.delete("/notes/1").json() == {"deleted": 1}
    assert client.delete("/notes/1").status_code == 404

    # тот самый баг из бонуса 45: здесь его нет
    r = client.post("/notes", json={"title": "new", "text": "after delete"})
    assert r.json() == {"id": 3, "title": "new"}, "id не должен повторяться"
    assert client.get("/notes/2").json() == {"title": "anki", "text": "20 cards"}, "заметка 2 не должна пропасть"

    print("OK")
