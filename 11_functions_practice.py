from collections import Counter, defaultdict
# 1. Функция even_squares(nums) возвращает квадраты только чётных чисел. Одной строкой, через генератор списка.

# 2. Функция merge(*dicts) принимает любое количество словарей и складывает значения одинаковых ключей. Исходные словари менять нельзя.

# 3. Функция count_words(text, min_len=1) считает слова в тексте, но только те, у которых длина не меньше min_len. Регистр не важен: «Кот» и «кот» — одно слово.

# 4. Функция report(**kwargs) возвращает строку, где каждая пара — отдельная строка вида ключ: значение, отсортированная по ключу.

def even_squares(nums):
    return [i**2 for i in nums if i%2==0]

def merge(*dicts):
    result = Counter()
    for i in dicts:
        result.update(i)
    return dict(result)

def count_words(text, min_len=1):
    return Counter([i.lower() for i in text.split() if len(i)>=min_len])

def report(**kwargs):
    return "\n".join(f"{k}: {kwargs[k]}" for k in sorted(kwargs))


# Тесты (вставь в конец файла):
assert even_squares([1, 2, 3, 4]) == [4, 16]
assert even_squares([]) == []

d1, d2 = {"a": 1}, {"a": 2, "b": 3}
assert merge(d1, d2, {"b": 1}) == {"a": 3, "b": 4}
assert merge() == {}
assert d1 == {"a": 1}

assert count_words("Кот пёс кот мышь") == {"кот": 2, "пёс": 1, "мышь": 1}
assert count_words("Кот пёс кот мышь", min_len=4) == {"мышь": 1}

assert report(b=2, a=1) == "a: 1\nb: 2"

print("Все тесты пройдены")