import psycopg2

# conn = psycopg2.connect(host='141.8.199.12', port=5432, user='postgres',
#                         password='20rasputin23', database='rasputin_base.db')
# cursor = conn.cursor()
#data = 469632258
# cursor.execute("DROP TABLE list_2;")
# conn.commit()

conn = psycopg2.connect(host='141.8.199.12', port=5432, user='postgres',
                        password='20rasputin23', database='rasputin_base.db')
cursor = conn.cursor()



cursor.execute("DELETE FROM list_1")
conn.commit()
cursor.execute("SELECT * FROM list_1")
res = cursor.fetchone()
conn.close()
print(res)