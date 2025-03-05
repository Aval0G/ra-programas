import os
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

# This function is not working, so save it in case it gets fixed in the future
""" def read_rtf_deprecated(file_path):
    if pypandoc.get_pandoc_path() is None:
        print("Installing pandoc to read RTF files...")
        pypandoc.download_pandoc()

    return pypandoc.convert_file(file_path, 'plain', format='rtf') """

def read_rtf(file_path):
    # use striprtf to extract text from RTF files
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
    # Since doc files are outdated, we can use textract to extract text
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
    y = height - 40  # Start near the top
    for line in text.split('\n'):
        pdf.drawString(40, y, line)
        y -= 15
        if y < 40:
            pdf.showPage()
            y = height - 40
    pdf.save()

def write_rtf(text, file_path):
    def escape_rtf(txt):
        """Convert special characters to RTF compatible escape sequences"""
        txt = txt.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
        txt = re.sub(r'([\u0080-\uffff])', lambda m: r'\u{}?'.format(ord(m.group(1))), text)
        return txt

    doc = RTFDocument()
    section = RTFSection()
    doc.Sections.append(section)
    
    # Use Paragraph instead of appending Text directly
    paragraph = RTFParagraph()
    paragraph.append(RTFText(escape_rtf(text)))
    section.append(paragraph)  # Append paragraph to the section

    renderer = Renderer()
    
    with open(file_path, 'w', encoding='utf-8') as fout:
        renderer.Write(doc, fout)

def write_html(text, file_path):
    # Make the text an HTML page (use <p> tags, one pair for each paragraph, and add <br> tags for line breaks)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('<html><body>')
        for paragraph in text.split('\n\n'):
            f.write('<p>')
            f.write(paragraph.replace('\n', '<br>'))
            f.write('</p>')
        f.write('</body></html>')

# Mapping extensions to their reader functions
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

def list_supported_files():
    files = [f for f in os.listdir() if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    return files

def main():
    print("📄 Searching for supported documents in this directory...\n")
    files = list_supported_files()
    
    if not files:
        print("No supported documents found.")
        return
    
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    
    choice = int(input("\nEnter the number of the file you want to convert: ")) - 1
    
    if choice < 0 or choice >= len(files):
        print("Invalid selection for input file.")
        return
    
    choice_output = int(input("Enter the number of the output format you want to convert to:\n1. PDF\n2. DOCX\n3. ODT\n4. TXT\n5. RTF\n6. HTML\n")) - 1
    if choice_output < 0 or choice_output >= 6:
        print("Invalid selection for output format.")
        return
    
    output_format = ['.pdf', '.docx', '.odt', '.txt', '.rtf', '.html'][choice_output]

    selected_file = files[choice]
    ext = os.path.splitext(selected_file)[1].lower()
    
    print(f"\nReading '{selected_file}'...")
    reader = READERS.get(ext)
    
    if not reader:
        print(f"No reader implemented for '{ext}' files.")
        return
    
    text = reader(selected_file)
    output_file = f"{os.path.splitext(selected_file)[0]}_converted{output_format}"
    
    print(f"Writing to '{output_file}'...")
    writer = WRITERS.get(output_format)
    
    if not writer:
        print(f"No writer implemented for '{output_format}' files.")
        return
    
    writer(text, output_file)
    
    print(f"Conversion complete! File saved to: {output_file}")

if __name__ == "__main__":
    main()