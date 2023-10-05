from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Create a canvas object with the specified PDF file name
pdf_path = 'output.pdf'
c = canvas.Canvas(pdf_path, pagesize=A4)

# Register the font file that supports Chinese characters
font_path = 'C:\windows\Fonts\simsun.ttc'
pdfmetrics.registerFont(TTFont('simsun', font_path))

# Set the font and font size
font_name = 'simsun'
font_size = 10

# Set the position to add the text 图标位置
x = 100
y = 100

# Open the file in read mode
with open('test.txt', 'r', encoding='utf-8') as file:
    # Read the contents line by line
    for line in file:
        # Print each line
        c.setFont(font_name, font_size)
        c.drawString(x, y, line.strip())
        c.showPage()

# Save the canvas to the PDF file
c.save()

pdf2 = PdfReader(open('output.pdf', 'rb'))

#读取已有的PDF
existing_pdf = PdfReader(open("9_pages.pdf", "rb"))
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
