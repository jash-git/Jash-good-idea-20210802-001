import itertools
from PyPDF2 import PdfFileReader

mylist = ("".join(x) for x in itertools.product("123abc", repeat=4))
path = r'C:\xxx'
pdf_reader = PdfFileReader(path + r'\test.pdf')

while True:
    i = next(mylist)
    if pdf_reader.decrypt(i):
        print(f'破解成功，密码为{i}')
        break
    else:
        print(f'破解不成功，密码{i}错误')