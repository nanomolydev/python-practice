# 44. FastAPI: POST и Pydantic (предскажи, ~15 минут)
# Сначала НЕ запускай. Для каждого print напиши в комментарии, что выведется.
# Потом запусти: python3 44_fastapi_post_predict.py и сверь. Ответы в самом низу.
#
# Новое:
#   GET читает данные, POST создаёт новые. Данные приходят в теле запроса (JSON).
#   class Book(BaseModel) описывает, какой JSON мы ждём: поля и их типы.
#   FastAPI сам проверяет тело по этой модели. Не подходит: 422.
#   book.title читает поле, book.model_dump() превращает модель в обычный dict.
#   status_code=201 в декораторе: код ответа "Created" вместо обычного 200.
#   В тесте тело передают так: client.post("/books", json={...})

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    year: int


app = FastAPI()
BOOKS = {}


@app.post("/books", status_code=201)
def add_book(book: Book):
    new_id = len(BOOKS) + 1
    BOOKS[new_id] = book.model_dump()
    return {"id": new_id, "title": book.title}


client = TestClient(app)

r = client.post("/books", json={"title": "Dune", "year": 1965})
print(1, r.status_code, r.json())      # 1, 201,  {"id": 1, "title": "Dune"}

r = client.post("/books", json={"title": "Metro", "year": "2002"})
print(2, r.status_code, r.json())      # 2, 422, {}

r = client.post("/books", json={"title": "X"})
print(3, r.status_code)                # 3, 201

r = client.post("/books", json={"title": "Y", "year": "abc"})
print(4, r.status_code)                # 4, 422

print(5, BOOKS)                        # {1: {"title": "Dune", "year": 1965}}

r = client.get("/books")
print(6, r.status_code)                # 6, 404
















































# ОТВЕТЫ
# 1 201 {'id': 1, 'title': 'Dune'}
#   status_code=201 из декоратора, id = len(пустого словаря) + 1.
# 2 201 {'id': 2, 'title': 'Metro'}
#   Pydantic сам превращает строку "2002" в число 2002, если она похожа на число.
# 3 422
#   Нет обязательного поля year. Функция даже не запускалась.
# 4 422
#   "abc" в int не превратить, проверка не прошла.
# 5 {1: {'title': 'Dune', 'year': 1965}, 2: {'title': 'Metro', 'year': 2002}}
#   Запросы 3 и 4 не дошли до функции, поэтому в словаре только 2 книги. И у Metro год уже число.
# 6 405
#   Путь /books есть, но только для POST. На GET FastAPI отвечает 405 Method Not Allowed
#   (а не 404: 404 значит "такого пути вообще нет").
