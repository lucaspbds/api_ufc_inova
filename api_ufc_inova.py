from fastapi import FastAPI, HTTPException
from datetime import datetime
import json
from  collections import defaultdict

nome_arquivo = nome_arquivo = "dados_ufcinova.json" 

def abrir_arquivo_json(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
    print("Dados salvos na memória")
    return dados

app = FastAPI(
        title="API - Tecnologias UFC Inova",
        description="API pública com informações sobre tecnologias da Universidade Federal do Ceará (UFC).",
        version="1.0.0"
)

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
