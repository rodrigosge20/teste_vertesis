from PyQt5 import QtCore, QtGui, QtWidgets

from uiVarTable import Ui_VarTable


class VarTable(QtWidgets.QWidget):
    #type - tipo de variável
    # -> "c": controlada
    # -> "m": manipulada
    # -> "p": perturbação
    def __init__(self, type, parent = None, window = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_VarTable()
        self.ui.setupUi(self)

        # parent window
        self.window = window

        # tipo e tag inicial da ID
        self.type = type

        #menu de contexto da tabela
        table = self.ui.table
        #table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #table.customContextMenuRequested.connect(self.tableContextMenu)

        # table.cellChanged.connect(self.tableModified)

    # def mainWindow(self):
    #     return self.topLevelWidget()
    #
    # def findVarByID(self, id):
    #     table = self.ui.table
    #     for i in range(table.rowCount()):
    #         if table.verticalHeaderItem(i).text() == id:
    #             return i
    #     return -1
    #
    # def findVarRow(self, name):
    #     table = self.ui.table
    #     for i in range(table.rowCount()):
    #         if table.item(i, 0).text() == name:
    #             return i
    #     return -1
    #
    # def findVarRowByID(self, id):
    #     table = self.ui.table
    #     for i in range(table.rowCount()):
    #         if table.verticalHeaderItem(i).text() == id:
    #             return i
    #     return -1
    #
    # def findVarIDByName(self, name):
    #     table = self.ui.table
    #     for i in range(table.rowCount()):
    #         if table.item(i, 0).text() == name:
    #             return table.verticalHeaderItem(i).text()
    #     return ""
    #
    # def findVarName(self, id):
    #     table = self.ui.table
    #     for i in range(table.rowCount()):
    #         if table.verticalHeaderItem(i).text() == id:
    #             return table.item(i, 0).text()
    #     return ""
    #
    # def varID(self, index):
    #     table = self.ui.table
    #     if index < table.rowCount():
    #         return table.verticalHeaderItem(index).text()
    #     return ""
    #
    # def insert(self, id, nome):
    #     table = self.ui.table
    #     if id == "" or nome == "":
    #         return -1
    #
    #     #verifica se já existe a variável pelo nome
    #     row = self.findVarRow(nome)
    #     if row != -1:
    #         return row
    #
    #     #verifica se já existe a variável pelo ID
    #     ntest = self.findVarName(id)
    #     if ntest != "":
    #         return self.findVarRow(nome)
    #
    #     #encontrar o local para inserir
    #     lst = []
    #     for i in range(table.rowCount()):
    #         lst.insert(len(lst),table.verticalHeaderItem(i).text())
    #     lst.insert(len(lst), id)
    #
    #     row = sorted(lst).index(id)
    #     table.insertRow(row)
    #
    #     # configura a altura da linha
    #     table.setRowHeight(row, 25)
    #
    #     #escreve o valor da ID no header vertical
    #     table.setVerticalHeaderItem(row, QtWidgets.QTableWidgetItem(id))
    #
    #     #escreve o nome da variável na coluna de nome
    #     table.setItem(row, 0, QtWidgets.QTableWidgetItem(nome))
    #
    #     #seleciona a linha
    #     table.selectRow(row)
    #
    #     return row
    #
    # def genID(self):
    #
    #     table = self.ui.table
    #     #encontrar o local para inserir
    #     row = 0
    #     if table.rowCount() != 0:
    #         if int(table.verticalHeaderItem(0).text()[1:]) == 0:
    #             if table.rowCount() > 1:
    #                 for i in range(1, table.rowCount()):
    #                     if int(table.verticalHeaderItem(i).text()[1:])-1 != int(table.verticalHeaderItem(i-1).text()[1:]):
    #                         row = i
    #                         break
    #                     else:
    #                         row = i+1
    #             else:
    #                 row = 1
    #
    #     return self.type + str(row).zfill(3)
    #
    # def tableModified(self):
    #     self.window.setWindowModified(True) #indica que o arquivo foi modificado
    #
    # def remove(self):
    #     self.window.setWindowModified(True) #indica que o arquivo foi modificado
    #     table = self.ui.table
    #     id = table.verticalHeaderItem(table.currentRow()).text()
    #     table.removeRow(table.currentRow())
    #
    #     if table.rowCount() == 0:
    #         self.ui.cfgButton.setDisabled(True)
    #         self.ui.remButton.setDisabled(True)
    #
    #     return id
    #
    # def tableContextMenu(self, point):
    #     menu = QtWidgets.QMenu(self)
    #     table = self.ui.table
    #
    #     header = table.horizontalHeader()
    #
    #     actionConfig = menu.addAction("Configurar")
    #     menu.addSeparator()
    #     actionAdd = menu.addAction("Adicionar")
    #     actionRem = menu.addAction("Remover")
    #
    #     actionConfig.triggered.connect(self.configVar)
    #     actionAdd.triggered.connect(self.insertVar)
    #     actionRem.triggered.connect(self.removeVar)
    #
    #     if not table.rowCount():
    #         actionRem.setDisabled(1)
    #         actionConfig.setDisabled(1)
    #
    #     point.setY(point.y()+header.height())
    #     menu.exec_(table.mapToGlobal(point))
    #
    # def selectRow(self):
    #     if self.ui.table.currentRow() >= 0:
    #         self.ui.cfgButton.setEnabled(True)
    #     else:
    #         self.ui.cfgButton.setEnabled(False)