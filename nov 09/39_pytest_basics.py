# 39. pytest: основы
#
# Установка (один раз):   python3 -m pip install --user pytest
# Запуск:                 python3 -m pytest "39_pytest_basics.py" -v
#                         (из папки nov 09)
#
# Как это работает:
#   pytest сам находит функции, имя которых начинается с test_,
#   и запускает каждую отдельно. Внутри обычный assert.
#   Если assert упал, тест FAILED, остальные тесты всё равно запускаются.
#   Не нужно print("OK") и не нужно вызывать тесты руками.
#
#   pytest.raises(ОшибкаКласс) проверяет, что код ВЫБРОСИЛ эту ошибку:
#       with pytest.raises(ValueError):
#           int("abc")
#   (да, это контекстный менеджер, как твой Transaction)
#
# ПРЕДСКАЖИ: какие тесты будут PASSED, а какие FAILED? Запиши, потом запусти.
# Ответы внизу.

import pytest


def discount(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("bad percent")
    return price - price * percent // 100


def test_no_discount():
    assert discount(200, 0) == 200


def test_half():
    assert discount(200, 50) == 100


def test_ten_percent():
    assert discount(99, 10) == 89.1


def test_bad_percent():
    with pytest.raises(ValueError):
        discount(100, 150)


def test_bad_percent_wrong():
    with pytest.raises(ValueError):
        discount(100, 100)


def helper_check():
    assert discount(100, 10) == 1


# Ответы ниже, не листай заранее.
#
#
#
#
#
#
#
#
#
#
#
# test_no_discount         PASSED
# test_half                PASSED
# test_ten_percent         FAILED: 99 * 10 // 100 = 9 (целочисленное деление), 99 - 9 = 90, а не 89.1
# test_bad_percent         PASSED: 150 вне диапазона, ValueError выброшен
# test_bad_percent_wrong   FAILED: 100 допустимо, ошибки НЕТ, а pytest.raises её ждал
#                          ("DID NOT RAISE")
# helper_check             не запускается вообще: имя не начинается с test_
# Итог: 3 passed, 2 failed
