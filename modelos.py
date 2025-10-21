from dataclasses import dataclass, field, asdict

#Molde das informações da tecnologia
@dataclass
class Tecnologia:
    """
    Representa uma tecnologia cadastrada na Vitrine Tecnológica da UFC Inova.

    Attributes:
        id (int): Identificador único da tecnologia.
        titulo (str): Nome da tecnologia.
        slug (str): Identificador amigável para URLs.
        data_publicacao (str): Data da publicação.
        data_ultima_modificacao (str): Última data de modificação.
        link_post_tecnologia (str): Link para a página da tecnologia.
        status (str): Situação da tecnologia (ex: "Vigente").
        trl (str): Nível de maturidade tecnológica.
        beneficios (list): Lista dos benefícios da tecnologia.
        descricao (list): Trechos descritivos sobre a invenção.
        pessoas_inventoras (list): Nomes dos inventores(as).
        departamento (str): Departamento ou laboratório responsável.
        contatos (list): Telefones e e-mails de contato.
    """
    id: int
    titulo: str
    slug: str
    data_publicacao: str
    data_ultima_modificacao: str
    link_post_tecnologia: str
    status: str = None
    trl: str = None
    beneficios: list = field(default_factory=list)
    descricao: list = field(default_factory=list)
    pessoas_inventoras: list = field(default_factory=list)
    departamento: str = None
    contatos: list = field(default_factory=list)

    def transformar_em_dicionario(self):
        return asdict(self)