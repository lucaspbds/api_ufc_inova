# 🚀 API - Tecnologias da UFC Inova

**Autor:** David Lucas Pereira Braga dos Santos  
**Linguagem:** Python   
**Framework:** FastAPI   

---

## 🧠 Sobre o projeto

Este projeto realiza **Web Scraping** no portal **UFC Inova**, coletando e organizando informações sobre as **tecnologias desenvolvidas pela Universidade Federal do Ceará (UFC)**.  
Os dados extraídos são estruturados em um arquivo **JSON**, que serve de base para uma **API** criada com **FastAPI**.

A API permite o acesso simples e rápido a informações como:
- ID da tecnologia: Identificador único da tecnologia; 
- Título: Nome da tecnologia;
- Slug: Identificador amigável para URLs;
- Descrição: Trechos descritivos sobre a invenção;
- Datas de publicação e atualização;   
- TRL: Nível de maturidade tecnológica;
- Inventores e departamentos: Nomes dos inventores(as) e Departamento ou laboratório responsável;
- Categoria e status da tecnologia: Nome da categoria (ex: ALIMENTOS) e situação da tecnologia (ex: "Vigente");  
- Links e contatos:  Link para a página da tecnologia e Telefones e e-mails de contato;
- Benefícios: Lista dos benefícios da tecnologia.
---


## 📊 Estrutura do projeto

📦 **webscraping-ufcinova**

 ┣ 📜 *dados_ufcinova.json* # Arquivo com os dados extraídos

 ┣ 📜 *main.py* # API principal (FastAPI)

 ┣ 📜 *modelos.py* # Classe Tecnologia que contém as informações que compõem a tecnologia

 ┣ 📜 *requirements.txt* # Dependências do projeto
 
 ┣ 📜 *web_scraping.py* # Script de coleta de dados (Web Scraping)
 
 ┗ 📜 *README.md* # Documentação

---

## ⚙️ Como executar localmente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/lucaspbds/api_ufc_inova.git
cd api_ufc_inova
```

### 2️⃣ Criar ambiente virtual 

#### Windows
```bash
python -m venv venv
venv\Scripts\activate     
```
#### Linux/Mac
```bash
source venv/bin/activate
```

### 3️⃣ Instalar dependências 
```bash
pip install -r requirements.txt
```

### 4️⃣ Rodar o servidor local
```bash
uvicorn main:app --reload
```

Acesse a documentação interativa da API: 👉 http://127.0.0.1:8000/docs


---

🌐 API Pública (deploy no Render)

Você também pode acessar a versão online da API:
🔗 https://api-ufc-inova.onrender.com


---

🔍 Endpoints principais

Método	Endpoint	Descrição

GET	/	Página inicial da API
GET	/tecnologias	Lista todas as tecnologias
GET	/categorias	Retorna todas as categorias disponíveis
GET	/tecnologias/{categoria}	Lista tecnologias por categoria
GET	/tecnologias/total	Retorna o número total de tecnologias cadastradas

---

🛠️ Tecnologias utilizadas

Python 3.13

FastAPI – criação da API

Requests – requisições HTTP

BeautifulSoup (bs4) – extração de dados HTML

Uvicorn – servidor ASGI



---

💬 Autor

Desenvolvido por David Lucas Pereira Braga dos Santos 💡

📍 Universidade Federal do Ceará — Ciência de Dados

📧 Contato: https://www.linkedin.com/in/david-lucas-pereira/


---

⭐ Se este projeto te ajudou, não esqueça de deixar uma estrela no repositório!
