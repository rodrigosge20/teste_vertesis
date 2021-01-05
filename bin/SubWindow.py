"""No Subwindow.py é definida a classe 'subWindow' .
A classe principal 'subWindow' é responsável pela configuração da janela secundária presente no teste e cada aba
presente nessa sub-janela.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime


from uiSubwindow import Ui_Subwindow
from configLista import listaTab
from  Variables import Project, Line
from XMLFile import XMLFile

class subWindow(QtWidgets.QWidget):
    """Recebe como parâmetro de entrada a classe QtWidgets.QWidget que faz a gestão da janela secundária da interface gráfica.

        Essa classe é responsável pelas comunicação entre a janela principal, a subjanela e as diversas abas presentes. A função
        principal é carregar as informações importadas para cada aba, criando uma variável global que armazena essas informações.
        Além disso, também é responsável pelas alterações feitas pelo usuário em cada aba.
        """

    def __init__(self, parent = None, projeto = Project()):
        """Função que inicializa a janela principal e seus atributos.
        São definidas as conexões entre os diferentes sinais e operações de usuário.

        :param filepath: caminho do arquivo no diretório local.
        :param filename: nome do arquivo.
        """
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Subwindow()  # armazena as informações da interface gráfica definida no Qt para a subjanela na variável 'self.ui'
        self.ui.setupUi(self)

        self.ui.tabListas = []  # vetor que armazena as informações da interface gráfica de cada tab de listas
        self.ui.tabela_linha = []  # vetor que armazena as informações da interface gráfica de cada tabela

        """
        Inserção de cada lista na subwindow atual, configurando a tabela para inserir as colunas com informações
        A tabela é objeto da classe listaTab, situada no arquivo configLista.py. 
        """
        keys = list(projeto.dirList.keys())
        for i in range(len(projeto.dirList)):

            id = keys[i]

            self.ui.tabListas.append(QtWidgets.QWidget())
            self.ui.tabListas[i].setObjectName("tabLista"+(str(i)))

            self.ui.tabEditor.addTab(self.ui.tabListas[i],"")
            self.ui.tabEditor.setTabText(i,projeto.dirList[id].name)

            self.ui.tabela_linha.append(listaTab(self.ui.tabListas[i], self))

            self.ui.tabela_linha[i].ui.table.setColumnWidth(0, 50)
            self.ui.tabela_linha[i].ui.table.setColumnWidth(5, 50)

            self.ui.verticalLayoutLista = QtWidgets.QVBoxLayout(self.ui.tabListas[i])
            self.ui.verticalLayoutLista.setObjectName("verticalLayoutLista")


            self.ui.verticalLayoutLista.addWidget(self.ui.tabela_linha[i])

            # Verificação se existem linhas na lista atual, populando a tabela caso existam com a função atualizaLinhas
            if projeto.dirList[id].dirLines == {}:
                pass
            else:
                self.atualizaLinhas(projeto.dirList[id],i)

        self.ui.tabEditor.setCurrentIndex(0)

    def atualizaLinhas(self,lista,index_lista):
        """Função responsável por inserir as informações de cada linha da lista na tabela

        :param lista: lista atual.
        :param index_lista: posição da lista atual na aba.
        """

        numLinhas = len(lista.dirLines.keys())

        for i in range(numLinhas):
            id = "l"+str((i+1))
            linha = lista.dirLines[id]
            self.alteraTabela(linha,index_lista,i)


    def insertLinha(self):
        """Função responsável por inserir uma nova linha na tabela, colocando informações default em cada coluna"""


        nomeProjetoAtual = self.windowTitle() # armazena o nome do projeto na janela atual

        index_lista = self.ui.tabEditor.currentIndex()
        nomeListaAtual = self.ui.tabEditor.tabText(index_lista) # armazena o nome da lista na aba atual

        mainWindow = self.window()

        # Verificação para armazenar a ID e nome do projeto atual
        numProjetos = mainWindow.dirProject.keys()
        for key in sorted(numProjetos):

            id_projeto = key
            projeto = mainWindow.dirProject[id_projeto]

            # se o nome do projeto é o mesmo nome do projeto na sub janela presente na UI, sai do loop
            if projeto.name == nomeProjetoAtual:
                break

        # Verificação para armazenar a ID e nome da lista atual
        numListas = projeto.dirList.keys()
        for key in sorted(numListas):

            id_lista = key
            lista = projeto.dirList[id_lista]

            # se o nome da lista é o mesmo nome da lista na aba presente na UI, sai do loop
            if lista.name == nomeListaAtual:
                break

        # Criação do objeto linha da classe Line
        linha = Line()

        # armazena a quantidade de linhas na tabela
        rowPosition = self.ui.tabela_linha[index_lista].ui.table.rowCount()

        # Atribuição de valores default para os atributos do objeto linha
        linha.id = "l"+str(rowPosition+1)

        linha.name = "Linha1"
        linha.tag = "TAG"
        linha.type = "Causa"
        linha.signal = "Digital"
        linha.pid = "PID"
        linha.version = 1
        linha.list_id = "L1"
        now = datetime.now()
        linha.created_at = str(now.strftime("%d/%m/%Y %H:%M:%S"))

        # Insere a linha recém criada no dicionário de linhas do objeto lista
        lista.dirLines[linha.id] = linha

        # Adiciona a nova linha na tabela da UI
        self.alteraTabela(linha,index_lista,rowPosition)

    def alteraTabela(self,linha,index_lista,rowPosition):
        """Função responsável por inserir as linhas na tabela da UI

        :param linha: linha atual a ser inserida.
        :param index_lista: posição da lista atual na aba.
        :param rowPosition: row atual na tabela.
        """

        # É necessário bloquear qualquer sinal emitido por alterações na interface para garantir que sinais externos
        # influenciem na geração das linhas
        self.ui.tabela_linha[index_lista].ui.table.blockSignals(True)

        # Cria nova linha
        self.ui.tabela_linha[index_lista].ui.table.insertRow(rowPosition)

        """
        Abaixo são criados os itens a serem inseridos em cada coluna da tabela, inserindo as informações corretas
        de acordo com a linha atual de acordo com os atributos do objeto,
        """
        self.ui.tabela_linha[index_lista].ui.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(''))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 0).setText(str(rowPosition+1))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.ui.tabela_linha[index_lista].ui.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(''))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 1).setText(linha.tag)

        self.ui.tabela_linha[index_lista].ui.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(''))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 2).setText(linha.type)

        self.ui.tabela_linha[index_lista].ui.table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(''))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 3).setText(linha.signal)

        self.ui.tabela_linha[index_lista].ui.table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(''))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 4).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 4).setText(linha.pid)

        self.ui.tabela_linha[index_lista].ui.table.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(''))
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 5).setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.tabela_linha[index_lista].ui.table.item(rowPosition, 5).setText(str(linha.version))

        # Desbloqueio da emissão de sinais da tabela
        self.ui.tabela_linha[index_lista].ui.table.blockSignals(False)





