from PyQt5 import QtCore

from VarTable import VarTable

class listaTab(VarTable):
    """Classe listaTab contem todas as funções e atributos necessários para configuração das tabelas

    """
    def __init__(self, parent=None, window=None):
        """Inicia listaTab

        :param parent: indica a classe que herdou listaTab
        :param window: indica a ui da classe que herdou
        """
        super(listaTab, self).__init__("m", parent, window)

        # Função responsável pela configuração inicial da tabela
        self.configTable()

        # Se o botão Adicionar for clicado, chama a função para inserir linha
        self.ui.addButton.released.connect(self.window.insertLinha)

    def configTable(self):
        """
        Função responsável por configurar a tabela, ajustando os headers de cada coluna e os comprimentos.
        """
        topHeader = "Num;TAG;Tipo;Sinal;PID;Versão"
        self.ui.table.setColumnCount(len(topHeader.split(";")))
        self.ui.table.setHorizontalHeaderLabels(topHeader.split(";"))

        self.ui.table.setColumnWidth(0, 130)
        self.ui.table.setColumnWidth(2, 60)
        self.ui.table.setColumnWidth(3, 60)

        self.ui.table.verticalHeader().hide()

        # Se alguma célula for modificada, chama a função responsável por alterar internamente os dados
        self.ui.table.cellChanged.connect(self.alteracaoTabela)

    def alteracaoTabela(self,row,col):
        """
        Função responsável por modificar internamente os dados quando o usuário altera algum campo da tabela.
        Além disso, é responsável por verificar se modificação é válida, caso contrário retorna uma janela de erro

        :param row: linha da célula alterada
        :param col: coluna da célula alterada
        """

        # armaneza o texto da célula modificada
        item_atual = self.ui.table.item(row,col).text()

        # armaneza o nome do projeto onde a tabela modificada
        nomeProjetoAtual = self.window.windowTitle()

        # armazena o nome da lista onde a tabela modificada
        index_lista = self.window.ui.tabEditor.currentIndex()
        nomeListaAtual = self.window.ui.tabEditor.tabText(index_lista)

        # variável que contem os atributos da janela principal
        mainWindow = self.window.window()

        # busca pela id a partir das chaves no dicionário de projetos
        numProjetos = mainWindow.dirProject.keys()
        for key in sorted(numProjetos):

            id_projeto = key
            projeto = mainWindow.dirProject[id_projeto]

            if projeto.name == nomeProjetoAtual:
                break

        # busca pela id a partir das chaves no dicionário de listas
        numListas = projeto.dirList.keys()
        for key in sorted(numListas):

            id_lista = key
            lista = projeto.dirList[id_lista]

            if lista.name == nomeListaAtual:
                break

        linha = lista.dirLines["l" + str(row + 1)]

        # Verifica-se qual coluna foi alterada, para fazer as verificações apropriadas
        if col == 1:
            linha.TAG = item_atual

        # se for coluna de Type, permite-se apenas inserir Causa ou Efeito na célula
        elif col == 2:
            if item_atual == "Causa" or item_atual == "Efeito":
                linha.type = item_atual
            else:
                self.ui.table.item(row, col).setText(linha.type)

        # se for coluna de Signal, permite-se apenas inserir Analógico ou Digital na célula
        elif col == 3:
            if item_atual == "Analógico" or item_atual == "Digital":
                linha.signal = item_atual
            else:
                self.ui.table.item(row, col).setText(linha.signal)

        elif col == 4:
            linha.PID = item_atual

        elif col == 5:
            linha.version = int(item_atual)



