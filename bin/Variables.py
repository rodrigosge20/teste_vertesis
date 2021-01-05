

class Project():
    """Classe projeto
    """

    def __init__(self):
        """Atributos da classe"""

        self.id = str() # ID sempre começa com P seguido de um valor inteiro

        self.name = str() # nome sempre começa com Projeto seguido do mesmo valor inteiro no final da ID
        self.description = str()
        self.created_at = str()

        self.dirList = dict() # Dicionário que armaneza cada objeto Lista

class List():

    def __init__(self):
        """Atributos da classe"""


        self.id = str() # ID sempre começa com L seguido de um valor inteiro

        self.name = str() # nome sempre começa com Lista seguido do mesmo valor inteiro no final da ID
        self.project_id = str()
        self.created_at = str()

        self.dirLines = dict() # Dicionário que armaneza cada objeto Linha

class Line():

    def __init__(self):
        """Atributos da classe"""

        self.id = str() # ID sempre começa com l seguido de um valor inteiro

        self.name = str() # nome sempre começa com Linha seguido do mesmo valor inteiro no final da ID
        self.tag = str()
        self.type = str()
        self.signal = str()
        self.pid = str()
        self.version = int()
        self.list_id = str()
        self.created_at = str()
