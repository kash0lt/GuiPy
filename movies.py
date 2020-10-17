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
        rating text,
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
root.geometry("500x320")
m_DvdMovie = DvdMovie("dvd_movies.db")


def AddDvdMovie():
    mm_title = m_title.get()  # Get all values from entry fields and save to db
    mm_index = m_index.get()
    mm_year = m_year.get()
    mm_genre = m_genre.get()
    mm_rating = m_rating.get()
    m_DvdMovie.execute("INSERT INTO movies(moviename, dvdnumber, year, genre) VALUES(:mn, :dn, :my, :mg, :mr)",
                       {
                           'mn': mm_title, 'dn': mm_index, 'my': mm_year, 'mg': mm_genre, 'mr': mm_rating
                       }
                       )
    m_DvdMovie.commit()
    # Clear entry fields
    m_title.delete(0, END)
    m_index.delete(0, END)
    m_year.delete(0, END)
    m_genre.delete(0, END)
    m_rating.delete(0, END)
    t_textResult.config(state=NORMAL)
    t_textResult.delete(1.0, END)
    t_textResult.insert(END, "Movie has been added\n")
    t_textResult.config(state=DISABLED)
    return


l_title = Label(root, text="DVD Title:")
l_title.grid(row=1, column=0, sticky=E)
m_title = Entry(root, width=60)
m_title.grid(row=1, column=1, sticky=W)
l_index = Label(root, text="DVD index:")
l_index.grid(row=2, column=0, sticky=E)
m_index = Entry(root, width=60)
m_index.grid(row=2, column=1, sticky=W)
l_year = Label(root, text="Year:")
l_year.grid(row=3, column=0, sticky=E)
m_year = Entry(root, width=20)
m_year.grid(row=3, column=1, sticky=W)
l_genre = Label(root, text="Genre:")
l_genre.grid(row=4, column=0, sticky=E)
m_genre = Entry(root, width=20)
m_genre.grid(row=4, column=1, sticky=W)
l_rating = Label(root, text="Rating:")
l_rating.grid(row=5, column=0, sticky=E)
m_rating = Entry(root, width=20)
m_rating.grid(row=5, column=1, sticky=W)
b_addButton = Button(root, text="Add Movie info", command=AddDvdMovie)
b_addButton.grid(row=6, column=1, ipadx=40)
t_textResult = Text(root, height=10, width=45)
t_textResult.grid(row=19, column=0, columnspan=3, padx=10, pady=10)
t_textResult.config(state=DISABLED)

# Now we need the event loop 'mainloop' for the root 'screen'
root.mainloop()
