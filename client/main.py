"""Arquivos main.py do client"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from PIL import Image, ImageTk
import os
import io

class ImageProcessorClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Imagens")
        
        # Variáveis
        self.server_url = "http://127.0.0.1:5000"
        self.api_key = "SECRET_KEY_123"
        self.selected_file = None
        self.original_image = None
        self.processed_image = None
        
        if not self.check_connection():
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor. Verifique o endereço e a rede.")
            root.destroy()
            return
        
        # Interface
        self.create_widgets()
    
    def check_connection(self):
        try:
            response = requests.get(f"{self.server_url}/images", 
                                   headers={'Authorization': f'Bearer {self.api_key}'},
                                   timeout=5)
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False
    
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
            messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}") # erro aqui
    
    def process_image(self):
        if not self.selected_file:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro")
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                data = {'filter': self.filter_var.get()}
                
                headers = {'Authorization': f'Bearer {self.api_key}'}

                response = requests.post(
                    f"{self.server_url}/upload", files=files,
                    data=data,
                    headers=headers,
                    timeout=10
                )

                if response.status_code == 401:
                    messagebox.showerror("Erro", "Acesso não autorizado. Verifique a chave de API.")
                    return
                
                response.raise_for_status()
                
                result = response.json()

                self.display_image(result['processed'], self.processed_panel)

                processed_url = f"{self.server_url}{result['processed']}"
                processed_response = requests.get(processed_url, headers=headers)
                processed_response.raise_for_status()
                
                # Salva temporariamente para exibição
                temp_path = "temp_processed.jpg"
                with open(temp_path, 'wb') as f:
                    f.write(processed_response.content)
                
                self.display_image(temp_path, self.processed_panel)
                os.remove(temp_path)  # Remove após exibir
                
                messagebox.showinfo("Sucesso", f"Imagem processada com filtro: {result['filter']}")
        # except requests.exceptions.RequestException as e:
        #     messagebox.showerror("Erro", f"Falha na comunicação com o servidor: {e}") # erro aqui
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar imagem: {e}")
    
    def show_history(self):
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(f"{self.server_url}/images", headers=headers, timeout=5)
            
            if response.status_code == 401:
                messagebox.showerror("Erro", "Acesso não autorizado. Verifique a chave de API.")
                return
            
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
                item_id = item['values'][0]
                
                # Busca detalhes completos do item
                detail_response = requests.get(
                    f"{self.server_url}/images",
                    headers=headers
                )
                detail_response.raise_for_status()
                
                full_history = detail_response.json()
                selected_item = next((x for x in full_history if x['id'] == item_id), None)
                
                if not selected_item:
                    messagebox.showerror("Erro", "Não foi possível encontrar os detalhes da imagem")
                    return
                
                view_window = tk.Toplevel(history_window)
                view_window.title(f"Visualizar - {item['values'][1]}")
                
                # Mostrar original
                original_label = tk.Label(view_window, text="Original")
                original_label.pack()
                original_img = ImageTk.PhotoImage(Image.open(original_img))
                original_panel = tk.Label(view_window, image=original_img)
                original_panel.image = original_img
                original_panel.pack()
                
                # Mostrar processada
                processed_label = tk.Label(view_window, text="Processada")
                processed_label.pack()
                processed_img = ImageTk.PhotoImage(Image.open(processed_img))
                processed_panel = tk.Label(view_window, image=processed_img)
                processed_panel.image = processed_img
                processed_panel.pack()
            
            tk.Button(history_window, text="Visualizar Selecionado", command=view_selected).pack(pady=5)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao carregar histórico: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = ImageProcessorClient(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"O aplicativo encontrou um erro: {e}")