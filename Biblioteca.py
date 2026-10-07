import os
from time import sleep
import json
import subprocess

save_path = "C:\\ProgramData\\Librarys\\"

op_bibl = ["[1] Cadastrar biblioteca",
           "[2] Acessar biblioteca",
           "[3] Sair"]

op_item = ["[1] Listar itens",
           "[2] Cadastrar novo item",
           "[3] Emprestar item",
           "[4] Devolver item",
           "[5] Retornar ao menu"]

def get_item(searched, list, variable=None):
    if variable:
        for item in list:
            if getattr(item, f"{variable}") == searched:
                return item
            else:
                continue
        return None
    else:
        for item in list:
            if item == searched:
                return item
            else:
                continue
        return None

def cont_regress(tempo):
    for t in range(tempo, 0 , -1):
        print(t)
        sleep(1)
    subprocess.run("cls", shell=True)

def pergunta(mensagem):
    while True:
        menu = input(f"\n{mensagem}\n[1] Sim\n[2] Não\n\nSeleção: ").lower()
        match menu:
            case "1" | "sim":
                return True
            case "2" | "nao" | "não" :
                return False
            case _:
                print("\nInsira uma opção válida.")
                continue

class Biblioteca:
    def __init__(self, nome, num_filial):
        self.nome = nome
        self.num_filial = str(num_filial)
        self.estoque_dict = []
        self.path = f"{save_path}{f"{self.num_filial} - {self.nome}"}.json"
        if not os.path.isfile(self.path):
            arq = open(self.path, "w")
            arq.write("[]")
            arq.close()
            self.estoque = []
        else:
            self.estoque = self.load_storage()
        
    def __str__(self):
        return f"{"[" + self.num_filial + "] " + self.nome:^50}"

    def load_storage(self):
        self.estoque_dict = []
        lista_interna = []
        if os.path.isfile(self.path):
            arq = open(self.path, "r")
            self.estoque_dict = json.load(arq)
            for prod in self.estoque_dict:
                lista_interna.append(Livro(**prod)) if prod["type"] == "Livro" else lista_interna.append(Revista(**prod))
            return lista_interna
        return []

    def save_storage(self):
        self.estoque_dict = []
        arq = open(self.path, "w")
        for item in self.estoque:
            self.estoque_dict.append(item.__dict__)
        json.dump(self.estoque_dict, arq)
        arq.close()

    def add_item(self, item):
        self.estoque.append(item)
        return

    def lend_item(self, item):
        item.can_lend = False
        pass

    def return_item(self, item):
        item.can_lend = True
        pass

    def has_lendable_items(self):
        if len([item for item in self.estoque if item.can_lend]) < 1:
            return False
        return True

    def has_returnable_items(self):
        if len([item for item in self.estoque if not item.can_lend]) < 1:
            return False
        return True

class ItemBiblioteca:
    def __init__(self, codigo, nome, genero, can_lend=True):
        self.codigo = codigo
        self.nome = nome
        self.genero = genero
        self.can_lend = can_lend

    def __str__(self):
        return f"{self.codigo} - {self.nome} - {"Disponivel" if self.can_lend else "Emprestado"}"

class Livro(ItemBiblioteca):
    def __init__(self, codigo, nome, genero, autor, editora, ano, page_num, type="Livro", can_lend=True):
        super().__init__(codigo, nome, genero, can_lend)
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.page_num = page_num
        self.type = type


class Revista(ItemBiblioteca):
    def __init__(self, codigo, nome, genero, edicao, mes, editora, type="Revista", can_lend=True):
        super().__init__(codigo, nome, genero, can_lend)
        self.edicao = edicao
        self.mes = mes
        self.editora = editora
        self.type = type

    def __str__(self):
        return f"{self.codigo:^10} - {self.nome} {self.edicao}ª edição - Mês de {self.mes} - Editora {self.editora} - {"Disponivel" if self.can_lend else "Emprestada"}"

def menu_biblioteca(biblioteca):
    while True:
        biblioteca.save_storage()
        print(f"{biblioteca.nome:=^50}")

        for op in op_item:
            print(f"{op:^50}\n")

        select = input("\nSelecione uma opção: ")

        match select:
            case "1":
                for item in biblioteca.estoque:
                    print(item)
                if pergunta("Deseja retornar ao menu?"):
                    print("\nRetornando ao menu...")
                    cont_regress(3)
                    continue
                else:
                    print("Saindo da biblioteca...")
                    cont_regress(3)
                    break

            case "2":
                while True:
                    print(f"\n{"CADASTRO DE PRODUTO":=^50}\n")
                    item_atual = None
                    codigo = input("\nInsira o codigo do item a ser cadastrado: ").strip()
                    nome = input("\nDigite o nome do item a ser cadastrado: ")
                    genero = input("\nDigite o gênero do item cadastrado: ")
        
                    while True:
                        select = input("\nO item cadastrado é um livro ou revista?\n" \
                        "[1] Livro\n" \
                        "[2] Revista\n" \
                        "Seleção: ").lower()
        
                        match select:
                            case "1" | "livro":
                                autor = input("\nInsira o nome do autor do livro: ")
                                editora = input("\nInsira o nome da editora do livro: ")
                                ano = input("\nDigite o ano de lançamento do livro: ")
                                page_num = int(input("\nDigite o número de páginas do livro: "))
        
                                item_atual = Livro(codigo,nome,genero,autor,editora,ano,page_num)
                                break
                            case "2" | "revista":
                                edicao = input("\nInsira o nº da edição: ")
                                mes = input("\nInsira o mês de emissão da edição: ")
                                editora = input("\nInsira o nome da editora da revista: ")
        
                                item_atual = Revista(codigo,nome,genero,edicao,mes,editora)
                                break
                            case _:
                                print("\nInsira uma opção válida.")
                                continue

                    biblioteca.add_item(item_atual)
                    print(f"\nSucesso no cadastro {"do livro" if item_atual.type=="Livro" else "da revista"} {item_atual.nome} (COD {item_atual.codigo})!")
                    if pergunta("Deseja cadastrar outro produto?"):
                        continue
                    else:
                        print("Retornando ao menu...")
                        cont_regress(3)
                        break
            case "3":
                while True:
                    print(f"\n{"EMPRÉSTIMO DE PRODUTO":=^50}\n")

                    if not biblioteca.has_lendable_items():
                        print("Não há itens disponíveis para empréstimo, retornando ao menu...")
                        cont_regress(3)
                        break

                    print("\nSelecione o item que deseja emprestar: \n")
                    for item in biblioteca.estoque:
                        if item.can_lend:
                            print(item)

                    try:
                        user_input = input('\nDigite o código que deseja emprestar, ou digite "SAIR" para cancelar: ')
                        
                        if user_input.lower() == "sair":
                            print("\nRetornando ao menu...")
                            cont_regress(3)
                            break

                        cod_item = get_item(user_input, biblioteca.estoque, "codigo")

                        if cod_item == None:
                            print("Não foi possível encontrar o item digitado, tente novamente!\n")
                            cont_regress(3)
                            continue

                        biblioteca.lend_item(cod_item)
                        print("Item emprestado com sucesso!")

                    except Exception as e:
                        print(e)
                        break

                    if pergunta("Deseja emprestar outro item?"):
                        continue
                    else:
                        print("Voltando ao menu...")
                        cont_regress(3)
                        break

            case "4":
                while True:
                    print(f"\n{"RETORNO DE PRODUTO":=^50}\n")
                    
                    if not biblioteca.has_returnable_items():
                        print("Não há itens disponíveis para retornar, voltando ao menu...")
                        cont_regress(3)
                        break

                    print('\nSelecione o item que deseja retornar: \n')
                    for item in biblioteca.estoque:
                        if not item.can_lend:
                            print(item)

                    try:
                        user_input = input('\nDigite o código que deseja retornar, ou digite "SAIR" para cancelar: ')

                        if user_input.lower() == "sair":
                            print("\nRetornando ao menu...")
                            cont_regress(3)
                            break

                        cod_item = get_item(user_input, biblioteca.estoque, "codigo")

                        if cod_item == None:
                            print("Não foi possível encontrar o item digitado, tente novamente!\n")
                            cont_regress(3)
                            continue
                        
                        biblioteca.return_item(cod_item)
                        print("Item retornado com sucesso!")

                    except Exception as e:
                        print(e)
                        break

                    if pergunta("Deseja retornar outro item?"):
                        continue
                    else:
                        print("Voltando ao menu...")
                        cont_regress(3)
                        break

            case "5":
                print("\nVoltando ao menu de seleção...")
                cont_regress(3)
                break

def load_library():
    internal_list = []
    for item in os.listdir(save_path):
        if item.endswith(".json"):
            filial, nome = item.strip().split("-")
            nome = nome.strip()
            internal_list.append(Biblioteca(nome.removesuffix(".json"), filial.strip()))
    return internal_list

bibliotecas = load_library()

def main():
    while True:
        print(f"{" SISTEMA DE BIBLIOTECA ":=^50}\n")
        for b in op_bibl:
            print(f"{b:^50}\n")

        select = int(input("Selecione uma opção: "))

        match select:
            case 1:
                while True:
                    nome = input("\nDigite o nome da nova biblioteca: ")
                    if "-" in nome:
                        print("\nO caractére '-' não é suportado, insira outro nome!")
                        continue
                    filial = int(input("\nAgora digite o número de filial da nova biblioteca: "))
                    bibliotecas.append(Biblioteca(nome, filial))
                    if pergunta("Deseja cadastrar uma nova biblioteca?"):
                        continue
                    else:
                        print("\nRetornando ao menu...")
                        cont_regress(3)
                        break

            case 2:
                if len(bibliotecas) <= 0:
                    print("\nNão há bibliotecas disponíveis para consulta. Retornando ao menu...\n")
                    cont_regress(3)
                    continue
                print(f"\n{" BIBLIOTECAS DISPONIVEIS ":=^50}\n")
                for b in bibliotecas:
                    print(b)
                selecao_filial = input("\nSelecione a biblioteca que deseja acessar: ")

                bibl = get_item(selecao_filial, bibliotecas, "num_filial")

                menu_biblioteca(bibl)

            case 3:
                print("\nFechando o programa...")
                cont_regress(3)
                break

main()