from time import sleep

bibliotecas = []

op_bibl = ["[1] Cadastrar biblioteca",
           "[2] Acessar biblioteca"]

op_item = ["[1] Cadastrar novo item",
           "[2] Emprestar item"]

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

def get_biblioteca(filial):
    for item in bibliotecas:
        if item.num_filial == filial:
            return item

def menu_biblioteca(biblioteca):
    print(f"{biblioteca.nome:=^50}")

class Biblioteca:
    def __init__(self, nome, num_filial):
        self.nome = nome
        self.num_filial = num_filial.strip()
        self.estoque = []

    def __str__(self):
        return f"{"[" + self.num_filial + "] " + self.nome:^50}"

    def adicionar_item(self, item):
        self.estoque.append(item)

    def emprest_item(self, item, destino):
        destino.adicionar_item(item)        

class Livro:
    def __init__(self, codigo, nome, genero, autor, editora, ano, page_num, saldo, possivel_emprest=True):
        self.codigo = codigo
        self.nome = nome
        self.genero = genero
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.page_num = page_num
        self.possivel_emprest = possivel_emprest
        self.saldo = saldo


class Revista(Livro):
    def __init__(self, codigo, nome, page_num, edicao, mes, editora, saldo, possivel_emprest=True):
        super().__init__(codigo, nome, page_num, editora, saldo, possivel_emprest)
        self.edicao = edicao
        self.mes = mes

while True:
    print(f"{" SISTEMA DE BIBLIOTECA ":=^50}\n")
    for b in op_bibl:
        print(f"{b:^50}\n")

    select = int(input("Selecione uma opção: "))

    match select:
        case 1:
            while True:
                nome, filial = input("\nDigite o nome e filial da nova biblioteca respectivamente, separando-os por vírgula: ").split(",")
                bibliotecas.append(Biblioteca(nome, filial))
                if pergunta("Deseja cadastrar uma nova biblioteca?"):
                    continue
                else:
                    print("\nRetornando ao menu...")
                    sleep(1.5)
                    break

        case 2:
            if len(bibliotecas) <= 0:
                print("\nNão há bibliotecas disponíveis para consulta. Retornando ao menu...\n")
                sleep(1.5)
                continue
            print(f"\n{" BIBLIOTECAS DISPONIVEIS ":=^50}\n")
            for b in bibliotecas:
                print(b)
            selecao_filial = input("\nSelecione a biblioteca que deseja acessar: ")

            bibl = get_biblioteca(selecao_filial)

            menu_biblioteca(bibl)