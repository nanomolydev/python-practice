prices = {"хлеб": 50, "молоко": 90}
print(prices.get("сыр", "нет в наличии")) # нет в наличии
print(prices.get("хлеб", 0)) # 50

total = 0
for name, price in prices.items():
    total += price
print(total) # 140

for x in prices:
    print(x) # хлеб, молоко