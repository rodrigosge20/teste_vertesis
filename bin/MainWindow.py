import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from time import time

from uiMain import Ui_MainWindow
import Variables


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



# Executa a interface gráfica
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = StartMain()
    myapp.show()

    sys.exit(app.exec_())