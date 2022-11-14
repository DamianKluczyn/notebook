from dbScripts import *
class loginMenu:
    db = db()
    def __init__(self):
        self.done = True
    def menu(self):
        menuOption = 5
        while(self.done):
            print("LOGIN MENU")
            print("1. Login")
            print("2. Register")
            print("0. Exit")
            menuOption = input("Choose: ")
            match menuOption:
                case "1":
                    if(not self.db.Login()):
                        print("Login failed")
                    else:
                        print("Login succesfull!")
                        self.done = False
                case "2":
                    if (not self.db.Register()):
                        print("Register failed")
                    else:
                        print("Register succesfull!")
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
        menuOption = 5
        while(self.done):
            print("NOTE MENU")
            print("1. Create")
            print("2. Read")
            print("3. Update")
            print("4. Delete")
            print("0. Exit")
            menuOption = input("Choose: ")
            match menuOption:
                case "1":

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