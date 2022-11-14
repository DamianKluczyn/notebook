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
            cur.execute('select login, password, id_account from public."Account"')

            rows = cur.fetchall()
            for r in rows:
             if r[0] == login and r[1] == passw:
                    self.id = r[2]
                    cur.close()
                    con.close()
                    return True
        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)
        finally:
            if con:
                cur.close()
                con.close()
                return False

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
        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)
        finally:
            if con:
                cur.close()
                con.close()
                return True

    def CreateNote(self):
        try:
            # Connect to database
            con = psycopg2.connect(
                host='localhost',
                database='note',
                user='postgres',
                password='290e47'
            )
            cur = con.cursor()

            title = input("Title od note: ")
            content = input("Note content: ")

            # Execute query
            cur.execute('insert into "Note" (title, content, id_account) values (%s, %s, %s)', (title, content, self.id))
            con.commit()
            print("Note added sucessfully")

        except(Exception, psycopg2.Error) as error:
            print("Error while fetchng data from PostgreSQL", error)

        finally:
            if con:
                cur.close()
                con.close()
                return False
