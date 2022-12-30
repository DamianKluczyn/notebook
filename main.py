import psycopg2
import bcrypt

class logged_user:
    def __init__(self, login):
        self.login = login
    def getlogin(self):
        return self.login

class database_connection:
    def __init__(self):
        self.con = psycopg2.connect(
            host='localhost',
            database='note',
            user='postgres',
            password='290e47'
        )
        self.cur = self.con.cursor()

class hash:
    def __init__(self, password):
        self.password = password.encode('utf-8')
        self.salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(self.password, self.salt)

    def get_hashed_password(self):
        return self.hashed_password

class user_exist(database_connection):
    def __init__(self, login):
        self.login = login
        super().__init__()

    def check(self):
        super().cur.execute('select count(*) from "Account" where login = %s', (self.login,))
        if (super().cur.fetchone() == 0):
            return False
        return True

class register(database_connection):
    def __init__(self):
        super().__init__()
        self.login, self.passw, self.fname, self.lname, self.exist = ""

    def register(self):
        self.login = input("\nLogin: ").lower()
        self.passw = input("Password: ")
        self.fname = input("First name: ").lower().capitalize()
        self.lname = input("Last name: ").lower().capitalize()
        self.exist = user_exist(self.login)
        if(not self.exist.check()):
            self.passw = hash(self.passw)
            super().cur.execute('insert into "Account" (login, password, fname, lname) values (%s, %s, %s, %s)',
                         (self.login, self.passw, self.fname, self.lname))
            super().con.commit()
            print("\nUser registered succesfully!\n")
            return True
        print("\nRegistration failed!\n")
        return False

class login(database_connection):
    def __init__(self):
        super().__init__()
        self.login, self.passw, self.exist = ""
    def login(self):
        self.login = input("\nLogin: ").lower()
        self.passw = input("Password: ")
        self.exist = user_exist(self.login())
        if(self.exist.check()):
            super().cur.execute('select login, password from "Account" where login = %s', (self.login,))
            rows = super().cur.fetchone()
            if(bcrypt.checkpw(self.passw.encode('utf-8'),rows[1].encode('utf-8')) == True):
                return True
            print("Zle haslo!")
        return False

class create_note(database_connection):
    def __init__(self):
        super().__init__()
    def create_note(self, user):
        title = input("Title: ")
        content = input("Content: ")

        super().cur.execute('select title, id_account from "Note"')

        rows = super().cur.fetchall()
        for r in rows:
            if r[0] == title and r[1] == self.id:
                return False

        super().cur.execute('insert into "Note" (title, content, login) values (%s, %s, %s)', (title, content, user.getlogin()))
        super().con.commit()
        print("Notatka dodana pomyslnie")
        return

class read_note(database_connection):
    def __init__(self):
        super().__init__()
    def read_note(self, user):
        # Check if any note exist
        super().cur.execute('select count(*) from "Note" where login = %s', (user.getlogin(),))
        if (super().cur.fetchone() == 0):
            print("Nie masz zadnej notatki")
            return

        super().cur.execute('select title, content, login from "Note" where login = %s', (user.getlogin(),))

        rows = super().cur.fetchall()
        counter = 0
        for r in rows:
            counter += 1
            print(f"{counter}. {r[0]}")
        while (True):
            choose = int(input("Choose number of note: "))
            if (choose < 1 or choose > counter):
                print("Choose correct number")
            else:
                break

        print(f"""\nTitle: {r[0]}\n{r[1]}\n""")
        input("Press Enter to continue...")
        super().con.commit()
        return

class update_note(database_connection):
    def __init__(self):
        super().__init__()
    def update_note(self, user):
        super().cur.execute('select count(*) from "Note" where login = %s', (user.getlogin(),))
        if (super().cur.fetchone() == 0):
            print("You dont have any notes yet")
            return

        super().cur.execute('select title, content, login, id_note from "Note" where login = %s', (user.getlogin,))

        rows = super().cur.fetchall()
        counter = 0
        for r in rows:
            counter += 1
            print(f"{counter}. {r[0]}")
        while (True):
            choose = int(input("Choose number of note: "))
            if (choose < 1 or choose > counter):
                print("Choose correct number")
            else:
                break

        id_note = rows[choose - 1][3]
        title = input("New title: ")
        content = input("New content: ")
        super().cur.execute('update "Note" set title = %s, content = %s where id_note = %s', (title, content, id_note))
        super().con.commit()
        print("Notatka pomyslnie zmieniona")
        return
class delete_note(database_connection):
    def __init__(self):
        super().__init__()
    def delete_note(self,user):
        super().cur.execute('select count(*) from "Note" where login = %s', (user.getlogin(),))
        if (super().cur.fetchone() == 0):
            print("You dont have any notes yet")
            return

        super().cur.execute('select title, content, id_account, id_note from "Note" where login = %s', (user.getlogin(),))

        rows = super().cur.fetchall()
        counter = 0
        for r in rows:
            counter += 1
            print(f"{counter}. {r[0]}")
        while (True):
            choose = int(input("Choose number of note: "))
            if (choose < 1 or choose > counter):
                print("Choose correct number")
            else:
                break

        id_note = rows[choose - 1][3]
        super().cur.execute('delete from "Note" where id_note = %s', (id_note,))
        super().con.commit()
        print("Notatka pomyslnie usunieta")
        return
class start_menu:
    def __init__(self):
        self.choice = ""
    def start(self):
        print("LAB 4 NOTEBOOK")
        while True:
            self.choice = int(input("""
            Choose an option:
            1. Login
            2. Register
            0. Exit
            """))
            match self.choice:
                case 1:
                    register().register()
                case 2:
                    log = login().login()
                    if log:
                        note_menu(log)
                case 0:
                    exit(0)

class note_menu:
    def __init__(self, log):
        self._user = logged_user(log)
        self.choice = ""

    def start(self):
        print("NOTEBOOK MENU")
        while True:
            self.choice = int(input("""
            Choose an option:
            1. Create
            2. Read 
            3. Update
            4. Delete
            0. Exit
            """))
            match self.choice:
                case 1:
                    create_note.create_note(self._user)
                case 2:
                    read_note.read_note(self._user)
                case 3:
                    update_note.update_note(self._user)
                case 4:
                    delete_note.delete_note(self._user)
                case 0:
                    exit(0)

if __name__ == '__main__':
    start = start_menu()
    start.start()

