from PyPDF2 import PdfFileReader

passw = []
path = r'C:\xxx'
file = open(path + r'\password.txt')
for line in file.readlines():
    passw.append(line.strip())
file.close()

path = r'C:\xxx'
pdf_reader = PdfFileReader(path + r'\test.pdf')

for i in passw:
    if pdf_reader.decrypt(i):
        print(f'破解成功，密码为{i}')
    else:
        print(f'破解不成功，密码{i}错误')