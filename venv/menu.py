from dbScripts import *
class Menu:
    db = db()
    def __init__(self):
        self.done = True
    def loginMenu(self):
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
                        input("\nPress Enter to continue...\n")
                    else:
                        print("Login succesfull!")
                        input("\nPress Enter to continue...\n")
                        self.done = False
                case "2":
                    if (not self.db.Register()):
                        print("Register failed")
                        input("\nPress Enter to continue...\n")
                    else:
                        print("Register succesfull!")
                        input("\nPress Enter to continue...\n")
                        self.done = False
                case "0":
                    print("Exiting program...")
                    exit(0)
                case _:
                    print("Choose option correctly")
    def noteMenu(self):
        self.done = True
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
                    if(not self.db.CreateNote()):
                        print("Note with same title already exist in your account")
                        input("\nPress Enter to continue...\n")
                    else:
                        print("Note created successfully")
                        input("\nPress Enter to continue...\n")
                case "2":
                    if(not self.db.ReadeNote()):
                        print("You dont have any notes yet")
                        input("\nPress Enter to continue...\n")
                case "3":
                    if(not self.db.UpdateNote()):
                        continue
                    else:
                        print("Note updated successfully")
                        input("\nPress Enter to continue...\n")
                case "4":
                    print("d")
                    # DELETE
                case "0":
                    print("Exiting program...")
                    exit(0)
                case _:
                    print("Choose option correctly\n")