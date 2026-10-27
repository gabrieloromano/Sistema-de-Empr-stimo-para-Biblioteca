import os
from time import sleep
import json
import subprocess

save_path = "C:\\ProgramData\\Librarys\\"

opt_rent = ["[1] Register Rental Store",
           "[2] Access Rental Store",
           "[3] Quit"]

opt_item = ["[1] List items",
           "[2] Register new item",
           "[3] Rent item",
           "[4] Return item",
           "[5] Return to menu"]

class CustomError(Exception):
    def __init__(self, message):
        self.message=message

    def __str__(self):
        return f"\nErro: {self.message}"

def get_item(searched, list_search, variable=None):
    if variable:
        for item in list_search:
            if getattr(item, f"{variable}") == searched:
                return item
            else:
                continue
        raise CustomError("Sorry! We couldn't find what you're searching for. Please try again!")
    else:
        for item in list_search:
            if item == searched:
                return item
            else:
                continue
        raise CustomError("Sorry! We couldn't find what you're searching for. Please try again!")

def regress_count(time):
    for t in range(time, 0 , -1):
        print(t)
        sleep(1)
    subprocess.run("cls", shell=True)

def question(message):
    while True:
        menu = input(f"\n{message}\n[1] Yes\n[2] No\n\nChoice: ").lower()
        match menu:
            case "1" | "yes":
                return True
            case "2" | "no":
                return False
            case _:
                print("\nInsert a valid option.")
                continue

class RentStore:
    def __init__(self, name, filial_number):
        self.name = name
        self.filial_number = str(filial_number)
        self.stock_dict = []
        self.path = f"{save_path}{f"{self.filial_number} - {self.name}"}.json"
        if not os.path.isfile(self.path):
            file = open(self.path, "w")
            file.write("[]")
            file.close()
            self.stock = []
        else:
            self.stock = self.load_storage()
        
    def __str__(self):
        return f"{"[" + self.filial_number + "] " + self.name:^50}"

    def list_items(self, num_param):
        media_types = ["Book", "Magazine", "DVD"]
        print(f"\n{[item for item in self.stock if item.media_type == media_types[num_param-1]] if num_param != 4 else [item for item in self.stock]}")

    def load_storage(self):
        self.stock_dict = []
        internal_list = []
        if os.path.isfile(self.path):
            file = open(self.path, "r")
            self.stock_dict = json.load(file)
            for prod in self.stock_dict:
                internal_list.append(Book(**prod) if prod["media_type"] == "Book" else Magazine(**prod) if prod["media_type"] == "Magazine" else DVD(**prod))
            return internal_list
        return []

    def save_storage(self):
        self.stock_dict = []
        file = open(self.path, "w")
        for item in self.stock:
            self.stock_dict.append(item.__dict__)
        json.dump(self.stock_dict, file)
        file.close()

    def add_item(self, item):
        self.stock.append(item)
        return

    def rent_item(self, item):
        if not item.can_rent:
            raise CustomError("This item is already rented! Please choose a valid item.")
        item.can_rent = False

    def return_item(self, item):
        if item.can_rent:
            raise CustomError("This item is not rented! Please choose a valid item to return.")
        item.can_rent = True

    def has_rentable_items(self):
        if len([item for item in self.stock if item.can_rent]) < 1:
            return False
        return True

    def has_returnable_items(self):
        if len([item for item in self.stock if not item.can_rent]) < 1:
            return False
        return True

class Media:
    def __init__(self, code, name, genre, media_type=None, rented_time=None, can_rent=True, max_renting=14):
        self.code = code
        self.name = name
        self.genre = genre
        self.media_type = media_type
        self.rented_time = rented_time
        self.can_rent = can_rent
        self.max_renting = max_renting
        
    def __str__(self):
        return f"{self.code} - {self.name} - {"Available" if self.can_rent else "Rented"}"

    def __repr__(self):
        return f"{self.code} - {self.name} - {"Available" if self.can_rent else "Rented"}"

class Book(Media):
    def __init__(self, code, name, genre, author, publisher, year, page_num, rented_time=None, can_rent=True, media_type="Book", max_renting=14):
        super().__init__(code=code, name=name, genre=genre, media_type=media_type, rented_time=rented_time, can_rent=can_rent, max_renting=max_renting)
        self.author = author
        self.publisher = publisher
        self.year = year
        self.page_num = page_num

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()

class Magazine(Media):
    def __init__(self, code, name, genre, edition, month, publisher, rented_time=None, can_rent=True, media_type="Magazine", max_renting=7):
        super().__init__(code=code, name=name, genre=genre, media_type=media_type, rented_time=rented_time, can_rent=can_rent, max_renting=max_renting)
        self.edition = edition
        self.month = month
        self.publisher = publisher

    def __str__(self):
        return f"{self.code:^10} - {self.name} Edition {self.edition}  - {self.month} - Publisher {self.publisher} - {"Available" if self.can_rent else "Rented"}"

    def __repr__(self):
        return f"{self.code:^10} - {self.name} Edition {self.edition}  - {self.month} - Publisher {self.publisher} - {"Available" if self.can_rent else "Rented"}"

class DVD(Media):
    def __init__(self, code, name, genre, length, director, year, rented_time=None, can_rent=True, media_type="DVD", max_renting=14):
        super().__init__(code=code, name=name, genre=genre, media_type=media_type, rented_time=rented_time, can_rent=can_rent, max_renting=max_renting)
        self.length = length
        self.director = director
        self.year = year

    def __str__(self):
        return f"{self.code:^10} - {self.name} - {self.length} min - {self.director} - {self.year} - {"Available" if self.can_rent else "Rented"}"

    def __repr__(self):
            return f"{self.code:^10} - {self.name} - {self.length} min - {self.director} - {self.year} - {"Available" if self.can_rent else "Rented"}"

def rent_menu(rentstore):
    while True:
        rentstore.save_storage()
        print(f"{rentstore.name:=^50}")

        for op in opt_item:
            print(f"{op:^50}\n")

        select = input("\nSelect a option: ")

        match select:
            case "1":
                if len(rentstore.stock) < 1:
                    print("\nThere is no available items on this Rental Store, returning to the menu...")
                    regress_count(3)
                    continue

                print(f"\n{"ITEMS LIST":=^50}\n")
                print("[1] List Books\n" \
                        "[2] List Magazines\n" \
                        "[3] List DVDs\n" \
                        "[4] List All Medias\n") \
        
                media_select = int(input("Choose your option: "))

                rentstore.list_items(media_select)
                
                if question("Do you wish to return to the menu?"):
                    print("\nReturning to menu...")
                    regress_count(3)
                    continue
                else:
                    print("Leaving rent menu...")
                    regress_count(3)
                    break
            case "2":
                while True:
                    print(f"\n{"ITEM REGISTRATION":=^50}\n")
                    current_item = None
                    item_type = None
                    code = input("\nInsert a code for the new item: ").strip()
                    name = input("\nInsert the new item name: ")
                    genre = input("\nInsert the new item genre: ")
        
                    while True:
                        select = input("\nChoose the item type\n" \
                        "[1] Book\n" \
                        "[2] Magazine\n" \
                        "[3] DVD\n" \
                        "Choice: ").lower()
        
                        match select:

                            case "1" | "book":
                                author = input("\nInsert the book author: ")
                                publisher = input("\nInsert the book publisher: ")
                                year = input("\nInsert the book release year:  ")
                                page_num = int(input("\nInsert the book number of pages:  "))
        
                                current_item = Book(code,name,genre,author,publisher,year,page_num)
                                item_type = "Book"
                                break

                            case "2" | "magazine":
                                edition = input("\nInsert the edition number: ")
                                month = input("\nInsert the release month: ")
                                publisher = input("\nInsert the publisher's name: ")
        
                                current_item = Magazine(code,name,genre,edition,month,publisher)
                                item_type = "Magazine"
                                break

                            case "3" | "dvd":
                                length = input("\nInsert the DVD's length (in minutes): ")
                                director = input("\nInsert the DVD director's name: ")
                                year = input("\nInsert the DVD's release year: ")

                                current_item = DVD(code,name,genre, length, director, year)
                                item_type = "DVD"
                                break
                            case _:
                                print("\nChoose a valid option.")
                                continue

                    rentstore.add_item(current_item)
                    print(f"\nSuccess registering the {item_type} {current_item.name} (COD {current_item.code})!")
                    if question("Do you wish to register another item?"):
                        continue
                    else:
                        print("Returning to menu...")
                        regress_count(3)
                        break
            case "3":
                while True:
                    if not rentstore.has_rentable_items():
                        print("There is no available items for renting, returning to menu...")
                        regress_count(3)
                        break    
                    
                    print(f"\n{"ITEM RENTING":=^50}\n")

                    print("\nChoose the item you wish to rent: \n")
                    for item in rentstore.stock:
                        if item.can_rent:
                            print(item)

                    try:
                        user_input = input('\nInsert the code of the item you wish to rent, or type "Quit" to cancel: ')
                        
                        if user_input.lower() == "quit":
                            print("\nReturning to menu...")
                            regress_count(3)
                            break

                        cod_item = get_item(user_input, rentstore.stock, "code")

                        if cod_item == None:
                            print("The code you typed doesn't exist, please try again!\n")
                            regress_count(3)
                            continue

                        rentstore.rent_item(cod_item)
                        print("Success on renting the item!")

                    except Exception as e:
                        print(e)
                        break

                    if question("Do you wish to rent another item?"):
                        continue
                    else:
                        print("Returning to menu...")
                        regress_count(3)
                        break

            case "4":
                while True:
                    print(f"\n{"RETURN ITEM":=^50}\n")
                    
                    if not rentstore.has_returnable_items():
                        print("There is no available items to return, returning to menu...")
                        regress_count(3)
                        break

                    print('\nChoose the item you wish to return: \n')
                    for item in rentstore.stock:
                        if not item.can_rent:
                            print(item)

                    try:
                        user_input = input('\nInsert the code of the item you wish to return, or type "Quit" to cancel: ')

                        if user_input.lower() == "quit":
                            print("\nReturning to menu...")
                            regress_count(3)
                            break

                        cod_item = get_item(user_input, rentstore.stock, "code")

                        if cod_item == None:
                            print("The code you typed doesn't exist, please try again!\n")
                            regress_count(3)
                            continue
                        
                        rentstore.return_item(cod_item)
                        print("Success on returning the item!")

                    except Exception as e:
                        print(e)
                        break

                    if question("Do you wish to return another item?"):
                        continue
                    else:
                        print("Returning to menu...")
                        regress_count(3)
                        break

            case "5":
                print("\nReturning to menu...")
                regress_count(3)
                break

def load_library():
    internal_list = []
    for item in os.listdir(save_path):
        if item.endswith(".json"):
            filial, name = item.strip().split("-")
            name = name.strip()
            internal_list.append(RentStore(name.removesuffix(".json"), filial.strip()))
    return internal_list

rentalstores = load_library()

def main():
    while True:
        print(f"{" RENT SYSTEM ":=^50}\n")
        for b in opt_rent:
            print(f"{b:^50}\n")

        select = int(input("Choose an option: "))

        match select:
            case 1:
                while True:
                    name = input("\nInsert the new Rental Store name: ")
                    if "-" in name:
                        print("\nThe character '-' isn't supported, please insert another name!")
                        continue
                    filial = int(input("\nPlease insert the filial number of the new Rental Store: "))
                    rentalstores.append(RentStore(name, filial))
                    if question("Do you wish to register a new Rental Store?"):
                        continue
                    else:
                        print("\nReturning to menu...")
                        regress_count(3)
                        break

            case 2:
                if len(rentalstores) <= 0:
                    print("\nThere is no available Rental Stores to access. Returning to menu...\n")
                    regress_count(3)
                    continue
                print(f"\n{" AVAILABLE RENTAL STORES ":=^50}\n")
                for b in rentalstores:
                    print(b)
                filial_choice = input("\nChoose the Rental Store you want to access: ")

                bibl = get_item(filial_choice, rentalstores, "filial_number")

                rent_menu(bibl)

            case 3:
                print("\nClosing the program...")
                regress_count(3)
                break

main()