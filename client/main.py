"""Arquivos main.py do client"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from PIL import Image, ImageTk
# import io
# import os

class ImageProcessorClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Imagens")
        
        # Variáveis
        self.server_url = "http://localhost:5000"
        self.selected_file = None
        self.original_image = None
        self.processed_image = None
        
        # Interface
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles superiores
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(control_frame, text="Selecionar Imagem", command=self.select_image).pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="pixelate")
        filter_options = ["pixelate", "grayscale", "blur", "invert"]
        filter_menu = tk.OptionMenu(control_frame, self.filter_var, *filter_options)
        filter_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Processar", command=self.process_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Histórico", command=self.show_history).pack(side=tk.LEFT, padx=5)
        
        # Visualização de imagens
        image_frame = tk.Frame(main_frame)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original
        original_label = tk.Label(image_frame, text="Original", relief=tk.RIDGE)
        original_label.grid(row=0, column=0, sticky="nsew")
        
        self.original_panel = tk.Label(image_frame)
        self.original_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Processada
        processed_label = tk.Label(image_frame, text="Processada", relief=tk.RIDGE)
        processed_label.grid(row=0, column=1, sticky="nsew")
        
        self.processed_panel = tk.Label(image_frame)
        self.processed_panel.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configurar pesos das colunas
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(1, weight=1)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.display_image(file_path, self.original_panel)
    
    def display_image(self, image_path, panel):
        try:
            img = Image.open(image_path)
            img.thumbnail((400, 400))  # Redimensiona para caber na interface
            
            photo = ImageTk.PhotoImage(img)
            panel.config(image=photo)
            panel.image = photo  # Mantém uma referência
            
            if panel == self.original_panel:
                self.original_image = img
            else:
                self.processed_image = img
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}")
    
    def process_image(self):
        if not self.selected_file:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro")
            return
        
        try:
            files = {'file': open(self.selected_file, 'rb')}
            data = {'filter': self.filter_var.get()}
            
            response = requests.post(f"{self.server_url}/upload", files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            self.display_image(result['processed'], self.processed_panel)
            
            messagebox.showinfo("Sucesso", f"Imagem processada com filtro: {result['filter']}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar imagem: {e}")
    
    def show_history(self):
        try:
            response = requests.get(f"{self.server_url}/images")
            response.raise_for_status()
            
            history = response.json()
            
            # Criar nova janela para o histórico
            history_window = tk.Toplevel(self.root)
            history_window.title("Histórico de Processamento")
            
            # Treeview para mostrar os itens
            tree = ttk.Treeview(history_window, columns=('ID', 'Nome', 'Filtro', 'Data'), show='headings')
            tree.heading('ID', text='ID')
            tree.heading('Nome', text='Nome do Arquivo')
            tree.heading('Filtro', text='Filtro Aplicado')
            tree.heading('Data', text='Data/Hora')
            
            for item in history:
                tree.insert('', tk.END, values=(
                    item['id'],
                    item['filename'],
                    item['filter'],
                    item['created_at']
                ))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Botão para visualizar
            def view_selected():
                selected = tree.focus()
                if not selected:
                    return
                
                item = tree.item(selected)
                original_path = next(x for x in history if x['id'] == item['values'][0])['original_path']
                processed_path = next(x for x in history if x['id'] == item['values'][0])['processed_path']
                
                view_window = tk.Toplevel(history_window)
                view_window.title(f"Visualizar - {item['values'][1]}")
                
                def resize_image(image_path, max_size=(350, 350)):  # Define um tamanho máximo
                    img = Image.open(image_path)
                    img.thumbnail(max_size)  # Mantém proporção e reduz para caber no tamanho máximo
                    return ImageTk.PhotoImage(img)

                # Mostrar original
                original_label = tk.Label(view_window, text="Original")
                original_label.pack()
                original_img = resize_image(original_path)
                original_panel = tk.Label(view_window, image=original_img)
                original_panel.image = original_img
                original_panel.pack()

                # Mostrar processada
                processed_label = tk.Label(view_window, text="Processada")
                processed_label.pack()
                processed_img = resize_image(processed_path)
                processed_panel = tk.Label(view_window, image=processed_img)
                processed_panel.image = processed_img
                processed_panel.pack()
            
            tk.Button(history_window, text="Visualizar Selecionado", command=view_selected).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar histórico: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorClient(root)
    root.mainloop()