import itertools
mylist = ("".join(x) for x in itertools.product("0123456789abcdef", repeat=4))
print(next(mylist))