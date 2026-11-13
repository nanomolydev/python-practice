# 41. Повторение pytest (15 минут)
# Запуск:  python3 -m pytest 41_pytest_review.py -v
#
# ЧАСТЬ 1. Предскажи (ответы в самом низу файла, не листай заранее)
#
#   а) В файле есть функции test_one, test_two и check_three, в каждой assert.
#      Сколько тестов запустит pytest?
#
#       два
#
#   б) Что будет с таким тестом?
#          def test_x():
#              with pytest.raises(ValueError):
#                  parse_price("100")
#
#   FAILED
#
# ЧАСТЬ 2. Напиши тесты к parse_price (каждый отдельной функцией test_...):
#   1. "1500" даёт 1500
#   2. "1 500" (с пробелом внутри) даёт 1500
#   3. "abc" выбрасывает ValueError
#   4. пустая строка "" выбрасывает ValueError
#
# Бонус: по правилам цена должна быть БОЛЬШЕ нуля. Напиши тест, который
# это проверяет. Если он упадёт, исправь функцию, чтобы прошли все тесты.

import pytest


def parse_price(text):
    text = text.replace(" ", "")
    if not text.isdigit():
        raise ValueError("not a number")
    price = int(text)
    if price < 0:
        raise ValueError("price must be positive")
    return price


# твои тесты здесь


def test_number():
    assert parse_price("1500") == 1500

def test_number_with_space():
    assert parse_price("1 500") == 1500

def test_value_error():
    with pytest.raises(ValueError):
        parse_price("abc")

def test_space():
    with pytest.raises(ValueError):
        parse_price("")
























# ОТВЕТЫ
# а) 2. pytest запускает только функции, имя которых начинается с test_.
#    check_three он просто не видит.
# б) Тест упадёт с "DID NOT RAISE": "100" нормальная цена, ошибки нет,
#    а pytest.raises требует, чтобы ошибка была.
