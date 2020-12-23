import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from time import time

from uiMain import Ui_MainWindow

import Variables
from SubWindow import subWindow


class StartMain(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.treeView.setHeaderHidden(True)
        self.ui.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        treeModel = QStandardItemModel()
        self.ui.treeView.setModel(treeModel)
        self.rootNode = treeModel.invisibleRootItem()

        self.dirProject = {}

        self.ui.novoProjetoButton.clicked.connect(self.novo_projeto)
        self.ui.novaListaButton.clicked.connect(self.nova_lista)
        self.ui.treeView.doubleClicked.connect(self.open_list)



    def novo_projeto(self):



        var_teste = QtWidgets.QMessageBox.question(self, "Aviso",
                                              'Deseja criar um novo projeto?',
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if var_teste == QtWidgets.QMessageBox.Yes:

            size_tree = len(self.dirProject.keys())


            projeto = Variables.Project()

            projeto.id = "P" + str(size_tree+1)
            projeto.nome = "Projeto" + str(size_tree+1)
            projeto.description = projeto.nome + " do teste para vertesis."
            projeto.timestamp = str(time())

            lista = Variables.List()

            lista.id = "L1"
            lista.nome = "Lista1"
            lista.project_id = projeto.id
            lista.timestamp = str(time())

            linha = Variables.Line()

            linha.id = "l1"

            linha.name = "Linha1"
            linha.tag = "TAG"
            linha.type = "Causa"
            linha.signal = "Digital"
            linha.pid = "PID"
            linha.version = 1
            linha.list_id = "L1"
            linha.created_at = str(time())

            lista.dirLines[linha.id] = linha

            projeto.dirList[lista.id] = lista

            self.dirProject[projeto.id] = projeto

            self.insertProject(projeto)

        else:
            pass


    def nova_lista(self):


        parents = set()
        for index in self.ui.treeView.selectedIndexes():
            while index.parent().isValid():
                index = index.parent()
            parents.add(index.sibling(index.row(), 0))

        index = [index.row() for index in sorted(parents)]
        index = index[0]


        if index == -1:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione um projeto.")

        else:

            var_teste = QtWidgets.QMessageBox.question(self, "Aviso",
                                                       'Deseja criar uma nova lista?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if var_teste == QtWidgets.QMessageBox.Yes:
                projeto = self.dirProject["P"+str(index+1)]

                size_tree = len(projeto.dirList.keys())

                lista = Variables.List()

                lista.id = "L" + str(size_tree+1)
                lista.nome = "Lista" + str(size_tree+1)
                lista.project_id = projeto.id
                lista.timestamp = str(time())

                projeto.dirList[lista.id] = lista

                self.dirProject[projeto.id] = projeto

                self.insertList(index,lista)

    def insertProject(self,project):

        projeto = QStandardItem(project.nome)

        lista1 = QStandardItem('Lista1')
        projeto.appendRow(lista1)

        self.rootNode.appendRow(projeto)
        self.ui.treeView.expandAll()

    def insertList(self,index,lists):

        lista = QStandardItem(lists.nome)

        self.ui.treeView.model().item(index).appendRow(lista)

        self.ui.treeView.expandAll()


    def open_list(self):

        self.ui.treeView.expandAll()

        parents = set()

        flag_lista = False
        for nomeProjeto in self.ui.treeView.selectedIndexes():
            while nomeProjeto.parent().isValid():
                nomeProjeto = nomeProjeto.parent()
                flag_lista = True

            parents.add(nomeProjeto.sibling(nomeProjeto.row(), 0))


        if flag_lista == False:
            nomeProjeto = [nomeProjeto.data() for nomeProjeto in sorted(parents)]
            nomeProjeto = nomeProjeto[0]

            index = [nomeProjeto.row() for nomeProjeto in sorted(parents)]
            index = index[0]

            id = "P" + str(index+1)

            child = subWindow(self,self.dirProject[id])

            self.ui.mdiArea.addSubWindow(child)
            child.setWindowTitle(nomeProjeto)

            child.show()



# Executa a interface gráfica
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = StartMain()
    myapp.show()

    sys.exit(app.exec_())