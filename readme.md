# Layred Client Server System

⚙️ Funcionamento

1. O cliente envia uma imagem via HTTP para o servidor.

2. O servidor aplica um filtro (ex: pixelização, troca de cores) e retorna a imagem modificada.

3. As imagens (original e processada) são salvas em disco.

4. Os metadados (nome do arquivo, filtro aplicado, data/hora) são armazenados em um banco de dados SQLite.

5. O cliente pode visualizar a imagem original e a imagem alterada.

🎥 Demonstração

O sistema permitirá visualizar as seguintes etapas:

✅ Envio da imagem pelo cliente.

✅ Recebimento e processamento da imagem no servidor.

✅ Exibição da imagem original e da imagem com filtro.

✅ Armazenamento das imagens no servidor.

✅ Registro de metadados no banco de dados SQLite.

🛠️ Tecnologias Utilizadas

* Python 🐍

* Flask (para comunicação HTTP) 🌐

* Tkinter (interface gráfica do cliente) 🖥️

* Pillow (processamento e filtros de imagem) 🎨

* SQLite (banco de dados para armazenamento de metadados) 🗄️

* Dois computadores (Cliente e Servidor) 💻💻

## Clonando e acessando o repositório
```bash
git clone https://github.com/MarcosAndreLS/Layered_Client-Server_System.git
cd Layered_Client-Server_System
```

## Instalando as dependências
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```bash
Layered_Client-Server_System/
    |--- client/
    |       |--- main.py
    |--- database/
    |       |--- imagens.db
    |--- images/
    |       |--- processed/
    |       |--- uploads/
    |--- server/
    |       |--- app.py
    |--- README.md
    |--- requirements.txt
```

## Executando o projeto
#### Rodando o server
```bash
cd server
python app.py
```

#### Rodando o cliente
```bash
cd client
python main.py
```

## Capturas de Tela do Projeto

1. Tela inicial do Cliente
   
   Na tela inicial é possível escolher a imagem, ao qual o usuário é direcionado ao seu próprio gerenciador de arquivos. É possível escolher qual o filtro de imagem, sendo eles: "pixelated", "grayscaling", "blur" e "inverted". Além disso, tem os botões de processamento da imagem e o botão de histórico o qual é mostrado outra interface com todas as imagens com seus respectivos nomes, filtros utilizados e a data/horário.
   
    <p align="center">
        <img src="https://github.com/user-attachments/assets/38cc4af0-2ce1-485b-ad6b-320b9f4a30a5"/>
    </p>
    
2. Tela do Histórico
   
   Na tela do histórico é possível selecionar uma imagem ao qual já foi processada, sendo possível visualizar a original e a processada.
   
   <p align="center">
       <img src="https://github.com/user-attachments/assets/ee705698-144d-4103-895f-dfb2502eecc8"/>
   </p>

3. Tela inicial com imagem original e processada lado a lado

   <p align="center">
        <img src="https://github.com/user-attachments/assets/ee307b09-cbb8-49e2-b761-03c58c621f2c"/>
   </p>
