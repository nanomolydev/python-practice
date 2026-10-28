def make_greeting(name):
    def greet():
        print(name)

    return greet


a = make_greeting("Test1")
b = make_greeting("Test2")

a() # Test1
b() # Test2
a() # Test1