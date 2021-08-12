passw = []
path = r'C:\Scientific Research\Python'
file = open(path + r'\password.txt')
for line in file.readlines():
    passw.append(line.strip())
print(passw)
file.close()