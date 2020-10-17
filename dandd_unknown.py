from tkinter import *
import sqlite3
import os


class MonsterDB:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __del__(self):
        self.commit()
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        # print("SQL: " + sql)
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        # print(sql)
        self.cursor.execute(sql, params or ())
        return self.fetchall()


root = Tk()
root.title("AD&D Monster/Treasure App")
root.iconbitmap(os.path.join(os.path.dirname(__file__), 'database.ico'))
root.geometry("400x620")
m_monsters = MonsterDB("dandd_monsters.db")


def AddRecord():
    m_name = m_Name.get()
    m_ac = int(m_AC.get())
    m_hp = int(m_HP.get())
    m_attack = int(m_Attacks.get())
    m_damage = m_Damage.get()
    m_thac0 = int(m_thaco.get())
    m_rm = m_room.get()
    m_isdead = (m_IsDead.get().lower() == 'true')
    m_monsters.execute("INSERT INTO monsters(mName, mAC, mHP, mAttack, mDamage, mthaco, mRoom, mIsDead) VALUES(:nm, :ac, :hp, :att, :dmg, :th0, :rm, :st)",
                       {
                           'nm': m_name, 'ac': m_ac, 'hp': m_hp, 'att': m_attack, 'dmg': m_damage,
                           'th0': m_thac0, 'rm': m_rm, 'st': m_isdead
                       }
                       )
    m_monsters.commit()
    print("Added...#" + str(m_monsters.query("SELECT COUNT(*) FROM monsters")))
    return


def ClearField():
    m_Name.delete(0, END)
    m_AC.delete(0, END)
    m_HP.delete(0, END)
    m_Attacks.delete(0, END)
    m_Damage.delete(0, END)
    m_thaco.delete(0, END)
    m_room.delete(0, END)
    m_IsDead.delete(0, END)
    tt_textResult.config(state=NORMAL)
    tt_textResult.delete(1.0, END)
    tt_textResult.config(state=DISABLED)
    return


def listMonster():
    mm_mRoom = m_room.get()
    m_room.delete(0, END)
    tt_textResult.config(state=NORMAL)
    tt_textResult.delete(1.0, END)
    if (len(mm_mRoom) != 0):
        tt_textResult.insert(END, "Monster in room: " + mm_mRoom + "\n")
        # print('wm' in mm_mRoom)
        if ('wm' in mm_mRoom):
            monst_records = m_monsters.query("SELECT * FROM monsters WHERE mRoom LIKE '" + mm_mRoom + "%'")
        elif ('*' in mm_mRoom):
            tt_textResult.insert(END, "Illegal search '*' \n")
            monst_records = ()
        else:
            monst_records = m_monsters.query("SELECT * FROM monsters WHERE mRoom=" + mm_mRoom)
        if (len(monst_records) > 0):
            for rec in monst_records:
                tt_textResult.insert(END, rec[1] + "|ac:" + str(rec[2]) + "|hp:" + str(rec[3]) + "|" + str(rec[4]) + "|" + rec[5] + "|" + str(rec[6]) + "|" + rec[7])
                if (rec[8] == 0):
                    tt_textResult.insert(END, "|alive\n")
                else:
                    tt_textResult.insert(END, "|dead\n")
        else:
            tt_textResult.insert(END, "None found")
    else:
        tt_textResult.insert(END, "ERR: No monster room given")
    tt_textResult.config(state=DISABLED)
    return


def killMonster():
    mm_mRoom = m_room.get()
    m_room.delete(0, END)
    tt_textResult.config(state=NORMAL)
    tt_textResult.delete(1.0, END)
    if (len(mm_mRoom) != 0):
        tt_textResult.insert(END, "Killing all monsters in room: " + mm_mRoom + "\n***\n******\n")
        m_monsters.execute("SELECT COUNT(*) FROM monsters WHERE mIsDead=0 AND mRoom='" + mm_mRoom + "'")
        monst_records = str(m_monsters.fetchone())
        m_monsters.execute("UPDATE monsters SET mIsDead=1 WHERE mRoom='" + mm_mRoom + "'")
        m_monsters.commit()
        tt_textResult.insert(END, monst_records + " monsters killed.\n")
        monst_records = str(m_monsters.query("SELECT SUM(mHp * 5) FROM monsters WHERE mRoom='" + mm_mRoom + "'"))
        tt_textResult.insert(END, monst_records + " experience gained total\n")
    else:
        tt_textResult.insert(END, "ERR: no room given")
    tt_textResult.config(state=DISABLED)
    return


def TreasAdd():
    mm_tName = m_tName.get()
    mm_tRoom = m_tRoom.get()
    mm_tPage = m_tPage.get()
    mm_tDesc = m_tDesc.get()
    mm_tFound = (m_tFound.get().lower() in ('t', 'true', 'yes', 'y'))
    # print(mm_tName)
    # print(mm_tRoom)
    # print(mm_tPage)
    # print(mm_tDesc)
    # print(mm_tFound)
    # print("\n")
    m_monsters.execute("INSERT INTO treasure (mName, mRoom, mPage, mDesc, mFound) \
        VALUES(:A, :B, :C, :D, :E)",
                       {
                           'A': mm_tName,
                           'B': mm_tRoom,
                           'C': mm_tPage,
                           'D': mm_tDesc,
                           'E': mm_tFound
                       }
                       )
    m_monsters.commit()
    # print("Added...#" + str(m_monsters.query("SELECT COUNT(*) FROM treasure")))
    return


def TreasClear():
    m_tName.delete(0, END)
    m_tRoom.delete(0, END)
    m_tPage.delete(0, END)
    m_tDesc.delete(0, END)
    m_tFound.delete(0, END)
    tt_textResult.config(state=NORMAL)
    tt_textResult.delete(1.0, END)
    tt_textResult.config(state=DISABLED)
    return


def TreasList():
    mt_room = m_tRoom.get()
    m_tRoom.delete(0, END)
    tt_textResult.config(state=NORMAL)
    tt_textResult.delete(1.0, END)
    if (len(mt_room) == 0):
        tt_textResult.insert(END, "ERR: No treasure room given")
        tt_textResult.config(state=DISABLED)
        return
    tt_textResult.insert(END, "Treasure in room: " + mt_room + "\n")
    m_monsters.execute("SELECT * FROM treasure WHERE mRoom=" + mt_room)
    recs = m_monsters.fetchall()
    if (len(recs) > 0):
        for rec in recs:
            tt_textResult.insert(END, rec[1] + "|" + rec[3] + "|" + rec[4])
            if (rec[5] == 0):
                tt_textResult.insert(END, "|notfound\n")
            else:
                tt_textResult.insert(END, "|found\n")
    else:
        tt_textResult.insert(END, "None found")
    tt_textResult.config(state=DISABLED)
    return


def TreasClaim():
    mt_room = m_tRoom.get()
    m_tRoom.delete(0, END)
    tt_textResult.config(state=NORMAL)
    tt_textResult.delete(1.0, END)
    if (len(mt_room) != 0):
        tt_textResult.insert(END, "Claiming treasure in room: " + mt_room + "\n")
        m_monsters.execute("SELECT COUNT(*) FROM treasure WHERE mFound=0 AND mRoom='" + mt_room + "'")
        recs = str(m_monsters.fetchone())
        m_monsters.execute("UPDATE treasure SET mFound=1 WHERE mRoom='" + mt_room + "'")
        m_monsters.commit()
        tt_textResult.insert(END, recs + " treasure items claimed\n")
    else:
        tt_textResult.insert(END, "ERR: No room given\n")
    tt_textResult.config(state=DISABLED)
    return


'''
c.execute("""CREATE TABLE monsters (
        mId INTEGER PRIMARY KEY AUTOINCREMENT,
        mName TEXT,
        mAC INT,
        mHP INT,
        mAttack INT,
        mDamage TEXT,
        mthaco INT,
        mRoom TEXT,
        mIsDead BOOL
    )""")
c.execute("""CREATE TABLE treasure (
        mId INTEGER PRIMARY KEY AUTOINCREMENT,
        mName TEXT,
        mRoom TEXT,
        mPage TEXT,
        mDesc TEXT,
        mFound BOOL
    )""")

conn.commit()
'''

# Create text entry fields for each database record. align entry boxes left
m_Name = Entry(root, width=30)
m_Name.grid(row=0, column=1, sticky=W)
m_AC = Entry(root, width=10)
m_AC.grid(row=1, column=1, sticky=W)
m_HP = Entry(root, width=10)
m_HP.grid(row=2, column=1, sticky=W)
m_Attacks = Entry(root, width=10)
m_Attacks.grid(row=3, column=1, sticky=W)
m_Damage = Entry(root, width=10)
m_Damage.grid(row=4, column=1, sticky=W)
m_thaco = Entry(root, width=10)
m_thaco.grid(row=5, column=1, sticky=W)
m_room = Entry(root, width=10)
m_room.grid(row=6, column=1, sticky=W)
m_IsDead = Entry(root, width=10)
m_IsDead.grid(row=7, column=1, sticky=W)

# Create labes for the GUI entry of the data, align lables right
l_Name = Label(root, text="Monster:")
l_Name.grid(row=0, column=0, sticky=E)
l_AC = Label(root, text="AC:")
l_AC.grid(row=1, column=0, sticky=E)
l_HP = Label(root, text="HP:")
l_HP.grid(row=2, column=0, sticky=E)
l_Attack = Label(root, text="#Attacks:")
l_Attack.grid(row=3, column=0, sticky=E)
l_Damage = Label(root, text="Damage (dice):")
l_Damage.grid(row=4, column=0, sticky=E)
l_thaco = Label(root, text="THAC0:")
l_thaco.grid(row=5, column=0, sticky=E)
l_Room = Label(root, text="In Room:")
l_Room.grid(row=6, column=0, sticky=E)
l_IsDead = Label(root, text="Dead (T/F)?:")
l_IsDead.grid(row=7, column=0, sticky=E)

m_addButton = Button(root, text="Add Monster", command=AddRecord)
m_addButton.grid(row=8, column=0, ipadx=40)
m_clearButton = Button(root, text="Clear Monster", command=ClearField)
m_clearButton.grid(row=8, column=1, ipadx=40)
m_listButton = Button(root, text="List Monsters", command=listMonster)
m_listButton.grid(row=9, column=0, columnspan=2, ipadx=135)
m_killButton = Button(root, text="Kill Monsters", command=killMonster)
m_killButton.grid(row=10, column=0, columnspan=2, ipadx=135)

# Treasure Fields
l_tName = Label(root, text="Treasure:")
l_tName.grid(row=11, column=0, sticky=E)
m_tName = Entry(root, width=20)
m_tName.grid(row=11, column=1, sticky=W)
l_tRoom = Label(root, text="Room:")
l_tRoom.grid(row=12, column=0, sticky=E)
m_tRoom = Entry(root, width=20)
m_tRoom.grid(row=12, column=1, sticky=W)
l_tPage = Label(root, text="Page#:")
l_tPage.grid(row=13, column=0, sticky=E)
m_tPage = Entry(root, width=20)
m_tPage.grid(row=13, column=1, sticky=W)
l_tDesc = Label(root, text="Desc:")
l_tDesc.grid(row=14, column=0, sticky=E)
m_tDesc = Entry(root, width=20)
m_tDesc.grid(row=14, column=1, sticky=W)
l_tFound = Label(root, text="Found(Y/n):")
l_tFound.grid(row=15, column=0, sticky=E)
m_tFound = Entry(root, width=20)
m_tFound.grid(row=15, column=1, sticky=W)

t_addButton = Button(root, text="Add Treasure", command=TreasAdd)
t_addButton.grid(row=16, column=0, ipadx=40)
t_clearButton = Button(root, text="Clear Treasure", command=TreasClear)
t_clearButton.grid(row=16, column=1, ipadx=40)
t_listButton = Button(root, text="List Treasure", command=TreasList)
t_listButton.grid(row=17, column=0, columnspan=2, ipadx=135)
t_claimButton = Button(root, text="Claim Treasure", command=TreasClaim)
t_claimButton.grid(row=18, column=0, columnspan=2, ipadx=135)

tt_textResult = Text(root, height=10, width=45)
tt_textResult.grid(row=19, column=0, columnspan=3, padx=10, pady=10)
tt_textResult.config(state=DISABLED)
root.mainloop()
