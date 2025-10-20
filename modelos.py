from dataclasses import dataclass, field, asdict

#Molde das informações da tecnologia
@dataclass
class Tecnologia:
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