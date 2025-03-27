import tkinter as tk
from tkinter import filedialog, messagebox
from api.image_api import ImageAPI
from utils.file_utils import ensure_processed_folder, get_processed_filename, save_processed_image
from utils.image_utils import open_image, resize_image, image_to_tk
from gui.components import create_button, create_label, create_option_menu
from gui.history_window import HistoryWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Imagens")
        self.api = ImageAPI()
        self.selected_file = None
        self.filter_var = tk.StringVar(value="pixelate")
        
        self.create_widgets()
        ensure_processed_folder()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles superiores
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        create_button(control_frame, "Selecionar Imagem", self.select_image).pack(side=tk.LEFT, padx=5)
        
        filter_options = ["pixelate", "grayscale", "blur", "invert"]
        create_option_menu(control_frame, self.filter_var, filter_options).pack(side=tk.LEFT, padx=5)
        
        create_button(control_frame, "Processar", self.process_image).pack(side=tk.LEFT, padx=5)
        create_button(control_frame, "Histórico", self.show_history).pack(side=tk.LEFT, padx=5)
        
        # Visualização de imagens
        image_frame = tk.Frame(main_frame)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original
        create_label(image_frame, text="Original", relief=tk.RIDGE).grid(row=0, column=0, sticky="nsew")
        self.original_panel = create_label(image_frame)
        self.original_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Processada
        create_label(image_frame, text="Processada", relief=tk.RIDGE).grid(row=0, column=1, sticky="nsew")
        self.processed_panel = create_label(image_frame)
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
            img = resize_image(open_image(image_path))
            photo = image_to_tk(img)
            panel.config(image=photo)
            panel.image = photo  # Mantém uma referência
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}")

    def process_image(self):
        if not self.selected_file:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro")
            return

        try:
            result = self.api.upload_image(self.selected_file, self.filter_var.get())
            
            # Baixa a imagem processada
            processed_bytes = self.api.get_image(result['processed'].lstrip('/image/'))
            
            # Salva a imagem processada
            processed_filename = get_processed_filename(self.selected_file, result['filter'])
            processed_path = save_processed_image(processed_bytes, processed_filename)
            
            # Exibe a imagem processada
            self.display_image(processed_path, self.processed_panel)
            
            messagebox.showinfo("Sucesso", f"Imagem processada salva em: {processed_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar imagem: {e}")

    def show_history(self):
        HistoryWindow(self.root)