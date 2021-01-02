from PyQt5 import QtCore, QtGui, QtWidgets

from VarTable import VarTable



class listaTab(VarTable):
    def __init__(self, parent=None, window=None):
        super(listaTab, self).__init__("m", parent, window)

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.configTable()

        self.ui.addButton.released.connect(self.window.insertLinha)

    def configTable(self):
        topHeader = "Num;TAG;Tipo;Sinal;PID;Versão"
        self.ui.table.setColumnCount(len(topHeader.split(";")))
        self.ui.table.setHorizontalHeaderLabels(topHeader.split(";"))

        self.ui.table.setColumnWidth(0, 130)
        self.ui.table.setColumnWidth(2, 60)
        self.ui.table.setColumnWidth(3, 60)

        self.ui.table.verticalHeader().hide()

        self.ui.table.cellChanged.connect(self.alteracaoTabela)

    def alteracaoTabela(self,row,col):

        item_atual = self.ui.table.item(row,col).text()

        nomeProjetoAtual = self.window.windowTitle()

        index_lista = self.window.ui.tabEditor.currentIndex()
        nomeListaAtual = self.window.ui.tabEditor.tabText(index_lista)

        mainWindow = self.window.window()

        numProjetos = mainWindow.dirProject.keys()
        for i in range(len(numProjetos)):

            id_projeto = "P" + str(i + 1)
            projeto = mainWindow.dirProject[id_projeto]

            if projeto.nome == nomeProjetoAtual:
                break

        numListas = projeto.dirList.keys()
        for i in range(len(numListas)):

            id_lista = "L" + str(i + 1)
            lista = projeto.dirList[id_lista]

            if lista.nome == nomeListaAtual:
                break

        linha = lista.dirLines["l" + str(row + 1)]



        if col == 1:
            linha.TAG = item_atual

        elif col == 2:
            if item_atual == "Causa" or item_atual == "Efeito":
                linha.type = item_atual
            else:
                self.ui.table.item(row, col).setText(linha.type)

        elif col == 3:
            if item_atual == "Analógico" or item_atual == "Digital":
                linha.signal = item_atual
            else:
                self.ui.table.item(row, col).setText(linha.signal)

        elif col == 4:
            linha.PID = item_atual

        elif col == 5:
            linha.version = int(item_atual)



