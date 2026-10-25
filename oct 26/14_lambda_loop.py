funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)
print([f() for f in funcs]) # [0,1,2]
