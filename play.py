from tkinter import *
import sqlite3
import os


root = Tk()
root.title('Kelly\'s Wonder App')
root.iconbitmap(os.path.join(os.path.dirname(__file__), 'database.ico'))
root.geometry("400x400")

root.mainloop()
