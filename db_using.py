import sqlite3


def connect():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, title VARCHAR, task VARCHAR, done BOOLEAN)")
    conn.commit()
    conn.close()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def add(title,task):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("INSERT INTO todo (title, task, done) VALUES(?,?,?)", (title,task,False))
    conn.commit()
    conn.close()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def view_all():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    conn.close()
    return rows

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def view_undone():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo WHERE done=0")
    all_rows = cur.fetchall()
    rows=[]
    for row in all_rows:
        if row[-1] == 0:
            rows.append(row)
    conn.close()
    return rows

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def view_done():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo WHERE done=1")
    all_rows = cur.fetchall()
    rows=[]
    for row in all_rows:
        if row[-1] == 1:
            rows.append(row)
    conn.close()
    return rows

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def view_one(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo WHERE id=?", (id))
    rows = cur.fetchone()
    conn.close()
    return rows

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def get_task(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo WHERE id=?", (id))
    rows = cur.fetchall()
    conn.close()
    return rows

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def edit_title(title,id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("UPDATE todo SET title=? WHERE id=?", (title,id))
    conn.commit()
    conn.close()

def edit_task(task,id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("UPDATE todo SET task=? WHERE id=?", (task,id))
    conn.commit()
    conn.close()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def delete_all():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("DELETE FROM todo")
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("DELETE FROM todo WHERE id=?", (str(id)))
    conn.commit()
    conn.close()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def done(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("UPDATE todo SET done=? WHERE id=?", (True,id))
    conn.commit()
    conn.close()

def undone(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("UPDATE todo SET done=? WHERE id=?", (False,id))
    conn.commit()
    conn.close()

connect()