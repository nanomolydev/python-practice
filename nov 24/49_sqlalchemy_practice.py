# 49. SQLAlchemy: пишем сами (~40 минут)
# Запуск: python3 49_sqlalchemy_practice.py   (все assert прошли -> "OK")
#
# Те же заметки, что в 45 и 46, только через ORM, а не через SQL руками.
# Пока без FastAPI: просто функции. В следующий раз подключим их к эндпоинтам.
# Подсматривай в 48, это нормально.

from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass
    

# 0. Модель Note: таблица "notes", поля id (primary key), title (строка до 100), text (строка до 500).

class Note(Base):
    __tablename__ = "notes "
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String(500))



engine = create_engine("sqlite://")


# Каждая функция получает session первым аргументом.
#
#   1. create_note(session, title, text) -> int
#      создаёт заметку, сохраняет, возвращает её id
#
#   2. get_note(session, note_id) -> dict или None
#      {"title": ..., "text": ...} или None, если нет
#
#   3. list_titles(session) -> list
#      названия всех заметок по алфавиту.
#      Попробуй сортировать в самом запросе: select(...).order_by(Note.title)
#
#   4. delete_note(session, note_id) -> bool
#      True, если удалили, False, если такой не было
#
#   5. update_text(session, note_id, new_text) -> bool
#      меняет text, True/False


# твой код здесь

def create_note(session,title,text):
    item = Note(title=title, text=text)
    session.add(item)
    session.commit()
    return item.id

def get_note(session:Session,note_id):
    row = session.get(Note, note_id)
    if(row is not None):
        return {"title": row.title, "text": row.text}
    else:
        return None

def list_titles(session: Session):
    rows = session.scalars(select(Note).order_by(Note.title)).all()
    if(rows is not None):
            return [row.title for row in rows]
    else:
        return None

def delete_note(session: Session, note_id):
    row = session.get(Note, note_id)
    if(row is not None):
        session.delete(row)
        session.commit()
        return True
    else:
        return False

def update_text(session: Session, note_id, new_text):
    row = session.get(Note, note_id)
    
    if(row is not None):
        row.text = new_text
        session.add(row)
        session.commit()
        return True
    else:
        return False
    

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        assert create_note(s, "shop", "milk, bread") == 1
        assert create_note(s, "anki", "20 cards") == 2
        assert create_note(s, "gym", "back day") == 3

        assert get_note(s, 1) == {"title": "shop", "text": "milk, bread"}
        assert get_note(s, 99) is None

        assert list_titles(s) == ["anki", "gym", "shop"]

        assert delete_note(s, 1) is True
        assert delete_note(s, 1) is False
        assert list_titles(s) == ["anki", "gym"]

        assert update_text(s, 2, "30 cards") is True
        assert update_text(s, 99, "x") is False
        assert get_note(s, 2) == {"title": "anki", "text": "30 cards"}

    # новая сессия: проверяем, что всё правда сохранилось (commit не забыт)
    with Session(engine) as s2:
        assert list_titles(s2) == ["anki", "gym"]
        assert get_note(s2, 2) == {"title": "anki", "text": "30 cards"}

    print("OK")

# Бонус: в 47 ты удалял одним запросом через rowcount. Здесь удаление в 2 шага:
# get, потом delete. Подумай, почему в ORM так обычно и делают, и когда это может быть плохо
# (подсказка: сколько запросов уходит в базу, если удалять 10 000 заметок по одной).
