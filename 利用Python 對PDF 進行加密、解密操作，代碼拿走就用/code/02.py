from PyPDF2 import PdfFileWriter, PdfFileReader
path = r'C:\xxx'

pdf_reader = PdfFileReader(path + r'\test.pdf')
pdf_reader.decrypt('a123') #
pdf_writer = PdfFileWriter()

for page in range(pdf_reader.getNumPages()):
    pdf_writer.addPage(pdf_reader.getPage(page))
with open(path + r'\test.pdf', 'wb') as out:
    pdf_writer.write(out)