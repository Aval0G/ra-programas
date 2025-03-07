import os
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu
from docx import Document as DocxDocument
from odf.opendocument import OpenDocumentText, load
from odf.text import P
from striprtf.striprtf import rtf_to_text
from bs4 import BeautifulSoup
import PyPDF2
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import textract
from PyRTF.Elements import Document as RTFDocument, Section as RTFSection, Text as RTFText
from PyRTF.Renderer import Renderer, Paragraph as RTFParagraph
import pypandoc
import re

SUPPORTED_EXTENSIONS = ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.html', '.odt']

"""READ FUNCTIONS"""
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_docx(file_path):
    doc = DocxDocument(file_path)
    return '\n'.join(p.text for p in doc.paragraphs)

def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def read_rtf(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return rtf_to_text(f.read())

def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text()

def read_odt(file_path):
    doc = load(file_path)
    text = ""
    for paragraph in doc.getElementsByType(P):
        for node in paragraph.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
        text += '\n'
    return text

def read_doc(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        return f"Error reading DOC file: {e}"

"""WRITE FUNCTIONS"""
def write_txt(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def write_docx(text, file_path):
    doc = DocxDocument()
    for line in text.split('\n'):
        doc.add_paragraph(line)
    doc.save(file_path)

def write_odt(text, file_path):
    doc = OpenDocumentText()
    doc.text.addElement(P(text=text))
    doc.save(file_path)

def write_pdf(text, file_path):
    pdf = canvas.Canvas(file_path, pagesize=LETTER)
    width, height = LETTER
    y = height - 40
    for line in text.split('\n'):
        pdf.drawString(40, y, line)
        y -= 15
        if y < 40:
            pdf.showPage()
            y = height - 40
    pdf.save()

def write_rtf(text, file_path):
    def escape_rtf(txt):
        txt = txt.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
        txt = re.sub(r'([\u0080-\uffff])', lambda m: r'\u{}?'.format(ord(m.group(1))), text)
        return txt

    doc = RTFDocument()
    section = RTFSection()
    doc.Sections.append(section)
    
    paragraph = RTFParagraph()
    paragraph.append(RTFText(escape_rtf(text)))
    section.append(paragraph)

    renderer = Renderer()
    
    with open(file_path, 'w', encoding='utf-8') as fout:
        renderer.Write(doc, fout)

def write_html(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('<html><body>')
        for paragraph in text.split('\n\n'):
            f.write('<p>')
            f.write(paragraph.replace('\n', '<br>'))
            f.write('</p>')
        f.write('</body></html>')

READERS = {
    '.txt': read_txt,
    '.docx': read_docx,
    '.pdf': read_pdf,
    '.rtf': read_rtf,
    '.html': read_html,
    '.odt': read_odt,
    '.doc': read_doc
}

WRITERS = {
    '.txt': write_txt,
    '.docx': write_docx,
    '.pdf': write_pdf,
    '.rtf': write_rtf,
    '.html': write_html,
    '.odt': write_odt
}

def convert_file(input_file, output_format, output_folder):
    ext = os.path.splitext(input_file)[1].lower()
    reader = READERS.get(ext)
    
    if not reader:
        print(f"No reader implemented for '{ext}' files.")
        return
    
    text = reader(input_file)
    output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_converted{output_format}")
    
    writer = WRITERS.get(output_format)
    
    if not writer:
        print(f"No writer implemented for '{output_format}' files.")
        return
    
    writer(text, output_file)
    print(f"Conversion complete! File saved to: {output_file}")

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    input_file_var.set(file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

def start_conversion():
    input_file = input_file_var.get()
    output_folder = output_folder_var.get()
    output_format = output_format_var.get()
    
    if not input_file or not output_folder:
        print("Please select both input file and output folder.")
        return
    
    convert_file(input_file, output_format, output_folder)

app = Tk()
app.title("Text Converter")

input_file_var = StringVar()
output_folder_var = StringVar()
output_format_var = StringVar(value=".pdf")

Label(app, text="Select Input File:").grid(row=0, column=0, padx=10, pady=10)
Button(app, text="Browse", command=select_input_file).grid(row=0, column=1, padx=10, pady=10)
Label(app, textvariable=input_file_var).grid(row=0, column=2, padx=10, pady=10)

Label(app, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=10)
Button(app, text="Browse", command=select_output_folder).grid(row=1, column=1, padx=10, pady=10)
Label(app, textvariable=output_folder_var).grid(row=1, column=2, padx=10, pady=10)

Label(app, text="Select Output Format:").grid(row=2, column=0, padx=10, pady=10)
OptionMenu(app, output_format_var, ".pdf", ".docx", ".odt", ".txt", ".rtf", ".html").grid(row=2, column=1, padx=10, pady=10)

Button(app, text="Convert", command=start_conversion).grid(row=3, column=0, columnspan=3, padx=10, pady=10)

app.mainloop()
