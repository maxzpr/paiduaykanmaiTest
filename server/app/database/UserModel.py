import sqlite3


def query(sqlString, params=None, returnType='result'):
    con = sqlite3.connect('app/database/user.db')
    cur = con.cursor()
    if params:
        cur.execute(sqlString, params)
    else:
        cur.execute(sqlString)
    con.commit()
    return cur


def getColumn():
    q = query("SELECT id,first_name,last_name,email,gender,age FROM users")
    columns = list(map(lambda x: x[0], q.description))
    return columns


def getUserList(page=1, limit=50):
    offset = (page-1) * limit
    q = query(f"""SELECT id,first_name,last_name,email,gender,age 
    FROM users
    LIMIT {offset},{limit}
    """)
    return q.fetchall()

def searchUserList(whereMap):
    q = query(f"""SELECT id,first_name,last_name,email,gender,age 
    FROM users
    WHERE {whereMap}
    """)
    return q.fetchall()


def createUser(data):
    q = query(f"""INSERT INTO users(first_name,last_name,email,gender,age)
    VALUES(?,?,?,?,?)
    """, (data['first_name'], data['last_name'], data['email'], data['gender'], data['age']) )
    return q

def editUser(data):
    q = query(f"""UPDATE users SET
    first_name=?,last_name=?,email=?,gender=?,age=?
    WHERE id=?
    """, (data['first_name'], data['last_name'], data['email'], data['gender'], data['age'],data['id']) )
    return q

def delUser(data):
    q = query(f"""DELETE FROM users WHERE id=?""", (str(data['id']) ) )
    return q
