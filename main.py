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
            database='note',
            user='postgres',
            password='290e47'
        )
        self.cur = self.con.cursor()

class hash:
    def __init__(self, password):
        self.password = password.encode('utf-8')
        self.salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(self.password, self.salt).decode('utf-8')

    def get_hashed_password(self):
        return self.hashed_password

class user_exist(database_connection):
    def __init__(self, login):
        super().__init__()
        self.login = login

    def check(self):
        self.cur.execute('select count(*) from "Account" where login = %s;', (self.login,))
        in_base = self.cur.fetchone()
        if (in_base[0] == 1):
            return False
        return True

class register(database_connection):
    def __init__(self):
        self.login, self.passw, self.fname, self.lname, self.exist = " ", " ", " ", " ", " "
        super().__init__()

    def register(self):
        self.login = input("\nLogin: ").lower()
        self.passw = input("Password: ")
        self.fname = input("First name: ").lower().capitalize()
        self.lname = input("Last name: ").lower().capitalize()
        self.exist = user_exist(self.login)
        if(self.exist.check()):
            self.passw = hash(self.passw)
            self.cur.execute('insert into "Account" (login, password, fname, lname) values (%s, %s, %s, %s);',
                         (self.login, self.passw.get_hashed_password(), self.fname, self.lname))
            self.con.commit()
            print("\nUser registered succesfully!\n")
            return True
        print("\nRegistration failed!\n")
        return False

class login(database_connection):
    def __init__(self):
        self.login = input("\nLogin: ").lower()
        self.passw = input("Password: ")
        self.exist = False
        super().__init__()
    def getLogin(self):
        return self.login
    def sign(self):
        self.exist = user_exist(self.login)
        if(not self.exist.check()):
            self.cur.execute('select password from "Account" where login = %s;', (self.login,))
            rows = self.cur.fetchone()
            if(bcrypt.checkpw(self.passw.encode('utf-8'),rows[0].encode('utf-8')) == True):
                return True
        return False

class create_note(database_connection):
    def __init__(self):
        super().__init__()
    def create_note(self, user):
        title = input("Title: ")
        content = input("Content: ")

        self.cur.execute('select id_account from "Account" where login = %s;',(user,))
        rows = self.cur.fetchone()
        id = rows[0]

        self.cur.execute('select title, id_account from "Note";')
        rows = self.cur.fetchall()
        for r in rows:
            if r[0] == title and r[1] == id:
                return False

        self.cur.execute('insert into "Note" (title, content, id_account) values (%s, %s, %s)', (title, content, id))
        self.con.commit()
        print("Notatka dodana pomyslnie")
        return

class read_note(database_connection):
    def __init__(self):
        super().__init__()
    def read_note(self, user):

        self.cur.execute('select id_account from "Account" where login = %s;', (user,))
        rows = self.cur.fetchone()
        id = rows[0]

        self.cur.execute('select count(*) from "Note" where id_account = %s;', (id,))
        if (self.cur.fetchone() == 0):
            print("Nie masz zadnej notatki")
            return

        self.cur.execute('select title, content, id_account from "Note" where id_account = %s;', (id,))

        rows = self.cur.fetchall()
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
        self.con.commit()
        return

class update_note(database_connection):
    def __init__(self):
        super().__init__()
    def update_note(self, user):
        self.cur.execute('select count(*) from "Note" where login = %s;', (user,))
        if (self.cur.fetchone() == 0):
            print("You dont have any notes yet")
            return

        self.cur.execute('select title, content, login, id_note from "Note" where login = %s;', (user,))

        rows = self.cur.fetchall()
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
        self.cur.execute('update "Note" set title = %s, content = %s where id_note = %s;', (title, content, id_note))
        self.con.commit()
        print("Notatka pomyslnie zmieniona")
        return
class delete_note(database_connection):
    def __init__(self):
        super().__init__()
    def delete_note(self,user):
        self.cur.execute('select count(*) from "Note" where login = %s;', (user,))
        if (self.cur.fetchone() == 0):
            print("You dont have any notes yet")
            return

        self.cur.execute('select title, content, id_account, id_note from "Note" where login = %s;', (user,))

        rows = self.cur.fetchall()
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
        self.cur.execute('delete from "Note" where id_note = %s;', (id_note,))
        self.con.commit()
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
            if self.choice == 1:
                log = login()
                if log.sign():
                    note = note_menu(log.getLogin())
                    note.start()
                else:
                    print("Zly login lub haslo!")
            elif self.choice == 2:
                register().register()
            elif self.choice == 0:
                break

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
            if self.choice == 1:
                create = create_note()
                create.create_note(self._user.getlogin())
            elif self.choice == 2:
                read = read_note()
                read.read_note(self._user.getlogin())
            elif self.choice == 3:
                update = update_note()
                update.update_note(self._user.getlogin())
            elif self.choice == 4:
                delete = delete_note()
                delete.delete_note(self._user.getlogin())
            elif self.choice == 0:
                break

if __name__ == '__main__':
    start = start_menu()
    start.start()

