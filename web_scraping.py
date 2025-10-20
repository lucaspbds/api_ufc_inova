import requests, json
from bs4 import BeautifulSoup
from collections import defaultdict
from modelos import Tecnologia
from dataclasses import dataclass

@dataclass
class WebScrapingUFC:
    url_base: str
    categorias_id: dict
    cabecalhos: dict
    nome_arquivo: str

    def coletar_dados_por_categoria(self) -> dict:
        """
        Coleta os dados de todas as categorias disponíveis na API da UFC Inova.

        Args:
            url_base (str): URL base da API.
            categorias (dict): Dicionário com nome e ID das categorias.

        Returns:
            dict: Dicionário contendo o nome da categoria como chave e uma lista de JSONs como valor.
        """

        self.dados_brutos = defaultdict(list)
        for categoria_nome, id in self.categorias_id.items():
            pagina_json = 1
            while True:
                try:
                    parametros = {
                        'categories': id,
                        'page': pagina_json
                    }
                    resposta = requests.get(self.url_base, headers=self.cabecalhos, timeout=20, params=parametros)
                    resposta.raise_for_status()
                    respostaJson = resposta.json()
                    self.dados_brutos[categoria_nome].append(respostaJson[:])
                    print("Página carregada com sucesso!")
                    total_paginas_json = int(resposta.headers.get("X-WP-TotalPages", 1))
                    print(f"{categoria_nome} - {pagina_json}/{total_paginas_json}")
                    if pagina_json == total_paginas_json:
                        break

                    pagina_json += 1

                except requests.exceptions.RequestException as e:
                        print(f"Erro ao acessar a categoria {categoria_nome} da página {pagina_json}: {e}")

    def extrair_campos_textos(self, lista_textos) -> dict:
        """
            Extrai informações estruturadas (benefícios, status, TRL, descrição, inventores, departamento e contatos)
            a partir de uma lista de textos obtida do conteúdo HTML de uma tecnologia na Vitrine Tecnológica da UFC Inova.

            Essa função assume que os textos seguem uma ordem padronizada na página da UFC Inova,
            permitindo identificar cada campo com base em palavras-chave (como "Benefícios", "Status", "TRL" etc.) e a ordem de aparição, que é
            benefício, status, TRL, descrição, pessoas inventoras, departamento e contatos.

            Args:
                lista_textos (list):
                    Lista de strings extraídas do HTML da página de uma tecnologia.
                    Cada elemento representa uma linha ou bloco de texto visível no site.

            Returns:
                dict:
                    Dicionário contendo as informações extraídas, com as seguintes chaves:
                        - "beneficios" (list[str]): lista dos benefícios da tecnologia.
                        - "status" (str): estado atual da tecnologia (ex: "Vigente").
                        - "trl" (str): nível de maturidade tecnológica.
                        - "descricao" (list[str]): parágrafos descritivos sobre a tecnologia.
                        - "pessoas_inventoras" (list[str]): nomes das pessoas inventoras.
                        - "departamento" (str): departamento ou laboratório responsável.
                        - "contatos" (list[str]): informações de contato (telefone e e-mail).
        """

        informacoes = defaultdict(list)
        tamanho = len(lista_textos)
        i = 0
        while i < tamanho:

            #Capturando o benefício
            if lista_textos[i].lower().startswith("benefícios"):
                i += 1
                while not lista_textos[i].lower().startswith("status"):
                    informacoes['beneficios'].append(lista_textos[i].strip().replace('\n', ' '))
                    i += 1
                continue

            #Capturando o status
            elif lista_textos[i].lower().startswith("status"):
                status = lista_textos[i].split(" ")[1].replace(".", "")
                informacoes['status'] = status.strip()

            #Capturando o TRL
            elif lista_textos[i].lower().startswith("tecnológica"):
                index_trl = i+1
                trl = lista_textos[index_trl]
                informacoes['trl'] = trl.strip()

            #Capturando a descrição
            elif lista_textos[i].lower().startswith("pessoas inventoras"):
                informacoes['descricao'] = lista_textos[index_trl+1:i]
                indexPessoas = i+1

            #Capturando o telefone, departamento e as pessoas inventoras
            elif lista_textos[i].lower().startswith('fone'):
                fone = lista_textos[i].split(":")[1]
                indexDepartamento = i-2
                departamento = lista_textos[indexDepartamento]
                pessoas_inventoras = lista_textos[indexPessoas:indexDepartamento]
                informacoes['pessoas_inventoras'] = pessoas_inventoras
                informacoes['contatos'].append(fone.strip())
                informacoes['departamento'] = departamento.strip()

            #Capturando o email
            elif lista_textos[i].lower().startswith('e-mail'):
                email = lista_textos[i].split(":")[1]
                informacoes['contatos'].append(email.strip())

            i += 1

        return informacoes

    def processar_dados_html(self) -> dict:
        """
        Processa o conteúdo HTML de cada tecnologia obtida da API da UFC Inova,
        extraindo informações relevantes e estruturando-as em instâncias da classe 'Tecnologia'.

        Esta função percorre o dicionário bruto retornado pela raspagem inicial,
        acessa o campo "content" (HTML) de cada post, e utiliza a função 'extrair_campos_textos'
        para capturar os dados específicos (benefícios, TRL, inventores etc.).

        Args:
            dados_brutos (dict):
                Dicionário contendo, para cada categoria, uma lista de páginas,
                e em cada página, uma lista de JSONs representando as tecnologias.

        Returns:
            dict:
                Dicionário com as categorias como chaves e listas de objetos 'Tecnologia' (convertíveis em dicionários)
                como valores. Cada objeto contém informações estruturadas sobre uma tecnologia.
        """

        self.tecnologias_processadas = defaultdict(list)

        for categoria_nome, paginas_json in self.dados_brutos.items():
            for pagina_json in paginas_json:
                for post_tecnologia in pagina_json:

                    html = post_tecnologia['content']['rendered']
                    soup = BeautifulSoup(html, 'html.parser')
                    lista_string = [text for text in soup.stripped_strings]
                    dados_extraidos = self.extrair_campos_textos(lista_string)

                    molde_tecnologia = Tecnologia(
                        id = post_tecnologia["id"],
                        titulo = post_tecnologia["title"]["rendered"],
                        slug = post_tecnologia["slug"],
                        data_publicacao = post_tecnologia["date_gmt"],
                        data_ultima_modificacao = post_tecnologia["modified_gmt"],
                        link_post_tecnologia = post_tecnologia["link"],
                        status = dados_extraidos.get('status'),
                        trl = dados_extraidos.get("trl"),
                        beneficios = dados_extraidos.get("beneficios", []),
                        descricao = dados_extraidos.get("descricao", []),
                        pessoas_inventoras = dados_extraidos.get("pessoas_inventoras", []),
                        departamento = dados_extraidos.get("departamento"),
                        contatos = dados_extraidos.get("contatos", [])
                    )

                    self.tecnologias_processadas[categoria_nome].append(molde_tecnologia)

    def salvar_dados_json(self):
        tecnologias_processadas_dict = defaultdict(list)
        for categoria, tecnologias in self.tecnologias_processadas.items():
            for tec in tecnologias:
                tec_dict = tec.transformar_em_dicionario()
                tecnologias_processadas_dict[categoria].append(tec_dict)

        with open(self.nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(tecnologias_processadas_dict, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    #API da UFC INOVA
    url_base = "https://ufcinova.ufc.br/wp-json/wp/v2/posts"

    #Nome do arquivo para salvar os dados
    nome_arquivo = "dados_ufcinova.json"

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
    aplicacao =  WebScrapingUFC(
        url_base,
        categorias_id,
        cabecalho,
        nome_arquivo
    )

    aplicacao.coletar_dados_por_categoria()
    aplicacao.processar_dados_html()
    aplicacao.salvar_dados_json()
    
    # dados_brutos = coletar_dados_por_categoria(url_base, categorias_id)
    # tecnologias_processadas = processar_dados_html(dados_brutos)
    # salvar_dados_json(tecnologias_processadas, nome_arquivo)




