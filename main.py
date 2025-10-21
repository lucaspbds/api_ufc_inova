from fastapi import FastAPI, HTTPException
from datetime import datetime
import json
from  collections import defaultdict
from web_scraping import WebScrapingUFC
import os
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

def carregar_arquivo_json(nome_arquivo):

    if os.path.exists("dados_ufcinova.json"):
        with open("dados_ufcinova.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
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
        carregar_arquivo_json(nome_arquivo)
        
 
app = FastAPI(
        title="API - Tecnologias UFC Inova",
        description="API pública com informações sobre tecnologias da Universidade Federal do Ceará (UFC).",
        version="1.0.0"
)

nome_arquivo = "dados_ufcinova.json"
dados = carregar_arquivo_json(nome_arquivo)

@app.get("/")
def home():
    """
    Endpoint raiz da API UFC Inova.

    Retorna uma mensagem de boas-vindas e o endpoint para a documentação da API.

    Returns:
        dict: Um dicionário contendo a mensagem de boas-vindas e instruções de uso.
    """
    return {"mensagem": "Bem-vindo à API da UFC Inova! Acesse /docs para explorar os endpoints."}

@app.get("/info")
def info():
    """
    Retorna informações gerais sobre a API UFC Inova.

    Returns:
        dict: Metadados sobre a API, incluindo nome, autor, versão e fonte dos dados.
    """
    return {
        "nome": "API UFC Inova",
        "autor": "David Lucas Pereira Braga dos Santos",
        "versao": "1.0.0",
        "fontes": "https://ufcinova.ufc.br/pt/vitrinetecnologica/"
    }

@app.get("/categorias")
def listar_categorias():
    lista_categorias = list(dados.keys())
    return {"categorias": lista_categorias}

@app.get("/tecnologias")
def listar_todas():
    """
    Retorna todas as tecnologias cadastradas na Vitrine Tecnológica da UFC Inova.

    Essa rota consolida os dados de todas as categorias (como Alimentos, Saúde, Software, etc.)
    em uma única lista de tecnologias disponíveis no arquivo JSON.

    Returns:
        dict: Dicionário contendo as tecnologias agrupadas por categoria.
    """

    return dados

@app.get("/tecnologias/total")
def quantidade_de_tecnologias():
    """
    Retorna a quantidade total de tecnologias cadastradas em cada categoria.

    Returns:
        dict: Um dicionário onde as chaves são os nomes das categorias
              e os valores são as quantidades de tecnologias em cada uma delas.
    """
    total = 0
    qtd_tecnologias = defaultdict(int)
    for categoria, tecnologias in dados.items():
        qtdItens = 0
        qtdItens += len(tecnologias)
        total += qtdItens
        qtd_tecnologias[categoria] = qtdItens
        
    qtd_tecnologias['Total'] = total
    
    return qtd_tecnologias

@app.get("/tecnologias/anos_publicacao")
def listar_anos_de_publicacao():
    """
    Agrupa as tecnologias por ano de publicação.

    Retorna um dicionário em que as chaves são as categorias e os valores são um dicionário
    que tem como chave os anos e os valores são a quantidade de tecnologias publicadas naquele período.

    Returns:
        dict: Quantidade de tecnologias publicadas naquele período agrupado por categoria.
    """

    resultados = []
    categoria_anos = defaultdict(list)
    for cat, tecs in dados.items():
        dict_temp = defaultdict(int)
        for tec in tecs:
            ano = datetime.strptime(tec["data_publicacao"], "%Y-%m-%dT%H:%M:%S").year
            dict_temp[ano] += 1

        categoria_anos[cat] = dict_temp

    resultados.append(categoria_anos)
    return resultados

@app.get("/tecnologias/categoria/{categoria}")
def listar_por_categoria(categoria: str):
    categoria = categoria.upper()
    if categoria not in dados:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return dados[categoria]

@app.get("/tecnologias/buscar_titulo/{titulo}")
def buscar_por_titulo(titulo: str):
    """
    Busca uma tecnologia específica pelo título.

    A pesquisa é feita de forma insensível a maiúsculas e minúsculas,
    retornando todas as tecnologias cujo título contém o termo informado.

    Args:
        titulo (str): Parte ou nome completo do título da tecnologia.

    Returns:
        list: Lista de tecnologias que correspondem ao termo buscado.
    """

    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            if titulo.lower() in tec["titulo"].lower():
                resultados.append(tec)
    return resultados

@app.get("/tecnologias/buscar_departamento/{departamento}")
def buscar_por_departamento(departamento: str):
    """
    Retorna todas as tecnologias pertencentes a um determinado departamento da UFC.

    Args:
        departamento (str): Nome completo ou parcial do departamento.

    Returns:
        list: Lista de tecnologias associadas ao departamento especificado.
    """

    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            if departamento.lower() in tec["departamento"].lower():
                resultados.append(tec)
    return resultados

@app.get("/tecnologias/buscar_ano_publicacao/{ano_publicacao}")
def buscar_por_ano_publicacao(ano_publicacao: int):
    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            ano = datetime.strptime(tec["data_publicacao"], "%Y-%m-%dT%H:%M:%S").year
            if ano_publicacao == ano:
                resultados.append(tec)
    return resultados

@app.get("/tecnologias/buscar_inventor/{nome_inventor}")
def buscar_por_inventor(nome_inventor: str):
    """
    Retorna todas as tecnologias associadas a um(a) inventor(a) específico(a).

    Args:
        nome (str): Nome completo ou parcial do inventor(a) desejado(a).

    Returns:
        list: Lista de tecnologias que possuem o inventor informado.
    """

    resultados = []
    for cat, tecs in dados.items():
        for tec in tecs:
            for pessoa in tec['pessoas_inventoras']:
                if nome_inventor.lower() == pessoa.lower():
                    resultados.append(tec)
    return resultados
