def parse_age(text):
    try:
        age = int(text)
        print("A")
    except ValueError:
        print("B")
        return -1
    else:
        print("C")
        return age
    finally:
        print("D")


print(parse_age("19"))     # 1
print(parse_age("abc"))    # 2

try:
    x = [1, 2][5]
except ValueError:
    print("E")
except IndexError as e:
    print("F", e)          # 3

try:
    raise KeyError("id")
except Exception:
    print("G")             # 4