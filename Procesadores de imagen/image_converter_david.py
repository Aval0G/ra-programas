import os
import tkinter as tk
from tkinter import filedialog, StringVar, ttk
from PIL import Image

# Load Cairo library explicitly for SVG support
import ctypes
# Use custom path to the libcairo-2.dll file (bin folder has to be in the same directory as the script)
current_dir = os.path.dirname(os.path.abspath(__file__))
cairo_path = os.path.join(current_dir, "bin\\libcairo-2.dll")
ctypes.windll.LoadLibrary(cairo_path)
import cairosvg

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg']

def convert_image(input_path, output_path, output_format):
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == '.svg' and output_format != '.svg':
        if output_format == '.png':
            cairosvg.svg2png(url=input_path, write_to=output_path)
        elif output_format == '.pdf':
            cairosvg.svg2pdf(url=input_path, write_to=output_path)
        else:
            print(f"SVG to {output_format} conversion not supported.")
        return
    
    with Image.open(input_path) as img:
        img = img.convert("RGBA") if output_format in ['.png', '.gif'] else img.convert("RGB")
        img.save(output_path, output_format.upper().replace('.', ''))

def select_input_file(input_file_var):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpeg;*.jpg;*.png;*.gif;*.bmp;*.tiff;*.svg")])
    if file_path:
        input_file_var.set(file_path)

def select_output_folder(output_folder_var):
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)

def start_conversion(input_file_var, output_folder_var, output_format_var, status_label):
    input_file = input_file_var.get()
    output_folder = output_folder_var.get()
    output_format = output_format_var.get()
    
    if not input_file or not output_folder:
        status_label.config(text="ERROR: Select both input file and output folder!", foreground="red")
        return
    
    output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_converted{output_format}")
    
    try:
        convert_image(input_file, output_file, output_format)
        status_label.config(text=f"SUCCESS: Converted to {output_format}!", foreground="green")
        os.startfile(output_folder)
    except Exception as e:
        status_label.config(text=f"ERROR: {e}", foreground="red")

def main():
    app = tk.Tk()
    app.title("Image Converter")
    
    width, height = 700, 400
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.configure(bg="#f0f0f0")
    
    input_file_var = StringVar()
    output_folder_var = StringVar()
    output_format_var = StringVar(value=".png")
    
    main_frame = ttk.Frame(app, padding=20)
    main_frame.pack(expand=True)
    
    ttk.Label(main_frame, text="Select Input File:").pack(anchor="w", pady=5)
    ttk.Entry(main_frame, textvariable=input_file_var, width=40, font=("Arial", 12), state='readonly').pack(pady=5)
    ttk.Button(main_frame, text="Browse", command=lambda: select_input_file(input_file_var)).pack(pady=5)
    
    ttk.Label(main_frame, text="Select Output Folder:").pack(anchor="w", pady=5)
    ttk.Entry(main_frame, textvariable=output_folder_var, width=40, font=("Arial", 12), state='readonly').pack(pady=5)
    ttk.Button(main_frame, text="Browse", command=lambda: select_output_folder(output_folder_var)).pack(pady=5)
    
    ttk.Label(main_frame, text="Select Output Format:").pack(anchor="w", pady=5)
    ttk.Combobox(main_frame, textvariable=output_format_var, values=SUPPORTED_EXTENSIONS, font=("Arial", 12), state='readonly').pack(pady=5)
    
    convert_button = ttk.Button(main_frame, text="Convert", command=lambda: start_conversion(input_file_var, output_folder_var, output_format_var, status_label))
    convert_button.pack(pady=20)
    
    status_label = ttk.Label(main_frame, text="", font=("Arial", 12, "bold"))
    status_label.pack(pady=5)
    
    app.mainloop()

if __name__ == "__main__":
    main()