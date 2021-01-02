from PyQt5 import QtCore, QtGui, QtWidgets
from time import time


from uiSubwindow import Ui_Subwindow
import configLista
import Variables

class subWindow(QtWidgets.QWidget):

    def __init__(self, parent = None, projeto = Variables.Project()):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Subwindow()  # armazena as informações da interface gráfica definida no Qt para a subjanela na variável 'self.ui'
        self.ui.setupUi(self)

        self.ui.tabListas = []
        self.tabListas = []


        for i in range(len(projeto.dirList)):
            id = "L"+str(i+1)

            self.ui.tabListas.append(QtWidgets.QWidget())
            self.ui.tabListas[i].setObjectName("tabLista"+(str(i)))

            self.ui.tabEditor.addTab(self.ui.tabListas[i],"")
            self.ui.tabEditor.setTabText(i,projeto.dirList[id].nome)

            self.tabListas.append(configLista.listaTab(self.ui.tabListas[i], self))

            self.tabListas[i].ui.table.setColumnWidth(0, 50)
            self.tabListas[i].ui.table.setColumnWidth(5, 50)

            self.ui.verticalLayoutLista = QtWidgets.QVBoxLayout(self.ui.tabListas[i])
            self.ui.verticalLayoutLista.setObjectName("verticalLayoutLista")


            self.ui.verticalLayoutLista.addWidget(self.tabListas[i])

            if projeto.dirList[id].dirLines == {}:
                pass
            else:
                self.atualizaLinhas(projeto.dirList[id],i)

        self.ui.tabEditor.setCurrentIndex(0)

    def atualizaLinhas(self,lista,index_lista):

        numLinhas = len(lista.dirLines.keys())

        for i in range(numLinhas):
            id = "l"+str((i+1))
            linha = lista.dirLines[id]
            self.alteraTabela(linha,index_lista,i)


    def insertLinha(self):


        nomeProjetoAtual = self.windowTitle()

        index_lista = self.ui.tabEditor.currentIndex()
        nomeListaAtual = self.ui.tabEditor.tabText(index_lista)

        mainWindow = self.window()

        numProjetos = mainWindow.dirProject.keys()
        for i in range(len(numProjetos)):

            id_projeto = "P"+str(i+1)
            projeto = mainWindow.dirProject[id_projeto]

            if projeto.nome == nomeProjetoAtual:
                break

        # print(projeto.nome)

        numListas = projeto.dirList.keys()
        for i in range(len(numListas)):

            id_lista = "L"+str(i+1)
            lista = projeto.dirList[id_lista]

            if lista.nome == nomeListaAtual:
                break

        # print(lista.nome)
        # print(lista.dirLines)

        linha = Variables.Line()

        rowPosition = self.tabListas[index_lista].ui.table.rowCount()

        linha.id = "l"+str(rowPosition+1)

        linha.name = "Linha1"
        linha.tag = "TAG"
        linha.type = "Causa"
        linha.signal = "Digital"
        linha.pid = "PID"
        linha.version = 1
        linha.list_id = "L1"
        linha.created_at = str(time())

        lista.dirLines[linha.id] = linha

        self.alteraTabela(linha,index_lista,rowPosition)



    def alteraTabela(self,linha,index_lista,rowPosition):

        self.tabListas[index_lista].ui.table.blockSignals(True)

        self.tabListas[index_lista].ui.table.insertRow(rowPosition)

        self.tabListas[index_lista].ui.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(''))
        self.tabListas[index_lista].ui.table.item(rowPosition, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabListas[index_lista].ui.table.item(rowPosition, 0).setText(str(rowPosition+1))
        self.tabListas[index_lista].ui.table.item(rowPosition, 0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.tabListas[index_lista].ui.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(''))
        self.tabListas[index_lista].ui.table.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabListas[index_lista].ui.table.item(rowPosition, 1).setText(linha.tag)

        self.tabListas[index_lista].ui.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(''))
        self.tabListas[index_lista].ui.table.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabListas[index_lista].ui.table.item(rowPosition, 2).setText(linha.type)

        self.tabListas[index_lista].ui.table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(''))
        self.tabListas[index_lista].ui.table.item(rowPosition, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabListas[index_lista].ui.table.item(rowPosition, 3).setText(linha.signal)

        self.tabListas[index_lista].ui.table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(''))
        self.tabListas[index_lista].ui.table.item(rowPosition, 4).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabListas[index_lista].ui.table.item(rowPosition, 4).setText(linha.pid)

        self.tabListas[index_lista].ui.table.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(''))
        self.tabListas[index_lista].ui.table.item(rowPosition, 5).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabListas[index_lista].ui.table.item(rowPosition, 5).setText(str(linha.version))

        self.tabListas[index_lista].ui.table.blockSignals(False)




