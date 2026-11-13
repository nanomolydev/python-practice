# 43. FastAPI: пишем эндпоинты сами (25 минут)
# Запуск:  python3 43_fastapi_practice.py   (если все assert прошли, увидишь "OK")
#
# Новое: как вернуть 404, если чего-то нет.
#   from fastapi import HTTPException
#   raise HTTPException(status_code=404, detail="book not found")
# Клиент получит код 404 и тело {"detail": "book not found"}.
#
# Данные лежат прямо в словаре (базу подключим позже):

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

BOOKS = {
    1: {"title": "Dune", "year": 1965},
    2: {"title": "Metro 2033", "year": 2002},
    3: {"title": "The Martian", "year": 2011},
}

app = FastAPI()

# ЗАДАНИЕ. Напиши три эндпоинта:
#
#   1. GET /ping
#      возвращает {"ok": True}
#
#   2. GET /books/{book_id}
#      возвращает книгу из BOOKS, например /books/1 даёт {"title": "Dune", "year": 1965}
#      если такой книги нет: 404 с detail "book not found"
#
#   3. GET /books?min_year=2000
#      возвращает {"titles": [...]} : названия книг, у которых year >= min_year,
#      по алфавиту. Если min_year не передали, считай его 0 (то есть все книги).


# твой код здесь

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/books/{book_id}") 
def book_return(book_id: int):
    result = BOOKS.get(book_id, None)
    if result is None:
        raise HTTPException(status_code=404, detail="book not found")
    else:
        return result

@app.get("/books")
def min_year_books(min_year: int = 0):
    result = []

    for i in BOOKS.values():
        if i.get("year") >= min_year:
            result.append(i.get("title"))
        
        
    return {"titles": sorted(result)}


if __name__ == "__main__":
    client = TestClient(app)

    assert client.get("/ping").json() == {"ok": True}
    assert client.get("/books/1").json() == {"title": "Dune", "year": 1965}
    r = client.get("/books/99")
    assert r.status_code == 404
    assert r.json() == {"detail": "book not found"}
    assert client.get("/books/abc").status_code == 422

    print(client.get("/books?min_year=2000").json())
    assert client.get("/books?min_year=2000").json() == {"titles": ["Metro 2033", "The Martian"]}
    assert client.get("/books").json() == {"titles": ["Dune", "Metro 2033", "The Martian"]}
    assert client.get("/books?min_year=2050").json() == {"titles": []}

    print("OK")

# Бонус (если останется время): запусти настоящий сервер
#   fastapi dev 43_fastapi_practice.py
# и открой в браузере http://127.0.0.1:8000/docs
# Там FastAPI сам нарисовал страницу со всеми твоими эндпоинтами, их можно потыкать.
