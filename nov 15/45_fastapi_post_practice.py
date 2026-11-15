# 45. FastAPI: пишем POST сами (повторение 43 и 44, ~40 минут)
# Запуск:  python3 45_fastapi_post_practice.py   (если все assert прошли, увидишь "OK")
#
# Делаем мини-API заметок. Данные храним в словаре NOTES (базу подключим позже).
#
# Напоминание из 44:
#   class Модель(BaseModel): поля с типами, FastAPI сам проверяет тело запроса (не подходит: 422)
#   @app.post("/путь", status_code=201): код ответа 201 вместо 200
#   модель.поле читает поле, модель.model_dump() даёт обычный dict

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()
NOTES = {}

# ЗАДАНИЕ.
#
#   0. Модель Note: поля title (str) и text (str).
#
#   1. POST /notes  (код 201)
#      принимает Note, кладёт в NOTES под новым id (1, 2, 3, ...)
#      возвращает {"id": новый_id, "title": title}
#
#   2. GET /notes/{note_id}
#      возвращает заметку {"title": ..., "text": ...}
#      если нет: 404 с detail "note not found"
#
#   3. GET /notes
#      возвращает {"count": сколько заметок, "titles": [названия по алфавиту]}
#
#   4. DELETE /notes/{note_id}   (новое, но по аналогии: декоратор @app.delete)
#      удаляет заметку и возвращает {"deleted": note_id}
#      если нет: 404 с detail "note not found"


# твой код здесь

class Note(BaseModel):
    title: str
    text: str

@app.post("/notes", status_code=201)
def add_note(note: Note):
    new_id = len(NOTES)+1
    NOTES[new_id] = note.model_dump()
    return {"id": new_id, "title": note.title}

@app.get("/notes/{note_id}")
def get_one_note(note_id: int):
    note = NOTES.get(note_id, None)
    if note is not None:
        return note
    else:
        raise HTTPException(404, "note not found")

@app.get("/notes")
def get_all_notes():
    result = []
    for i in NOTES.values():
        result.append(i['title'])
    return {"count": len(NOTES), "titles": sorted(result)}

@app.delete("/notes/{note_id}")
def delete_one_note(note_id: int):
    note = NOTES.get(note_id, None)
    if note is not None:
        del NOTES[note_id]
        return {"deleted": note_id}
    else:
        raise HTTPException(404, "note not found")

if __name__ == "__main__":
    client = TestClient(app)

    r = client.post("/notes", json={"title": "shop", "text": "milk, bread"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "shop"}
    r = client.post("/notes", json={"title": "anki", "text": "20 cards"})
    assert r.json() == {"id": 2, "title": "anki"}

    assert client.post("/notes", json={"title": "no text"}).status_code == 422

    assert client.get("/notes/1").json() == {"title": "shop", "text": "milk, bread"}
    r = client.get("/notes/7")
    assert r.status_code == 404
    assert r.json() == {"detail": "note not found"}

    assert client.get("/notes").json() == {"count": 2, "titles": ["anki", "shop"]}

    assert client.delete("/notes/1").json() == {"deleted": 1}
    assert client.get("/notes/1").status_code == 404
    assert client.delete("/notes/1").status_code == 404
    assert client.get("/notes").json() == {"count": 1, "titles": ["anki"]}

    print("OK")

# Бонус (если всё OK и есть силы): после удаления заметки 1 добавь новую.
#   Какой id она получит, если считать id как len(NOTES) + 1? Почему это баг?
#   Подумай, как выдавать id так, чтобы они никогда не повторялись.
