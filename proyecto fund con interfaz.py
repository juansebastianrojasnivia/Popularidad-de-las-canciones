import tkinter as tk
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk 
import os

# --- Configuración Fija del Archivo ---
RUTA_CSV_FIJA = r'C:\Users\juanj\Desktop\ARCHIVO DE FUND\archivo.csv'
COLUMNA_IMAGEN = r'C:\Users\juanj\Desktop\ARCHIVO DE FUND\IMAGENES FUND' 

class CSVImageApp:
    def __init__(self, master):
        self.master = master
        master.title("Visualizador de Datos e Imágenes CSV")

        # >>>>>> SOLUCIÓN AÑADIDA AQUÍ <<<<<<
        # Asocia la tecla Enter (<Return>) al método para mostrar la fila.
        master.bind('<Return>', lambda event=None: self.display_row_and_image())
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # Variables y Datos
        self.df = None
        self.max_rows = 0
        self.row_index = tk.StringVar(value="")
        self.current_image = None 
        
        # 1. Cargar el archivo inmediatamente
        self.load_csv_file()

        # --- Interfaz del Visor de Filas ---
        
        # ... (El resto de la configuración de la interfaz, etiquetas y widgets sigue igual) ...
        
        # Etiqueta de contexto y rango
        tk.Label(master, text=f"Archivo: {os.path.basename(RUTA_CSV_FIJA)}", fg='gray').grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
        self.range_label = tk.Label(master, text=f"Rango: 1 a {self.max_rows}", fg='blue')
        self.range_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Entrada y Botón
        tk.Label(master, text="Nº de Fila:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.row_index, width=10).grid(row=2, column=1, padx=10, pady=5, sticky='w')
        tk.Button(master, text="Mostrar", command=self.display_row_and_image).grid(row=2, column=2, padx=10, pady=5)

        # Frame de Datos (Izquierda)
        data_frame = tk.Frame(master)
        data_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nw')
        tk.Label(data_frame, text="Contenido de la Fila:").pack(anchor='w')
        self.result_text = tk.Text(data_frame, height=15, width=45, wrap=tk.WORD, state='disabled')
        self.result_text.pack()
        
        # Frame de Imagen (Derecha)
        image_frame = tk.Frame(master)
        image_frame.grid(row=3, column=2, padx=10, pady=10, sticky='ne')
        tk.Label(image_frame, text="Imagen:").pack(anchor='w')
        
        self.image_label = tk.Label(image_frame, text="Esperando Imagen...")
        self.image_label.pack()
        
        self.clear_result_text("Introduce un número de fila para comenzar.")
        self.image_label.config(width=450, height=250)
        
    # (El resto de las funciones: load_csv_file, display_row_and_image, load_and_display_image, etc., permanecen sin cambios)

    def load_csv_file(self):
        # ... (código sin cambios)
        try:
            self.df = pd.read_csv(RUTA_CSV_FIJA)
            self.max_rows = len(self.df)
            if hasattr(self, 'range_label'):
                 self.range_label.config(text=f"Rango: 1 a {self.max_rows}")
        except FileNotFoundError:
            messagebox.showerror("Error Fatal", f"No se encontró el archivo: {RUTA_CSV_FIJA}")
            self.df = None
            self.max_rows = 0
            
    def display_row_and_image(self):
        # ... (código sin cambios)
        if self.df is None or self.max_rows == 0:
            messagebox.showwarning("Advertencia", "Error de carga. Revise la ruta del CSV.")
            return

        try:
            numero_fila = int(self.row_index.get())
            
            if not (1 <= numero_fila <= self.max_rows):
                messagebox.showwarning("Fuera de rango", f"El número debe ser de 1 a {self.max_rows}.")
                return

            fila = self.df.iloc[numero_fila - 1]
            output = f"--- Fila N° {numero_fila} ---\n\n"
            output += fila.to_string()
            self.update_result_text(output)
            #mod
            image_path =f'{numero_fila}.png'# fila[COLUMNA_IMAGEN]
            print(os.listdir("./"),image_path)
            if image_path in os.listdir("./IMAGENES FUND"):
                
                
                self.load_and_display_image(f"./IMAGENES FUND/{image_path}")
                print (image_path)
            else:
                self.clear_image("No hay ruta de imagen especificada.")
            #mod
        except ValueError:
            messagebox.showerror("Error de entrada", "Ingrese un número entero válido.")
            self.clear_result_text("Entrada inválida.")
        except Exception as e:
             messagebox.showerror("Error", f"Error al procesar: {e}")
             self.clear_result_text()
             self.clear_image()
             
    def load_and_display_image(self, path):
        # ... (código sin cambios)
        MAX_WIDTH = 400
        MAX_HEIGHT = 240
        
        try:
            img = Image.open(path)
            
            img_width, img_height = img.size
            ratio = min(MAX_WIDTH/img_width, MAX_HEIGHT/img_height)
            
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.current_image = ImageTk.PhotoImage(img) 
            
            self.image_label.config(image=self.current_image, text="")
            self.image_label.image = self.current_image
            
        except FileNotFoundError:
            self.clear_image(f"ERROR: Imagen no encontrada en: {path}")
        except Exception as e:
            self.clear_image(f"ERROR al cargar la imagen: {e}")

    def update_result_text(self, text):
        # ... (código sin cambios)
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', text)
        self.result_text.config(state='disabled')
        
    def clear_result_text(self, default_text="Aquí se mostrará el contenido de la fila."):
        # ... (código sin cambios)
        self.update_result_text(default_text)
        
    def clear_image(self, message="Sin imagen"):
        # ... (código sin cambios)
        self.image_label.config(image='', text=message)
        self.current_image = None
        self.image_label.image = None


# --- Ejecución de la Aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVImageApp(root)
    root.config(bg="#88A0EF")
    root.mainloop()
    