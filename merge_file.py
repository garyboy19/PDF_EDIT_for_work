from PyPDF2 import PdfWriter, PdfReader

pdf2 = PdfReader(open('output.pdf', 'rb'))

#读取已有的PDF
existing_pdf = PdfReader(open("test01.pdf", "rb"))
output = PdfWriter()

# Get the number of pages in the PDF files
num_pages = min(len(existing_pdf.pages), len(pdf2.pages))
#
for i in range(0,num_pages):
    page = existing_pdf.pages[i]
    page.merge_page(pdf2.pages[i])
    output.add_page(page)

# 最后，向目标的pdf写出
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()