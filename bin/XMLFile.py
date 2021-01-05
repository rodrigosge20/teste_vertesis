import xml.etree.ElementTree as ET

import Variables


class XMLFile:
    """Classe responsável pela manipulação dos dados para criação de arquivos .xml.

    O usuário pode salvar todos Projetos ou uma Lista específica.

    Por fim, o usuário pode abrir na interface um arquivo de .xml que contenha projetos.
    """

    def carrega_xml(self, filename, filepath):
        """Função responsável por carregar o arquivo .xml que contenha projetos

        :param filename contem o nome do arquivo
        :param filepath contem o caminho do arquivo
        """

        # Cria uma árvore que contem os dados do arquivo .xml especificado
        tree = ET.parse(filepath + '/' + filename)
        root = tree.getroot()

        # flag criada para verificação de ramos de Projeto, gerando uma janela de erro informando o usuário caso o
        # arquivo .xml for inválido, ou seja, caso não contenha informações de projeto
        erro_lista = root.find('Projeto')

        # se a variável não possuir ramos 'Projeto' retorna para geração da janela de aviso
        if erro_lista == None:
            return -1

        else:
            # cria um novo dicionário de projetos
            self.dirProject = {}

            # para cada ramo de projeto contido no arquivo .xml checa-se cada informação para adicionar ao dicionário
            for projeto_xml in root.findall('Projeto'):

                projeto = Variables.Project()

                projeto.id = projeto_xml.get('id')

                projeto.name = projeto_xml.find('name').text
                projeto.description = projeto_xml.find('description').text
                projeto.created_at = projeto_xml.find('created_at').text

                listas = projeto_xml.find('Listas')

                # para cada ramo de lista contido no arquivo .xml, dentro de projeto, checa-se cada informação para
                # adicionar ao dicionário de listas
                for lista_xml in listas.findall('Lista'):

                    lista = Variables.List()

                    lista.id = lista_xml.get('id')

                    lista.name = lista_xml.find('name').text
                    lista.project_id = lista_xml.find('project_id').text
                    lista.created_at = lista_xml.find('created_at').text

                    linhas = lista_xml.find('Linhas')

                    # para cada ramo de linha contido no arquivo .xml, dentro da lista, checa-se cada informação para
                    # adicionar ao dicionário de linhas
                    for linha_xml in linhas.findall('Linha'):

                        linha = Variables.Line()

                        linha.id = linha_xml.get('id')

                        linha.name = linha_xml.find('name').text
                        linha.tag = linha_xml.find('tag').text
                        linha.type = linha_xml.find('type').text
                        linha.signal = linha_xml.find('signal').text
                        linha.pid = linha_xml.find('pid').text
                        linha.version = int(linha_xml.find('version').text)
                        linha.list_id = linha_xml.find('list_id').text
                        linha.created_at = linha_xml.find('created_at').text

                        # Adiciona a nova linha ao dicionário de linhas
                        lista.dirLines[linha.id] = linha

                    # Adiciona a nova lista ao dicionário de lista
                    projeto.dirList[lista.id] = lista

                # Adiciona o novo projeto ao dicionário de projeto
                self.dirProject[projeto.id] = projeto

                # Chama a função insertProject para inserir o novo projeto na árvore
                self.insertProject(projeto)

            return 1

    def save_lista_xml(self,file,lista):
        """Função responsável por salvar um lista num arquivo .xml

        :param file contem o nome e caminho do arquivo
        :param lista contem as informações da lista a ser salva
        """

        # Criação do ramo principal do arquivo .xml
        root = ET.Element('Lista')

        # Identifica o id do ramo como sendo o id da lista
        root.set('id', lista.id)

        # Busca de cada informação contida na lista, inserindo no ramo principal
        ET.SubElement(root, 'name').text = lista.name
        ET.SubElement(root, 'project_id').text = lista.project_id
        ET.SubElement(root, 'created_at').text = lista.created_at

        # Criação de um sub-ramo contendo as linhas da lista
        linhas = ET.SubElement(root, 'Linhas')

        # Variável que armaneza o dicionário de linhas da lista
        data_linha = lista.dirLines

        # Busca de todas as ids de linhas presente no dicionário, que correspondem às chaves do dicionário
        for key_linha in sorted(data_linha):
            linha = ET.SubElement(linhas, 'Linha')

            # Identifica o id do ramo como sendo o id da linha
            linha.set('id', key_linha)

            # Busca de cada informação contida na linha, inserindo no sub-ramo atual de lista
            ET.SubElement(linha, 'name').text = data_linha[key_linha].name
            ET.SubElement(linha, 'tag').text = data_linha[key_linha].tag
            ET.SubElement(linha, 'type').text = data_linha[key_linha].type
            ET.SubElement(linha, 'signal').text = data_linha[key_linha].signal
            ET.SubElement(linha, 'pid').text = data_linha[key_linha].pid
            ET.SubElement(linha, 'version').text = str(data_linha[key_linha].version)
            ET.SubElement(linha, 'list_id').text = lista.id
            ET.SubElement(linha, 'created_at').text = data_linha[key_linha].created_at

        # Identação do arquivo .xml
        XMLFile.indent(self, root)

        # Cria a árvore e escreve no arquivo com caminho "file" as informações obtidas
        tree = ET.ElementTree(root)
        tree.write(file, xml_declaration=True, encoding='iso-8859-1', method="xml")

    def save_xml(self, file):

        # Variável que armaneza o dicionário com todos Projetos criados
        data_projeto = self.dirProject

        # Criação do ramo principal Projetos
        root = ET.Element('Projetos')

        # Busca de todas as ids de projetos presente no dicionários, que correspondem às chaves do dicionário
        for key_projeto in sorted(data_projeto):
            projeto = ET.SubElement(root,'Projeto')

            # Identifica o id do ramo como sendo o id do projeto
            projeto.set('id', key_projeto)

            # Busca de cada informação contida no projeto, inserindo no ramo principal
            ET.SubElement(projeto, 'name').text = data_projeto[key_projeto].name
            ET.SubElement(projeto, 'description').text = data_projeto[key_projeto].description
            ET.SubElement(projeto, 'created_at').text = data_projeto[key_projeto].created_at

            # Sequencia em diante é semelhante à função de Salvar Listas, salvando porém TODAS as listas presentes
            # nos projetos.
            listas = ET.SubElement(projeto,'Listas')

            data_lista = data_projeto[key_projeto].dirList

            for key_lista in sorted(data_lista):
                lista = ET.SubElement(listas,'Lista')

                lista.set('id', key_lista)

                ET.SubElement(lista, 'name').text = data_lista[key_lista].name
                ET.SubElement(lista, 'project_id').text = key_projeto
                ET.SubElement(lista, 'created_at').text = data_lista[key_lista].created_at

                linhas = ET.SubElement(lista, 'Linhas')

                data_linha = data_lista[key_lista].dirLines

                for key_linha in sorted(data_linha):
                    linha = ET.SubElement(linhas, 'Linha')

                    linha.set('id', key_linha)

                    ET.SubElement(linha, 'name').text = data_linha[key_linha].name
                    ET.SubElement(linha, 'tag').text = data_linha[key_linha].tag
                    ET.SubElement(linha, 'type').text = data_linha[key_linha].type
                    ET.SubElement(linha, 'signal').text = data_linha[key_linha].signal
                    ET.SubElement(linha, 'pid').text = data_linha[key_linha].pid
                    ET.SubElement(linha, 'version').text = str(data_linha[key_linha].version)
                    ET.SubElement(linha, 'list_id').text = key_lista
                    ET.SubElement(linha, 'created_at').text = data_linha[key_linha].created_at

            # Identação do arquivo .xml
            XMLFile.indent(self, root)

            # Cria a árvore e escreve no arquivo com caminho "file" as informações obtidas
            tree = ET.ElementTree(root)
            tree.write(file, xml_declaration=True, encoding='iso-8859-1', method="xml")


    def indent(self, elem, level=0):
        """Função criada para melhorar a identação do arquivo .xml gerado."""
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                XMLFile.indent(self, elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
