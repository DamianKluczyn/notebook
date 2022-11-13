class loginMenu:
    def __init__(self):
        self.done = True
    def menu(self):
        option = 5
        while(self.done):
            print("LOGIN MENU")
            print("1. Login")
            print("2. Register")
            print("0. Exit")
            option = input("Choose: ")
            match option:
                case "1":
                    #LOGOWANIE
                    print("logowanie")
                    self.done = False
                case "2":
                    print("rejestracja")
                    #REGISTER
                    self.done = False
                case "0":
                    print("Exiting program...")
                    exit(0)
                case _:
                    print("Choose option correctly")

class noteMenu:
    def __init__(self):
        self.done = True
    def menu(self):
        option = 5
        while(self.done):
            print("NOTE MENU")
            print("1. Create")
            print("2. Read")
            print("3. Update")
            print("4. Delete")
            print("0. Exit")
            option = input("Choose: ")
            match option:
                case "1":
                    print("c")
                    # CREATE
                    self.done = False
                case "2":
                    print("r")
                    # READ
                    self.done = False
                case "3":
                    print("u")
                    # UPDATE
                    self.done = False
                case "4":
                    print("d")
                    # DELETE
                    self.done = False
                case "0":
                    print("Exiting program...")
                    exit(0)
                case _:
                    print("Choose option correctly")