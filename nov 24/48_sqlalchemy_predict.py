# 48. Новая тема: SQLAlchemy ORM (предскажи, ~20 минут)
#
# Установка (один раз):  python3 -m pip install --user sqlalchemy
#
# Сначала НЕ запускай. Для каждого print напиши в комментарии, что выведется.
# Потом запусти и сверь. Ответы с объяснениями в самом низу.
#
# Зачем это: в 46 ты писал SQL руками. ORM позволяет работать с таблицей как с классом:
# строка таблицы = объект, колонка = атрибут. Почти во всех вакансиях Python backend
# стоит SQLAlchemy, и с FastAPI её используют чаще всего.
#
# Новое:
#   class Note(Base): описывает таблицу. __tablename__ = имя таблицы.
#   Mapped[int] и mapped_column(...): колонка и её тип.
#   Base.metadata.create_all(engine): создаёт таблицы (как CREATE TABLE).
#   Session: "разговор" с базой. session.add(obj) кладёт объект, session.commit() сохраняет.
#   session.get(Note, 1): найти по id (нет такой строки -> None).
#   select(Note).where(...): запрос как SELECT ... WHERE, session.scalars(...).all() даёт список объектов.
#   session.delete(obj): удалить объект (сохранится после commit).

from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)


engine = create_engine("sqlite://")      # sqlite в памяти
Base.metadata.create_all(engine)

with Session(engine) as session:
    a = Note(title="shop")
    b = Note(title="anki", done=True)
    print(1, a.id)                                   # 1 1

    session.add_all([a, b])
    session.commit()
    print(2, a.id, b.id)                             # 2 1 2

    print(3, a.done)                                 # 3 False

    n = session.get(Note, 2)
    print(4, n.title, n is b)                        # 4 anki True

    print(5, session.get(Note, 7))                   # 5 Not Found

    rows = session.scalars(select(Note).where(Note.done == False)).all()
    print(6, [r.title for r in rows])                # 6 [Note(id="1", title="shop", done=False)]

    a.title = "shop: milk"
    session.commit()
    print(7, session.get(Note, 1).title)             # 7 shop: milk

    session.delete(b)
    session.commit()
    print(8, len(session.scalars(select(Note)).all()))   # 8 1




















































# ОТВЕТЫ
# 1 None
#   Объект создан, но в базу ещё не попал. id выдаёт база, а до commit её никто не спрашивал.
# 2 1 2
#   После commit база выдала id, и SQLAlchemy записала их в объекты.
# 3 False
#   default=False подставился, потому что done не передали.
# 4 anki True
#   session.get нашёл строку с id 2. И это ТОТ ЖЕ объект b, а не копия: в одной сессии
#   одна строка = один объект.
# 5 None
#   Строки с id 7 нет. Ошибки нет, просто None (как dict.get). Отсюда в FastAPI будет 404.
# 6 ['shop']
#   where(Note.done == False) превращается в SQL "WHERE done = 0". Пишем ==, а не is:
#   это не обычное сравнение Python, SQLAlchemy строит из него условие запроса.
# 7 shop: milk
#   Поменял атрибут и сделал commit: SQLAlchemy сама сделала UPDATE. SQL руками писать не нужно.
# 8 1
#   delete + commit удалили строку, осталась одна заметка.
