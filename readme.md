# Layred Client Server System

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