# 42. FastAPI: первые эндпоинты (предскажи, 20 минут)
#
# Установка (один раз):  python3 -m pip install --user "fastapi[standard]"
# Запуск:                python3 42_fastapi_basics.py
#
# Как это устроено:
#   app = FastAPI()          создаём приложение
#   @app.get("/путь")        "когда придёт GET-запрос на этот путь, вызови функцию ниже"
#   return {...}             словарь, который вернула функция, клиент получит как JSON
#
#   /users/{user_id}         кусок пути в фигурных скобках попадает в аргумент функции
#   def search(q: str)       аргумент, которого нет в пути, берётся из ?q=... в адресе
#
# TestClient шлёт запросы прямо из кода, сервер запускать не нужно:
#   r.status_code   код ответа: 200 всё ок, 404 нет такого адреса, 422 неверные данные
#   r.json()        тело ответа как словарь
#
# ЗАДАНИЕ: напиши рядом с каждым print, что он выведет. Потом запусти и сверь.
# Ответы с объяснениями в самом низу, не листай заранее.

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
def home():
    return {"message": "hello"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "double": user_id * 2}


@app.get("/search")
def search(q: str, limit: int = 10):
    return {"q": q, "limit": limit}


client = TestClient(app)

print(1, client.get("/").json())                          # твой ответ: {"message": "hello"}
print(2, client.get("/users/5").json())                   # твой ответ: {"id": 5, "double": 10}
print(3, client.get("/users/abc").status_code)            # твой ответ: 422
print(4, client.get("/search?q=python").json())           # твой ответ: {"q": python, "limit": 10}
print(5, client.get("/search?q=python&limit=3").json())   # твой ответ: {"q": python, "limit": 3}
print(6, client.get("/search").status_code)               # твой ответ: 422
print(7, client.get("/nothing").status_code)              # твой ответ: 404





























# ОТВЕТЫ
# 1 {'message': 'hello'}
# 2 {'id': 5, 'double': 10}
#   В адресе "5" это строка, но из-за user_id: int FastAPI сам превратил её в число.
#   Без аннотации было бы "55" (строка * 2).
# 3 422
#   "abc" не число. FastAPI сам проверил тип и отказал, функция даже не вызывалась.
# 4 {'q': 'python', 'limit': 10}
#   limit не передали, взялось значение по умолчанию.
# 5 {'q': 'python', 'limit': 3}
#   "3" из адреса тоже стало числом.
# 6 422
#   у q нет значения по умолчанию, значит он обязательный.
# 7 404
#   такого пути нет.
