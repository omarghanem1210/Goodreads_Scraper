import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root',
                       passwd='6456456456456456-*-*/hfd -*-/*-gd*//>?[gdfg', db='mysql')

cur = conn.cursor()
cur.execute('USE goodreads')
cur.execute('DESCRIBE books;')

print(cur.fetchall())
cur.close()
conn.close()
