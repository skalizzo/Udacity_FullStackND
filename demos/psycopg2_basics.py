import psycopg2

class psycopg2_basic_examples():
    def create_table(self):
        conn = psycopg2.connect("dbname='todoapp_development' user='postgres' host='localhost' password='Postgresisamotherfucker01'")

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # drop any existing todos table
        cur.execute("DROP TABLE IF EXISTS todos;")

        # (re)create the todos table
        # (note: triple quotes allow multiline text in python)
        cur.execute("""
          CREATE TABLE todos (
            id serial PRIMARY KEY,
            description VARCHAR NOT NULL
          );
        """)

        # commit, so it does the executions on the db and persists in the db
        conn.commit()
        cur.close()
        conn.close()

    def insert_records(self):
        conn = psycopg2.connect(
            "dbname='todoapp_development' user='postgres' host='localhost' password='Postgresisamotherfucker01'")
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS table2;')

        cur.execute('''
          CREATE TABLE table2 (
            id INTEGER PRIMARY KEY,
            completed BOOLEAN NOT NULL DEFAULT False
          );
        ''')

        cur.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

        SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

        data = {
            'id': 2,
            'completed': False
        }
        cur.execute(SQL, data)

        conn.commit()
        cur.close()
        conn.close()


    def fetch_results(self):
        conn = psycopg2.connect(
            "dbname='todoapp_development' user='postgres' host='localhost' password='Postgresisamotherfucker01'")
        cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM table2;")
        result = cur.fetchall()
        print(result)
        cur.close()
        conn.close()

if __name__ == '__main__':
    basics = psycopg2_basic_examples()
    basics.create_table()
    basics.insert_records()
    basics.fetch_results()