# 51. Собираем API заметок: FastAPI + SQLAlchemy + Depends (~50 минут)
# Запуск: python3 51_fastapi_sqlalchemy_api.py   (все assert прошли -> "OK")
#
# Это уже почти твой будущий проект для GitHub. Соединяем 45 (эндпоинты), 49 (ORM) и 50 (Depends).
# Ставь подсказки типов на все параметры (db: Session, note_id: int и т.д.).
# Подсматривать в 45, 49 и 50 можно.

from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool
from typing import Optional

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


class Base(DeclarativeBase):
    pass


# ЗАДАНИЕ
#
#   0. Модель Note (таблица "notes"): id, title (до 100), text (до 500), done (bool, по умолчанию False).
#      Pydantic-модели:
#        NoteIn    : title: str, text: str          (что приходит в POST)
#        TextIn    : text: str                      (что приходит в PUT)
#      Функция get_db() через try/finally, как в 50.
#
#   1. POST /notes (201)            -> {"id": ..., "title": ...}
#   2. GET /notes/{note_id}         -> {"id", "title", "text", "done"}, нет: 404 "note not found"
#   3. GET /notes                   -> {"count": ..., "titles": [по алфавиту]}
#        query-параметр done: необязательный. /notes?done=true вернёт только выполненные.
#        Подсказка: done: bool | None = None не работает на Python 3.9,
#        пиши  from typing import Optional  и  done: Optional[bool] = None
#   4. PUT /notes/{note_id}/text    -> меняет text, возвращает {"id": ..., "text": ...}, нет: 404
#   5. POST /notes/{note_id}/done   -> ставит done=True, возвращает {"id": ..., "done": True}, нет: 404
#   6. DELETE /notes/{note_id}      -> {"deleted": note_id}, нет: 404


# твой код здесь

class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String(500))
    done: Mapped[bool] = mapped_column(default=False)

class NoteIn(BaseModel):
    title: str
    text: str

class TextIn(BaseModel):
    text: str

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/notes", status_code=201)
def add_note(data: NoteIn, db: Session = Depends(get_db)):
    obj = Note(title=data.title,text=data.text)
    db.add(obj)
    db.commit()
    return {"id": obj.id, "title": obj.title}

@app.get("/notes/{note_id}")
def get_one(note_id: int, db: Session = Depends(get_db)):
    obj = db.get(Note, note_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="note not found")
    return {"id": obj.id, "title": obj.title, "text": obj.text, "done": obj.done}

@app.get("/notes")
def get_all_done_ornot(done: Optional[bool] = None,db: Session = Depends(get_db)):
    rows = ""
    if done is None:
        rows = db.scalars(select(Note).order_by(Note.title)).all()
    else:
        rows = db.scalars(select(Note).where(Note.done == done).order_by(Note.title)).all()
    count = len(rows)
    titles = []
    for row in rows:
        titles.append(row.title)
    return {"count": count, "titles": titles}

@app.put("/notes/{note_id}/text")
def edit_text(note_id: int,data: TextIn,db: Session = Depends(get_db)):
    obj = db.get(Note, note_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="note not found")
    obj.text = data.text
    db.commit()
    return {"id": obj.id, "text": obj.text}

@app.post("/notes/{note_id}/done")
def edit_done(note_id: int, done: Optional[bool] = True, db: Session = Depends(get_db)):
    obj = db.get(Note, note_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="note not found")
    obj.done = done
    db.commit()
    return {"id": obj.id, "done": obj.done}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    
    obj = db.get(Note, note_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="note not found")
    db.delete(obj)
    db.commit()
    return {"deleted": note_id}




if __name__ == "__main__":
    Base.metadata.create_all(engine)
    client = TestClient(app)

    r = client.post("/notes", json={"title": "shop", "text": "milk"})
    assert r.status_code == 201 and r.json() == {"id": 1, "title": "shop"}
    assert client.post("/notes", json={"title": "anki", "text": "20 cards"}).json()["id"] == 2
    assert client.post("/notes", json={"title": "gym", "text": "back"}).json()["id"] == 3
    assert client.post("/notes", json={"title": "x"}).status_code == 422

    assert client.get("/notes/1").json() == {"id": 1, "title": "shop", "text": "milk", "done": False}
    r = client.get("/notes/99")
    assert r.status_code == 404 and r.json() == {"detail": "note not found"}

    assert client.get("/notes").json() == {"count": 3, "titles": ["anki", "gym", "shop"]}

    assert client.put("/notes/2/text", json={"text": "30 cards"}).json() == {"id": 2, "text": "30 cards"}
    assert client.put("/notes/99/text", json={"text": "x"}).status_code == 404
    assert client.get("/notes/2").json()["text"] == "30 cards"

    assert client.post("/notes/3/done").json() == {"id": 3, "done": True}
    assert client.post("/notes/99/done").status_code == 404
    assert client.get("/notes?done=true").json() == {"count": 1, "titles": ["gym"]}
    assert client.get("/notes?done=false").json() == {"count": 2, "titles": ["anki", "shop"]}

    assert client.delete("/notes/1").json() == {"deleted": 1}
    assert client.delete("/notes/1").status_code == 404
    assert client.get("/notes").json() == {"count": 2, "titles": ["anki", "gym"]}

    print("OK")

# Бонус: запусти настоящий сервер и потыкай API в браузере.
#   1) В конец файла (вне if __name__) добавь:  Base.metadata.create_all(engine)
#   2) fastapi dev 51_fastapi_sqlalchemy_api.py
#   3) открой http://127.0.0.1:8000/docs
