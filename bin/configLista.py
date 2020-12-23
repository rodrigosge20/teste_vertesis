from PyQt5 import QtCore, QtGui, QtWidgets

from VarTable import VarTable



class listaTab(VarTable):
    def __init__(self, parent=None, window=None):
        super(listaTab, self).__init__("m", parent, window)

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.configTable()

        self.ui.addButton.released.connect(self.window.insertMan)

    def configTable(self):
        topHeader = "Num;TAG;Tipo;Sinal;PID;Versão"
        self.ui.table.setColumnCount(len(topHeader.split(";")))
        self.ui.table.setHorizontalHeaderLabels(topHeader.split(";"))

        self.ui.table.setColumnWidth(0, 130)
        self.ui.table.setColumnWidth(2, 60)
        self.ui.table.setColumnWidth(3, 60)


