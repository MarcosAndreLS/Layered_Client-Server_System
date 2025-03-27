import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from api.image_api import ImageAPI
from utils.image_utils import bytes_to_image, image_to_tk, resize_image

class HistoryWindow:
    def __init__(self, parent):
        self.parent = parent
        self.api = ImageAPI()
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Histórico de Processamento")
        
        # Treeview para mostrar os itens
        self.tree = ttk.Treeview(self.window, columns=('ID', 'Nome', 'Filtro', 'Data'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome do Arquivo')
        self.tree.heading('Filtro', text='Filtro Aplicado')
        self.tree.heading('Data', text='Data/Hora')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.load_history()
        
        tk.Button(self.window, text="Visualizar Selecionado", command=self.view_selected).pack(pady=5)

    def load_history(self):
        try:
            history = self.api.get_history()
            for item in history:
                self.tree.insert('', tk.END, values=(
                    item['id'],
                    item['filename'],
                    item['filter'],
                    item['created_at']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar histórico: {e}")

    def view_selected(self):
        selected = self.tree.focus()
        if not selected:
            return
        
        item = self.tree.item(selected)
        item_id = item['values'][0]
        
        try:
            history = self.api.get_history()
            selected_item = next((x for x in history if x['id'] == item_id), None)
            
            if not selected_item:
                messagebox.showerror("Erro", "Não foi possível encontrar os detalhes da imagem")
                return
            
            self.show_image_details(selected_item)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao visualizar imagem: {e}")

    def show_image_details(self, item):
        detail_window = tk.Toplevel(self.window)
        detail_window.title(f"Visualizar - {item['filename']}")
        
        # Baixa e exibe a imagem original
        original_bytes = self.api.get_image(item['original_path'])
        original_img = resize_image(bytes_to_image(original_bytes))
        original_photo = image_to_tk(original_img)
        
        tk.Label(detail_window, text="Original").pack()
        original_panel = tk.Label(detail_window, image=original_photo)
        original_panel.image = original_photo
        original_panel.pack()
        
        # Baixa e exibe a imagem processada
        processed_bytes = self.api.get_image(item['processed_path'])
        processed_img = resize_image(bytes_to_image(processed_bytes))
        processed_photo = image_to_tk(processed_img)
        
        tk.Label(detail_window, text="Processada").pack()
        processed_panel = tk.Label(detail_window, image=processed_photo)
        processed_panel.image = processed_photo
        processed_panel.pack()