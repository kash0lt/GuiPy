from tkinter import *
import sqlite3
import os

# Databases
'''
# Create a database or connect to one
conn = sqlite3.connect('dvd_movies.db')

# Create cursor
c = conn.cursor()

# Create table

c.execute("""CREATE TABLE movies (
        id integer primary key autoincrement,
        moviename text,
        dvdnumber text,
        year text,
        genre text
        )""")

conn.commit()
conn.close()
'''
# Create Update function to update a record


class DvdMovie:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __del__(self):
        self._conn.commit()
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tbl):
        self._conn.commit()
        self._conn.close()

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self._conn.commit()

    def execute(self, sql, params=None):
        # print("SQL: " + sql)
        self._cursor.execute(sql, params or ())

    def fetchall(self):
        return self._cursor.fetchall()

    def fetchone(self):
        return self._cursor.fetchone()

    def query(self, sql, params=None):
        # print(sql)
        self._cursor.execute(sql, params or ())
        return self.fetchall()


root = Tk()
root.title('Kelly\'s DVD Movies App')
root.iconbitmap(os.path.join(os.path.dirname(__file__), 'database.ico'))
root.geometry("480x400")
m_DvdMovie = DvdMovie("dvd_movies.db")


def AddDvdMovie():
    mm_title = m_title.get()
    mm_index = m_index.get()


l_title = Label(root, text="Dvd Title:")
l_title.grid(row=1, column=0, sticky=E)
m_title = Entry(root, width=60)
m_title.grid(row=1, column=1, sticky=W)
l_index = Label(root, text="dvd index:")
l_index.grid(row=2, column=0, sticky=E)
m_index = Entry(root, width=60)
m_index.grid(row=2, column=1, sticky=W)

# Now we need the event loop 'mainloop' for the root 'screen'
root.mainloop()
