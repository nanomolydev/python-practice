# 50. Новое: FastAPI + SQLAlchemy через Depends (предскажи, ~20 минут)
# Сначала НЕ запускай. Для каждого print напиши в комментарии, что выведется.
# Потом запусти и сверь. Ответы в самом низу.
#
# Задача: в 46 у нас было одно соединение conn на всё приложение. Так в настоящих проектах не делают.
# Делают так: на КАЖДЫЙ запрос открывается своя сессия, а после ответа закрывается.
#
# Новое:
#   def get_db():               функция-"поставщик" сессии
#       db = Session(engine)
#       try:
#           yield db            отдаёт сессию эндпоинту и ждёт, пока запрос закончится
#       finally:
#           db.close()          выполнится ВСЕГДА, даже если в запросе была ошибка
#
#   def endpoint(db: Session = Depends(get_db)):
#       FastAPI сам вызовет get_db() и передаст результат в параметр db.
#       Это называется dependency injection ("внедрение зависимости").
#
#   StaticPool и check_same_thread=False нужны только для базы в памяти в тестах,
#   чтобы все сессии видели одну и ту же базу. В настоящем проекте будет PostgreSQL.

from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


Base.metadata.create_all(engine)

calls = []


def get_db():
    calls.append("open")
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
        calls.append("close")


class NoteIn(BaseModel):
    title: str


app = FastAPI()


@app.post("/notes", status_code=201)
def create(note: NoteIn, db: Session = Depends(get_db)):
    obj = Note(title=note.title)
    db.add(obj)
    db.commit()
    return {"id": obj.id, "title": obj.title}


@app.get("/notes/{note_id}")
def read(note_id: int, db: Session = Depends(get_db)):
    obj = db.get(Note, note_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="note not found")
    return {"id": obj.id, "title": obj.title}


@app.get("/ping")
def ping():
    return {"ok": True}


client = TestClient(app)

print(1, client.post("/notes", json={"title": "shop"}).json())     # 1 {"id": 1, "title": "shop"}
print(2, calls)                                                    # 2 ["open", "close"]

print(3, client.get("/notes/1").json())                            # 3 {"id": 1, "title": "shop"}
print(4, len(calls))                                               # 4 4

print(5, client.get("/notes/9").status_code)                       # 5 404

calls.clear()
client.get("/ping")
print(6, calls)                                                    # 6 []

print(7, client.post("/notes", json={}).status_code)               # 7 401
print(8, calls)                                                    # 8 ["open", "close"]
















































# ОТВЕТЫ
# 1 {'id': 1, 'title': 'shop'}
# 2 ['open', 'close']
#   На запрос FastAPI вызвал get_db: "open", отдал сессию через yield, а после ответа
#   выполнил finally: "close". Сессия живёт ровно один запрос.
# 3 {'id': 1, 'title': 'shop'}
#   Новая сессия, но та же база, поэтому заметка нашлась.
# 4 4
#   Второй запрос: ещё open и close.
# 5 404
# 6 []
#   У ping нет параметра Depends(get_db), значит сессия ему не нужна и не открывается.
# 7 422
#   Нет поля title, Pydantic отклонил тело.
# 8 ['open', 'close']
#   FastAPI подготовил зависимости (open), потом тело не прошло проверку и вернулся 422.
#   Но сессия всё равно закрылась, потому что close стоит в finally.
#   Ради этого get_db и пишут через try/finally: сессия закрывается при любой ошибке,
#   и соединения с базой не "утекают".
