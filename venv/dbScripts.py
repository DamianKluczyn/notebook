import psycopg2

class db:
    def __init__(self):
        self.id = ""

    def Login(self):
        try:
            con = psycopg2.connect(
                host='localhost',
                database='note',
               user='postgres',
               password='290e47'
            )

            login = input("Login: ")
            passw = input("Password: ")

            cur = con.cursor()
            cur.execute('select login, password, id_account from "Account"')

            rows = cur.fetchall()
            for r in rows:
                if r[0] == login and r[1] == passw:
                    self.id = r[2]
                    cur.close()
                    con.close()
                    return True
            cur.close()
            con.close()
            return False

        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)


    def Register(self):
        try:
            #Connect to database
            con = psycopg2.connect(
                host='localhost',
                    database='note',
                user='postgres',
                password='290e47'
            )

            login = input("Login: ")
            passw = input("Password: ")
            name = input("Name: ")

            #Create cursor
            cur = con.cursor()

            #Execute query
            cur.execute('select login from public."Account"')

            #Check if login already exist in database
            rows = cur.fetchall()
            for r in rows:
               if r[0] == login:
                   cur.close()
                   con.close()
                   return False

            cur.execute('insert into public."Account" (login, password, name) values (%s, %s, %s)', (login, passw, name))

            cur.execute('SELECT id_account, login FROM "Account" WHERE login = %s', (login,))
            rows = cur.fetchone()
            self.id = rows[0]

            # Commit changes
            con.commit()

            cur.close()
            con.close()
            return True
        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)



    def CreateNote(self):
        try:
            # Connect to database
            con = psycopg2.connect(
                host='localhost',
                database='note',
                user='postgres',
                password='290e47'
            )
            # Open cursor
            cur = con.cursor()

            title = input("Title od note: ")
            content = input("Note content: ")

            # Execute query
            cur.execute('select title, id_account from "Note"')

            # Check if login already exist in database
            rows = cur.fetchall()
            for r in rows:
                if r[0] == title and r[1] == self.id:
                    cur.close()
                    con.close()
                    return False

            # Execute query
            cur.execute('insert into "Note" (title, content, id_account) values (%s, %s, %s)', (title, content, self.id))

            # Commit changes
            con.commit()

            # Close cursor and db
            cur.close()
            con.close()
            return True
        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)
    def ReadeNote(self):
        try:
            # Connect to database
            con = psycopg2.connect(
                host='localhost',
                database='note',
                user='postgres',
                password='290e47'
            )
            cur = con.cursor()

            # Check if any note exist
            cur.execute('select count(*) from "Note" where id_account = %s', (self.id,))
            if (cur.fetchone() == 0):
                return False

            # Execute query
            cur.execute('select title, content, id_account from "Note" where id_account = %s', (self.id,))

            # Check if login already exist in database
            rows = cur.fetchall()

            counter = 0
            for r in rows:
                counter += 1
                print(f"{counter}. {r[0]}")
            while(True):
                choose = int(input("Choose number of note: "))
                if (choose < 1 or choose > counter):
                    print("Choose correct number")
                else:
                    break

            print(f"""\nTitle: {r[0]}\n{r[1]}\n""")

            input("Press Enter to continue...")

            con.commit()

            cur.close()
            con.close()
            return True

        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)
