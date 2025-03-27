import tkinter as tk
from tkinter import messagebox
from gui.main_window import MainWindow
from api.image_api import ImageAPI

class ImageProcessorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.api = ImageAPI()
        
        if not self.api.check_connection():
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor. Verifique o endereço e a rede.")
            self.root.destroy()
            return
        
        try:
            self.main_window = MainWindow(self.root)
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"O aplicativo encontrou um erro: {e}")

if __name__ == "__main__":
    app = ImageProcessorApp()