import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Imágenes")
        self.root.geometry("400x250")

        self.label = tk.Label(root, text="Seleccionar imagen")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Cargar Imagen", command=self.load_image)
        self.select_button.pack()

        self.format_label = tk.Label(root, text="Selecciona el formato de salida:")
        self.format_label.pack(pady=5)

        self.format_options = ["JPEG", "PNG", "GIF", "BMP", "TIFF", "SVG"]
        self.format_var = tk.StringVar(value=self.format_options[0])
        self.format_menu = tk.OptionMenu(root, self.format_var, *self.format_options)
        self.format_menu.pack()

        self.convert_button = tk.Button(root, text="Convertir y Guardar", command=self.convert_image)
        self.convert_button.pack(pady=10)

        self.image_path = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Todos los formatos soportados", "*.jpeg;*.jpg;*.png;*.gif;*.bmp;*.tiff;*.svg"),
            ("JPEG", "*.jpeg;*.jpg"),
            ("PNG", "*.png"),
            ("GIF", "*.gif"),
            ("BMP", "*.bmp"),
            ("TIFF", "*.tiff"),
            ("SVG", "*.svg")
        ])
        
        if file_path:
            self.image_path = file_path
            self.label.config(text=f"Imagen cargada: {os.path.basename(file_path)}")

    def convert_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Por favor, selecciona una imagen primero")
            return

        output_format = self.format_var.get()
        save_path = filedialog.asksaveasfilename(defaultextension=f".{output_format.lower()}",
                                                 filetypes=[(output_format, f"*.{output_format.lower()}")])
        
        if not save_path:
            return

        try:
            img = Image.open(self.image_path)
            img.save(save_path, output_format)
            messagebox.showinfo("Éxito", f"Imagen guardada en {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo convertir la imagen: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
