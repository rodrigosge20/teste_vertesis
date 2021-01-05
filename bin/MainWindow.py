"""No MainWindow.py é definida a classe 'StartMain' e o comando para invocar a interface gráfica.
A classe principal 'StartMain' contem os principais elementos da janela principal da interface.
"""

import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem, QStandardItemModel
from datetime import datetime

from uiMain import Ui_MainWindow

from Variables import Project, List, Line
from SubWindow import subWindow
from XMLFile import XMLFile


class StartMain(QtWidgets.QMainWindow):
    """Recebe como parâmetro de entrada a classe QtWidgets.QMainWindow que faz a gestão da janela principal da interface gráfica.

    Essa classe é responsável pelas operações básicas da interface, como abrir, salvar e fechar arquivos, a partir da
    utilização da barra de ferramentas.
    """

    def __init__(self, parent=None):
        """Função que inicializa a janela principal e seus atributos.
        São definidas as conexões entre os diferentes sinais e operações de usuário.

        """

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        Criação da variável que armazenará as informações da interface responsável pela árvore de projetos e listas
        """
        self.ui.treeView.setHeaderHidden(True)
        self.ui.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        treeModel = QStandardItemModel()
        self.ui.treeView.setModel(treeModel)
        self.rootNode = treeModel.invisibleRootItem()

        self.ui.treeView.setExpandsOnDoubleClick(False)


        """
        A variável dirProject é um dicionário que armaneza todas as informações dos projetos criados
        As chaves do diciionários são os ids de cada projeto, todas começando com a letra P
        """
        self.dirProject = {}

        """
        A função connect tem como objetivo criar uma ponte entre ações do usuário e o resultado que deseja-se obter
        após a ação ter sido terminada.
        """

        """
        Connects da barra de ferramentas
        """
        self.ui.actionNovoProjeto.triggered.connect(self.projeto_branco) # Se na barra de ferramentas for clicado em Novo
                                                                       # Projeto, chama-se função novo_projeto
        self.ui.actionFecharProjeto.triggered.connect(self.close) # Se na barra de ferramentas for clicado em Fechar,
                                                                  # chama-se função close, fechando a UI
        self.ui.actionSalvarProjeto.triggered.connect(self.salvar_projeto) # Se na barra de ferramentas for clicado em
                                                                           # Salvar Projeto, chama-se função salvar_projeto
        self.ui.actionAbrirProjeto.triggered.connect(self.abrir_projeto) # Se na barra de ferramentas for clicado em
                                                                         # Abrir Projeto, chama-se função abrir_projeto
        self.ui.actionSobre.triggered.connect(self.sobre_projeto)  # Se na barra de ferramentas for clicado em
                                                                   # Sobre, chama-se função sobre_projeto

        """
        Connects dos botões acima da árvore, seguindo a mesma lógica para a barra de ferramentas
        """
        self.ui.novoProjetoButton.clicked.connect(self.novo_projeto)

        self.ui.salvarProjetoButton.clicked.connect(self.salvar_projeto)
        self.ui.salvarListaButton.clicked.connect(self.salvar_lista)
        self.ui.abrirProjetoButton.clicked.connect(self.abrir_projeto)
        self.ui.treeView.doubleClicked.connect(self.abrir_arvore) # Se for clicado no botão para abrir uma lista
                                                               # chama-se a função open_list
        self.ui.novaListaButton.clicked.connect(self.nova_lista)  # Se for clicado no botão para criar nova lista
                                                                  # chama-se a função nova_lista

        """
        A função setToolTip ajuda na usabilidade da interface, criando uma dica ao usuário quando ele mantem o mouse
        em cima dos botões presentes.
        """
        self.ui.novoProjetoButton.setToolTip('Adicionar Projeto')
        self.ui.salvarProjetoButton.setToolTip('Salvar Projeto')
        self.ui.salvarListaButton.setToolTip('Salvar Lista')
        self.ui.abrirProjetoButton.setToolTip('Abrir Projeto')
        self.ui.novaListaButton.setToolTip('Adicionar Lista')

        """
        Criação de atalhos para adição e remoção de projetos ou listas usando botão direito do Mouse
        """
        self.ui.treeView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)


        actionAdicionar = QtWidgets.QAction("Adicionar", self)
        actionRemover = QtWidgets.QAction("Remover", self)

        actionAdicionar.triggered.connect(self.novo_projeto)
        actionAdicionar.setShortcut("+")
        actionAdicionar.setShortcutContext(QtCore.Qt.ApplicationShortcut)

        actionRemover.triggered.connect(self.remover)
        actionRemover.setShortcut("-")
        actionRemover.setShortcutContext(QtCore.Qt.ApplicationShortcut)

        self.ui.treeView.addAction(actionAdicionar)
        self.ui.treeView.addAction(actionRemover)


    def projeto_branco(self):
        """Função responsável por reiniciar um projeto novo em branco"""


        self.dirProject = {}

        """
       Criação da variável que armazenará as informações da interface responsável pela árvore de projetos e listas
       """
        self.ui.treeView.setHeaderHidden(True)
        self.ui.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        treeModel = QStandardItemModel()
        self.ui.treeView.setModel(treeModel)
        self.rootNode = treeModel.invisibleRootItem()

        self.ui.treeView.setExpandsOnDoubleClick(False)

        self.ui.actionSalvarProjeto.setEnabled(False)
        self.ui.salvarListaButton.setEnabled(False)
        self.ui.salvarProjetoButton.setEnabled(False)

        try:
            subwindow = self.ui.mdiArea.currentSubWindow()
            subwindow.close()
        except AttributeError:
            pass

    def novo_projeto(self):
        """Função responsável por criar um novo projeto.
        """

        """
        Cria-se a variável var_teste para verificar se o usuário realmente deseja iniciar um projeto, usando a função
        QtWidgets.QMessageBox.question, que retorna "Yes" ou "No", indicando a resposta do usuário
        """
        var_teste = QtWidgets.QMessageBox.question(self, "Aviso",
                                              'Deseja criar um novo projeto?',
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        """
        É criado um novo projeto apenas se o usuário escolheu "Yes"
        """
        if var_teste == QtWidgets.QMessageBox.Yes:

            """
            Habilita os botões de salvar. Para fins de usabilidade, elas permanecem desativadas quando não há nenhum 
            projeto aberto            """

            self.ui.actionSalvarProjeto.setEnabled(True)
            self.ui.salvarListaButton.setEnabled(True)
            self.ui.salvarProjetoButton.setEnabled(True)

            # A variável 'projeto' é criada como objeto da classe Project, definida em Variables.py
            projeto = Project()


            # A variável 'last_key' armaneza o id do último projeto armazenado em dirProject

            key = list(self.dirProject.keys())
            if key != []: # verifica-se se existe alguma chave no dicionário
                last_key = int(key[-1].replace('P',''))
            else:
                last_key = 0

            # Cada atributo do objeto Projeto é atribuído um valor
            # As id sempre iniciam com P mais um valor inteiro
            # O projeto sempre inicia com Projeto mais um valor inteiro
            projeto.id = "P" + str(last_key+1)
            projeto.name = "Projeto" + str(last_key+1)
            projeto.description = projeto.name + " do teste para vertesis."
            now = datetime.now()
            projeto.created_at = str(now.strftime("%d/%m/%Y %H:%M:%S"))

            # A variável 'lista' é criada como objeto da classe List, definida em Variable.py
            lista = List()

            # Os atributos da lista são atruídos valores iniciados conforme abaixo
            lista.id = "L1"
            lista.name = "Lista1"
            lista.project_id = projeto.id
            now = datetime.now()
            lista.created_at = str(now.strftime("%d/%m/%Y %H:%M:%S"))

            # Armazena-se no dicionário dirList, que é atributo do objeto projeto, a lista criada
            projeto.dirList[lista.id] = lista

            # Armazena-se no dicionário dirProject o projeto criado
            self.dirProject[projeto.id] = projeto

            # Insere na árvore presente na UI o projeto e sua lista
            self.insertProject(projeto)

            self.ui.treeView.expandAll()

        else:
            pass

    def remover(self):
        """Função responsável por remover um Projeto ou Lista"""


        # A variável 'parents' é utilizada para verificar se o item clicado na árvore possui algum ramo "pai"
        # Isso é feito para verificar se foi clicado numa lista ou num projeto e então remover corretamente o
        # ramo especificado
        parents = set()

        """
        A variável 'flag_lista' armazena a informação se foi lista ou projeto clicado.
        # True indica que foi clicado numa lista
        # False indica que foi clicado num projeto
        """
        flag_lista = False

        # Verifica todos itens clicados na árvore
        for nomeProjeto in self.ui.treeView.selectedIndexes():
            while nomeProjeto.parent().isValid(): # enquanto o item clicado possuir um ramo pai, o nome desse item é
                                                  # alterado para o do pai, de forma a armazenar o nome do projeto
                                                  # da lista que foi clicada
                                                  # a flag_lista é alterada pra indicar que uma lista foi clicada
                nomeProjeto = nomeProjeto.parent()
                flag_lista = True

            parents.add(nomeProjeto.sibling(nomeProjeto.row(), 0))

        # row armazena a posição do ramo pai na árvore
        row = nomeProjeto.row()

        """
        Cria-se uma lista com o nome de todos projetos clicados
        Como apenas um projeto pode ser clicado em qualquer situação, pega-se a primeira posição do vetor com todos
        nomes para armazenar o nome do projeto que foi clicado no momento
        """
        nomeProjeto = [nomeProjeto.data() for nomeProjeto in sorted(parents)]
        nomeProjeto = nomeProjeto[0]

        # a variável 'key_projeto' armazena a id (chave) do projeto atual
        for keys in sorted(self.dirProject):
            if self.dirProject[keys].name == nomeProjeto:
                key_projeto = keys

        # se o item clicado na árvore for um projeto, então remove esse projeto da árvore e do dicionário que armazena
        # os projetos
        if flag_lista == False:

            self.ui.treeView.model().removeRow(row)

            self.dirProject.pop(key_projeto)

        # se o item clicado na árvore for uma lista, verifica-se o nome e a chave dessa lista no dicionário de projetos
        # e então remove-se da árvore e do dicionário a lista clicada
        else:
            for index in self.ui.treeView.selectedIndexes():
                nomeLista = index.data()
                row = index.row()


                for keys in sorted(self.dirProject[key_projeto].dirList):
                    if self.dirProject[key_projeto].dirList[keys].name == nomeLista:
                        self.dirProject[key_projeto].dirList.pop(keys)

                self.ui.treeView.model().removeRow(row,index.parent())


    def salvar_projeto(self):
        """Função responsável por salvar o projeto.
        """

        # O nome default do arquivo é "Untitled"
        title = "Untitled"

        # Abre-se uma janela de diálogo para salvar o arquivo desejado
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Salvar Projeto como", title, "*.xml")

        # Se o usuário clicou em Ok, a função save_xml da classe XMLFile é chamada para então criar um arquivo .xml
        # com os projetos, listas e linhas criadas pelo usuário
        if filename:
            XMLFile.save_xml(self, filename)

    def salvar_lista(self):
        """Função responsável por salvar uma lista.
        """

        parents = set()
        flag_lista = False
        # Verifica todos itens clicados na árvore
        for nomeProjeto in self.ui.treeView.selectedIndexes():
            while nomeProjeto.parent().isValid():  # enquanto o item clicado possuir um ramo pai, o nome desse item é
                # alterado para o do pai, de forma a armazenar o nome do projeto
                # da lista que foi clicada
                # a flag_lista é alterada pra indicar que uma lista foi clicada
                nomeProjeto = nomeProjeto.parent()
                flag_lista = True

            parents.add(nomeProjeto.sibling(nomeProjeto.row(), 0))

        nomeProjeto = [nomeProjeto.data() for nomeProjeto in sorted(parents)]
        nomeProjeto = nomeProjeto[0]

        # a variável 'key_projeto' armazena a id (chave) do projeto atual
        for keys in sorted(self.dirProject):
            if self.dirProject[keys].name == nomeProjeto:
                key_projeto = keys

        if flag_lista == True:
            for index in self.ui.treeView.selectedIndexes():
                nomeLista = index.data()
                row = index.row()

                for keys in sorted(self.dirProject[key_projeto].dirList):
                    if self.dirProject[key_projeto].dirList[keys].name == nomeLista:
                        lista = self.dirProject[key_projeto].dirList[keys]


        # O nome default do arquivo é "Untitled"
        title = "Untitled"

        # Abre-se uma janela de diálogo para salvar o arquivo desejado
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Salvar Lista como", title, "*.xml")

        # Se o usuário clicou em Ok, a função save_xml da classe XMLFile é chamada para então criar um arquivo .xml
        # com os projetos, listas e linhas criadas pelo usuário
        if filename:
            XMLFile.save_lista_xml(self, filename, lista)

    def abrir_projeto(self):
        """Função responsável por abrir um novo projeto na janela principal.
        """

        """
        Todas informações atuais da árvore são apagadas para abrir o arquivo desejado
        """
        treeModel = QStandardItemModel()
        self.ui.treeView.setModel(treeModel)
        self.rootNode = treeModel.invisibleRootItem()

        # As informações antigas do dicionário de projetos são removidas


        # A variável 'fileinfo' armazena o caminho do arquivo que deseja-se abrir
        fileinfo, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir', '', '*.xml')
        if not fileinfo:
            return
        filename = os.path.basename(fileinfo)
        filepath = os.path.dirname(fileinfo)

        # Se o usuário clicou escolheu um arquivo, a função carrega_xml da classe XMLFile é chamada para então carregar
        # o arquivo .xml selecionado com os seus respectivos projetos, listas e linhas criadas pelo usuário
        # A variável 'flag' é utiliza para verificar se o arquivo .xml é consistente, retornando -1 caso seja inválido e
        # retornando 1 caso seja válido.
        flag = XMLFile.carrega_xml(self, filename, filepath)

        if flag == -1:
            QtWidgets.QMessageBox.warning(self, "Aviso", "XML Inválido")
        else:
            self.ui.actionSalvarProjeto.setEnabled(True)
            self.ui.salvarListaButton.setEnabled(True)
            self.ui.salvarProjetoButton.setEnabled(True)

            # A nova árvore aberta então é expandida e qualquer projeto antigo aberto é fechado
            self.ui.treeView.expandAll()

            try:
                subwindow = self.ui.mdiArea.currentSubWindow()
                subwindow.close()
            except AttributeError:
                pass



    def nova_lista(self):
        """Função responsável por criar novas listas"""


        """
        Verifica se ao clicar no botão de criar lista, algum projeto está selecionado
        """
        parents = set()
        for nomeProjeto in self.ui.treeView.selectedIndexes():
            while nomeProjeto.parent().isValid():
                nomeProjeto = nomeProjeto.parent()
            parents.add(nomeProjeto.sibling(nomeProjeto.row(), 0))

        index = [nomeProjeto.row() for nomeProjeto in sorted(parents)]
        nomeProjeto = [nomeProjeto.data() for nomeProjeto in sorted(parents)]


        #se nenhum projeto for selecionado, uma janela de aviso é gerada, informando o usuário.
        if index == -1 or index == []:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione um projeto.")

        #se houver um projeto selecionado, pergunta-se ao usuário se ele deseja criar uma lista
        else:

            #armazena qual a posição do projeto clicado na árvore e o seu nome, pegando o id a partir do valor inteiro
            #presente no final do nome do projeto
            index = index[0]
            nomeProjeto = nomeProjeto[0]
            idProjeto = nomeProjeto[-1]

            var_teste = QtWidgets.QMessageBox.question(self, "Aviso",
                                                       'Deseja criar uma nova lista?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if var_teste == QtWidgets.QMessageBox.Yes:
                projeto = self.dirProject["P"+idProjeto]


                key = list(projeto.dirList.keys())
                if key != []:
                    last_key = int(key[-1].replace('L', ''))
                else:
                    last_key = 0

                # Semelhante a criação de projeto
                lista = List()

                lista.id = "L" + str(last_key+1)
                lista.name = "Lista" + str(last_key+1)
                lista.project_id = projeto.id
                now = datetime.now()
                lista.created_at = str(now.strftime("%d/%m/%Y %H:%M:%S"))

                # Adiciona a lista ao dicionario de listas do objeto projeto
                projeto.dirList[lista.id] = lista

                # Modifica o objeto projeto no dicionário de projetos para conter a nova lista
                self.dirProject[projeto.id] = projeto

                # Insere a lista na árvore
                self.insertList(index,lista)

    def insertProject(self,project):
        """Função responsável por inserir um novo projeto na árvore da UI"""

        projeto = QStandardItem(project.name)

        # Adiciona todas as listas que o projeto possui
        for key in sorted(project.dirList):

            lista1 = QStandardItem(project.dirList[key].name)
            projeto.appendRow(lista1)

        self.rootNode.appendRow(projeto)

    def insertList(self,index,lists):
        """Função respons+avel por adicionar uma lista num projeto específico"""

        lista = QStandardItem(lists.name)

        self.ui.treeView.model().item(index).appendRow(lista)


    def abrir_arvore(self):
        """Função responsável por abrir um projeto selecionado pelo usuário da árvore e todas as suas listas
         na SubWindow presente na UI
        """


        """
        É feita uma verificação se o usuário clicou numa lista ou num projeto, de forma que apenas quando um projeto é
        clicado que a SubWindow é
        """
        parents = set()

        flag_lista = False
        for nomeProjeto in self.ui.treeView.selectedIndexes():
            while nomeProjeto.parent().isValid():
                nomeProjeto = nomeProjeto.parent()
                flag_lista = True

            parents.add(nomeProjeto.sibling(nomeProjeto.row(), 0))

        # Se for um projeto clicado na árvore
        if flag_lista == False:
            nomeProjeto = [nomeProjeto.data() for nomeProjeto in sorted(parents)]
            nomeProjeto = nomeProjeto[0]

            index = [nomeProjeto.row() for nomeProjeto in sorted(parents)]
            index = index[0]

            keys = list(self.dirProject.keys())
            id = keys[index]

            # cria-se uma subwindow que recebe como parâmetro o projeto que foi selecionado
            child = subWindow(self,self.dirProject[id])

            self.ui.mdiArea.addSubWindow(child)
            child.setWindowTitle(nomeProjeto)

            child.show()

    def sobre_projeto(self):
        """Função responsável por abrir a janela contendo informações básicas sobre o teste.
        """

        sobre = QtWidgets.QMessageBox()

        sobre.setWindowIcon(QtGui.QIcon(":/icons/images/br.jpg"))
        sobre.setText("<b>Teste Vertesis</b>")
        sobre.setInformativeText("Versão 1.0.0.\n\n Desenvolvido por Rodrigo Gesser. \n\n Ferramenta para armazenar lista de TAGs.")
        sobre.setWindowTitle("Sobre o Teste")
        sobre.setStandardButtons(QtWidgets.QMessageBox.Cancel)

        retval = sobre.exec_()

# Executa a interface gráfica
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = StartMain()
    myapp.show()

    sys.exit(app.exec_())