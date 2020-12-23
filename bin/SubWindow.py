from PyQt5 import QtCore, QtGui, QtWidgets

from uiSubwindow import Ui_Subwindow
import configLista
import Variables

class subWindow(QtWidgets.QWidget):

    def __init__(self, parent = None, projeto = Variables.Project()):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Subwindow()  # armazena as informações da interface gráfica definida no Qt para a subjanela na variável 'self.ui'
        self.ui.setupUi(self)

        print(projeto.dirList)

        self.ui.tabListas = []
        self.tabListas = []


        for i in range(len(projeto.dirList)):
            id = "L"+str(i+1)

            self.ui.tabListas.append(QtWidgets.QWidget())
            self.ui.tabListas[i].setObjectName("tabLista"+(str(i)))

            self.ui.tabEditor.addTab(self.ui.tabListas[i],"")
            self.ui.tabEditor.setTabText(i,projeto.dirList[id].nome)

            self.tabListas.append(configLista.listaTab(self.ui.tabListas[i], self))

            self.ui.verticalLayoutLista = QtWidgets.QVBoxLayout(self.ui.tabListas[i])
            self.ui.verticalLayoutLista.setObjectName("verticalLayoutLista")


            self.ui.verticalLayoutLista.addWidget(self.tabListas[i])

        self.ui.tabEditor.setCurrentIndex(0)


    def insertMan(self):
        print("ok")