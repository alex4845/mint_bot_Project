import sqlite3
from datetime import datetime

async def telegramm_base(state):
    async with state.proxy() as data:
        conn = sqlite3.connect('tele_table_mint.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS list_1
               (number INTEGER PRIMARY KEY, name TEXT (30), insta TEXT (50),
               username TEXT (30), user_id INTEGER (20), sex TEXT (10), qr BLOB)""")
        cursor.execute('INSERT INTO list_1 (name, insta, username, user_id, sex, qr) VALUES (?,?,?,?,?,?)',
                       (data['name'], data['insta'], data['username'], data['user_id'], data['sex'], data['qr']))
        conn.commit()
        conn.close()

async def get_info():
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT number, name, insta, username, user_id, sex FROM list_1")
    res = cursor.fetchall()
    list = []
    for i in res:
        a = str(i)
        list.append(a[1:-1])
    conn.close()
    return list

async def get_user(a):
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_1 WHERE user_id = ?", (a,))
    res = cursor.fetchone()
    conn.close()
    return res

async def del_user(a):
    conn = sqlite3.connect('tele_table_mint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_1 WHERE user_id = ?", (a,))
    res = cursor.fetchone()
    if res is not None:
        record_id = res[0]
        cursor.execute("DELETE FROM list_1 WHERE number = ?", (record_id,))
        conn.commit()
        b = f"Пользователь {res[1]} удален"
    else:
        b = "Пользователь не найден в базе данных"
    conn.close()
    return b

async def act_user(b):
    tims = datetime.now()
    sur = '---'
    conn = sqlite3.connect('table_mint_2.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_2
                      (number INTEGER PRIMARY KEY, name TEXT (30), username TEXT (30), user_id INTEGER (20), 
                      sex TEXT (10), time DATETIME, sur TEXT (3))""")
    cursor.execute('INSERT INTO list_2 (name, username, user_id, sex, time, sur) VALUES (?,?,?,?,?,?)',
                   (b[1], b[3], b[4], b[5], tims, sur))
    conn.commit()
    b = f'Пользователь {b[1]} активирован'
    conn.close()
    return b

async def get_info_act():
    conn = sqlite3.connect('table_mint_2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT number, name, username, user_id, sex, time, sur FROM list_2")
    res = cursor.fetchall()
    list = []
    for i in res:
        a = str(i)
        list.append(a)
    conn.close()
    return list

async def interval():
    l = []
    conn = sqlite3.connect('table_mint_2.db')
    cursor = conn.cursor()
    t_n = datetime.now()
    current_time = datetime.now().replace(hour=22, minute=10, second=0)
    if t_n > current_time:
        cursor.execute("DELETE FROM list_2")
        conn.commit()
        conn.close()
    else:
        cursor.execute("SELECT time, number, user_id FROM list_2 WHERE sur = ?", ("---",))
        res = cursor.fetchall()
        if res:
            for i in res:
                time_1 = datetime.strptime(str(i[0]), "%Y-%m-%d %H:%M:%S.%f")
                diff_minutes = t_n - time_1
                minutes = diff_minutes.total_seconds() // 60
                if minutes > 1:
                    cursor.execute("UPDATE list_2 SET sur = ? WHERE number = ?", ('+', i[1]))
                    l.append(i[2])
                conn.commit()
            conn.close()
            return l

async def get_user_act(a):
    conn = sqlite3.connect('table_mint_2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_2 WHERE user_id = ?", (a,))
    res = cursor.fetchone()
    conn.close()
    return res

async def get_sur(b):
    tims = datetime.now()
    conn = sqlite3.connect('table_mint_2.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE list_2 SET sur = ? WHERE number = ?", ('---', b[0]))
    cursor.execute("UPDATE list_2 SET time = ? WHERE number = ?", (tims, b[0]))
    conn.commit()
    conn.close()
    res = "Угощение получено"
    return res