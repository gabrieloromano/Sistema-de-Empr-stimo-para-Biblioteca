from time import sleep

op_bibl = ["[1] Cadastrar biblioteca",
           "[2] Acessar biblioteca"]

op_item = ["[1] Listar itens",
           "[2] Cadastrar novo item",
           "[3] Emprestar item",
           "[4] Devolver item"]

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
        self.num_filial = num_filial.strip()
        self.estoque = []
        self.estoque_dict = []
        self.path = f"C:\\ProgramData\\Librarys\\{self.nome}.json"

    def __str__(self):
        return f"{"[" + self.num_filial + "] " + self.nome:^50}"

    def adicionar_item(self):
        while True:
            print(f"\n{"CADASTRO DE PRODUTO":=^50}\n")
            item_atual = None
            codigo = input("\nInsira o codigo do item a ser cadastrado: ")
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
                        self.estoque.append(item_atual)
                        break
                    case "2" | "revista":
                        edicao = input("\nInsira o nº da edição: ")
                        mes = input("\nInsira o mês de emissão da edição: ")
                        editora = input("\nInsira o nome da editora da revista: ")

                        item_atual = Revista(codigo,nome,genero,edicao,mes,editora)
                        self.estoque.append(item_atual)
                        break
                    case _:
                        print("\nInsira uma opção válida.")
                        continue

            print(f"\nSucesso no cadastro {"do livro" if item_atual.type=="Livro" else "da revista"} {item_atual.nome} (COD {item_atual.codigo})!")
            if pergunta("Deseja cadastrar outro produto?"):
                continue
            else:
                break

    def emprest_item(self, item, destino):
        destino.adicionar_item(item)        

class ItemBiblioteca:
    def __init__(self, codigo, nome, genero, possivel_empre=None, emprestado=False):
        self.codigo = codigo
        self.nome = nome
        self.genero = genero
        self.possivel_empre = possivel_empre
        self.emprestado = emprestado

    def __str__(self):
        return f"{self.codigo:^10} - {self.nome}"

class Livro(ItemBiblioteca):
    def __init__(self, codigo, nome, genero, autor, editora, ano, page_num, possivel_empre=None, emprestado=False):
        super().__init__(codigo, nome, genero, possivel_empre=None, emprestado=False)
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.page_num = page_num
        self.type = "Livro"


class Revista(ItemBiblioteca):
    def __init__(self, codigo, nome, genero, edicao, mes, editora, possivel_emprest = None, emprestado=False):
        super().__init__(codigo, nome, genero, possivel_emprest = None, emprestado=False)
        self.edicao = edicao
        self.mes = mes
        self.editora = editora
        self.type = "Revista"

def menu_biblioteca(biblioteca):
    while True:
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
                    sleep(1.5)
                    continue
                else:
                    print("Saindo da biblioteca...")
                    sleep(1.5)
                    break

            case "2":
                biblioteca.adicionar_item()

def main():
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

bibliotecas = [Biblioteca("Padrao", "1")]

def get_biblioteca(filial):
    for item in bibliotecas:
        if item.num_filial == filial:
            return item

main()