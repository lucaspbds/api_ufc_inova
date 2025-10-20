from fastapi import FastAPI, HTTPException
from datetime import datetime
import json
from  collections import defaultdict
from web_scraping import WebScrapingUFC
"""
Projeto: Web Scraping - Tecnologias da UFC Inova
Autor: David Lucas Pereira Braga dos Santos

Descrição:
    Este projeto realiza Web Scraping no portal UFC Inova, coletando dados sobre
    tecnologias desenvolvidas pela Universidade Federal do Ceará (UFC).
    As informações extraídas incluem:
    - ID da Tecnologia
    - Título
    - Slug
    - Data da publicação
    - Data da última modificação
    - Link do pôster da tecnologia
    - Descrição
    - Benefícios
    - Status
    - TRL
    - Inventores
    - Departamento
    - Contatos

Resultado:
    Os dados são estruturados e exportados em formato JSON.
"""

def abrir_arquivo_json(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        print("Dados salvos na memória")
        return dados
    except FileNotFoundError:
        print("Arquivo JSON não encontrado. Iniciando o Web Scraping...")
        #API da UFC INOVA
        url_base = "https://ufcinova.ufc.br/wp-json/wp/v2/posts"

        categorias_id ={
            "ALIMENTOS": 36,
            "COSMÉTICOS": 34,
            "QUÍMICO": 32,
            "TIC": 44,
            "CIÊNCIAS DA SAÚDE": 38,
            "ENERGIA E MEIO AMBIENTE": 46,
            "BIOTECNOLOGIA": 40,
            "ENGENHARIAS": 48,
            "AGROPECUÁRIA": 42,
            "INDÚSTRIA": 50,
            "SOFTWARE": 115
        }

        cabecalho = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0"}

        raspagem_dados = WebScrapingUFC(
                            url_base,
                            categorias_id,
                            cabecalho,
                            nome_arquivo
                    )
        raspagem_dados.coletar_dados_por_categoria()
        raspagem_dados.processar_dados_html()
        raspagem_dados.salvar_dados_json()
        abrir_arquivo_json(nome_arquivo)
        
 
app = FastAPI(
        title="API - Tecnologias UFC Inova",
        description="API pública com informações sobre tecnologias da Universidade Federal do Ceará (UFC).",
        version="1.0.0"
)

nome_arquivo = nome_arquivo = "dados_ufcinova.json"
dados = abrir_arquivo_json(nome_arquivo)

@app.get("/")
def root():
    return {"mensagem": "Bem-vindo à API da UFC Inova! Acesse /docs para explorar os endpoints."}

@app.get("/categorias")
def listar_categorias():
    lista_categorias = list(dados.keys())
    return {"categorias": lista_categorias}

@app.get("/tecnologias")
def listar_todas():
    return dados

@app.get("/tecnologias/total")
def quantidade_de_tecnologias():
    total = 0
    qtd_tecnologias = defaultdict(int)
    for key, paginas in dados.items():
        qtdItens = 0
        qtdItens += len(paginas)
        total += qtdItens
        qtd_tecnologias[key] = qtdItens
        
    qtd_tecnologias['Total'] = total
    
    return qtd_tecnologias

@app.get("/tecnologias/categoria/{categoria}")
def listar_por_categoria(categoria: str):
    categoria = categoria.upper()
    if categoria not in dados:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return dados[categoria]

@app.get("/buscar_titulo/{titulo}")
def buscar_por_titulo(titulo: str):
    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            if titulo.lower() in tec["titulo"].lower():
                resultados.append(tec)
    return resultados

@app.get("/buscar_departamento/{departamento}")
def buscar_por_departamento(departamento: str):
    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            if departamento.lower() in tec["departamento"].lower():
                resultados.append(tec)
    return resultados

@app.get("/buscar_ano_publicacao/{ano_publicacao}")
def buscar_por_ano_publicacao(ano_publicacao: int):
    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            ano = datetime.strptime(tec["data_publicacao"], "%Y-%m-%dT%H:%M:%S").year
            if ano_publicacao == ano:
                resultados.append(tec)
    return resultados

@app.get("/buscar_inventor/{nome_inventor}")
def buscar_por_ano_publicacao(nome_inventor):
    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            for pessoa in tec['pessoas_inventoras']:
                if nome_inventor.lower() == pessoa.lower():
                    resultados.append(tec)
    return resultados
