# 40. Пишем тесты сами (15 минут)
#
# Функция parse_age уже написана. Твоя задача: написать к ней тесты.
# Запуск:  python3 -m pytest 40_pytest_practice.py -v
#
# Напиши 4 теста (каждый отдельной функцией test_...):
#   1. обычная строка "19" превращается в число 19
#   2. пробелы по краям не мешают: "  25 " даёт 25
#   3. "abc" выбрасывает ValueError
#   4. "-5" выбрасывает ValueError
#
# Потом бонус: найди, что функция делает НЕ так, напиши тест, который это ловит
# (он должен упасть), и исправь функцию, чтобы все тесты прошли.
# Подсказка к бонусу: людям не бывает 500 лет.

import pytest


def parse_age(text):
    text = text.strip()
    if not text.isdigit():
        raise ValueError("not a number")
    age = int(text)
    if age < 0:
        raise ValueError("negative")
    return age


# твои тесты здесь
def test_text_to_number():
    assert parse_age("19") == 19

def test_space_delete():
    assert parse_age("  25 ") == 25

def test_string_error():
    with pytest.raises(ValueError):
        assert parse_age("abc")

def test_negative_number():
    with pytest.raises(ValueError):
        assert parse_age("-5")