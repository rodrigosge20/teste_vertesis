from PyQt5 import  QtWidgets

from uiVarTable import Ui_VarTable


class VarTable(QtWidgets.QWidget):

    """Classe responsável pela configuração das tabelas presentes

    Para futuras implementações, aqui ficaram diferentes tipos de funções para as listas.
    Para o teste atual a função dessa classe é pequena.
    """

    def __init__(self, type, parent = None, window = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_VarTable()
        self.ui.setupUi(self)

        # parent window
        self.window = window