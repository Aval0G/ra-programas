import os
import sys
import pdfplumber
import docx
import pypandoc
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messageboxe

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([p.text for p in doc.paragraphs])

def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def convert_text(text, output_format, output_path):
    try:
        if output_format == "txt":
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(text)
        elif output_format in ["docx", "odt", "rtf", "html"]:
            pypandoc.convert_text(text, output_format, format="md", outputfile=output_path)
        messagebox.showinfo("Conversión exitosa", f"Archivo convertido y guardado en: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error en la conversión: {e}")

def convert_file(input_path, output_format, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".txt":
        text = read_txt(input_path)
    elif ext == ".pdf":
        text = read_pdf(input_path)
    elif ext in [".doc", ".docx"]:
        text = read_docx(input_path)
    elif ext == ".html":
        text = read_html(input_path)
    else:
        messagebox.showerror("Error", "Formato no soportado para lectura.")
        return
    
    convert_text(text, output_format, output_path)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])
    entry_input.delete(0, tk.END)
    entry_input.insert(0, file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension="", filetypes=[("Texto", "*.txt"), ("Word", "*.docx"), ("RTF", "*.rtf"), ("HTML", "*.html"), ("ODT", "*.odt")])
    entry_output.delete(0, tk.END)
    entry_output.insert(0, file_path)

def start_conversion():
    input_file = entry_input.get()
    output_file = entry_output.get()
    output_format = os.path.splitext(output_file)[1][1:].lower()
    
    if not input_file or not output_file:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de entrada y una ruta de salida.")
        return
    
    convert_file(input_file, output_format, output_file)

# Interfaz gráfica
root = tk.Tk()
root.title("Conversor de Archivos de Texto")
root.geometry("500x250")

tk.Label(root, text="Archivo de Entrada:").pack()
entry_input = tk.Entry(root, width=50)
entry_input.pack()
tk.Button(root, text="Abrir", command=open_file).pack()

tk.Label(root, text="Archivo de Salida:").pack()
entry_output = tk.Entry(root, width=50)
entry_output.pack()
tk.Button(root, text="Guardar como", command=save_file).pack()

tk.Button(root, text="Convertir", command=start_conversion).pack()

if pypandoc.get_pandoc_path() is None:
    print("Descargando Pandoc...")
    pypandoc.download_pandoc()


root.mainloop()
